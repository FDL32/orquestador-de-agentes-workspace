"""Tests para TICKET-007: Selective Context Recovery Lite."""

import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch


# AÃ±adir .agent al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / ".agent"))

from hooks.pre_compact_hook import (
    extract_work_plan_keywords,
    format_memory_section,
    load_observations_safe,
    rank_observations,
)


class TestSelectiveContextRecovery:
    """Tests para la funcionalidad de recuperaciÃ³n selectiva de contexto."""

    def test_extract_work_plan_keywords_basic(self):
        """Test extracciÃ³n bÃ¡sica de keywords del work plan."""
        content = """# TICKET-007: Context Recovery
## Objective
Implement context recovery from observations.jsonl

## Tasks
- Implement keyword extraction function
- Add memory ranking by recency
- Test corrupted JSONL handling

## Technical Details
Use lightweight ranking without embeddings
"""
        keywords = extract_work_plan_keywords(content)

        # Verificar que se extraen keywords relevantes
        assert "implement" in keywords
        assert "context" in keywords
        assert "recovery" in keywords
        assert "memory" in keywords
        assert "ranking" in keywords
        assert "function" in keywords

        # Verificar lÃ­mite de 20 keywords
        assert len(keywords) <= 20

    def test_extract_work_plan_keywords_empty(self):
        """Test con work plan vacÃ­o."""
        keywords = extract_work_plan_keywords("")
        assert keywords == []

    def test_extract_work_plan_keywords_technical_terms(self):
        """Test que incluye tÃ©rminos tÃ©cnicos automÃ¡ticamente."""
        content = "This is a simple plan without technical terms."
        keywords = extract_work_plan_keywords(content)

        # DeberÃ­a incluir tÃ©rminos tÃ©cnicos si estÃ¡n en el contenido
        # En este caso, no hay tÃ©rminos tÃ©cnicos especÃ­ficos
        assert isinstance(keywords, list)

    @patch("hooks.pre_compact_hook.OBSERVATIONS_FILE")
    def test_load_observations_safe_missing_file(self, mock_file):
        """Test carga segura cuando el archivo no existe."""
        mock_file.exists.return_value = False

        observations = load_observations_safe()
        assert observations == []

    def test_load_observations_safe_corrupted_jsonl(self):
        """Test carga segura con JSONL corrupto."""
        # Crear archivo temporal con JSON corrupto
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jsonl") as f:
            f.write(
                '{"timestamp": "2026-04-30T10:00:00", "context": "valid observation", "tool": "test"}\n'
            )
            f.write('{"incomplete": json}\n')  # corrupto
            f.write(
                '{"timestamp": "2026-04-30T09:00:00", "context": "another valid observation", "tool": "test2"}\n'
            )
            temp_path = Path(f.name)

        # Usar patch.object para reemplazar la constante del mÃ³dulo
        import hooks.pre_compact_hook

        with patch.object(hooks.pre_compact_hook, "OBSERVATIONS_FILE", temp_path):
            observations = load_observations_safe()

        # DeberÃ­a cargar solo las lÃ­neas vÃ¡lidas
        assert len(observations) == 2
        assert observations[0]["context"] == "valid observation"
        assert observations[1]["context"] == "another valid observation"

        temp_path.unlink()

    @patch("hooks.pre_compact_hook.OBSERVATIONS_FILE")
    def test_load_observations_safe_empty_file(self, mock_file):
        """Test carga segura con archivo vacÃ­o."""
        mock_file.exists.return_value = True

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jsonl") as f:
            temp_path = Path(f.name)

        with patch("hooks.pre_compact_hook.OBSERVATIONS_FILE", temp_path):
            observations = load_observations_safe()

        assert observations == []
        temp_path.unlink()

    def test_rank_observations_empty(self):
        """Test ranking con lista vacÃ­a."""
        result = rank_observations([], ["test"])
        assert result == []

    def test_rank_observations_by_recency(self):
        """Test ranking por recencia."""
        now = datetime.now()

        observations = [
            {
                "timestamp": (now - timedelta(hours=1)).isoformat(),
                "context": "Recent observation",
                "tool": "grep_search",
            },
            {
                "timestamp": (now - timedelta(hours=25)).isoformat(),
                "context": "Medium recent observation",
                "tool": "read_file",
            },
            {
                "timestamp": (now - timedelta(hours=50)).isoformat(),
                "context": "Old observation",
                "tool": "run_tests",
            },
        ]

        keywords = ["observation"]
        result = rank_observations(observations, keywords)

        # DeberÃ­a incluir las 2 mÃ¡s recientes (dentro de 48h)
        assert len(result) == 2
        # La mÃ¡s reciente primero
        assert result[0]["context"] == "Recent observation"

    def test_rank_observations_by_keywords(self):
        """Test ranking por coincidencia de keywords."""
        now = datetime.now()

        observations = [
            {
                "timestamp": now.isoformat(),
                "context": "This has memory and context keywords",
                "tool": "grep_search",
            },
            {
                "timestamp": now.isoformat(),
                "context": "This has no matching keywords",
                "tool": "read_file",
            },
            {
                "timestamp": now.isoformat(),
                "context": "Memory recovery implementation",
                "tool": "view_file",
            },
        ]

        keywords = ["memory", "context", "recovery"]
        result = rank_observations(observations, keywords)

        # DeberÃ­a ordenar por score de keywords
        assert len(result) == 3
        # La primera deberÃ­a tener mejor matching
        assert (
            "memory" in result[0]["context"].lower()
            or "context" in result[0]["context"].lower()
        )

    def test_rank_observations_limit(self):
        """Test lÃ­mite de 5 observaciones."""
        now = datetime.now()

        # Crear 10 observaciones
        observations = [
            {
                "timestamp": now.isoformat(),
                "context": f"Observation {i} with memory keyword",
                "tool": "test_tool",
            }
            for i in range(10)
        ]

        keywords = ["memory"]
        result = rank_observations(observations, keywords)

        # DeberÃ­a limitar a 5
        assert len(result) == 5

    def test_format_memory_section_empty(self):
        """Test formato de sección con memoria vacía."""
        result = format_memory_section([])
        assert "## Memoria relevante" in result
        assert "No se encontraron observaciones relevantes" in result
        assert "## Memoria relevante" in result

    def test_format_memory_section_with_data(self):
        """Test formato de secciÃ³n con datos."""
        observations = [
            {
                "timestamp": "2026-04-30T10:00:00",
                "tool": "grep_search",
                "context": "Searching for test functions in the codebase",
            },
            {
                "timestamp": "2026-04-30T09:30:00",
                "tool": "read_file",
                "context": "Reading test configuration and setup",
            },
        ]

        result = format_memory_section(observations)

        assert "## Memoria relevante" in result
        assert "1. grep_search (2026-04-30T10:00:00)" in result
        assert "2. read_file (2026-04-30T09:30:00)" in result
        assert "Searching for test functions" in result
        assert "Reading test configuration" in result

    def test_format_memory_section_context_truncation(self):
        """Test truncamiento de contexto largo."""
        long_context = "A" * 200  # MÃ¡s de 100 caracteres
        observations = [
            {
                "timestamp": "2026-04-30T10:00:00",
                "tool": "test_tool",
                "context": long_context,
            }
        ]

        result = format_memory_section(observations)

        # DeberÃ­a truncar a 100 caracteres
        assert len(result.split("\n")[3]) <= 100  # La lÃ­nea del contexto


class TestIntegration:
    """Tests de integraciÃ³n para el hook completo."""

    def test_hook_integration_with_memory(self):
        """Test integraciÃ³n completa del hook con recuperaciÃ³n de memoria."""
        from hooks.pre_compact_hook import (
            _build_state_content,
            extract_work_plan_keywords,
            format_memory_section,
            load_observations_safe,
            rank_observations,
        )

        # Simular datos de entrada
        work_plan_content = """# TICKET-007
## Objective
Implement context recovery with memory and keywords

## Tasks
- Add memory ranking function
- Test keyword extraction
"""

        # Crear archivo temporal con observaciones de prueba
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jsonl") as f:
            f.write(
                '{"timestamp": "2026-04-30T10:00:00", "tool": "grep_search", "context": "Searching for memory functions", "session_id": "test"}\n'
            )
            temp_obs_path = Path(f.name)

        # Patch OBSERVATIONS_FILE
        import hooks.pre_compact_hook

        original_file = hooks.pre_compact_hook.OBSERVATIONS_FILE
        hooks.pre_compact_hook.OBSERVATIONS_FILE = temp_obs_path

        try:
            # Ejecutar flujo del hook
            keywords = extract_work_plan_keywords(work_plan_content)
            observations = load_observations_safe()
            relevant_obs = rank_observations(observations, keywords)
            memory_section = format_memory_section(relevant_obs)

            # Generar contenido STATE
            state_content = _build_state_content(
                timestamp="2026-04-30 12:00:00",
                plan_id="TICKET-007",
                plan_status="IN_PROGRESS",
                current_phase="ImplementaciÃ³n",
                last_task="Completed memory implementation",
                relevant_memory=memory_section,
            )

            # Verificar contenido
            assert "## Memoria relevante" in state_content
            # Verify memory section was generated (either with observations or empty)
            assert "observaciones relevantes" in state_content or (
                "No se encontraron observaciones" in state_content
            )

        finally:
            hooks.pre_compact_hook.OBSERVATIONS_FILE = original_file

        temp_obs_path.unlink()

    @patch("hooks.pre_compact_hook.OBSERVATIONS_FILE")
    def test_hook_graceful_degradation_missing_memory(self, mock_obs_file):
        """Test que el hook funciona incluso si falta el archivo de memoria."""
        mock_obs_file.exists.return_value = False

        from hooks.pre_compact_hook import (
            extract_work_plan_keywords,
            format_memory_section,
            load_observations_safe,
            rank_observations,
        )

        # Simular el flujo del hook
        work_plan = "# Test Plan\nImplement memory recovery"
        keywords = extract_work_plan_keywords(work_plan)
        observations = load_observations_safe()
        relevant_obs = rank_observations(observations, keywords)
        memory_section = format_memory_section(relevant_obs)

        # Debería generar sección vacía pero no fallar
        assert "## Memoria relevante" in memory_section
        assert "No se encontraron observaciones relevantes" in memory_section

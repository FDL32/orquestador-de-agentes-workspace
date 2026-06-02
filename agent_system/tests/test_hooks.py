"""Tests para el sistema de hooks.

Ejecutar:
    python scripts/run_pytest_safe.py -- tests/test_hooks.py -v
    python scripts/run_pytest_safe.py -- tests/test_hooks.py -v -k test_name
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.filterwarnings("ignore")

# AÃ±adir .agent al path para imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / ".agent"))

from hooks import HookRegistry
from hooks.pre_action_hook import (
    pre_action_hook,
    extract_plan_id,
    extract_objective,
    extract_current_phase
)
from hooks.post_tool_hook import (
    reset_counter,
    load_counter,
    save_counter,
    READ_TOOLS
)
from hooks.stop_hook import (
    stop_hook,
    check_all_phases_complete
)


class TestHookRegistry:
    """Tests para la clase HookRegistry."""
    
    def test_init_creates_empty_registry(self):
        """Test que el registro se inicializa vacÃ­o."""
        registry = HookRegistry()
        assert registry._hooks == {
            "pre_action": [],
            "post_tool": [],
            "stop": []
        }
    
    def test_register_adds_hook(self):
        """Test que register aÃ±ade un hook correctamente."""
        registry = HookRegistry()
        
        def dummy_hook(context):
            pass
        
        registry.register("pre_action", dummy_hook)
        assert len(registry._hooks["pre_action"]) == 1
        assert registry._hooks["pre_action"][0] == dummy_hook
    
    def test_register_invalid_type_raises_error(self):
        """Test que register lanza error con tipo invÃ¡lido."""
        registry = HookRegistry()
        
        def dummy_hook(context):
            pass
        
        with pytest.raises(ValueError, match="Tipo de hook 'invalid' no vÃ¡lido"):
            registry.register("invalid", dummy_hook)
    
    def test_execute_calls_hooks(self):
        """Test que execute llama a los hooks registrados."""
        registry = HookRegistry()
        
        called = []
        def hook1(context):
            called.append("hook1")
        def hook2(context):
            called.append("hook2")
        
        registry.register("pre_action", hook1)
        registry.register("pre_action", hook2)
        
        registry.execute("pre_action", {"test": True})
        
        assert "hook1" in called
        assert "hook2" in called
    
    def test_execute_handles_errors_gracefully(self):
        """Test que execute maneja errores sin detenerse."""
        registry = HookRegistry()
        
        def failing_hook(context):
            raise ValueError("Test error")
        
        def working_hook(context):
            context["worked"] = True
        
        registry.register("pre_action", failing_hook)
        registry.register("pre_action", working_hook)
        
        context = {}
        # No debe lanzar excepciÃ³n
        registry.execute("pre_action", context)
        
        # El segundo hook debe haberse ejecutado
        assert context.get("worked") is True
    
    def test_get_registered_hooks(self):
        """Test que get_registered_hooks retorna nombres correctos."""
        registry = HookRegistry()
        
        def my_hook(context):
            pass
        
        registry.register("pre_action", my_hook)
        
        names = registry.get_registered_hooks("pre_action")
        assert "my_hook" in names


class TestPreActionHook:
    """Tests para pre_action_hook."""
    
    def test_extract_plan_id_finds_id(self):
        """Test que extract_plan_id encuentra el ID correctamente."""
        content = "# Plan\n\n**ID:** WP-2026-001\n"
        result = extract_plan_id(content)
        assert result == "WP-2026-001"
    
    def test_extract_plan_id_returns_none_if_not_found(self):
        """Test que extract_plan_id retorna None si no encuentra ID."""
        content = "# Plan sin ID"
        result = extract_plan_id(content)
        assert result is None
    
    def test_extract_objective_finds_objective(self):
        """Test que extract_objective encuentra el objetivo."""
        content = "## ðŸŽ¯ Objetivo\n\nCrear sistema de hooks.\n"
        result = extract_objective(content)
        assert "Crear sistema de hooks" in result
    
    def test_extract_objective_limits_length(self):
        """Test que extract_objective limita a 80 caracteres."""
        content = "## ðŸŽ¯ Objetivo\n\n" + "A" * 100 + "\n"
        result = extract_objective(content)
        assert len(result) <= 80
        assert "..." in result
    
    def test_extract_current_phase_finds_pending_tasks(self):
        """Test que extract_current_phase encuentra fase con tareas."""
        content = """
### Fase 1: Setup
- [x] Tarea completada
- [ ] Tarea pendiente
"""
        result = extract_current_phase(content)
        assert "Fase 1" in result
        assert "tareas pendientes" in result
    
    def test_extract_current_phase_all_completed(self):
        """Test que extract_current_phase detecta cuando todo estÃ¡ completo."""
        content = """
### Fase 1
- [x] Tarea 1
- [x] Tarea 2
"""
        result = extract_current_phase(content)
        assert "Todas las fases completadas" in result


class TestPostToolHook:
    """Tests para post_tool_hook (2-Action Rule)."""
    
    def test_read_tools_defined(self):
        """Test que READ_TOOLS contiene herramientas de lectura."""
        assert "view_file" in READ_TOOLS
        assert "grep_search" in READ_TOOLS
        assert "read_file" in READ_TOOLS
    
    def test_load_counter_returns_default_if_not_exists(self, tmp_path):
        """Test que load_counter retorna valores por defecto."""
        with patch('hooks.post_tool_hook.COUNTER_FILE', tmp_path / "counter.json"):
            result = load_counter()
            assert result["count"] == 0
            assert result["last_tool"] is None
    
    def test_save_counter_creates_file(self, tmp_path):
        """Test que save_counter crea el archivo correctamente."""
        counter_file = tmp_path / "counter.json"
        with patch('hooks.post_tool_hook.COUNTER_FILE', counter_file):
            save_counter({"count": 2, "last_tool": "view_file"})
            
            assert counter_file.exists()
            data = json.loads(counter_file.read_text(encoding="utf-8"))
            assert data["count"] == 2
            assert data["last_tool"] == "view_file"
    
    def test_reset_counter_sets_zero(self, tmp_path):
        """Test que reset_counter pone el contador a cero."""
        counter_file = tmp_path / "counter.json"
        with patch('hooks.post_tool_hook.COUNTER_FILE', counter_file):
            # Primero guardar un valor
            save_counter({"count": 5, "last_tool": "test"})
            
            # Resetear
            reset_counter()
            
            # Verificar
            result = load_counter()
            assert result["count"] == 0
            assert result["last_tool"] is None


class TestStopHook:
    """Tests para stop_hook."""
    
    def test_stop_hook_disabled_mode(self):
        """Test que modo disabled permite siempre."""
        result = stop_hook({"plan_status": "COMPLETED", "mode": "disabled"})
        assert result["can_complete"] is True
        assert result["warnings"] == []
    
    @patch('hooks.stop_hook.check_tests_passing', return_value=True)
    def test_stop_hook_not_completed_status(self, mock_tests):
        """Test que no verifica si no es COMPLETED."""
        result = stop_hook({"plan_status": "IN_PROGRESS", "mode": "normal"})
        assert result["can_complete"] is True
    
    def test_check_all_phases_complete_no_pending(self, tmp_path):
        """Test que detecta cuando no hay tareas pendientes."""
        work_plan = tmp_path / "work_plan.md"
        work_plan.write_text("- [x] Tarea 1\n- [x] Tarea 2\n", encoding="utf-8")
        
        with patch('hooks.stop_hook.WORK_PLAN', work_plan):
            result = check_all_phases_complete()
            assert result is True
    
    def test_check_all_phases_complete_with_pending(self, tmp_path):
        """Test que detecta cuando hay tareas pendientes."""
        work_plan = tmp_path / "work_plan.md"
        work_plan.write_text("- [x] Tarea 1\n- [ ] Tarea 2\n", encoding="utf-8")
        
        with patch('hooks.stop_hook.WORK_PLAN', work_plan):
            result = check_all_phases_complete()
            assert result is False


class TestIntegration:
    """Tests de integraciÃ³n."""
    
    def test_full_hook_workflow(self):
        """Test del flujo completo de hooks."""
        registry = HookRegistry()
        
        # Pre-action hook
        pre_action_calls = []
        def mock_pre_action(context):
            pre_action_calls.append(context.get("action_type"))
        
        registry.register("pre_action", mock_pre_action)
        
        # Ejecutar
        registry.execute("pre_action", {"action_type": "TEST"})
        
        assert "TEST" in pre_action_calls
    
    def test_hooks_handle_missing_files(self, tmp_path):
        """Test que los hooks manejan archivos faltantes sin fallar."""
        # Pre-action hook sin work_plan.md
        with patch('hooks.pre_action_hook.WORK_PLAN', tmp_path / "no_existe.md"):
            # No debe lanzar excepciÃ³n
            pre_action_hook({"action_type": "IMPLEMENT"})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


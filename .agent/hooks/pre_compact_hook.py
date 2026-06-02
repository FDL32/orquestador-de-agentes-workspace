#!/usr/bin/env python3
"""Hook PreCompact (Claude Code): guarda estado antes de compactar contexto.

TICKET-007: Selective Context Recovery Lite
- Recupera contexto relevante de observations.jsonl usando recencia + keywords
- Añade sección "Memoria relevante" a STATE.md
- No bloqueante, sin dependencias pesadas
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

AGENT_DIR = Path(__file__).resolve().parent.parent
COLLAB_DIR = AGENT_DIR / "collaboration"
MEMORY_DIR = AGENT_DIR / "runtime" / "memory"
WORK_PLAN = COLLAB_DIR / "work_plan.md"
EXEC_LOG = COLLAB_DIR / "execution_log.md"
OBSERVATIONS_FILE = MEMORY_DIR / "observations.jsonl"
STATE_FILE = COLLAB_DIR / "STATE.md"


def _load_payload() -> dict:
    """Lee el payload JSON desde stdin. Si no existe, devuelve dict vacio."""
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_field(content: str, markers: tuple[str, ...]) -> str:
    for line in content.splitlines():
        for marker in markers:
            if marker in line:
                return line.split(marker, 1)[1].strip()
    return "N/A"


def _extract_current_phase(content: str) -> str:
    current_phase = "Sin fases detectadas"
    in_phase = False
    has_any_checkbox = False
    last_section = ""

    for line in content.splitlines():
        if "- [ ]" in line or "- [x]" in line or "- [X]" in line:
            has_any_checkbox = True

        if line.startswith("### Fase") or line.startswith("## Fase"):
            current_phase = line.replace("###", "").replace("##", "").strip()
            last_section = current_phase
            in_phase = True
            continue
        elif line.startswith("#### "):
            last_section = line.replace("####", "").strip()

        if in_phase and "- [ ]" in line:
            return current_phase

        if in_phase and line.startswith("## ") and "Fase" not in line:
            in_phase = False

    if not has_any_checkbox and last_section:
        return f"{last_section} (fase activa - plan narrativo)"

    return (
        current_phase
        if current_phase != "Sin fases detectadas"
        else "Todas las fases completadas"
    )


def _extract_last_logged_task(content: str) -> str:
    for line in reversed(content.splitlines()):
        stripped = line.strip()
        if stripped.startswith("### "):
            return stripped.removeprefix("### ").strip()
    return "Sin tareas documentadas"


# TICKET-007: Selective Context Recovery Lite
def extract_work_plan_keywords(content: str) -> List[str]:
    """Extrae palabras clave relevantes del work plan para matching.

    Busca títulos de tareas, fases, objetivos y términos técnicos.
    """
    keywords = set()

    # Buscar títulos de secciones y tareas
    for line in content.splitlines():
        line = line.strip()
        # Headers principales
        if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
            # Extraer palabras clave del título
            title = re.sub(r"^#+\s*", "", line)
            words = re.findall(r"\b\w{4,}\b", title.lower())
            keywords.update(words)
        # Items de lista (tareas)
        elif line.startswith("- ") and any(
            term in line.lower()
            for term in ["implement", "create", "add", "update", "test"]
        ):
            words = re.findall(r"\b\w{4,}\b", line.lower())
            keywords.update(words)

    # Palabras clave específicas del contexto técnico
    technical_terms = [
        "test",
        "function",
        "class",
        "module",
        "script",
        "hook",
        "memory",
        "context",
        "recovery",
    ]
    keywords.update(term for term in technical_terms if term in content.lower())

    return list(keywords)[:20]  # Limitar a 20 keywords max


def load_observations_safe() -> List[Dict[str, Any]]:
    """Carga observaciones de forma segura, manejando archivos corruptos o ausentes."""
    if not OBSERVATIONS_FILE.exists():
        return []

    observations = []
    try:
        with open(OBSERVATIONS_FILE, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obs = json.loads(line)
                    # Validar estructura mínima
                    if (
                        isinstance(obs, dict)
                        and "timestamp" in obs
                        and "context" in obs
                    ):
                        observations.append(obs)
                except json.JSONDecodeError:
                    # Saltar líneas corruptas silenciosamente
                    continue
    except (OSError, IOError):
        # Archivo no accesible - devolver lista vacía
        return []

    return observations


def rank_observations(
    observations: List[Dict[str, Any]], keywords: List[str], max_hours: int = 48
) -> List[Dict[str, Any]]:
    """Rankea observaciones por recencia + coincidencia de keywords."""
    if not observations:
        return []

    now = datetime.now()
    cutoff = now - timedelta(hours=max_hours)

    scored_obs = []
    for obs in observations:
        try:
            # Parsear timestamp
            obs_time = datetime.fromisoformat(obs["timestamp"].replace("Z", "+00:00"))
            if obs_time < cutoff:
                continue

            # Calcular score de recencia (0-1, más reciente = mayor score)
            hours_old = (now - obs_time).total_seconds() / 3600
            recency_score = max(0, 1 - (hours_old / max_hours))

            # Calcular score de keyword matching
            context_lower = obs.get("context", "").lower()
            keyword_matches = sum(1 for kw in keywords if kw.lower() in context_lower)
            keyword_score = min(1.0, keyword_matches / max(1, len(keywords)))

            # Score total: 70% recencia + 30% keywords
            total_score = (recency_score * 0.7) + (keyword_score * 0.3)

            scored_obs.append(
                {
                    "observation": obs,
                    "score": total_score,
                    "recency_score": recency_score,
                    "keyword_score": keyword_score,
                }
            )

        except (ValueError, KeyError):
            # Saltar observaciones con timestamps inválidos
            continue

    # Ordenar por score descendente y tomar top 5
    scored_obs.sort(key=lambda x: x["score"], reverse=True)
    return [item["observation"] for item in scored_obs[:5]]


def format_memory_section(relevant_observations: List[Dict[str, Any]]) -> str:
    """Formatea la sección 'Memoria relevante' para STATE.md."""
    if not relevant_observations:
        return """## Memoria relevante

*No se encontraron observaciones relevantes en las últimas 48 horas.*

---
"""

    lines = ["## Memoria relevante", ""]

    for i, obs in enumerate(relevant_observations, 1):
        timestamp = obs.get("timestamp", "N/A")
        tool = obs.get("tool", "N/A")
        context = obs.get("context", "N/A")[:100]  # Limitar longitud

        lines.append(f"### {i}. {tool} ({timestamp[:19]})")
        lines.append(f"{context}")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)


def _build_state_content(
    *,
    timestamp: str,
    plan_id: str,
    plan_status: str,
    current_phase: str,
    last_task: str,
    relevant_memory: str = "",
) -> str:
    next_step = (
        "Retomar la primera tarea pendiente de la fase actual."
        if "Todas las fases completadas" not in current_phase
        else "Revisar el cierre del plan o preparar el siguiente trabajo."
    )

    # Insertar sección de memoria relevante antes del contexto para próxima sesión
    memory_section = (
        relevant_memory
        or """## Memoria relevante

*No se encontraron observaciones relevantes en las últimas 48 horas.*

---
"""
    )

    return f"""# STATE — Snapshot Operativo

> Estado generado automáticamente por `pre_compact_hook.py` antes de compactar
> contexto.

**Actualizado:** {timestamp}

---

## Plan activo

- **ID:** {plan_id}
- **Estado actual:** {plan_status}
- **Fase actual:** {current_phase}

---

## Último progreso documentado

- **Último task en execution_log.md:** {last_task}

---

{memory_section}

## Contexto para la próxima sesión

- **Próximo paso recomendado:** {next_step}
- **Archivos que mirar primero:** `work_plan.md`, `execution_log.md`, `STATE.md`
- **Notas:** Reanudar desde este snapshot antes de seguir editando.
"""


def main() -> int:
    """Genera un snapshot del estado sin bloquear la compactación."""
    try:
        _load_payload()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plan_content = _read_text(WORK_PLAN)
        log_content = _read_text(EXEC_LOG)

        plan_id = _extract_field(
            plan_content, ("- ID:", "- plan ID:", "**ID:**", "**Plan ID:**")
        )
        plan_status = _extract_field(
            plan_content, ("- State:", "- Estado:", "**Estado:**")
        )
        current_phase = _extract_current_phase(plan_content)
        last_task = _extract_last_logged_task(log_content)

        # TICKET-007: Recuperar contexto relevante
        work_plan_keywords = extract_work_plan_keywords(plan_content)
        observations = load_observations_safe()
        relevant_observations = rank_observations(observations, work_plan_keywords)
        memory_section = format_memory_section(relevant_observations)

        STATE_FILE.write_text(
            _build_state_content(
                timestamp=timestamp,
                plan_id=plan_id,
                plan_status=plan_status,
                current_phase=current_phase,
                last_task=last_task,
                relevant_memory=memory_section,
            ),
            encoding="utf-8",
        )

        print(
            "[PreCompact] STATE.md actualizado | "
            f"Plan: {plan_id} | Estado: {plan_status} | Fase: {current_phase} | "
            f"Memoria: {len(relevant_observations)} observaciones"
        )
    except Exception as exc:  # pragma: no cover - hook informativo
        print(f"[PreCompact] No se pudo actualizar STATE.md: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

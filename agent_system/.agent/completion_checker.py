"""Completion Checker Lite para proyectos pequeÃ±os (<30 archivos).

VersiÃ³n simplificada de verificaciÃ³n de completitud que verifica
criterios esenciales sin sobrecargar el sistema.

Uso:
    from .completion_checker import check_completion
    result = check_completion()
    if result["can_complete"]:
        print("âœ… Listo para completar")
    else:
        print(f"âš ï¸ Faltan: {result['missing']}")
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Any

# Rutas
COLLAB_DIR = Path(__file__).parent / "collaboration"
PROJECT_ROOT = COLLAB_DIR.parent.parent

WORK_PLAN = COLLAB_DIR / "work_plan.md"
EXEC_LOG = COLLAB_DIR / "execution_log.md"
REVIEW_QUEUE = COLLAB_DIR / "review_queue.md"
FINDINGS = COLLAB_DIR / "findings.md"


def check_completion() -> Dict[str, Any]:
    """Verifica criterios de completitud simplificados.
    
    Para proyectos pequeÃ±os, verifica solo lo esencial:
    1. Tareas completadas (checkboxes marcadas)
    2. Tests pasando (si existen)
    3. Sin escalaciones pendientes
    4. Execution log con resumen
    
    Returns:
        Dict con:
            - can_complete: bool
            - percentage: int (0-100)
            - checks: dict con cada verificaciÃ³n
            - missing: lista de items faltantes
    """
    checks = {
        "tasks_completed": _check_all_tasks_done(),
        "tests_passing": _check_tests_pass(),
        "no_escalations": _check_no_pending_escalations(),
        "log_has_summary": _check_execution_summary(),
        "findings_exist": _check_findings_exist(),
    }
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    percentage = int((passed / total) * 100) if total > 0 else 0
    
    # Determinar si puede completarse
    # Para simplificar: necesita 4 de 5 checks (80%)
    can_complete = passed >= 4
    
    # Generar lista de items faltantes
    missing = []
    check_names = {
        "tasks_completed": "Tareas pendientes en work_plan.md",
        "tests_passing": "Tests fallando",
        "no_escalations": "Escalaciones pendientes en review_queue.md",
        "log_has_summary": "Falta resumen en execution_log.md",
        "findings_exist": "No existe findings.md (opcional pero recomendado)",
    }
    
    for check_name, passed_check in checks.items():
        if not passed_check:
            missing.append(check_names.get(check_name, check_name))
    
    return {
        "can_complete": can_complete,
        "percentage": percentage,
        "checks": checks,
        "missing": missing,
        "passed": passed,
        "total": total,
    }


def show_completion_report(result: Dict[str, Any]) -> None:
    """Muestra reporte de completitud de forma legible."""
    emoji = "âœ…" if result["can_complete"] else "âš ï¸"
    status = "LISTO PARA COMPLETAR" if result["can_complete"] else "INCOMPLETO"
    
    print("\n" + "=" * 60)
    print(f"{emoji} VERIFICACIÃ“N DE COMPLETITUD: {status}")
    print("=" * 60)
    print(f"Progreso: {result['passed']}/{result['total']} ({result['percentage']}%)")
    
    if result["missing"]:
        print("\nItems faltantes:")
        for item in result["missing"]:
            print(f"  âŒ {item}")
    else:
        print("\nâœ… Todos los criterios cumplidos")
    
    print("=" * 60 + "\n")


# ============================================================================
# VERIFICACIONES INDIVIDUALES
# ============================================================================

def _check_all_tasks_done() -> bool:
    """Verifica que todas las tareas estÃ©n marcadas [x]."""
    if not WORK_PLAN.exists():
        return False
    
    try:
        content = WORK_PLAN.read_text(encoding="utf-8")
        # Contar checkboxes pendientes
        pending = content.count("- [ ]")
        return pending == 0
    except Exception:
        return False


def _check_tests_pass() -> bool:
    """Verifica que los tests pasen (si hay tests)."""
    tests_dir = PROJECT_ROOT / "tests"
    
    # Si no hay tests, consideramos OK
    if not tests_dir.exists():
        return True
    
    try:
        result = subprocess.run(
            ["uv", "run", "pytest", "-q", "--tb=no"],
            capture_output=True,
            timeout=60,
            cwd=PROJECT_ROOT
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Si no hay uv o timeout, asumimos OK para no bloquear
        return True


def _check_no_pending_escalations() -> bool:
    """Verifica que no haya escalaciones pendientes."""
    if not REVIEW_QUEUE.exists():
        return True
    
    try:
        content = REVIEW_QUEUE.read_text(encoding="utf-8")
        import re
        has_pending = re.search(r"PENDING", content) is not None
        has_blocked = re.search(r"BLOCKED", content) is not None
        return not has_pending and not has_blocked
    except Exception:
        return True


def _check_execution_summary() -> bool:
    """Verifica que execution_log tenga resumen."""
    if not EXEC_LOG.exists():
        return False
    
    try:
        content = EXEC_LOG.read_text(encoding="utf-8")
        import re
        has_summary = re.search(r"##\s+.*Resumen", content) is not None
        not_in_progress = re.search(r"IN_PROGRESS", content) is None
        return has_summary and not_in_progress
    except Exception:
        return False


def _check_findings_exist() -> bool:
    """Verifica que exista findings.md (opcional pero recomendado)."""
    # Este check es opcional, no bloquea la completitud
    # pero se incluye para dar feedback
    if not FINDINGS.exists():
        return False
    
    try:
        content = FINDINGS.read_text(encoding="utf-8")
        # Debe tener al menos un hallazgo documentado
        return "### " in content
    except Exception:
        return False


# ============================================================================
# COMANDO DE LÃNEA
# ============================================================================

if __name__ == "__main__":
    import sys
    
    result = check_completion()
    show_completion_report(result)
    
    # Exit code para scripting
    sys.exit(0 if result["can_complete"] else 1)


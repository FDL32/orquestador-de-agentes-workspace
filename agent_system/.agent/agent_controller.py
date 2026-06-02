#!/usr/bin/env python3
"""
Agent Controller v5 - Sistema Multi-Agente
==========================================
Orquestador con:
- Hook System (pre-action, post-tool y stop hooks)
- Native Claude Code hooks (PostToolUse, PreCompact, Stop, SubagentStop)
- Completion Verification antes de review
- Quality Gates extendidos
- Session Recovery
- Project Map y estado del workflow

Uso:
    python .agent/agent_controller.py              # Ver estado y turno actual
    python .agent/agent_controller.py --json       # Output en JSON
    python .agent/agent_controller.py --skip-gates # Saltar Quality Gates
    python .agent/agent_controller.py --archive    # Archivar notificaciones antiguas
    python .agent/agent_controller.py --validate   # Solo validar archivos de estado
    python .agent/agent_controller.py --strict     # Modo estricto (bloquea si falla)
"""

# Fix encoding issues on Windows
import codecs
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# Fix imports when run as script (not as package)
_AGENT_DIR = Path(__file__).parent.resolve()
if str(_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(_AGENT_DIR))

# ============================================================================
# IMPORTS: HOOK SYSTEM, SESSION TRACKER & COMPLETION CHECKER
# ============================================================================
try:
    from hooks import registry as hook_registry
    from hooks.pre_action_hook import pre_action_hook
    from hooks.post_tool_hook import post_tool_hook
    from hooks.stop_hook import stop_hook
    HOOKS_AVAILABLE = True
    hook_registry.register("pre_action", pre_action_hook)
    hook_registry.register("post_tool", post_tool_hook)
    hook_registry.register("stop", stop_hook)
except ImportError:
    HOOKS_AVAILABLE = False
    hook_registry = None

try:
    from session_tracker import save_session, recover_session, show_recovery_hint
    SESSION_TRACKER_AVAILABLE = True
except ImportError:
    SESSION_TRACKER_AVAILABLE = False

try:
    from completion_checker import check_completion, show_completion_report
    COMPLETION_CHECKER_AVAILABLE = True
except ImportError:
    COMPLETION_CHECKER_AVAILABLE = False

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
AGENT_DIR = PROJECT_ROOT / ".agent"
COLLAB_DIR = AGENT_DIR / "collaboration"
CONTEXT_DIR = AGENT_DIR / "context"

# State files
WORK_PLAN = COLLAB_DIR / "work_plan.md"
EXEC_LOG = COLLAB_DIR / "execution_log.md"
REVIEW_QUEUE = COLLAB_DIR / "review_queue.md"
NOTIFICATIONS = COLLAB_DIR / "notifications.md"
TURN_FILE = COLLAB_DIR / "TURN.md"
PROJECT_MAP = CONTEXT_DIR / "project_map.md"
ARCHIVE_DIR = COLLAB_DIR / "archive"

# Archive configuration
MAX_NOTIFICATIONS_SIZE_KB = 50
MAX_NOTIFICATION_ENTRIES = 20

# Configuracion de comprobaciones
MAX_FILES_CIRCULAR_CHECK = 50

# Estados validos para validacion
VALID_PLAN_STATES = {"DRAFT", "IN_PLANNING", "APPROVED", "IN_REVIEW", "COMPLETED", "N/A"}
VALID_LOG_STATES = {"PENDING", "IN_PROGRESS", "BLOCKED", "READY_FOR_REVIEW", "COMPLETED", "N/A"}

# Ensure directories exist
CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def read_file(path: Path) -> str:
    """Lee un archivo si existe, retorna string vacio si no."""
    if not path.exists():
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str) -> None:
    """Escribe contenido a un archivo, creando directorios si es necesario."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_status(content: str, marker: str) -> str:
    """Extrae el estado de un archivo buscando un marcador."""
    for line in content.split("\n"):
        if marker in line:
            return line.split(marker)[1].strip()
    return "UNKNOWN"


def get_plan_id(content: str) -> str:
    """Extrae el ID del plan de trabajo."""
    for line in content.split("\n"):
        if "**ID:**" in line or "**Plan ID:**" in line:
            return line.split(":**")[1].strip()
    return "N/A"


def get_plan_type(content: str) -> str:
    """Extrae el tipo de plan. Valores: IMPLEMENTATION (default) | FINALIZATION."""
    for line in content.split("\n"):
        if "**Tipo:**" in line:
            return line.split(":**")[1].strip().upper()
    return "IMPLEMENTATION"


def check_git_status() -> Optional[bool]:
    """Verifica si el repositorio esta limpio."""
    if not (PROJECT_ROOT / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        if result.stdout.strip():
            return False
        return True
    except FileNotFoundError:
        return None


def extract_status_emoji(status_str: str) -> Tuple[str, str]:
    """Extrae el estado limpio y el emoji."""
    emojis = {"ðŸŸ¢", "ðŸŸ¡", "ðŸ”´", "ðŸŸ£", "âœ…", "â³", "âŒ", "âš ï¸"}
    status_clean = status_str.strip()
    found_emoji = ""
    for emoji in emojis:
        if emoji in status_clean:
            found_emoji = emoji
            status_clean = status_clean.replace(emoji, "").strip()
            break
    return status_clean, found_emoji


def validate_state_files() -> Dict[str, List[str]]:
    """Valida el formato y consistencia cruzada de los archivos de estado."""
    errors: Dict[str, List[str]] = {
        "work_plan.md": [], "execution_log.md": [],
        "notifications.md": [], "TURN.md": [], "consistency": [],
    }

    plan_content = read_file(WORK_PLAN)
    plan_status_raw = ""
    if plan_content:
        plan_status_raw = get_status(plan_content, "**Estado:**")
        status_clean, _ = extract_status_emoji(plan_status_raw)
        if status_clean and status_clean not in VALID_PLAN_STATES:
            errors["work_plan.md"].append(f"Estado invalido: '{status_clean}'")
        if "**ID:**" not in plan_content:
            errors["work_plan.md"].append("Falta campo **ID:**")

    log_content = read_file(EXEC_LOG)
    log_status_raw = ""
    if log_content:
        log_status_raw = get_status(log_content, "**Estado:**")
        status_clean, _ = extract_status_emoji(log_status_raw)
        if status_clean and status_clean not in VALID_LOG_STATES:
            errors["execution_log.md"].append(f"Estado invalido: '{status_clean}'")

    turn_content = read_file(TURN_FILE)
    if turn_content:
        if "## Agente Activo" not in turn_content:
            errors["TURN.md"].append("Falta secciÃ³n '## Agente Activo'")

    notif_content = read_file(NOTIFICATIONS)
    if notif_content:
        if "</thinking>" in notif_content:
            errors["notifications.md"].append("Contiene etiquetas </thinking> (corrupto)")

    # --- Validacion de consistencia cruzada ---
    if plan_content and log_content:
        plan_clean, _ = extract_status_emoji(plan_status_raw)
        log_clean, _ = extract_status_emoji(log_status_raw)

        # Plan APPROVED pero log aun en PENDING (Builder no ha arrancado aun puede ser OK,
        # pero si existe log previo con otro plan es sospechoso)
        if "APPROVED" in plan_clean and "COMPLETED" in log_clean:
            errors["consistency"].append(
                "DRIFT: plan=APPROVED pero log=COMPLETED â€” "
                "el log pertenece a un ciclo anterior. Limpia execution_log.md."
            )

        # Plan COMPLETED pero log aun IN_PROGRESS
        if "COMPLETED" in plan_clean and "IN_PROGRESS" in log_clean:
            errors["consistency"].append(
                "DRIFT: plan=COMPLETED pero log=IN_PROGRESS â€” "
                "el Builder no cerro su bitacora correctamente."
            )

        # Plan IN_PLANNING con log READY_FOR_REVIEW (imposible)
        if "IN_PLANNING" in plan_clean and "READY_FOR_REVIEW" in log_clean:
            errors["consistency"].append(
                "DRIFT: plan=IN_PLANNING pero log=READY_FOR_REVIEW â€” "
                "estado imposible. El plan debe estar APPROVED antes de que el Builder entregue."
            )

        # Plan N/A pero log activo
        if ("N/A" in plan_clean or not plan_clean) and log_clean not in ("N/A", "COMPLETED", "PENDING", ""):
            errors["consistency"].append(
                f"DRIFT: no hay plan activo pero log={log_clean} â€” "
                "limpia execution_log.md o crea un nuevo work_plan.md."
            )

    return errors


def fix_corrupted_notifications() -> bool:
    """Intenta reparar notifications.md si esta corrupto."""
    content = read_file(NOTIFICATIONS)
    if not content:
        return False
    original = content
    content = re.sub(r"</thinking>\s*", "", content)
    content = re.sub(r"\n{4,}", "\n\n---\n\n", content)
    if content != original:
        write_file(NOTIFICATIONS, content)
        return True
    return False


def archive_old_notifications() -> Optional[str]:
    """Archiva notificaciones antiguas si el archivo es muy grande."""
    content = read_file(NOTIFICATIONS)
    if not content:
        return None

    file_size_kb = len(content.encode("utf-8")) / 1024
    entry_count = len([e for e in content.split("---") if e.strip() and "ðŸ“¨" in e])

    if file_size_kb < MAX_NOTIFICATIONS_SIZE_KB and entry_count <= MAX_NOTIFICATION_ENTRIES:
        return None

    parts = content.split("---")
    entries = [p.strip() for p in parts if p.strip() and "ðŸ“¨" in p]

    if len(entries) <= MAX_NOTIFICATION_ENTRIES:
        return None

    entries_to_archive = entries[:-MAX_NOTIFICATION_ENTRIES]
    entries_to_keep = entries[-MAX_NOTIFICATION_ENTRIES:]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = ARCHIVE_DIR / f"notifications_{timestamp}.md"

    archive_content = "# Notificaciones Archivadas\n\n"
    archive_content += f"**Fecha:** {datetime.now():%Y-%m-%d %H:%M:%S}\n"
    archive_content += "\n---\n\n".join(entries_to_archive)

    write_file(archive_file, archive_content)

    new_content = "# Registro de Notificaciones\n\n---\n\n"
    new_content += "\n\n---\n\n".join(entries_to_keep)
    new_content += "\n\n---\n"
    write_file(NOTIFICATIONS, new_content)

    return str(archive_file)


def run_finalization_checks() -> dict:
    """Checks adicionales para planes de tipo FINALIZATION."""
    results = {"passed": True, "summary": []}
    checks = {
        "README.md": PROJECT_ROOT / "README.md",
        "CHANGELOG.md": PROJECT_ROOT / "CHANGELOG.md",
        "closeout_report.md": COLLAB_DIR / "closeout_report.md",
    }
    for name, path in checks.items():
        if path.exists():
            results["summary"].append(f"[OK] {name}: Presente")
        else:
            results["summary"].append(f"[WARN] {name}: No encontrado")
    return results


def run_quality_gates(extended: bool = True, plan_type: str = "IMPLEMENTATION") -> dict:
    """Ejecuta validaciones automaticas."""
    print("\n[QUALITY GATES] Ejecutando Quality Gates...")
    results = {"passed": True, "errors": [], "summary": [], "warnings": []}

    state_errors = validate_state_files()
    total_state_errors = sum(len(errs) for errs in state_errors.values())
    if total_state_errors > 0:
        results["warnings"].append(f"Archivos de estado: {total_state_errors} problemas")
    else:
        results["summary"].append("[OK] Estado: Archivos validos")

    src_dir = PROJECT_ROOT / "src"
    tests_dir = PROJECT_ROOT / "tests"
    dirs_to_check = [str(src_dir)]
    if tests_dir.exists():
        dirs_to_check.append(str(tests_dir))

    try:
        ruff = subprocess.run(
            ["uv", "run", "ruff", "check"] + dirs_to_check,
            capture_output=True,
            text=True,
            timeout=60
        )
        if ruff.returncode != 0:
            results["passed"] = False
            results["summary"].append("[FAIL] Ruff: Errores de linting")
        else:
            results["summary"].append("[OK] Ruff: Limpio")
    except FileNotFoundError:
        results["summary"].append("[WARN] Ruff: No instalado")

    if tests_dir.exists():
        try:
            pytest_result = subprocess.run(
                ["uv", "run", "pytest", "-q"],
                capture_output=True,
                timeout=120,
                cwd=PROJECT_ROOT
            )
            if pytest_result.returncode != 0:
                results["passed"] = False
                results["summary"].append("[FAIL] Pytest: Tests fallando")
            else:
                results["summary"].append("[OK] Pytest: Tests OK")
        except FileNotFoundError:
            results["summary"].append("[WARN] Pytest: No instalado")

    if plan_type == "FINALIZATION":
        fin_results = run_finalization_checks()
        results["summary"].extend(fin_results["summary"])

    status = "[PASSED]" if results["passed"] else "[FAILED]"
    print(f"   {status}")
    return results


def update_log_status(new_status: str, note: str) -> bool:
    """Actualiza el estado en execution_log.md."""
    content = read_file(EXEC_LOG)
    if not content:
        return False
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "**Estado:**" in line:
            lines[i] = f"**Estado:** {new_status}"
            new_content = "\n".join(lines) + f"\n\n{note}"
            write_file(EXEC_LOG, new_content)
            return True
    return False


def create_findings_file(plan_id: str = "N/A") -> Path:
    """Crea findings.md desde template."""
    findings_path = COLLAB_DIR / "findings.md"

    if findings_path.exists():
        return findings_path

    template_path = AGENT_DIR / "templates" / "findings_template.md"

    try:
        if template_path.exists():
            template = template_path.read_text(encoding="utf-8")
        else:
            template = """# Hallazgos de Investigacion

**Plan ID:** {{PLAN_ID}}
**Creado:** {{DATE}}

---

## Hallazgos

<!-- Documenta aqui tus hallazgos durante la investigacion -->
"""

        content = template.replace("{{PLAN_ID}}", plan_id)
        content = content.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        write_file(findings_path, content)
        print("  [OK] Creado findings.md")

    except Exception as e:
        print(f"  [WARN] Error creando findings.md: {e}")

    return findings_path


def generate_project_map() -> str:
    """Genera un mapa actualizado del proyecto."""
    output = [
        "# Mapa del Proyecto",
        f"**Actualizado:** {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        "## Estructura de Archivos",
        "```"
    ]

    ignore = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    extensions = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}

    files_found = []
    for path in sorted(PROJECT_ROOT.rglob("*")):
        if any(part in ignore for part in path.parts):
            continue
        if path.is_file() and path.suffix in extensions:
            files_found.append(str(path.relative_to(PROJECT_ROOT)))

    output.extend(files_found[:50])
    if len(files_found) > 50:
        output.append(f"... (+{len(files_found) - 50} archivos mas)")

    output.append("```")
    content = "\n".join(output)
    write_file(PROJECT_MAP, content)
    return content


def determine_next_action(skip_gates: bool = False, strict_mode: bool = False) -> dict:
    """Analiza el estado y determina la siguiente accion."""
    plan_content = read_file(WORK_PLAN)
    log_content = read_file(EXEC_LOG)

    plan_status = get_status(plan_content, "**Estado:**")
    log_status = get_status(log_content, "**Estado:**")
    plan_id = get_plan_id(plan_content)
    plan_type = get_plan_type(plan_content)

    def _action(**kwargs) -> dict:
        """Helper: aÃ±ade plan_type a todos los action dicts."""
        return {"plan_type": plan_type, **kwargs}

    pre_action_type = "CHECK_STATUS"
    if not plan_content.strip() or "COMPLETED" in plan_status or "N/A" in plan_status:
        pre_action_type = "CREATE_PLAN"
    elif "APPROVED" in plan_status and "READY_FOR_REVIEW" in log_status:
        pre_action_type = "REVIEW_WORK"
    elif "APPROVED" in plan_status:
        pre_action_type = "IMPLEMENT"

    if HOOKS_AVAILABLE and hook_registry:
        hook_registry.execute("pre_action", {
            "action_type": pre_action_type,
            "plan_id": plan_id,
            "plan_status": plan_status,
            "log_status": log_status,
        })

    gate_result = None
    if "APPROVED" in plan_status and "READY_FOR_REVIEW" in log_status and not skip_gates:
        gate_result = run_quality_gates(plan_type=plan_type)
        if not gate_result["passed"]:
            update_log_status("IN_PROGRESS", "AUTO-REJECTED: Quality Gates fallaron")
            return _action(
                role="BUILDER",
                context_file=".builder_rules",
                workflow_file=".agent/workflows/builder_workflow.md",
                instruction="RECHAZADO. Quality Gates fallaron. Corrige errores.",
                plan_id=plan_id,
                plan_status=plan_status,
                log_status="AUTO-REJECTED",
                action_type="FIX_QUALITY_ISSUES",
            )

    if not plan_content.strip() or "COMPLETED" in plan_status or "N/A" in plan_status:
        return _action(
            role="MANAGER",
            context_file=".manager_rules",
            workflow_file=".agent/workflows/manager_workflow.md",
            instruction="No hay plan activo. Crea un nuevo work_plan.md",
            plan_id="NINGUNO",
            plan_status=plan_status or "N/A",
            log_status=log_status or "N/A",
            action_type="CREATE_PLAN",
        )

    if "IN_PLANNING" in plan_status:
        return _action(
            role="MANAGER",
            context_file=".manager_rules",
            workflow_file=".agent/workflows/manager_workflow.md",
            instruction=f"Plan {plan_id} en borrador. Finaliza y cambia a APPROVED",
            plan_id=plan_id,
            plan_status=plan_status,
            log_status=log_status,
            action_type="FINALIZE_PLAN",
        )

    if "BLOCKED" in log_status:
        return _action(
            role="MANAGER",
            context_file=".manager_rules",
            workflow_file=".agent/workflows/manager_workflow.md",
            instruction=f"Builder BLOQUEADO en {plan_id}. Resuelve en review_queue.md",
            plan_id=plan_id,
            plan_status=plan_status,
            log_status=log_status,
            action_type="RESOLVE_BLOCK",
        )

    if "APPROVED" in plan_status and "READY_FOR_REVIEW" in log_status:
        if HOOKS_AVAILABLE and hook_registry:
            stop_result = stop_hook({
                "plan_status": plan_status,
                "plan_type": plan_type,
                "mode": "strict" if strict_mode else "normal",
            })
            if strict_mode and not stop_result.get("can_complete", True):
                return _action(
                    role="BUILDER",
                    context_file=".builder_rules",
                    workflow_file=".agent/workflows/builder_workflow.md",
                    instruction=(
                        f"Plan {plan_id} no supera Completion Verification. "
                        "Corrige advertencias antes de review."
                    ),
                    plan_id=plan_id,
                    plan_status=plan_status,
                    log_status=log_status,
                    action_type="FIX_QUALITY_ISSUES",
                )

        return _action(
            role="MANAGER",
            context_file=".manager_rules",
            workflow_file=".agent/workflows/manager_workflow.md",
            instruction=f"Builder completo {plan_id}. Revisa el trabajo.",
            plan_id=plan_id,
            plan_status=plan_status,
            log_status=log_status,
            action_type="REVIEW_WORK",
        )

    if "IN_REVIEW" in plan_status:
        return _action(
            role="MANAGER",
            context_file=".manager_rules",
            workflow_file=".agent/workflows/manager_workflow.md",
            instruction=f"Plan {plan_id} en revision. Verifica cambios.",
            plan_id=plan_id,
            plan_status=plan_status,
            log_status=log_status,
            action_type="REVIEW_CHANGES",
        )

    if "APPROVED" in plan_status:
        instruction = (
            f"Plan {plan_id} aprobado. Ejecuta cierre segun work_plan.md"
            if plan_type == "FINALIZATION"
            else f"Plan {plan_id} aprobado. Implementa segun work_plan.md"
        )
        return _action(
            role="BUILDER",
            context_file=".builder_rules",
            workflow_file=".agent/workflows/builder_workflow.md",
            instruction=instruction,
            plan_id=plan_id,
            plan_status=plan_status,
            log_status=log_status,
            action_type="IMPLEMENT",
        )

    return _action(
        role="UNKNOWN",
        context_file="N/A",
        workflow_file="N/A",
        instruction="Estado indeterminado. Revisa archivos manualmente.",
        plan_id=plan_id,
        plan_status=plan_status,
        log_status=log_status,
        action_type="MANUAL_INTERVENTION",
    )


def should_overwrite_turn(turn_path: Path, force_reset: bool = False) -> bool:
    """Devuelve True solo si TURN.md debe ser regenerado."""
    if force_reset or not turn_path.exists():
        return True
    try:
        content = turn_path.read_text(encoding="utf-8")
        if "UNKNOWN" in content or "MANUAL_INTERVENTION" in content:
            return True
        return False
    except Exception:
        return True


def update_turn_file(action: dict) -> None:
    """Actualiza TURN.md con informacion del turno actual."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# TURNO ACTUAL

**Ultima actualizacion:** {timestamp}

---

## Agente Activo

| Campo | Valor |
|-------|-------|
| **ROL** | **{action['role']}** |
| **Plan ID** | {action['plan_id']} |
| **Tipo** | {action.get('plan_type', 'IMPLEMENTATION')} |
| **Accion** | {action['action_type']} |

---

## Instruccion

> {action['instruction']}

---

## Archivos a Leer

1. `{action['context_file']}` (Contexto del rol)
2. `{action['workflow_file']}` (Flujo de trabajo)
3. `.agent/context/project_map.md` (Estructura)

---

## Estado del Sistema

| Archivo | Estado |
|---------|--------|
| work_plan.md | {action['plan_status']} |
| execution_log.md | {action['log_status']} |

---

*Generado por agent_controller.py v5*
"""
    write_file(TURN_FILE, content)


def print_human_readable(action: dict) -> None:
    """Muestra el estado de forma legible."""
    role = action["role"]
    role_emoji = {"MANAGER": "MANAGER", "BUILDER": "BUILDER", "UNKNOWN": "UNKNOWN"}.get(role, "UNKNOWN")

    plan_type = action.get("plan_type", "IMPLEMENTATION")
    type_label = " [CIERRE]" if plan_type == "FINALIZATION" else ""

    print("\n" + "=" * 70)
    print("  SISTEMA MULTI-AGENTE v5 - Panel de Control")
    print("=" * 70)
    print(f"\n  TURNO ACTUAL: {role_emoji} {role}{type_label}")
    print(f"  Plan: {action['plan_id']}")
    print("\n  ESTADOS:")
    print(f"     - Plan:     {action['plan_status']}")
    print(f"     - Progreso: {action['log_status']}")
    print("\n  ACCION:")
    print(f"     {action['instruction']}")

    # Siguiente paso accionable para el usuario
    next_role = "BUILDER" if role == "MANAGER" else "MANAGER"
    action_type = action.get("action_type", "")
    if action_type == "IMPLEMENT":
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y continua con el plan'"
    elif action_type in ("REVIEW_WORK", "REVIEW_CHANGES"):
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y revisa la implementacion'"
    elif action_type == "CREATE_PLAN":
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y crea el plan'"
    elif action_type == "FIX_QUALITY_ISSUES":
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y corrige los errores'"
    elif action_type == "RESOLVE_BLOCK":
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y resuelve el bloqueo'"
    else:
        next_msg = f"Abre el agente {role} y dile: 'Ejecuta python .agent/agent_controller.py y continua'"

    print("\n  SIGUIENTE PASO:")
    print(f"     {next_msg}")
    print("\n  COMANDOS:")
    print("     python .agent/agent_controller.py")
    print("     python .agent/agent_controller.py --strict")
    print("=" * 70 + "\n")


def main():
    """Funcion principal del controller."""
    skip_gates = "--skip-gates" in sys.argv
    json_output = "--json" in sys.argv
    archive_mode = "--archive" in sys.argv
    validate_only = "--validate" in sys.argv
    force_mode = "--force" in sys.argv
    strict_mode = "--strict" in sys.argv
    recover_mode = "--recover" in sys.argv
    reset_turn_mode = "--reset-turn" in sys.argv

    if recover_mode:
        if SESSION_TRACKER_AVAILABLE:
            result = recover_session()
            if not result:
                print("[INFO] No hay sesion previa para recuperar.")
        else:
            print("[WARN] Session tracker no disponible.")
        return 0

    if "--check-completion" in sys.argv:
        if COMPLETION_CHECKER_AVAILABLE:
            result = check_completion()
            show_completion_report(result)
            return 0 if result["can_complete"] else 1
        print("[WARN] Completion checker no disponible.")
        return 1

    git_status = check_git_status()
    if not force_mode and git_status is False:
        print("\n[WARN] Tienes cambios sin guardar en git.")
        print("   Guarda tus cambios antes de continuar:")
        print("   git add . && git commit -m 'Guardo trabajo'")
        print("   O usa --force para ignorar.\n")
        return 1

    if validate_only:
        errors = validate_state_files()
        total = sum(len(errs) for errs in errors.values())
        if json_output:
            print(json.dumps(errors, indent=2))
        else:
            if total == 0:
                print("[OK] Todos los archivos de estado son validos.")
            else:
                print(f"[WARN] {total} problema(s) encontrados.")
        return 0 if total == 0 else 1

    if archive_mode:
        archive_path = archive_old_notifications()
        if archive_path:
            print(f"[OK] Archivado: {archive_path}")
        else:
            print("[INFO] No es necesario archivar.")
        return 0

    if SESSION_TRACKER_AVAILABLE:
        show_recovery_hint()

    print("\n  Generando mapa del proyecto...")
    generate_project_map()
    print("  [OK] Mapa actualizado")

    notif_errors = validate_state_files().get("notifications.md", [])
    if notif_errors:
        fix_corrupted_notifications()

    archive_old_notifications()

    action = determine_next_action(skip_gates=skip_gates, strict_mode=strict_mode)

    if should_overwrite_turn(TURN_FILE, force_reset=reset_turn_mode):
        update_turn_file(action)

    if json_output:
        print(json.dumps(action, indent=2, ensure_ascii=False))
    else:
        print_human_readable(action)

    if SESSION_TRACKER_AVAILABLE:
        save_session()

    return 0


if __name__ == "__main__":
    sys.exit(main())


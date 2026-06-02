#!/usr/bin/env python3
"""
Instalador del Sistema Multi-Agente
====================================
Copia el sistema de agentes a un nuevo proyecto.

Uso:
    python install_agent_system.py /ruta/a/mi/proyecto
    python install_agent_system.py .  # Proyecto actual
"""

import json
import shutil
import sys
from datetime import date
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

LOCAL_GITIGNORE_ENTRIES = [
    ".claude/settings.local.json",
    ".agent/config/hooks_config.local.json",
]

DEFAULT_AGENT_ALLOWLIST = {
    "write_roots": ["."],
    "stable_engines": ["goose"],
    "experimental_engines": ["claw"],
}

DEFAULT_AGENT_DENYLIST = {
    "protected_paths": ["privada/", ".ssh/", ".gnupg/"],
    "protected_filenames": ["TURN.md", ".env", ".env.local", ".env.production", ".env.development"],
    "blocked_command_patterns": [
        "\\brm\\s+-rf\\b",
        "\\brmdir\\b",
        "\\bdel\\b",
        "\\berase\\b",
        "\\bgit\\s+push\\b",
        "\\bgit\\s+reset\\s+--hard\\b",
        "\\bgit\\s+clean\\s+-fd\\b",
        "\\bgit\\s+clean\\s+-xdf\\b",
    ],
}

DEFAULT_KNOWN_MODELS = [
    "claude-sonnet-4-6",
    "claude-haiku-4-5",
    "kilo-code",
    "codex",
]

# Definir exclusiones de runtime para empaquetado seguro (TICKET-014)
RUNTIME_EXCLUSIONS = [
    "STATE.md",
    "TURN.md",
    "execution_log.md",
    ".session_state.json",
    ".tool_counter.json",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
]


def install(target_dir: Path, full_structure: bool = False) -> None:
    """Instala el sistema de agentes en el directorio objetivo."""

    # Directorio raÃ­z del sistema (agent_system/)
    source_dir = Path(__file__).resolve().parent.parent

    # Archivos y carpetas a copiar
    items_to_copy = [
        (".agent", "carpeta del sistema de agentes"),
        ("skills", "micro-skills del sistema"),
        ("scripts/orquestador.py", "orquestador multi-agente con modos research/write"),
        ("scripts/run_pytest_safe.py", "runner seguro de pytest para el proyecto"),
    ]
    
    print("\n" + "=" * 60)
    print("ðŸ¤– INSTALADOR DEL SISTEMA MULTI-AGENTE")
    print("=" * 60)
    print(f"\nðŸ“‚ Destino: {target_dir.absolute()}")
    if full_structure:
        print("ðŸ—ï¸  Modo: Estructura Completa (publica/privada)")
    else:
        print("ðŸ—ï¸  Modo: Estructura Plana")
    print()
    
    # Verificar que el directorio destino existe
    if not target_dir.exists():
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"âŒ Error: El directorio {target_dir} no existe y no pudo ser creado: {e}")
            sys.exit(1)
            
    if full_structure:
        base_copy_dir = target_dir / "publica" / "repo"
        base_copy_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "publica" / "cuarentena").mkdir(parents=True, exist_ok=True)
        (target_dir / "publica" / "backups").mkdir(parents=True, exist_ok=True)
        (target_dir / "privada" / "config").mkdir(parents=True, exist_ok=True)
    else:
        base_copy_dir = target_dir
    
    # Copiar cada elemento
    for item, description in items_to_copy:
        source = source_dir / item
        dest = base_copy_dir / item
        
        if not source.exists():
            print(f"âš ï¸  {item} no encontrado en origen, saltando...")
            continue
        
        # Si ya existe, preguntar
        if dest.exists():
            response = input(f"âš ï¸  {item} ya existe. Â¿Sobrescribir? [s/N]: ")
            if response.lower() != 's':
                print(f"   Saltando {item}")
                continue
            # Eliminar existente
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        
        # Copiar
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            # Aplicar exclusiones de runtime para evitar contaminar el destino
            ignore_func = shutil.ignore_patterns(*RUNTIME_EXCLUSIONS)
            shutil.copytree(source, dest, ignore=ignore_func)
        else:
            shutil.copy2(source, dest)
        
        print(f"âœ… Copiado: {item} ({description})")
    
    # Instrucciones finales
    print("\n" + "-" * 60)
    print("âœ… INSTALACIÃ“N COMPLETADA")
    print("-" * 60)

    # Generar lanzador .bat
    generate_bat_launcher(base_copy_dir)

    # Generar infraestructura Claude Code
    generate_claude_config(base_copy_dir, source_dir)

    # Generar configuracion local de seguridad
    generate_agent_security_config(base_copy_dir)

    # Asegurar overrides locales en .gitignore
    ensure_local_override_entries(base_copy_dir)

    print(f"""
ðŸ“‹ PrÃ³ximos pasos:

1. Estructura instalada:
{"   â†’ Usa publica/repo/ para tu cÃ³digo y donde trabajan los agentes" if full_structure else "   â†’ Modo plano: agentes y cÃ³digo operan en el directorio raÃ­z"}
{"   â†’ Usa privada/config/ para tus credenciales (los agentes no las ven)" if full_structure else "   â†’ ATENCIÃ“N: En modo plano no hay carpeta separada para secretos"}

2. Configurar Reglas:
   â†’ El archivo .manager_rules se lee automÃ¡ticamente (si la extensiÃ³n lo soporta)
   â†’ O copia .manager_rules a las instrucciones del sistema del Manager

3. Iniciar el sistema:
{"   â†’ cd publica/repo/" if full_structure else "   â†’ Ve a la raÃ­z de tu proyecto"}
   â†’ Abre tu agente Manager o Builder
   â†’ Escribe: "Ejecuta python .agent/agent_controller.py"

4. Claude Code (si usas Claude Code CLI):
   â†’ CLAUDE.md generado automÃ¡ticamente con el contexto del proyecto
   â†’ Hook guard_paths activo: protege privada/ y TURN.md ante escrituras accidentales
   â†’ Agentes nativos disponibles: manager Â· builder
""")


def generate_claude_config(target_dir: Path, source_dir: Path) -> None:
    """Genera la infraestructura Claude Code en el proyecto instalado.

    Crea:
    - .claude/README.md             (documentaciÃ³n local del setup)
    - .claude/config.json           (configuraciÃ³n base del proyecto)
    - .claude/settings.local.json   (override local gitignored)
    - .claude/agents/*.md           (agentes nativos Manager y Builder)
    - .claude/settings.json         (hooks PreToolUse, PostToolUse, PreCompact, Stop y SubagentStop)
    - .claude/commands/agent-status.md
    - .claude/commands/quality-gates.md
    - .claude/commands/*.md         (workflow commands)
    - CLAUDE.md                     (generado desde templates/repo_root/CLAUDE.md.template)
    - PROJECT.md / README.md / CHANGELOG.md (generados desde templates/repo_root/)
    """
    print("\nðŸ”§ Configurando Claude Code...")

    source_claude_dir = source_dir / ".claude"
    claude_dir = target_dir / ".claude"
    commands_dir = claude_dir / "commands"
    agents_dir = claude_dir / "agents"
    claude_dir.mkdir(exist_ok=True)
    commands_dir.mkdir(exist_ok=True)
    agents_dir.mkdir(exist_ok=True)

    # Copiar archivos base de .claude si existen
    for filename in ["README.md", "config.json", "settings.local.json"]:
        source_file = source_claude_dir / filename
        dest_file = claude_dir / filename
        if source_file.exists() and not dest_file.exists():
            shutil.copy2(source_file, dest_file)
            print(f"   âœ… .claude/{filename}")

    # Copiar agentes nativos
    source_agents_dir = source_claude_dir / "agents"
    if source_agents_dir.exists():
        for source_file in sorted(source_agents_dir.glob("*.md")):
            dest_file = agents_dir / source_file.name
            if not dest_file.exists():
                shutil.copy2(source_file, dest_file)
                print(f"   âœ… .claude/agents/{source_file.name}")

    # Copiar slash commands de workflow
    source_commands_dir = source_claude_dir / "commands"
    if source_commands_dir.exists():
        for source_file in sorted(source_commands_dir.glob("*.md")):
            dest_file = commands_dir / source_file.name
            if not dest_file.exists():
                shutil.copy2(source_file, dest_file)
                print(f"   âœ… .claude/commands/{source_file.name}")

    # --- .claude/settings.json ---
    settings_path = claude_dir / "settings.json"
    settings = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit|Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python .agent/hooks/guard_paths.py"
                        }
                    ]
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Read|Grep|Glob|WebFetch",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python .agent/hooks/native_post_tool_hook.py"
                        }
                    ]
                }
            ],
            "PreCompact": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python .agent/hooks/pre_compact_hook.py"
                        }
                    ]
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python .agent/hooks/native_stop_hook.py"
                        }
                    ]
                }
            ],
            "SubagentStop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python .agent/hooks/subagent_stop_hook.py"
                        }
                    ]
                }
            ],
        }
    }
    # Fusionar con settings existente si lo hay
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text(encoding="utf-8"))
            existing.setdefault("hooks", {})
            for hook_name, hook_value in settings["hooks"].items():
                existing["hooks"][hook_name] = hook_value
            settings = existing
        except Exception:
            pass  # Si el settings existente estÃ¡ corrupto, sobreescribir

    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    print("   âœ… .claude/settings.json (hooks: PreToolUse, PostToolUse, PreCompact, Stop, SubagentStop)")

    # --- .claude/commands/agent-status.md ---
    agent_status_content = """Ejecuta el siguiente comando y muestra el resultado interpretado:

```bash
python .agent/agent_controller.py
```

Si el comando falla, muestra el turno actual desde `collaboration/TURN.md`, \
las fases de `collaboration/work_plan.md` (completadas / pendientes) y \
las notificaciones pendientes de `collaboration/notifications.md`.

Indica claramente quiÃ©n tiene el turno (Manager o Builder), quÃ© fase estÃ¡ activa \
y cuÃ¡l es el siguiente paso recomendado.
"""
    (commands_dir / "agent-status.md").write_text(agent_status_content, encoding="utf-8")
    print("   âœ… .claude/commands/agent-status.md")

    # --- .claude/commands/quality-gates.md ---
    quality_gates_content = """Ejecuta los Quality Gates del proyecto en este orden:

```bash
python scripts/run_pytest_safe.py --status
ruff check src/ tests/ --fix
ruff format src/ tests/
python scripts/run_pytest_safe.py
```

Si algÃºn paso falla, muestra el error completo, explica la causa mÃ¡s probable \
y propone la correcciÃ³n concreta. Si todos pasan, confirma con un resumen: \
N tests pasados, 0 errores ruff, formato correcto.
"""
    (commands_dir / "quality-gates.md").write_text(quality_gates_content, encoding="utf-8")
    print("   âœ… .claude/commands/quality-gates.md")

    generate_repo_root_files(target_dir, source_dir)


def derive_project_name(target_dir: Path) -> str:
    """Deriva un nombre humano del proyecto destino."""
    if target_dir.name == "repo" and target_dir.parent.name == "publica":
        return target_dir.parent.parent.name
    return target_dir.name


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    """Renderiza una plantilla textual con reemplazos simples."""
    content = template_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def write_repo_root_template(
    target_dir: Path,
    source_dir: Path,
    template_name: str,
    output_name: str,
    replacements: dict[str, str],
) -> None:
    """Genera un archivo de raÃ­z del repo si no existe todavÃ­a."""
    template_path = source_dir / "templates" / "repo_root" / template_name
    output_path = target_dir / output_name

    if output_path.exists():
        print(f"   â„¹ï¸  {output_name} ya existe, no se sobreescribe")
        return

    if not template_path.exists():
        print(f"   âš ï¸  Template {template_name} no encontrado, saltando")
        return

    output_path.write_text(render_template(template_path, replacements), encoding="utf-8")
    print(f"   âœ… {output_name}")


def generate_repo_root_files(target_dir: Path, source_dir: Path) -> None:
    """Genera archivos base del repo a partir de templates/repo_root/."""
    print("\nðŸ§¾ Generando archivos base del repo...")

    project_name = derive_project_name(target_dir)
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{DATE}}": date.today().isoformat(),
    }

    write_repo_root_template(target_dir, source_dir, "CLAUDE.md.template", "CLAUDE.md", replacements)
    write_repo_root_template(target_dir, source_dir, "PROJECT.md.template", "PROJECT.md", replacements)
    write_repo_root_template(target_dir, source_dir, "CHANGELOG.md.template", "CHANGELOG.md", replacements)
    write_repo_root_template(target_dir, source_dir, "README.md.template", "README.md", replacements)
    write_repo_root_template(target_dir, source_dir, "AGENT_SECURITY.md.template", "AGENT_SECURITY.md", replacements)


def generate_agent_security_config(target_dir: Path) -> None:
    """Genera allowlist/denylist externas para hooks y orquestador."""
    allowlist_path = target_dir / ".agent_allowlist.json"
    denylist_path = target_dir / ".agent_denylist.json"
    known_models_path = target_dir / ".agent" / "known_models.json"

    if not allowlist_path.exists():
        allowlist_path.write_text(
            json.dumps(DEFAULT_AGENT_ALLOWLIST, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("   [OK] .agent_allowlist.json")
    else:
        print("   [INFO] .agent_allowlist.json ya existe, no se sobreescribe")

    if not denylist_path.exists():
        denylist_path.write_text(
            json.dumps(DEFAULT_AGENT_DENYLIST, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("   [OK] .agent_denylist.json")
    else:
        print("   [INFO] .agent_denylist.json ya existe, no se sobreescribe")

    known_models_path.parent.mkdir(parents=True, exist_ok=True)
    if not known_models_path.exists():
        known_models_path.write_text(
            json.dumps(DEFAULT_KNOWN_MODELS, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("   [OK] .agent/known_models.json")
    else:
        print("   [INFO] .agent/known_models.json ya existe, no se sobreescribe")


def ensure_local_override_entries(target_dir: Path) -> None:
    """Asegura que las entradas de overrides locales existan en .gitignore."""
    gitignore_path = target_dir / ".gitignore"

    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
    else:
        content = ""

    missing_entries = [entry for entry in LOCAL_GITIGNORE_ENTRIES if entry not in content]

    if not missing_entries:
        print("   â„¹ï¸  .gitignore ya contiene overrides locales")
        return

    if not content.endswith("\n"):
        content += "\n"

    content += "\n# Overrides locales del sistema multi-agente\n"
    content += "\n".join(missing_entries) + "\n"
    gitignore_path.write_text(content, encoding="utf-8")
    print("   âœ… .gitignore actualizado con overrides locales")


def detect_gui_usage(target_dir: Path) -> bool:
    """Detecta si el proyecto usa GUI buscando imports comunes."""
    gui_keywords = [
        "tkinter", "PyQt5", "PyQt6", "PySide2", "PySide6", 
        "wx", "kivy", "streamlit", "gradio"
    ]
    
    encodings = ["utf-8", "utf-16", "cp1252"]

    # Buscar en requirements.txt o pyproject.toml
    req_files = ["requirements.txt", "pyproject.toml"]
    for req_file in req_files:
        f = target_dir / req_file
        if f.exists():
            for enc in encodings:
                try:
                    content = f.read_text(encoding=enc)
                    if any(k.lower() in content.lower() for k in gui_keywords):
                        return True
                    # Si leÃ­mos con Ã©xito pero no encontramos nada, paramos con este archivo 
                    # (asumiendo que si decodifica bien en utf-8, no es utf-16)
                    break 
                except UnicodeError:
                    continue

    # Buscar en cÃ³digo fuente
    src_dir = target_dir / "src"
    if src_dir.exists():
        for file in src_dir.rglob("*.py"):
            found_in_file = False
            for enc in encodings:
                try:
                    content = file.read_text(encoding=enc)
                    # Buscar imports explÃ­citos
                    for k in gui_keywords:
                        if f"import {k}" in content or f"from {k}" in content:
                            return True
                    found_in_file = True
                    break
                except UnicodeError:
                    continue
            
            if found_in_file:
                continue
                
    return False


def generate_bat_launcher(target_dir: Path) -> None:
    """Genera un archivo .bat para lanzar el proyecto."""
    
    # Determinar ubicaciÃ³n del .bat
    # Si target_dir termina en "repo" o "src", asumimos estructura anidada y subimos un nivel
    # para poner el .bat en la raÃ­z del proyecto (junto a "publica" y "privada")
    if target_dir.name in ["repo", "src"]:
        # Subir niveles hasta salir de publica/repo
        # Si estamos en .../publica/repo -> bat en .../
        bat_dir = target_dir.parent.parent
        project_name = bat_dir.name
        
        # Ruta relativa desde el bat al script
        # Ejemplo: publica\repo
        relative_project_path = target_dir.relative_to(bat_dir)
        project_path_var = f"%~dp0{relative_project_path}"
    else:
        # Estructura plana o desconocida, poner en el mismo dir
        bat_dir = target_dir
        project_name = target_dir.name
        project_path_var = "%~dp0"  # Directorio actual del script .bat
        if str(project_path_var).endswith("\\"):
             project_path_var = "%~dp0." # Evitar doble backslash si es raÃ­z

    bat_path = bat_dir / f"{project_name}.bat"
    
    print(f"\nðŸš€ Generando lanzador en: {bat_path}")
    
    # Detectar GUI
    has_gui = detect_gui_usage(target_dir)
    gui_status = "DETECTADO (Consola se cerrarÃ¡)" if has_gui else "NO DETECTADO (Consola permanecerÃ¡ abierta)"
    print(f"   Modo GUI: {gui_status}")
    
    # Seleccionar plantilla
    template_name = "bat_launcher_gui.template" if has_gui else "bat_launcher_cli.template"
    template_path = Path(__file__).parent / ".agent" / "templates" / template_name
    
    # Si estamos corriendo desde el repo de scripts (durante dev)
    if not template_path.exists():
         # Intentar ruta relativa al script actual en estructura de dev
        template_path = Path(__file__).parent.parent / ".agent" / "templates" / template_name
        
    if not template_path.exists():
        # Fallback: buscar en el target si ya se copiÃ³
        template_path = target_dir / ".agent" / "templates" / template_name

    if not template_path.exists():
        print(f"âš ï¸  No se encontrÃ³ la plantilla {template_name}. Saltando generaciÃ³n de .bat")
        return

    try:
        content = template_path.read_text(encoding="utf-8")
        
        # Reemplazar variables
        content = content.replace("{PROJECT_NAME}", project_name)
        
        # Usamos ruta dinÃ¡mica basada en la ubicaciÃ³n del .bat
        # Antes usÃ¡bamos ruta absoluta: content = content.replace("{PROJECT_PATH}", str(target_dir.absolute()))
        # Ahora usamos variable de batch
        content = content.replace("{PROJECT_PATH}", str(project_path_var))
        
        bat_path.write_text(content, encoding="utf-8")
        print("âœ… Lanzador creado exitosamente")
        
    except Exception as e:
        print(f"âŒ Error creando lanzador: {e}")


def main():
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] == "--full-structure"):
        print("Uso: python install_agent_system.py /ruta/al/proyecto [--full-structure]")
        print("     python install_agent_system.py .  # Proyecto actual")
        sys.exit(1)
    
    full_structure = "--full-structure" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    
    if not args:
        print("Falta directorio destino")
        sys.exit(1)
        
    target = Path(args[0]).resolve()
    
    # Auto-detect full-structure if .agent isn't present
    if not full_structure and not (target / ".agent").exists():
        full_structure = True
        
    install(target, full_structure)


if __name__ == "__main__":
    main()


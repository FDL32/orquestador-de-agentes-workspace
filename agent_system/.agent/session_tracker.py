"""Session Tracker Lite para proyectos pequeÃ±os (<30 archivos).

VersiÃ³n simplificada de Session Recovery optimizada para uso local
con proyectos pequeÃ±os. No usa hashes MD5 complejos.

Uso:
    from .session_tracker import save_session, detect_stale_session, recover_session
    
    # Al finalizar
    save_session()
    
    # Al iniciar (detectar sesiÃ³n antigua)
    if detect_stale_session():
        recover_session()
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Rutas
COLLAB_DIR = Path(__file__).parent / "collaboration"
SESSION_FILE = COLLAB_DIR / ".session_state.json"

# ConfiguraciÃ³n
STALE_THRESHOLD_HOURS = 2  # Considerar stale despuÃ©s de 2 horas
MAX_FILES_TO_LIST = 10     # MÃ¡ximo archivos a mostrar en recuperaciÃ³n


def save_session() -> None:
    """Guarda estado simple de la sesiÃ³n actual.
    
    Almacena: timestamp, plan activo, conteo de archivos.
    Para proyectos <30 archivos, esto es suficiente y rÃ¡pido.
    """
    try:
        COLLAB_DIR.mkdir(parents=True, exist_ok=True)
        
        session = {
            "last_activity": datetime.now().isoformat(),
            "active_plan": _get_current_plan_id(),
            "files_count": _count_project_files(),
            "version": "1.0-lite"
        }
        
        SESSION_FILE.write_text(
            json.dumps(session, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except Exception:
        # Silenciosamente ignorar errores de escritura
        pass


def detect_stale_session() -> bool:
    """Detecta si han pasado >2 horas desde la Ãºltima actividad.
    
    Returns:
        True si la sesiÃ³n es antigua (>2h), False en caso contrario
    """
    if not SESSION_FILE.exists():
        return False
    
    try:
        session = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        last_activity = datetime.fromisoformat(session["last_activity"])
        
        return datetime.now() - last_activity > timedelta(hours=STALE_THRESHOLD_HOURS)
    except (json.JSONDecodeError, KeyError, ValueError):
        return False


def recover_session() -> Optional[Dict]:
    """Recupera informaciÃ³n de la sesiÃ³n anterior.
    
    Para proyectos pequeÃ±os, muestra informaciÃ³n simple y Ãºtil
    sin sobrecargar con datos innecesarios.
    
    Returns:
        Dict con informaciÃ³n de la sesiÃ³n o None si no hay sesiÃ³n
    """
    if not SESSION_FILE.exists():
        return None
    
    try:
        session = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        
        # Calcular tiempo transcurrido
        last = datetime.fromisoformat(session["last_activity"])
        elapsed = datetime.now() - last
        hours_ago = elapsed.total_seconds() / 3600
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("ðŸ’¡ SESIÃ“N ANTERIOR DETECTADA")
        print("=" * 60)
        print(f"ðŸ“… Ãšltima actividad: hace {hours_ago:.1f} horas")
        print(f"ðŸ“‹ Plan activo: {session.get('active_plan', 'N/A')}")
        print(f"ðŸ“ Archivos en proyecto: {session.get('files_count', 'N/A')}")
        
        # Listar archivos modificados recientemente (solo para <30 archivos)
        modified = _get_recently_modified_files(hours=int(hours_ago) + 1)
        if modified:
            print(f"\nðŸ“ Archivos modificados:")
            for filepath in modified[:MAX_FILES_TO_LIST]:
                print(f"   â€¢ {filepath}")
            if len(modified) > MAX_FILES_TO_LIST:
                print(f"   ... y {len(modified) - MAX_FILES_TO_LIST} mÃ¡s")
        
        print("=" * 60 + "\n")
        
        return session
        
    except Exception:
        return None


def show_recovery_hint() -> None:
    """Muestra hint suave si hay sesiÃ³n antigua.
    
    VersiÃ³n no intrusiva para mostrar al inicio sin bloquear.
    """
    if detect_stale_session():
        print("ðŸ’¡ Hay una sesiÃ³n anterior (>2h). Usa --recover para ver detalles.")


# ============================================================================
# FUNCIONES AUXILIARES (privadas)
# ============================================================================

def _get_current_plan_id() -> str:
    """Obtiene el ID del plan actual desde work_plan.md."""
    work_plan = COLLAB_DIR / "work_plan.md"
    if not work_plan.exists():
        return "N/A"
    
    try:
        content = work_plan.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if "**ID:**" in line:
                return line.split(":**")[1].strip()
    except Exception:
        pass
    
    return "N/A"


def _count_project_files() -> int:
    """Cuenta archivos relevantes en el proyecto.
    
    Para proyectos <30 archivos, esto es rÃ¡pido.
    """
    project_root = COLLAB_DIR.parent.parent  # .agent/ -> repo/
    
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache"}
    extensions = {".py", ".md", ".json", ".yaml", ".yml", ".toml"}
    
    count = 0
    try:
        for filepath in project_root.rglob("*"):
            if any(part in ignore_dirs for part in filepath.parts):
                continue
            if filepath.is_file() and filepath.suffix in extensions:
                count += 1
                if count > 50:  # Limitar por seguridad
                    break
    except Exception:
        pass
    
    return count


def _get_recently_modified_files(hours: int = 2) -> List[str]:
    """Obtiene archivos modificados en las Ãºltimas N horas.
    
    Para proyectos pequeÃ±os, esto es eficiente.
    """
    project_root = COLLAB_DIR.parent.parent
    cutoff = datetime.now() - timedelta(hours=hours)
    
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache"}
    extensions = {".py", ".md", ".json", ".yaml", ".yml", ".toml"}
    
    modified = []
    
    try:
        for filepath in project_root.rglob("*"):
            if any(part in ignore_dirs for part in filepath.parts):
                continue
            
            if filepath.is_file() and filepath.suffix in extensions:
                try:
                    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if mtime > cutoff:
                        rel_path = filepath.relative_to(project_root)
                        modified.append(str(rel_path))
                except (OSError, ValueError):
                    continue
    except Exception:
        pass
    
    return sorted(modified)


# ============================================================================
# COMANDO DE LÃNEA (para testing)
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "save":
            save_session()
            print("âœ… SesiÃ³n guardada")
        
        elif command == "check":
            if detect_stale_session():
                print("âš ï¸  SesiÃ³n antigua detectada (>2h)")
            else:
                print("âœ… SesiÃ³n reciente o no hay sesiÃ³n")
        
        elif command == "recover":
            result = recover_session()
            if not result:
                print("â„¹ï¸  No hay sesiÃ³n previa para recuperar")
        
        else:
            print(f"Comando desconocido: {command}")
            print("Usa: save | check | recover")
    else:
        # Por defecto: recuperar si existe
        recover_session()


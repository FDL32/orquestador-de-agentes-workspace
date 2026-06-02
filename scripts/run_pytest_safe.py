#!/usr/bin/env python3
"""
run_pytest_safe.py v2.0
Runner robusto de pytest con manejo de errores explÃ­cito, exit codes y logging.
"""

import subprocess
import sys
import logging
from pathlib import Path

# ConfiguraciÃ³n de Logging en .session/
log_dir = Path(".session")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "pytest_runs.log"

# Setup logging con manejo explÃ­cito de handlers para evitar closed file errors
_log_handler = None


def setup_logging():
    """Inicializar logger con file handler."""
    global _log_handler
    _log_handler = logging.FileHandler(log_file, encoding="utf-8")
    _log_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(_log_handler)


def cleanup_logging():
    """Cerrar file handler de forma segura."""
    global _log_handler
    if _log_handler:
        _log_handler.close()
        logging.getLogger().removeHandler(_log_handler)
        _log_handler = None


def resolve_pytest_plan() -> tuple[Path, list[str]]:
    """Elegir el root y los argumentos base de pytest."""
    root_tests = Path("tests")

    if root_tests.exists():
        test_files = list(root_tests.rglob("test_*.py"))
        if test_files:
            return Path("."), ["tests", "-q", "-p", "no:cacheprovider"]
        return Path("."), []
    return Path("."), []


def run_pytest_safe():
    """Ejecutor de pytest con manejo de errores y logging mejorado."""
    # Soporte para chequeo de estado rÃ¡pido
    if "--status" in sys.argv:
        print("[OK] Safe Runner v2.0: Operacional")
        sys.exit(0)

    # Inicializar logging ANTES de imprimir
    setup_logging()

    try:
        print("\n[SAFE_RUNNER] Iniciando suite de tests...")
        logging.info("Iniciando ejecuciÃ³n de run_pytest_safe")

        # 1. Fase de ConfiguraciÃ³n (Exit Code 2 si falla)
        try:
            logging.info("Validando entorno de ejecuciÃ³n...")
            # Verificamos si pytest estÃ¡ disponible
            subprocess.run(["pytest", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            msg = (
                "[ERROR] CONFIG: Pytest no esta instalado o no se encuentra en el PATH."
            )
            print(msg)
            logging.error("Config Error: Pytest environment not found")
            sys.exit(2)
        except Exception as e:
            print(f"[ERROR] Unexpected (Config): {e}")
            logging.error(f"Unexpected Config Error: {e}")
            sys.exit(2)

        # 2. Fase de EjecuciÃ³n (Exit Code 1 si fallan los tests)
        try:
            logging.info("Ejecutando tests...")
            extra_args = sys.argv[1:]
            pytest_cwd, base_args = resolve_pytest_plan()
            if not base_args:
                print("[OK] No test files found under ./tests; skipping pytest run.")
                logging.info("No test files found under ./tests; skipping run.")
                sys.exit(0)

            args = base_args + extra_args

            # EjecuciÃ³n principal
            result = subprocess.run(["pytest"] + args, cwd=pytest_cwd)

            if result.returncode == 0:
                print("\n[OK] EXITO: Todos los tests pasaron correctamente.")
                logging.info("Resultado: Todos los tests pasaron (SUCCESS)")
                sys.exit(0)
            else:
                msg = (
                    f"\n[WARN] FALLO: Algunos tests no pasaron"
                    f" (Codigo de salida pytest: {result.returncode})"
                )
                print(msg)
                logging.warning(
                    f"Resultado: Los tests fallaron (Code {result.returncode})"
                )
                sys.exit(1)

        except Exception as e:
            msg = f"\n[ERROR] EXEC: OcurriÃ³ un fallo critico durante los tests: {e}"
            print(msg)
            logging.error(f"Execution Error: {e}")
            sys.exit(1)

    finally:
        # Limpiar logging de forma segura SIEMPRE
        cleanup_logging()


if __name__ == "__main__":
    run_pytest_safe()


#!/usr/bin/env python3
"""
Orquestador de auditorÃ­a completa del codebase.

Uso:
    python scripts/audit_codebase.py --status  # Health check rÃ¡pido
    python scripts/audit_codebase.py --report  # AnÃ¡lisis completo
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    # Intento de importaciÃ³n como paquete
    from scripts.state_drift import check_state_drift
except (ImportError, ModuleNotFoundError):
    # Fallback para ejecuciÃ³n directa desde el directorio scripts/
    from state_drift import check_state_drift


@dataclass
class Finding:
    archivo: str
    lineas: int  # LÃ­neas totales del archivo
    herramienta: str
    tipo: str
    linea: int | None
    simbolo: str
    usos: int
    commits: int
    accion: str


def parse_arguments():
    parser = argparse.ArgumentParser(description="AuditorÃ­a completa del codebase")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", action="store_true", help="Health check rÃ¡pido")
    group.add_argument("--report", action="store_true", help="AnÃ¡lisis completo")
    return parser.parse_args()


def list_python_files() -> list[Path]:
    """Listar archivos Python usando pathlib."""
    return list(Path(".").rglob("*.py"))


def run_health_check() -> int:
    """Health check: ejecutar herramientas y verificar que no fallen."""
    try:
        # Drift check (Warning only)
        if not check_state_drift():
            print("Warning: State drift detected, but continuing health check")
            # No return 1 aquÃ­ - permitir que continÃºe para validaciÃ³n tÃ©cnica completa

        from deadcode.actions.parse_arguments import parse_arguments
        from deadcode.actions.find_python_filenames import find_python_filenames
        from deadcode.actions.find_unused_names import find_unused_names

        try:
            args = parse_arguments(
                [".", "--exclude", "venv,.venv,__pycache__,.git,agent_system,.agent"]
            )
            files = find_python_filenames(args)
            unused_items = list(
                find_unused_names(files, args)
            )  # Validar que se puede ejecutar sin acceder .ruff_cache
            print(f"Deadcode found {len(unused_items)} unused items")
        except Exception as e:
            print(f"Deadcode failed: {e}")
            return 1

        # Ruff enfocado al hardening de esta WP para evitar ruido legacy del repo.
        try:
            focus_files = [
                Path("scripts/audit_codebase.py"),
                Path("scripts/run_pytest_safe.py"),
                Path("scripts/state_drift.py"),
                Path("scripts/artifact_graph.py"),
            ]
            ruff_targets = [str(path) for path in focus_files if path.exists()]
            if not ruff_targets:
                print(
                    "Warning: No focused ruff targets found, skipping lint validation"
                )
            else:
                result = subprocess.run(
                    ["ruff", "check", "--no-cache", *ruff_targets],
                    capture_output=True,
                    text=False,
                    cwd=".",
                    timeout=60,
                )
                if result.returncode != 0:  # 0=OK, !=0=issues detected
                    stdout = (
                        result.stdout.decode("utf-8", errors="replace")
                        if result.stdout
                        else ""
                    )
                    stderr = (
                        result.stderr.decode("utf-8", errors="replace")
                        if result.stderr
                        else ""
                    )
                    message = stdout if stdout else stderr
                    message = message.encode("ascii", errors="replace").decode("ascii")
                    print(f"Ruff issues detected: {message}")
                    return 1
        except subprocess.TimeoutExpired:
            print("Ruff timed out (likely .ruff_cache permission issue)")
            return 1
        except Exception as e:
            print(f"Ruff error: {e}")
            return 1

        # Git
        result = subprocess.run(
            ["git", "status"], capture_output=True, text=True, cwd="."
        )
        if result.returncode != 0:
            print("Warning: Not a git repository, skipping git validation")
            # Permitir que continÃºe en lugar de retornar 1

        print("Health check passed: all tools executed successfully")
        return 0

    except Exception as e:
        print(f"Health check failed: {e}")
        return 1


def run_vulture() -> list[Finding]:
    """Ejecutar vulture (sin capturar output por issues de encoding en Windows)."""
    findings = []
    try:
        result = subprocess.run(
            [
                "uv",
                "run",
                "vulture",
                ".",
                "--exclude",
                "venv,.venv",
                "--min-confidence",
                "80",
                "--sort-by-size",
            ],
            cwd=".",
            timeout=30,
        )
        if result.returncode in (0, 1):
            print(
                "Vulture executed successfully (output not captured due to Windows encoding issues)"
            )
        else:
            print("Vulture failed to execute")
    except subprocess.TimeoutExpired:
        print("Vulture timed out")
    except Exception as e:
        print(f"Error running vulture: {e}")

    return findings  # No findings captured


def run_deadcode() -> list[Finding]:
    """Ejecutar deadcode usando librerÃ­a."""
    findings = []
    try:
        from deadcode.actions.parse_arguments import parse_arguments
        from deadcode.actions.find_python_filenames import find_python_filenames
        from deadcode.actions.find_unused_names import find_unused_names

        args = parse_arguments(
            [".", "--exclude", "venv,.venv,__pycache__,.git,agent_system,.agent"]
        )
        files = find_python_filenames(args)
        unused_items = find_unused_names(files, args)

        for item in unused_items:
            findings.append(
                Finding(
                    archivo=str(item.filename),
                    lineas=get_file_line_count(str(item.filename)),
                    herramienta="deadcode",
                    tipo=str(item.type_),
                    linea=item.name_line,
                    simbolo=item.name,
                    usos=item.number_of_uses,
                    commits=get_git_commits(str(item.filename)),
                    accion="DEAD",
                )
            )
    except Exception as e:
        print(f"Error running deadcode: {e}")

    return findings


def get_file_line_count(filepath: str) -> int:
    """Contar lÃ­neas de un archivo."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_git_commits(filepath: str) -> int:
    """Contar commits para un archivo."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--follow", "--", filepath],
            capture_output=True,
            text=True,
            cwd=".",
        )
        if result.returncode == 0:
            return (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )
        return 0
    except Exception:
        return 0


def run_ruff() -> list[Finding]:
    """Ejecutar ruff y parsear deuda tÃ©cnica."""
    findings = []
    try:
        result = subprocess.run(
            ["ruff", "check", ".", "--exclude", "venv,.venv"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        # Parsear output: formato "file.py:line:col: code message"
        for line in (result.stdout or "").strip().split("\n"):
            if not line.strip():
                continue
            try:
                parts = line.split(":")
                if len(parts) >= 4:
                    archivo = parts[0]
                    linea = int(parts[1])
                    code = parts[3].strip()
                    findings.append(
                        Finding(
                            archivo=archivo,
                            lineas=get_file_line_count(archivo),
                            herramienta="ruff",
                            tipo="lint",
                            linea=linea,
                            simbolo=code,
                            usos=1,  # Not applicable
                            commits=get_git_commits(archivo),
                            accion="SMELL",
                        )
                    )
            except (ValueError, IndexError):
                continue
    except Exception as e:
        print(f"Error running ruff: {e}")

    return findings


def categorize_findings(findings: list[Finding]) -> list[Finding]:
    """Categorizar findings: DEAD | LEGACY | ABANDONED | SMELL."""
    for f in findings:
        if f.herramienta in ("vulture", "deadcode") and f.commits == 0:
            f.accion = "DEAD"
        elif f.herramienta in ("vulture", "deadcode") and f.commits < 5:
            f.accion = "ABANDONED"
        elif f.herramienta in ("vulture", "deadcode") and f.commits >= 5:
            f.accion = "LEGACY"
        elif f.herramienta == "ruff":
            f.accion = "SMELL"
        # Else keep as is
    return findings


def generate_report(findings: list[Finding]):
    """Generar tabla Markdown."""
    session_dir = Path(".session")
    session_dir.mkdir(exist_ok=True)
    report_path = session_dir / "audit_report.md"

    with open(report_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("# Audit Report\n\n")
        file_handle.write(
            "| Archivo | LÃ­neas | Herramienta | Tipo | LÃ­nea | SÃ­mbolo | Usos | Commits | AcciÃ³n |\n"
        )
        file_handle.write(
            "|---------|--------|-------------|------|-------|---------|------|---------|--------|\n"
        )

        for finding in sorted(findings, key=lambda x: (x.archivo, x.linea or 0)):
            file_handle.write(
                f"| {finding.archivo} | {finding.lineas} | {finding.herramienta} | {finding.tipo} | {finding.linea or ''} | {finding.simbolo} | {finding.usos} | {finding.commits} | {finding.accion} |\n"
            )

    print(f"Report generated: {report_path}")


def run_full_audit():
    """AnÃ¡lisis completo."""
    print("Running full audit...")

    findings = []
    findings.extend(run_vulture())
    findings.extend(run_deadcode())
    findings.extend(run_ruff())

    # Agregar git activity para todos los archivos Python
    python_files = list_python_files()
    for pf in python_files:
        commits = get_git_commits(str(pf))
        if commits == 0:  # Archivos nuevos o no committed
            findings.append(
                Finding(
                    archivo=str(pf),
                    lineas=get_file_line_count(str(pf)),
                    herramienta="git",
                    tipo="file",
                    linea=None,
                    simbolo="uncommitted",
                    usos=0,
                    commits=commits,
                    accion="ABANDONED",
                )
            )

    findings = categorize_findings(findings)
    generate_report(findings)
    print("Audit complete.")


def main():
    args = parse_arguments()

    if args.status:
        sys.exit(run_health_check())
    elif args.report:
        run_full_audit()


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Detector de desalineaciÃ³n (drift) entre artefactos de sesiÃ³n.
"""

from __future__ import annotations

import sys
from pathlib import Path


TERMINAL_STATUSES = {"COMPLETED", "READY_FOR_CLOSEOUT"}


def extract_status(content: str) -> str:
    """Extrae el estado normalizado del contenido."""
    content_upper = content.upper()
    if "READY_FOR_CLOSEOUT" in content_upper:
        return "READY_FOR_CLOSEOUT"
    if "ESTADO: COMPLETED" in content_upper or "COMPLETED" in content_upper:
        return "COMPLETED"
    if (
        "ESTADO: READY_FOR_REVIEW" in content_upper
        or "READY_FOR_REVIEW" in content_upper
    ):
        return "READY_FOR_REVIEW"
    if "ESTADO: IN_PROGRESS" in content_upper or "IN_PROGRESS" in content_upper:
        return "IN_PROGRESS"
    return "UNKNOWN"


def check_state_drift() -> bool:
    """Verifica la consistencia entre work_plan, execution_log y TURN."""
    session_dir = Path(".session")
    wp_path = session_dir / "work_plan.md"
    log_path = session_dir / "execution_log.md"
    turn_path = session_dir / "TURN.md"

    if not wp_path.exists():
        return True

    wp_content = wp_path.read_text(encoding="utf-8")
    log_content = log_path.read_text(encoding="utf-8") if log_path.exists() else ""

    wp_status = extract_status(wp_content)
    log_status = extract_status(log_content)
    wp_upper = wp_content.upper()
    log_upper = log_content.upper()

    issues: list[str] = []

    if wp_status == "COMPLETED" and log_status != "COMPLETED":
        issues.append(
            "Drift: work_plan dice COMPLETED pero execution_log no estÃ¡ sincronizado."
        )
    elif wp_status == "READY_FOR_REVIEW" and log_status == "COMPLETED":
        issues.append(
            "Drift: work_plan en READY_FOR_REVIEW pero execution_log ya cerrado."
        )
    elif wp_status == "READY_FOR_CLOSEOUT" and log_status not in TERMINAL_STATUSES:
        issues.append(
            "Drift: work_plan en READY_FOR_CLOSEOUT pero execution_log aÃºn no estÃ¡ cerrado."
        )

    if (
        turn_path.exists()
        and wp_status not in TERMINAL_STATUSES
        and log_status not in TERMINAL_STATUSES
    ):
        turn_content = turn_path.read_text(encoding="utf-8").upper()
        current_turn = "MANAGER" if "MANAGER" in turn_content else "BUILDER"
        expected_status = (
            "READY_FOR_REVIEW" if current_turn == "MANAGER" else "IN_PROGRESS"
        )
        if expected_status not in log_upper and expected_status not in wp_upper:
            issues.append(
                f"Drift: Turno del {current_turn} pero no hay {expected_status} marcado."
            )

    fases_wp = wp_content.count("### Fase")
    fases_log = log_content.count("## Fase") + log_content.count("### Fase")
    if (
        wp_status not in TERMINAL_STATUSES
        and log_status not in TERMINAL_STATUSES
        and abs(fases_log - fases_wp) > 1
    ):
        issues.append(
            f"Drift: execution_log tiene {fases_log} fases vs plan {fases_wp}."
        )

    if issues:
        print("\n[CRITICAL] State Drift Detected:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return False

    print("[OK] State alignment verified.")
    return True


if __name__ == "__main__":
    sys.exit(0 if check_state_drift() else 1)


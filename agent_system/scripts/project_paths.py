#!/usr/bin/env python3
"""
Project paths resolution helper.

Centralized logic for resolving canonical project root and agent directory.
Detects path drift and ensures consistent path handling across scripts.
"""

from pathlib import Path
from typing import Dict, Optional


class ProjectPathsResolver:
    """Resolve canonical project paths and detect drift."""

    def __init__(self, start_dir: str | Path):
        self.start_path = Path(start_dir).resolve()
        if not self.start_path.exists():
            raise FileNotFoundError(f"Start directory not found: {start_dir}")

    def resolve_paths(self) -> Dict[str, str | bool]:
        """
        Resolve canonical project root and agent directory.

        Returns dict with:
        - project_root: str | None
        - agent_dir: str | None
        - drift_detected: bool
        - drift_type: str | None ('multiple_agent_dirs', 'agent_not_at_root', 'none')
        - message: str

        Drift is detected if:
        - Multiple .agent/ directories found in the tree
        - .agent/ not at project root (though we still resolve it)
        """
        # Find project root by searching upwards for .agent
        project_root = self._find_project_root(self.start_path)
        if not project_root:
            return {
                "project_root": None,
                "agent_dir": None,
                "drift_detected": False,
                "drift_type": None,
                "message": "No .agent directory found"
            }

        agent_dir = project_root / ".agent"

        # Check for drift: multiple .agent in the tree
        all_agent_dirs = list(self.start_path.rglob(".agent"))
        all_agent_dirs = [d for d in all_agent_dirs if d.is_dir()]

        drift_detected = False
        drift_type = "none"

        if len(all_agent_dirs) > 1:
            drift_detected = True
            drift_type = "multiple_agent_dirs"
        elif self.start_path != project_root and (self.start_path / ".agent").exists():
            # Started from subdir that has its own .agent, but canonical is elsewhere
            drift_detected = True
            drift_type = "agent_not_at_root"

        message = "Paths resolved successfully"
        if drift_detected:
            if drift_type == "multiple_agent_dirs":
                message = f"Multiple .agent directories found: {[str(d) for d in all_agent_dirs]}"
            elif drift_type == "agent_not_at_root":
                message = f"Local .agent at {self.start_path}, but canonical at {project_root}"

        return {
            "project_root": str(project_root),
            "agent_dir": str(agent_dir),
            "drift_detected": drift_detected,
            "drift_type": drift_type,
            "message": message
        }

    def _find_project_root(self, start_path: Path) -> Optional[Path]:
        """Find project root by searching upwards for .agent directory."""
        current = start_path
        while current != current.parent:
            if (current / ".agent").exists():
                return current
            current = current.parent
        return None

    def get_project_root(self) -> Optional[Path]:
        """Get canonical project root path."""
        result = self.resolve_paths()
        if result["project_root"]:
            return Path(result["project_root"])
        return None

    def get_agent_dir(self) -> Optional[Path]:
        """Get canonical agent directory path."""
        result = self.resolve_paths()
        if result["agent_dir"]:
            return Path(result["agent_dir"])
        return None

    def has_drift(self) -> bool:
        """Check if path drift is detected."""
        return self.resolve_paths()["drift_detected"]

    def get_drift_info(self) -> Dict:
        """Get drift information."""
        result = self.resolve_paths()
        return {
            "drift_detected": result["drift_detected"],
            "drift_type": result["drift_type"],
            "message": result["message"]
        }

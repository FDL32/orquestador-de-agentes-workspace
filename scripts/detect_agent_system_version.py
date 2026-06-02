#!/usr/bin/env python3
"""
Detect z_scripts agent system version by architectural patterns.

Usage:
  python scripts/detect_agent_system_version.py /path/to/project
  python scripts/detect_agent_system_version.py .  # Current directory
"""

import json
from pathlib import Path
from typing import Tuple, Dict, List


class AgentSystemDetector:
    """Detect agent system version by fingerprinting project structure."""

    # Markers for each version
    MARKERS = {
        "v8.x": {
            "required": [".agent/agent_controller.py", "scripts/run_pytest_safe.py"],
            "optional": [".agent/hooks/guard_paths.py", ".agent/collaboration/"],
            "absent": [".agent/rules", "skills", "AGENTS.md", "orquestacion_agentes"],
        },
        "v9.0-v9.1": {
            "required": [
                ".agent/agent_controller.py",
                ".agent/rules/",
                "skills/",
                "CLAUDE.md",
            ],
            "optional": ["scripts/discover_skills.py", ".agent/collaboration/"],
            "absent": [".claude/rules", "AGENTS.md", "agent_system/refactor_kit"],
        },
        "v9.2": {
            "required": [
                ".agent/agent_controller.py",
                ".agent/rules/",
                "skills/",
                "agent_system/refactor_kit/",
                "CLAUDE.md",
            ],
            "optional": ["orquestacion_agentes/", "AGENTS.md"],
            "absent": [".claude/rules"],  # Pre-9.2.1
        },
        "v9.2.1+": {
            "required": [
                ".agent/agent_controller.py",
                ".agent/rules/",
                ".claude/rules/",
                "skills/",
                "agent_system/refactor_kit/",
                "AGENTS.md",
                "CLAUDE.md",
            ],
            "optional": ["orquestacion_agentes/", ".version_manifest.json"],
            "absent": [],
        },
        "v9.4": {
            "required": [
                ".agent/agent_controller.py",
                ".agent/rules/",
                ".claude/rules/",
                "skills/",
                "agent_system/refactor_kit/",
                "AGENTS.md",
                "CLAUDE.md",
                "QUICKSTART.md",
            ],
            "optional": ["orquestacion_agentes/", ".version_manifest.json"],
            "absent": [],
        },
    }

    def __init__(self, project_dir: str):
        self.project_path = Path(project_dir).resolve()
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")

    def has_multi_agent_system(self) -> bool:
        """Check if project has any version of the agent system."""
        return (self.project_path / ".agent" / "agent_controller.py").exists()

    def check_markers(self, version: str) -> Tuple[bool, Dict]:
        """Check if project matches markers for a specific version."""
        markers = self.MARKERS.get(version)
        if not markers:
            return False, {}

        required_met = all(
            (self.project_path / marker).exists() for marker in markers["required"]
        )

        optional_met = sum(
            1 for marker in markers["optional"] if (self.project_path / marker).exists()
        )

        absent_violated = any(
            (self.project_path / marker).exists() for marker in markers["absent"]
        )

        return (required_met and not absent_violated), {
            "required_met": required_met,
            "optional_met": optional_met,
            "optional_total": len(markers["optional"]),
            "absent_violated": absent_violated,
        }

    def detect_version(self) -> Dict:
        """Detect project version with confidence score."""
        if not self.has_multi_agent_system():
            return {
                "detected": False,
                "message": "No agent system found (.agent/ not present)",
            }

        results = {}
        for version in ["v9.4", "v9.2.1+", "v9.2", "v9.0-v9.1", "v8.x"]:
            matches, details = self.check_markers(version)
            results[version] = {"matches": matches, **details}

        # Find best match
        best_match = None
        for version, result in results.items():
            if result["matches"]:
                best_match = version
                break

        if best_match:
            return {
                "detected": True,
                "version": best_match,
                "confidence": "high",
                "details": results[best_match],
            }
        else:
            # Partial match - find closest
            closest = max(
                results.items(),
                key=lambda x: (x[1]["required_met"], x[1]["optional_met"]),
            )
            return {
                "detected": True,
                "version": closest[0],
                "confidence": "low",
                "message": "Partial match - system may be customized or corrupted",
                "details": closest[1],
            }

    def suggest_upgrade_path(self, detected_version: str) -> str:
        """Suggest upgrade path from detected version."""
        paths = {
            "v8.x": "v8.x -> v9.0-v9.1 -> v9.2 -> v9.2.1+ -> v9.4",
            "v9.0-v9.1": "v9.0-v9.1 -> v9.2 -> v9.2.1+ -> v9.4",
            "v9.2": "v9.2 -> v9.2.1+ -> v9.4",
            "v9.2.1+": "v9.2.1+ -> v9.4",
            "v9.4": "Already latest",
        }
        return paths.get(detected_version, "Unknown")

    def create_version_manifest(self, version: str) -> Dict:
        """Create .version_manifest.json for detected version."""
        manifest = {
            "version": version,
            "detected_date": __import__("datetime").datetime.now().isoformat(),
            "detected_by": "detect_agent_system_version.py",
            "confidence": "auto-detected",
            "markers_matched": self._get_matched_markers(version),
        }
        return manifest

    def _get_matched_markers(self, version: str) -> List[str]:
        """Get list of markers that matched for a version."""
        matched = []
        markers = self.MARKERS.get(version, {})
        for marker in markers.get("required", []):
            if (self.project_path / marker).exists():
                matched.append(marker)
        return matched


def main():
    import sys

    if len(sys.argv) < 2:
        project_dir = "."
    else:
        project_dir = sys.argv[1]

    print("=== AGENT SYSTEM VERSION DETECTION ===\n")
    print(f"Project: {Path(project_dir).resolve()}\n")

    detector = AgentSystemDetector(project_dir)
    result = detector.detect_version()

    if result["detected"]:
        version = result["version"]
        confidence = result.get("confidence", "unknown")

        print(f"Detected Version: {version}")
        print(f"Confidence: {confidence}")
        print(f"Upgrade Path: {detector.suggest_upgrade_path(version)}\n")

        if "details" in result:
            details = result["details"]
            print("Diagnostic:")
            print(f"  Required markers met: {details.get('required_met')}")
            print(
                f"  Optional markers: {details.get('optional_met')}/{details.get('optional_total')}"
            )
            print(f"  No conflicts: {not details.get('absent_violated')}")

        # Create manifest file
        manifest_path = Path(project_dir) / ".agent" / ".version_manifest.json"
        manifest = detector.create_version_manifest(version)

        # Don't overwrite if exists (preserve history)
        if not manifest_path.exists():
            manifest_path.write_text(json.dumps(manifest, indent=2))
            print(f"\nCreated: {manifest_path}")

        return 0
    else:
        print(result.get("message", "Unknown error"))
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())


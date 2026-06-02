#!/usr/bin/env python3
"""
Skill Discovery System â€” Finds and indexes skills with triggers.

Generates trigger_map for orquestador.py (v2.4+) and external agents (Goose, Claw).
"""

import json
import sys
from pathlib import Path
from typing import Any


def extract_frontmatter(path: Path) -> dict[str, Any]:
    """Extract YAML frontmatter from SKILL.md"""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return {}

        _, fm, _ = content.split("---", 2)
        data: dict[str, Any] = {}

        for line in fm.strip().split("\n"):
            if ": " in line:
                key, val = line.split(": ", 1)
                key = key.strip()
                val = val.strip()

                # Parse arrays (triggers: [/impl, implement])
                if val.startswith("[") and val.endswith("]"):
                    val = [t.strip() for t in val[1:-1].split(",")]

                data[key] = val

        return data
    except Exception:
        return {}


def discover_skills(skills_dir: Path = Path("skills")) -> dict[str, Any]:
    """Discover all skills and their triggers."""

    if not skills_dir.exists():
        return {"skills": [], "trigger_map": {}}

    skills: list[dict[str, Any]] = []
    trigger_map: dict[str, str] = {}

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        fm = extract_frontmatter(skill_file)
        skill_name = fm.get("name", skill_dir.name)
        triggers = fm.get("triggers", [])

        # Normalize triggers to list
        if isinstance(triggers, str):
            triggers = [triggers]

        skill_entry = {
            "name": skill_name,
            "path": str(skill_dir),
            "triggers": triggers,
            "version": fm.get("version", "1.0.0"),
            "description": fm.get("description", ""),
        }
        skills.append(skill_entry)

        # Map each trigger to skill path
        for trigger in triggers:
            trigger_map[trigger] = str(skill_file)

    return {
        "skills": skills,
        "trigger_map": trigger_map,
        "total_skills": len(skills),
        "total_triggers": len(trigger_map),
    }


def main() -> None:
    """CLI entry point."""

    result = discover_skills()

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    elif "--goose" in sys.argv:
        # Format for .goosehints consumption
        print("# Available Triggers for Goose\n")
        for trigger, path in sorted(result["trigger_map"].items()):
            print(f"- **{trigger}** -> {path}")
    else:
        # Table format
        print("\nSKILL DISCOVERY RESULTS\n")
        print(f"Total Skills: {result['total_skills']}")
        print(f"Total Triggers: {result['total_triggers']}\n")

        if result["skills"]:
            print("| Skill | Triggers | Version |")
            print("|-------|----------|---------|")
            for skill in result["skills"]:
                triggers_str = (
                    ", ".join(skill["triggers"]) if skill["triggers"] else "â€”"
                )
                print(f"| {skill['name']} | {triggers_str} | {skill['version']} |")
        else:
            print("No skills found in skills/ directory")


if __name__ == "__main__":
    main()


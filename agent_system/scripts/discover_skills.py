#!/usr/bin/env python3
"""Descubrimiento automÃ¡tico de skills y extracciÃ³n de triggers.

Genera un Ã­ndice de skills con triggers para que agentes externos (Goose, etc)
puedan invocar skills por palabra clave.

Uso:
    python discover_skills.py              # Imprime tabla de skills + triggers
    python discover_skills.py --json       # JSON con mapeo trigger â†’ skill
    python discover_skills.py --goose      # Formato optimizado para .goosehints
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def extract_frontmatter(content: str) -> Optional[Dict[str, any]]:
    """Extrae el frontmatter YAML de un archivo Markdown."""
    lines = content.split('\n')
    if len(lines) < 3 or lines[0].strip() != '---':
        return None

    frontmatter_lines = []
    i = 1
    while i < len(lines) and lines[i].strip() != '---':
        frontmatter_lines.append(lines[i])
        i += 1

    if i >= len(lines) or lines[i].strip() != '---':
        return None

    frontmatter_text = '\n'.join(frontmatter_lines)

    try:
        import yaml
        return yaml.safe_load(frontmatter_text)
    except ImportError:
        # Fallback simple para campos bÃ¡sicos
        frontmatter = {}
        for line in frontmatter_lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('[') and value.endswith(']'):
                    # Lista simple
                    value = [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                frontmatter[key] = value
        return frontmatter


def discover_all_skills(skills_dir: Path) -> Dict:
    """Descubre todas las skills y extrae su metadata incluyendo triggers."""
    skills = []
    trigger_map = {}

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)

            if not frontmatter or 'name' not in frontmatter:
                continue

            skill_info = {
                'name': frontmatter.get('name'),
                'path': str(skill_md.relative_to(skills_dir.parent)),
                'version': frontmatter.get('version', '1.0.0'),
                'description': frontmatter.get('description', ''),
                'triggers': frontmatter.get('triggers')
            }

            skills.append(skill_info)

            # Agregar al trigger_map si tiene triggers
            if skill_info['triggers']:
                for trigger in skill_info['triggers']:
                    trigger_map[trigger] = {
                        'skill': skill_info['name'],
                        'path': skill_info['path']
                    }

        except Exception as e:
            print(f"Error procesando {skill_md}: {e}", file=sys.stderr)
            continue

    return {
        'timestamp': datetime.now().isoformat(),
        'total_skills': len(skills),
        'skills_with_triggers': len([s for s in skills if s['triggers']]),
        'skills': skills,
        'trigger_map': trigger_map
    }


def print_table(data: Dict):
    """Imprime tabla de skills."""
    print("INDICE DE SKILLS")
    print("=" * 80)
    print(f"{'SKILL':<25} {'VER':<8} {'TRIGGERS':<35} {'DESCRIPCION'}")
    print("-" * 80)

    for skill in data['skills']:
        triggers_str = ', '.join(skill['triggers']) if skill['triggers'] else 'Ninguno'
        desc_str = skill['description'][:30] + '...' if len(skill['description']) > 30 else skill['description']
        print(f"{skill['name']:<25} {skill['version']:<8} {triggers_str:<35} {desc_str}")

    print("=" * 80)
    print(f"Total skills: {data['total_skills']}")
    print(f"Con triggers: {data['skills_with_triggers']}")


def print_goose_format(data: Dict):
    """Formato optimizado para .goosehints."""
    print("## Triggers Disponibles")
    print()

    if data['trigger_map']:
        print("```")
        for trigger, info in data['trigger_map'].items():
            print(f"{trigger:<15} -> {info['path']}")
        print("```")
    else:
        print("NingÃºn trigger definido aÃºn.")

    print()
    print("**Nota:** Ejecuta `python scripts/discover_skills.py --json` para obtener la lista mÃ¡s reciente.")


def print_markdown_table(data: Dict):
    """Genera tabla Markdown para README con lista de skills."""

    print("| Skill | DescripciÃ³n | Tipo | Triggers | Status |")
    print("|-------|-------------|------|----------|--------|")

    for skill in sorted(data['skills'], key=lambda s: s['name']):
        name = skill['name']
        desc = skill['description'][:50]

        if name.startswith('man-'):
            skill_type = "Manager"
        elif name.startswith('bui-'):
            skill_type = "Builder"
        else:
            skill_type = "Meta"

        if skill['triggers']:
            triggers = ', '.join(skill['triggers'][:2])
            if len(skill['triggers']) > 2:
                triggers += "..."
        else:
            triggers = "-"

        status = "OK"

        print(f"| `{name}` | {desc} | {skill_type} | {triggers} | {status} |")

    print()
    print("**Nota:** Para triggers completos: `python scripts/discover_skills.py --goose`")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Discover and display agent skills')
    parser.add_argument('--json', action='store_true', help='Output skills data as JSON')
    parser.add_argument('--goose', action='store_true', help='Output skills in Goose format')
    parser.add_argument('--markdown', action='store_true', help='Generate markdown table for README.md')

    args = parser.parse_args()

    skills_dir = Path(__file__).parent.parent / 'skills'

    if not skills_dir.exists():
        print(f"Error: Directorio {skills_dir} no existe", file=sys.stderr)
        sys.exit(1)

    data = discover_all_skills(skills_dir)

    if args.markdown:
        print_markdown_table(data)
    elif args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.goose:
        print_goose_format(data)
    else:
        print_goose_format(data)

if __name__ == '__main__':
    main()

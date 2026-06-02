#!/usr/bin/env python3
"""Validador de micro-skills del sistema multi-agente.

Verifica que cada SKILL.md tenga frontmatter YAML vÃ¡lido con los campos requeridos:
- name: nombre de la skill
- version: versiÃ³n semÃ¡ntica
- description: descripciÃ³n breve
- author: autor de la skill
- tags: lista de etiquetas

Uso:
    python validate_all.py              # Valida todas las skills
    python validate_all.py --verbose    # Muestra detalles de cada skill
    python validate_all.py --json       # Output en formato JSON
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Campos obligatorios en el frontmatter
REQUIRED_FIELDS = {"name", "version", "description", "author", "tags"}

# Directorio base de skills
SKILLS_DIR = Path(__file__).parent


def extract_frontmatter(content: str) -> Optional[Dict[str, any]]:
    """Extrae el frontmatter YAML del contenido de un SKILL.md.
    
    El frontmatter debe estar delimitado por --- al inicio y final.
    
    Args:
        content: Contenido completo del archivo SKILL.md
        
    Returns:
        Diccionario con el frontmatter parseado, o None si no existe o es invÃ¡lido
    """
    # Buscar patrÃ³n ---\n...\n---
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    frontmatter_text = match.group(1)
    result = {}
    
    # Parsear lÃ­neas del frontmatter
    for line in frontmatter_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Buscar patrÃ³n key: value
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            # Parsear listas (tags: [item1, item2])
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
            else:
                # Quitar comillas si existen
                value = value.strip('"').strip("'")
            
            result[key] = value
    
    return result


def validate_skill(skill_dir: Path) -> Tuple[bool, List[str]]:
    """Valida una skill individual.
    
    Args:
        skill_dir: Ruta al directorio de la skill
        
    Returns:
        Tupla (es_vÃ¡lida, lista_de_errores)
    """
    errors = []
    skill_name = skill_dir.name
    
    # Verificar que existe SKILL.md
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return False, [f"No existe SKILL.md"]
    
    # Leer contenido
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error leyendo archivo: {e}"]
    
    # Extraer frontmatter
    frontmatter = extract_frontmatter(content)
    if frontmatter is None:
        return False, [f"No se encontrÃ³ frontmatter YAML vÃ¡lido (debe iniciar con ---)"]
    
    # Verificar campos requeridos
    missing_fields = REQUIRED_FIELDS - set(frontmatter.keys())
    if missing_fields:
        errors.append(f"Faltan campos obligatorios: {', '.join(sorted(missing_fields))}")
    
    # Validar tipos y contenido
    if "name" in frontmatter:
        name = frontmatter["name"]
        if not name or not isinstance(name, str):
            errors.append("El campo 'name' debe ser un string no vacÃ­o")
        elif " " in name:
            errors.append("El campo 'name' no debe contener espacios (usar kebab-case)")
    
    if "version" in frontmatter:
        version = frontmatter["version"]
        # Validar formato semver simple (X.Y.Z)
        if not re.match(r"^\d+\.\d+\.\d+$", str(version)):
            errors.append("El campo 'version' debe seguir formato semver (X.Y.Z)")
    
    if "tags" in frontmatter:
        tags = frontmatter["tags"]
        if not isinstance(tags, list):
            errors.append("El campo 'tags' debe ser una lista")
    elif len(tags) == 0:
        errors.append("El campo 'tags' no debe estar vacÃ­o")

    # Validar triggers si estÃ¡ presente (OPCIONAL)
    if "triggers" in frontmatter:
        triggers = frontmatter["triggers"]
        if not isinstance(triggers, list):
            errors.append("El campo 'triggers' debe ser una lista (si estÃ¡ presente)")
        elif len(triggers) == 0:
            errors.append("El campo 'triggers' no debe estar vacÃ­o (si estÃ¡ presente)")
        elif not all(isinstance(t, str) for t in triggers):
            errors.append("Todos los elementos en 'triggers' deben ser strings")

    # Verificar que existe carpeta references/
    references_dir = skill_dir / "references"
    if not references_dir.exists():
        errors.append("No existe carpeta 'references/'")
    
    return len(errors) == 0, errors


def validate_all_skills(verbose: bool = False) -> Dict:
    """Valida todas las skills en el directorio.
    
    Args:
        verbose: Si es True, muestra informaciÃ³n detallada
        
    Returns:
        Diccionario con resultados de la validaciÃ³n
    """
    results = {
        "total": 0,
        "valid": 0,
        "invalid": 0,
        "skills": []
    }
    
    # Encontrar todos los directorios de skills
    skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    
    for skill_dir in sorted(skill_dirs):
        # Ignorar directorios especiales
        if skill_dir.name in ["__pycache__", "scripts"]:
            continue
        
        results["total"] += 1
        is_valid, errors = validate_skill(skill_dir)
        
        skill_result = {
            "name": skill_dir.name,
            "valid": is_valid,
            "errors": errors
        }
        results["skills"].append(skill_result)
        
        if is_valid:
            results["valid"] += 1
        else:
            results["invalid"] += 1
    
    return results


def print_results(results: Dict, verbose: bool = False) -> None:
    """Imprime los resultados de la validaciÃ³n.
    
    Args:
        results: Diccionario con resultados
        verbose: Si es True, muestra detalles de cada skill
    """
    print("=" * 60)
    print("ðŸ” VALIDACIÃ“N DE MICRO-SKILLS")
    print("=" * 60)
    print(f"\nðŸ“Š Resumen:")
    print(f"   Total: {results['total']}")
    print(f"   âœ… VÃ¡lidas: {results['valid']}")
    print(f"   âŒ InvÃ¡lidas: {results['invalid']}")
    
    if verbose or results['invalid'] > 0:
        print(f"\nðŸ“‹ Detalles por skill:")
        for skill in results["skills"]:
            status = "âœ…" if skill["valid"] else "âŒ"
            print(f"\n   {status} {skill['name']}")
            
            if not skill["valid"]:
                for error in skill["errors"]:
                    print(f"      - {error}")
            elif verbose:
                print(f"      - OK")
    
    print("\n" + "=" * 60)
    
    if results['invalid'] == 0:
        print("ðŸŽ‰ Â¡Todas las skills son vÃ¡lidas!")
    else:
        print(f"âš ï¸  {results['invalid']} skill(s) con errores")
    
    print("=" * 60)


def main():
    """FunciÃ³n principal."""
    # Fix encoding issues on Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    verbose = "--verbose" in sys.argv
    json_output = "--json" in sys.argv
    
    results = validate_all_skills(verbose=verbose)
    
    if json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_results(results, verbose=verbose)
    
    # Exit code: 0 si todo vÃ¡lido, 1 si hay errores
    sys.exit(0 if results['invalid'] == 0 else 1)


if __name__ == "__main__":
    main()


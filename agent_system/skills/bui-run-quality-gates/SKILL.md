---
name: bui-run-quality-gates
version: 1.0.0
description: Skill para que el Builder ejecute validaciÃ³n completa de cÃ³digo con ruff, pytest y verificaciÃ³n de seguridad
author: agent-system
tags: [builder, testing, quality, linting, security]
triggers: [/gates, /quality, quality-gates]
allowed-tools: [Bash]
---

# bui-run-quality-gates

Skill para ejecutar validaciÃ³n completa de cÃ³digo antes de solicitar revisiÃ³n.

## Overview

Antes de marcar trabajo como `ðŸŸ£ READY_FOR_REVIEW`, el Builder debe ejecutar Quality Gates para asegurar calidad.

## Workflow

### Paso 0: Verificar Pre-condiciones
- CÃ³digo implementado segÃºn plan
- Tests escritos para funcionalidad nueva
- Cambios guardados

### Paso 1: Sintaxis Python

```bash
# Verificar sintaxis de todos los archivos
uv run python -m py_compile src/**/*.py
```

**Si falla:** Corregir errores de sintaxis antes de continuar.

### Paso 2: Linting con Ruff

```bash
# Verificar src/ y tests/
uv run ruff check src/ tests/

# Auto-corregir si es posible
uv run ruff check src/ tests/ --fix
```

**Errores comunes y soluciones:**
| Error | Significado | SoluciÃ³n |
|-------|-------------|----------|
| F401 | Import no usado | Eliminar import o usar `# noqa: F401` |
| F841 | Variable no usada | Eliminar variable o usar `_` |
| E501 | LÃ­nea muy larga | Dividir lÃ­nea (>120 chars) |
| I001 | Imports desordenados | Ejecutar `ruff check --fix` |

### Paso 3: Formateo

```bash
# Formatear cÃ³digo automÃ¡ticamente
uv run ruff format src/ tests/
```

### Paso 4: Ejecutar Tests

Si el repo incluye `scripts/run_pytest_safe.py`, usalo como via principal para
evitar solapes y residuos temporales. Usa `uv run pytest` solo como fallback.

```bash
# Todos los tests
python scripts/run_pytest_safe.py

# Tests especÃ­ficos del mÃ³dulo
python scripts/run_pytest_safe.py -- tests/test_[modulo].py -v

# Con cobertura
python scripts/run_pytest_safe.py -- tests/ --cov=src --cov-report=term-missing

# Fallback si el proyecto no tiene runner seguro
uv run pytest tests/ -v
uv run pytest tests/test_[modulo].py -v
uv run pytest tests/ --cov=src --cov-report=term-missing
```

**Todos los tests deben pasar.**

### Paso 5: Verificar Imports

```bash
# Verificar que no hay imports circulares
uv run python -c "import src"
uv run python -c "import src.main"
```

### Paso 6: Verificar Seguridad

Buscar patrones sensibles:

```bash
# Buscar posibles secrets hardcodeados
grep -r "API_KEY\|api_key" src/ --include="*.py"
grep -r "password\|PASSWORD" src/ --include="*.py"
grep -r "token\|TOKEN" src/ --include="*.py"
grep -r "secret\|SECRET" src/ --include="*.py"
```

**Verificar:**
- No hay credenciales en cÃ³digo
- Variables de entorno usadas correctamente
- No hay `print()` con datos potencialmente sensibles

### Paso 7: Reportar Resultado

Documentar en `execution_log.md`:

```markdown
### ðŸ§ª Quality Gates - [FECHA]

**Resultado:** âœ… PASSED / âŒ FAILED

**Checks ejecutados:**
- [x] Sintaxis Python: OK
- [x] Ruff: PASSED (0 errores)
- [x] Tests: PASSED (X/Y tests)
- [x] Imports: OK
- [x] Seguridad: VERIFIED

**Errores encontrados:**
- [ ] [Si hay, listar aquÃ­]

**Correcciones aplicadas:**
- [CorrecciÃ³n realizada]
```

## Output Format

### âœ… PASSED
Todos los gates pasaron. Listo para `ðŸŸ£ READY_FOR_REVIEW`.

### âŒ FAILED
Hay errores que corregir:
1. Documentar errores en execution_log.md
2. Corregir errores
3. Volver a ejecutar Quality Gates
4. Repetir hasta PASSED

## References

- `references/common-fixes.md` - Soluciones a errores comunes
- `BUILDER_SKILLS.md` - Capacidades tÃ©cnicas del Builder

## Constraints

- **NO** solicitar revisiÃ³n con tests fallando
- **NO** ignorar errores de linting
- **NO** dejar secrets hardcodeados
- **SIEMPRE** ejecutar antes de `READY_FOR_REVIEW`


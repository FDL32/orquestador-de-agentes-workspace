# Protocolo de Inicio y Flujo Principal

## Flujo de Trabajo (Manager â†’ Builder)
1. **[Usuario]** Describe tarea al Manager.
2. **[Manager]** Crea `work_plan.md` (Tipo: IMPLEMENTATION) â†’ Usuario aprueba.
3. **[Builder]** Implementa â†’ Ejecuta Quality Gates (`ruff`, `pytest`, `pip-audit`).
4. **[Manager]** Revisa cÃ³digo real (no solo logs) â†’ Usuario aprueba.
5. **[Manager]** Crea `work_plan.md` (Tipo: FINALIZATION) â†’ cierre por fases.
6. **[Builder]** Ejecuta cierre fase a fase â†’ Manager aprueba cada fase.
7. **[Usuario]** Recibe proyecto cerrado profesionalmente.

## Quality Gates (obligatorios antes de cada review)
- **AuditorÃ­a de dependencias:** `uv run pip-audit .`
- **Linter y Formatter:** `ruff check src/ tests/ --fix` y `ruff format src/ tests/`
- **Tests:** `python scripts/run_pytest_safe.py`

## Error y Debug
- Registrar errores persistentes en `PROJECT.md` (sin datos sensibles, usar `***REDACTED***`).
- Scripts de un solo uso o depuraciÃ³n deben ir a `tests/sandbox/debug_*.py`. Nunca en la raÃ­z.


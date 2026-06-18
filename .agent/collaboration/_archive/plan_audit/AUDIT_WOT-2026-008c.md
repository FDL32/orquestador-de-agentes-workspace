# AUDIT_WOT-2026-008c.md

## Checklist Manager

- Confirmar que `T-008C-001` existe, esta frozen y ya no contradice `DEC-008B-001`.
- Confirmar que no se crea `registry.json` ni manifest central equivalente.
- Confirmar que `docs/registry/INDEX.md` se genera desde discovery recursivo.
- Ejecutar o inspeccionar el stale-check: debe fallar si `INDEX.md` diverge del output generado.
- Revisar que el diff no mueve, renombra ni borra prompts/skills.
- Comprobar que no se ejecuta scope de `008d`.
- Comprobar que los tests prueban comportamiento real, no solo existencia de archivos.
- Confirmar `run_pytest_safe --level all` con `args_mode=default_discovery`, `exit_code=0` y `tested_commit_sha==HEAD`.
- Confirmar `validate --json` en 0 errors / 0 warnings.

## Anti-patrones a rechazar

- Crear `registry.json` pese a la DEC congelada.
- INDEX manual que no se regenera desde discovery.
- Stale-check pass-open o solo documental.
- Mover shims o renombrar prompts/skills dentro de 008c.
- Tests que aceptan cualquier Markdown valido sin validar drift real.

## Criterio de aprobacion

Aprobar si el cambio formaliza la proyeccion generada existente, anade barrera stale-check real, respeta `DEC-008B-001`, mantiene 008d fuera de scope y deja los gates canonicos verdes.
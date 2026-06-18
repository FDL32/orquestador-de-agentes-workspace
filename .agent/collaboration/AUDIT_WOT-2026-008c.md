# AUDIT_WOT-2026-008c.md

## Checklist Manager

- Confirmar que `T-008C-001` existe y esta frozen.
- Confirmar que `STATE.md` y `TURN.md` apuntan a `WOT-2026-008c` antes de aceptar handoff.
- Revisar que el diff no mueve, renombra ni borra prompts/skills.
- Revisar que `docs/registry/INDEX.md` se deriva del registry y no introduce una segunda verdad manual.
- Ejecutar o inspeccionar el stale-check: debe fallar si registry/INDEX quedan desactualizados.
- Comprobar que el registry incluye prompts, skills, templates/references y consumidores relevantes.
- Comprobar que no se ejecuta scope de 008d.
- Comprobar que los tests prueban comportamiento real, no solo existencia de archivos.
- Confirmar `run_pytest_safe --level all` con `args_mode=default_discovery`, `exit_code=0` y `tested_commit_sha==HEAD`.
- Confirmar `validate --json` en 0 errors / 0 warnings.

## Anti-patrones a rechazar

- INDEX manual que no se regenera desde la fuente canonica.
- Registry que solo lista skills y omite prompts o referencias.
- Campos vagos sin criterio reproducible.
- Mover shims o renombrar prompts/skills dentro de 008c.
- Tests que aceptan cualquier JSON valido sin validar cobertura real.
- Pass-open si el generator/check no puede clasificar un recurso.

## Criterio de aprobacion

Aprobar si el cambio crea una fuente generada verificable, conserva paridad de superficies existentes, mantiene 008d fuera de scope y deja los gates canónicos verdes.
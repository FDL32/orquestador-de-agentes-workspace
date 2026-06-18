# AUDIT_WOT-2026-008f.md

## Checklist Manager

- Confirmar `T-008F-001` frozen y coherente con `work_plan.md`.
- Confirmar `008e` cerrado canonicamente y `008c` satisfecho como premisa tecnica.
- Confirmar baseline pre-cambio de `validate --json` y `check_destino_publish_ready.py`.
- Confirmar que existe un wrapper unico `check_motor_destination_integration.py` y que no duplica scanners/validate.
- Confirmar que destination_context.py, check_destino_publish_ready.py, classify_publication.py y validate_authority.py solo cambian, si hace falta, para extraer helpers exportables sin alterar su contrato CLI.
- Confirmar separacion entre gate operativo por defecto y auditoria opcional de primera publicacion.
- Confirmar tests de barrera para link roto, propagacion de fallo pre-push y publication audit opt-in.
- Confirmar `run_pytest_safe --level all`, `ruff`, encoding y `validate 0/0`.

## Anti-patrones a rechazar

- Reimplementar `classify_publication.py` o `check_destino_publish_ready.py` dentro del wrapper.
- Cambiar la logica central o el contrato CLI de scripts envueltos en vez de delegar via wrapper.
- Ejecutar auditoria historica de publicacion siempre, sin flag explicito.
- Probar guards o settings mutando un destino real.
- Abrir scope a instalador/launcher sin evidencia de necesidad.
- Introducir dependencias nuevas.

## Criterio de aprobacion

Aprobar si el wrapper integrado reutiliza piezas existentes, falla cerrado con diagnostico util, separa correctamente operacion cotidiana de auditoria de primera publicacion y deja todos los gates canonicos en verde.
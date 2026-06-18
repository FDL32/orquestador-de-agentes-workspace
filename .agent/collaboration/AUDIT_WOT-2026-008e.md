# AUDIT_WOT-2026-008e.md

## Checklist Manager

- Confirmar `T-008E-001` frozen y coherente con work_plan.
- Confirmar que `008d` esta cerrado canonicamente.
- Confirmar baseline pre-cambio de `--check-naming`, `--check-contract`, collisions, json y rg.
- Confirmar que `prompts/manager_review.md` es canonico y `prompts/review_manager.md` es stub-alias.
- Confirmar que `KNOWN_LEGACY_NAMES` ya no contiene `review_manager`.
- Confirmar que los 6 consumidores vivos declarados en DEC quedan actualizados o justificados.
- Confirmar que `rg "review_manager"` queda limitado a stub, legacy_aliases, docs historicas/deprecacion o tests de compatibilidad.
- Confirmar `--check-naming`, `--check-contract`, collisions y json verdes.
- Confirmar suite canonica con `level=all`, `args_mode=default_discovery`, `tested_commit_sha==HEAD`, y validate 0/0.

## Anti-patrones a rechazar

- Borrar `review_manager.md` sin stub.
- Mantener `review_manager` en `KNOWN_LEGACY_NAMES`.
- Actualizar solo `source_prompt` y olvidar prose viva.
- Introducir manifest central o sidecar JSON.
- Tocar bus/runtime o `pre_handoff_guard.py`.
- Declarar paridad sin baseline pre/post.

## Criterio de aprobacion

Aprobar si el rename versionado queda atomico, el alias legacy queda limitado a compatibilidad documentada, el gate de naming pasa sin excepciones, los consumidores vivos no se rompen y todos los gates canonicos pasan.
# AUDIT_WOT-2026-008d.md

## Checklist Manager

- Confirmar que `T-008D-001` existe, esta frozen y coincide con el work_plan activo.
- Confirmar que la DEC existe y fue creada antes de cualquier rename.
- Confirmar que la DEC define patrones, prefijos de rol, shim/frontmatter, fuente de INDEX y ortogonalidad con 010s.
- Confirmar que `discover_skills.py --check-naming` existe y tiene test fail-closed real.
- Confirmar que `run_gates_dispatch.py` invoca el gate en perfiles aplicables.
- Confirmar baseline pre/post de `--check-contract`, `check_skill_collisions.py` y `discover_skills.py --json`, con paridad salvo renames/aliases declarados.
- Confirmar que no se crea `registry.json` ni sidecar JSON.
- Confirmar que `pre_handoff_guard.py` no contiene logica de naming.
- Confirmar que cualquier rename piloto actualiza prompt, frontmatter `source_prompt`, prose viva y shim legacy atomicamente.
- Confirmar `rg` de nombres antiguos limitado a shims, docs historicas/deprecacion, changelog/backlog o tests de compatibilidad.
- Confirmar suite canonica con `level=all`, `args_mode=default_discovery`, `tested_commit_sha==HEAD`, y `validate --json` 0/0.

## Anti-patrones a rechazar

- DEC escrita despues del rename.
- Naming gate implementado en `pre_handoff_guard.py`.
- `check_skill_collisions.py` modificado sin autorizacion explicita de la DEC.
- Shim que rompe `--check-contract`.
- Manifest central, `registry.json` o sidecar JSON.
- Migracion masiva disfrazada de piloto.
- Tests que solo comprueban existencia y no bloquean un nombre invalido.

## Criterio de aprobacion

Aprobar si el ticket define la convencion por DEC, implementa y conecta un gate de naming verificable, mantiene paridad de discovery/contract/collision, aplica como maximo un piloto reversible y deja los gates canonicos verdes sin expandir scope.
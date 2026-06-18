# Strategy: WOT-2026-010u

## Enfoque

Implementar una barrera fail-closed, no un automatismo de commit. El fallo recurrente no es que el archivador mueva mal los archivos: es que el movimiento queda sin commit y el siguiente ciclo lo descubre tarde. La solucion segura es detectar ese estado en el mismo cierre/handoff y dar remediacion exacta.

## Orden recomendado

1. Crear fixture de repo git real con `.agent/collaboration/AUDIT_WOT-TEST.md` y su copia movida a `_archive/plan_audit/` sin stage/commit.
2. Escribir test rojo que espere bloqueo con diagnostico `archive_rename_uncommitted`.
3. Implementar helper que inspeccione `git status --porcelain -z` y detecte pares delete/untracked con mismo basename bajo `collaboration/` -> `_archive/plan_audit/`.
4. Conectar el helper al punto menos invasivo: preferir pre-handoff/validate hygiene antes que cambiar el archivador para commitear.
5. Documentar el procedimiento en `docs/protocol/archive_rename_hygiene_WOT-2026-010u.md`.

## Riesgos

- Falso positivo si el usuario borro intencionalmente un artefacto y creo otro con mismo nombre. Mitigacion: limitar a `STRATEGY_`, `PLAN_`, `AUDIT_` y `_archive/plan_audit/`.
- Romper handoff por superficies vivas. Mitigacion: no tocar `archive/` de notifications ni events.
- Parser git status fragil. Mitigacion: usar `--porcelain -z` y tests con git real.

## Gates esperados

- `python -m pytest tests/test_pre_handoff_guard.py tests/test_archive_collaboration_artifacts.py tests/unit/test_delivery_hygiene_check.py -q`
- `ruff check <python files touched>`
- `ruff format --check <python files touched>`
- `python scripts/check_encoding_guard.py <files touched>`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## CONTRACT_GAP

Emitir CONTRACT_GAP si el unico fix viable exige auto-commit, borrar artefactos, tocar bus runtime o cambiar la politica de superficies vivas de `_archive/` de forma incompatible con tickets cerrados.
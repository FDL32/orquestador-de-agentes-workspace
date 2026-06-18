# work_plan.md -- WOT-2026-008f

## Metadata

- **ID:** WOT-2026-008f
- **Contract ID:** T-008F-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Crear un gate integrado `scripts/check_motor_destination_integration.py` que valide el engranaje motor-destino y el lifecycle operativo reutilizando checks existentes antes de inventar validadores nuevos. Debe cubrir link `motor_destination_link.json`, compatibilidad de autoridad/version/manifest, resolucion de contexto destino, gate operativo pre-push y auditoria opcional de primera publicacion, con diagnostico self-service y sin mutar un destino real durante las pruebas.

## Premisas verificadas antes de Builder

- `WOT-2026-008e` esta COMPLETED y es la dependencia funcional directa del siguiente tramo; `WOT-2026-008c` queda satisfecho como premisa tecnica de `INDEX.md` generado y `--check-index` verde.
- `scripts/destination_context.py` existe y hoy expone `--bootstrap --project-root`; es una pieza viva de resolucion destino.
- `scripts/check_destino_publish_ready.py` existe y ya orquesta `validate --json` + estado operativo pre-push.
- `scripts/classify_publication.py` existe y ya clasifica publicacion en dry-run con `--repo-root`.
- El problema de 008f es de integracion/orquestacion entre piezas existentes, no de ausencia total de checks.

## Decision Arquitectonica

La entrada canonica del ticket sera `scripts/check_motor_destination_integration.py`. El wrapper debe delegar en logica existente siempre que sea posible: `destination_context.py`, `check_destino_publish_ready.py`, `classify_publication.py` y helpers de autoridad/topologia ya presentes. El modo por defecto cubre integracion operativa cotidiana; la auditoria de primera publicacion queda separada detras de un flag explicito para no mezclar un gate pre-push con un scan historico mas caro.

## Non-goals

- No duplicar scanners de secretos, `validate`, ni la clasificacion de publicacion.
- No mutar un `repo_destino` real para probar guards o settings.
- No tocar bus runtime/events manualmente.
- No redisenar `install_agent_system.py` ni el launcher.
- No tocar dependencias.
- No convertir el wrapper en un orquestador generico de session-close.

## Files Likely Touched

### repo_motor

- `scripts/check_motor_destination_integration.py`
- `tests/test_check_motor_destination_integration.py`
- `docs/protocol/motor_destination_integration_WOT-2026-008f.md`
- `scripts/destination_context.py`
- `scripts/check_destino_publish_ready.py`
- `scripts/classify_publication.py`
- `scripts/validate_authority.py`
- `tests/test_destination_context.py`
- `tests/test_prepush_check.py`
- `tests/test_classify_publication.py`
- `prompts/destination_bootstrap.md`
  - Nota FLT: si se toca, solo para anadir una referencia minima al wrapper nuevo; no reescribir el flujo operativo.
- `prompts/audit_git_publication.md`
  - Nota FLT: si se toca, solo para anadir una referencia minima al wrapper nuevo; no reescribir el flujo operativo.

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/install_agent_system.py`
- `.agent/agent_controller.py`
- `.agent/config/motor_destination_link.json`
- `MANIFEST.distribute`
- `MANIFEST.workspace`
- `prompts/orchestrator_pipeline.md`
- `prompts/audit_complete_motor_destination.md`
- `tests/test_motor_root_gates.py`
- `.agent/runtime/events/`
- `bus/`

## Manager-only

- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/AUDIT_WOT-2026-008f.md`
- `.agent/collaboration/STRATEGY_WOT-2026-008f.md`
- `.agent/planning/ticket_contracts.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- Bus runtime/events editado manualmente.
- Nuevo scanner de secretos o clon de `classify_publication.py`.
- Reimplementar `validate --json` o `check_destino_publish_ready.py` en vez de delegar.
- Escribir en un destino real para probar `guard_paths`, settings o lifecycle.
- Dependencias, `privada/`, `.env`.

## Fase 0 obligatoria

1. Confirmar `T-008F-001` frozen, `008e` completed y `008c` satisfecho como premisa tecnica.
2. Capturar baseline read-only:
   - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
   - `python scripts/check_destino_publish_ready.py --project-root <repo_destino> --motor-root <repo_motor>`
   - inspeccion de `destination_context.py`, `check_destino_publish_ready.py`, `classify_publication.py` y `validate_authority.py`
3. Verificar que el wrapper puede delegar en piezas existentes; si obliga a copiar logica central o a cambiar el contrato CLI de los scripts envueltos, emitir CONTRACT_GAP.
4. Registrar baseline y seams en `execution_log.md` antes de tocar codigo.

## Criterios binarios

- Existe `python scripts/check_motor_destination_integration.py --project-root <repo_destino> [--motor-root <repo_motor>]` con diagnostico self-service y exit codes documentados.
- El wrapper reutiliza checks existentes cuando existen; no duplica la logica de `classify_publication.py`, `check_destino_publish_ready.py`, `destination_context.py` ni validaciones de autoridad/settings ya presentes.
- destination_context.py, check_destino_publish_ready.py, classify_publication.py y validate_authority.py solo pueden cambiarse para extraer helpers exportables sin alterar su contrato CLI; el wrapper delega via import, no via copia ni reescritura de su logica central.
- El wrapper valida que `motor_destination_link.json` resuelve `motor_root` y `destination_root` coherentes con el contrato y falla cerrado ante link ausente o invalido.
- El wrapper distingue gate operativo pre-push de auditoria de primera publicacion; la auditoria historica solo corre con flag explicito y sigue siendo dry-run.
- El wrapper demuestra que el contexto destino puede resolver el lifecycle/registry del motor sin depender de escribir sobre un destino real.
- Las pruebas reproducen al menos: link roto, fallo propagado desde `check_destino_publish_ready`, modo auditoria opcional y fallo cerrado de autoridad/version/manifest sobre fixture o tmp.
- `ruff`, tests focales reales, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` pasan en verde.

## CONTRACT_GAP behavior

Emitir `CG-WOT-2026-008f.md` si el wrapper exige reimplementar scanners/validate, si la unica forma de probar guards requiere mutar un destino real, si obliga a cambiar la logica central o el contrato CLI de scripts ya vivos, o si la separacion entre gate operativo y auditoria de primera publicacion no puede mantenerse.

## STOP conditions

Parar si el wrapper reimplementa scanners de secretos o `validate`; parar si requiere escribir en `repo_destino` real para probar guards; parar si obliga a cambiar la logica central o el contrato CLI de scripts ya vivos en vez de delegar; parar si aparece dependencia nueva; parar si el cambio deriva en redisenar `install_agent_system.py` o el launcher en vez de integrar checks existentes.
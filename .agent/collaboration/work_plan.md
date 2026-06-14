# Work Plan: WOT-2026-007a - Contract Formation Pipeline v0 (contrato documental minimo)

## Metadata
- **ID:** WOT-2026-007a
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Contrato documental minimo del Contract Formation Pipeline v0
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (documental; no toca runtime/bus/controller/CI).
- **Contrato PROVISIONAL** hasta ratificacion en WOT-2026-007b.
- **Depende de:** -
- **Origen:** session-2026-06-14-contract-formation

## Objetivo
Implementar SOLO el contrato documental minimo del Contract Formation Pipeline v0 en el
motor (prompt + README + plantillas + decision MANIFEST + handoff), sin runtime ni
automatizacion, suficiente para que un Manager redacte tickets y otro agente los audite
antes de pasar a Builder.
Verificable por: existencia de los 6 entregables declarados, `check_encoding_guard.py`
exit 0 sobre los archivos tocados, y `agent_controller --validate --json` del repo_destino
con 0 errores (ver Criterios binarios y Gates).

## Decision Arquitectonica
- **Ruta documental:** `docs/contract_formation/` (el motor solo tenia 2 .md sueltos en
  `docs/`; subcarpeta dedicada = ruta limpia y descubrible).
- **`.agent/planning/` como superficie destino-keep:** se declara en `MANIFEST.workspace`
  por precedente directo de `.agent/audits/system_health/` (superficie destino-generada /
  motor-producida ya listada ahi). MANIFEST gobierna copy_tree (seed), no prune; la
  persistencia tambien queda protegida del prune por el guard git-tracked del instalador
  (WOT-2026-003d). Se elige declararla ya (en vez de diferir) para no bloquear 007b.
- **Prompt como router, no muro:** `contract_formation_pipeline.md` referencia las
  plantillas y delega `Intent/Impact Audit` a `audit_agent_output.md` 2.b/2.c en vez de
  redefinirlos, evitando dos definiciones que deriven.
- **Provisionalidad explicita:** 007a no prueba autonomia; 007b la falsa con vertical minima.

## Entregables (repo_motor)
- prompts/contract_formation_pipeline.md (fases, roles, status machine, DEC-* tiers, STOP, handoff).
- docs/contract_formation/README.md (indice humano + mapa de plantillas).
- docs/contract_formation/templates/repo_charter.md
- docs/contract_formation/templates/ticket_contract.md
- docs/contract_formation/templates/evidence_catalog.md
- docs/contract_formation/templates/contract_gap.md
- MANIFEST.workspace: `.agent/planning/` declarado destino-keep.

## Files Likely Touched (repo_motor)
prompts/contract_formation_pipeline.md
docs/contract_formation/README.md
docs/contract_formation/templates/repo_charter.md
docs/contract_formation/templates/ticket_contract.md
docs/contract_formation/templates/evidence_catalog.md
docs/contract_formation/templates/contract_gap.md
MANIFEST.workspace

## Non-goals
- No tocar runtime, bus, controller, scripts ejecutables ni CI (007a es documental).
- No cerrar 007b/007c/007d.
- No pedir al usuario que edite Markdown/codigo: decide via DEC-*.
- No introducir INDEX.md manual como fuente de verdad.

## Criterios binarios (a READY_FOR_REVIEW)
- [x] prompts/contract_formation_pipeline.md con fases, roles, maquina de status, DEC-* tiers, STOP y handoff a orchestrator_pipeline.md (gate 2.a).
- [x] README + 4 plantillas (repo_charter, ticket_contract, evidence_catalog, contract_gap).
- [x] Decision explicita `.agent/planning/` en MANIFEST.workspace.
- [x] 007a declarado PROVISIONAL hasta ratificacion en 007b.
- [x] Contrato separa decisiones humanas (DEC-*) de trabajo tecnico; research read-only.
- [x] check_encoding_guard.py exit 0; diff revisable sin scope creep.
- [x] agent_controller --validate --json (repo_destino): 0 errores.
- [x] Revision independiente (Manager/usuario) antes de cerrar. NO self-close (provisional).

## Gates (deliverable_type: documentation)
- check_encoding_guard.py sobre archivos tocados.
- agent_controller --validate --json (repo_destino): 0 errores.
- discover/check skills: N/A (no se crean skills).

## STOP
- Si se necesita codigo runtime/CLI/bus/validador ejecutable: parar y abrir 007c/007f.

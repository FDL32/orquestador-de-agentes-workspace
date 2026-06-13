# Work Plan: WOT-2026-002b - ORPHANS decision promover-vs-conservar-vs-archivar

## Metadata
- **ID:** WOT-2026-002b
- **Estado:** COMPLETED
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-ORPHANS
- **Titulo:** Decidir con evidencia el destino de los 10 huerfanos del triage_manifest
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (analisis read-only + doc; no mueve ni borra nada)
- **Origen:** WOT-AUDIT-A2 / triage_manifest.md (bucket huerfano-needs-decision)

## Objetivo
Para cada una de las 10 rutas del bucket `huerfano-needs-decision` del
`.agent/docs/triage_manifest.md`, emitir una decision con evidencia:
promover-al-motor, conservar-como-host-specific (destino-keep), o archivar-legacy.
El entregable es un doc de decisiones; NO mueve ni borra nada (eso es A2d /
WOT-2026-002c). Reduce a 0 los huerfanos sin resolver para que A2d ejecute.

## Decision Arquitectonica
El entregable es un doc de decisiones NUEVO (`orphans_decision_WOT-2026-002b.md`) que
cruza referencia al `triage_manifest.md`, en lugar de mutar el manifiesto: el
manifiesto es un deliverable de analisis ya cerrado (A2b) y debe permanecer como
inventario congelado; las decisiones son una capa posterior. La decision por huerfano
se ancla en evidencia FUNCIONAL (grep de invocacion viva en motor + destino), nunca en
basename ni ubicacion, para no archivar un flujo vivo ni promover ruido. El ticket es
analysis puro: separa decidir (aqui) de ejecutar (A2d / WOT-2026-002c).

## Rubrica de decision (congelada, del triage_manifest)
Eje: desarrollo/creacion del sistema -> motor; estado operativo / integracion /
host config / overrides del host / funcionalidad de dominio -> destino. "Particular
por dominio" cuenta como destino-keep SOLO si implementa comportamiento del
repo_destino, no por ser tooling del sistema que casualmente solo existe en el
destino. Equivalencia juzgada FUNCIONALMENTE (diff/behavior), nunca por basename.

Mapa de decisiones:
- **promote-to-motor:** es tooling de desarrollo/creacion del sistema, util y vivo
  o reutilizable, sin equivalente funcional en el motor -> pertenece al motor.
- **destino-keep:** implementa dominio/integracion/config real del repo_destino.
- **archive-legacy:** muerto (sin invocacion viva, superado por otra superficie, o
  deprecado) -> archivar, no promover.

## Los 10 huerfanos a decidir
1. `scripts/artifact_graph.py`
2. `scripts/audit_codebase.py`
3. `scripts/rollback_agent_system.py`
4. `scripts/state_drift.py`
5. `scripts/test_refactor_manager_skill.py`
6. `tests/test_ticket_007_context_recovery.py`
7. `.agent/hooks/pre_compact_hook.py`
8. `.agent/microagents/onboarding.md`
9. `.agent/glossary.md`
10. `.goosehints`

## Evidencia requerida por huerfano
- Invocacion viva: grep del basename / entrypoint en el MOTOR y en el DESTINO
  (scripts, hooks, CI, prompts, skills, configs). Citar archivo:linea o "sin hits".
- Equivalente funcional en el motor: confirmar ausencia/presencia (no por basename).
- Dominio: determinar si implementa comportamiento del repo_destino o es tooling.
- Para deprecados conocidos (`.goosehints` -> WT-2026-254a), citar la deprecacion.

## Files Likely Touched
- `.agent/docs/orphans_decision_WOT-2026-002b.md`
- `.agent/collaboration/execution_log.md`

## Superficies
- **Builder (crea/modifica):** `.agent/docs/orphans_decision_WOT-2026-002b.md`;
  `execution_log.md`.
- **Read/inspect only:** `.agent/docs/triage_manifest.md`, el arbol del motor y del
  destino para grep de invocaciones. NO mover ni borrar ningun huerfano.
- **Manager-only:** review de que cada decision tiene evidencia real (grep citado).

## Non-goals
- NO mover, borrar ni `git mv` ningun huerfano (eso es WOT-2026-002c / A2d).
- NO tocar el motor.
- NO promover a memoria estable un huerfano "dudoso" sin evidencia.

## Criterios binarios de cierre
- [ ] Los 10 huerfanos tienen una decision (promote-to-motor / destino-keep /
      archive-legacy); 0 sin resolver.
- [ ] Cada decision cita evidencia concreta: grep con archivo:linea o "sin hits
      en motor ni destino", y la determinacion de dominio.
- [ ] Doc `orphans_decision_WOT-2026-002b.md` creado, cruzando referencia al
      triage_manifest.
- [ ] `agent_controller --validate --project-root .` = 0/0.

## STOP / escalado
1. Si un huerfano resulta ser dominio real del destino (p.ej. `test_ticket_007`
   como experimento vivo con invocacion o intencion documentada): marcar
   destino-keep y NO archivar; anotar que corrige la conclusion "dominio vacio"
   del triage_manifest. Esto es un hallazgo, no un fallo.
2. Si un huerfano tiene invocacion viva en el destino sin equivalente en el motor:
   no archivar; promover o keep segun la rubrica, y marcarlo como barrera para A2d.
3. Si la evidencia es ambigua para un huerfano concreto: marcar `dudoso` con la
   evidencia parcial y la decision conservadora (no archivar), no forzar.

## Gates (deliverable_type: analysis)
- Existencia del deliverable `.agent/docs/orphans_decision_WOT-2026-002b.md`.
- `agent_controller --validate --project-root .` 0/0 (gate de estado).
- Encoding guard UTF-8 limpio sobre el doc.
- ruff/pytest: N/A (analisis; no se toca Python). Salto auditable.

## Entregables
- `.agent/docs/orphans_decision_WOT-2026-002b.md`: tabla de 10 decisiones con
  evidencia (grep citado, dominio, decision), lista de barreras para A2d, y
  cualquier correccion a la conclusion "dominio vacio" del triage_manifest.

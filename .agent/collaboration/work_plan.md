# Work Ticket - WT-2026-229a

## Metadata
- **ID:** WT-2026-229a
- **Title:** Cierre de sesion portable: motor agnostico, historico al destino y memoria propuesta
- **Scope:** system/session-closeout-portability
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-228a

## Problema
El `repo_motor` debe ser el producto portable y agnostico del sistema. Hoy aun
contiene artefactos operativos historicos en la raiz, por ejemplo
`PLAN_WP-2026-150.md` y `AUDIT_WP-2026-150.md`. Esos archivos son historia de
trabajo del `repo_destino`, no parte del motor reusable.

Ademas, el cierre de sesion debe convertir las ensenanzas del dia en decisiones
claras: barreras ya implantadas, memoria candidata y deuda explicita. La memoria
no se escribe automaticamente; primero se propone siguiendo
`prompts/memory_upload.md`.

## Objetivo
Dejar el `repo_motor` limpio como producto portable:
1. mover planes/audits historicos `PLAN_WP-2026-*.md` y `AUDIT_WP-2026-*.md`
   desde la raiz del `repo_motor` al `repo_destino`;
2. ubicar ese historico en `.agent/collaboration/archive/legacy_motor_root/`;
3. auditar si quedan otros artefactos locales o historicos en `repo_motor` que
   contradigan su portabilidad;
4. revisar aprendizajes del dia y proponer memoria sin escribirla todavia;
5. contrastar la filosofia de `prompts/audit_agent_output.md` y CEM v0 contra
   el codigo/prompts tocados en la sesion.

## Contrato CEM v0
- Contrato antes que fix.
- Evidencia antes que relato.
- Rigor proporcional: toca higiene de repo, memoria y cierre de sesion.
- Ninguna afirmacion sin artefacto verificable.
- El `repo_motor` conserva solo resultado reusable: codigo, tests, prompts,
  docs del producto, templates y tooling.
- El `repo_destino` conserva historico operativo: planes, auditorias, estado,
  execution logs y memoria project.

## Decision Arquitectonica
- No mover historico operativo a `docs/` del motor.
- No borrar historico sin migrarlo primero al `repo_destino`.
- No escribir memoria engine/meta sin propuesta humana aprobada.
- No meter rutas absolutas locales nuevas en el motor.
- No mezclar esta limpieza con refactors funcionales.

## Evidencia minima esperada
El cierre debe dejar:
- `git status` limpio en `repo_motor` despues del commit;
- raiz del `repo_motor` sin `PLAN_WP-2026-*.md` ni `AUDIT_WP-2026-*.md`;
- los archivos migrados visibles en
  `.agent/collaboration/archive/legacy_motor_root/` del `repo_destino`;
- inventario breve de otros artefactos sospechosos y decision por cada grupo:
  mover ahora, dejar porque es producto, ignorar por gitignore o abrir deuda;
- propuesta de memoria en formato de `prompts/memory_upload.md`, sin escritura
  automatica;
- auditoria corta de coherencia con `prompts/audit_agent_output.md` y
  `.agent/rules/common/sustainable_engineering.md`;
- `validate --json` del `repo_destino` con 0 errores y 0 warnings.

## Non-goals
- No borrar `.venv`, `.git`, caches o directorios locales sin comprobar si estan
  trackeados y si pertenecen al producto.
- No modificar codigo funcional salvo que una barrera de portabilidad ya
  existente falle y el cambio sea minimo.
- No publicar memoria al `repo_motor` sin confirmacion humana explicita.
- No reescribir historico de git.
- No mover docs de arquitectura vigentes como `docs/BUS_ARCHITECTURE_*`.

## Fases
### Fase 0: Diagnostico
- Confirmar `repo_motor` limpio antes de tocar.
- Listar artefactos root `PLAN_WP-2026-*.md` y `AUDIT_WP-2026-*.md`.
- Confirmar que estan trackeados en git.
- Revisar `docs/`, `.agent/collaboration/archive/`, `.gitignore` y manifests.
- Revisar `prompts/audit_agent_output.md`,
  `prompts/memory_upload.md` y
  `.agent/rules/common/sustainable_engineering.md`.

### Fase 1: Migracion de historico
- Crear en `repo_destino`:
  `.agent/collaboration/archive/legacy_motor_root/`.
- Mover alli los `PLAN_WP-*` y `AUDIT_WP-*` historicos desde la raiz del
  `repo_motor`.
- En `repo_motor`, registrar los deletes como limpieza portable.
- En `repo_destino`, conservar el historico como estado operativo del proyecto.

### Fase 2: Auditoria de portabilidad
- Inventariar root y directorios locales del `repo_motor`.
- Clasificar cada grupo relevante:
  - producto portable;
  - historico operativo a destino;
  - runtime/cache gitignored;
  - deuda follow-up.
- No tocar grupos ambiguos sin justificar en `execution_log.md`.

### Fase 3: Memoria y filosofia
- Proponer aprendizajes del dia con el formato de `memory_upload.md`.
- No escribir memoria hasta aprobacion humana.
- Revisar si `audit_agent_output.md`, `review_manager.md` y `launch_builder.md`
  reflejan la regla: evidencia real antes que auto-reporte.
- Registrar gaps como deuda o ticket follow-up.

## Files Likely Touched
- `PLAN_WP-2026-*.md`
- `AUDIT_WP-2026-*.md`
- `.agent/collaboration/archive/legacy_motor_root/`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-229a.md`
- `.agent/collaboration/AUDIT_WT-2026-229a.md`
- `.agent/collaboration/execution_log.md`

## TP Check
TP-01: `repo_motor` root queda sin `PLAN_WP-2026-*.md` ni
`AUDIT_WP-2026-*.md`.
TP-02: esos artefactos existen en el `repo_destino` bajo
`.agent/collaboration/archive/legacy_motor_root/`.
TP-03: no se pierden contenidos; conteo y nombres coinciden antes/despues.
TP-04: la auditoria de portabilidad clasifica grupos sospechosos con evidencia.
TP-05: la propuesta de memoria se entrega sin escribir `observations.jsonl`.
TP-06: la revision CEM cita artefactos reales: `audit_agent_output.md`,
`memory_upload.md`, `sustainable_engineering.md` y commits/tests del dia.
TP-07: `repo_motor` no recibe rutas absolutas locales nuevas.
TP-08: `validate --json` del `repo_destino` queda en 0/0.

## Criterio binario de salida
- `git status --short` del `repo_motor` muestra solo cambios esperados antes del
  commit y queda limpio tras commit.
- `git ls-files "PLAN_WP-2026-*.md" "AUDIT_WP-2026-*.md"` en `repo_motor`
  devuelve vacio despues de la migracion.
- `Get-ChildItem .agent/collaboration/archive/legacy_motor_root` en
  `repo_destino` muestra los 12 archivos migrados.
- `agent_controller.py --validate --json --project-root <repo_destino>` devuelve
  0 errores y 0 warnings.

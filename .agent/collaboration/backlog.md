# Backlog

> Tickets candidatos y planes futuros del workspace.
> No es estado activo: el ticket activo vive en `work_plan.md`.
> Al arrancar un item, se convierte en `work_plan.md`; al cerrarlo, pasa a `CHANGELOG.md`.

## Politica
- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` — repo destino real que sirve para desarrollar el motor.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` — repo portable con `.git` propio.
- **Contrato:** mejoras que nacen en el workspace y deben ser globales se portan explicitamente al motor; nunca se asume sincronizacion implicita.
- **Escritura:** humano o Manager; Builder solo lo toca si el plan lo pide explicitamente.
- **Destino:** cada proyecto destino tendra su propio `.agent/collaboration/backlog.md`.

## Vista rapida

| Prioridad | Ticket | Titulo | Scope | Estado | Depende de | Origen |
|-----------|--------|--------|-------|--------|------------|--------|
| Alta | WP-2026-176 | Implantar Modelo B workspace/code-only | system | completed | - | session-2026-05-29 |
| Alta | WP-2026-177 | Unificar schema memoria + bridge por domain | system/meta | completed | WP-2026-176 | memory-design |
| Media | WP-2026-178 | L2/L3 memory rules + memory_loader.py | system/meta | completed | WP-2026-177 | memory-design |
| Media | WP-2026-179 | Namespaces wing + instalador scope-aware | system/meta | completed | WP-2026-178 | memory-design |
| Media | WP-2026-180 | Persistencia sesion Builder --session OpenCode | system | completed | WP-2026-178 | session-2026-05-30 |
| Baja | TBD | guard_paths: proteger archivos de estado del workspace | system | backlog | WT-2026-182 | session-2026-05-30 |
| Baja | TBD | BUILDER_STARTED liveness | system | idea | - | session-2026-05-29 |
| Baja | TBD | Flag manual --reset-circuit-breaker | system | backlog | - | CB-RESET-01 |
| Media | WT-2026-182 | Integracion Repomix para Contexto y Repo-Compare | system/skills | completed | - | session-2026-05-30 |
| Alta | WT-2026-183 | Resiliencia ante Supervisor muerto en CHANGES | system/bus | completed | WT-2026-182 | session-2026-05-30 |
| Baja | WT-2026-181 | Migracion nomenclatura WP->WT + Plan como epica | system/meta | completed | WP-2026-179 | session-2026-05-30 |
| Media | WT-2026-184 | Scaffold de PROJECT.md para repositorios destino | system/templates | completed | WT-2026-183 | session-2026-05-30 |
| Media | WT-2026-185 | Knowledge Layer: Glosario + Microagent + skill_resolver | system/knowledge | completed | WT-2026-184 | session-2026-05-31 |
| Alta | WT-2026-186 | Idempotencia del instalador y contrato de rutas gestionadas | system/install | completed | WT-2026-185 | session-2026-05-31-audit |
| Alta | WT-2026-198 | Idempotencia del instalador y contrato de rutas gestionadas | system/install | active | WT-2026-185 | session-2026-06-01-reopen |
| Critica | WT-2026-199 | Claim atomico de requeue y verificacion de Builder vivo | system/supervisor | completed | WT-2026-198 | session-2026-06-01-hotfix |
| Alta | WT-2026-200 | Launcher/supervisor: resume sin supervisor fresco | system/launcher | paused | WT-2026-199 | session-2026-06-01-followup |
| Media | WT-2026-201 | Hardening runtime del launcher tras WT-2026-200 | system/launcher | completed | WT-2026-200 | session-2026-06-01-followup |
| Alta | WT-2026-187 | Portabilidad Modelo B y limpieza legacy | system/portability | completed | WT-2026-186 | session-2026-05-31-audit |
| Media | WT-2026-188 | Modularizacion progresiva de agent_controller.py | system/architecture | completed | WT-2026-187 | session-2026-05-31-audit |
| Alta | WT-2026-189 | Guard anti doble lanzamiento de Builder tras CHANGES | system/bus | completed | WT-2026-187 | session-2026-05-31-hotfix |
| Alta | WT-2026-190 | Rotacion segura de review_queue.md y contrato de memoria | system/hygiene | completed | WT-2026-189 | session-2026-06-01-memory |
| Alta | WT-2026-196 | Manager adaptativo ante blockers repetidos | system/review | completed | WT-2026-190 | session-2026-06-01-review-loop |
| Alta | WT-2026-191 | Migracion determinista de memoria y bootstrap real | system/memory | completed | WT-2026-196 | session-2026-06-01-memory |
| Media | TBD | Inventario y estabilizacion de suite global | system/testing | backlog | WT-2026-191 | session-2026-06-01-suite |
| Media | WT-2026-192 | Claude Memory Mirror local opt-in | system/devx | completed | WT-2026-191 | session-2026-06-01-memory |
| Media | WT-2026-197 | Supervisor post-restart sin Builder tras CHANGES | system/bus | completed | WT-2026-192 | session-2026-06-01-review-loop |
| Baja | WT-2026-193 | Redaccion previa en pipeline de memoria persistente | system/security | completed | WT-2026-191 | session-2026-06-01-memory |
| Alta | WT-2026-203 | Barreras de packaging y propagacion de blockers en review loop | system/review | completed | WT-2026-193 | session-2026-06-02-followup |
| Alta | WT-2026-204 | Hardening de materializacion de blockers con parser unico | system/review | completed | WT-2026-203 | session-2026-06-02-followup |
| Alta | WT-2026-205 | Supervisor liveness; closeout reconciliado canonicamente | system/closeout | completed | WT-2026-204 | session-2026-06-02-followup |
| Critica | WT-2026-210 | Auditoria integral y rediseno del bus multi-agente | system/bus-architecture | completed | WT-2026-205 | session-2026-06-02-bus-audit |
| Critica | WT-2026-211 | Centralizacion del write-path y proyecciones operativas | system/bus-write-path | completed | WT-2026-210 | session-2026-06-02-write-path |
| Alta | WT-2026-212 | Consumidor durable de CHANGES y requeue garantizado | system/bus-durable-requeue | completed | WT-2026-211 | session-2026-06-02-durable-changes |
| Alta | WT-2026-214 | Protocolo de forced close: reconciliacion automatica del ticket anterior en preflight | system/preflight-reconcile | completed | WT-2026-210, WT-2026-216 | session-2026-06-02-preflight-reconcile |
| Alta | WT-2026-216 | Launcher lee el bus en vez de TURN.md para decidir que agente lanzar | system/launcher-bus-read | completed | WT-2026-211 | session-2026-06-02-launcher-bus-read |
| Alta | WT-2026-215 | Gates Modelo B: operaciones git de tooling resuelven motor_root | system/gates-motor-root | backlog | WT-2026-210 | session-2026-06-02-bridge-diff |
| Alta | WT-2026-217 | Pre-check de packaging usa la ruta canonica de transicion al emitir CHANGES | system/bus-transition | backlog | WT-2026-210 | session-2026-06-02-precheck-transition |
| Baja | WT-2026-213 | Eliminar el doble STATE_CHANGED de --mark-ready | system/bus-events | backlog | WT-2026-210 | session-2026-06-02-bus-audit |
| Media | WT-2026-206 | Scope gate y cierres manuales en workspace+motor | system/hygiene | backlog | WT-2026-211 | session-2026-06-02-followup |
| Media | WT-2026-207 | Gobernanza de collaboration legacy en el motor durante session-close | system/hygiene | backlog | WT-2026-211 | session-2026-06-02-closeout |
| Alta | WT-2026-208 | Estabilizacion de suite global tras transicion workspace+motor | system/testing | backlog | WT-2026-211 | session-2026-06-02-suite |
| Baja | WT-2026-209 | Sustituir nomenclatura Modelo B por estandar workspace+motor | system/docs | backlog | WT-2026-211 | session-2026-06-02-terminology |
| Baja | TBD | Repomix falla en Windows por permisos Node.js/globby | system/devx | backlog | WT-2026-182 | session-2026-05-31 |
| Media | WT-2026-218 | Regenerar y commitear memory_rules.md en el motor | system/memory | backlog | - | session-2026-06-02-memory-bootstrap |
| Media | WT-2026-219 | Bootstrap de memoria garantizado en destinos nuevos | system/memory | backlog | WT-2026-218 | session-2026-06-02-memory-bootstrap |
| Media | WT-2026-220 | Flujo de promocion upstream de memoria para dogfooding | system/memory | backlog | WT-2026-219 | session-2026-06-02-memory-bootstrap |

## Reordenacion 2026-06-02 - auditoria del bus

Esta seccion ordena la deuda viva antes de abrir mas parches. La regla es: todo lo que afecte a autoridad de estado, eventos, requeue, liveness, proyecciones o cierre canonico entra primero en `WT-2026-211`; lo demas queda fuera o espera a que el contrato del bus sea estable.

### Epica propuesta

`WT-2026-211 - Centralizacion del write-path y proyecciones operativas`

- **Prioridad:** Critica
- **Scope:** system/bus-write-path
- **Estado:** completed
- **Objetivo:** centralizar la materializacion de proyecciones operativas en un unico writer y eliminar escrituras directas del camino de transicion en controller/bridge, manteniendo el bus como fuente canonica de hechos.
- **Non-goal inicial:** no resolver aun el watcher durable de CHANGES, la eliminacion del doble STATE_CHANGED ni el launcher leyendo el bus; eso queda para tickets hijos.
- **Criterio de salida:** controller y bridge dejan de escribir proyecciones de transicion por su cuenta; supervisor materializa TURN.md/STATE.md/execution_log.md desde el bus; tests de coherencia pasan.

### Deuda que entra en WT-2026-211

| Item | Motivo |
|------|--------|
| Supervisor idle timeout con Builder silencioso | Es un fallo de liveness del bus: idle no debe significar "sin trabajo activo" si Builder sigue vivo. |
| `BUILDER_STARTED` / heartbeat / renovacion de lock | Pertenece al contrato explicito de vida del Builder, no a un hotfix aislado. |
| `REVIEW_DECISION=CHANGES` sin watcher durable | La requeue debe ser procesada aunque el supervisor reactivo anterior haya salido. |
| `BUILDER_RELAUNCH_ATTEMPTED` con `builder_launch_unverified` | Evidencia que launcher, lock y supervisor no comparten una senal fiable de arranque. |
| `WT-2026-200` y deuda de launcher/supervisor resume | Afecta al ciclo CHANGES -> Builder -> Manager y debe revisarse junto al bus. |
| `WT-2026-201` hardening runtime del launcher | Se convierte en subtema de pruebas de integracion del bus/launcher. |
| `WT-2026-206` scope gate y cierres manuales | Dependiente de la nueva autoridad de write-path y sus proyecciones. |
| `WT-2026-207` collaboration legacy | Queda pendiente hasta que el writer unico quede establecido. |
| Actor `SUPERVISOR` emitido por controller | Sigue como deuda semantica de eventos: actor logico vs proceso emisor real. |
| Drift `STATE.md`/`TURN.md`/bus durante requeue | Se reduce al centralizar la materializacion de proyecciones. |

### Deuda que no entra en WT-2026-211

| Item | Decision |
|------|----------|
| `WT-2026-198` idempotencia del instalador | Mantener separado: instalacion y rutas gestionadas, no ciclo bus/Manager/Builder. |
| `WT-2026-208` estabilizacion suite global | Esperar a WT-2026-211; despues clasificar fallos contra el nuevo contrato. |
| `WT-2026-209` nomenclatura workspace+motor | Mantener separado y posterior; mejor documentar despues de decidir arquitectura. |
| Repomix Windows/globby | Deuda devx independiente; no bloquea bus. |
| Redaccion de memoria / Claude Memory Mirror | Deuda de memoria y seguridad, no de orquestacion del bus. |
| `guard_paths` | Seguridad operacional separada; puede recibir requisitos de WT-2026-210 pero no debe mezclarse con el rediseno. |
| `--reset-circuit-breaker` manual | Mantener como herramienta de recuperacion posterior; WT-2026-210 debe decidir si sigue siendo necesaria. |

### Orden recomendado

1. Cerrar o congelar explicitamente `WT-2026-205`, dejando documentado el estado del bus y cualquier warning residual.
2. Abrir y ejecutar `WT-2026-211` como implementacion del write-path centralizado.
3. De `WT-2026-211`, derivar tickets hijos pequenos: watcher durable de CHANGES, actor/source en eventos, launcher bus-read, proyecciones canonicas y scope gate.
4. Solo despues ejecutar `WT-2026-206`, `WT-2026-207`, `WT-2026-208` y `WT-2026-209` con el contrato nuevo ya fijado.

## WT-2026-212 - Consumidor durable de CHANGES y requeue garantizado
- **Prioridad:** Alta
- **Scope:** system/bus-durable-requeue
- **Estado:** completed
- **Problema:** `REVIEW_DECISION=CHANGES` puede quedar sin consumidor durable si el supervisor reactivo anterior ya no esta vivo. Eso deja tickets huérfanos en `READY_FOR_REVIEW` hasta intervención manual o bootstrap tardío.
- **Objetivo:** garantizar que cada `CHANGES` tenga procesamiento durable y produzca relanzamiento o requeue sin depender de que el supervisor anterior siga vivo.
- **Sketch inicial:** reforzar el consumidor de `CHANGES` con una ruta durable y verificable; puede ser supervisor persistente, bootstrap watchdog explícito o disparo controlado de `ticket_supervisor.py --once`, pero debe quedar una sola autoridad observable en el bus.
- **Criterio:** un `REVIEW_DECISION=CHANGES` pendiente se procesa dentro de una ventana acotada sin intervención manual y sin tickets huérfanos.
- **Depende de:** WT-2026-211.
- **Cierre:** la ruta canónica queda en `bus/review_bridge.py`: `REVIEW_DECISION=CHANGES` -> `--request-changes` -> `_ensure_durable_changes_consumer(...)` -> `bootstrap()+run_once()` del supervisor. Tests focales y regresión de bridge aprobados.

## WT-2026-214 - Protocolo de forced close en preflight para ticket anterior y runtime stale
- **Prioridad:** Alta
- **Scope:** system/preflight-reconcile
- **Estado:** completed
- **Problema:** el launcher ya lee el bus como autoridad primaria para elegir agente, pero el preflight todavía no distingue formalmente entre limpiar runtime stale y reconciliar historia en el bus. Eso deja abierta la misma familia de drift que originó `WT-2026-205`.
- **Objetivo:** integrar una decisión de preflight con tres casos explícitos:
  - ticket previo terminal -> cleanup local;
  - ticket previo no terminal -> reconciliación canónica;
  - bus ilegible o contradictorio -> aborto.
- **Sketch inicial:** insertar la decisión entre `Assert-StartupAlignment` / `Repair-StartupSupervisorState` y `Remove-StaleRuntimeArtifacts`, reutilizando el bus como autoridad canónica e invocando `scripts/reconcile_ticket.py` solo cuando el drift no terminal esté confirmado.
- **Criterio:** abrir WT-N+1 con runtime stale de WT-N no mezcla historias: limpia si WT-N ya cerró, reconcilia si WT-N quedó colgado y aborta si no puede decidir con seguridad.
- **Depende de:** WT-2026-210, WT-2026-216.
- **Cierre:** implementacion aprobada y commiteada; cierre canonico emitido en el bus con `scripts/reconcile_ticket.py`; runtime stale de `WT-2026-214` limpiado antes de la migracion fisica del workspace.

## WT-2026-216 - Launcher lee el bus en vez de TURN.md para decidir que agente lanzar
- **Prioridad:** Alta
- **Scope:** system/launcher-bus-read
- **Estado:** completed
- **Problema:** el launcher sigue tomando su decisión operativa principal desde `TURN.md`. Si esa proyección queda stale aunque el bus refleje el estado correcto, puede relanzar el agente equivocado o no relanzar ninguno.
- **Objetivo:** mover la decisión de arranque a lectura del bus o de un helper canónico basado en el bus, dejando `TURN.md` como proyección operativa secundaria.
- **Sketch inicial:** introducir una ruta de decisión bus-read en `launch_agent_terminals.ps1`, con fallback explícito y acotado solo si el bus no puede leerse; cubrir el caso de `TURN.md` stale con tests focales.
- **Criterio:** con bus correcto y `TURN.md` stale, el launcher sigue eligiendo el agente correcto; el rescate durable de `WT-2026-212` pasa a ser fallback excepcional y no camino normal.
- **Depende de:** WT-2026-211.
- **Cierre:** `launch_agent_terminals.ps1` consulta `scripts/get_launcher_state.py` antes de leer `TURN.md`; el helper deriva estado vía `StateMachine.derive_state_from_events()` y los tests focales del launcher pasan.
- **Nota residual:** el mapeo `TicketState -> (role, action)` está duplicado entre `scripts/get_launcher_state.py` y `bus/supervisor.py`; candidata a ticket de limpieza posterior, no bloqueante.

## WT-2026-215 - Gates Modelo B: operaciones git de tooling resuelven motor_root
- **Prioridad:** Alta
- **Scope:** system/gates-motor-root
- **Estado:** backlog
- **Problema:** varias operaciones git del tooling corren con `cwd=project_root` (el workspace, que NO es repo git) en vez de `motor_root` (`orquestador_de_agentes/`, que SÍ es repo y contiene los commits). El resultado es `git diff` vacío y decisiones falsas. Sintoma verificado en esta sesion: el pre-check de packaging del review bridge (`check_review_packet_diff_empty`) reporta "empty review diff" y emite `REVIEW_DECISION=CHANGES` automatico aunque el Builder SI haya commiteado codigo real en el motor. Bloqueo dos ciclos seguidos en `WT-2026-214` sin que el Manager llegara a revisar codigo.
- **Causa raiz (VERIFICADA EN CODIGO):** `bus/review_bridge.py` -> `_git_diff_stat()`, `_resolve_review_base()` y `_build_diff_for_files_likely_touched()` usan `cwd=self.project_root`. `WT-2026-187` ya extrajo `runtime/motor_link.py` (`resolve_motor_root`) y listo `review_bridge.py` como consumidor, pero solo se migro `_resolve_motor_controller`; las funciones git quedaron sin migrar. Mismo patron en las gates diferidas de `WT-2026-205`: `prepush_check.py` y `session_closeout.py`.
- **Principio unificador:** todas las operaciones git del tooling resuelven `motor_root` via `motor_link` y corren con ese `cwd`. "Las operaciones git siempre corren en motor_root, punto."
- **Superficies a cubrir:**
  - `bus/review_bridge.py`: `_git_diff_stat`, `_resolve_review_base`, `_build_diff_for_files_likely_touched` (trigger principal de esta sesion).
  - `scripts/prepush_check.py`: gate Modelo B diferida de `WT-2026-205`.
  - `scripts/session_closeout.py`: invoca scripts asumiendo `project_root/scripts/`; gate diferida de `WT-2026-205`.
- **Sketch:** introducir un seam unico de resolucion de repo git (reusando `motor_link.resolve_motor_root`) y pasar ese `cwd` a toda invocacion de `git` del tooling de review/gates/closeout. Fallback explicito y acotado si no hay link ni repo.
- **Tests requeridos:** con workspace no-repo + motor con commits reales, `check_review_packet_diff_empty` devuelve False (diff visible); el pre-check no emite CHANGES espurio; `prepush_check`/`session_closeout` resuelven el repo del motor; fallback si no hay repo.
- **Criterio:** un Builder que commitea codigo real en el motor pasa el pre-check de packaging del bridge y el Manager revisa codigo de verdad; las gates de cierre operan sobre el repo del motor sin overrides manuales.
- **Depende de:** WT-2026-210. Relacionado: WT-2026-187 (motor_link), WT-2026-203 (introdujo el diff check), WT-2026-206 (scope gate, superficie adyacente).
- **Nota de simplificacion:** si el motor pasa a ser carpeta hermana del workspace (decision en curso), el principio se vuelve trivial de razonar: no hay repo anidado, el `cwd` de git es siempre el repo del motor sin ambiguedad. La migracion fisica no arregla este bug por si sola — el codigo sigue viviendo en el repo del motor — pero elimina la confusion conceptual.

## WT-2026-217 - Pre-check de packaging usa la ruta canonica de transicion al emitir CHANGES
- **Prioridad:** Alta
- **Scope:** system/bus-transition
- **Estado:** backlog
- **Problema:** cuando el pre-check de packaging del review bridge rechaza un paquete (diff vacio), emite `REVIEW_DECISION=CHANGES` pero NO completa la transicion canonica de estado: no emite `STATE_CHANGED -> IN_PROGRESS`. El ticket queda en `READY_FOR_REVIEW` en el bus con un CHANGES colgante, y el supervisor no puede reencolar (READY_FOR_REVIEW esta en `RELAUNCH_BLOCKED_STATES`). Resultado: sistema atascado que requiere cirugia manual del bus. Verificado en esta sesion (`WT-2026-214`): hubo que emitir `STATE_CHANGED -> IN_PROGRESS` a mano y reiniciar el supervisor para destrabar.
- **Distincion respecto a WT-2026-215:** son bugs independientes. `WT-2026-215` ataca la *causa* del rechazo falso (git en `cwd` equivocado -> diff vacio falso). Este ataca el *hazard de stall*: aunque el diff vacio sea legitimo (Builder que de verdad no commitea), el camino CHANGES del pre-check deja el supervisor colgado. Arreglar `WT-2026-215` reduce la frecuencia del trigger; este elimina el stall cuando el trigger es legitimo.
- **Causa raiz:** el camino CHANGES del pre-check se salta la ruta canonica de transicion. El CHANGES normal del Manager llama a `--request-changes`, que emite `STATE_CHANGED -> IN_PROGRESS` (o HUMAN_GATE) y luego `_ensure_durable_changes_consumer` (`WT-2026-212`). El pre-check emite el `REVIEW_DECISION` directamente sin pasar por esa maquinaria.
- **Sketch:** hacer que el camino CHANGES del pre-check use la MISMA ruta canonica que el CHANGES normal: invocar `--request-changes` (transicion + ApprovalRequest si aplica) y `_ensure_durable_changes_consumer`. Una sola autoridad de transicion, coherente con `WT-2026-211`/`WT-2026-212`.
- **Tests requeridos:** un pre-check que rechaza por diff vacio produce `STATE_CHANGED -> IN_PROGRESS` en el bus; el supervisor reencola sin intervencion manual; no hay doble relaunch; el caso de diff valido no cambia.
- **Criterio:** un rechazo de packaging (falso o legitimo) deja el ticket en estado consistente y reencola al Builder por la ruta durable, sin cirugia manual del bus.
- **Depende de:** WT-2026-210. Relacionado: WT-2026-203 (introdujo el pre-check), WT-2026-212 (ruta canonica de CHANGES), WT-2026-215 (misma region de codigo: pre-check de `review_bridge.py`).

## WT-2026-213 - Eliminar el doble STATE_CHANGED de --mark-ready
- **Prioridad:** Baja
- **Scope:** system/bus-events
- **Estado:** backlog
- **Problema:** `--mark-ready` emite dos eventos `STATE_CHANGED` consecutivos para la misma transicion a `READY_FOR_REVIEW`. Es idempotente en efecto practico (el estado derivado es el mismo), pero ensucia el bus y complica auditorias y cualquier consumidor que asuma unicidad de eventos de transicion.
- **Impacto:** ruido semantico, no fallo operativo. Ningun stall ni drift conocido atribuible a esto. Por eso Baja.
- **Sketch:** identificar los dos emisores en el camino de `--mark-ready` (controller + sync de targets) y dejar una sola emision canonica. Verificar contra `bus/state_machine.py` que no se rompa la derivacion.
- **Tests requeridos:** `--mark-ready` emite exactamente un `STATE_CHANGED -> READY_FOR_REVIEW`; estado derivado intacto; idempotencia de re-ejecucion preservada.
- **Criterio:** una sola transicion canonica por `--mark-ready`; bus sin evento duplicado.
- **Depende de:** WT-2026-210.

## WP-2026-176 - Implantar Modelo B workspace/code-only
- **Prioridad:** Alta
- **Scope:** system
- **Estado:** completed
- **Problema:** existen dos `.agent` paralelos; `z_scripts/.agent` debe ser workspace canonico y `orquestador_de_agentes/` motor code-only.
- **Sketch:** bridge/launcher resuelven controller desde `motor_root` con `--project-root`; guard anti-drift; tests; backup; migracion fisica; bus limpio.
- **Criterio:** `AGENT_PROJECT_ROOT=C:\Users\fdl\Proyectos_Python\z_scripts python orquestador_de_agentes\.agent\agent_controller.py --validate --json --force` funciona sin bus historico ni controller local.
- **Notas:** no migrar bus historico como bus vivo.

## WP-2026-177 - Unificar schema memoria + bridge por domain
- **Prioridad:** Alta
- **Scope:** system/meta
- **Estado:** completed
- **Problema:** `observations.jsonl` tiene schemas incompatibles y `review_bridge.py` solo lee `topic == manager-review-rubric`.
- **Sketch:** schema canonico con `id`, `domain`, `scope`, `wing`, `confidence`, `source_ticket`; migracion retrocompatible; bridge consulta dominios relevantes.
- **Criterio:** Manager ve observaciones de `review-quality`, `delivery-hygiene`, `builder-contract`, `testing` y fallback por topic legacy.
- **Depende de:** WP-2026-176.

## WP-2026-178 - L2/L3 memory rules + memory_loader.py
- **Prioridad:** Media
- **Scope:** system/meta
- **Estado:** completed
- **Problema:** la memoria se carga como observaciones sueltas; falta destilacion reusable y carga centralizada.
- **Sketch:** `memory_consolidate.py` genera `memory_rules.md` y `memory_profile.md`; nuevo `bus/memory_loader.py`; hooks y review bridge delegan en loader.
- **Criterio:** bootstrap carga L3, Builder/Manager cargan L2 por dominio, L1 queda para drill-down.
- **Depende de:** WP-2026-177.

## WP-2026-180 - Persistencia de sesion Builder entre relaunch (--session OpenCode)
- **Prioridad:** Media
- **Scope:** system
- **Estado:** completed
- **Problema:** cada relaunch del Builder por CHANGES abre sesion OpenCode nueva, recarga todo el contexto (50k+ tokens) y pierde el razonamiento previo.
- **Sketch:** (1) launcher guarda session ID en `.agent/runtime/builder_session.json` al arrancar; (2) en relaunch por CHANGES, ejecutar `opencode run <feedback> --session <ID>` en vez de sesion limpia; (3) fallback a sesion limpia si el ID no existe o sesion fue killed.
- **Advertencias:** verificar que `--session` mantiene contexto de archivos (no solo conversacion); probar fallback con sesion killed; medir token savings reales antes de asumir el beneficio.
- **Criterio:** relaunch por CHANGES reanuda sesion cuando viable; fallback transparente; tokens en segundo relaunch menos del 20pct del primero.
- **Depende de:** WP-2026-178 (completado).

## TBD - guard_paths: proteger archivos de estado del workspace
- **Prioridad:** Baja
- **Scope:** system
- **Estado:** backlog
- **Problema:** `guard_paths.py` usa patrones de seguridad (privada, .env) pero no protege archivos de estado del workspace (work_plan.md, execution_log.md). En Modelo B, si el cwd es el motor, el guard no "ve" el workspace — work_plan.md puede sobreescribirse accidentalmente. Incidente: WP-2026-178 pisó WT-2026-182 en sesión 2026-05-30.
- **Sketch:** añadir a `guard_paths.py` una lista de archivos de estado sagrados del workspace resueltos vía `AGENT_PROJECT_ROOT`; cualquier write a esos paths requiere confirmación explícita.
- **Criterio:** intentar editar `z_scripts/.agent/collaboration/work_plan.md` desde Claude Code muestra alerta de guard y requiere confirmación.
- **Depende de:** WT-2026-182 (completado).

## WT-2026-182 - Integracion Repomix para Context Bootstrapping y Repo-Compare
- **Prioridad:** Media
- **Scope:** system/skills
- **Estado:** backlog
- **Problema:** En el arranque, los agentes exploran "a ciegas" perdiendo turnos; además, las herramientas de repo-compare son lentas fichero a fichero.
- **Sketch:** 
  1) `repomix-context`: generar `.agent/context/repomix.xml` (con `--compress`) del workspace en arranque y pasarlo como `-f` a los agentes para inyección de contexto Cero-Turno.
  2) `repo-compare`: usar repomix para empaquetar origen + destino en XMLs comprimidos para que el agente reciba ambos de golpe detectando gaps inmediatamente.
- **Criterio:** El agente arranca recibiendo todo el contexto comprimido automáticamente (sin overhead notable en repos pequeños), y la herramienta de repo-compare empaqueta y compara vía Repomix.
- **Notas:** Depende de Node.js (que ya está instalado por OpenCode). Ideal usar opción `--compress` nativa de Tree-sitter.

## WT-2026-185 - Knowledge Layer: Glosario + Microagent + skill_resolver
- **Prioridad:** Media
- **Scope:** system/knowledge
- **Estado:** completed
- **Problema:** Los agentes carecían de marco canónico de terminología y onboarding; el skill_resolver fallaba silenciosamente ante catálogos vacíos.
- **Sketch:** actualizar `EmptySkillCatalogError` para mencionar `.agent/microagents/`; crear `agent_system/templates/glossary.md` (14 términos); crear `templates/microagents/onboarding.md` con triggers y heurísticas de tech stack; integrar en instalador con guard `if not exists`; test unitario del mensaje.
- **Criterio:** excepción guía al usuario; instalador deposita knowledge docs; `--validate` no emite warning `host-project` tras install.
- **Depende de:** WT-2026-184.
- **Nota post-cierre:** los knowledge docs depositados en `.agent/` raíz son vulnerables al prune de `--sync` → corregido en WT-2026-186.

## WT-2026-186 - Idempotencia del instalador y contrato de rutas gestionadas
- **Prioridad:** Alta
- **Scope:** system/install
- **Estado:** backlog
- **Problema:** `scripts/install_agent_system.py --sync` puede podar `.agent/glossary.md` y `.agent/microagents/` en la segunda sincronizacion estricta. Esas rutas se depositan desde `agent_system/templates/`, no existen en `.agent/` fuente y no estan cubiertas por `LOCAL_DIRS`.
- **Decision de semantica:** `glossary.md` y `microagents/` son plantilla-una-vez: el instalador los crea si faltan, luego pertenecen al workspace destino. `--sync` no los sobrescribe, pero tampoco debe podarlos.
- **Sketch:**
  1) Introducir `INSTALLER_MANAGED_PATHS = {"glossary.md", "microagents"}` — constante separada de `LOCAL_DIRS` con semántica distinta: estas rutas se depositan una vez y luego pertenecen al destino; `--sync` no las poda pero tampoco las sobrescribe. NO usar `is_preserved()` (footgun: bloquearía sync si algún día se añaden a la fuente).
  2) Modificar `detect_destination_residues()` para excluir las rutas de `INSTALLER_MANAGED_PATHS` antes de podar.
  3) `copy_tree()`: corregir comportamiento — el allowlist se valida por archivo, no solo por directorio raíz; `shutil.copytree` sobre un dir parcialmente allowlisted puede meter archivos no permitidos. Alinear docstring con comportamiento real (hoy promete `RuntimeError`, hace `SKIP`+continue).
  4) Eliminar entrada fantasma `BACKUP_VERIFIED.md` de `MANIFEST.workspace` (no existe en fuente ni destino).
- **Tests requeridos:** `install && sync && sync` preserva knowledge docs; sync preserva glosario modificado por usuario; residuo real se poda; archivo no-allowlisted dentro de dir permitido no se copia; dry-run no escribe ni borra pero reporta correctamente; glosario y microagents existentes no se sobrescriben.
- **Criterio:** `--install && --sync && --sync` deja vivos y personalizados los knowledge docs de WT-2026-185, mientras los residuos reales siguen siendo podados.
- **Depende de:** WT-2026-185.

## WT-2026-187 - Portabilidad Modelo B y limpieza legacy
- **Prioridad:** Alta
- **Scope:** system/portability
- **Estado:** backlog
- **Problema:** varias rutas y comandos todavia asumen codigo local en el workspace o nombres fijos del motor. Esto debilita Modelo B y deja deuda legacy visible tras la auditoria de cierre.
- **Sketch:**
  1) Extraer `runtime/motor_link.py`: API `resolve_motor_root(project_root)`, `resolve_motor_controller(project_root)`, `resolve_motor_script(project_root, script_name)`. Lee `motor_destination_link.json`. Consumidores: `review_bridge.py`, `prepush_check.py`, `session_closeout.py`.
  2) Portabilidad: corregir `TEMPLATE_ROOT = Path(__file__).resolve().parent.parent` (bug activo: falla si motor se renombra); corregir log de éxito en install (usa `PROJECT_AGENT` global, debería usar `project_agent` local).
  3) Portabilidad Modelo B: `prepush_check.py` usa `.agent/agent_controller.py` relativo — rompe en destino puro; resolver vía `motor_link`; mismo problema en `session_closeout.py` (invoca 6+ scripts desde `project_root/scripts/`).
  4) Ampliar `_check_portability()` en `session_closeout.py` — hoy solo escanea `docs/markdowns/skills/.agent/rules` en `*.md`; no ve `scripts/`, `bus/`, `*.py`, `*.ps1` (los hardcodes de esta auditoría habrían sido invisibles).
  5) `.git` check frágil: `pre_handoff_guard.py` devuelve `valid=True` silenciosamente si `.git` no existe en `project_root` (bypass de todos los checks). Decidir: "sin .git → skip con warning" vs `git -C <path> rev-parse --is-inside-work-tree`.
  6) Limpieza legacy: eliminar `sync_agent_core.py` (deprecado v9.4.1, nadie lo importa, 35 occ mojibake); `strict_sync` no-op en `sync_agent_system()`; `import shutil` redundante en `copy_knowledge_docs()`.
  7) Mensaje `EmptySkillCatalogError` engañoso (dice "add microagents" pero resolver no las conoce); test superficial de WT-2026-185 — reemplazar por test que ejerce ruta real de catálogo vacío.
  8) Decisión explícita: `orquestador.py` usa rutas cwd (`Path(".agent/logs")`, allowlist/denylist) sin migrar a `runtime.project_root` + 9 occ mojibake. ¿Legacy o migrar?
  9) Comandos en `AGENTS.md` listan `python .agent/agent_controller.py` sin `--project-root` — contradice la arquitectura Modelo B documentada en el mismo archivo.
- **Criterio:** los comandos de cierre/calidad funcionan desde workspace destino Modelo B puro; chequeo de portabilidad detecta hardcodes en código fuente; no hay bypasses silenciosos en guards de higiene.
- **Depende de:** WT-2026-186.

## WT-2026-188 - Modularizacion progresiva de agent_controller.py
- **Prioridad:** Media
- **Scope:** system/architecture
- **Estado:** completed
- **Problema:** `.agent/agent_controller.py` concentra CLI, validacion, materializacion de estado y orquestacion. Es mantenible hoy, pero su tamano y centralidad elevan el coste de cambio.
- **Non-goal:** no crear codigo bajo `.agent/validators/` — viola Modelo B (`.agent/` es estado, no codigo del motor). Namespace del motor: `bus/validators/`, `runtime/validators/` o similar segun dependencias reales.
- **Sketch:** mapear responsabilidades internas (CLI dispatch, validacion, materializacion de estado, orquestacion) antes de mover nada; extraer solo funciones puras con tests previos; mantener `agent_controller.py` como fachada CLI estable; un modulo por responsabilidad; evitar refactors masivos sin cobertura previa.
- **Criterio:** cada extraccion conserva comportamiento, reduce complejidad local y mantiene compatibilidad de CLI.
- **Depende de:** WT-2026-187.

## Nota WT-2026-188 - cierre canonico y estados auxiliares
- `--manager-approve` debe cerrar el ticket canonico y limpiar los estados auxiliares del bridge/supervisor (`manager_bridge_state.json`, `supervisor_state.json`) para no arrastrar contexto del ticket anterior.
- El launcher debe seguir tratando esos estados auxiliares como parte de la alineacion inicial, no como ruido opcional.
- El cierre canonico debe validar que el ultimo commit no sea un checkpoint generico y que referencie el ticket activo correcto. Debe emitir `WARN` bloqueante con confirmacion explicita requerida, sin reescribir commits automaticamente.
- `--mark-ready` debe incluir un Builder ready evidence gate minimo: cambios reales fuera de `.agent/collaboration/`, evidencia no-boilerplate en `execution_log.md` y, si se parsea `Files Likely Touched`, al menos un path esperado en el diff.
- Tests principales de este alcance: `orquestador_de_agentes/tests/test_agent_controller.py`.
- Documentacion preparada: `PLAN_WT-2026-188.md` y `AUDIT_WT-2026-188.md`.

## TBD - Repomix falla en Windows por permisos Node.js/globby
- **Prioridad:** Baja
- **Scope:** system/devx
- **Estado:** backlog
- **Problema:** `npx repomix` falla con `Permission denied while scanning directory` en `z_scripts` y `orquestador_de_agentes` en Windows. El error ocurre en globby antes de aplicar filtros de include/exclude. PowerShell accede sin problemas; el bloqueo es específico de Node.js (posiblemente antivirus o Windows Search). Repomix es best-effort y no bloquea el arranque.
- **Sketch:** investigar ACLs con `icacls`, probar desactivar indexación de Windows Search en la carpeta, probar versión más reciente de repomix, o como alternativa usar `--working-dir` apuntando a un subdirectorio accesible.
- **Criterio:** `npx repomix --compress` genera `.agent/context/repomix.xml` sin errores en el siguiente arranque del launcher.
- **Depende de:** WT-2026-182.

## WT-2026-189 - Guard anti doble lanzamiento de Builder tras CHANGES
- **Prioridad:** Alta
- **Scope:** system/bus
- **Estado:** completed
- **Problema:** tras `REVIEW_DECISION: changes`, el Supervisor puede relanzar Builder y hacer cooperative exit; el bridge puede ver el lock stale y lanzar un segundo Builder para el mismo ticket.
- **Sketch:** en `review_bridge.py`, antes de `requeue_ticket()`, comprobar si ya existe `BUILDER_RELAUNCH_ATTEMPTED` posterior al `REVIEW_DECISION: changes` procesado. Si existe, no relanzar. Si no existe, mantener comportamiento actual.
- **Tests requeridos:** `test_review_bridge_does_not_double_relaunch_when_supervisor_already_relaunched`; `test_review_bridge_relaunches_when_no_builder_relaunch_event_exists_after_changes`.
- **Criterio:** una decision `CHANGES` no produce dos ventanas Builder por la combinacion Supervisor + bridge.
- **Depende de:** WT-2026-187.

## WT-2026-190 - Rotacion segura de review_queue.md y contrato de memoria
- **Prioridad:** Alta
- **Scope:** system/hygiene
- **Estado:** completed
- **Problema:** `review_queue.md` supera los 2.6 MB y `manager_feedback_*` suma varios MB. No hay rotacion real para estas superficies, y `closeout_lessons.md` `CL-03` prohibe podado manual sin distinguirlo de rotacion automatica segura.
- **Decision:** usar estrategia `truncate-keeping-recent`, no full-rotate.
- **Sketch:**
  1) Crear/actualizar `memory_architecture.md` con una tabla de superficies: `canonical`, `projection`, `persistent-memory`, `private-mirror`, `cache`, `archive`; incluir owner, readers, writers, politica de rotacion y si puede cargarse en bootstrap.
  2) Integrar la rotacion en el flujo existente de cierre: extender `session_closeout.py` y/o `archive_collaboration_artifacts.py`, no crear un script suelto desconectado. Debe ejecutarse entre `_step_archive_collaboration` y `_step_archive_execution_log` para conservar el orden offline.
  3) Implementar rotacion offline de `review_queue.md` solo dentro del pipeline de `--session-close`, nunca con agentes activos.
  4) Documentar writers reales antes de tocar la rotacion: `bus/supervisor.py`, `scripts/manager_review_bridge.py`, `.agent/agent_controller.py`, `.agent/completion_checker.py`, `.agent/hooks/stop_hook.py` y cualquier writer adicional encontrado por grep.
  5) Antes de rotar, verificar como minimo `.agent/runtime/builder_lock.txt` y `.agent/runtime/supervisor_lock.txt`; si hay lock vivo, no rotar. Si existe mecanismo reutilizable para detectar Manager Bridge/Stop Hook vivos, usarlo como check best-effort. Si no existe mecanismo reutilizable, registrar warning advisory y proceder con la rotacion; no inventar detector fragil.
  6) Archivar entradas antiguas en `.agent/collaboration/archive/review_queue_YYYY-MM-DD.md`.
  7) Definir "entrada reciente" como una seccion logica delimitada por una linea que empiece con `## ` o por separador `---` en `review_queue.md`. No contar lineas. La cabecera canonica (`## Estado Actual`, `**Ticket:**`, `**Decision:**`) debe preservarse.
  8) Mantener en `review_queue.md` la cabecera canonica, el ticket activo si existe y las 10 entradas recientes mas relevantes.
  9) Archivar `manager_feedback_*` de tickets cerrados a `.agent/collaboration/archive/manager_feedback/`.
  10) Criterio de cerrado para `manager_feedback_*`: usar el bus como fuente canonica y archivar solo si hay cierre/aprobacion inequivoca del ticket. Si no se puede probar que el ticket esta cerrado, dejar el archivo vivo.
  11) Actualizar `closeout_lessons.md` `CL-03`: prohibido podado manual; permitida rotacion automatica offline del motor.
- **Tests requeridos:** no rota con `builder_lock.txt` vivo; no rota con `supervisor_lock.txt` vivo; archiva contenido antiguo y conserva ticket activo + 10 entradas recientes logicas; no cuenta lineas como entradas; solo archiva `manager_feedback_*` con cierre probado por bus; conserva feedback cuyo cierre no puede verificarse; rotacion idempotente; `CL-03` queda alineada con el comportamiento real.
- **Criterio:** tras `--session-close`, `review_queue.md` queda por debajo de 50 KB salvo que las 10 entradas conservadas lo impidan; si esas 10 entradas superan 50 KB, registrar warning advisory y conservarlas igualmente. Conserva cabecera, ticket activo y 10 entradas recientes logicas; todos los `manager_feedback_*` con cierre/aprobacion inequivoca en el bus quedan en `archive/manager_feedback/`; ningun archivo sin cierre probado se archiva.
- **Depende de:** WT-2026-189.

## WT-2026-201 - Hardening runtime del launcher tras WT-2026-200
- **Prioridad:** Media
- **Scope:** system/launcher
- **Estado:** backlog
- **Problema:** WT-2026-200 corrigio el bug real de precedencia `-OnlyBuilder` / `-ResumeBuilder`, pero aun quedan mejoras de robustez que conviene aislar para no reabrir un ticket ya cerrable: falta una prueba mas cercana al runtime real desde `bus/supervisor.py:_relaunch_builder()`, algunos tests dependen de asserts textuales sobre el `.ps1`, y el invariante de precedencia vive en codigo/tests pero no en una nota durable cercana al launcher.
- **Sketch:**
  1) Añadir un test o eval de integracion ligera que ejerza la invocacion real desde `_relaunch_builder()` hasta `launch_agent_terminals.ps1`.
  2) Reducir dependencia de asserts sobre texto literal del script PowerShell, favoreciendo verificaciones de comportamiento.
  3) Documentar cerca del launcher/supervisor que `-OnlyBuilder` tiene precedencia sobre `-ResumeBuilder` para la decision de lanzar supervisor.
- **Criterio:** una refactorizacion cosmetica del `.ps1` no rompe tests validos, el camino real supervisor -> launcher queda cubierto por al menos una prueba, y la precedencia de flags queda documentada junto al codigo que la implementa.
- **Depende de:** WT-2026-200.

## WT-2026-205 - Supervisor liveness; closeout diferido a WT-2026-210
- **Prioridad:** Alta
- **Scope:** system/closeout
- **Estado:** completed
- **Problema:** el ticket nacio para desbloquear closeout, pero durante la implementacion aparecio un bug mas urgente y verificable: el supervisor reactivo podia expirar por idle timeout mientras el Builder seguia trabajando en silencio.
- **Cierre documental:** se conserva como entregable real el fix de liveness del supervisor. El objetivo original de `prepush_check`/`session_closeout.py` se difiere a `WT-2026-210` porque los fallos restantes son contrato arquitectonico de `workspace activo + motor portable`, no bug puntual.
- **Criterio cumplido:** supervisor no aplica `idle_timeout` si `_builder_alive()` indica Builder vivo; `max_runtime` sigue siendo limite duro; tests focales y ruff focal pasan.
- **Diferido:** gates Modelo B, closeout real y governance de collaboration legacy.
- **Depende de:** WT-2026-204.

## WT-2026-210 - Auditoria integral y rediseno del bus multi-agente
- **Prioridad:** Critica
- **Scope:** system/bus-architecture
- **Estado:** approved
- **Problema:** los ultimos tickets revelaron deuda estructural en el contrato entre bus, Supervisor, Manager, Builder, controller, bridge, hooks, gates y closeout. Se estan acumulando hotfixes sin mapa completo de fuente canonica, proyecciones, liveness y requeue durable.
- **Sketch:** auditar eventos, actores, writers, transiciones, locks, gates Modelo B y surfaces legacy; separar hechos verificados de inferencias; proponer arquitectura objetivo minima y tickets hijos pequenos.
- **Criterio:** existe mapa de actores/writers, tabla de eventos, invariantes rotas/objetivo, frontera canonico/proyeccion/cache/legacy y backlog hijo para liveness, requeue durable, gates Modelo B y closeout.
- **Depende de:** WT-2026-205.

## WT-2026-206 - Scope gate y cierres manuales en workspace+motor
- **Prioridad:** Media
- **Scope:** system/hygiene
- **Estado:** backlog
- **Problema:** los cierres manuales en Modelo B siguen chocando con el scope gate porque el workspace `z_scripts` no es repo git y las rutas reales del motor viven en `orquestador_de_agentes/`. Esto obliga a `--scope-override` y `--force` en operaciones que deberian ser mas mecanicas.
- **Sketch:** resolver de raiz la relacion entre `Files Likely Touched`, motor subdir y proyecto raiz; reducir o eliminar la necesidad de overrides manuales en `--mark-ready` y `--manager-approve` bajo Modelo B.
- **Criterio:** los cierres manuales canonicos en Modelo B pueden completarse sin friccion estructural recurrente del scope gate.
- **Depende de:** WT-2026-210.

## WT-2026-207 - Gobernanza de collaboration legacy en el motor durante session-close
- **Prioridad:** Media
- **Scope:** system/hygiene
- **Estado:** backlog
- **Problema:** hoy existen dos superficies de collaboration: la activa en `z_scripts/.agent/collaboration` y una copia legacy/stale en `orquestador_de_agentes/.agent/collaboration`. El `session_closeout` solo opera sobre el workspace activo, por lo que la copia del motor acumula `manager_feedback_*`, `review_queue.md`, `work_plan.md`, `TURN.md` y `execution_log.md` obsoletos sin una politica explicita.
- **Sketch:** decidir y automatizar una de estas dos semanticas: (a) tratar la collaboration del motor como superficie legacy congelada y excluirla del lifecycle operativo; o (b) archivarla/limpiarla explicitamente durante `session-close` cuando `project_root != motor_root`. En ambos casos, dejarlo documentado y testeado para que no vuelva a parecer estado canonico.
- **Criterio:** tras un cierre de sesion, no queda ambiguedad sobre cual collaboration es canonica y la copia del motor no arrastra estado operativo engañoso.
- **Depende de:** WT-2026-210.

## WT-2026-208 - Estabilizacion de suite global tras transicion workspace+motor
- **Prioridad:** Alta
- **Scope:** system/testing
- **Estado:** backlog
- **Problema:** la suite global del motor esta rota de forma amplia tras la transicion a workspace+motor. Verificacion local el 2026-06-02: `46 failed`, `45 errors`, `1742 passed`, `21 skipped` en `uv run pytest orquestador_de_agentes/tests -q`. El informe previo del Builder ya apuntaba el problema, pero el recuento actual muestra que la deuda es mas grande de lo esperado.
- **Patrones observados:**
  1) tests que asumen cwd o rutas del motor (`test_windows_safe_temp_runtime`, `test_run_llm_evals`);
  2) tests que intentan renombrar o ocultar `.agent/` real del repo y fallan por permisos (`test_project_paths`, `test_migrate_legacy_project`, `test_upgrade`);
  3) drift de semantica en estado/cierre (`test_controller_integration`, `test_manager_approve`, `test_mark_ready_idempotency`, `test_ui_state`, `test_completion_checker`);
  4) mojibake y artefactos de encoding (`test_encoding_integrity`, `test_project_map_freshness`);
  5) fallos de sandbox/copias de fixtures en integracion (`test_completion_integration`).
- **Sketch:** inventariar fallos por familia, distinguir regresiones reales de tests obsoletos, y restaurar una baseline verde compatible con la arquitectura workspace+motor actual. La prioridad es recuperar confianza en la suite antes de seguir acumulando deuda en review/closeout.
- **Criterio:** la suite global vuelve a una baseline estable o, como minimo, queda segmentada en subconjuntos fiables con backlog explicito para el resto.
- **Depende de:** WT-2026-210.

## WT-2026-209 - Sustituir nomenclatura Modelo B por estandar workspace+motor
- **Prioridad:** Baja
- **Scope:** system/docs
- **Estado:** backlog
- **Problema:** el termino `Modelo B` sigue apareciendo en codigo, tests, changelog, AGENTS y prompts, pero ya no describe una opcion vigente. La arquitectura actual es una sola: workspace activo + motor portable separado. Mantener la terminologia antigua mete ruido conceptual y hace parecer que sigue habiendo modos paralelos.
- **Sketch:** inventariar referencias a `Modelo B` / `Model B`, decidir redaccion canonica (`workspace+motor`, `workspace activo`, `motor portable`) y actualizar codigo, docs, tests y mensajes de runtime para usar ese lenguaje de forma uniforme.
- **Criterio:** no quedan referencias activas a `Modelo B` en superficies operativas; la arquitectura se explica con una unica terminologia consistente.
- **Depende de:** WT-2026-210.

## WT-2026-196 - Manager adaptativo ante blockers repetidos
- **Prioridad:** Alta
- **Scope:** system/review
- **Estado:** active
- **Problema:** el Manager puede emitir el mismo feedback `CHANGES` durante varios ciclos aunque el Builder no resuelva un blocker concreto. En WT-2026-190 el Manager identifico blockers reales con archivo y linea, pero repitio instrucciones equivalentes sin activar un analisis nuevo del codigo ni proponer una solucion mas concreta. Subir `max_attempts` mitiga el bloqueo operacional, pero no corrige el patron de review repetitiva.
- **Decision:** mantener `manager_review.max_attempts` finito (`8`) y hacer que el Manager escale cognitivamente cuando detecte blockers repetidos. El objetivo no es aprobar mas facil ni hacer patching automatico, sino convertir feedback repetido en diagnostico accionable.
- **Sketch:**
  1) **Firma estable de blocker:** extraer de cada feedback una firma normalizada por blocker usando, en este orden de preferencia: `file:line`, `file:function`, `file + summary normalizado`. Normalizar mayusculas, espacios y prefijos decorativos (`BLOCKER`, bullets, markdown).
  2) **Historial del ticket:** antes de emitir `REVIEW_DECISION -> changes`, comparar los blockers actuales con el feedback anterior del mismo ticket (`manager_feedback_<ticket>.md`, review artifacts o bus segun superficie real usada por `manager_review_bridge.py`).
  3) **Umbral de repeticion:** si al menos un blocker reaparece en 2 reviews consecutivas, marcarlo como `REPEATED_BLOCKER`. Si el overlap de blockers por firma supera 50% entre dos reviews consecutivas, activar `DIAGNOSTIC_MODE`.
  4) **Modo normal (intentos 1-2):** mantener feedback actual: evidencia, severidad, archivo/linea, criterio de aceptacion.
  5) **Modo diagnostico (desde intento 3 o `REPEATED_BLOCKER`):** el prompt del Manager debe obligar a releer el codigo exacto afectado, comprobar si el Builder modifico el archivo desde el feedback anterior, comparar la condicion actual contra el blocker previo y explicar por que el fallo persiste.
  6) **Propuesta concreta:** en `DIAGNOSTIC_MODE`, cada blocker repetido debe incluir una seccion `Propuesta de solucion` con funcion exacta, condicion/logica esperada y test minimo. Si el cambio es pequeno y seguro, incluir un patch-plan textual (`old behavior` / `new behavior` o pseudo-diff), sin exigir al Manager que escriba codigo directamente.
  7) **HUMAN_GATE enriquecido:** si se alcanza `max_attempts`, el gate debe incluir resumen de blockers repetidos, intentos en que aparecieron, si el Builder toco o no los archivos afectados y la ultima propuesta concreta del Manager.
  8) **No falsos positivos:** no activar diagnostico por blockers distintos que comparten archivo pero no firma; no colapsar sugerencias menores con blockers bloqueantes.
- **Files Likely Touched:**
  - `orquestador_de_agentes/scripts/manager_review_bridge.py`
  - `orquestador_de_agentes/bus/review_bridge.py` si participa en la construccion del prompt o decision
  - `orquestador_de_agentes/.agent/config/agents.json` solo si necesita exponer umbrales configurables
  - `orquestador_de_agentes/tests/`
- **Tests requeridos:**
  - `test_repeated_blocker_signature_matches_same_file_line`
  - `test_repeated_blocker_signature_ignores_markdown_noise`
  - `test_diagnostic_mode_activates_after_repeated_blocker`
  - `test_diagnostic_mode_does_not_activate_for_distinct_blockers_same_file`
  - `test_manager_prompt_includes_code_reread_and_diff_check_in_diagnostic_mode`
  - `test_human_gate_includes_repeated_blocker_summary`
  - `test_max_attempts_remains_finite_and_configured_to_8`
- **Criterio:** ante dos reviews consecutivas con el mismo blocker, el siguiente feedback del Manager contiene `DIAGNOSTIC_MODE`, identifica si el Builder modifico el archivo afectado, explica por que el bug persiste y propone una solucion concreta con test minimo. Si el ciclo llega a HUMAN_GATE, el humano recibe una sintesis accionable, no solo una repeticion del ultimo feedback.
- **Depende de:** WT-2026-190.

## WT-2026-191 - Migracion determinista de memoria y bootstrap real
- **Prioridad:** Alta
- **Scope:** system/memory
- **Estado:** backlog
- **Problema:** `observations.jsonl` tiene schema mixto; `memory_rules.md` y `memory_profile.md` no existen; `session_bootstrap.md` describe L1/L2/L3 en prosa pero no ejecuta el loader.
- **Decision:** migrar a schema canonico usando solo dominios de `VALID_DOMAINS`; mantener compatibilidad legacy defensiva, pero el estado migrado debe validar limpio.
- **Mapping exacto:**
  - `audit_closeout` -> `domain: delivery-hygiene`, `topic: installer-managed-paths`.
  - `engineering_invariant` con `domain: bus/recovery` -> `domain: bus-architecture`, `topic: recovery-idempotency`.
  - `planning_rule` con `domain: ticket-planning` -> `domain: review-quality`, `topic: plan-test-path-verification`.
  - `testing_pattern` con `domain: validator-design` -> `domain: testing`, `topic: orthogonal-validator-tests`.
  - `engineering_invariant` con `domain: builder-control` -> `domain: builder-contract`, `topic: builder-evidence-gate`.
  - Entrada legacy obsoleta con `kind == "repo_state"` y campos `ts/text/kind` -> no migrar a memoria activa; conservar solo en backup/reporte como observacion obsoleta.
  - Entrada ya canonica `obs-commit-hygiene-protocol` -> mantener sin cambios.
- **Reglas de migracion:**
  1) Crear backup exacto `observations.jsonl.bak.<timestamp>` antes de escribir.
  2) La migracion es idempotente: una entrada que ya pasa `validate_observations.py` se deja intacta.
  3) Si `validate_observations.py` falla tras migrar, restaurar desde el backup y abortar; no dejar el archivo a medias.
  4) `date` o `ts` -> `timestamp` ISO-8601 UTC.
  5) `summary` o `text` -> `signal`.
  6) `ticket` -> `source_ticket`.
  7) Toda entrada migrada debe tener `source`; default `source: migrated:WT-2026-191`, salvo que exista `source` original.
  8) Si falta `id`, generar `obs-<hash-estable>`.
  9) Si falta `confidence`, usar `0.9`.
  10) Si falta `applies_to`, usar `mixed`.
  11) No introducir dominios nuevos en este ticket.
- **Bootstrap real:** crear un wrapper CLI real, por ejemplo `scripts/memory_context.py --bootstrap`, que delegue en `bus.memory_loader.get_bootstrap_context()`; actualizar `prompts/session_bootstrap.md` para pedir ese comando explicito, no solo describir la jerarquia.
- **L2/L3:** generar `memory_rules.md` y `memory_profile.md` mediante `memory_consolidate.py`; `get_bootstrap_context()` debe preferir L3, luego L2, luego L1.
- **Tests requeridos:** migracion produce schema exacto y valido; `kind == "repo_state"` queda fuera de activa pero preservado en backup/reporte; `validate_observations.py` falla antes de migrar si aplica y pasa tras migrar; loader no pierde contenido legacy si aparece como fallback defensivo; `scripts/memory_context.py --bootstrap` imprime contexto L3/L2; `session_bootstrap.md` referencia el comando real; ejecutar migracion dos veces no cambia entradas ya canonicas.

## TBD - Inventario y estabilizacion de suite global
- **Prioridad:** Media
- **Scope:** system/testing
- **Estado:** backlog
- **Problema:** tras cerrar el hotfix del launcher/supervisor, los tests relacionados con los archivos tocados ya pasan (`140 passed`, `ruff` limpio), pero la suite global sigue acumulando decenas de `fails/errors` en modulos no relacionados (`test_audit_rules`, `test_completion_checker`, `test_encoding_integrity`, etc.). Ese frente es independiente del hotfix actual y hoy no esta inventariado de forma util para decidir si bloquea el siguiente ticket o si es deuda preexistente.
- **Sketch:**
  1) Ejecutar la suite completa con captura de resumen por modulo.
  2) Construir un inventario corto de fallos agrupado por archivo/modulo.
  3) Clasificar cada grupo en una de dos cestas: `infraestructura/preexistente` o `regresion del ticket activo`.
  4) Identificar blockers reales para el flujo actual (`WT-2026-191`) frente a deuda de estabilizacion general.
  5) Decidir con evidencia si abrir ticket especifico de estabilizacion de suite o si basta con aislar y corregir solo los blockers del flujo actual.
- **Criterio:** existe un inventario breve, accionable y por modulo de la suite rota; cada grupo de fallos queda clasificado como preexistente o regresion actual; se toma una decision explicita sobre si la estabilizacion global entra antes o despues del siguiente ticket funcional.
- **Depende de:** WT-2026-191.
- **Criterio:** memoria canonica valida, L2/L3 pobladas y bootstrap consume loader de forma operativa.
- **Depende de:** WT-2026-196.

## WT-2026-192 - Claude Memory Mirror local opt-in
- **Prioridad:** Media
- **Scope:** system/devx
- **Estado:** completed
- **Problema:** Claude memory vive fuera del repo y no es portable. No debe convertirse en segunda fuente de verdad ni acoplarse a `--validate`, install o session-close.
- **Non-goals:** `install_agent_system.py` no lee ni escribe `~/.claude/`; `--validate` no depende de `~/.claude/`; `--session-close` no sincroniza Claude memory; CI no asume rutas locales de Claude.
- **Sketch:**
  1) Crear herramienta local opt-in, por ejemplo `scripts/claude_memory_mirror.py`.
  2) Usar ruta real canonica del motor: `.agent/runtime/memory/`.
  3) Exportar reglas compactas hacia Claude memory con dry-run por defecto.
  4) Importar solo observaciones seleccionadas con procedencia y dedupe.
  5) El check "Claude mas fresca que canonica" vive solo en este script.
- **Tests requeridos:** ruta `~/.claude/` inexistente no rompe; permiso denegado se reporta como warning local; `--validate` pasa sin Claude instalado; dry-run no escribe; dedupe evita duplicados.
- **Criterio:** Claude memory queda como mirror privado opcional, no como parte del motor portable.
- **Depende de:** WT-2026-191.

## WT-2026-197 - Supervisor post-restart sin Builder tras CHANGES
- **Prioridad:** Media
- **Scope:** system/bus
- **Estado:** active
- **Problema:** cuando el supervisor se cae durante un BUILDER_RELAUNCH_ATTEMPTED, al reiniciar lee el estado proyectado del bus. Si sigue siendo READY_FOR_REVIEW (porque el estado no se resetó a IN_PROGRESS antes del crash), despacha al Manager directamente sin relanzar Builder. Observado en WT-2026-192: seq 322 BUILDER_RELAUNCH_ATTEMPTED, seq 323 SUPERVISOR_RESTARTED, seq 324 MANAGER_REVIEWING sin Builder intermedio.
- **Root cause:** el supervisor en startup no distingue entre READY_FOR_REVIEW legítimo (Builder terminó) y READY_FOR_REVIEW espurio (crash durante relaunch post-CHANGES).
- **Sketch:** al reiniciar, el supervisor comprueba los últimos N eventos del bus. Si el último REVIEW_DECISION fue CHANGES y no hay BUILDER_EXIT posterior, forzar relaunch de Builder independientemente del estado proyectado. La condición es:  AND .
- **Tests requeridos:** supervisor reinicia con READY_FOR_REVIEW tras CHANGES sin BUILDER_EXIT → lanza Builder, no Manager; supervisor reinicia con READY_FOR_REVIEW legítimo (BUILDER_EXIT posterior a REVIEW_DECISION) → lanza Manager correctamente; test de regresión del doble-requeue (no debe dispararse).
- **Criterio:** tras reinicio del supervisor, el ciclo CHANGES → Builder → Manager se ejecuta siempre en orden correcto, incluso si el crash ocurrió entre REVIEW_DECISION y BUILDER_EXIT.
- **Depende de:** WT-2026-192.

## WT-2026-193 - Redaccion previa en pipeline de memoria persistente
- **Prioridad:** Baja
- **Scope:** system/security
- **Estado:** backlog
- **Problema:** `bus/redact.py` (redacta JWT, auth headers, API keys, emails, usernames de Windows) solo lo invoca `bus/event_bus.py`. El pipeline de memoria persistente NO redacta antes de escribir `observations.jsonl`, asi que un secreto en un output de tool o una ruta de usuario puede quedar persistido en memoria.
- **Origen:** evaluacion de patrones de `supermemoryai/opencode-supermemory` (tag `<private>`). Decision: no inventar mecanismo nuevo; cablear el `redact.py` existente. Ver [[reference-memory-tools-evaluated]].
- **Writers verificados a cubrir:**
  - `.agent/hooks/post_tool_hook.py` -> PRIORIDAD: es auto-ingest tras tool calls, el vector real de fuga.
  - `scripts/session_close_observations.py` -> escritor de cierre.
  - `scripts/memory_consolidate.py` -> consolidacion L1/L2/L3.
  - `.agent/runtime/memory/memory_helpers.py` y `tools/scripts/memory_manager.py` -> verificar si escriben observaciones; cubrir si aplica.
- **Sketch:** aplicar `redact.redact_text()` (o equivalente) sobre `signal`/`text` antes de persistir cada observacion; un solo punto de paso si es posible (helper compartido), no redaccion duplicada por writer.
- **Tests requeridos:** una observacion con API key / JWT / ruta `C:\Users\<user>\` se persiste redactada; `post_tool_hook` no escribe secretos crudos; redaccion idempotente; no rompe entradas sin secretos.
- **Criterio:** ninguna observacion nueva persiste secretos en claro; reusa `redact.py`, sin mecanismo paralelo.
- **Depende de:** WT-2026-191.

## WT-2026-218 - Regenerar y commitear memory_rules.md en el motor
- **Prioridad:** Media
- **Scope:** system/memory
- **Estado:** backlog
- **Problema:** el motor no tiene `memory_rules.md`. `install_agent_system.py` ya implementa `sync_memory_rules()` que fusiona wings engine/meta del motor al destino preservando el wing project del destino — pero si el motor no tiene `memory_rules.md`, el sync es un no-op y los destinos no reciben reglas portables. Verificado: `git log --oneline -- .agent/runtime/memory/memory_rules.md` devuelve vacio; el archivo no esta en history ni gitignoreado.
- **Causa raiz:** `memory_rules.md` es un artefacto derivado deterministamente de `observations.jsonl` via `memory_consolidate.py`. El motor tiene `observations.jsonl` vivo (35 KB, schema canonico) pero nunca se corrio la consolidacion para generar `memory_rules.md` y commitearlo.
- **Contexto clave (leer antes de ejecutar):**
  - `memory_consolidate.py` tiene flags `--apply` (default dry-run) y modifica `observations.jsonl` (dedupe+filter+archive). NO correr `--apply` sobre el motor sin revisar el dry-run primero.
  - El motor tiene `observations.jsonl` con cambios en working tree (modificado pero no commiteado a 2026-06-02). Verificar `git diff .agent/runtime/memory/observations.jsonl` antes de consolidar.
  - `memory_rules.md` generado contendra wings engine/meta/project derivados de las observaciones del motor. Revisar que las reglas son coherentes antes de commitear.
  - Una vez commiteado en el motor, el siguiente `--sync` en cualquier destino propagara automaticamente las wings engine/meta.
- **Sketch:**
  1) `git -C motor diff .agent/runtime/memory/observations.jsonl` — entender que cambio.
  2) `python scripts/memory_consolidate.py` (dry-run) desde el motor — ver que generaria.
  3) `python scripts/memory_consolidate.py --apply` — generar `memory_rules.md`, `MEMORY.md`, `memory_profile.md`.
  4) Revisar `memory_rules.md` generado: debe tener wings coherentes y reglas derivadas de tickets reales.
  5) Commitear en el motor: `memory_rules.md` (nuevo) + `observations.jsonl` (si cambio) + `MEMORY.md` (si cambio).
  6) Verificar que el motor tiene `memory_rules.md` en git y que `.gitignore` del motor NO lo ignora.
  7) Opcional: correr `install --sync --dry-run` en el workspace para confirmar que el sync ya ve la fuente.
- **Tests requeridos:** `memory_rules.md` existe en motor tras consolidacion; contiene al menos un wing engine o meta; `install --sync --dry-run` desde workspace reporta "Would sync memory_rules.md" en vez de "Motor has no memory_rules.md".
- **Criterio:** motor tiene `memory_rules.md` commiteado y el sync de destinos propaga wings engine/meta reales.
- **Depende de:** ninguno. Es el desbloqueador de WT-2026-219 y WT-2026-220.
- **Origen:** session-2026-06-02-memory-bootstrap

## WT-2026-219 - Bootstrap de memoria garantizado en destinos nuevos
- **Prioridad:** Media
- **Scope:** system/memory
- **Estado:** backlog
- **Problema:** `install_agent_system.py --install/--sync` no garantiza que el directorio `runtime/memory/` del destino tenga los archivos minimos. `sync_memory_rules()` hace `mkdir` pero solo si va a escribir `memory_rules.md`; si el motor no tiene ese archivo (situacion pre-WT-2026-218), ni siquiera crea el directorio. `observations.jsonl` y `MEMORY.md` no se crean en ninguna ruta del instalador.
- **Contexto clave:**
  - `memory_consolidate.py` asume que `MEMORY_DIR` y `OBS` ya existen; si se llama sobre un destino virgen, puede fallar o crear archivos en el motor en vez del destino (usa `get_agent_dir()` que resuelve segun contexto de ejecucion).
  - El sistema de wings (engine/meta/project) ya esta completamente implementado y es idempotente. Solo falta el bootstrap del esqueleto.
  - El workspace actual ya tiene los archivos por ser heredero de `z_scripts`, pero un destino nuevo instalado desde cero no los tendria.
- **Sketch:**
  1) Crear funcion `ensure_memory_skeleton(project_agent, dry_run)` en `install_agent_system.py`.
  2) Crea `runtime/memory/` si no existe.
  3) Crea `observations.jsonl` vacio `[]` si no existe (nunca sobreescribe si ya existe).
  4) Crea `MEMORY.md` con cabecera minima si no existe (nunca sobreescribe).
  5) Crea `memory_rules.md` con estructura de wings vacia si no existe Y el motor tampoco tiene fuente (fallback seguro).
  6) Llamar a `ensure_memory_skeleton` al inicio de `run_install()` y `run_sync()`, antes de `sync_memory_rules`.
  7) Tests: instalar en directorio vacio crea el esqueleto; instalar en directorio con memoria existente no la pisa; dry-run reporta "Would create" sin escribir; idempotencia (instalar dos veces no cambia nada).
- **Tests requeridos:** `install` en destino virgen crea `runtime/memory/{observations.jsonl,MEMORY.md}`; `sync` no pisa `observations.jsonl` con entradas; dry-run no escribe pero reporta; segunda ejecucion no altera nada.
- **Criterio:** cualquier repo destino recien instalado tiene esqueleto de memoria funcional sin intervencion manual; la memoria existente nunca se pisa.
- **Depende de:** WT-2026-218 (para que el sync posterior ya tenga fuente real).
- **Origen:** session-2026-06-02-memory-bootstrap

## WT-2026-220 - Flujo de promocion upstream de memoria para dogfooding
- **Prioridad:** Media
- **Scope:** system/memory
- **Estado:** backlog
- **Problema:** el flujo normal de memoria es downstream (motor -> destino via sync). Pero este workspace es dogfooding: sus tickets mejoran el motor, por lo que genera aprendizajes de wing engine/meta que deberian propagarse al motor, no quedarse solo en el workspace. `memory_upload.md` (prompt canonico en `orquestador_de_agentes/prompts/`) describe inspeccion y propuesta de memoria, pero solo contempla dos destinos: memoria del proyecto y memoria personal de Claude. No menciona promocion al repo motor externo.
- **Contexto clave:**
  - El modelo de wings ya hace la separacion conceptual: `engine`/`meta` = portables al motor; `project` = locales al destino.
  - La promocion debe ser MANUAL con propuesta asistida. No automatica en cierre de ticket (riesgo de contaminar el motor con aprendizajes a medio cocer).
  - La ruta fisica de promocion es: escribir observacion en `orquestador_de_agentes/.agent/runtime/memory/observations.jsonl` + reconsolidar motor (o dejar para siguiente sesion de consolidacion).
  - `memory_upload.md` ya tiene la estructura correcta ("no escribas todavia; primero propón"). Solo necesita un tercer destino posible.
- **Sketch:**
  1) Extender `memory_upload.md` con una seccion "Destinos posibles" que incluya explicitamente: (a) memoria del proyecto destino (`wing: project`), (b) motor externo (`wing: engine` o `meta`, escribe en `orquestador_de_agentes/.agent/runtime/memory/observations.jsonl`), (c) memoria personal de Claude (habitos transversales del usuario).
  2) La propuesta debe incluir el campo `wing` sugerido y el destino recomendado como parte del formato existente.
  3) Si el destino es el motor externo, la propuesta debe mostrar el texto exacto de la observacion en formato canonico (json) lista para insertar manualmente o con confirmacion explicita.
  4) El agente no escribe en el motor sin confirmacion humana explicita.
  5) Opcional: crear `scripts/promote_observation.py --to-motor` como herramienta CLI que automatiza el append a `observations.jsonl` del motor y emite un recordatorio de reconsolidacion pendiente.
- **Criterio:** al usar `memory_upload.md` en este workspace, el agente propone correctamente si un aprendizaje pertenece al proyecto, al motor o a Claude memory; el formato de propuesta incluye wing, destino y texto canonico; la escritura al motor requiere confirmacion humana.
- **Depende de:** WT-2026-219.
- **Origen:** session-2026-06-02-memory-bootstrap

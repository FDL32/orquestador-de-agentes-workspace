# Closeout Lessons

Lecciones curadas del ciclo de desarrollo del motor.
Leidas por el Manager en Paso 0b de `man-create-work-plan` antes de planificar.
Fuente: observaciones promovidas desde `observations.jsonl`.

---

## builder-contract

### CL-01 - Estado enum del controller (ticket-state-enum-contract)
`IDLE` es un sentinel de workspace sin ticket activo, no un estado valido del controller.
Al cerrar un ticket, `work_plan.md`, `execution_log.md` y `STATE.md` deben usar el enum
del controller: `APPROVED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `COMPLETED`.
Escribir `IDLE` en el motor activa errores de validacion y bloquea `--manager-approve`.
**Regla:** usar `IDLE` solo en workspaces destino sin ticket activo, nunca en el motor durante cierre.

### CL-02 - Consistencia de superficies al cierre (state-surface-separation)
`STATE.md`, `execution_log.md`, `work_plan.md` y `TURN.md` deben reflejar el mismo
estado antes de `--manager-approve`. Si difieren, el controller lo detecta como drift
y puede bloquear el cierre o producir un falso `APPROVE` sobre estado inconsistente.
**Regla:** verificar que las cuatro superficies coinciden antes de cualquier operacion de cierre.

### CL-11 - La autoridad cross-process de requeue es el claim atomico (atomic-requeue-claim)
El watermark de requeue parece suficiente hasta que dos supervisores compiten o
un subprocess reordena la escritura. Un read-modify-write compartido no sobrevive
esa carrera de forma fiable.
**Regla:** la autoridad real para requeue debe ser un claim atomico por
`(ticket_id, trigger_seq)` con `O_CREAT|O_EXCL`; el watermark solo puede ser
un fast-path en proceso. `trigger_seq` es obligatorio y `None` falla cerrado.

### CL-14 - Builder valida trabajo ya existente, no lo reimplementa (builder-validates-existing-work)
Cuando la implementacion ya esta commiteada, el valor del Builder no esta en
rehacer el cambio sino en contrastarlo de forma sistematica contra `AUDIT`,
`TP Check`, tests y gates de cierre. Reimplementar en ese punto introduce ruido
y puede ocultar que el trabajo real ya estaba hecho.
**Regla:** si la evidencia inicial muestra que el cambio ya existe, tratar el
rol Builder como verificacion estructurada y cierre canonico: reunir evidencia,
detectar gaps reales y aprobar o pedir cambios con base objetiva.

## delivery-hygiene

### CL-03 - review_queue.md es trazabilidad viva (review-queue-traceability)
`review_queue.md` es escrita por `manager_review_bridge.py` en cada review.
Editarla manualmente durante el cierre rompe la trazabilidad del ciclo y puede
causar que el bridge duplique o pierda entradas en la siguiente review.
**Regla:** no editar `review_queue.md` manualmente. Esta permitida la rotacion
automatica offline gestionada por el motor en `session_closeout.py` durante
`--session-close`, que preserva cabecera, ticket activo y 10 entradas recientes.
El podado manual queda terminantemente prohibido (ver WT-2026-190).

### CL-04 - No cerrar tickets unilateralmente (no-unilateral-ticket-close)
`--manager-approve` y cualquier cierre canonico que emita `SUPERVISOR_CLOSED`
son acciones irreversibles sobre el bus historico. Si un ticket esta en
`HUMAN_GATE`, el sistema esta pidiendo intervencion humana, no permiso implicito
para que un agente cierre el ticket.
**Regla:** ningun agente debe ejecutar `--manager-approve` ni cerrar un ticket en
`HUMAN_GATE` salvo peticion explicita del usuario o flujo automatico autorizado
sin blockers pendientes. Primero pedir confirmacion humana y preservar el bus.

### CL-12 - Un doble relanzado en el bus delata una carrera de requeue (double-requeue-diagnostics)
Si aparecen dos `BUILDER_RELAUNCH_ATTEMPTED` para el mismo ticket con `round`
distinto, el sistema no emitio un intento "duplicado" inocente: `requeue_ticket()`
corrio dos veces para la misma decision. Y si en historia antigua aparece
`outcome=success`, eso solo prueba que el launcher salio 0, no que el Builder
estuviera vivo.
**Regla:** diagnosticar ese patron como doble requeue real y usar la taxonomia
`builder_started_verified` / `builder_launch_unverified` para distinguir liveness
de un simple exit limpio del launcher.

## review-quality

### CL-05 - max_attempts es fusible, no obstaculo (max-attempts-safety-net)
`manager_review.max_attempts` protege al sistema cuando Builder y Manager entran
en loop. Subirlo a infinito o a un valor arbitrario oculta el problema y puede
dejar el sistema trabajando sobre feedback repetido sin mejora.
**Regla:** si el Builder repite fallos, mejorar el loop de review del Manager
(diagnostico, blockers repetidos, instrucciones mas concretas) antes de tocar el
limite. Mantener `max_attempts` finito salvo decision humana explicita.

### CL-06 - Tickets complejos necesitan AUDIT y contratos cerrados (complex-ticket-planning-contract)
Los tickets complejos generan fabricacion si el plan deja schemas, triggers o
criterios de aceptacion abiertos. Sin `AUDIT_*.md`, el Manager no tiene blockers
verificables y tiende a repetir feedback generico.
**Regla:** antes de arrancar tickets complejos, crear `AUDIT_<ticket>.md` con
BLOCKERs verificables, una seccion `TP Check`, y en `work_plan.md` una seccion
`Contratos de Implementacion Cerrados` con schemas, triggers, estados y artefactos
de Fase 1 definidos de forma exacta.

### CL-07 - El launcher es el unico dueno del closeout del Builder (launcher-owns-closeout)
El patron legacy donde un template o prompt del Builder inyecta `{{close_command}}`
o pide al agente ejecutar el cierre manualmente introduce dos riesgos: doble
closeout en backends legacy y tickets atascados si el runner muere antes de llegar
al final del turno. El cierre canonico del Builder ya vive en el launcher dentro
de un bloque `try/finally`.
**Regla:** no volver a inyectar `{{close_command}}` en templates o prompts del
Builder ni pedir al AI que ejecute `--pre-handoff` o `--mark-ready` manualmente
como parte del flujo normal. El launcher garantiza el closeout al salir el
proceso; el prompt solo describe la tarea tecnica.

### CL-08 - La memoria del workspace requiere scope-override (workspace-memory-scope-gate)
Los archivos de memoria del proyecto (`.agent/runtime/memory/observations.jsonl`,
`memory_rules.md`, `memory_profile.md` y similares) viven en el workspace portable
y no aparecen en el git diff del repo del motor `orquestador_de_agentes`. El
scope gate no puede ver esos cambios aunque sean el deliverable principal.
**Regla:** si un ticket modifica principalmente archivos de `.agent/runtime/memory/`,
el cierre con `--mark-ready` debe usar `--scope-override` con una razon explicita
indicando que los archivos viven en el workspace portable y no son git-tracked
dentro del repo del motor.

### CL-09 - Los mappings de migracion deben usar claves reales del dataset (dataset-keyed-migration-mapping)
Un contrato de migracion que se apoya en labels semanticos externos obliga al
Builder a inferir que filas del dataset corresponden a cada etiqueta. Eso abre la
puerta a fabricacion y a migraciones no deterministas. La clave del mapping debe
ser un valor real de los campos que ya existen en los datos.
**Regla:** todo mapping de migracion debe estar keyed en valores exactos del
dataset fuente (por ejemplo, `domain`, `kind` o `type` reales), nunca en nombres
conceptuales externos inventados para el plan. Si hace falta reinterpretar
semanticamente un registro, la correspondencia debe quedar explicitada con el
campo real que activa la regla.

### CL-10 - El auditor escéptico busca contraejemplos en el código real (auditor-skeptic-review)
Un contrato puede sonar impecable y aun asi fallar en detalles que solo aparecen
cuando se cruza contra el codigo real, la suite y las superficies de estado.
El Manager tiende a validar coherencia interna; el auditor escéptico busca el
contraejemplo concreto que rompa la hipotesis del plan.
**Regla:** cuando un ticket modifica contratos o superficies de control, revisar
el contrato contra el codigo real y los tests con mentalidad adversarial: firma
de mocks, rutas reales, comparaciones temporales, estados de retorno y carreras
entre procesos. Si aparece un contraejemplo, priorizarlo aunque el plan "suene"
correcto.

### CL-13 - Los fixes de una linea necesitan contrato minimo exacto (one-line-fix-contract-pattern)
En fixes pequenos con mucho riesgo de regresion, el contrato no gana valor por
crecer indiscriminadamente. Lo que evita derivas de verdad es cerrar tres cosas:
la mutacion exacta `old -> new`, el test que debe romperse por diseno y las dos
anti-regresiones simetricas alrededor del cambio.
**Regla:** para tickets de una linea o casi una linea, el plan debe nombrar la
cadena, simbolo o linea exacta que cambia, identificar cualquier test que haya
que migrar por rotura esperada y declarar explicitamente el caso corregido y el
caso legitimo que no debe romperse.

### CL-15 - Verifica si los tests del plan ya existen (planning-test-existence-check)
Antes de cerrar la seccion `Tests Esperados`, comprobar si cada test nombrado ya
existe en la suite. Cuando un test ya esta presente, deja de ser deliverable del
Builder y pasa a ser check de no-regresion; listarlo como "nuevo" abre la puerta
a duplicados silenciosos y a scope confuso.
**Regla:** antes de aprobar un PLAN/AUDIT, verificar existencia real de los tests
propuestos y distinguir explicitamente entre tests nuevos y tests ya presentes
que solo deben seguir pasando.

### CL-16 - Los snippets del plan son especificacion ejecutable (planning-snippets-are-executable-spec)
Regex, import paths, literales y pequenos fragmentos de codigo dentro del plan
no son prosa decorativa: Builder tiende a copiarlos verbatim. Un escape mal
puesto o un literal incorrecto convierte el propio contrato en la fuente del
fallo y genera tests rotos sin traza clara.
**Regla:** validar antes de lanzar cualquier snippet mecanico del plan que pueda
copiarse tal cual: regex en REPL, import paths reales y literales exactos.

### CL-17 - Los bugs cross-proceso necesitan prueba runtime real (runtime-proof-for-concurrency-fixes)
En bugs de concurrencia o coordinacion cross-proceso, una suite en verde no
prueba por si sola el comportamiento bajo scheduler real. El contrato puede ser
correcto y los mocks tambien, pero la carrera solo aparece o desaparece en un
ciclo vivo del bus.
**Regla:** para declarar resuelto un fix de este tipo, pedir al menos un ciclo
runtime real con evidencia del bus ademas de los tests automatizados.

### CL-18 - Files Likely Touched debe usar el formato exacto del diff (scope-gate-path-format)
`Files Likely Touched` no es una nota decorativa: el scope gate hace una
interseccion directa de strings con la salida de `git diff --name-only`.
Si el plan usa rutas con prefijo del workspace o del repo padre, la
interseccion queda vacia aunque el Builder haya tocado el archivo correcto.
**Regla:** escribir `Files Likely Touched` con rutas relativas al repo git del
motor, exactamente en el formato del diff. Ejemplo correcto: `bus/redact.py`.
Ejemplo incorrecto: `orquestador_de_agentes/bus/redact.py`.

### CL-19 - Corregir siempre los dos contratos del ticket (dual-contract-sync)
`work_plan.md` y `PLAN_WT-*` parecen duplicados, pero tienen lectores distintos.
`work_plan.md` gobierna validacion y estado canonico; `PLAN_WT-*` es el contrato
tecnico que lee Builder. Corregir solo uno deja al sistema y al Builder leyendo
dos verdades diferentes y suele forzar otra ronda de review.
**Regla:** cuando una revision cambie paths, firmas de funciones, tests o
alcance, aplicar la correccion a `work_plan.md` y a `PLAN_WT-*` en la misma
edicion.

### CL-20 - UTF-8 con BOM rompe validadores ligeros y degrada diagnosticos (bom-breaks-lightweight-validators)
Cuando un validador usa heuristicas simples (`^---` para frontmatter, lectura
por `cp1252` en subprocess, regex al principio de archivo), un BOM UTF-8 o una
codificacion heredada puede hacer que el contenido "parezca" sano al ojo humano
pero falle como si faltara por completo. El resultado es doble ruido:
falsos negativos de validacion y mojibake en mensajes de error.
**Regla:** en superficies operativas y artefactos parseados por heuristicas,
escribir UTF-8 sin BOM y forzar UTF-8 explicito en subprocesses que leen texto.

### CL-21 - El recovery Manager-Builder por chat ya es un patron validado (chat-manager-builder-recovery)
Cuando el cambio productivo ya existe o el bus queda a medio cerrar, el camino
estable no es insistir sobre el mismo flujo roto sino cerrar el `...a` por chat
con evidencia, reparar la trazabilidad minima y sacar los arreglos de
infraestructura a tickets derivados. Varias sesiones intensas confirmaron que
este patron reduce ruido y evita mezclar diagnostico con remediacion del bus.
**Regla:** si el bus o el `session-close` deriva pero la implementacion esta
verificada, usar cierre por chat del ticket base y mover la reparacion del flujo
automatico a follow-ups explicitamente trazados.

### CL-22 - El propio Manager es superficie corregible del sistema (manager-is-fix-surface)
Cuando el problema vive en el contrato del review, en un prompt o en una
expectativa de parser, tratar al Manager como "fuente intocable" prolonga el
fallo. La correccion del propio Manager forma parte normal del hardening del
sistema y debe documentarse igual que cualquier otra capa.
**Regla:** si una sesion demuestra que el error esta en instrucciones,
criterios o artefactos del Manager, corregir esa superficie de frente y dejar
la leccion curada en memoria en lugar de esconderla como incidente puntual.

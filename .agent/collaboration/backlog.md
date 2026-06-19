# Backlog (cola viva)

> Cola viva de tickets candidatos y en curso del workspace.
> NO es estado activo: el ticket activo vive en `work_plan.md`.
> Historico de tickets terminales: `.agent/collaboration/_archive/backlog_done.md`.
> Snapshot pre-corte WOT-2026-012a: `.agent/collaboration/_archive/backlog_pre_012a.md`.

## Politica

- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -- repo destino real.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` -- repo portable con `.git` propio.
- **Escritura:** humano o Manager; Builder solo lo toca si el plan lo pide explicitamente.
- **Contrato de cola viva (WOT-2026-012a):**
  - La tabla `Vista rapida` es la UNICA fuente parseable. No usar comentarios HTML como semantica obligatoria.
  - Estados permitidos en cola viva: `pending`, `blocked`, `deferred`, `ready-for-review`, `awaiting-manager`, `completed-partial`.
  - Estados terminales (`completed`, `done`, `closed`, `absorbed`) NO viven aqui: al cerrar, el Manager los mueve a `_archive/backlog_done.md` en un commit de documentacion (NUNCA via archivador del closeout/mark-ready).
  - Columna `Reactivation` obligatoria: `-` para estados activos sin trigger; `deferred`/`completed-partial`/`blocked` declaran trigger estructurado (`WOT-...`, `commit:<sha>`, `external:<ref>`, `condition:<slug>`).
  - `completed` solo cuando el bus confirma `STATE_CHANGED -> COMPLETED`; antes, usar `ready-for-review` o `awaiting-manager`.

## Vista rapida

| Prioridad | Ticket | Titulo | Scope | Estado | Depende de | Origen | Reactivation |
|-----------|--------|--------|-------|--------|------------|--------|--------------|
| Alta | WOT-2026-002c | A2d: eliminar copias motor-provides + ejecutar decisiones (FASE3 diferida) | system/host-extends | completed-partial | WOT-2026-002a, WOT-2026-002b | session-2026-06-13-host-extends | condition:install-sync-revendor-resuelto |
| Alta | WOT-2026-010x | Sustituir gitleaks-action licenciado por CLI OSS en security-audit.yml | motor/ci-security | pending | - | session-2026-06-19-gitleaks-ci | - |
| Alta | WOT-2026-011b | Relaunch timeout determinism: fijar BUILDER_START_VERIFY_TIMEOUT_SECONDS en tests de relaunch | motor/test-suite-perf | pending | - | session-2026-06-19-process-debt | - |
| Alta | WOT-2026-011e | pytest-xdist opt-in + medicion + fallback seguro para subset unitario | motor/test-suite-perf | pending | - | session-2026-06-19-improvement-backlog | - |
| Alta | WOT-2026-011h | Barrera de archivado tambien en mark-ready | motor/collab-hygiene | pending | WOT-2026-011a, WOT-2026-011d | session-2026-06-19-improvement-backlog | - |
| Alta | WOT-2026-012a | Reestructurar backlog: cola viva vs historico + formato parseable | system/collab-hygiene | blocked | - | session-2026-06-19-backlog-contract | WOT-2026-011j |
| Alta | WOT-2026-011j | Corregir fuente BOM en writer PowerShell y preparar regeneracion limpia de 012a | motor/devex-encoding | pending | WOT-2026-011c | session-2026-06-19-011c-followup | - |
| Media | WOT-2026-011f | .gitattributes / line endings: normalizar contrato multiplataforma | motor/devex-encoding | pending | WOT-2026-010w, WOT-2026-011c | session-2026-06-19-improvement-backlog | - |
| Media | WOT-2026-011g | Prompts/politica: explicitar 'loop rapido' vs 'cierre canonico' | motor/protocol-docs | pending | WOT-2026-010c, WOT-2026-010q | session-2026-06-19-improvement-backlog | - |
| Media | WOT-2026-012b | Gate check_backlog_contract.py sobre cola viva | motor/quality-gates | pending | WOT-2026-012a | session-2026-06-19-backlog-contract | - |
| Baja | WOT-2026-010m | Piloto xdist/sharding en CI para subset unitario aislado | motor/ci-performance | deferred | WOT-2026-010j, WOT-2026-010k | session-2026-06-17-suite-performance | condition:011e-estable-y-barrera-state-leak-verde |
| Baja | WOT-2026-011i | Si 011e sale estable: evaluar default unit en run_pytest_safe.py | motor/test-suite-perf | pending | WOT-2026-011e | session-2026-06-19-improvement-backlog | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |

> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist/sharding en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Solo tickets vivos con ficha congelada. El resto de tickets vivos (011b, 011f, 011g, 011i, 010m, 010x, 002c, 256a) tienen su contrato resumido en la tabla; su ficha `###` se materializa al congelar cada uno (deuda senalada por WOT-2026-012a).

### WOT-2026-012a - Reestructurar backlog: cola viva vs historico + formato parseable
- **Prioridad:** Alta
- **Scope:** system/collab-hygiene
- **Estado:** blocked
- **deliverable_type:** mixed
- **delivery_authority:** repo_destino
- **Depende de:** -.
- **Reactivation:** WOT-2026-011j (aplicar fix de fuente BOM-safe en writer PowerShell y sanear los 3 control chars historicos para regenerar snapshot/historico limpios y reintentar handoff canonico).
- **Supersede / Merge decision:** absorbe el objetivo de `WT-2026-250c`.
  Decision `011e <-> 010m` ya tomada: `keep-both-with-boundary`.
  `011e` queda acotado a runner local opt-in sobre subset unitario;
  `010m` conserva el piloto CI/xdist aislado. `011e` no puede congelarse en
  `work_plan.md` si su contrato vuelve a invadir el alcance CI de `010m`.
- **Origen:** session-2026-06-19-backlog-contract.
- **Problema:** `backlog.md` mezcla cola viva, fichas operativas e historico de
  cierres. La politica escrita promete que los tickets cerrados pasan a
  `CHANGELOG.md`, pero el archivo ha retenido terminales y comentarios forenses
  hasta convertirse en un pseudo-CHANGELOG. La tabla activa tampoco es fuente
  parseable robusta hoy, y las fichas `###` no cubren de forma consistente los
  tickets vivos de alta prioridad.
- **Objetivo:** dejar `backlog.md` como cola viva con formato parseable estable,
  separar el historico mediante un paso explicito del Manager en commit normal
  de documentacion y fijar el contrato minimo que luego consumira `012b`.
- **Files Likely Touched:**
  - Builder repo_destino: `.agent/collaboration/backlog.md`
  - Builder repo_destino: `.agent/collaboration/_archive/backlog_done.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `CHANGELOG.md`; `STATE.md`; `TURN.md`;
  `.agent/planning/ticket_contracts.md`; historico previo de `backlog.md`;
  filas `011e`..`011i`; `WOT-2026-010m`.
- **Contrato operativo a fijar:**
  - La tabla activa es la unica fuente parseable; los comentarios HTML pueden
    sobrevivir como nota humana, pero dejan de ser semantica obligatoria.
  - La tabla activa usa columnas fijas y vocabulario cerrado para el estado.
  - El schema entregable de la tabla activa incluye explicitamente la columna
    `Reactivation`.
  - `Reactivation` es obligatoria para `deferred` y `completed-partial`; para
    el resto el valor puede ser `-`.
  - Formato minimo de `Reactivation`: `-` es exclusivo de estados que no
    requieren reactivacion (`pending`, `blocked`, `ready-for-review`,
    `awaiting-manager`). Para `deferred` y `completed-partial`, debe existir un
    trigger real y verificable con formato estructurado (`WOT-...`,
    `commit:<sha>`, `external:<ref>` o `condition:<slug>`). Valores como `-`,
    `N/A`, `pendiente` o equivalentes vagos no cumplen el contrato.
  - La cola viva, a efectos de `012a` y del conteo objetivo, incluye solo
    filas con `Status in {pending, blocked, deferred, ready-for-review,
    awaiting-manager, completed-partial}`; los terminales viven fuera de la
    cola activa.
  - El movimiento de terminales al historico NO ocurre dentro de
    `--session-close` ni `--mark-ready`: lo hace un paso explicito del Manager
    en commit normal de documentacion.
  - Antes de cualquier corte del historico debe existir un snapshot/backup del
    `backlog.md` original como evidencia de recovery documental.
  - El corte del historico debe hacerse por bloques logicos auditablemente
    reconocibles (familias completas o grupos por estado terminal), no por
    copy-paste disperso de lineas individuales.
  - Una ficha `###` es obligatoria para cualquier ticket con `Priority=Alta` o
    `Status in {pending, ready-for-review, awaiting-manager}`.
  - El encabezado de cada ficha debe ser exactamente el ID canonico del ticket
    (por ejemplo `### WOT-2026-012a`); no se permiten variantes abreviadas.
- **Criterios binarios:**
  - `backlog.md` activo deja de contener terminales vivos mezclados con la cola
    operativa.
  - Existe un historico separado (`_archive/backlog_done.md` o decision
    equivalente documentada) mantenido por paso explicito del Manager, no por
    el archivador del closeout.
  - Antes de commitear el corte, existe evidencia mecanica de integridad del
    movimiento (conteo de filas terminales y conteo de fichas `###` movidas,
    antes/despues), suficiente para auditar que no se perdio historico.
  - La tabla activa queda en formato parseable estable y documentado, sin
    depender de HTML comments para semantica, e incluye la columna
    `Reactivation` como parte del schema obligatorio.
  - `deferred` y `completed-partial` declaran condicion de reactivacion y
    criterio de salida.
  - Las filas `011e`..`011i` quedan materializadas o reclasificadas de forma
    coherente con el contrato nuevo.
  - La decision `011e <-> 010m` queda resuelta como
    `keep-both-with-boundary`, con frontera explicita entre runner local
    opt-in (`011e`) y piloto CI/xdist (`010m`), antes de congelar `011e`.
  - `backlog.md` activo reduce tamano de forma material; objetivo operativo
    no bloqueante: aproximarse a una cola viva <= 200 lineas al cierre de
    `012a`.
  - `python scripts/check_encoding_guard.py` y
    `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
    quedan verdes.
- **STOP:**
  - Si separar vivo/historico exige tocar el archivador del closeout o anadir
    renames automaticos al cierre, detener: eso pertenece a `011h`/follow-up
    de runtime, no a `012a`.
  - Si la decision `011e <-> 010m` requiere una apuesta de producto no
    disponible, registrar `pending-human` y bloquear el congelado de `011e`
    sin inventar una fusion.

### WOT-2026-011j - Corregir fuente BOM en writer PowerShell y preparar regeneracion limpia de 012a
- **Prioridad:** Alta
- **Scope:** motor/devex-encoding
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011c.
- **Origen:** session-2026-06-19-011c-followup.
- **Problema:** `WOT-2026-011c` verifico dos fenomenos distintos: el BOM proviene de escrituras PowerShell 5.1 con `Set-Content`/`Out-File -Encoding UTF8`, mientras que los 3 control chars ya NO viven en la cola activa sino solo en `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md`. Parchear esos archives a mano mezclaria fix de fuente con reconstruccion historica. La ruta segura es endurecer el writer PowerShell en `repo_motor` y dejar que `012a` regenere despues sus artefactos historicos desde la fuente viva ya limpia.
- **Objetivo:** eliminar las escrituras BOM-prone in-scope del launcher/runtime PowerShell y dejar evidencia verificable de que `012a` debe reintentarse regenerando `_archive/backlog_*` desde el backlog vivo actual, no editando snapshots heredados a mano.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/launch_agent_terminals.ps1`
  - Builder repo_motor: `tests/test_opencode_config_stability.py`
  - Builder repo_motor: `tests/test_launch_agent_terminals_script.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`; `.agent/collaboration/backlog.md`; `.agent/collaboration/_archive/backlog_done.md`; `.agent/collaboration/_archive/backlog_pre_012a.md`; `CG-WOT-2026-012a.md`; `.agent/agent_controller.py`; `scripts/check_encoding_guard.py`.
- **Forbidden Surfaces:** editar a mano `_archive/backlog_done.md` o `_archive/backlog_pre_012a.md`; broad-strip de BOM/control chars en el repo; tocar `scripts/check_encoding_guard.py`; reintentar `012a` dentro de `011j`; tocar `TURN.md`/`STATE.md`/bus manualmente.
- **Premisa operativa a verificar al arrancar:**
  - `python scripts/check_encoding_guard.py .agent/collaboration/backlog.md` verde.
  - `python scripts/check_encoding_guard.py .agent/collaboration/_archive/backlog_done.md .agent/collaboration/_archive/backlog_pre_012a.md` rojo por los 3 control chars historicos.
  - `scripts/launch_agent_terminals.ps1` conserva al menos una escritura BOM-prone in-scope o, si no la conserva, el ticket debe bloquearse porque el fix ya no vive en la superficie declarada.
- **Criterios binarios:**
  - El diff elimina las escrituras PowerShell BOM-prone que este ticket declare in-scope y las sustituye por un patron BOM-safe verificable.
  - Existe al menos una barrera de regresion que falla sin el fix y pasa con el fix para la primitiva o ruta tocada por `011j`.
  - `tests/test_opencode_config_stability.py` sigue verde y documenta que el patron BOM-safe existente no regresa.
  - `011j` NO edita manualmente `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md`; deja explicitado en `execution_log.md` que esos artefactos se regeneraran al reactivar `012a`.
  - `python scripts/check_encoding_guard.py` sobre las superficies propias del ticket queda verde.
  - `uv run ruff check` sobre los Python tocados, `python -m pytest` focal aplicable y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:**
  - Si la premisa re-check demuestra que ya no existe ningun writer BOM-prone in-scope en `repo_motor`, detener y emitir `CONTRACT_GAP`: el follow-up ya no coincide con la superficie real.
  - Si la unica forma de poner verde el ticket exige editar manualmente los archives de `012a`, detener: esa regeneracion pertenece al relanzamiento de `012a`, no a `011j`.
  - Si el fix real exige tocar `agent_controller.py` o el guard de encoding en vez del launcher/runtime PowerShell declarado, detener y devolver a Contract Formation.
- **Reactivation / salida esperada:** tras cerrar `011j`, `WOT-2026-012a` debe relanzarse para regenerar `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` desde la fuente viva ya limpia.

### WOT-2026-012b - Gate check_backlog_contract.py sobre cola viva
- **Prioridad:** Media
- **Scope:** motor/quality-gates
- **Estado:** blocked
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-012a.
- **Origen:** session-2026-06-19-backlog-contract.
- **Objetivo:** convertir el contrato fijado por `012a` en una barrera
  automatica sobre la cola viva del backlog post-migracion de `012a`, sin
  depender de prose libre ni de HTML comments y con rollout
  `warning -> error` una vez asentado el formato.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/check_backlog_contract.py`
  - Builder repo_motor: `tests/unit/test_check_backlog_contract.py`
  - Builder repo_motor: integracion en `scripts/run_gates_dispatch.py` o en el
    flujo equivalente ya existente
- **Read/inspect only:** backlog migrado por `012a`; `scripts/run_gates_dispatch.py`;
  `scripts/check_deliverables_exist.py`; `scripts/validate_ticket_prose.py`;
  `STATE.md`; `TURN.md`.
- **Contexto de ejecucion:** el gate vive en `repo_motor`, pero debe leer
  `repo_destino/.agent/collaboration/backlog.md` resolviendo el proyecto por
  `--project-root <repo_destino>` o `AGENT_PROJECT_ROOT`; no puede depender del
  cwd dogfooding.
- **Fail-closed:** cualquier violacion estructural o semantica obligatoria de
  la tabla activa debe terminar con `exit != 0` cuando el gate opere en modo
  bloqueante; no puede degradar silenciosamente a warning salvo en el rollout
  explicitamente declarado.
  Si falta `--project-root` o `AGENT_PROJECT_ROOT`, tambien falla cerrado.
- **Criterios binarios:**
  - El gate parsea solo la tabla activa de `repo_destino`; no lee HTML comments
    ni prose libre para decidir estado o semantica obligatoria.
  - El gate valida estructura y contenido: columnas esperadas, encabezados de
    ficha exactos, vocabulario cerrado de `Status` y valores permitidos de
    `Reactivation`.
  - La lista de estados que define la `cola viva` se implementa como vocabulario
    cerrado codificado en el propio gate:
    `{pending, blocked, deferred, ready-for-review, awaiting-manager,
    completed-partial}`.
  - Sobre el formato post-migracion de `012a`, falla con `exit != 0` si hay
    estados terminales en la cola viva.
  - Sobre el formato post-migracion de `012a`, falla con `exit != 0` si una
    fila con `Priority=Alta` o `Status in {pending, ready-for-review,
    awaiting-manager}` no tiene ficha `###`.
  - Sobre el formato post-migracion de `012a`, falla con `exit != 0` si
    `deferred` o `completed-partial` no declaran `Reactivation` valida y
    criterio de salida en su ficha.
  - Sobre el formato post-migracion de `012a`, falla con `exit != 0` si una
    ficha declara solapamiento/supersede sin decision resuelta.
  - Existe test que demuestra fail-closed si el gate se ejecuta sin
    `--project-root` ni `AGENT_PROJECT_ROOT`.
  - Puede advertir, pero no fallar aun, si la cola viva supera el umbral de
    tamano acordado durante la fase de migracion.
  - Cada regla tiene test de barrera que falla sin el fix y pasa con el fix.
  - `ruff`, tests focales, suite aplicable y `validate` quedan verdes.
- **STOP / CONTRACT_GAP:**
  - Si el parser necesita recuperar semantica desde HTML comments o prose, el
    formato fijado por `012a` es insuficiente: devolver a `012a`.
  - Si la unica forma de mantener el historico sin limbo obliga a acoplar el
    gate al archivador del closeout, detener y coordinar con `011h` en vez de
    duplicar barreras.



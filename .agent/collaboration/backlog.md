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
| Alta | WOT-2026-011h | Barrera de archivado tambien en mark-ready | motor/collab-hygiene | pending | WOT-2026-011a, WOT-2026-011d | session-2026-06-19-improvement-backlog | - |
| Media | WOT-2026-011g | Prompts/politica: explicitar 'loop rapido' vs 'cierre canonico' | motor/protocol-docs | pending | WOT-2026-010c, WOT-2026-010q | session-2026-06-19-improvement-backlog | - |
| Media | WOT-2026-013a | Test de integracion fragil (test_approved_pending) + --validate-topology guard contra __file__ drift en sandbox | motor/test-robustness | pending | - | session-2026-06-20-hermes-audit | - |
| Baja | WOT-2026-010m | Piloto xdist/sharding en CI para subset unitario aislado | motor/ci-performance | deferred | WOT-2026-010j, WOT-2026-010k | session-2026-06-17-suite-performance | condition:011e-estable-y-barrera-state-leak-verde |
| Baja | WOT-2026-011i | Si 011e sale estable: evaluar default unit en run_pytest_safe.py | motor/test-suite-perf | pending | WOT-2026-011e | session-2026-06-19-improvement-backlog | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |

> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist/sharding en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

### WOT-2026-011b - Relaunch timeout determinism en tests de relaunch
- **Prioridad:** Alta
- **Scope:** motor/test-suite-perf
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Reactivation:** -
- **Origen:** session-2026-06-19-process-debt.
- **Problema (VERIFICADO):** `bus/builder_relaunch.py` ya expone la costura `_BUILDER_START_VERIFY_TIMEOUT_SECONDS` con default `20.0`, pero la familia de relaunch sigue apoyandose en helpers/polling temporizado y hoy no tiene un contrato explicito que fuerce tiempos cortos y deterministas al ejercer las rutas de verificacion. La deuda no es de producto sino de robustez de test: evitar waits dependientes del host y dejar evidencia clara de las rutas `builder_started_verified` / `builder_launch_unverified` sin tocar la semantica productiva del relaunch.
- **Objetivo:** fijar un contrato determinista para las pruebas de relaunch usando la costura existente de timeout, de modo que los tests que ejerzan la verificacion de arranque no dependan del timeout default ni del wall-clock del host, manteniendo intacta la semantica productiva y el valor por defecto del runtime.
- **Files Likely Touched:**
  - repo_motor: `bus/builder_relaunch.py`
  - repo_motor: `tests/test_supervisor.py`
  - repo_destino: `.agent/collaboration/execution_log.md`
- **Criterios binarios:** las pruebas de relaunch que ejercen verificacion temporal fijan explicitamente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` o una costura equivalente determinista dentro del propio test; el contrato productivo conserva `BUILDER_START_VERIFY_TIMEOUT_SECONDS` y `20.0` como default salvo refactor semantico neutro; existe al menos una barrera FAIL-sin/PASS-con que demuestra que la ruta temporizada deja de depender del timeout default del host; las rutas `builder_started_verified` y `builder_launch_unverified` siguen cubiertas sin cambiar su semantica observable; `pytest` focal, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** parar si la unica forma de volver deterministas los tests cambia la semantica productiva del relaunch o el default runtime; parar si la costura real del timeout cae fuera de `bus/builder_relaunch.py` / `tests/test_supervisor.py`; parar si para probar la ruta temporizada hace falta depender de sleeps wall-clock o procesos de launcher reales no acotables.
- **Depende de:** -.



### WOT-2026-013a - Test de integracion fragil + guard de topologia
- **Prioridad:** Media
- **Scope:** motor/test-robustness
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Reactivation:** -
- **Origen:** session-2026-06-20-hermes-audit (unico hallazgo verificado de la auditoria externa de Hermes).
- **Problema (VERIFICADO):** tests/test_controller_integration.py::test_approved_pending_returns_builder_implement
  es fragil ante el entorno de ejecucion: falla al correrse AISLADO (`pytest -k approved_pending`) y pasa
  dentro de la suite canonica (`run_pytest_safe --level all` = 0 failed). Causa raiz: el fixture copia
  agent_controller.py a un sandbox y el controller resuelve el proyecto via `__file__.parent.parent`, que en
  la copia apunta al sandbox (sin bus/scripts/prompts), no al motor real -> el controller devuelve
  role=UNKNOWN y data is None. NO es bug de produccion: el controller real funciona.
- **Objetivo:** (1) hacer el fixture robusto -> usar AGENT_PROJECT_ROOT real o PYTHONPATH en vez de copiar
  agent_system/, de modo que el test falle solo ante un bug real del controller; (2) opcional, anadir un
  guard `--validate-topology` en agent_controller que verifique que `__file__.parent.parent` cae dentro del
  repo_motor y no en un sandbox copiado, cerrando esta clase de drift.
- **Files Likely Touched:**
  - repo_motor: `tests/test_controller_integration.py`
  - repo_motor: `.agent/agent_controller.py` (solo si se implementa --validate-topology)
- **Criterios binarios:** el test falla SIN el fix solo ante bug real (no por fixture); pasa CON el fix tanto
  aislado como en suite; barrera de regresion que demuestre la diferencia; ruff + run_pytest_safe --level all
  0 failed; validate 0/0.
- **STOP:** si robustecer el fixture exige reescribir la arquitectura de copia de agent_system/ (deuda H-07),
  parar y abrir follow-up separado en vez de ampliar scope.
- **Depende de:** -.
- **Descartado de la auditoria de Hermes (ruido, NO accionar):** H-05 settings.json permissions.allow
  (FALSO: el archivo real no lo tiene, guard de portabilidad pasa); H-03/H-06/H-11 (conocidos por diseno);
  confusion motor-vs-destino (artefacto de su clon shallow Linux sin destino).


> Solo tickets vivos con ficha congelada. El resto de tickets vivos (011b, 011f, 011g, 011i, 010m, 010x, 002c, 256a) tienen su contrato resumido en la tabla; su ficha ### se materializa al congelar cada uno (deuda senalada por WOT-2026-012a).

### WOT-2026-012b - Gate check_backlog_contract.py sobre cola viva
- **Prioridad:** Media
- **Scope:** motor/quality-gates
- **Estado:** pending
- **deliverable_type:** code
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

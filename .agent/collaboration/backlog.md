# Backlog

> Tickets candidatos y planes futuros del workspace.
> No es estado activo: el ticket activo vive en `work_plan.md`.
> Al arrancar un item, se convierte en `work_plan.md`; al cerrarlo, pasa a `CHANGELOG.md`.
> Historico de tickets completados/absortos: ver `CHANGELOG.md` del motor.

## Politica
- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -- repo destino real.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` -- repo portable con `.git` propio.
- **Contrato:** mejoras globales se portan explicitamente al motor; nunca se asume sincronizacion implicita.
- **Escritura:** humano o Manager; Builder solo lo toca si el plan lo pide explicitamente.
- **Destino:** cada proyecto destino tendra su propio `.agent/collaboration/backlog.md`.

## Vista rapida

| Prioridad | Ticket | Titulo | Scope | Estado | Depende de | Origen |
|-----------|--------|--------|-------|--------|------------|--------|
| Media | WT-2026-250c | Poda documental de backlog y saneo de mojibake en superficies vivas | system/collab-hygiene | deferred | - | session-2026-06-11-system-audit |
| Alta | WT-2026-251b | Migrar el dogfooding al prefijo WOT como validacion viva | system/ticket-prefix-portability | done | WT-2026-251a, WT-2026-250a | session-2026-06-11-system-audit |  <!-- verificado: absorbido: backfill 9d97df7 + pipeline canonico 961f210 -->
| Alta | WT-2026-252a | Decision-artifact estructurado del Manager con fallback a parser NDJSON | system/review-decision-contract | done | WT-2026-248b | session-2026-06-11-system-audit |  <!-- verificado: 2dda386 + 886652b (decision artifact canal primario) -->
| Media | WT-2026-253a | Reescribir skill code-audit sobre CLIs directas | system/skills-product | done | - | session-2026-06-11-system-audit |  <!-- verificado: 02fdf81 -->
| Media | WT-2026-253b | Des-localizar repo-compare y graphify del entorno del autor | system/skills-product | done | - | session-2026-06-11-system-audit |  <!-- verificado: d19ff6b -->
| Media | WT-2026-253c | local_audit veraz y AUDIT.md autogenerado en el launcher | system/bootstrap-observability | done | - | session-2026-06-11-system-audit |  <!-- verificado: bd3f3a0 -->
| Media | WT-2026-254a | Deprecacion formal Goose/Claw fase 1 (docs y tests) | system/legacy-deprecation | done | - | session-2026-06-11-system-audit |  <!-- verificado: 3f6aad3 -->
| Media | WT-2026-254b | Regenerar .claude/rules del destino desde el estado real | system/docs-coherence | done | WT-2026-254a | session-2026-06-11-system-audit |  <!-- verificado: 3f6aad3 -->
| Media | WT-2026-255a | Extraer parser de decisiones de review_bridge a modulo propio | system/seam-extraction | done | WT-2026-252a | session-2026-06-11-system-audit |  <!-- verificado: 2dda386 + 886652b (decision artifact canal primario) -->
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked-external | - | session-2026-06-11-security-followup |  <!-- 2026-06-12: uv sigue resolviendo pip<=26.1.1; excepcion legitima -->
| - | WOT-AUDIT-A2a | Contrato de precedencia host-extends/motor-provides | system/host-extends | completed | - | session-2026-06-13-host-extends |  <!-- verificado: 6240dc0 + 26afa33 -->
| - | WOT-AUDIT-A2b | Manifiesto de triage por ruta del destino | system/host-extends | completed | WOT-AUDIT-A2a | session-2026-06-13-host-extends |  <!-- verificado: 4452e6f + bec8468 -->
| Alta | WOT-AUDIT-CI | CI del destino portable bajo host-extends | system/ci-portability | completed | WOT-AUDIT-A2b | session-2026-06-13-host-extends |
| Media | WOT-2026-002a | A2c: demo de clone limpio + install --sync sin copias legacy | system/host-extends | completed | WOT-AUDIT-A2b, WOT-AUDIT-CI | session-2026-06-13-host-extends |  <!-- verificado: cca3540 -->

| Media | WOT-2026-002b | ORPHANS: decision promover-vs-archivar de los 10 huerfanos | system/host-extends | completed | WOT-AUDIT-A2b, WOT-AUDIT-CI | session-2026-06-13-host-extends |  <!-- verificado: 48754f8 -->

| Alta | WOT-2026-002c | A2d: eliminar copias motor-provides + ejecutar decisiones | system/host-extends | completed-partial | WOT-2026-002a, WOT-2026-002b | session-2026-06-13-host-extends |  <!-- FASE1+2: 1a2d700+bf451f2 (162 removed+7 archived); FASE3 diferida (incidente install --sync); recovery 791787b -->
| Baja | WOT-2026-002d | LOG-COMPACT: compactar historico A2a en execution_log | system/collab-hygiene | absorbed | - | session-2026-06-13-host-extends |  <!-- premisa obsoleta: log ya compacto -->
| Alta | WOT-2026-003a | CI: validate falla en checkout por bus gitignored (invariantes COMPLETED sin eventos) | system/ci-portability | done | WOT-AUDIT-CI | session-2026-06-14-post-a2d-hardening |  <!-- motor cf59288 + release ea8936e; CI destino re-run SUCCESS -->
| Alta | WOT-2026-003b | Restaurar guard_paths hook (fail-closed) + des-personalizar settings.json del destino | system/security-hooks | completed | WOT-2026-002c | session-2026-06-14-post-a2d-hardening |  <!-- cd0ecfb; mitiga regresion fail-open de A2d -->
| Alta | WOT-2026-003c | Barrera estructural de hooks Claude en el motor (gate + entry script + test) | motor/security-hooks | completed | WOT-2026-003b | session-2026-06-14-post-a2d-hardening |  <!-- motor d6d2588 + 3e3b87a; destino 6a2f494; gate + claude_guard_entry + 22 tests; pre-commit -->
| Baja | WOT-2026-003d | install host-extends-aware: retirar bundle del destino sin re-vendorizar | motor/installer | pending | WOT-2026-002c | session-2026-06-14-post-a2d-hardening |  <!-- alias: MOTOR-FU-001. scope: repo_motor. A2d FASE3 lo necesita -->
| Baja | WOT-2026-003e | gates-dispatch: manejar 'destino sin tests locales' (run_pytest_safe exit 4) | motor/quality-gates | pending | WOT-2026-002c | session-2026-06-14-post-a2d-hardening |  <!-- alias: MOTOR-FU-002. scope: repo_motor. Hallazgo 002a -->
| Baja | WOT-2026-003f | CI del destino: paso que corre el gate de portabilidad contra su .claude/settings.json | system/ci-portability | pending | WOT-2026-003c | session-2026-06-14-post-a2d-hardening |  <!-- follow-up de 003c: protege el settings del destino via CI -->
| Alta | WOT-2026-004a | Suprimir 2 falsos positivos de gitleaks en CI del destino (scan full-history) | system/ci-portability | completed | - | session-2026-06-14-session-close |  <!-- 3e23873; .gitleaks.toml useDefault+allowlist tight; placeholder didactico (sk_live_1234567890) + SHA git publico (9c92e3d4, repo-compare WT-2026-236a); gitleaks 8.30.1 local 101 commits 0 leaks exit 0 -->
| Baja | WOT-2026-004b | Motor: seed .gitleaks.toml en bundle + politica generic-api-key-on-SHA en logs operativos + fix guard \.git over-match | motor/security-hooks | pending | WOT-2026-004a | session-2026-06-14-session-close |  <!-- scope: repo_motor. guard \.git (substring) bloquea Write a .gitleaks*/.github/ legitimos; verificado en guard_paths.py:25 -->


## Completados en sesion 2026-06-11 (audit integral)

| Ticket | Titulo | Commit(s) |
|--------|--------|-----------|
| WT-2026-248b | Alinear prompts wrapper y skills canonicas | 568f6a0 |
| WT-2026-249c | Review bridge: normalizar parseo de CHANGES | repo_motor |
| WT-2026-250a | Archivador reconoce sufijos de letra | d6d4461 |
| WT-2026-250b | Rotacion review_queue y split feedback digest/raw | 89ee4ac |
| WT-2026-250d | manager-approve resuelve repo git correcto | 31336f1 |
| WT-2026-251a | Centralizar ticket-ID regex + prefijos 2-3 letras | edbad61 |

> Nota: para historial previo ver `CHANGELOG.md` del motor (git conserva todo).

## WOT-2026-001x - Resolucion formal en closeout 2026-06-12

| Ticket | Estado | Resolucion formal |
|--------|--------|-------------------|
| WOT-2026-001a | absorbed | Absorbido por el endurecimiento ya entregado en pipeline + prompt (`WT-2026-248b` y contrato canonico derivado). |
| WOT-2026-001b | completed | Cerrado documentalmente en este closeout: el patron Manager -> Builder por chat queda validado y registrado como recovery canonico en memoria/changelog. |
| WOT-2026-001c | completed | Cerrado documentalmente en este closeout: se consolida la leccion de mojibake/BOM recurrente y la correccion del propio Manager como superficie legitima. |
| WOT-2026-001d | completed | Cumplido de facto: `review_bridge.py` ya esta por debajo del umbral (`2618 < 2700`). |

> Serie 001x resuelta sin abrir trabajo activo nuevo en `repo_destino`.

## Cadena WOT-AUDIT-A2 - Migracion host-extends / motor-provides (sesion 2026-06-13)

> Origen: auditoria host-extends. A2a (contrato de precedencia) y A2b (manifiesto
> de triage) ya cerrados y publicados. CI portable tambien esta cerrado y
> publicado. Autoridad de clasificacion: `.agent/docs/triage_manifest.md`.
> Estos tickets ejecutan el manifiesto.
>
> Nota de arranque 2026-06-13: el motor ya incluye el fix M3
> `bae1906`/`d21f6cc` publicado en `origin/main`. El ultimo `WOT-2026` emitido
> en el destino es `WOT-2026-001d`; los tickets nuevos usan IDs canonicos
> consecutivos `WOT-2026-002x` para que `manager-approve` valide commits sin
> `--force`; los IDs historicos `WOT-AUDIT-*` quedan como alias de auditoria.
>
> Orden de ejecucion por dependencias: WOT-2026-002a y WOT-2026-002b
> (paralelizables tras A2b+CI) -> WOT-2026-002c. WOT-2026-002d es independiente
> y de baja prioridad.

### Completados de la cadena
| Ticket | Titulo | Commit(s) |
|--------|--------|-----------|
| WOT-AUDIT-A2a | Contrato de precedencia + correccion STOP#1 | 6240dc0, 26afa33 |
| WOT-AUDIT-A2b | Manifiesto de triage por ruta | 4452e6f, bec8468 |
| WOT-AUDIT-CI | CI portable del destino via checkout publico del motor | 6b2cfc3, d2aac16, 53241cd |

## WOT-AUDIT-CI - CI del destino portable bajo host-extends
- **Prioridad:** Alta
- **Scope:** system/ci-portability
- **Estado:** completed
- **Cierre real:** completed (publicado). Mantener seccion como evidencia historica; no relanzar.
- **deliverable_type:** code
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Problema:** `.github/workflows/quality-gates.yml` ejecuta `compileall scripts tests`
  y `discover_skills.py` sobre copias locales. GitHub Actions hace checkout SOLO del
  destino: no hay motor sibling, asi que la migracion no puede "reapuntar" el CI a
  `../orquestador_de_agentes/`. Es el unico bloqueante machine-executed de A2d
  (ver `triage_manifest.md` bucket ci-portability-blocker).
- **Objetivo:** redefinir el CI para el modelo host-extends: o bien hace checkout del
  motor como segundo repo y corre sus tools con `AGENT_PROJECT_ROOT=<destino>`, o
  bien valida solo lo que el destino posee (estado `.agent/` via
  `agent_controller --validate`) y retira los gates que solo tenian sentido con
  copias vendorizadas.
- **Files Likely Touched:** `.github/workflows/quality-gates.yml`.
- **Criterio:** el workflow no depende de `scripts/`/`tests/`/`skills/` locales del
  destino; un push de prueba (o `act`/dry equivalente) pasa; el CI sigue validando
  algo real del destino (estado `.agent/` o tools del motor via checkout). validate
  del destino 0/0.
- **STOP:** si el checkout del motor en Actions exige secretos/credenciales o el repo
  motor es privado sin token disponible, documentar el blocker y proponer la variante
  validate-state-only en vez de forzar el checkout.
- **Depende de:** WOT-AUDIT-A2b.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-002a - A2c: demo de clone limpio + install --sync sin copias legacy
- **Prioridad:** Media
- **Scope:** system/host-extends
- **Estado:** completed (cca3540; closeout closeout_WOT-2026-002a.md)
- **Resultado:** A2d parcialmente des-riesgado. install --sync (exit 0) y
  discover_skills (exit 0, 28 skills del MOTOR) operan sin las copias motor-provides.
  DEPENDENCIA VIVA detectada para A2d: `run_pytest_safe.py` corre pytest contra
  `tests/` LOCAL; sin `tests/` da exit 4 (0 coleccionados). WOT-2026-002c debe
  definir la estrategia de pytest del destino post-A2d.
- **deliverable_type:** mixed
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-A2c
- **Objetivo:** demostrar, sobre un clone limpio del destino en `tmp_path`, que
  `install_agent_system.py --sync` regenera `motor_destination_link.json`, que las
  skills/prompts/scripts del motor quedan accesibles via el motor externo, y que el
  destino opera SIN necesitar las copias legacy de `scripts/`/`skills/`/`agent_system/`.
- **Files Likely Touched:** `orchestrator_pipeline/reports/` (evidencia del demo);
  ninguna superficie productiva del destino (es validacion).
- **Criterio:** clone limpio + `install --sync` regenera el link (exit 0);
  `discover_skills`/`run_pytest_safe`/`validate` del motor corren contra el clone con
  `AGENT_PROJECT_ROOT`; reporte con exit codes reales; sin tocar el arbol legacy.
- **STOP:** si install --sync requiere las copias legacy para regenerar el link,
  documentarlo: cambia el alcance de A2d (algunas copias serian dependencia del
  instalador, no vestigios).
- **Depende de:** WOT-AUDIT-A2b, WOT-AUDIT-CI.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-002b - ORPHANS: decision promover-vs-archivar de los 10 huerfanos
- **Prioridad:** Media
- **Scope:** system/host-extends
- **Estado:** completed (48754f8; deliverable .agent/docs/orphans_decision_WOT-2026-002b.md)
- **Resultado:** 10/10 decididos. 7 archive-legacy solidos (artifact_graph,
  audit_codebase, rollback_agent_system, state_drift, test_refactor_manager_skill,
  test_ticket_007, .goosehints). 3 RECLASIFICADOS a motor-provides installer-managed
  (pre_compact_hook, microagents/onboarding, glossary): A2d = remove + re-sync desde
  motor, NO archive-a-tumba. Correccion verificada al triage: el motor SI tiene
  .agent/hooks/pre_compact_hook.py (v2).
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-ORPHANS
- **Objetivo:** para cada ruta del bucket `huerfano-needs-decision` del
  `triage_manifest.md` (5 scripts del cluster audit/upgrade, `test_ticket_007`,
  `.agent/hooks/pre_compact_hook.py`, `.agent/microagents/onboarding.md`,
  `.agent/glossary.md`, `.goosehints`), decidir con evidencia: promover al motor,
  conservar como host-specific real, o archivar como legacy muerto.
- **Files Likely Touched:** `.agent/docs/triage_manifest.md` (anexar decision por
  fila) o un doc de decisiones nuevo en `.agent/docs/`.
- **Criterio:** cada uno de los 10 huerfanos tiene una decision con evidencia
  (invocacion viva, dominio real, o ausencia de uso); 0 huerfanos sin resolver;
  validate 0/0.
- **STOP:** si alguno resulta ser dominio real del destino (p.ej. `test_ticket_007`
  como experimento vivo), marcar destino-keep y NO archivar; cambia la conclusion
  "dominio vacio" del manifiesto.
- **Depende de:** WOT-AUDIT-A2b, WOT-AUDIT-CI.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-002c - A2d: eliminar copias motor-provides + ejecutar decisiones
- **Prioridad:** Alta
- **Scope:** system/host-extends
- **Estado:** completed-partial (FASE 1+2 hechas; FASE 3 diferida)
- **Resultado:** FASE 1 (1a2d700) archivo 7 legacy a `_legacy/`. FASE 2 (bf451f2)
  retiro 162 motor-provides (`agent_system/` 113, `skills/` 41, 7 scripts,
  `test_event_bus_hygiene`). `.agent/README.md` conservado (STOP#3: customizado).
  Clone-demo verde (destino opera via motor), CI sin refs a copias, validate 0/0,
  motor pristine, 0 destino-keep tocado. FASE 3 (3 installer-managed) DIFERIDA: el
  re-sync via `install --sync` re-vendoriza el bundle completo (incidente; recovery
  791787b). Los 3 quedan destino-keep -> follow-up MOTOR-FU-001. Pytest -> MOTOR-FU-002.
- **deliverable_type:** code
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-A2d
- **Severidad:** Alta | **Riesgo:** Alto (blast radius ~166 archivos + estado CI).
- **Objetivo:** retirar del destino las copias `motor-provides` (`agent_system/` 113,
  `skills/` ~41, `tests/` 1, `scripts/` 7, `.agent/README.md`) via `git mv` a
  `_legacy/` o borrado, y ejecutar las decisiones de WOT-2026-002b. El destino
  queda con su `.agent/` de estado + integracion + docs de identidad (coherente con
  MANIFEST.workspace).
- **Files Likely Touched:** `scripts/`, `skills/`, `agent_system/`, `tests/`,
  `.agent/README.md`, `_legacy/`, `.gitignore` del destino.
- **Criterio:** 0 copias motor-provides trackeadas; `git ls-files` sin
  `agent_system/`/`skills/`/los 7 scripts comunes; CI verde (gracias a WOT-AUDIT-CI);
  clone limpio sigue operando (WOT-2026-002a); validate 0/0; ningun flujo vivo roto.
- **STOP / barrera obligatoria:** NO eliminar ninguna copia `stale-diverged` sin
  reconciliar antes que la version del motor cubre el uso del destino (diff hasta
  601 lineas en `run_pytest_safe`); NO borrar por basename. Si una copia tiene
  invocacion viva sin equivalente funcional confirmado, parar y escalar.
- **Input de WOT-2026-002a (A2c):** retirar `tests/` deja `run_pytest_safe.py` (que el
  gates-dispatch invoca para tickets `code`/`mixed`) sin coleccion (exit 4). A2d DEBE
  decidir la estrategia: apuntar el pytest del destino a `<MOTOR>/tests`, conservar un
  `tests/` minimo propio del destino, o ensenar al gates-dispatch a manejar 'sin tests
  locales'. El CI ya pivoto a validate-state (WOT-AUDIT-CI), pero el dispatch local no.
- **Input de WOT-2026-002b (ORPHANS):** decisiones de los 10 huerfanos
  (`.agent/docs/orphans_decision_WOT-2026-002b.md`):
  - archive-legacy (mover a `_legacy/`/`_archive/`, no re-proveer): `scripts/artifact_graph.py`,
    `scripts/audit_codebase.py`, `scripts/rollback_agent_system.py`, `scripts/state_drift.py`,
    `scripts/test_refactor_manager_skill.py`, `tests/test_ticket_007_context_recovery.py`,
    `.goosehints`.
  - motor-provides installer-managed (retirar copia del destino + RE-SYNC desde motor,
    NO archivar-a-tumba): `.agent/hooks/pre_compact_hook.py`, `.agent/microagents/onboarding.md`,
    `.agent/glossary.md`. Barreras: para `pre_compact_hook` verificar/actualizar el wiring
    de `.claude/settings.json` (PreCompact) para que resuelva al hook del motor antes de
    retirar; para onboarding/glossary correr `install --sync` tras retirar.
- **Depende de:** WOT-2026-002a, WOT-2026-002b.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-003b - Restaurar guard_paths hook (fail-closed) + des-personalizar settings.json
- **Prioridad:** Alta
- **Scope:** system/security-hooks
- **Estado:** completed (cd0ecfb)
- **deliverable_type:** code | **delivery_authority:** repo_destino
- **Problema:** A2d (WOT-2026-002c) retiro `agent_system/`, donde el hook PreToolUse
  del `.claude/settings.json` del destino resolvia `guard_paths.py`. Sin candidato, el
  hook caia a `sys.exit(0)` -> FAIL-OPEN (escrituras permitidas con falsa proteccion).
  Verificado empiricamente. Ademas el settings.json tracked mezclaba 12 grants
  personales (paperclip.ing, z_scripts, broad).
- **Resultado:** tracked `.claude/settings.json` = solo hooks; hook portable que
  resuelve el `guard_paths.py` del motor via `motor_destination_link.json`, corre con
  `cwd=<destino>` y FALLA CERRADO (exit 2) si no resuelve. Grants utiles (github
  domains) -> `settings.local.json` gitignored; resto dropeado. Checklist verificado
  (block prohibido, allow benigno, cwd hardening, link-ausente/motor-inexistente exit 2).
- **Origen:** session-2026-06-14-post-a2d-hardening.

## WOT-2026-003c - Barrera estructural de hooks Claude en el motor (alias MOTOR-FU-003)
- **Prioridad:** Alta
- **Scope:** motor/security-hooks (repo_motor)
- **Estado:** completed (motor d6d2588 + 3e3b87a; destino 6a2f494)
- **deliverable_type:** mixed | **delivery_authority:** repo_motor
- **Resultado:** (a) `scripts/check_claude_settings_portability.py` (gate): no
  `permissions.allow`; hook de escritura obligatorio (matcher cubre Write+Edit+MultiEdit);
  comando debe ser el bootstrap canonico (check estatico, sin ejecutar shell arbitrario);
  el entrypoint canonico debe fail-closed (verificado dinamicamente). (b) Entrypoint
  versionado `.agent/hooks/claude_guard_entry.py` + `canonical_hook_command()` (fuente
  unica); motor y destino lo usan. (c) 22 tests (12 gate + 10 entrypoint). (d) Wireado en
  pre-commit del motor. Endurecido tras doble audit (shell arbitrario + hook borrable).
  Suite 2618 passed. La integracion en install --sync (paso d original) y el paso de CI
  del destino quedan como follow-up WOT-2026-003f.
- **Politica:** un hook de seguridad nunca debe `exit 0` cuando su guard no resuelve.
- **Depende de:** WOT-2026-003b.
- **Origen:** session-2026-06-14-post-a2d-hardening.

## WOT-2026-003f - CI del destino: paso del gate de portabilidad de settings (follow-up 003c)
- **Prioridad:** Baja
- **Scope:** system/ci-portability
- **Estado:** pending
- **deliverable_type:** code | **delivery_authority:** repo_destino
- **Objetivo:** anadir al workflow del destino un paso que corra
  `check_claude_settings_portability.py` (del motor, via checkout) contra el
  `.claude/settings.json` del destino, para que un fail-open o grants personales se
  detecten en CI, no solo en pre-commit del motor. Nota: el filtro `paths:` del CI debe
  incluir `.claude/**` para que el paso dispare en cambios de settings.
- **Pendiente relacionado de 003c:** integracion del gate/entrypoint en `install --sync`
  (garantizar el link + recovery) si se decide automatizar el provisioning del hook.
- **Depende de:** WOT-2026-003c.
- **Origen:** session-2026-06-14-post-a2d-hardening.

## WOT-2026-003d - install host-extends-aware (retirar bundle sin re-vendorizar) (alias MOTOR-FU-001)
- **Prioridad:** Baja
- **Scope:** motor/installer (repo_motor)
- **Estado:** pending
- **deliverable_type:** code
- **Problema (hallazgo WOT-2026-002c FASE 3):** `install_agent_system.py --sync`
  re-provisiona el bundle COMPLETO en el destino (re-crea `agent_system/` + caches),
  ademas de borrar superficies no-managed en el working tree. No existe un modo que
  RETIRE las copias motor-provides del destino dejandolo como workspace puro.
- **Objetivo:** modo install host-extends que (a) no re-vendorice `agent_system/`/
  `skills/`/scripts cuando el destino opera por referencia externa al motor, y (b)
  re-provisione SOLO los installer-managed declarados (onboarding, glossary) sin
  arrastrar el bundle ni borrar superficies destino-keep.
- **Desbloquea:** FASE 3 de A2d (retirar los 3 installer-managed del destino).
- **Depende de:** WOT-2026-002c.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-003e - gates-dispatch: manejar 'destino sin tests locales' (alias MOTOR-FU-002)
- **Prioridad:** Baja
- **Scope:** motor/quality-gates (repo_motor)
- **Estado:** pending
- **deliverable_type:** code
- **Problema (hallazgo WOT-2026-002a):** tras retirar `tests/`, `run_pytest_safe.py`
  (que `run_gates_dispatch` invoca para tickets `code`/`mixed`) colecciona 0 y da
  exit 4 contra el destino. El CI ya pivoto a validate-state, pero el dispatch local no.
- **Objetivo:** `run_gates_dispatch` detecta 'sin tests locales' y o bien apunta a
  `<motor>/tests`, o salta pytest de forma auditable, en vez de fallar con exit 4.
- **Depende de:** WOT-2026-002c.
- **Origen:** session-2026-06-13-host-extends.

## WOT-2026-002d - LOG-COMPACT: compactar historico A2a en execution_log
- **Prioridad:** Baja
- **Scope:** system/collab-hygiene
- **Estado:** absorbed (premisa obsoleta)
- **Resolucion:** la premisa ("el execution_log arrastra el historico completo de
  A2a") ya no se cumple: el log se reescribio en cada ticket (002a -> 002b) y el
  ciclado natural elimino el historico A2a. Verificado 2026-06-13: execution_log.md =
  89 lineas, 0 menciones de A2a (`grep -c A2a` = 0). El detalle historico vive en git
  (commits de A2a). No requiere accion; trazabilidad preservada.
- **deliverable_type:** documentation
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-LOG-COMPACT
- **Problema:** `execution_log.md` arrastra el historico completo de A2a (sugerencia
  no bloqueante del Manager en review de A2b): dificulta leer el packet activo.
- **Objetivo:** dejar una cabecera corta del ticket activo y mover el historico A2a a
  una nota resumida o a `_archive/`, sin perder trazabilidad (el detalle vive en git).
- **Files Likely Touched:** `.agent/collaboration/execution_log.md`.
- **Criterio:** `execution_log.md` del ticket activo legible sin el historico A2a
  embebido; trazabilidad preservada (referencia a commits); validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-13-host-extends.

---

## WT-2026-250c - Poda documental de backlog y saneo de mojibake en superficies vivas
- **Prioridad:** Media
- **Scope:** system/collab-hygiene
- **Estado:** deferred
- **deliverable_type:** documentation
- **Criterio:** backlog <200 lineas; 0 mojibake en superficies vivas; PYSEC-196 tiene ficha con criterio de salida; validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-251b - Migrar el dogfooding al prefijo WOT como validacion viva
- **Prioridad:** Alta
- **Scope:** system/ticket-prefix-portability
- **Estado:** done
- **deliverable_type:** mixed
- **Objetivo:** correr el proximo ticket bajo prefijo `WOT-`. Actualizar `PROJECT.md` del destino con `Ticket prefix: WOT`.
- **Criterio:** un ticket `WOT-2026-001a` completa el ciclo bus con validate 0/0 y archivado correcto.
- **STOP:** no-match silencioso de `WOT-*` en logs -> reabrir WT-2026-251a.
- **Depende de:** WT-2026-251a, WT-2026-250a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-252a - Decision-artifact estructurado del Manager con fallback a parser NDJSON
- **Prioridad:** Alta
- **Scope:** system/review-decision-contract
- **Estado:** done
- **deliverable_type:** code
- **Objetivo:** el prompt/skill de review instruye al Manager a escribir `.agent/runtime/reviews/decision_<ticket>.json`; el bridge lo lee como canal primario; el parser NDJSON queda como fallback.
- **Files Likely Touched:** `prompts/review_manager.md`, `skills/man-review-implementation/SKILL.md`, `bus/review_bridge.py`, tests (repo_motor).
- **Criterio:** con artifact presente el bridge decide sin leer el transcript (test); `discover_skills.py --check-contract` pasa; ruff + pytest-safe + validate 0/0.
- **STOP:** si el backend no puede garantizar escritura del archivo, degradar a artifact opcional + telemetria.
- **Depende de:** WT-2026-248b.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253a - Reescribir skill code-audit sobre CLIs directas
- **Prioridad:** Media
- **Scope:** system/skills-product
- **Estado:** done
- **deliverable_type:** documentation
- **Problema:** `skills/code-audit/SKILL.md` instruye ejecutar `python scripts/audit_codebase.py`, que no existe. La skill es inejecutable.
- **Objetivo:** reescribir el Workflow a `uv run vulture`, `uv run deadcode`, `ruff check --select C90,ERA,SIM`; corregir version.
- **Files Likely Touched:** `skills/code-audit/SKILL.md` (repo_motor).
- **Criterio:** cada comando del Workflow ejecuta en el motor real; validate 0/0.
- **STOP:** si vulture/deadcode no corren en Windows, anotar la limitacion en la skill.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253b - Des-localizar repo-compare y graphify del entorno del autor
- **Prioridad:** Media
- **Scope:** system/skills-product
- **Estado:** done
- **deliverable_type:** documentation
- **Problema:** `skills/repo-compare/SKILL.md` define el proyecto local como `z_scripts/`; `skills/graphify/SKILL.md` usa bash en runtime Windows.
- **Objetivo:** parametrizar proyecto local en repo-compare; pasos agnosticos de shell en graphify; declarar o reescribir networkx.
- **Criterio:** `rg z_scripts skills/` devuelve 0; pasos de graphify ejecutables en PowerShell 5.1; validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253c - local_audit veraz y AUDIT.md autogenerado en el launcher
- **Prioridad:** Media
- **Scope:** system/bootstrap-observability
- **Estado:** done
- **deliverable_type:** code
- **Problema:** `scripts/local_audit.py:44` busca `- Version:` pero `PROJECT.md:2` usa `**Version:**`, reportando Unknown. El launcher nunca invoca `local_audit.py`.
- **Objetivo:** alinear parsers; invocar `local_audit.py` en el launcher con timeout best-effort.
- **Criterio:** AUDIT.md reporta la version real; tras lanzar sesion existe AUDIT.md fresco; ruff + pytest-safe + validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-254a - Deprecacion formal Goose/Claw fase 1 (docs y tests)
- **Prioridad:** Media
- **Scope:** system/legacy-deprecation
- **Estado:** done
- **deliverable_type:** mixed
- **Objetivo:** fase 1 sin borrar codigo: marcar DEPRECATED en docs, mover `test_goose_*.py` fuera de `scripts/`.
- **Files Likely Touched:** `AGENTS.md`, `README.md`, `QUICKSTART.md`, `.goosehints`, scripts de test (repo_motor).
- **Criterio:** ninguna doc del motor presenta Goose/Claw como via oficial; test_goose ya no viven en `scripts/`; suite verde; validate 0/0.
- **STOP:** si el instalador copia superficies Goose a destinos, documentar antes de mover nada.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-254b - Regenerar .claude/rules del destino desde el estado real
- **Prioridad:** Media
- **Scope:** system/docs-coherence
- **Estado:** done
- **deliverable_type:** documentation
- **Problema:** las reglas del destino son plantilla sin adaptar: rutas erroneas (`src/`, `orquestacion_agentes/`, `z_scripts`, `publica/`), `work_plan.md` en `.session/` (el canonico es `.agent/collaboration/`).
- **Objetivo:** reglas regeneradas desde el estado real del destino y del motor.
- **Criterio:** cada comando en las reglas existe en el destino; 0 referencias a rutas inexistentes; validate 0/0.
- **Depende de:** WT-2026-254a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-255a - Extraer parser de decisiones de review_bridge a modulo propio
- **Prioridad:** Media
- **Scope:** system/seam-extraction
- **Estado:** done
- **deliverable_type:** code
- **Problema:** `bus/review_bridge.py` (3266 lineas) mezcla transporte, parseo y requeue. El parseo tiene mayor churn.
- **Objetivo:** extraer parseo NDJSON + decision-artifact a `bus/review_decision.py`; `review_bridge.py` queda como orquestacion. Sin cambios de comportamiento.
- **Files Likely Touched:** `bus/review_bridge.py`, `bus/review_decision.py` (nuevo), tests (repo_motor).
- **Criterio:** suite review verde; `review_bridge.py` reduce >=600 lineas; ruff + pytest-safe + validate 0/0.
- **STOP:** si la extraccion exige cambiar firmas consumidas por supervisor, replantear el corte.
- **Depende de:** WT-2026-252a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-256a - Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2
- **Prioridad:** Baja
- **Scope:** system/security-dependencies
- **Estado:** blocked-external
- **deliverable_type:** code
- **Problema:** `repo_motor` ignora temporalmente `PYSEC-2026-196` en `[tool.pip-audit].ignore-vuln`. La excepcion no tiene propietario ni caducidad.
- **Objetivo:** cuando `uv lock --upgrade-package pip` fije `pip>=26.1.2`, retirar la excepcion y verificar `python scripts/pip_audit_project.py` sin vulnerabilidades ignoradas.
- **Criterio:** pip-audit pasa sin ignorar PYSEC-2026-196; commit en repo_motor con evidencia de uv lock actualizado; ruff + pytest-safe verdes.
- **STOP:** si `uv` sigue resolviendo `pip<26.1.2`, documentar blocker y retrasar hasta nueva release.
- **Evidencia de origen:** commit `3601312` en repo_motor introdujo el wrapper.
- **Depende de:** -.
- **Origen:** session-2026-06-07-security-followup (reintroducida 2026-06-11).

## Nota de colision de IDs (2026-06-12)

Los tickets de chat de los giros 9-12 se asignaron manualmente como
WT-2026-256a..259a y COLISIONAN con WT-2026-256a (PYSEC-2026-196) de esta
tabla. Los IDs de los commits 8d385df (giro 9), 4970529 (giro 10),
827f96c (giro 11) y 929ca09 (giro 12) se refieren a los giros de
descomposicion, NO al ticket PYSEC. Leccion ya conocida: derivar IDs del
estado real del backlog antes de asignar. El ticket PYSEC conserva el ID
WT-2026-256a en esta tabla.

## Hallazgo 2026-06-12: suite canonica es allowlist parcial

`scripts/run_pytest_safe.py` ejecuta una lista explicita de 28 archivos
(DEFAULT_PYTEST_ARGS), no descubrimiento sobre `tests/`: 119 de 147
archivos de test del motor NO corren en la suite "canonica" (los "642
passed" de los gates son una fraccion). Detectado al observar que un
test nuevo no alteraba el conteo. CEM clase D (gate que no cubre lo que
dice cubrir). Medicion del estado real en curso; candidato a ticket:
migrar DEFAULT a descubrimiento `tests/` tras triage de los excluidos.

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
| Baja | WOT-2026-003d | install/sync: jamas prunear rutas trackeadas del destino (RE-SCOPED) | motor/installer | completed | WOT-2026-002c | session-2026-06-14-post-a2d-hardening |  <!-- RE-SCOPED: premisa re-vendor obsoleta; riesgo real = strict prune borraba .agent/docs trackeado. motor ff05b8d+50beca6. prune_residues guard git-tracked + fail-safe; barrera real (worktree ba52a86 falla sin fix); review independiente APROBADO. alias MOTOR-FU-001 -->
| Baja | WOT-2026-006b | Encoding guard: explicit-path checking + UTF-8 BOM detection | motor/quality-gates | completed | - | session-2026-06-14-post-pipeline-external-audit |  <!-- motor 3df6620 (commiteado bajo 003d; trazabilidad post-review). check_encoding_guard.py ahora chequea rutas explicitas (antes ignoraba argv y solo miraba staged) + has_utf8_bom; 2 tests nuevos -->
| Baja | WOT-2026-003e | gates-dispatch: manejar 'destino sin tests locales' (run_pytest_safe exit 4) | motor/quality-gates | completed | WOT-2026-002c | session-2026-06-14-post-a2d-hardening |  <!-- verificado: motor 50bdf07. has_local_tests() + skip auditable en run_code_gates; 5 tests barrera; suite 2631 passed -->
| Baja | WOT-2026-003f | CI del destino: paso que corre el gate de portabilidad contra su .claude/settings.json | system/ci-portability | completed | WOT-2026-003c | session-2026-06-14-post-a2d-hardening |  <!-- verificado: destino dd8c79d. quality-gates.yml corre check_claude_settings_portability.py contra .claude/settings.json + .claude/** en paths; gate local exit 0; motor intacto -->
| Alta | WOT-2026-004a | Suprimir 2 falsos positivos de gitleaks en CI del destino (scan full-history) | system/ci-portability | completed | - | session-2026-06-14-session-close |  <!-- 3e23873; .gitleaks.toml useDefault+allowlist tight; placeholder didactico (sk_live_1234567890) + SHA git publico (9c92e3d4, repo-compare WT-2026-236a); gitleaks 8.30.1 local 101 commits 0 leaks exit 0 -->
| Baja | WOT-2026-004b | Motor: seed .gitleaks.toml en bundle + politica generic-api-key-on-SHA en logs operativos + fix guard \.git over-match | motor/security-hooks | completed | WOT-2026-004a | session-2026-06-14-session-close |  <!-- verificado: motor 9c7c91d. guard .git anclado a segmento (^|/)\.git(/|$); seed agent_system/templates/gitleaks.config.toml paths-only; copy_gitleaks_config no-clobber; 7 tests barrera; suite 2626 passed -->
| Media | WOT-2026-005a | Separacion memoria privada vs portable en memory_upload | motor/protocol-docs | completed | WOT-2026-003b, WOT-2026-003c | session-2026-06-14-host-extends-learnings |  <!-- verificado: motor 260c0c4. memory_upload.md seccion decision de destino (privada/portable motor/portable destino) + regla drift schema; encoding 0 -->
| Alta | WOT-2026-005b | Bootstrap/preflight destino: checks host-extends, settings y guard fail-closed | motor/protocol-docs | completed | WOT-2026-003c | session-2026-06-14-host-extends-learnings |  <!-- verificado: motor 9c1ba3d. bootstrap+preflight+SKILL body con checks topologia/settings/guard/resolvers; frontmatter intacto; skill_collisions 0; discover OK -->
| Media | WOT-2026-005c | Audit post-change: resolver integrity, hooks, CI e install-sync risk | motor/protocol-docs | completed | WOT-2026-005b | session-2026-06-14-host-extends-learnings |  <!-- verificado: motor c783e40. audit_post_change Fase4/Fase5 + SKILL body: Resolver integrity, hook behavior test, settings/CI/install-sync; frontmatter intacto -->
| Media | WOT-2026-005d | Audit completo motor-destino: patrones estrategicos host-extends y memoria | motor/protocol-docs | completed | WOT-2026-005c | session-2026-06-14-host-extends-learnings |  <!-- verificado: motor f53dd1a. audit_complete: resolvers/bootstraps, fail-open ampliado, bus ausente-vs-violado, memoria por capas; fuentes host-extends; referencia 005a/b/c -->
| Alta | WOT-2026-006a | Correccion post-audit: quitar false-greens de pytest + barrera return-not-none + politica de cierre FALLBACK | motor/quality-gates | completed | - | session-2026-06-14-post-pipeline-external-audit |  <!-- CORRECCION POST-AUDIT (no parte del pipeline original). motor df7dd6f (test) + ba52a86 (docs). refactor_kit path (hyphen->underscore, 5 false-greens), trigger ==38 (real 87, false-green), ruff-warnings-pass; pytest.ini filterwarnings=error::PytestReturnNotNoneWarning; politica FALLBACK close. Auditoria externa independiente -->
| Alta | WOT-2026-007a | Contract Formation Pipeline v0: contrato minimo documental | motor/protocol-docs | completed | - | session-2026-06-14-contract-formation |  <!-- motor 7bf57f8; contrato documental v0 provisional aprobado por Manager; .agent/planning/ declarado destino-keep; 007b ratifica/corrige con vertical minima -->
| Alta | WOT-2026-007b | Validacion vertical: idea -> contrato -> backlog -> Builder sin aclaraciones | motor/protocol-validation | completed | WOT-2026-007a | session-2026-06-14-contract-formation |  <!-- motor bb60532; clarification_rate=0; prueba destructiva bloqueada; 007a ratificado -->
| Media | WOT-2026-007c | Validador de contratos de ticket y planning docs | motor/quality-gates | completed | WOT-2026-007a, WOT-2026-007b | session-2026-06-14-contract-formation |  <!-- motor b29a8da+5dafbc7; validador+36 tests; suite 2676 passed; revision independiente Manager (CHANGES->B1+B2 fixed); aprobado humano; cierre canonico via reconcile_ticket+BUILDER_EXIT; validate 0/0 -->
| Media | WOT-2026-007d | Skills/prompts de auditoria de idea, plan y ticket | motor/protocol-docs | completed | WOT-2026-007a | session-2026-06-14-contract-formation |  <!-- motor 11e7ad8; 3 prompts audit_cf_* (charter/plan_graph/ticket) + routing en pipeline/README; rutan audit_agent_output 2.b/2.c sin duplicar; encoding 0 -->
| Baja | WOT-2026-008a | Manifiesto de taxonomia y migracion de prompts/skills | system/docs-coherence | in_progress | WOT-2026-007d | session-2026-06-15-contract-formation |  <!-- analysis en repo_destino; contrato enmendado tras CHANGES: inventario ampliado a templates/references/_shared/llms/tools + DEC-008-004 manifest-first; cero moves/edits en repo_motor -->
| Alta | WOT-2026-008b | Discovery/frontmatter hardening: BOM y registry decision | motor/skills-discovery | pending | WOT-2026-008a, WOT-2026-009b | session-2026-06-15-taxonomy |
| Media | WOT-2026-008c | Registry/INDEX generado de prompts y skills | motor/skills-discovery | pending | WOT-2026-008b | session-2026-06-15-taxonomy |
| Media | WOT-2026-008d | Migracion de naming audit/version con shims | motor/skills-taxonomy | pending | WOT-2026-008c | session-2026-06-15-taxonomy |
| Baja | WOT-2026-008e | Retirada versionada de shims y compat legacy | motor/skills-taxonomy | pending | WOT-2026-008d | session-2026-06-15-taxonomy |
| Alta | WOT-2026-009a | Pre-Builder contract gate deliverable-aware y fail-closed | motor/protocol-runtime | pending | WOT-2026-008a | session-2026-06-15-contract-formation |  <!-- follow-up: ningun Builder arranca con contrato que no valide en modo handoff; override debe ser evento auditable, no nota markdown -->
| Alta | WOT-2026-009b | Scope gate topology-aware por delivery_authority y FLT namespaced | motor/protocol-runtime | pending | WOT-2026-009a | session-2026-06-15-contract-formation |
| Media | WOT-2026-009c | Guardias reciprocas de aislamiento repo_motor/repo_destino | motor/protocol-runtime | pending | WOT-2026-009b | session-2026-06-15-contract-formation |
| Media | WOT-2026-007e | Plan graph avanzado: paralelismo, shared dependencies y anti-scope | motor/protocol-validation | completed | WOT-2026-007a, WOT-2026-007b | session-2026-06-14-contract-formation |  <!-- motor 1dc5447; plantilla plan_graph dedicada + paralelizable yes/no/after + Merge Regression Audit; checks estructurales ya en validador 007c; enforcement de valores = follow-up tras cierre 007c -->
| Baja | WOT-2026-007g | Validador plan_graph: enforce paralelizable in {yes,no,after} + presencia Merge Regression Audit | motor/quality-gates | completed | WOT-2026-007c, WOT-2026-007e | session-2026-06-15-contract-formation |  <!-- motor ce83621; destino 03efad4+ae5bb67+closeout; validate_plan_graph localiza Paralelizable por header, acepta parallelism_notes separado, exige Merge Regression Audit; cierre canonico manager-approve 0/0 -->
| Baja | WOT-2026-007f | Integracion runtime de CONTRACT_GAP en bus/controller | motor/protocol-runtime | completed | WOT-2026-007c, WOT-2026-007e, WOT-2026-007g | session-2026-06-14-contract-formation |  <!-- motor f5923d7+c5d81ee+5fab636+ece7524; suite independiente 2713 passed; Manager APROBADO; cierre canonico manager-approve; validate 0/0 -->

## Plan WOT-2026-007 - Contract Formation Pipeline v0

> Objetivo de familia: crear la etapa previa al pipeline de implantacion que convierte
> una idea de repo en contratos ejecutables por agentes: `repo_charter -> plan_graph ->
> ticket_contracts -> backlog`. Esta etapa NO busca maxima autonomia: busca comprension,
> decisiones humanas explicitas y tickets congelados con suficiente calidad para que el
> Builder barato pueda implantar sin preguntar.
>
> Principio de producto: el usuario decide, no escribe codigo ni edita contratos tecnicos.
> El sistema debe presentarle decisiones `DEC-*` con recomendacion, impacto, reversibilidad
> y evidencia; el Manager convierte esas decisiones en contrato operativo.
>
> Orden recomendado para pipeline: 007a -> 007b. Despues 007c/007d/007e pueden avanzar
> segun prioridad. 007f queda diferido hasta que el contrato documental y el validador
> esten probados. No construir una catedral: cada ticket debe preservar una vertical
> minima verificable.
>
> Nomenclatura: los tickets reales siguen siendo `WOT-2026-NNNx` en este repo destino
> dogfooding y `WP-2026-NNNx` en el motor. Los IDs internos (`OBJ-001`, `PLAN-001`,
> `DEC-001`, `EVID-001`, `ACCEPT-001`, `CG-<TICKET_ID>`) son trazabilidad interna del
> contrato; no sustituyen al ticket real.
>
> Control adversarial nuevo: la familia 007 debe cubrir tres riesgos sistemicos antes
> de automatizar: (1) ilusion de planificacion -> `Impact Simulation`; (2) drift de
> verdad operativa -> `context_baseline` y recheck de contratos pendientes; (3) auditoria
> superficial -> `Intent Audit` contra el charter, arquitectura, no-objetivos y restricciones.

### WOT-2026-007a - Contract Formation Pipeline v0: contrato minimo documental
- **Prioridad:** Alta
- **Scope:** motor/protocol-docs
- **Estado:** pending
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Problema:** hoy existe un pipeline fuerte de implantacion/revision, pero la fase
  previa de investigacion, decisiones, descomposicion en planes y tickets congelados
  vive en chat y memoria. Eso produce tickets con premisas obsoletas, dependencias
  implicitas, criterios de cierre ambiguos o superficies no declaradas.
- **Objetivo:** crear el contrato portable minimo del `Contract Formation Pipeline` sin
  automatizar aun el runtime. Debe ser suficiente para que un Manager redacte tickets
  con calidad y para que otro agente audite el contrato antes de pasar a Builder.
- **Files Likely Touched:**
  - Builder: `prompts/contract_formation_pipeline.md` (nuevo).
  - Builder: `docs/contract_formation/README.md` (nuevo) o ruta equivalente si el motor
    ya tiene una carpeta documental mas apropiada.
  - Builder: `docs/contract_formation/templates/repo_charter.md` (nuevo).
  - Builder: `docs/contract_formation/templates/ticket_contract.md` (nuevo).
  - Builder: `docs/contract_formation/templates/evidence_catalog.md` (nuevo).
  - Builder: `docs/contract_formation/templates/contract_gap.md` (nuevo).
  - Builder: `MANIFEST.workspace` para decidir y, si procede, declarar
    `.agent/planning/` como superficie destino-keep antes de que 007b la materialice
    en un destino.
  - Read/inspect only: `prompts/orchestrator_pipeline.md`, `prompts/audit_plan.md`,
    `prompts/audit_agent_output.md`, `prompts/launch_builder.md`,
    `prompts/review_manager.md`, `prompts/destination_bootstrap.md`,
    `AGENTS.md`, `MANIFEST.workspace`.
- **Contrato minimo que debe documentar:**
  - Artefactos destino: `.agent/planning/repo_charter.md`, `.agent/planning/plan_graph.md`,
    `.agent/planning/ticket_contracts.md`, `.agent/planning/evidence_catalog.md`,
    `.agent/planning/decisions.md`, `.agent/planning/contract_gaps/CG-<TICKET_ID>.md`.
  - `INDEX.md` no es fuente manual de verdad: o queda fuera de v0 o se define como
    proyeccion generada/validada. No introducir un router manual que pueda mentir.
  - `DEC-*` con tiers: `T1a` humano obligatorio, maximo 3 por ronda; `T1b/T1c` humano
    recomendado segun coste; `T2` decision por defecto del agente con override humano.
  - Cada `DEC-*` declara: opciones, recomendacion del Manager, evidencia `EVID-*`,
    impacto, reversibilidad, `invalidates`, `supersedes`, `decided_by`, fecha y estado.
  - `evidence_catalog.md` declara fuente, tipo (`user_doc`, `github`, `web`,
    `official_doc`, `inferred`), fiabilidad, fecha, claims, corroboracion, decisiones
    afectadas y riesgo de prompt-injection. Evidencia externa/inferida de fiabilidad
    media/baja no puede sostener una decision `T1a` sin corroboracion.
  - `repo_charter.md` declara objetivos `OBJ-*`, no-objetivos, restricciones, criterios
    de exito, riesgos y decisiones pendientes. Debe incluir las secciones minimas
    `Product Intent`, `Architecture Constraints`, `Non-Goals`, `Quality Bar` y
    `Security Constraints`; no crear `VISION.md`/`ARCHITECTURE.md` obligatorios en v0.
  - Cada `OBJ-*` debe declarar `failure_modes`: condiciones concretas que harian
    fallar el objetivo aunque un ticket local pareciera cumplido.
  - `plan_graph.md` declara `PLAN-*`, dependencias, superficies de archivo, interfaces,
    `shared_dependencies` y reglas de paralelismo. La independencia entre planes se
    verifica, no se declara por buena fe.
  - `Impact Simulation`: antes de emitir tickets, el Manager/Auditor simula el plan
    contra la arquitectura actual y enumera colisiones de estado, archivos/configs
    compartidos, interfaces inestables, supuestos de entorno y tickets que deben
    serializarse. La salida debe ser una seccion auditable del `plan_graph`, no relato.
  - Cada `ticket_contract` declara: ticket real, `Objective-Link`, `Plan-Link`, premisa,
    `status` (`draft`, `review`, `frozen`, `invalidated`), `Premise Re-check` read-only,
    `Files Likely Touched`, `Forbidden Surfaces`, DoD, STOP conditions, integracion
    cross-ticket, `CONTRACT_GAP behavior` y presupuesto de aclaraciones esperado
    (`Builder clarification rate = 0`). Solo contratos `frozen` pueden convertirse en
    `work_plan.md`; `CONTRACT_GAP` es la via canonica para invalidar/descongelar.
  - `CONTRACT_GAP` conceptual: si el Builder detecta premisa falsa, ambiguedad, necesidad
    de tocar superficie prohibida, criterio de aceptacion incompleto o conflicto de
    dependencias, no improvisa; escribe `CG-<TICKET_ID>.md`, bloquea el ticket y devuelve
    el caso a Contract Formation.
  - `ACCEPT_WITH_FOLLOWUPS` solo es valido si materializa followups como tickets reales
    o contratos minimos, con criterio de salida.
  - Mapeo explicito hacia ejecucion: como convertir `ticket_contract` en
    `.agent/collaboration/work_plan.md`, `PLAN_<ticket>.md` y fila de `backlog.md`.
  - Anti-scope: cada ticket declara superficies prohibidas derivadas del plan y de sus
    dependencias para que scope-gate pueda proteger paralelismo.
- **Criterios binarios:**
  - Existe `prompts/contract_formation_pipeline.md` y contiene fases, roles,
    artefactos, STOP conditions y handoff a `orchestrator_pipeline.md`.
  - Existen las plantillas documentales declaradas o una ruta documental equivalente
    justificada en el diff.
  - El prompt declara explicitamente que `WOT-2026-007b` es validacion obligatoria y que
    007a queda como contrato v0 provisional: no prueba autonomia real hasta que 007b lo
    ratifique o lo corrija con una vertical minima.
  - El contrato separa decisiones humanas de trabajo tecnico del agente; no pide al
    usuario editar archivos.
  - El contrato separa evidencia de internet/GitHub/docs de capacidades ejecutables:
    research es read-only y no concede permisos.
  - El contrato define `Impact Simulation`, `context_baseline`, `Pending-contract recheck`
    e `Intent Audit` como obligaciones documentales de v0, no como runtime automatico.
  - El contrato incluye checklist negativa, `failure_modes` por objetivo, baseline
    evidence y politica de warnings tratados/reconciliados antes de ejecutar genesis.
  - `Negative Audit Checklist`: el charter debe listar antipatrones verificables que
    invalidan la aceptacion (por ejemplo: aumentar acoplamiento motor-destino, exigir
    que el usuario edite codigo/Markdown tecnico, degradar seguridad/trazabilidad,
    o introducir complejidad sin reducir riesgo).
  - `Context Baseline Evidence`: cada ticket derivado debe capturar evidencia minima
    de arranque: `git_head`, `git_status`, `validate_result`, `local_audit_result`
    si existe comando disponible, artefactos relevantes y `generated_at`. Si un flag
    `--out` no existe, no inventarlo: capturar salida real o abrir follow-up code.
  - Un pipeline de genesis no arranca con warnings de `validate` sin tratar: primero
    corrige las reparables con herramienta canonica (por ejemplo `bus_drift` via
    `scripts/reconcile_ticket.py`); solo warnings no reparables pueden quedar como
    `fixed_before_start`, `accepted_health_exception` o `blocking`, con evidencia y
    propietario.
  - `MANIFEST.workspace` queda coherente: 007a decide explicitamente si `.agent/planning/`
    sera superficie destino-keep. Si 007b va a materializar `.agent/planning/` en el
    destino, 007a debe anadirlo a `MANIFEST.workspace` o bloquear 007b hasta decidirlo.
  - `python scripts/check_encoding_guard.py <archivos_md_tocados>` exit 0.
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
    exit 0, 0 errors.
- **STOP:**
  - Si el Builder necesita crear codigo runtime, CLI, bus events o validador ejecutable,
    detener y abrir 007c/007f; 007a es documental.
  - Si aparece conflicto entre prompt nuevo y `orchestrator_pipeline.md`, no duplicar
    reglas: documentar el handoff y referenciar la fuente canonica.
  - Si se propone `INDEX.md` manual como fuente de verdad, rechazar o convertirlo en
    proyeccion generada/validada.
  - Si alguna decision humana exige editar Markdown directamente, redisenar como `DEC-*`.
- **Depende de:** -.
- **Origen:** session-2026-06-14-contract-formation.

### WOT-2026-007b - Validacion vertical: idea -> contrato -> backlog -> Builder sin aclaraciones
- **Prioridad:** Alta
- **Scope:** motor/protocol-validation
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Problema:** un contrato bonito no demuestra que el Builder pueda operar con
  autonomia. Hay que falsar la hipotesis con una rebanada vertical pequena antes de
  construir mas automatizacion.
- **Objetivo:** probar el Contract Formation Pipeline v0 sobre un arquetipo minimo
  (preferente: servicio Python pequeno), generando `OBJ-001 -> PLAN-001 -> ticket_contract
  -> backlog/work_plan -> Builder`, y medir si el Builder necesita aclaraciones.
- **Files Likely Touched:**
  - Builder: `docs/contract_formation/examples/python_service_minimal/` o ruta equivalente
    de ejemplo.
  - Builder: `prompts/contract_formation_pipeline.md` solo para ajustes derivados de la
    validacion.
  - Builder: tests o scripts solo si el plan re-clasifica el ticket como code/mixed con
    alcance claro.
  - Read/inspect only: artefactos de 007a, `prompts/orchestrator_pipeline.md`,
    `prompts/launch_builder.md`, `prompts/review_manager.md`.
- **Criterios binarios:**
  - Existe un ejemplo completo con `repo_charter`, `evidence_catalog`, `decisions`,
    `plan_graph` y al menos un `ticket_contract`.
  - El ejemplo incluye una `Impact Simulation` que detecta al menos una colision o
    dependencia compartida plausible y decide serializar/paralelizar con evidencia.
  - El ejemplo ejecuta una prueba de destructividad controlada: intentar violar una
    restriccion o non-goal del charter y demostrar que el contrato/auditoria lo detecta
    antes de Builder.
  - El `ticket_contract` resultante tiene `status: frozen` y puede convertirse en una
    fila de backlog y un `work_plan.md` sin campos inventados; si necesita cambiar,
    se emite `CONTRACT_GAP` en vez de mutar el contrato en silencio.
  - El Builder clarification rate queda medido: numero de preguntas necesarias antes de
    implementar. Objetivo: `0`; si no es 0, se documenta `CONTRACT_GAP` y se corrige el
    contrato antes de cerrar.
  - Se demuestra un `Premise Re-check` read-only sobre el ejemplo.
  - Se demuestra un `context_baseline` inicial y un recheck de contratos pendientes tras
    un cambio simulado de un ticket previo.
  - Se demuestra un `Intent Audit`: el review rechaza o marca riesgo si un cambio cumple
    el ticket pero contradice `Non-Goals`, `Quality Bar` o `Security Constraints`.
  - Se demuestra que `Forbidden Surfaces` habria bloqueado un scope creep plausible.
  - Se ejecutan gates aplicables: encoding para Markdown; validate del destino 0/0;
    cualquier test nuevo debe fallar sin la mejora que pretende proteger.
- **STOP:**
  - Si la validacion exige que el usuario escriba codigo o edite contratos, volver a 007a.
  - Si el Builder necesita preguntar por intencion de producto que deberia estar en
    `repo_charter`, marcar fallo de contrato, no fallo del Builder.
  - Si el ejemplo se vuelve multi-plan complejo, recortarlo: esta ticket prueba una
    vertical minima, no el sistema completo.
- **Depende de:** WOT-2026-007a.
- **Origen:** session-2026-06-14-contract-formation.

### WOT-2026-007c - Validador de contratos de ticket y planning docs
- **Prioridad:** Media
- **Scope:** motor/quality-gates
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Problema:** si el contrato se queda solo en Markdown, futuros Managers pueden omitir
  campos criticos y el Builder barato volvera a operar con huecos semanticos.
- **Objetivo:** implementar un validador stdlib-only que revise `repo_charter`,
  `plan_graph`, `ticket_contracts` y `CONTRACT_GAP` contra el contrato definido en 007a.
- **Files Likely Touched:** `scripts/validate_contract_formation.py` (o nombre equivalente),
  tests, documentacion de uso en `prompts/contract_formation_pipeline.md`.
- **Criterios binarios:**
  - Falla si falta `status`, `Premise Re-check`, `Objective-Link`, `Forbidden Surfaces`,
    DoD, STOP, `CONTRACT_GAP behavior` o evidencia para decisiones `T1a`.
  - Falla si faltan `failure_modes`, `Negative Audit Checklist`, baseline evidence
    o clasificacion de warnings de `validate` cuando existan.
  - Falla si una decision `T1a` se apoya solo en evidencia externa/inferida no corroborada.
  - Falla si un ticket documental declara criterios de exito que dependen de ejecutar
    Builder/codigo/tests sin marcar `mixed` o abrir ticket separado.
  - Incluye fixtures positivos y negativos basados en el ejemplo de 007b; al menos un
    fixture negativo debe demostrar fallo por contrato malformado (por ejemplo sin
    `status: frozen`, sin `failure_modes`, sin baseline evidence o sin checklist
    negativa), y el fixture valido debe pasar.
  - Gate self-service: el error indica archivo, campo, razon y como revalidar.
- **STOP:** si validar Markdown requiere parser fragil o dependencias nuevas, limitar v1 a
  estructura simple y abrir follow-up; no introducir dependencia sin aprobacion.
- **Depende de:** WOT-2026-007a, WOT-2026-007b.
- **Origen:** session-2026-06-14-contract-formation.

### WOT-2026-007d - Skills/prompts de auditoria de idea, plan y ticket
- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** pending
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Problema:** las auditorias actuales cubren plan, implementacion, bus, pipeline y salud
  del sistema, pero no separan todavia auditoria adversarial de idea/charter, plan_graph
  y ticket_contract antes de ejecutar Builder.
- **Objetivo:** definir prompts/skills finos para revisar: idea general de repo,
  plan_graph, ticket_contract y decision queue, heredando la filosofia de
  `audit_agent_output.md` y `audit_plan.md`.
- **Files Likely Touched:** prompts nuevos `audit_repo_charter.md`, `audit_plan_graph.md`,
  `audit_ticket_contract.md` (nombres finales a decidir), skills wrapper si procede,
  `AGENTS.md`/`QUICKSTART.md` solo si se documenta trigger nuevo.
- **Criterios binarios:**
  - Cada prompt declara modo read-only, entradas obligatorias, hallazgos por severidad,
    STOP conditions y salida apta para bucle de mejora.
  - No colisiona con triggers existentes: `discover_skills.py --json` y
    `check_skill_collisions.py` pasan si se crean skills.
  - Los prompts no duplican `audit_agent_output.md`; lo referencian como marco general y
    anaden criterios especificos de genesis/contrato.
  - `Intent Audit` e `Impact Simulation` tienen fuente canonica en
    `prompts/audit_agent_output.md` secciones 2.b y 2.c; 007d solo las enruta y
    especializa para charter/plan/ticket, sin redefinirlas en paralelo.
- **STOP:** si el trigger/nombre no es claro para usuario no tecnico, ajustar antes de
  crear skill. El usuario ve decisiones y revisiones, no rutas internas.
- **Depende de:** WOT-2026-007a.
- **Origen:** session-2026-06-14-contract-formation.

### WOT-2026-007e - Plan graph avanzado: paralelismo, shared dependencies y anti-scope
- **Prioridad:** Media
- **Scope:** motor/protocol-validation
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Problema:** ejecutar planes en paralelo es el claim mas fragil. Las superficies de
  archivo pueden parecer disjuntas mientras comparten base de datos, API, config global,
  schema o installer.
- **Objetivo:** endurecer `plan_graph` con dependencias compartidas, reglas mecanicas de
  paralelismo y anti-scope por ticket.
- **Files Likely Touched:** contrato/plantillas de 007a, ejemplos de 007b, posible script
  o test si se implementa una comprobacion parcial.
- **Criterios binarios:**
  - `plan_graph` declara `shared_dependencies` ademas de archivos/interfaz.
  - `Impact Simulation` queda formalizada como tabla obligatoria: plan, superficies,
    shared deps, conflicto esperado, mitigacion, paralelizable (`yes/no/after`).
  - Hay regla explicita: solo paralelizar planes con superficies e interfaces disjuntas
    o dependencias compartidas estabilizadas por contrato.
  - Cada ticket derivado recibe `Forbidden Surfaces` calculables desde el plan.
  - El merge entre planes exige auditoria transversal de regresion.
- **STOP:** si el chequeo automatico no puede probar independencia, debe degradar a
  `requires_serialization`, no asumir paralelo por defecto.
- **Depende de:** WOT-2026-007a, WOT-2026-007b.
- **Origen:** session-2026-06-14-contract-formation.

### WOT-2026-007f - Integracion runtime de CONTRACT_GAP en bus/controller
- **Prioridad:** Baja
- **Scope:** motor/protocol-runtime
- **Estado:** completed
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Cierre:** motor f5923d7+c5d81ee+5fab636+ece7524; 2713 tests; review independiente APROBADO; validate 0/0.
- **Problema:** en 007a `CONTRACT_GAP` queda como contrato documental; para automatizarlo
  de verdad el bus/controller debe poder representar que un ticket no fallo por codigo,
  sino porque el contrato estaba incompleto u obsoleto.
- **Objetivo:** integrar `CONTRACT_GAP` como estado/evento operativo, con proyeccion en
  `STATE.md`/`TURN.md` y handoff de vuelta al Manager/Contract Formation.
- **Files Likely Touched:** `.agent/agent_controller.py`, bus/supervisor o modulos de
  eventos si aplica, tests de estado, prompts/skills afectados.
- **Criterios binarios:**
  - Builder puede emitir un gap estructurado sin cerrar falsamente el ticket.
  - Al cerrar un ticket, el sistema puede representar un recheck que marca tickets
    pendientes como CONTRACT_INVALID o NEEDS_REBASE cuando cambia su baseline.
  - Manager ve el gap en `TURN.md` con accion concreta.
  - `--validate` acepta el nuevo estado cuando el evento esta presente y falla ante
    proyeccion incoherente.
  - Tests cubren al menos `premise_false`, `forbidden_surface_needed` y
    `missing_acceptance`.
- **STOP:** no tocar runtime antes de que 007a/007b/007c estabilicen el contrato. Si el
  contrato cambia durante este ticket, volver a 007c.
- **Depende de:** WOT-2026-007c.
- **Origen:** session-2026-06-14-contract-formation.

## Plan WOT-2026-005 - Protocolizar aprendizajes host-extends en prompts y skills

> Objetivo de familia: convertir los fallos reales del ciclo host-extends
> (resolvers rotos tras retirar copias motor-provides, hooks fail-open, CI sin bus,
> install --sync re-vendorizando, y ambiguedad de memorias) en preflights y checks
> explicitos dentro de prompts/skills. No implementar gates nuevos ni cambiar logica
> runtime en esta familia; si aparece necesidad de codigo, abrir follow-up separado.
>
> Orden recomendado para pipeline: 005a y 005b pueden correr en paralelo; despues
> 005c -> 005d. Los tickets son documentales pero afectan autonomia operativa:
> deben dejar instrucciones binarias para Manager/Builder, no relato historico de
> la sesion.

### WOT-2026-005a - Separacion memoria privada vs portable en memory_upload
- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** completed (motor 260c0c4)
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Resultado:** `prompts/memory_upload.md` ahora obliga a decidir destino de memoria
  antes de escribir (`Claude privada`, `portable motor`, `portable destino`, `varias`),
  exige evidencia/condicion de promocion, y documenta el drift de schema como STOP.
  La premisa de mojibake quedo descartada con evidencia explicita; no se tocaron
  acentos legitimos sin prueba.
- **Problema:** `prompts/memory_upload.md` no separaba con suficiente fuerza memoria
  Claude privada, memoria portable del motor y memoria portable del destino.
- **Objetivo:** anadir al prompt una decision explicita antes de guardar y criterio de
  promocion a `observations.jsonl`.
- **Files Likely Touched:** `prompts/memory_upload.md`.
- **Criterios binarios:** cumplidos y verificados en cierre.
- **STOP:** si aparece cambio de schema o codigo de memoria, abrir ticket code
  separado.
- **Depende de:** WOT-2026-003b, WOT-2026-003c.
- **Origen:** session-2026-06-14-host-extends-learnings.

### WOT-2026-005b - Bootstrap/preflight destino: checks host-extends, settings y guard fail-closed
- **Prioridad:** Alta
- **Scope:** motor/protocol-docs
- **Estado:** completed (motor 9c1ba3d)
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Resultado:** `destination_bootstrap`, el preflight de pipeline y la `SKILL` de
  `orchestrate-pipeline` ahora fuerzan checks de topologia, settings, guard fail-closed
  y resolvers vivos antes de lanzar Builder. El contrato documental ya no permite
  arrancar ciego en topologia host-extends.
- **Problema:** el bootstrap y el preflight no obligaban a verificar resolvers vivos ni
  hooks fail-closed antes de operar sobre destinos host-extends.
- **Objetivo:** endurecer el arranque documental para Manager/Builder.
- **Files Likely Touched:** `prompts/destination_bootstrap.md`,
  `skills/orchestrate-pipeline/SKILL.md`,
  `skills/orchestrate-pipeline/references/destination-preflight.md`.
- **Criterios binarios:** cumplidos; `check_skill_collisions.py` y `discover_skills.py`
  verificados en cierre.
- **STOP:** si un check exige gate nuevo o shell arbitrario, sigue siendo follow-up code.
- **Depende de:** WOT-2026-003c.
- **Origen:** session-2026-06-14-host-extends-learnings.

### WOT-2026-005c - Audit post-change: resolver integrity, hooks, CI e install-sync risk
- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** completed (motor c783e40)
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Resultado:** el prompt `audit_post_change_system_health` y la skill asociada ahora
  exigen `Resolver integrity`, pruebas de comportamiento del hook, chequeo de settings,
  CI y riesgo de `install --sync` cuando el cambio toca host-extends o limpieza de copias.
- **Problema:** los fallos recientes vivian en memoria pero no en el checklist de la
  auditoria post-cambio.
- **Objetivo:** pasar esos aprendizajes a contrato reusable de auditoria.
- **Files Likely Touched:** `prompts/audit_post_change_system_health.md`,
  `skills/system-health-audit/SKILL.md`.
- **Criterios binarios:** cumplidos; `check_skill_collisions.py` y `discover_skills.py`
  verificados en cierre.
- **STOP:** un fail-open real sigue escalando a ticket code/security.
- **Depende de:** WOT-2026-005b.
- **Origen:** session-2026-06-14-host-extends-learnings.

### WOT-2026-005d - Audit completo motor-destino: patrones estrategicos host-extends y memoria
- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** completed (motor f53dd1a)
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Resultado:** el audit completo ya evalua integracion motor-destino con foco en
  resolvers/bootstraps, fail-open, distincion `no verificable` vs `violado` cuando falta
  el bus runtime, y separacion de capas de memoria. Quedo portable para cualquier
  destino, no solo este dogfooding.
- **Problema:** el audit completo no elevaba aun los incidentes 002/003 a patrones
  estrategicos reutilizables.
- **Objetivo:** actualizar el prompt de auditoria completa con foco host-extends.
- **Files Likely Touched:** `prompts/audit_complete_motor_destination.md`.
- **Criterios binarios:** cumplidos y verificados en cierre.
- **STOP:** la regla de no duplicar checklists se mantiene; referencias canonicas en 005b/005c.
- **Depende de:** WOT-2026-005c.
- **Origen:** session-2026-06-14-host-extends-learnings.


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
- **Estado:** completed (destino dd8c79d)
- **deliverable_type:** code | **delivery_authority:** repo_destino
- **Resultado:** el workflow del destino ahora corre `check_claude_settings_portability.py`
  contra su `.claude/settings.json` y dispara tambien por `.claude/**`, de modo que un
  fail-open o grants personales quedan atrapados en CI y no solo en pre-commit del motor.
- **Objetivo:** anadir el paso CI del gate de portabilidad de settings.
- **Pendiente relacionado de 003c:** la automatizacion de provisioning via `install --sync`
  queda fuera de este ticket y se sigue tratando por separado.
- **Depende de:** WOT-2026-003c.
- **Origen:** session-2026-06-14-post-a2d-hardening.

## WOT-2026-003d - install/sync: jamas prunear rutas trackeadas del destino (RE-SCOPED) (alias MOTOR-FU-001)
- **Prioridad:** Baja
- **Scope:** motor/installer (repo_motor)
- **Estado:** completed (motor ff05b8d + 50beca6)
- **deliverable_type:** code
- **Resultado:** el ticket se re-scopo con evidencia dura: la premisa "re-vendoriza el
  bundle completo" habia quedado obsoleta; el riesgo real era que `--sync` en modo
  estricto podia prunear rutas trackeadas del destino, incluida `.agent/docs/`. El fix
  impide borrar rutas git-trackeadas del destino, endurece el fail-safe de `prune_residues`
  y aclara el reporting de dry-run. Revision independiente aprobada.
- **Problema corregido:** `install_agent_system.py --sync` podia seleccionar para prune
  superficies destino-keep trackeadas fuera del `MANIFEST.workspace`.
- **Objetivo final:** que `--sync` nunca pode rutas trackeadas del destino aunque no sean
  installer-managed.
- **Desbloquea:** la parte segura de FASE 3 de A2d sin exponer entregables trackeados a
  perdida silenciosa.
- **Nota de trazabilidad:** `WOT-2026-006b` recoge aparte el endurecimiento del
  encoding guard (`3df6620`), que se commiteo durante este tramo pero quedo fuera del
  scope funcional principal de 003d.
- **Depende de:** WOT-2026-002c.
- **Origen:** session-2026-06-14-post-a2d-hardening.

## WOT-2026-003e - gates-dispatch: manejar 'destino sin tests locales' (alias MOTOR-FU-002)
- **Prioridad:** Baja
- **Scope:** motor/quality-gates (repo_motor)
- **Estado:** completed (motor 50bdf07)
- **deliverable_type:** code
- **Resultado:** `run_gates_dispatch` ya detecta ausencia de tests locales y hace skip
  auditable de pytest en vez de fallar con exit 4 sobre el destino. Quedaron 5 tests
  barrera y la suite cerro en verde.
- **Problema corregido:** tras retirar `tests/`, `run_pytest_safe.py` rompia los gates
  locales del destino con coleccion vacia.
- **Objetivo:** manejar el caso `destino sin tests locales` sin falso rojo.
- **Depende de:** WOT-2026-002c.
- **Origen:** session-2026-06-14-post-a2d-hardening.

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


## Plan WOT-2026-008 - Taxonomia portable

> 008a produce el manifiesto verificable sin modificar el motor. Los tickets de
> infraestructura discovery, migracion de prompts, migracion de skills y retirada
> de shims se crean solo despues de aprobar el manifiesto. No se permite un rename
> masivo ni anidar skills mientras discovery/collision sigan siendo planos.
>
> Secuencia canonica: 009a primero si se va a lanzar Builder; despues 008b
> (discovery/BOM/decision registry), 008c (registry/INDEX generado), 008d
> (renames con shims) y 008e (retirada versionada de shims). Las propuestas de
> prefijo `aud-*`, `manager_review_rubric.md` o carpetas nuevas son hipotesis de
> 008d, no acciones directas.

### WOT-2026-008b - Discovery/frontmatter hardening: BOM y registry decision
- **Prioridad:** Alta
- **Scope:** motor/skills-discovery
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008a, WOT-2026-009b
- **Problema:** el manifiesto 008a detecto 29 `SKILL.md` en disco pero solo 28
  skills descubiertas. La causa verificada fue BOM UTF-8 en
  `skills/man-review-implementation/SKILL.md`, que hace que `parse_frontmatter`
  vea `NO_FRONTMATTER` y omita la skill.
- **Objetivo:** barrer BOMs historicos en skills/prompts, hacer
  `discover_skills.py` tolerante o fail-closed ante BOM/frontmatter roto, y
  decidir el modelo canonico de registro: manifest-first explicito vs discovery
  por glob/recursivo/description. No mover ni renombrar skills.
- **Evidencia externa a evaluar:** `mattpocock/skills` usa skill-as-package,
  namespaces de dominio y un manifest/plugin registry explicito minimo
  (`plugin.json` lista paths). Tomar como patron de diseno, no como plantilla a
  copiar: sus categorias no son nuestro contrato Manager/Builder, no valida un
  `registry.json` rico y el manifest no elimina la necesidad de detectar BOM en
  `SKILL.md`.
- **Files Likely Touched:**
  - `scripts/discover_skills.py`
  - `scripts/check_skill_collisions.py`
  - `scripts/check_encoding_guard.py` si el gap real esta en su cobertura
  - tests de discovery/collision/encoding
  - documentacion minima del contrato de registry si se adopta manifest-first
- **Criterios binarios:**
  - Test reproduce el fallo: un `SKILL.md` con BOM no puede desaparecer
    silenciosamente del discovery.
  - Barrido unico de BOMs historicos en `skills/**/SKILL.md`, prompts relevantes
    y referencias de skill; el resultado queda documentado con rutas exactas.
  - Se aclara la diferencia entre `scripts/check_encoding_guard.py` (bloquea BOM,
    pero normalmente sobre archivos explicitos/staged) y cualquier script hermano
    de encoding; si hay inconsistencia CLI, queda corregida o ticketizada.
  - El sistema falla con diagnostico accionable o normaliza BOM de forma
    deliberada; no hay omision silenciosa.
  - `discover_skills.py --check-contract` y `check_skill_collisions.py` cubren el
    caso `man-review-implementation`.
  - DEC de registry resuelta: manifest-first explicito, glob recursivo o hibrido,
    con tradeoffs y compatibilidad.
  - DEC de discovery resuelta: mantener `triggers` como API propia, migrar a
    discovery por `description` estilo Claude, o soportar hibrido. La decision
    declara compatibilidad, coste de migracion y efecto en prompts/skills actuales.
  - Matriz `agents.json` allowlist vs triggers reales de `SKILL.md`: antes de
    clasificar ghosts, reparar BOM/discovery y re-ejecutar discovery. El caso
    `/review` se trata como `BOM/discovery casualty` verificado
    (`man-review-implementation`) y NO se retira de la allowlist solo porque hoy
    sea invisible. Los ghosts se separan en `BOM/discovery casualty` vs
    `invented/retired`; lista inicial a verificar en implementacion:
    `/impl`, `/test`, `/fix`, `/orchestrate`, `/archive`, `/report`, `/audit`,
    `/validate`. Todo trigger permitido por rol debe resolver a una skill real
    tras el fix de discovery, o quedar documentado como retirada intencional; toda
    skill critica de Builder/Manager debe estar alcanzable por su rol o documentar
    por que no.
  - Si se adopta discovery por `description` o hibrido, las descriptions siguen un
    patron verificable tipo `Use when ...`; se mide longitud y claridad antes de
    convertirlo en contrato obligatorio.
  - La DEC compara al menos cuatro opciones: registry central, manifest por skill
    (`manifest.json`), `.claude-plugin/plugin.json` compatible y discovery
    recursivo sin manifest.
  - La DEC evalua un esquema minimo de campos: `public_id`, `source`
    (`motor|host`), `canonical_source`, `path`, `trigger`, `role`, `status`
    (`active|deprecated|draft`), `deliverable_types`, `deprecated_by`,
    `compat_until` y, solo si aporta valor demostrado, `deliverable_profile`.
    `deliverable_profile` no se adopta por defecto: primero se contrasta contra
    `run_gates_dispatch.py` para evitar duplicar `deliverable_type`.
  - Registry/manifest rico queda atribuido como diseno propio (OKF/CEM/host-extends),
    no como patron probado por `mattpocock/skills`, que solo valida lista explicita
    de paths.
  - El contrato declara que el registry/manifest define la API publica activa,
    mientras el layout fisico puede contener docs, tests, deprecated o in-progress.
  - El contrato declara como se integra host-first: un posible
    `<repo_destino>/.agent/registry.json` puede extender/overridear el registry del
    motor, pero nunca contaminar `repo_motor`; la precedencia host local sigue
    siendo superior al fallback read-only del motor.
  - Si se adopta manifest-first, el manifest controla que esta activo; carpetas
    `deprecated/` o `in-progress/` solo son layout, no API publica.
  - Aunque se adopte manifest-first, hay barrera separada para `SKILL.md` con BOM
    o frontmatter roto, porque el agente aun debe leer semantica on-demand.
  - No hay renames, moves ni cambios de trigger.
- **STOP:**
  - Si el fix requiere reorganizar carpetas, abrir 008d; no mezclar.
  - Si el registry introduce fuente de verdad manual no validada, bloquear. Por
    defecto el registry debe ser generado/validado desde frontmatter/filesystem;
    los overrides host-first son la excepcion explicita.
  - Si la propuesta intenta crear `skills/domain/...` o `prompts/system/...` en
    008b, bloquear y moverlo a 008d tras registry + shims.

### WOT-2026-008c - Registry/INDEX generado de prompts y skills
- **Prioridad:** Media
- **Scope:** motor/skills-discovery
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008b
- **Problema:** los agentes descubren prompts/skills por memoria, glob o nombres
  humanos. Eso escala mal cuando haya categorias, shims o deprecated entries.
- **Objetivo:** crear un registry/INDEX generado y validable de prompts y skills
  con rutas canonicas, triggers, rol, tipo de artefacto y estado activo/deprecated.
  Si 008b adopta manifest-first, el INDEX es proyeccion generada del manifest; no
  una segunda fuente de verdad.
- **Files Likely Touched:**
  - script generador/validador de registry
  - `skills/INDEX.md` o manifest equivalente generado
  - docs de contrato del registry
  - tests
- **Criterios binarios:**
  - El INDEX/registry se genera desde fuente canonica validada; no es una tabla
    manual que pueda derivar.
  - Incluye prompts, skills, templates/references relevantes y scripts consumidores
    declarados por 008a.
  - Incluye owner/source (`motor|host`) y `canonical_source` para distinguir
    extensiones del destino, overrides y componentes canonicos del motor.
  - Distingue API publica, layout fisico y shims.
  - Distingue componentes activos de `deprecated`/`in-progress`; presencia en disco
    no implica disponibilidad para agentes.
  - Check de CI/pre-commit o gate local falla si el registry generado esta stale.
  - No mueve carpetas ni renombra archivos.
- **STOP:**
  - Si el INDEX exige mantenimiento manual, redisenar.
  - Si se detectan colisiones de trigger/nombre, abrir ticket dedicado antes de
    migrar.

### WOT-2026-008d - Migracion de naming audit/version con shims
- **Prioridad:** Media
- **Scope:** motor/skills-taxonomy
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008c
- **Problema:** hay hipotesis de mejora de naming (`aud-*`, `manager_review_rubric`,
  `bui-version-changelog`), pero renombrar sin registry y shims rompe triggers,
  docs, memoria y agentes externos.
- **Objetivo:** ejecutar solo los renames aprobados por DEC de 008a/008b, con shims
  temporales, warnings de deprecacion y pruebas de compatibilidad. Tambien evaluar
  progressive disclosure para prompts grandes: routers pequenos con referencias
  relativas a documentos de fase, cargados on-demand.
- **Files Likely Touched:**
  - prompts/skills afectados por renames aprobados
  - registry/manifest/INDEX
  - docs y referencias
  - tests discovery/collision
- **Criterios binarios:**
  - Cada rename tiene DEC aprobada, motivo, compatibilidad y fecha de retirada.
  - Los triggers antiguos siguen resolviendo mediante shim durante la ventana
    declarada.
  - `discover_skills.py --check-contract`, collision check, registry check y
    encoding pasan.
  - `rg` de nombres antiguos solo aparece en shims/deprecation docs permitidos.
  - No se fusionan prompts/skills solo por similitud de nombre; debe haber mejora
    demostrada de descubribilidad o reduccion de duplicacion.
  - Si se divide un prompt grande, queda un router canonico estable, referencias
    relativas validables y test/check de enlaces; no se duplican reglas entre
    router y subdocumentos.
  - Antes de mover prompts a subdirectorios, se lista toda referencia hardcoded a
    `prompts/*.md` en scripts, skills, prompts, docs y launchers; cada referencia
    tiene resolver/fallback o shim probado antes del move.
  - La opcion `deprecated/` se prefiere a borrar recursos legacy cuando aun hay
    referencias historicas o riesgo de compatibilidad; debe incluir README/registry
    que marque no uso.
  - DEC de longitud/progressive-disclosure resuelta con evidencia: no adoptar el
    limite de 100 lineas como contrato inicial (23/29 skills lo superan). Mantener
    o endurecer primero el umbral existente de 250 lineas (6/29 skills lo superan)
    y exigir migracion gradual a docs/references antes de cualquier rewrite masivo.
    Endurecer significa CABLEAR un gate con test (un SKILL.md de 251 lineas falla),
    no mantener el numero en prosa: hoy el 250 vive solo en create-agent-skill/SKILL.md
    sin enforcement (6/29 violadores silenciosos), mismo patron que la funcion BOM
    de 006b (definida pero no llamada). Sin gate+test no cuenta como cerrado.
- **STOP:**
  - Si un rename no puede tener shim, requiere aprobacion humana explicita.
  - Si rompe un contrato publicado, aplazar a major/versioned migration.

### WOT-2026-008e - Retirada versionada de shims y compat legacy
- **Prioridad:** Baja
- **Scope:** motor/skills-taxonomy
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008d
- **Problema:** los shims ayudan a migrar, pero si no tienen retirada versionada se
  convierten en deuda permanente.
- **Objetivo:** retirar shims ya caducados tras verificar que no quedan referencias
  vivas, con changelog y rollback claro.
- **Criterios binarios:**
  - `rg` no encuentra consumidores vivos de nombres legacy fuera de changelog/docs
    historicos.
  - Registry no lista entradas legacy como activas.
  - Tests de discovery/collision/registry pasan sin shims.
  - CHANGELOG documenta retirada y ruta nueva.
- **STOP:**
  - Si cualquier destino activo sigue usando el shim, aplazar y registrar evidencia.

## Plan WOT-2026-009 - Contract gates antes del Builder

> Objetivo de familia: impedir que el Builder arranque con contratos que ya
> contienen warnings, secciones incompatibles con `deliverable_type` o huecos
> que solo aparecen al hacer handoff. El Builder implementa contratos limpios;
> no repara contratos.
>
> Secuencia canonica: 009a cierra el parsing deliverable-aware inmediato; 009b
> resuelve la topologia multi-root (`delivery_authority` + FLT namespaced);
> 009c anade guardias reciprocas de aislamiento. No arrancar 008b hasta 009b.

### WOT-2026-009a - Pre-Builder contract gate deliverable-aware y fail-closed
- **Prioridad:** Alta
- **Scope:** motor/protocol-runtime
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008a
- **Problema:** WOT-2026-008a llego a Builder con un `work_plan.md` semanticamente
  claro para humanos, pero incompleto para el scope-gate mecanico. El warning solo
  aparecio en el cierre/handoff, cuando ya era tarde para tratarlo como preflight.
- **Objetivo:** bloquear mecanicamente el lanzamiento de Builder si el contrato del
  ticket no valida limpio en el mismo modo en que fallaria durante handoff. El gate
  debe respetar `deliverable_type` y aceptar las superficies documentales canonicas
  (`Builder`, `Read/inspect only`, `Manager-only`) en tickets `analysis`,
  `documentation` y `research`.
- **Files Likely Touched:**
  - `prompts/orchestrator_pipeline.md`
  - `prompts/launch_builder.md`
  - `.agent/agent_controller.py` o modulo de validacion de contratos si aplica
  - `scripts/validate_contract_formation.py` o validador/scope-gate equivalente
  - tests unitarios del validador/preflight
- **Criterios binarios:**
  - Existe un preflight mecanico antes de Builder que falla si `validate` no puede
    cerrar 0 errors / 0 warnings en modo equivalente a handoff.
  - Toda auditoria/review de cierre declara al inicio `repo_motor`, `repo_destino`,
    HEADs auditados, si tiene acceso real al destino y que claims quedan fuera de
    alcance. Sin acceso al destino, el veredicto maximo es `NO AUDITABLE`.
  - El gate es `deliverable_type`-aware: para `analysis`/`documentation`/`research`
    acepta `Builder` + `Read/inspect only` + `Manager-only` como contrato valido de
    superficies, sin exigir una forma propia de tickets `code`.
  - Post-cierre verifica que cada deliverable declarado existe en el workspace activo
    donde se cerro el ticket; si no existe, el cierre queda bloqueado.
  - Test negativo: un ticket `analysis` sin superficie Builder ni Files Likely
    Touched falla antes de Builder.
  - Test positivo: un ticket `analysis` con superficies documentales canonicas pasa
    el preflight.
  - Test negativo: un warning que solo aparece en modo handoff bloquea el arranque.
  - Override excepcional se modela como evento auditable del bus con owner, razon y
    alcance; no como nota Markdown.
  - El prompt del pipeline indica que ningun Builder arranca si falla este preflight.
- **STOP:**
  - Si introducir `READY_FOR_BUILDER` exige tocar state-machine amplia, separar ese
    estado a un ticket posterior y cerrar 009a con gate previo al lanzamiento.
  - Si el fix relaja warnings globalmente, parar: el objetivo es distinguir contrato
    valido por tipo, no permitir warnings.
  - Si el override no queda auditable por bus, no implementarlo.

### WOT-2026-009b - Scope gate topology-aware por delivery_authority y FLT namespaced
- **Prioridad:** Alta
- **Scope:** motor/protocol-runtime
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-009a
- **Problema:** en tickets con `delivery_authority: repo_motor`, el estado operativo
  vive en `repo_destino` pero el diff productivo vive en `repo_motor`. El scope gate
  actual puede comparar el diff/whitelist contra el root equivocado y producir
  warnings falsos (`Files Likely Touched` sin cobertura) aunque el commit del motor
  este dentro de scope. Usar `--scope-override` oculta el mismatch en vez de resolverlo.
- **Objetivo:** hacer que validate/pre-handoff resuelvan el root productivo segun
  `delivery_authority` usando una unica seccion de scope: `## Files Likely Touched`
  con namespaces `### repo_motor` / `### repo_destino`. No crear `External Scope` ni
  `Operational Surfaces` como secciones nuevas manuales: duplicarian semantica ya
  cubierta por FLT y por la excludelist operativa.
- **Contrato propuesto en `work_plan.md`:**
  - `delivery_authority` sigue siendo el campo canonico.
  - `## Files Likely Touched` admite subsecciones opcionales:
    - `### repo_motor` para rutas productivas relativas a `repo_motor`.
    - `### repo_destino` para rutas productivas relativas a `repo_destino`.
  - Rutas sin namespace mantienen backward compatibility y se resuelven contra el root
    de autoridad del ticket.
  - Las superficies operativas del destino no se declaran manualmente: se excluyen por
    la excludelist existente y el gate las reporta como `excluded_operational` en su
    diagnostico.
- **Files Likely Touched:**
  - `.agent/scope_gate.py`
  - `.agent/agent_controller.py`
  - `scripts/pre_handoff_guard.py`
  - `scripts/delivery_hygiene_check.py` si participa en validate/preflight
  - tests unitarios de scope/topologia
  - prompts/plantillas de contrato solo si necesitan documentar FLT namespaced
- **Callers obligatorios a revisar en 009b:**
  - Flujo validate/caller de `check_scope_gate` en `.agent/agent_controller.py`: debe usar diff
    productivo por autoridad, no diff monolitico del destino. No asumir que existe
    una funcion llamada `_check_scope_for_validate`; verificar el caller real por grep.
  - Flujo `mark-ready`/staging en `.agent/agent_controller.py`: debe usar el mismo
    dispatch por autoridad.
  - `scripts/pre_handoff_guard.py`: verificar existencia y contenido antes de tocar codigo.
    Si mantiene parser propio de FLT, debe delegar en
    `scope_gate.parse_files_likely_touched` o recibir `delivery_authority` + roots
    equivalentes. No puede seguir resolviendo siempre contra `project_root`.
- **Criterios binarios:**
  - Test positivo: ticket `delivery_authority: repo_motor` con diff en motor declarado
    bajo `## Files Likely Touched / ### repo_motor` y solo superficies operativas en
    destino valida 0/0.
  - Test/parser: `## Files Likely Touched` distingue subsecciones `### repo_motor` y
    `### repo_destino`; no mezcla rutas de ambos namespaces en un unico set.
  - Test negativo: ticket `delivery_authority: repo_motor` con diff en motor fuera de
    `### repo_motor` bloquea o emite warning/error accionable.
  - Test negativo: ticket `delivery_authority: repo_motor` sin namespace ni FLT valido
    pero con diff productivo en motor NO pasa como limpio.
  - Test negativo: un plan que solo declara `### repo_destino` no cubre diff productivo
    del motor.
  - Test legacy/backward-compatible: ticket sin namespaces y autoridad destino conserva
    comportamiento actual o emite warning de migracion documentado.
  - `Files Likely Touched` plano sigue funcionando para tickets simples de destino.
  - El validador no exige que rutas del motor existan bajo `repo_destino`.
  - El resultado del gate incluye, cuando aplique, `excluded_operational` informativo
    para superficies vivas ignoradas por excludelist; no requiere mantener una segunda
    lista manual en el plan.
  - El error indica que repo/root se valido, que subseccion falta y como revalidar.
  - `ruff`, tests focales y validate destino final pasan con evidencia real.
- **STOP:**
  - No introducir guardias reciprocas amplias en este ticket; eso es 009c.
  - No crear secciones nuevas `External Scope` ni `Operational Surfaces` salvo que la
    auditoria demuestre que FLT namespaced no puede cubrir el caso.
  - No reemplazar `delivery_authority` por `target_repository`; si se necesita alias,
    debe ser backward-compatible y documentado como derivado.
  - No invertir globalmente la prioridad de `get_changed_files`; crear/usar una ruta
    explicita tipo `get_productive_changed_files(delivery_authority, roots)` para scope.
  - No usar `accepted_health_exception` permanente para warnings de topologia.
  - No relajar scope global: el objetivo es validar contra el root correcto.
  - Primer paso obligatorio de 009b: `rg "parse_files_likely_touched|Files Likely Touched" .agent scripts bus tests` para inventariar callsites/parsers antes de editar.
  - Verificar explicitamente si existe `_check_scope_for_validate`; si no existe, documentar el caller real de validate que invoca `check_scope_gate`.
  - No anadir otro parser FLT. Si no se pueden unificar todos los parsers en este ticket,
    inventariar los restantes como deuda con criterio de salida.

### WOT-2026-009c - Guardias reciprocas de aislamiento repo_motor/repo_destino
- **Prioridad:** Media
- **Scope:** motor/protocol-runtime
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-009b
- **Problema:** resolver el root correcto evita falsos warnings, pero aun falta una
  barrera explicita contra contaminacion cruzada: tickets de motor no deben dejar
  cambios productivos en destino, y tickets de destino no deben mutar el motor salvo
  contrato topology-aware explicito.
- **Objetivo:** implementar guardias de aislamiento reciproco apoyadas en
  `delivery_authority`, FLT namespaced y la excludelist operativa existente, con
  diagnosticos self-service y tests bidireccionales.
- **Files Likely Touched:**
  - `.agent/agent_controller.py`
  - `.agent/scope_gate.py`
  - `scripts/pre_handoff_guard.py`
  - `scripts/delivery_hygiene_check.py`
  - tests unitarios/integracion de aislamiento multi-root
- **Criterios binarios:**
  - Ticket `repo_motor`: cambios productivos no-operativos en `repo_destino` bloquean.
  - Ticket `repo_motor`: cambios en `repo_destino` excluidos por la excludelist operativa
    pasan y se reportan como `excluded_operational`, sin contarse como entrega productiva.
  - Ticket `repo_destino`: cambios productivos en `repo_motor` bloquean salvo contrato
    explicito y validado que declare ambos roots.
  - Ticket mixto/topologico: solo pasa si declara ambos namespaces y sus superficies.
  - Los mensajes distinguen `contaminacion productiva`, `superficie operativa excluida`
    y `scope externo no declarado`.
  - Tests demuestran que cada guardia falla sin la mejora y pasa con ella.
  - No se toca state machine salvo que sea imprescindible; si lo es, separar ticket.
- **STOP:**
  - Si la implementacion exige cambiar eventos de bus o estados canonicos, abrir ticket
    separado antes de tocar runtime amplio.
  - Si una guardia bloquea superficies vivas (`work_plan`, `execution_log`, `STATE`,
    bus runtime) cubiertas por excludelist, ajustar el modelo antes de cerrar.
  - Si no hay fixture multi-root realista, no aprobar solo con mocks monoliticos.

### WOT-2026-009d - Consolidar parsers Files Likely Touched restantes
- **Prioridad:** Baja
- **Scope:** motor/protocol-runtime
- **Estado:** candidate
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-009b
- **Problema:** hay multiples parsers de `Files Likely Touched` en el motor
  (`scope_gate`, `agent_controller`, `motor_checkpoint`, `pre_handoff_guard`,
  `pip_audit_policy`, `graph_context`, `validate_ticket_prose`). Cada nueva semantica
  de FLT (namespaces, authority, warnings) amplifica la deriva si no se centraliza.
- **Objetivo:** reducir los parsers activos a una fuente canonica o dejar wrappers
  delgados con tests de paridad.
- **Criterios binarios:**
  - Inventario actualizado de parsers FLT con consumidor y semantica.
  - Los parsers operativos delegan en una funcion canonica o tienen test de paridad.
  - Ningun parser nuevo se introduce sin justificar por que no puede delegar.
  - Tests cubren FLT plano y FLT namespaced.
- **STOP:** si un parser es solo lint/prosa y no puede compartir semantica exacta, dejar
  wrapper documentado con limites y test minimo.

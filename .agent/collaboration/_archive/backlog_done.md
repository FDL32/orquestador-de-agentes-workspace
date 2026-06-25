# Backlog -- historico (movido por WOT-2026-012a)

> Historico de tickets terminales y fichas cerradas, movido aqui por WOT-2026-012a
> para dejar backlog.md como cola viva parseable.
> Contenido = backlog.md integro PRE-corte (HEAD), cero perdida de historico.
> NOTA: conserva 3 control chars heredados de HEAD (region historica) cuya FUENTE
> investiga WOT-2026-011c; no se reconstruyen aqui para no falsear el historico.
> Conserva integra la seccion ### WOT-2026-012a.

---

## Cierres posteriores al corte 012a

| Ticket | Estado | Nota |
|--------|--------|------|
| WOT-2026-012b | completed | cerrado canonico 2026-06-20; gate backlog fail-closed aprobado y cerrado por Manager. |
| WOT-2026-011e | completed | cerrado canonico 2026-06-20; xdist opt-in local entregado; default del runner sigue intacto por 3 tests no parallel-safe. |
| WOT-2026-010x | completed | cerrado canonico 2026-06-21; security-audit.yml migro a gitleaks CLI OSS sin action licenciado. |
| WOT-2026-010m | completed | cerrado canonico 2026-06-21; quality-gates.yml gano piloto xdist non-blocking sin tocar el cierre serial canonico. |
| WOT-2026-011c | completed | cerrado canonico 2026-06-19; spike research completado. Follow-up registrado: `WOT-2026-011j`. |
| WOT-2026-013e | completed | cerrado canonico 2026-06-22; inventario auditable de la suite (3111 tests). Follow-ups vivos: WOT-2026-013f (poda tests/deprecated/), WOT-2026-013g (coste unknown). |
| WOT-2026-013f | completed | cerrado canonico 2026-06-22; poda segura de `tests/deprecated/` entregada. Siguiente ticket vivo: WOT-2026-013g. |
| WOT-2026-013g | completed | cerrado canonico 2026-06-22; el coste del outlier quedo atribuido al purge de sandbox en setup, sin optimizacion segura en este ticket. Follow-ups vivos: WOT-2026-013h y WOT-2026-013i. |
| WOT-2026-013h | completed | cerrado canonico 2026-06-22; el archivador pasa a dejar renames staged (sin auto-commit) y se cierra la herencia recurrente de `archive_rename_uncommitted`. Siguiente ticket vivo: WOT-2026-013i. |
| WOT-2026-013i | completed | cerrado canonico 2026-06-22; purge de sandbox arreglado (PermissionError en .git read-only que ignore_errors tragaba, dejando el purge no-op). Latencia recurrente ~39s/sesion creciente -> ~0s en estado estable. Follow-up: WOT-2026-013j (drift FLT backlog<->contrato). |
| WOT-2026-013j | completed | cerrado canonico 2026-06-22 (bus seq 1358 COMPLETED, Manager-approved); gate ejecutable que bloquea fichas de backlog que re-declaran Files Likely Touched (check_backlog_contract). Follow-ups: 013k/013l/013m. |
| WOT-2026-013s | completed | cerrado canonico 2026-06-25; `repo_motor/.agent/runtime/memory/observations.jsonl` paso de 168 errores a `validate_observations.py --strict` EXIT 0 sin tocar `signal`. Sucesor vivo desbloqueado: WOT-2026-013r. |
| WOT-2026-013r | completed | cerrado canonico 2026-06-25; fix motor `8e84a25` (barrera honesta contra FP-012 en `tests/unit/test_upgrade.py`) y cierre workspace `39eabd6`. Follow-ups vivos: WOT-2026-013u (parser CLI de closeout/review expuesto por el cierre) y WOT-2026-013t (deuda estructural opcional de dedup/binding independiente). |
| WOT-2026-013u | completed | cerrado canonico 2026-06-25; parser CLI de closeout/review ahora honra `--ticket` y el help quedo alineado. Commit motor `416a8f0`; cierre/proyecciones en workspace ya sincronizados. |
| WOT-2026-013l | completed | cerrado canonico 2026-06-25; CLI opt-in `prune_runtime_retention.py` entregada con barreras hermeticas y suite canonica verde. Commit motor `cf689eb`; follow-up opcional visible: WOT-2026-013v sobre semantica de `reviews/` por mtime de directorio. |
| WOT-2026-013v | completed | cerrado canonico 2026-06-25; semantica de `reviews/` por `mtime` de directorio hecha explicita y blindada sin cambiar el algoritmo de orden. Commit motor `9ddfe5d`; follow-ups vivos restantes de la familia: `013k` (notifications versionado) y `013t` (deuda estructural opcional de upgrade). |
| WOT-2026-013k | completed | cerrado canonico 2026-06-25; `prune_runtime_retention.py` ahora incluye `collaboration/archive/notifications_*.md` como cuarta superficie local gitignored opt-in, con help alineado y suite canonica verde al HEAD `84726ad`. Follow-up vivo restante de runtime-retention: WOT-2026-013t (deuda estructural opcional de upgrade, no relacionada con retention). |
| WOT-2026-013m | delivered-no-bus | ENTREGADO Y VERIFICADO fuera del lifecycle de bus (2026-06-22): commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de Overall FAIL a WARN. overall_status del closeout ahora respeta blocking=False (un step no-bloqueante ya no fuerza exit 1). NO tiene eventos de bus por no haberse bootstrappeado como ticket activo; cierre canonico por bus no realizado, evidencia = commit+tests+efecto. |
| WOT-2026-013n | completed | cerrado canonico 2026-06-22; commit motor f48191f y cierre destino 935907c/85b76cb. El motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin mapearlos a `COMPLETED`; validate final 0/0 tras session-close y health audit 1449. Follow-up vivo: WOT-2026-013o (strict-green de observations portable antes de nuevas memorias). |
| WT-2026-200 | completed | reconciliado canonico 2026-06-22 (campana legacy WT). Entrega real: commit motor 3b9f649 (launcher/supervisor resume, 5 tests regresion, ruff PASSED). Aprobado: bus seq 414 REVIEW_DECISION=approve. Atasco solo operativo: faltaba STATE_CHANGED->COMPLETED + SUPERVISOR_CLOSED tras READY_TO_CLOSE (seq 415). reconcile_ticket.py READY_TO_CLOSE->COMPLETED, validate 0/0. |
| WT-2026-249b | completed | reconciliado canonico 2026-06-22 (campana legacy WT). Entrega real: commit motor bb7edfc (excluir BUILDER_BRIEF_ del guard de superficies vivas) + CHANGELOG L208/L212 + AUDIT archivado. Cerrado en sesion destino 2026-06-11 (commit 7e2519f). Bus BLOCKED (seq 1130/1131) era approval-timeout huerfano del 2026-06-17 (from_state=UNKNOWN), 6 dias posterior al cierre real; no es rechazo funcional. reconcile_ticket.py BLOCKED->COMPLETED, validate 0/0. |
| WT-2026-238a | completed | reconciliado canonico 2026-06-22 (campana legacy WT). Ticket documental (PLAN: "no es un ticket de codigo"). Entrega real: commit destino 8c4f6ad (closeout/handoff documental) con entrada propia en CHANGELOG. AUDIT archivado, sin riesgos bloqueantes disparados. Bus HANDOFF_BLOCKED (seq 4-10) eran fallos mecanicos del guard de pre-handoff sobre un ticket documental; cierre por via documental. reconcile_ticket.py IN_PROGRESS->COMPLETED, validate 0/0. |
| WT-2026-245a | completed | reconciliado canonico 2026-06-22 (campana legacy WT). Entrega real: commit motor db22117 (expand ticket prefix support, +230 incl test unit 206 lineas). Aprobado: AUDIT_WT-2026-245a archivado Estado=APPROVED, TP-01..07 verificados, FLT coincide con diff. manager_feedback vivo INSPECT/empty-stdout era del primer intento fallido (16:14) ANTES del READY_FOR_REVIEW final (17:16); no es rechazo funcional. reconcile_ticket.py READY_FOR_REVIEW->COMPLETED, validate 0/0. |
| WT-2026-182 | completed | reconciliado canonico 2026-06-22 (campana legacy WT) con APROBACION VERIFICABLE hecha hoy. Entrega real: commit motor 5398b0a (repomix context injection en review_bridge; codigo vive y fue extendido). Historia: review-1 emitio changes (seq 83), Builder retrabajo (seq 85), review-2 fallo por bridge (fallback_inspect exit 1) -> nunca obtuvo approve en su dia. Cierre HOY: Manager Review-1 APROBADO (ruff PASS, 12/12 tests focales repomix en test_manager_review_bridge.py) + Review-2 adversarial CONFIRMA CIERRE (4 counterexamples refutados: changes irrecuperable pero retrabajo coherente, except amplio resuelto en codigo vivo, -y no enmascara hang, codigo es del ticket). reconcile_ticket.py READY_FOR_REVIEW->COMPLETED, validate 0/0. |
| WT-2026-245b | completed | reconciliado canonico 2026-06-22 (campana legacy WT) con PRIMERA REVIEW VERIFICABLE hecha hoy. Entrega real: commits motor 5f3247b (checkpoint M3 Model B para non-code) + 327e5b0 (excluir _archive/ del scope gate), ambos en main. NUNCA tuvo review en su dia (murio por bridge_heartbeat_stale seq 1129, 8 dias despues; fallo de infra, no rechazo). Cierre HOY: Manager Review-1 APROBADO (ruff PASS, 12/12 tests checkpoint Model B, 86/86 pre-handoff sin regresion, suite completa 3095 passed/0 failed) + Review-2 adversarial CONFIRMA CIERRE (agujero _archive/ teorico-no-practico, sin mock drift ni floor assertion, bypass non-code no degrada code/mixed). reconcile_ticket.py READY_FOR_REVIEW->COMPLETED, validate 0/0. |
| WT-2026-239a | superseded | NO completado, cierre honesto Ruta B 2026-06-22 (campana legacy WT). Distinto de 182/245b: NO se hizo review-de-rescate porque el Manager YA emitio veredicto de contenido sustantivo (no fallo de infra). El Manager EMITIO CHANGES (MANAGER_REVIEW_WT-2026-239a.md Status: "CHANGES (no aprobado)", "No apruebo el cierre", bug CRITICO de seguridad: bypass documental no detecta motor sucio + test que cementa el bug). Commit destino 38bdd74 = "manager closeout WITHOUT approval". El scope migro a tickets hijos WT-2026-240a (commit aa1b3cd "bloquear repo_motor sucio en pre-handoff documental") y WT-2026-241a, que SI entregaron el fix. 239a NO se cierra como COMPLETED: stop condition (REVIEW_DECISION=changes sin retrabajo verificable en este ticket). Bus permanece en READY_FOR_REVIEW con MANAGER_REVIEW vivo como evidencia; NO se emiten eventos de bus para no falsear historia. validate sigue 0/0 (el validador no trata tickets legacy no-activos como drift). |

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
| Baja | WOT-2026-008a | Manifiesto de taxonomia y migracion de prompts/skills | system/docs-coherence | completed | WOT-2026-007d | session-2026-06-15-contract-formation |  <!-- analysis en repo_destino; cerrado canonico (bus: REVIEW_DECISION approve -> COMPLETED -> SUPERVISOR_CLOSED, commit 2e74fce); artefacto .agent/docs/taxonomy_migration_WOT-2026-008a.md; contrato enmendado tras CHANGES: inventario ampliado a templates/references/_shared/llms/tools + DEC-008-004 manifest-first; cero moves/edits en repo_motor -->
| Alta | WOT-2026-008b | Discovery/frontmatter hardening: BOM y registry decision | motor/skills-discovery | completed | WOT-2026-008a, WOT-2026-009b | session-2026-06-15-taxonomy |  <!-- motor 869b920; BOM false-green fixed, discovery visible 29/29, DEC-008B registry model closed; bus reconciliado a COMPLETED 2026-06-22 (drift: bus quedo en READY_FOR_REVIEW tras cierre real) -->
| Media | WOT-2026-008c | Registry/INDEX generado de prompts y skills | motor/skills-discovery | completed | WOT-2026-008b | session-2026-06-15-taxonomy |  <!-- cerrado canonico 2026-06-18: motor 67c2dcc; INDEX generado por discover_skills --generate-index + stale-check; DEC-008B Opcion 4 respetada; validate 0/0 --> |
| Media | WOT-2026-008d | Migracion de naming audit/version con shims | motor/skills-taxonomy | completed | WOT-2026-008c | session-2026-06-15-taxonomy |  <!-- cerrado canonico 2026-06-18: motor 4871536+af1359f; DEC-008D-001 + discover_skills.py --check-naming + run_gates_dispatch; actor-first enforced; suite 2965 passed; validate 0/0 --> |
| Baja | WOT-2026-008e | Rename versionado review_manager -> manager_review con shim y retirada de excepcion legacy | motor/skills-taxonomy | closed | WOT-2026-008d | session-2026-06-15-taxonomy |
| Media | WOT-2026-008f | Gate de integracion destino-motor y lifecycle operativo | motor/protocol-destino | completed | WOT-2026-008c | session-2026-06-16-taxonomy-review |  <!-- cerrado canonico 2026-06-18: motor 86c6425; wrapper destino-motor; suite 2994 passed; validate 0/0 --> |
| Media | WOT-2026-008g | DEC de vocabulario y naming por rol | motor/skills-taxonomy | completed | WOT-2026-008f, WOT-2026-008d, WOT-2026-008e | session-2026-06-18-role-naming |  <!-- cerrado canonico 2026-06-18: motor 79da19d+264a6ad+6216b12+a7640ee; contrato T-008G-001 restaurado; validate 0/0 --> |
| Alta | WOT-2026-008h | Rename versionado de 5 prompts orchestrator con shims | motor/skills-taxonomy | completed | WOT-2026-008g | session-2026-06-18-role-naming |  <!-- motor e5975eb; 5 canonicos + 5 stubs; source_prompt migrado; prose viva legacy barrida; 46 focales + suite 3006/0; Manager APROBADO; cierre canonico 0/0 -->
| Alta | WOT-2026-008k | Formalizar role: auditor en frontmatter de skills auditoras | motor/skills-taxonomy | completed | WOT-2026-008g | session-2026-06-18-role-naming |  <!-- cerrado canonico 2026-06-18: motor fba7a39; role separado de owner, 70 focales, suite 3012 passed, validate 0/0 --> |
| Alta | WOT-2026-009a | Pre-Builder contract gate deliverable-aware y fail-closed | motor/protocol-runtime | completed | WOT-2026-008a | session-2026-06-15-contract-formation |  <!-- motor 440e878+9b7666f; scope gate deliverable-aware; preflight protocol fail-closed; Manager APROBADO; cierre canonico 0/0 -->
| Alta | WOT-2026-009b | Scope gate topology-aware por delivery_authority y FLT namespaced | motor/protocol-runtime | completed | WOT-2026-009a | session-2026-06-15-contract-formation |  <!-- motor c308f40+35fb46b; parse_flt_namespaced+_parse_flt_section; pre_handoff_guard delega a scope_gate; 67 focal tests; Manager APROBADO; validate 0/0 -->
| Media | WOT-2026-009c | Guardias reciprocas de aislamiento repo_motor/repo_destino | motor/protocol-runtime | completed | WOT-2026-009b | session-2026-06-15-contract-formation |  <!-- motor a020afd + destino closeout canonico; validate 0/0 -->
| Baja | WOT-2026-009d | Consolidar parsers Files Likely Touched restantes | motor/protocol-runtime | completed | WOT-2026-009b | session-2026-06-15-contract-formation |  <!-- motor 43e80bb; parse_flt_raw_buckets canonico en scope_gate; 3 consumidores delegando; 64 tests; cierre canonico manager-approve; validate 0/0 -->
| Media | WOT-2026-009e | Launcher Builder relaunch cleanup con $BuilderOnly + locks/session cleanup | motor/launcher-runtime | completed | WOT-2026-009b | session-2026-06-15-launcher-followup |  <!-- motor cf12068 + docs hardening follow-up; cierre canonico manager-approve; validate 0/0 -->
| Media | WOT-2026-009f | Gate de publicacion pre-push para repo_destino | motor/protocol-destino | completed | WOT-2026-009c | session-2026-06-15-contract-formation |  <!-- motor a5c2d94+scripts/check_destino_publish_ready.py; exit1=drift/exit2=APPROVED/exit0=OK; orchestrator_pipeline seccion gate; 8 tests; cierre canonico manager-approve; validate 0/0 -->
| Alta | WOT-2026-009g | Pre-handoff: work_plan.md debe estar commiteado al handoff | motor/protocol-runtime | completed | WOT-2026-008b, WOT-2026-009b | session-2026-06-16-handoff-hardening |  <!-- motor d245ba5+4b61b4b; helper assert_work_plan_committed fail-closed; cubre --mark-ready + --pre-handoff; Manager APROBADO; validate 0/0; cierre publicado -->
| Media | WOT-2026-010a | Glosario de nomenclatura + rename PLAN_WT->STRATEGY_WOT / audit_plan->audit_ticket_contract | motor/protocol-docs | completed | WOT-2026-008b, WOT-2026-009g | session-2026-06-16-naming-debt |  <!-- motor cac2648+842184a+585fadb; gate nomenclature classify history/generator; closeout canonico 2026-06-16 -->  <!-- reservar PLAN para familia; ticket=WOT; STRATEGY_WOT-<ID> estrategia tecnica; AUDIT_WOT-<ID>; audit_ticket_contract.md; WP/WT legacy sin migracion; toca 5 archivos codigo; validate_ticket_prose.py SI se toca en 010a pero solo tras cerrar 009g -->
| Alta | WOT-2026-010c | Gate de cierre: exigir evidencia literal "0 failed" de run_pytest_safe antes de mark-ready | motor/quality-gates | completed | WOT-2026-010b | session-2026-06-16-canonical-close-debt |  <!-- Origen: 010a se publico con suite canonica ROJA (test_no_inline_ticket_regex); CI GitHub Quality Gates fallo en 842184a y 585fadb. Causa raiz VERIFICADA: focal verde != canonica verde; el cierre cito "N passed" sin cruzar "1 failed". 010b lo arreglo (69d53c1) pero la grieta de proceso sigue: nada bloquea mark-ready si run_pytest_safe tiene failed>0. Objetivo: el handoff (mark-ready / pre-handoff) exige evidencia literal de run_pytest_safe con 0 failed leida hasta el final, no solo passed. Barrera verificada: con una suite roja simulada, mark-ready debe bloquear. Ver memoria canonical-close-read-failed-not-only-passed. Scope: pre_handoff_guard / agent_controller mark-ready path + test. NO confundir con scope gate ni con work_plan-committed (009g). -->
| Media | WOT-2026-010e | Encoding early-detection tras Write/Edit/MultiEdit de agentes | motor/devex-encoding | completed | WOT-2026-010c | session-2026-06-16-encoding-early-detection |  <!-- verificado: motor fec2766+b0248b1; bus seq 1103-1108; cierre canonico 2026-06-16; hook encoding post-write + 18 tests focales; validate 0/0. -->
| Alta | WOT-2026-010d | Pausar/reanudar ticket activo con bus canonico y resume fail-closed | motor/protocol-runtime | done | WOT-2026-010c | session-2026-06-16-pause-lifecycle |  <!-- verificado: motor eda918f (impl: PAUSED enum + flags pause/resume/abort + artefacto paused/<ticket>.json) + f4e5502 (fix regresion enum READY_TO_CLOSE/UNKNOWN + NON_TERMINAL_STATES). Cierre canonico 2026-06-17: REVIEW_DECISION approve->READY_TO_CLOSE->CLOSE_CONFIRMED->COMPLETED->SUPERVISOR_CLOSED (seq 1114-1118). Suite 0 failed (-m "not integration and not slow"); validate 0/0. -->
| Baja | WOT-2026-010f | Limpieza/investigacion de checkpoint/review-none | motor/protocol-runtime | completed | WOT-2026-010c | session-2026-06-16-review-none-checkpoint |  <!-- verificado: motor ec4526b; bus seq 1119-1127; cierre canonico 2026-06-17; INVALID_PLAN_IDS y no checkpoint/review-none; validate 0/0. -->
| Media | WOT-2026-010g | Auditoria y clasificacion de prompts/skills legacy | motor/protocol-docs | completed | WOT-2026-010c | session-2026-06-16-legacy-prompts-skills |  <!-- verificado: destino 8c9fe42 (R2) + 33ff0d2 (manager line-75 fix); reporte .agent/docs/prompts_skills_inventory_WOT-2026-010g.md (20 prompts + 29 skills + 2 support); motor read-only (status vacio); F1 (goose-skill.json mal etiquetado deprecated-removable con consumidor vivo test_skill_manifest) corregido en R2 a legacy-retained; taxonomia final: 49 canonical, 1 alias-compat, 3 legacy-retained, 0 deprecated-removable, 0 destination-only; bus REVIEW_DECISION changes->approve -> CLOSE_CONFIRMED -> SUPERVISOR_CLOSED; validate 0/0; cierre canonico 2026-06-17. Follow-ups identificados (no abiertos): retirar test_goose_native_skill + borrar goose-skill.json/goose_integration.py; deprecar scripts/orquestador.py GooseAdapter; actualizar INDEX.md para quickstart-checklist. -->  <!-- Objetivo: inventariar prompts/skills como canonical, alias-compat, legacy-retained, deprecated-removable o destination-only antes de mover/eliminar. Origen: cierre de sesion detecto audit_plan.md stub alias, quickstart-checklist legacy, Goose/Claw deprecated y refactor-manager con piezas Goose. Regla: tooling portable permanece en repo_motor; historia operativa especifica del destino vive en repo_destino; alias de compat se conservan hasta demostrar cero consumidores. Barrera: rg de consumidores vivos antes de cualquier move/delete; no reescribir historia fiel. -->
| Media | WOT-2026-010h | Propagar regla de prefijo per-project a bootstrap y auditorias | motor/protocol-docs | completed | WOT-2026-010a | session-2026-06-16-prefix-per-project |  <!-- verificado: motor 8dbfcda; 4 prompts (session/destination_bootstrap + audit_complete/audit_post_change) con formulacion canonica unica (PREFIX se lee de AGENTS.md/CLAUDE.md; WOT-=motor only; verify via --validate); diff +6/-2 dentro de FLT; nomenclatura exit 0, encoding exit 0, validate 0/0; bus REVIEW_DECISION approve -> CLOSE_CONFIRMED -> SUPERVISOR_CLOSED; decision artifact decision_WOT-2026-010h.json; cierre canonico 2026-06-17. Non-finding investigado: --validate lee Ticket prefix de PROJECT.md (agent_controller:1691) mientras la fuente conceptual es AGENTS.md/CLAUDE.md; el contrato separa fuente-de-regla de mecanismo-de-verificacion a proposito. Follow-up sugerido (no bloqueante): si la fuente del prefijo migra a AGENTS.md/CLAUDE.md, actualizar _validate_host_project_prefix. --> <!-- Origen historico: la regla "el <PREFIX> de ticket es per-project, no universal" esta fijada en codigo (bus/ticket_id.py: (?:WP|WT|[A-Z]{3})) y parcialmente en session_bootstrap.md (lineas 59,88), pero NO explicita ni consistente en los prompts de arranque/auditoria. Un agente en otro repo_destino podria asumir WOT- erroneamente. Scope: prompts/session_bootstrap.md, prompts/destination_bootstrap.md, prompts/audit_complete_motor_destination.md, prompts/audit_post_change_system_health.md. Criterios binarios: (1) cada prompt dice explicitamente que el <PREFIX> se lee del contrato del repo activo, con ORDEN DE FUENTE: primario = AGENTS.md/CLAUDE.md autocargado del destino; cuando el sistema exige "Ticket prefix: XXX", verificar via agent_controller --validate (no fiarse de una linea suelta de PROJECT.md sobre validate); (2) WOT- se describe SOLO como prefijo del motor/dogfooding, no universal; (3) los 4 prompts no se contradicen entre si; (4) no se generan ejemplos vivos nuevos con WP-/WT-; (5) check_ticket_nomenclature.py + encoding guard + validate pasan. deliverable_type: documentation. NO mezclar con 010g (010g = clasificacion/retirada de legacy; 010h = endurecer nomenclatura de prefijo). Ver memoria ticket-nomenclature-canonical. -->
| Media | WOT-2026-010i | Hardening de review packet, forbidden surfaces y tests semanticos | motor/protocol-runtime | completed | WOT-2026-010e, WOT-2026-010q | session-2026-06-16-review-hardening |  <!-- verificado: motor fdd55b6; bus seq 1195-1203; cierre canonico 2026-06-17; hardening de forbidden surfaces, commit-visible y tests semanticos; validate 0/0. -->
| Media | WOT-2026-010j | Baseline de performance de suite: durations y hotspots subprocess/git | motor/test-performance | completed-via-010n | WOT-2026-010c | session-2026-06-17-suite-performance |  <!-- verificado: motor c05dbfe; reporte en repo_motor; CONTRACT_GAP de deliverables resuelto por 010n; 010j no requirio cierre independiente segun cierre de 010n; bus reconciliado a COMPLETED 2026-06-22 (drift: bus quedo en IN_PROGRESS tras cierre via 010n) -->
| Media | WOT-2026-010k | Reducir coste de tests git/subprocess sin cambiar politica de gates | motor/test-performance | completed | WOT-2026-010j | session-2026-06-17-suite-performance |  <!-- verificado: motor 55d84bb; bus seq 1151-1161; cierre canonico aaaff65; dos hotspots reducidos; validate 0/0. -->
| Baja | WOT-2026-010o | Tests deterministas para evidence-gate real (manager_review_bridge/review_bridge sin acoplar a repo_destino vivo) | motor/test-determinism | completed | WOT-2026-010k | session-2026-06-17-suite-performance |  <!-- verificado: motor 591bec5; closeout canonico b087ef5; suite --level all 2910 passed, level=all/default_discovery, validate 0/0. -->
| Baja | WOT-2026-010p | Medir varianza de run_pytest_safe --level all y aislar outliers inestables | motor/test-performance | completed | WOT-2026-010o | session-2026-06-17-suite-performance |  <!-- verificado: motor e5d4a9d; bus seq 1186-1194; cierre canonico 2026-06-17; C1 5m34s, C2 5m29s, conclusion entorno/I-O. -->
| Alta | WOT-2026-010q | Pre-handoff: exigir suite canonica real en last-run.json (level=all + default_discovery) | motor/quality-gates | completed | WOT-2026-010o | session-2026-06-17-suite-performance |  <!-- verificado: motor 849e7d5; guard exige level=all + args_mode=default_discovery; tests barrera 41 passed; suite --level all 2913 passed; validate 0/0; cierre canonico 2026-06-17. -->
| Media | WOT-2026-010l | Selector focal por diff para run_pytest_safe con fail-open a suite canonica | motor/quality-gates | completed | WOT-2026-010j, WOT-2026-010i, WOT-2026-010q | session-2026-06-17-suite-performance |  <!-- verificado: motor 915d2be (selector + fail-open); destino reconciliacion archivado 010i 6de40a4; bus REVIEW_DECISION approve -> CLOSE_CONFIRMED -> SUPERVISOR_CLOSED; suite --level all 2932 passed/20 skipped/0 failed (level=all/default_discovery/sha=915d2be==HEAD); validate 0/0; cierre canonico 2026-06-17. -->
| Alta | WOT-2026-010v | Hardening de encoding guard: detectar control chars <32 no-whitespace | motor/devex-encoding | completed | WOT-2026-010e, WOT-2026-008j | session-2026-06-19-encoding-hardening |  <!-- cerrado canonico 2026-06-19: motor 6e55f86; detecta <32 no-whitespace en CLI + hook sin detector paralelo; 304 focales, suite 3024 passed, validate 0/0 --> |
| Alta | WOT-2026-010w | Hardening de session-close: subprocess utf-8 en closeout_steps para Windows | motor/closeout-runtime | completed | WOT-2026-010v | session-2026-06-19-session-close-blocker |  <!-- cerrado canonico 2026-06-19: motor 99bdae4; encoding="utf-8", errors="replace" en los 3 call sites (support.py:40 run_script, support.py:291 check_versioned_filenames, rotation.py:369 step_git_clean); test de regresion subprocess real FAIL-sin/PASS-con; suite 3026 passed sobre 149d821 (tree-diff vs HEAD solo prompt md inerte); validate 0/0; pusheado 5b59441..99bdae4. --> |
| Alta | WOT-2026-011a | Session-close: fail-closed ante archival-limbo con remediacion auditable (NO auto-commit v1) | motor/collab-hygiene | pending | WOT-2026-010u, WOT-2026-010w | session-2026-06-19-process-debt |  <!-- follow-up estrechado y congelado: 010u ya bloquea el rename sin commit en pre-handoff/validate, pero 011d demostro que --session-close aun puede dejar el limbo y trasladar la contaminacion al ticket siguiente. V1: post-condicion fail-closed en closeout_steps/archival o session_closeout que nombre origen/destino + comando exacto de reconcile. NO auto-commit del archivador en este ticket. --> |
| Alta | WOT-2026-011b | Relaunch timeout determinism: fijar BUILDER_START_VERIFY_TIMEOUT_SECONDS en tests de relaunch | motor/test-suite-perf | pending | - | session-2026-06-19-process-debt |  <!-- ~15 tests de relaunch no overridean BUILDER_START_VERIFY_TIMEOUT_SECONDS (bus/builder_relaunch.py:30 default 20.0s) -> pagan hasta 20s c/u via tasklist/PID liveness en Windows. VERIFICADO: 2 tests x 20s trazados al timeout (collection 0.95s descarta sandbox). La oscilacion 5<->13min es INFERENCIA razonable (no causa raiz cerrada); el fix es correcto independientemente del mecanismo. Patron ya usado para IDLE_TIMEOUT: monkeypatch.setenv(...,"0.5"). Un ticket, ~15 ediciones; suite 5-13min -> ~5min estable. --> |
| Media | WOT-2026-011c | BOM/control-char SOURCE audit: identificar que inyecta BOM+CR-stray en .md (code-spike, sin fix) | motor/devex-encoding | pending | WOT-2026-010v | session-2026-06-19-process-debt |  <!-- recurre 008f/008k/008j/010w. 010v detecta control chars <32 (defensa-en-profundidad) pero la FUENTE que inyecta BOM+CR-stray en .md NO esta verificada (sospechas: PowerShell heredoc, launcher, pre-commit). SPIKE primero: identificar la fuente con evidencia antes de proponer cualquier fix; nace abierto si se salta el spike. Decidir despues si hay fix de fuente o si 010v ya es suficiente. --> |
| Media | WOT-2026-011d | Retirada auditada de 7 stubs de prompts legacy (alias-compat de 008h/010a) | motor/legacy-deprecation | completed | WOT-2026-008h, WOT-2026-010g | session-2026-06-19-legacy-prompts |  <!-- cerrado y aprobado 2026-06-19. motor 28bbe85: lifecycle de prompts derivado desde fuente real, consumidores vivos repointados, 7 stubs retirados con barrera rg pre/post delete. cierre Manager canonico registrado en repo_destino (c71370d) tras resolver el falso 0/0 causado por archival rename pendiente de 010w. --> |
| Alta | WOT-2026-010x | Sustituir gitleaks-action licenciado por CLI OSS en security-audit.yml | motor/ci-security | pending | - | session-2026-06-19-gitleaks-ci |  <!-- follow-up verificado tras push de 467b1c8: .github/workflows/security-audit.yml usa gitleaks/gitleaks-action@v2 y falla por licencia obligatoria + rate limit de API. El warning de Node 20 no bloquea; la causa real es la dependencia del action licenciado. Objetivo: ejecutar gitleaks OSS por CLI en el workflow, sin GITLEAKS_LICENSE y sin depender del runtime JS del action. --> |
| Baja | WOT-2026-010m | Piloto xdist/sharding en CI para subset unitario aislado | motor/ci-performance | pending | WOT-2026-010j, WOT-2026-010k | session-2026-06-17-suite-performance |  <!-- Fase 2, alto riesgo por estado compartido. Objetivo: probar paralelizacion solo en subset unitario puro y demostrar que no pisa .agent, tmp_path, cwd ni locks. No activar por defecto hasta barrera anti state-leak verde. --> 
| Alta | WOT-2026-010n | Gate de deliverables namespaced por delivery_authority para repo_motor/repo_destino | motor/protocol-runtime | completed | WOT-2026-010j | session-2026-06-17-deliverable-gate-bug |  <!-- verificado: motor b355cb0+453967d+c7249b8; bus seq 1140-1150; cierre canonico c5368b4; deliverables namespaced resueltos. -->
| Media | WOT-2026-007e | Plan graph avanzado: paralelismo, shared dependencies y anti-scope | motor/protocol-validation | completed | WOT-2026-007a, WOT-2026-007b | session-2026-06-14-contract-formation |  <!-- motor 1dc5447; plantilla plan_graph dedicada + paralelizable yes/no/after + Merge Regression Audit; checks estructurales ya en validador 007c; enforcement de valores = follow-up tras cierre 007c -->
| Baja | WOT-2026-007g | Validador plan_graph: enforce paralelizable in {yes,no,after} + presencia Merge Regression Audit | motor/quality-gates | completed | WOT-2026-007c, WOT-2026-007e | session-2026-06-15-contract-formation |  <!-- motor ce83621; destino 03efad4+ae5bb67+closeout; validate_plan_graph localiza Paralelizable por header, acepta parallelism_notes separado, exige Merge Regression Audit; cierre canonico manager-approve 0/0 -->
| Baja | WOT-2026-007f | Integracion runtime de CONTRACT_GAP en bus/controller | motor/protocol-runtime | completed | WOT-2026-007c, WOT-2026-007e, WOT-2026-007g | session-2026-06-14-contract-formation |  <!-- motor f5923d7+c5d81ee+5fab636+ece7524; suite independiente 2713 passed; Manager APROBADO; cierre canonico manager-approve; validate 0/0 -->
| Media | WOT-2026-010r | DECISION: mapear skills a user/model-invoked + inventario de consumidores + ruta de migracion | motor/skills-taxonomy | completed | WOT-2026-008b, WOT-2026-010g | session-2026-06-17-mattpocock-v1 |  <!-- ORIGEN EXTERNO (candidate, sin abrir): mattpocock/skills v1.0.0 (release commit 00ff03c; primary change 47bde84; license to verify, likely MIT), docs/invocation.md. deliverable_type: analysis/research (DECIDE, NO migra; cero cambios de codigo). Outputs: (1) mapeo de las 29 skills a user-invoked (disable-model-invocation: true, description humana) vs model-invoked (description con triggers); (2) DISCOVERY CONSUMER INVENTORY: para cada consumidor del campo triggers:, documentar QUE hace con el (discover_skills=construye trigger_map/aliases L109,123; orquestador=dispatch; skill_resolver=filtro/resolucion; check_skill_collisions=unicidad; validate_agent_config=valida; local_audit=audita); (3) DECISION EXPLICITA backward-compat: hibrido (triggers + disable-model-invocation coexisten durante transicion) VS break-glass directo -- recomendacion Manager: hibrido reduce riesgo de regresion en el bus. HALLAZGO VERIFICADO Y CORREGIDO (Manager, 2026-06-17): el campo triggers: tiene 6 consumidores de codigo REALES (scripts/discover_skills.py, check_skill_collisions.py, local_audit.py, orquestador.py, validate_agent_config.py, bus/skill_resolver.py). bus/review_bridge.py NO es consumidor: el grep previo conto la palabra inglesa 'triggers requeue', 0 hits del campo YAML (verificado: fm.get triggers/trigger_map = 0). 'disable-model-invocation' NO existe aun en ninguna skill; test-driven-development ya coexiste triggers:+description:. Matar el trigger YAML NO es migracion de nomenclatura: reescribe el grafo de resolucion del bus. NO mezclar con 010g ni 008d. Adapted NO ported. Inspired by + fila CREDITS al abrir. -->
| Media | WOT-2026-010s | MIGRACION hibrida: disable-model-invocation con paridad de trigger_map | motor/skills-discovery | completed | WOT-2026-010r | session-2026-06-17-mattpocock-v1 |  <!-- ORIGEN EXTERNO (candidate, sin abrir): mattpocock/skills v1.0.0 (release commit 00ff03c; primary change 47bde84; license to verify, likely MIT), docs/invocation.md. deliverable_type: mixed (code). delivery_authority: repo_motor. Aqui se ejecuta la ruta hibrida decidida en 010r, con tests, no por decreto. Migra el mecanismo de resolucion en los 6 consumidores reales: introducir disable-model-invocation sin retirar triggers, hacer que skill_resolver.py + discover_skills.py respeten la semantica user/model-invoked. BARRERA DE REGRESION OBLIGATORIA: test de paridad de trigger_map -- `python scripts/discover_skills.py --json` antes y despues debe producir dispatches funcionalmente equivalentes (mismos trigger->path); el test falla sin el fix. EFECTO SECUNDARIO REQUERIDO (limpieza Goose, coordinar con follow-ups de 010g): discover_skills.py L5 docstring menciona Goose/Claw (DEPRECATED WT-2026-254a) y L555-560 flag --goose itera trigger_map -- ambos deben limpiarse/decidirse al tocar el archivo. Alto riesgo: bus = estado compartido. Forbidden: cambiar resolucion sin test de paridad; mezclar con vocabulario (010t). Depende de 010r. Inspired by + fila CREDITS al abrir. -->
| Media | WOT-2026-010t | Portar vocabulario de diseno (deep module/seam/adapter) al review del Manager | motor/manager-review-rubric | completed | WOT-2026-010r | session-2026-06-17-mattpocock-v1 |  <!-- ORIGEN EXTERNO (candidate, sin abrir): mattpocock/skills v1.0.0 (release commit 00ff03c; primary change 47bde84; license to verify, likely MIT), skills/engineering/codebase-design (deep module, interface, seam, adapter, deletion test, 'the interface is the test surface'). Da al Manager lenguaje de review preciso que se solapa con anti-patrones vivos: zero-logic wrapper (CLAUDE.md), index/inline R-006, Test Util vs Basura. Tambien contrastar diagnosing-bugs (antes diagnose) vs nuestro skills/systematic-debugging (CONSERVAR limite 3 intentos como restriccion de seguridad del motor). deliverable_type: documentation (vocabulario en man-review-implementation/references/review-checklist.md + _shared/anti-patterns.md + nota de uso). GATE ANTI-OVER-ENGINEERING (binario y explicito): demostrar que seam/adapter YA existen en un decision_artifact, NO crear nuevas abstracciones; el vocabulario describe lo que existe, no exige arquitectura nueva. PATRON DE REFERENCIA OBLIGATORIO: incluir un ejemplo concreto del vocabulario aplicado a un decision_artifact EXISTENTE (p.ej. WOT-2026-009b scope_gate: su interface, su seam, su adapter reales) para que el Manager tenga patron, no solo definiciones abstractas. Adapted NO ported. Depende de 010r. Inspired by + fila CREDITS al abrir. -->
| Alta | WOT-2026-010u | Barrera: archivado de colaboracion debe quedar commiteado o el cierre falla | motor/collab-hygiene | completed | WOT-2026-010c | session-2026-06-18-archival-debt |  <!-- PREMISA VERIFICADA (Builder/Manager, 2026-06-18): scripts/archive_collaboration_artifacts.py:119 SOLO MUEVE archivos (sin git add/commit), dejando STRATEGY_/AUDIT_ del ticket cerrado en delete+untracked. La deteccion ya existe pero LLEGA TARDE: contaminacion_productiva se emite en validate/handoff del SIGUIENTE ticket (agent_controller.py:4074, delivery_hygiene_check.py:369, pre_handoff_guard.py:967), no en el cierre que lo causa. PATRON RECURRENTE esta sesion: 3 tickets seguidos bloqueados por archivado sin commitear (010l->010i, 010g->010h, 010t->010s), cada uno requirio reconciliacion manual (git add rename + commit + revalidar). Objetivo: convertir la reconciliacion manual recurrente en barrera automatica. Dos opciones a decidir en el ticket: (A) el archivador hace git add del rename (move como rename trazable) y deja el commit al flujo de cierre; o (B) un guard de cierre/handoff que FALLE si detecta artefactos de archivado en delete+untracked, con diagnostico self-service (el comando exacto de reconciliacion). deliverable_type: mixed (code + test de barrera que falle sin el fix). delivery_authority: repo_motor. Forbidden: borrar artefactos (siempre rename, nunca delete-sin-copia); editar bus manualmente. Barrera verificada: el test debe reproducir el limbo delete+untracked y demostrar que el fix lo evita o lo bloquea. Ver memoria pre-handoff-commit-order y lightweight-workplan-edits-cause-state-drift. -->


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
- **Estado:** completed
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
- **Estado:** completed
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
- **Estado:** completed
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
- **Estado:** completed
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
- **Estado:** completed
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
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008a, WOT-2026-009b
- **Problema:** el manifiesto 008a detecto 29 `SKILL.md` en disco pero solo 28
  skills descubiertas. La causa verificada fue BOM UTF-8 en
  `skills/man-review-implementation/SKILL.md`: `discover_skills.py` no tolera
  BOM y devuelve `NO_FRONTMATTER`, mientras `check_skill_collisions.py` si lo
  tolera. El resultado actual es falso verde: `discover_skills.py --check-contract`
  puede pasar aunque una skill critica quede invisible.
- **Objetivo:** corregir el falso verde de discovery/frontmatter/BOM y cerrar la
  DEC de modelo de registry sin implementar todavia el registry completo, sin
  mover, renombrar ni crear shims.
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
  - documentacion minima del contrato de registry si se adopta registry-first
- **Criterios binarios:**
  - Test reproduce el fallo actual: un `SKILL.md` con BOM no puede desaparecer
    silenciosamente del discovery mientras `--check-contract` queda verde.
  - `discover_skills.py --check-contract` y `check_skill_collisions.py` cubren el
    caso `man-review-implementation`; si una skill con frontmatter roto queda
    invisible, el diagnostico es accionable.
  - Existe una semantica canonica o test de paridad para frontmatter entre
    discovery/collision/contract-check; no quedan parsers operativos con
    comportamiento incompatible sin cobertura explicita.
  - Barrido unico de BOMs historicos en `skills/**/SKILL.md`, prompts relevantes
    y referencias de skill; el resultado queda documentado con rutas exactas.
  - Se aclara la diferencia entre `scripts/check_encoding_guard.py` y cualquier
    script hermano de encoding; si hay inconsistencia CLI, queda corregida o
    ticketizada.
  - DEC de registry resuelta: registry-first explicito, glob recursivo o hibrido,
    con tradeoffs y compatibilidad. Si se adopta registry-first, el contrato
    declara `registry.json` como autoridad logica de API activa/despacho y
    `INDEX.md` como proyeccion generada, nunca como fuente manual.
  - DEC de discovery resuelta: mantener `triggers` como API propia, migrar a
    discovery por `description` estilo Claude, o soportar hibrido. La decision
    declara compatibilidad, coste de migracion y efecto en prompts/skills actuales.
  - Matriz `agents.json` allowlist vs triggers reales de `skills/**/SKILL.md`:
    antes de clasificar ghosts, reparar BOM/discovery y re-ejecutar discovery.
    La lista de triggers se deriva exhaustivamente de las allowlists vivas en
    `.agent/config/agents.json` y del frontmatter real de skills; no se mantiene
    una lista manual. El caso `/review` se trata como `BOM/discovery casualty`
    verificado (`man-review-implementation`) y NO se retira de la allowlist solo
    porque hoy sea invisible.
  - La DEC compara al menos cuatro opciones: registry central, manifest por skill
    (`manifest.json`), `.claude-plugin/plugin.json` compatible y discovery
    recursivo sin manifest.
  - La DEC evalua un esquema minimo de campos: `public_id`, `source`
    (`motor|host`), `canonical_source`, `path`, `trigger`, `role`, `status`
    (`active|deprecated|draft`), `deliverable_types`, `deprecated_by`,
    `compat_until`, `aliases` y, solo si aporta valor demostrado,
    `deliverable_profile`.
  - Registry/manifest rico queda atribuido como diseno propio
    (OKF/CEM/host-extends), no como patron probado por `mattpocock/skills`, que
    solo valida lista explicita de paths.
  - El contrato declara que el registry/manifest define la API publica activa,
    mientras el layout fisico puede contener docs, tests, deprecated o in-progress.
  - El contrato declara como se integra host-first: un posible
    `<repo_destino>/.agent/registry.json` puede extender/overridear el registry
    del motor, pero nunca contaminar `repo_motor`; la precedencia host local sigue
    siendo superior al fallback read-only del motor.
  - La DEC declara si aliases/deprecations se modelan como metadatos logicos del
    registry antes que como archivos shim fisicos; cualquier shim fisico futuro
    requiere evidencia de referencia hardcoded que no pueda resolverse por registry.
  - Aunque se adopte registry-first, hay barrera separada para `SKILL.md` con BOM
    o frontmatter roto, porque el agente aun debe leer semantica on-demand.
  - No hay renames, moves, cambios de trigger, implementacion completa de registry,
    aliases runtime ni shims en 008b.
- **STOP:**
  - Si el fix requiere reorganizar carpetas, abrir 008d; no mezclar.
  - Si el registry introduce fuente de verdad manual no validada, bloquear.
  - Si 008b intenta implementar el registry completo, `agent_controller` dispatch,
    aliases o shims, bloquear y moverlo a 008c/008d.
  - Si la propuesta intenta crear `skills/domain/...` o `prompts/system/...` en
    008b, bloquear y moverlo a 008d tras registry + aliases/shims.

### WOT-2026-008c - Registry/INDEX generado de prompts y skills
- **Prioridad:** Media
- **Scope:** motor/skills-discovery
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008b
- **Problema:** los agentes descubren prompts/skills por memoria, glob o nombres
  humanos. Eso escala mal cuando haya categorias, aliases, shims o deprecated
  entries.
- **Objetivo:** crear un `registry.json` generado/validable como autoridad logica
  de prompts y skills (rutas canonicas, triggers, rol, tipo de artefacto, estado
  activo/deprecated/draft y aliases). El `INDEX.md` es solo una proyeccion generada
  del registry; no una segunda fuente de verdad.
- **Files Likely Touched:**
  - script generador/validador de registry
  - `registry.json` o manifest equivalente generado
  - `skills/INDEX.md` o indice equivalente generado
  - docs de contrato del registry
  - tests
- **Criterios binarios:**
  - `registry.json`/manifest es la autoridad logica validada de API activa;
    `INDEX.md` es proyeccion generada y falla si queda stale.
  - Incluye prompts, skills, templates/references relevantes y scripts consumidores
    declarados por 008a.
  - Incluye owner/source (`motor|host`) y `canonical_source` para distinguir
    extensiones del destino, overrides y componentes canonicos del motor.
  - Distingue API publica, layout fisico, aliases logicos y shims fisicos
    excepcionales.
  - Distingue componentes activos de `deprecated`/`in-progress`/`draft`; presencia
    en disco no implica disponibilidad para agentes.
  - Check de CI/pre-commit o gate local falla si el registry o INDEX generado
    esta stale.
  - El discovery/dispatch que se toque consulta el registry para `active`,
    `deprecated`, `draft` y aliases en vez de inferir solo por presencia en disco.
  - No mueve carpetas ni renombra archivos.
- **STOP:**
  - Si el INDEX exige mantenimiento manual, redisenar.
  - Si se detectan colisiones de trigger/nombre, abrir ticket dedicado antes de
    migrar.
  - Si el registry duplica logica de frontmatter sin test de paridad, bloquear.

### WOT-2026-008d - Convencion de naming de prompts/skills con shims versionados
- **Prioridad:** Media
- **Scope:** motor/skills-taxonomy
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008c
- **Problema:** los prompts usan `snake_case` con orden inconsistente (`review_manager.md`, `launch_builder.md`, `audit_*`) y las skills usan `kebab-case` mayormente dominio/actor primero (`man-review-implementation`, `bui-implement-from-plan`). Renombrar sin decision congelada rompe `source_prompt`, `contract_id`, docs, memoria y agentes externos. Tras 008c no hay `registry.json`: la compatibilidad debe vivir en shims/stubs, frontmatter y checks existentes.
- **Objetivo:** fijar una DEC de convencion de nombres antes de mover nada, aplicar un piloto minimo y atomico, y preservar compatibilidad con shims versionados. La convencion debe cubrir prompts, skills, scripts y artefactos auxiliares, distinguiendo actor/dominio primero vs accion primero por tipo. No hay migracion masiva en este ticket.
- **Decision previa obligatoria:** crear una DEC nueva (por ejemplo `docs/decisions/DEC-008D-001-naming-convention.md`) que primero revalide la premisa contra 010s y congele:
  - prompts: `snake_case`, patron `<domain_or_actor>_<action>_<object>.md` salvo familias historicas justificadas como `audit_*`; decidir explicitamente prefijos de rol (`man_`/`bui_` o `manager_`/`builder_`);
  - skills: `kebab-case`, patron `<domain-or-actor>-<action>-<object>/`;
  - scripts: `snake_case` verbo primero para CLIs (`check_*`, `generate_*`, `validate_*`, `discover_*`, `archive_*`, `run_*`);
  - shims/stubs: formato, ventana de retirada y ticket propietario (`008e`);
  - criterio de legacy permitido y etiquetas de compatibilidad;
  - ortogonalidad entre naming lexico y taxonomia de invocacion `disable-model-invocation` de 010s.
- **Files Likely Touched:**
  - Builder: DEC de naming en `docs/decisions/`
  - Builder: `docs/registry/README.md`
  - Builder: `docs/registry/INDEX.md`
  - Builder: prompts piloto y sus stubs/aliases versionados
  - Builder: skills piloto que referencian esos prompts por `source_prompt`
  - Builder: `scripts/discover_skills.py`
  - Builder: `scripts/run_gates_dispatch.py`
  - Builder: tests de discovery, contract-check, naming, gate-dispatch, collisions e INDEX si aplica
  - Read/inspect only: `scripts/check_skill_collisions.py` salvo DEC explicita, `scripts/check_ticket_nomenclature.py`, `scripts/validate_ticket_prose.py`, `skills/`, `prompts/`
- **Criterios binarios:**
  - Existe DEC congelada de naming antes de cualquier rename.
  - El piloto toca prompt + skill consumidora de forma atomica cuando existe `source_prompt`.
  - `python scripts/discover_skills.py --check-contract` queda verde tras el rename.
  - `python scripts/check_skill_collisions.py` queda verde.
  - Antes del piloto, capturar baseline de `python scripts/discover_skills.py --check-contract`, `python scripts/check_skill_collisions.py` y `python scripts/discover_skills.py --json`; despues del piloto, repetirlos y demostrar paridad salvo renames/aliases declarados en la DEC.
  - El INDEX generado expone `canonical_name`, `legacy_aliases` y `naming_status` o campos equivalentes; la fuente debe ser frontmatter (`legacy_aliases:`) o derivacion por filename en `discover_skills.py`, nunca sidecar JSON ni manifest central.
  - Los nombres legacy quedan como shims/stubs versionados con retirada asignada a `008e`; la DEC define si el shim es alias documental o prompt ejecutable, y como conserva `source_prompt`/`contract_id` sin romper `--check-contract`.
  - `rg` de nombres antiguos solo aparece en shims, docs de deprecacion, changelog/backlog historico o tests de compatibilidad.
  - `discover_skills.py --check-naming` no existe aun: es deliverable de 008d y debe existir antes de cerrar, con test bloqueador fail-closed para un nombre fuera de convencion. Si se crea un script separado (`check_naming_convention.py`) o se extiende `check_skill_collisions.py`, justificar por que no encaja como subcomando de discovery.
  - No se hace migracion masiva; maximo piloto pequeno y reversible. `scripts/run_gates_dispatch.py` invoca `--check-naming` o equivalente decidido por DEC; el handoff debe quedar verde: `pre_handoff_guard` verifica gates frescos y la barrera 010u de archival-rename, pero no debe reimplementar la logica de naming.
  - Tests focales, ruff/format si toca Python, encoding guard, suite canonica y validate 0/0 pasan.
- **Piloto sugerido:** evaluar `prompts/review_manager.md` -> nombre canonico actor/dominio primero solo si se actualiza a la vez `skills/man-review-implementation/SKILL.md:source_prompt` y se conserva stub legacy. Si el analisis muestra mayor riesgo que valor, elegir un piloto documental de menor blast radius.
- **STOP:**
  - Si no hay DEC aprobada, no renombrar.
  - Si un rename rompe `--check-contract`, bloquear y ajustar contrato antes de seguir.
  - Si el piloto exige tocar bus, runtime, dependencias o migracion de carpetas, emitir CONTRACT_GAP.
  - Si la regla requiere gate nuevo, justificar por que no se puede extender un gate existente antes de implementarlo.
  - Si un rename no puede tener shim seguro, requiere aprobacion humana explicita.
  - Si rompe un contrato publicado, aplazar a major/versioned migration.
### WOT-2026-008e - Retirada versionada de aliases/shims y compat legacy
- **Prioridad:** Baja
- **Scope:** motor/skills-taxonomy
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008d
- **Problema:** aliases o shims ayudan a migrar, pero si no tienen retirada
  versionada se convierten en deuda permanente.
- **Objetivo:** retirar aliases legacy y cualquier shim fisico caducado tras
  verificar con escaneo reproducible que no quedan referencias vivas, con changelog
  y rollback claro.
- **Criterios binarios:**
  - `rg` no encuentra consumidores vivos de nombres legacy fuera de changelog/docs
    historicos.
  - Un scan reproducible (por ejemplo `scripts/check_alias_usage.py`) revisa
    backlog, execution logs vivos/archivados, docs y commits recientes configurados
    y confirma 0 usos bloqueantes de aliases/triggers legacy.
  - Registry no lista entradas legacy como activas.
  - Tests de discovery/collision/registry pasan sin aliases legacy ni shims.
  - CHANGELOG documenta retirada y ruta nueva.
- **STOP:**
  - Si cualquier destino activo sigue usando el alias/shim, aplazar y registrar evidencia.

### WOT-2026-008f - Gate de integracion destino-motor y lifecycle operativo
- **Prioridad:** Media
- **Scope:** motor/protocol-destino
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008c
- **Problema:** el ajuste de un `repo_destino` al motor y su preparacion para Git
  estan cubiertos por piezas separadas (`install_agent_system.py`,
  `destination_bootstrap`, `destination-preflight`, `check_destino_publish_ready.py`,
  `audit_git_publication`, `system-health-audit`), pero no existe un gate integrado
  que verifique que el destino quedo engranado de punta a punta.
- **Objetivo:** crear un wrapper/gate de integracion que orqueste checks existentes
  antes de inventar validadores nuevos. Debe validar link motor-destino,
  version/manifest compatible, settings/guard fail-closed, resolucion de registry
  desde contexto destino, estado operativo pre-push y riesgos de publicacion cuando
  aplique.
- **Files Likely Touched:**
  - script wrapper de integracion (nombre a decidir, p.ej. `scripts/check_integration.py`)
  - docs/prompts de lifecycle destino si se decide consolidar router
  - tests del wrapper sobre fixtures motor/destino
- **Criterios binarios:**
  - El wrapper reutiliza checks existentes cuando existan; no duplica logica de
    `classify_publication.py`, `check_destino_publish_ready.py`,
    `destination_context.py` ni settings portability.
  - Valida que `motor_destination_link.json` apunta a un motor con contrato compatible.
  - Verifica que el registry del motor resuelve triggers desde el contexto del destino.
  - Verifica guard/settings fail-closed con fixture o prueba no destructiva.
  - Distingue gate operativo pre-push de auditoria de primera publicacion.
  - Produce diagnostico self-service y exit codes documentados.
- **STOP:**
  - Si el wrapper reimplementa scanners de secretos o validate en vez de delegar, bloquear.
  - Si requiere escribir en repo_destino para probar guard_paths, usar fixture/tmp o
    modo dry-run; no mutar un destino real.

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
- **Estado:** completed
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
- **Estado:** completed
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
- **Estado:** completed
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

---

## WOT-2026-009f -- Gate de publicacion pre-push para repo_destino

- **Prioridad:** Media
- **Scope:** motor/protocol-destino
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-009c (COMPLETED)
- **Incidente de origen:** 0081fb6 (repo_destino, 2026-06-15) -- publico work_plan.md en APPROVED sin alinear execution_log/TURN/STATE; CI fallo con DRIFT: plan=APPROVED pero log=COMPLETED.
- **Problema:** No existe gate mecanica que bloquee un push de repo_destino cuando .agent/collaboration/ tiene drift entre superficies vivas (work_plan, execution_log, TURN, STATE). La unica regla es documental, no ejecutable.
- **Objetivo:** Antes de git push en repo_destino, el validador debe correr automaticamente y bloquear si hay errores. Un estado APPROVED pre-Builder no es publicable a main por defecto.
- **Criterios binarios:**
  - Gate documentada en orchestrator_pipeline.md: "antes de push, correr --validate --json; bloquear si errors > 0".
  - Semantica explicita en AGENTS.md o protocol doc: APPROVED pre-Builder no es publicable aislado.
  - Opcionalmente: script o hook que ejecute validate antes de push en repo_destino.
  - Test o ejemplo que demuestre que 0081fb6-equivalent falla la gate y 9422d6e-equivalent la pasa.
- **STOP:** si la gate mecanica requiere instalar hooks en el repo_destino sin consent del propietario del proyecto, documentar solo y dejar la gate como recomendacion en orchestrator_pipeline.md.


## WOT-2026-010a -- Glosario de nomenclatura + rename de artefactos de ticket

- **Scope:** motor/protocol-docs
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-008b, WOT-2026-009g (no arrancar hasta que ambos cierren; 008b por si descubre mas casos de naming durante su implementacion, 009g por el conflicto de superficie con validate_ticket_prose.py)
- **Origen:** Revision de nomenclatura (2026-06-16). El Manager senalo `audit_plan.md` como nombre ambiguo. Inspeccion de codigo revela deuda mas profunda: dos prefijos en paralelo (`WP-` 161 archivos, `WT-` 72) y uso de "PLAN" tanto para familia como para artefacto de ticket.
- **Decision de nomenclatura (fijada por el propietario):**
  - `WOT-` es el prefijo canonico de ticket (tres letras). `WP-`/`WT-` = legacy historico, SIN migracion masiva.
  - "Plan" se reserva para el plan/familia completo (ej. `WOT-2026-009` = familia). NO para el artefacto de un ticket.
  - `work_plan.md` permanece como contrato operativo del ticket activo (sin cambio).
- **Renames (con alias de compat durante ventana, NO rename brusco):**
  - `PLAN_WT-<ID>.md` -> `STRATEGY_WOT-<ID>.md` (estrategia tecnica del ticket; libera "PLAN" para familia).
  - `AUDIT_WT-<ID>.md` -> `AUDIT_WOT-<ID>.md` (solo prefijo WT->WOT).
  - `prompts/audit_plan.md` -> `prompts/audit_ticket_contract.md` (audita el contrato/plan operativo del ticket ANTES de Builder; nombre preciso para no confundir con review de implementacion, bus, cierre o publicacion).
- **Generadores activos (corregir PRIMERO, antes que consumidores/validadores):**
  Son skills/prompts que CREAN o ENSENAN IDs/artefactos con prefijo viejo. El
  mas peligroso es `skills/man-create-work-plan/SKILL.md:79` (`ID: WP-[YYYY]-[NNN]`):
  si alguien usa esa skill antes de 010a, regenera nomenclatura antigua por la
  puerta principal. VERIFICADO 2026-06-16: el patron `WP/WT/PLAN_WP/PLAN_WT/AUDIT_WT`
  aparece en 23 archivos activos de `skills/` + `prompts/` (NO 7; lista manual
  quedaria incompleta -- usar la gate grep como fuente, no una enumeracion fija).
  Foco prioritario confirmado: `skills/man-create-work-plan/SKILL.md` +
  `references/plan-template.md` / `plan-quality-checklist.md`, `prompts/session_bootstrap.md`,
  `prompts/launch_builder.md`, `skills/deep-research/`, `skills/_shared/ticket-anti-patterns.md`.
- **Orden de ejecucion:** (1) generadores activos -> (2) consumidores/validadores
  -> (3) mantener WP/WT solo como legacy documentado y etiquetado.
- **Criterios binarios:**
  - Glosario canonico creado (en AGENTS.md o doc dedicado): familia/plan / ticket / work_plan.md / STRATEGY_ / AUDIT_ / prefijo WOT / WP-WT legacy.
  - Ningun prompt/template/skill activo genera `WP-[YYYY]`, `WT-[YYYY]`, `PLAN_WP`, `PLAN_WT`, `AUDIT_WT` salvo en seccion marcada explicitamente como legacy/compat.
  - Gate grep de aceptacion: buscar esos patrones en `prompts/`, `skills/`, `scripts/` y clasificar cada hit como `canonical`, `legacy-compat` o `bug`. La gate falla si queda algun hit no clasificado fuera de seccion legacy.
  - Corregir texto del backlog/docs que aun describe el motor como `WP-YYYY-NNN` -> `WOT-YYYY-NNNx` canonico; WP/WT = legacy historico.
  - Renames aplicados con alias de compat; primera linea del alias apunta al nombre nuevo.
  - Referencias canonicas actualizadas: las 2 de `audit_plan` (`orchestrator_pipeline.md`, `orchestrate-pipeline/SKILL.md`) + consumidores de patrones `PLAN_WT-`/`AUDIT_WT-`.
  - Consumidores de codigo a revisar (VERIFICADO 2026-06-16): `scripts/archive_collaboration_artifacts.py`, `scripts/pre_handoff_guard.py`, `bus/review_bridge.py`, `.agent/motor_checkpoint.py`, `scripts/validate_ticket_prose.py`. Los 5 consumen el patron `PLAN_WT-`/`AUDIT_WT-`. `validate_ticket_prose.py` SI entra en scope de 010a (ver STOP de orden).
  - `ruff check .` exit 0; tests focales exit 0; validate destino 0/0.
- **STOP:**
  - NO migrar los 161+72 archivos historicos `WP-`/`WT-` (eso seria otra familia de tickets, no este).
  - NO romper consumidores que esperan los patrones viejos sin alias de transicion.
  - Antes de tocar `scripts/validate_ticket_prose.py`, verificar en preflight que WOT-2026-009g esta cerrado/publicado y que no hay cambios vivos en esa superficie. En 010a SI puede tocarse; el STOP de orden queda levantado por cierre de 009g.
  - Si el rename de `audit_plan.md` rompe el dispatch de skills/prompts, dejar alias y documentar.


## WOT-2026-010e - Encoding early-detection tras escritura de agentes

- **Prioridad:** Media
- **Scope:** motor/devex-encoding
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010c
- **Orden recomendado:** WOT-2026-010c -> WOT-2026-010e -> WOT-2026-010d -> WOT-2026-008d
- **Origen:** En varias sesiones los agentes perdieron tiempo detectando tarde BOM/mojibake en `backlog.md`, artefactos de ticket y ficheros generados. La extension de VS Code ayuda a ediciones humanas, pero no cubre la tuberia real: agentes escribiendo por Write/Edit/MultiEdit, scripts o heredocs.
- **Problema:** `scripts/check_encoding_guard.py` existe y funciona como autoridad de cierre, pero se ejecuta demasiado tarde. El agente puede escribir contenido corrupto y descubrirlo al final del ticket, cuando el coste de reparar y separar scope ya es mayor.
- **Objetivo:** ejecutar una deteccion temprana de encoding justo despues de escrituras nativas de agentes (`Write|Edit|MultiEdit`) sobre archivos texto, con diagnostico self-service y sin convertir el IDE en dependencia. V1 no promete cubrir escrituras hechas dentro de `Bash`/heredocs; esas quedan cubiertas por convencion + guard final.
- **Decision de producto:** no recomendar extension VS Code como infraestructura canonica. Puede ser conveniencia personal, pero el contrato operativo vive en hooks/gates versionados.
- **Arquitectura propuesta:**
  - Mantener `scripts/check_encoding_guard.py` como autoridad de cierre.
  - Anadir un hook autonomo versionado en `scripts/encoding_post_write_hook.py`, invocado desde `.claude/settings.json` en `PostToolUse` para `Write|Edit|MultiEdit`. No extender `native_post_tool_hook.py`.
  - Extraer una constante compartida `TEXT_EXTENSIONS` en `scripts.encoding_guard` para el filtro temprano (`.md`, `.py`, `.json`, `.jsonl`, `.toml`, `.yaml`, `.yml`, `.sh`, `.ps1`, `.txt`, `.xml`). No derivarla de `GLOB_PATTERNS`, que son patrones de rutas, no sufijos.
  - El hook autonomo anade `repo_root` a `sys.path` de forma explicita, extrae paths tolerando schemas `tool_input.file_path`, `tool_input.filePath`, `result.filePath` y variantes futuras razonables, resuelve `repo_destino` cuando exista (`AGENT_PROJECT_ROOT` o `motor_destination_link.json`), filtra solo archivos texto versionables ANTES de invocar el guard y ejecuta el detector in-process importando `scripts.encoding_guard` para evitar latencia de subprocess en Windows.
  - El hook usa subprocess solo como fallback si no puede resolver/importar el modulo interno; ese fallback corre con `cwd=<repo_root>` y entorno `PYTHONIOENCODING=utf-8`.
  - El hook reporta diagnostico accionable al agente con ruta relativa al root correspondiente, severidad (`ERROR`, `WARN`, `INFO`), categoria (`bom`, `mojibake`, `question_mark_corruption`, `skipped`), comando de reproduccion si aplica y una linea `ACTION:` especifica para cerrar el loop en el siguiente turno.
- **Files Likely Touched:**
  - Builder: `.claude/settings.json`.
  - Builder: `scripts/encoding_post_write_hook.py` (nuevo, autonomo).
  - Builder: `scripts/check_encoding_guard.py` / `scripts/encoding_guard.py` para extraer `TEXT_EXTENSIONS` o helper path-friendly; no duplicar detector.
  - Builder: tests unitarios/integracion del hook y del parser de payload PostToolUse.
  - Builder: `AGENTS.md` o doc de convenciones para preferir herramientas Write/Edit sobre heredocs cuando haya contenido no ASCII, y documentar explicitamente que Bash/heredoc no queda cubierto por el hook temprano de v1.
- **Criterios binarios:**
  - `.claude/settings.json` incluye una entrada `PostToolUse` separada para `Write|Edit|MultiEdit` que apunta a `scripts/encoding_post_write_hook.py`, sin romper el `PreToolUse` fail-closed existente ni la entrada `Read|Grep|Glob|WebFetch`.
  - El hook es autonomo: no extiende `native_post_tool_hook.py`, no depende de imports relativos del paquete `hooks`, y prioriza API interna (`scripts.encoding_guard`) con `scripts/check_encoding_guard.py` solo como fallback subprocess; no reimplementa una segunda lista divergente de codepoints sospechosos ni una segunda lista de extensiones texto.
  - Existe `TEXT_EXTENSIONS` compartida en `scripts.encoding_guard` y el hook la usa. Debe incluir al menos `.md`, `.py`, `.json`, `.jsonl`, `.toml`, `.yaml`, `.yml`, `.sh`, `.ps1`, `.txt`, `.xml`.
  - El hook filtra por extension ANTES de llamar al guard; cualquier otra extension se salta sin invocar el guard para evitar falsos positivos en binarios. Ademas, cualquier `UnicodeDecodeError` durante analisis se captura y se transforma en skip diagnostico (`INFO/WARN`), nunca traceback.
  - El hook resuelve `repo_root`. Si usa fallback subprocess, llama al guard con `cwd=<repo_root>` y `PYTHONIOENCODING=utf-8`; el camino principal in-process no debe arrancar otra VM Python por cada escritura.
  - En topologia multi-root, el hook permite paths bajo `repo_motor` y bajo `repo_destino` cuando `repo_destino != repo_root`; resuelve `repo_destino` desde `AGENT_PROJECT_ROOT` o `motor_destination_link.json`.
  - Si el path resuelto queda fuera de ambos roots permitidos, el hook hace skip sin leer el archivo ni bloquear. Si el root parece inesperado, emite `WARN encoding_guard_skipped_outside_allowed_roots`; si es una escritura externa intencionada, emite `INFO` equivalente.
  - Archivo recien escrito con BOM emite `ERROR` inmediatamente con diagnostico self-service y categoria `bom`.
  - Archivo recien escrito con mojibake real (`\u00c3`, `\u00c2`, `\u00e2`, `\ufffd`, etc.) emite `ERROR` inmediatamente con categoria `mojibake`.
  - `question_mark_corruption` tambien es `ERROR`. Skips legitimos son `INFO`; skips por root inesperado son `WARN`.
  - Si el hook usa API interna en vez de subprocess, debe llamar tambien a `has_utf8_bom()`; `find_mojibake()` no detecta BOM porque es byte-level.
  - Cada diagnostico incluye `ACTION:`. Acciones minimas: `bom` -> rewrite as UTF-8 without BOM; `mojibake` -> replace corrupted sequence and prefer Write/Edit with UTF-8 text over shell heredoc for non-ASCII; `question_mark_corruption` -> recover intended character from source/context, do not blindly replace `?`; `encoding_guard_skipped_outside_allowed_roots` -> `VERIFY_ROOTS_IF_UNEXPECTED; otherwise no action required`; `encoding_guard_skipped_no_path` -> `NO_ACTION_REQUIRED; final gates still apply`.
  - Markdown con ASCII limpio pasa.
  - Markdown con Unicode valido que no sea codepoint sospechoso pasa; si se decide politica ASCII-only para docs, debe ser decision separada, no falso positivo accidental.
  - Si el payload PostToolUse no contiene path resoluble, el hook no bloquea por defecto: reporta `encoding_guard_skipped_no_path`, imprime un resumen debug del schema recibido para `Write|Edit|MultiEdit` y deja al cierre canonico capturar problemas.
  - Tests cubren: BOM detectado como `ERROR bom`, mojibake detectado como `ERROR mojibake`, `question_mark_corruption` como `ERROR`, archivo limpio pasa, em-dash legitimo en pipeline completo del hook pasa sin stderr y exit 0, extension no-text skip antes de invocar el guard, payload sin path como `INFO` con `NO_ACTION_REQUIRED` + schema debug, path fuera de roots permitidos como `WARN` o `INFO` segun caso, path bajo `repo_destino` aceptado en multi-root, multiples paths con uno corrupto falla, `UnicodeDecodeError` se convierte en skip diagnostico y no traceback, camino in-process no invoca subprocess, fallback subprocess recibe `cwd=<repo_root>` y `PYTHONIOENCODING=utf-8`, y cada categoria de error/skip incluye `ACTION:`.
  - `python scripts/check_encoding_guard.py <archivos_tocados>` exit 0 al cierre.
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` exit 0, 0 errors.
- **STOP:**
  - No instalar ni declarar extensiones VS Code como requisito del repo.
  - No confiar en `files.autoGuessEncoding`/settings del IDE como garantia de agentes.
  - No meter heredocs largos dentro de `.claude/settings.json`; delegar a script versionado.
  - No intentar interceptar Bash/heredocs en v1; documentar el gap y mantener pre-commit/encoding guard como red final.
  - No extender `native_post_tool_hook.py`; su cadena de imports tiene diferencias test-vs-produccion y debe tratarse como follow-up independiente si se corrige.
  - No bloquear escrituras por no poder parsear payload si el archivo no es identificable; diagnosticar y dejar que la gate final cubra.
  - No duplicar `SUSPICIOUS_CODEPOINTS` en otro modulo sin extraer fuente compartida.
  - No mover la politica de que escrituras se chequean al guard general; el hook decide que paths recientes merecen chequeo extra, pero usa `TEXT_EXTENSIONS` compartida como fuente de verdad de sufijos texto.
  - No ampliar este ticket a saneo masivo de mojibake historico; solo deteccion temprana y convencion.
  - No autocorregir archivos en el hook; `ACTION:` es feedback operable, no mutacion automatica.
  - No convertir skips legitimos en errores; el feedback temprano debe distinguir `ERROR` de encoding real frente a `INFO/WARN` de omision de escaneo.
- **Limitaciones conocidas:**
  - `check_encoding_guard.py` salta tambien el BOM-check para archivos allowlisted porque el bloque allowlist hace `continue` antes de `has_utf8_bom()`. `ALLOWLIST` esta vacio hoy; no corregir en 010e salvo que la implementacion introduzca allowlist.
  - V1 del hook solo cubre herramientas nativas `Write|Edit|MultiEdit`. Escrituras realizadas dentro de `Bash`/heredocs no exponen un path PostToolUse fiable; quedan cubiertas por convencion operacional y por el guard final antes de handoff/commit.
  - Posible follow-up independiente: corregir/import-testear `native_post_tool_hook.py`, cuyo import `from hooks.post_tool_hook` puede comportarse distinto en produccion que en tests.
- **Notas para documentacion canonica posterior:**
  - Frase guia: "Si los agentes escriben el 100% del codigo, la prevencion debe vivir en la tuberia de escritura del agente, no en el editor humano."
  - Relacion con WOT-2026-010c: 010c protege cierre; 010e reduce el coste de llegar a cierre limpio detectando antes.
  - Relacion con WOT-2026-010d: 010e es independiente de lifecycle y puede ejecutarse antes de 010d para bajar friccion operativa.

## WOT-2026-010d - Pausar/reanudar ticket activo con bus canonico

- **Prioridad:** Alta
- **Scope:** motor/protocol-runtime
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010c
- **Orden recomendado:** WOT-2026-010c -> WOT-2026-010e -> WOT-2026-010d -> WOT-2026-008d
- **Origen:** Durante WOT-2026-008c hubo que pausar el ticket para abrir el hotfix WOT-2026-010b. Se hizo a mano con stash path-limited y funciono, pero el estado de pausa vivia en relato + stash, no en bus ni en artefacto recuperable.
- **Problema:** Los seguros actuales protegen handoff/cierre, pero hacen torpe resolver un blocker externo durante una implementacion. Sin estado canonico de pausa, un corte de sesion entre stash y resume deja trabajo oculto y no auditable.
- **Objetivo:** introducir lifecycle minimo `IN_PROGRESS -> PAUSED -> IN_PROGRESS` con razon obligatoria, eventos de bus, artefacto legible, recuperacion fail-closed y bloqueo de cierres incompatibles.
- **Comandos propuestos:**
  - `python .agent/agent_controller.py --pause-ticket <ticket> --reason <texto>`
  - `python .agent/agent_controller.py --resume-ticket <ticket>`
  - `python .agent/agent_controller.py --abort-paused-ticket <ticket> --force --reason <texto>` (contrato/slot v1; si no se implementa, dejar NotImplemented/follow-up explicito)
- **Estado/artefactos canonicos:**
  - `STATE.md`: conserva `ACTIVE_TICKET: <ticket>` y `STATUS: PAUSED`.
  - `TURN.md`: puede pasar a `MANAGER / CREATE_PLAN` para abrir hotfix.
  - Evento bus `TICKET_PAUSED` con reason, repo, dirty surfaces, diff_stat, stash_ref/wip_commit, `bus_last_seq_global`, `ticket_last_seq`.
  - Evento bus `TICKET_RESUMED` tras restauracion completa y validate limpio.
  - Artefacto `repo_destino/.agent/collaboration/paused/<ticket>.json` con: `ticket_id`, `status` (`PAUSED|ABORTED`), `reason`, `timestamp`, `repo`, `changed_paths`, `diff_stat`, `stash_ref` nullable, `wip_commit` nullable, `bus_last_seq_global`, `ticket_last_seq`, `state_snapshot`, `turn_snapshot`, `resume_instructions`, `abort_reason`, `aborted_at`, `aborted_by`.
- **Files Likely Touched:**
  - Builder: `.agent/agent_controller.py`.
  - Builder: `.agent/scope_gate.py` solo si validate necesita reconocer pausas activas.
  - Builder: `scripts/pre_handoff_guard.py`.
  - Builder: tests unitarios/integracion de pause/resume/pre-handoff.
  - Builder: docs/prompts de lifecycle si el contrato requiere documentar comandos.
- **Criterios binarios:**
  - `--pause-ticket` falla si el ticket activo no coincide o falta `--reason`.
  - Antes de stash/commit WIP, captura `changed_paths` + `diff_stat`.
  - Si `changed_paths=[]`, no crea stash y guarda `stash_ref=null`.
  - Si `changed_paths!=[]`, crea stash path-limited/ref estable `pause/<ticket>/<timestamp>` o commit WIP no publicable, y guarda la ref en JSON.
  - `--pause-ticket` emite `TICKET_PAUSED`, escribe `STATE=PAUSED`, actualiza `TURN=MANAGER/CREATE_PLAN` y crea `.agent/collaboration/paused/<ticket>.json` legible.
  - Profundidad v1 = una pausa activa. Si existe `paused/*.json` activo, otro `--pause-ticket` falla con diagnostico self-service.
  - `--resume-ticket` localiza artefacto por ticket, verifica stash/ref resoluble y aplicable, compara `ticket_last_seq` contra ultimo evento actual del ticket, y falla si el ticket recibio eventos posteriores a la pausa.
  - El avance global del bus por otros tickets se permite pero se reporta comparando `bus_last_seq_global`.
  - `--resume-ticket` restaura de forma atomica o falla sin dejar working tree parcialmente mutado.
  - Test de corte: pause -> nueva invocacion/sesion -> detecta pausa activa y no permite abrir/ejecutar otro ticket sin resolverla.
  - `pre_handoff_guard`/mark-ready bloquea si existe pausa activa ajena o pausa corrupta.
  - `validate --json` distingue pausa legitima de drift con diagnosticos `paused_ticket_active`, `paused_ticket_corrupt`, etc.
  - `--abort-paused-ticket`, si entra en v1, exige `--force` + razon y registra evento bus auditable; si queda pospuesto, el JSON ya soporta `status=ABORTED` y campos `abort_reason`, `aborted_at`, `aborted_by`.
  - Tests demuestran pause limpio, pause con dirty tree declarado, no-stash si no hay diff, resume correcto, resume conflictivo fail-closed, bus advance del mismo ticket bloqueado, bus advance de otro ticket reportado, pausa unica, crash/restart y bloqueo de handoff con pausa ajena.
- **STOP:**
  - No implementar pausas anidadas en v1.
  - No usar stash global ni indices `stash@{n}` como fuente de verdad.
  - No crear stashes vacios.
  - No vaciar `ACTIVE_TICKET` durante la pausa.
  - No permitir que `resume` resuelva conflictos automaticamente o deje arbol a medias.
  - No mezclar con la gate `0 failed` de WOT-2026-010c; 010d depende de ella.
  - Si el modelo exige cambiar la state-machine amplia o eventos incompatibles, parar y separar DEC antes de tocar runtime.
- **Notas para documentacion canonica posterior:**
  - Frase guia: "La pausa no es un stash; es un estado canonico recuperable tras corte de sesion, con artefacto legible, bus coherente y resume fail-closed."
  - Relacion con WOT-2026-010c: 010c protege cierres; 010d permite interrumpir implementaciones sin romper esas garantias.
  - Relacion con WOT-2026-008d: 008d debe arrancar despues de 010d si queremos una valvula formal para blockers externos durante cambios de taxonomy/naming.


## WOT-2026-010f - Limpieza/investigacion de checkpoint/review-none

- **Prioridad:** Baja
- **Scope:** motor/protocol-runtime
- **Estado:** completed
- **deliverable_type:** analysis/mixed (analysis si solo se confirma deuda; mixed si hay fix de runtime)
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010c
- **Origen:** Durante la review final de WOT-2026-010c se verifico que HEAD tenia dos tags M3: `checkpoint/review-WOT-2026-010c` y `checkpoint/review-none`. El tag correcto no esta afectado, pero `checkpoint/review-none` sugiere una ruta previa que creo un checkpoint con `plan_id="none"`.
- **Problema:** Un checkpoint con ticket `none` es ruido operativo y puede ocultar drift de bus o de bootstrap si se normaliza. No bloqueo WOT-2026-010c porque la barrera valida el checkpoint del ticket correcto y la suite canonica verde fresca.
- **Objetivo:** investigar el origen de `checkpoint/review-none`, decidir si es artefacto historico unico o ruta viva, y dejar barrera/fix minimo si existe riesgo de repeticion.
- **Criterios binarios:**
  - Inventario de tags `checkpoint/review-*` y evidencia de si `checkpoint/review-none` es unico o reproducible.
  - Si existe ruta viva: test que falle antes y pase despues demostrando que no se crea `checkpoint/review-none` cuando no hay ticket valido.
  - Si es solo historico: documentar decision y limpiar tag solo con evidencia de que no es referenciado por bus/backlog/archive.
  - Confirmar que `checkpoint/review-<ticket>` sigue funcionando.
  - `validate --json` 0/0 tras la accion elegida.
- **Non-goals:**
  - No tocar WOT-2026-010e ni WOT-2026-010d.
  - No reescribir la politica M3 completa.
  - No borrar tags sin verificar referencias vivas.

## WOT-2026-010g - Auditoria y clasificacion de prompts/skills legacy

- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** completed
- **deliverable_type:** analysis/mixed (analysis si solo inventaria; mixed si ajusta aliases/docs)
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010c
- **Origen:** En el cierre de sesion se detectaron artefactos con semantica legacy/deprecated: `prompts/audit_plan.md` como stub alias, `skills/setup-agent-system/references/quickstart-checklist.md` como legacy, Goose/Claw deprecated en `AGENTS.md` y piezas Goose dentro de `skills/refactor-manager/`.
- **Objetivo:** clasificar prompts, skills y referencias antes de mover, archivar o eliminar cualquier pieza legacy.
- **Clasificacion requerida:**
  - `canonical`: fuente viva del motor portable.
  - `alias-compat`: stub o alias necesario para compatibilidad.
  - `legacy-retained`: historia o referencia conservada deliberadamente.
  - `deprecated-removable`: candidato a retirada tras demostrar cero consumidores.
  - `destination-only`: artefacto que pertenece a historia operativa del `repo_destino`, no al motor portable.
- **Reglas:**
  - Si ayuda a instalar/operar cualquier destino, vive en `repo_motor`.
  - Si documenta una sesion/ticket concreto de este destino, vive en `repo_destino`.
  - Si es compatibilidad de nombres antiguos, se conserva como stub/alias hasta que una gate confirme cero consumidores.
  - Si es historia fiel, no se reescribe ni se moderniza.
- **Criterios binarios:**
  - Inventario completo de `prompts/` y `skills/` con estado por archivo o familia.
  - `rg` de consumidores vivos antes de proponer move/delete.
  - Lista de candidatos a mover al `repo_destino` con justificacion `destination-only`.
  - Lista de candidatos a archivar en `repo_motor` con rollback.
  - Cero cambios destructivos sin ticket de follow-up explicito.
  - `validate --json` 0/0 y encoding guard limpio si se modifican docs.
- **Non-goals:**
  - No mover/eliminar archivos en la fase de inventario salvo autorizacion explicita.
  - No migrar referencias historicas `WP-/WT-` ni comentarios de historia fiel.
  - No mezclar con WOT-2026-010e, WOT-2026-010d ni WOT-2026-008d.

## WOT-2026-010i - Hardening de review packet, forbidden surfaces y tests semanticos

- **Prioridad:** Media
- **Scope:** motor/protocol-runtime
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010e, WOT-2026-010q
- **Origen:** La review Manager de WOT-2026-010e detecto cuatro clases de fallo que el contrato describia pero el sistema aun no bloquea con suficiente precision: packet sin commit visible al review, touch de Forbidden Surfaces sin gate automatica, test de fallback con falso verde y bug semantico de campo leido vs campo retornado en _resolve_destino(). NOTA (verificado 2026-06-17): el bug de _resolve_destino() YA esta corregido en encoding_post_write_hook.py:54 (lee `destination_root`); esta linea se conserva como test de regresion que blinda el fix, NO como bug vivo a arreglar.
- **Problema:** El contrato actual detecta estos fallos en review humana, pero demasiado tarde. Falta convertirlos en barreras mecanicas previas al handoff o en tests utiles que fallen exactamente por la semantica equivocada.
- **Objetivo:** endurecer el sistema para que estos fallos de packaging, scope y contrato semantico fallen automaticamente antes de Manager o durante la propia suite focal.
- **Lineas de trabajo:**
  - Gate de Forbidden Surfaces contra diff real: cruzar archivos tocados por el ticket con la seccion Forbidden Surfaces del plan y fallar antes de review/handoff si hay interseccion.
  - Packaging gate en --mark-ready para tickets code y mixed: exigir commit visible del ticket y packet revisable; un dirty tree solo bloquea en transicion de handoff, no durante iteracion normal.
  - Tests semanticos para resolutores/parsers: si una funcion lee destination_root, el test debe afirmar que retorna destination_root, no solo una ruta util cualquiera.
  - Hardening anti-falso-verde para ramas de fallback: los tests deben observar la rama real ejecutada con spy, marcador temporal o efecto verificable, no inferirla indirectamente por entorno.
- **Criterios binarios:**
  - Existe una barrera automatica que falla si el diff toca una ruta declarada en Forbidden Surfaces.
  - --mark-ready o su guard equivalente falla para tickets code y mixed si no hay commit visible del ticket o si el packet no es revisable.
  - Test de regresion (blinda el fix ya hecho): falla si _resolve_destino() volviera a devolver motor_root cuando el link declara destination_root. El fix ya esta en encoding_post_write_hook.py:54; el test impide la regresion futura.
  - Al menos un test de fallback falla si la rama fallback no se ejecuta realmente aunque el test pretenda cubrirla.
  - validate --json y gates del ticket quedan 0/0 al cierre.
- **Non-goals:**
  - No reabrir ni mezclar el cierre funcional de WOT-2026-010e con este hardening.
  - No convertir cualquier dirty tree en bloqueo continuo fuera del handoff.
  - No introducir marcadores runtime permanentes solo para tests si un spy o artefacto temporal verificable basta.
  - No tocar la logica de negocio del hook de encoding salvo lo necesario para exponer barreras de sistema reutilizables.
## WOT-2026-010j - Baseline de performance de suite: durations y hotspots subprocess/git

- **Prioridad:** Media
- **Scope:** motor/test-performance
- **Estado:** completed-via-010n
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010c
- **Origen:** Discusion de 2026-06-17 sobre coste de suite completa. Verificado: `run_pytest_safe.py` ya acepta argumentos focales; `pytest-cache` esta deshabilitado por contrato; `integration`/`slow` apenas reducen la suite. Hipotesis previa al ticket: el coste podria estar distribuido en unitarios y en tests que invocan `subprocess`/`git`; esta hipotesis es INFERENCIA por grep y 010j debe confirmarla o refutarla con medicion, no tratarla como hecho.
- **Problema:** Se proponen optimizaciones como cache, sharding o selector focal sin baseline objetiva. Eso arriesga cambiar el contrato de calidad sin saber donde esta el coste real.
- **Objetivo:** producir un reporte accionable de performance de la suite antes de tocar runtime, gates o politica Builder/Manager.
- **Files Likely Touched:**
  - Builder: `docs/test_performance/test_performance_baseline_WOT-2026-010j.md` en `repo_motor`.
  - Read/inspect only: `scripts/run_pytest_safe.py`, `scripts/run_gates_dispatch.py`, `pytest.ini`, `pyproject.toml`, `tests/`, `.agent/agent_controller.py`.
- **Criterios binarios:**
  - Ejecuta la medicion canonica con `python scripts/run_pytest_safe.py --level all -- --durations=50` o documenta con evidencia por que no fue viable.
  - Reporta tiempo total, top tests lentos, top modulos lentos y peso relativo de `subprocess`/`git` con tiempo observado.
  - Cuenta archivos/tests que usan `subprocess`, `git`, filesystem real, controller/bus y marcas `integration`/`slow`.
  - Clasifica propuestas en: quick wins de tests, cambios de fixtures, cambios de politica de gates, y paralelizacion/CI.
  - Verifica existencia real del reporte en `repo_motor` con lectura o check compatible con el entorno; el encoding guard no sustituye esta verificacion.
  - Recomienda el siguiente ticket ejecutable con evidencia, no por intuicion.
  - `validate --json` 0 errors / 0 warnings al cierre.
- **Non-goals:**
  - No modificar `run_pytest_safe.py`, `run_gates_dispatch.py`, `pytest.ini` ni politica de gates.
  - No activar cache, xdist, sharding ni selector focal.
  - No cambiar tests productivos salvo que sea necesario para generar el reporte y quede justificado.

## WOT-2026-010k - Reducir coste de tests git/subprocess sin cambiar politica de gates

- **Prioridad:** Media
- **Scope:** motor/test-performance
- **Estado:** completed
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010j
- **Origen:** Follow-up condicionado por la baseline de 010j. La medicion real refuto `git/subprocess` como hotspot dominante y senalo que el coste principal vive en tests de filesystem/scan y setup repetido caro.
- **Objetivo:** reducir tiempo de suite atacando hotspots reales de filesystem/scan, setup repetido y fixtures pesadas sin relajar la suite canonica ni cambiar cuando se ejecuta.
- **Criterios binarios:**
  - Solo optimiza tests o fixtures identificados por 010j como hotspots reales de tiempo wall-clock.
  - Prioriza tests de scan/filesystem real, setup repetido y recorridos de arbol grandes antes que `git/subprocess`.
  - Mantiene tests de contrato que validan filesystem real, git real o bus real donde ese comportamiento sea la API observable bajo prueba.
  - Cada fixture nueva o endurecida que sustituya setup caro queda cubierta por al menos un smoke test sin el shortcut, para evitar mock drift o falso-verde.
  - Usa helpers/fixtures realistas o monkeypatch solo donde el test no pretende validar el comportamiento real del subsistema optimizado.
  - Demuestra mejora con medicion antes/despues bajo condiciones comparables del mismo entorno y suite focal verde.
  - No reduce cobertura semantica ni convierte tests utiles en mocks cosmeticos.
- **Non-goals:**
  - No tocar `run_gates_dispatch.py` ni politica Builder/Manager.
  - No introducir cache de resultados pytest.
  - No paralelizar la suite.

## WOT-2026-010l - Selector focal por diff para run_pytest_safe con fail-open a suite canonica

- **Prioridad:** Media
- **Scope:** motor/quality-gates
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010j, WOT-2026-010i, WOT-2026-010q
- **Origen:** `run_pytest_safe.py` ya acepta argumentos focales manuales; falta derivar el subset desde diff/FLT de forma conservadora.
- **Objetivo:** crear un selector focal por diff que proponga tests candidatos para iteracion rapida, con fail-open a suite canonica cuando no pueda demostrar cobertura suficiente.
- **Files Likely Touched:**
  - Builder: `scripts/run_pytest_safe.py` o script/helper nuevo del selector en `repo_motor`.
  - Builder: tests focales del selector en `tests/` segun el modulo elegido (`scope_gate`, `pre_handoff_guard` o helper dedicado).
  - Read/inspect only: `pytest.ini`, `pyproject.toml`, `.agent/agent_controller.py`, `scripts/run_gates_dispatch.py`.
- **Criterios binarios:**
  - Consume diff real o `get_changed_files`/`scope_gate` y produce una lista de tests candidatos reproducible.
  - Si no hay mapeo seguro, si `git diff` falla, si hay cambios en archivos troncales de configuracion (`pyproject.toml`, `pytest.ini`, `.agent/**`) o si el set de tests resuelto es vacio, falla abierto a la suite canonica completa con razon auditable.
  - No sustituye por defecto la suite canonica de handoff hasta que un ticket posterior cambie explicitamente la politica.
  - Incluye tests que demuestran fail-open ante archivos compartidos, cambios en controller/bus/gates, mapeos incompletos, `git diff` con exit code no-cero y resolucion vacia.
  - Documenta como usar el selector con `run_pytest_safe.py -- <subset>`.
- **Non-goals:**
  - No cambiar el contrato de cierre de WOT-2026-010c.
  - No depender de herramientas IA externas ni servicios SaaS.
  - No activar cache de resultados.

## WOT-2026-010m - Piloto xdist/sharding en CI para subset unitario aislado

- **Prioridad:** Baja
- **Scope:** motor/ci-performance
- **Estado:** completed
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010j, WOT-2026-010k
- **Origen:** Paralelizar puede reducir tiempo wall-clock, pero el repo tiene estado compartido sensible (`.agent`, cwd, tmp_path, locks). Debe probarse como piloto aislado, no como cambio por defecto.
- **Objetivo:** evaluar xdist/sharding solo sobre un subset unitario puro y demostrar que no introduce state-leak ni flakiness. La premisa de paralelizacion no arranca hasta leer el reporte final de 010j.
- **Nota de dependencia:** `pytest-xdist` NO esta instalado hoy. Si el piloto sigue adelante, anadir `pytest-xdist` como dependencia de desarrollo forma parte del ticket; si el piloto se descarta, revertir esa dependencia.
- **Criterios binarios:**
  - Define subset piloto aislado y justifica por que es paralelizable; excluye tests que mutan variables de entorno globales, usan `os.chdir()` o leen/escriben en `.agent/collaboration`.
  - Ejecuta comparacion serial vs paralelo con tiempos y resultados, arrancando con `-n 2` para el runner objetivo actual y sin subir el paralelismo sin medicion adicional.
  - Demuestra que no pisa `.agent/collaboration`, tmp runtime, cwd ni locks.
  - Si falla o es flaky, documenta `no-go` sin activar el cambio.
- **Non-goals:**
  - No activar paralelizacion para toda la suite.
  - No modificar la suite canonica local por defecto.
  - No ocultar flakiness bajo retries.

## WOT-2026-010n - Gate de deliverables namespaced por delivery_authority para repo_motor/repo_destino

- **Prioridad:** Alta
- **Scope:** motor/protocol-runtime
- **Estado:** completed
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010j
- **Origen:** session-2026-06-17-deliverable-gate-bug
- **Problema:** `WOT-2026-010j` produjo correctamente un artefacto `analysis` en
  `repo_motor`, pero `check_deliverables_exist.py` valida los deliverables Builder
  solo relativos a `--project-root`. Hoy no resuelve rutas namespaced por
  `repo_motor`/`repo_destino` ni por `delivery_authority`, asi que bloquea tickets
  legitimos con entrega documental en el motor.
- **Objetivo:** corregir el gate de existencia de deliverables para que resuelva
  cada entrada de `Files Likely Touched` segun su namespace y/o `delivery_authority`,
  manteniendo fail-closed cuando la ruta sea ambigua, inexistente o salga de los
  roots permitidos.
- **Files Likely Touched:**
  - Builder: `scripts/check_deliverables_exist.py`
  - Builder: tests del gate de deliverables
  - Builder: docs del gate solo si hace falta explicitar la regla namespaced
  - Read/inspect only: `scripts/scope_gate.py`, `.agent/agent_controller.py`,
    `scripts/pre_handoff_guard.py`, `work_plan.md` y `ticket_contracts.md` de `010j`
- **Criterios binarios:**
  - Un ticket `analysis` con deliverable Builder en `repo_motor` y
    `delivery_authority: repo_motor` pasa el gate cuando el artefacto existe.
  - Un deliverable Builder en `repo_destino` sigue pasando cuando existe.
  - Una ruta namespaced invalida, ambigua o fuera de root falla cerrado con
    diagnostico claro.
  - El gate no trata notas libres ni bullets `Read/inspect only` como deliverables.
  - Existe barrera de regresion que falla sin el fix para el caso real de `010j`.
  - `WOT-2026-010j` puede cerrar sin duplicar el reporte en `repo_destino`.
- **Non-goals:**
  - No duplicar artefactos entre `repo_motor` y `repo_destino` para satisfacer el gate.
  - No convertir el gate en pass-open.
  - No mezclar optimizaciones de runner ni cambios ajenos de politica de closeout.

## WOT-2026-010o - Tests deterministas para evidence-gate real (manager_review_bridge/review_bridge sin acoplar a repo_destino vivo)

- **Prioridad:** Baja
- **Scope:** motor/test-determinism
- **Estado:** completed
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010k
- **Origen:** session-2026-06-17-suite-performance

### Problema

Durante la implementacion de `WOT-2026-010k` (optimizacion de dos hotspots de
filesystem/scan, sin relacion funcional con este hallazgo), una corrida
intermedia de `python scripts/run_pytest_safe.py --level all` mostro 6 fallos
en `tests/test_manager_review_bridge.py` y `tests/test_review_bridge.py`. El
fallo observado fue del tipo:

```
AssertionError: assert ReviewDecision.CHANGES == ReviewDecision.APPROVE
```

con un mensaje de evidence-gate real adjunto, de la forma:

```
[evidence-gate] REJECTED: Ticket WP-2026-072: all changes are
collaboration-only artifacts...
```

Se investigo exhaustivamente para descartar que fuera una regresion
introducida por el diff de `010k` (que solo tocaba
`tests/unit/test_project_scanner.py` y
`tests/unit/test_no_legacy_topology_terms.py`), siguiendo esta secuencia:

1. Se corrio el test fallido en aislamiento -> seguia fallando con el mismo
   mensaje de evidence-gate.
2. Se hizo `git stash` de los cambios de `010k` en `repo_destino` y se
   re-corrio -> seguia fallando. Esto descarto que el propio diff de
   `010k` en `repo_destino` (ediciones de `work_plan.md`/`execution_log.md`)
   fuera la causa.
3. Se uso `git worktree add /tmp/baseline-check <commit-pre-010k>` para
   probar el commit baseline (anterior a cualquier cambio de la sesion) en un
   working tree aislado -> el test PASO ahi. La diferencia clave: ese
   worktree aislado no tenia el archivo
   `.agent/config/motor_destination_link.json` (gitignored, local-only) que
   resuelve `destination_root` al `repo_destino` real de esta maquina.
4. Se revirtio temporalmente el contenido de los archivos de test +
   `bus/` en el checkout real (que SI tiene el link al `repo_destino` real) a
   sus versiones del commit baseline -> el test seguia fallando igual.
5. Se restauraron los archivos de test a su version de HEAD -> el test volvio
   a pasar cuando se re-corrio con el `repo_destino` real en un estado de git
   estable (sin cambios uncommitted productivos pendientes).

Conclusion: el fallo NO es una regresion de codigo introducida por `010k`.
Es un acoplamiento de entorno preexistente: estos tests no mockean el
evidence-gate, lo ejercitan de verdad contra el `repo_destino` real
resuelto via `motor_destination_link.json`. Su resultado (`APPROVE` vs
`CHANGES`) depende de si ese `repo_destino` real tiene, en el momento exacto
de la corrida, cambios git uncommitted que el evidence-gate clasifique como
"collaboration-only" o como "productivos". Como ese estado fluctua durante
una sesion de trabajo activa sobre el propio `repo_destino` (exactamente lo
que estaba ocurriendo en paralelo durante `010k`), el resultado del test
fluctua con el, sin que el codigo bajo prueba haya cambiado.

### Objetivo

Hacer que `test_manager_review_bridge.py` y `test_review_bridge.py` validen
la logica real del evidence-gate (que es valiosa y no debe debilitarse) sin
depender del estado de git del `repo_destino` real de quien ejecuta la
suite. La fixture debe construir o simular un estado de repo controlado
(por ejemplo un repo git temporal en `tmp_path` con commits/diffs
preparados deliberadamente) en vez de resolver
`motor_destination_link.json` hacia un repo_destino vivo y mutable.

### Files Likely Touched

- Builder: `tests/test_manager_review_bridge.py`
- Builder: `tests/test_review_bridge.py`
- Builder: fixture/helper nuevo de repo git temporal si se decide esa via
  (ubicacion a definir por el Builder, p.ej. `tests/conftest.py` o un modulo
  de fixtures compartido existente)
- Read/inspect only: `bus/review_bridge.py`, `bus/manager_review_bridge.py`
  (o los modulos reales que implementan el evidence-gate; confirmar nombre
  exacto en Fase 0 de diagnostico), `.agent/config/motor_destination_link.json`
  (NO editar; es local-only y gitignored, solo sirve para entender el
  mecanismo de resolucion que hay que desacoplar en el test)

### Criterios binarios

- Los tests de evidence-gate en ambos archivos pasan de forma reproducible
  sin importar el estado git real (uncommitted o no) del `repo_destino` de
  quien ejecuta la suite.
- Existe al menos un fixture/test que demuestra el caso `APPROVE` (cambios
  solo collaboration-only) y al menos uno que demuestra `CHANGES` (cambios
  productivos detectados), ambos contra el repo simulado, no contra el
  repo_destino real.
- Correr la suite completa dos veces en el mismo checkout, con el
  `repo_destino` real en dos estados git distintos entremedio (por ejemplo
  con y sin un archivo nuevo sin commitear), produce el mismo resultado en
  estos tests las dos veces.
- No se relaja la logica real del evidence-gate: el test sigue ejercitando
  el codigo de produccion real (`bus/review_bridge.py` o equivalente), solo
  cambia la fuente del estado de repo que ese codigo inspecciona.
- `ruff check`, `pytest-safe` (suite completa) y
  `validate --json --project-root <repo_destino>` en 0/0 al cierre.

### Non-goals

- No mover ni redefinir el contrato canonico del evidence-gate
  (`bus/review_bridge.py` o equivalente); este ticket es de determinismo de
  test, no de cambio de politica de revision.
- No tocar `.agent/config/motor_destination_link.json` ni su mecanismo de
  resolucion en produccion; el fix vive en la capa de test/fixture.
- No mezclar con `WOT-2026-010k` (hotspots de filesystem/scan, ya cerrado) ni
  reabrir su scope.

### STOP

- Si desacoplar el test del `repo_destino` real exige cambiar la firma o el
  contrato publico de `bus/review_bridge.py` (no solo su fixture de test),
  detener y evaluar si esto debe ser un ticket `code` mas amplio en vez de
  un ticket de test-determinism.
- Si el repo git temporal en `tmp_path` no puede reproducir fielmente la
  senal real que el evidence-gate necesita (por ejemplo dependencias de
  configuracion global de git no disponibles en sandbox), documentar el
  blocker concreto en vez de forzar un mock que vacie el test de contenido
  real.

## WOT-2026-010p - Medir varianza de run_pytest_safe --level all y aislar outliers inestables

- **Prioridad:** Baja
- **Scope:** motor/test-performance
- **Estado:** completed
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010o
- **Origen:** session-2026-06-17-suite-performance

### Problema

Durante `WOT-2026-010o`, una corrida `python scripts/run_pytest_safe.py
--level all` tardo `42m47s`, frente a los `~28min` observados durante
`WOT-2026-010k`. El diff de `010o` fue una linea en un test y no toca runner,
CI, cache ni codigo productivo, por lo que el aumento no puede asumirse como
regresion del ticket sin medicion adicional. Tampoco debe ignorarse: una
varianza de este tamano erosiona la utilidad del cierre canonico.

### Objetivo

Medir la varianza real de `run_pytest_safe --level all` con evidencia
reproducible, usando `--durations=50` en corridas repetidas, para distinguir
entre carga/entorno, I/O inestable, tests que compiten por estado temporal o
nuevos hotspots reales. El ticket produce diagnostico y recomendacion; no
optimiza ni cambia politica de gates.

Tambien debe documentar la regla operativa observada en `010o`: suites directas
con duracion esperada menor de 10 minutos se ejecutan en foreground; background
queda reservado para tareas asincronas largas con polling fiable y evidencia de
progreso. Esta regla evita confundir tiempo real de pytest con espera del agente.

### Files Likely Touched

- Builder: `docs/test_performance/test_performance_variance_WOT-2026-010p.md`
- Builder: `INTERACTION_MODES.md` o `AGENTS.md` solo para documentar la regla
  foreground/background, escogiendo la superficie canonica existente
- Builder: `.agent/collaboration/execution_log.md`
- Read/inspect only: `scripts/run_pytest_safe.py`, `pytest.ini`,
  `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`,
  `docs/test_performance/test_performance_followup_WOT-2026-010k.md`

### Criterios binarios

- Ejecuta al menos dos corridas comparables de
  `python scripts/run_pytest_safe.py --level all -- --durations=50`, o documenta
  un STOP si el coste total impide completar ambas en una sesion razonable.
- Cada corrida registra tiempo wall-clock total, `exit_code`, `tested_commit_sha`
  y top-50 de `--durations`.
- El reporte compara si los mismos tests dominan ambas corridas o si el top
  cambia sustancialmente.
- La recomendacion final clasifica el problema como `entorno/I-O`,
  `test inestable`, `nuevo hotspot verificable` o `no concluyente`, con
  evidencia.
- Documenta la regla foreground/background en una superficie operacional
  canonica: suite esperada <10 min en foreground; background solo para tareas
  largas con polling/progreso verificable.
- No toca `run_gates_dispatch.py`, `scripts/run_pytest_safe.py`, cache pytest,
  xdist ni politica de cierre.
- `validate --json --project-root <repo_destino>` termina 0/0.

### Non-goals

- No optimizar tests en este ticket.
- No activar cache, xdist, sharding ni selector focal.
- No usar la medicion para bloquear retroactivamente `010o` si su diff y gates
  propios son correctos.

## WOT-2026-010q - Pre-handoff: exigir suite canonica real en last-run.json

- **Prioridad:** Alta
- **Scope:** motor/quality-gates
- **Estado:** completed
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010o
- **Origen:** session-2026-06-17-suite-performance

### Problema

La review de `WOT-2026-010o` detecto un gap de contrato en el handoff:
`pre_handoff_guard.py` valida que `last-run.json` este terminado, tenga
`exit_code == 0` y `tested_commit_sha == HEAD`, pero no valida que la corrida
sea realmente la suite canonica completa. Una corrida focal reciente puede
dejar `last-run.json` fresco y verde, y desbloquear `--mark-ready` aunque el
contrato del ticket exija `python scripts/run_pytest_safe.py --level all`.

El caso adversarial no es teorico: un `last-run.json` con `level="unit"` y
`args_mode="explicit_args"` puede ser fresco respecto a HEAD y tener exit 0.
Tambien hay que bloquear el caso `level="all"` con args explicitos, porque
`python scripts/run_pytest_safe.py --level all -- tests/unit/test_x.py` no es
la suite canonica aunque declare nivel `all`.

### Objetivo

Endurecer el pre-handoff para que "fresh green" signifique suite canonica real:

- `status == "finished"`
- `exit_code == 0`
- `tested_commit_sha == HEAD`
- `level == "all"`
- `args_mode == "default_discovery"`

Si cualquiera de esas condiciones falla, `--pre-handoff`/`--mark-ready` debe
bloquear con diagnostico self-service que indique que hay que ejecutar la suite
canonica completa desde `repo_motor`.

### Files Likely Touched

- Builder: `scripts/pre_handoff_guard.py` o el modulo real que implementa
  `_check_canonical_suite_fresh_green` (confirmar ruta exacta en Fase 0)
- Builder: `tests/test_pre_handoff_guard.py`
- Builder: `AGENTS.md` o `QUICKSTART.md` solo si hace falta documentar la
  semantica estricta de "suite canonica"
- Read/inspect only: `scripts/run_pytest_safe.py`, `.agent/agent_controller.py`,
  `prompts/launch_builder.md`

### Criterios binarios

- Un `last-run.json` con `level="unit"`, `status="finished"`, `exit_code=0` y
  `tested_commit_sha==HEAD` bloquea el handoff.
- Un `last-run.json` con `level="all"` pero `args_mode="explicit_args"` bloquea
  el handoff.
- Un `last-run.json` con `level="all"`, `args_mode="default_discovery"`,
  `status="finished"`, `exit_code=0` y `tested_commit_sha==HEAD` permite el
  handoff si el resto de gates estan satisfechos.
- El diagnostico de bloqueo nombra la causa concreta (`not_full_suite` o
  equivalente) y la remediacion: ejecutar `python scripts/run_pytest_safe.py
  --level all` sin argumentos explicitos de test.
- No cambia `run_pytest_safe.py`, no cambia politica de runner y no relaja
  ningun gate existente.
- `ruff check`, tests focales de pre-handoff y `validate --json --project-root
  <repo_destino>` terminan verdes.

### Non-goals

- No implementar selector focal.
- No agrupar gates ni cambiar el flujo Manager.
- No optimizar tiempos de suite.
- No tocar xdist/cache/sharding.

### STOP

- Si el guard canonico vive en otro modulo distinto al esperado, ajustar el FLT
  antes de tocar codigo.
- Si el fix requiere cambiar el esquema de `last-run.json`, detener y abrir un
  contrato mas amplio; `010q` debe consumir campos ya existentes.

## Filas CREDITS candidatas (sin pegar aun)

> Convencion `CREDITS.md`: una fila por ticket que adopta una idea externa; el
> humano decide cuando pegarla. Estas filas quedan PREPARADAS aqui y se mueven a
> `CREDITS.md` (raiz del `repo_motor`) cuando se abra el ticket que adopta la idea.
> Origen: release `mattpocock/skills v1.0.0` (2026-06-17, SHA `dcfc232`, MIT),
> accedido via `gh`. Influencia previa: `mattpocock-skills@1.0.0`.

Para WOT-2026-010s (cuando se migre el mecanismo de resolucion y se adopte de verdad la taxonomia; 010r solo decide y no adopta aun):

```
| WOT-2026-010s | [mattpocock/skills@mattpocock-skills@1.0.0](https://github.com/mattpocock/skills/tree/mattpocock-skills%401.0.0) | User-invoked vs model-invoked skill taxonomy (`disable-model-invocation` + description audience split), from `docs/invocation.md` | MIT | Adapted (concept only; our frontmatter/discovery model, no bundle/deps imported) |
```

Para WOT-2026-010t (cuando se porte el vocabulario de review):

```
| WOT-2026-010t | [mattpocock/skills@mattpocock-skills@1.0.0](https://github.com/mattpocock/skills/tree/mattpocock-skills%401.0.0) | Deep-module design vocabulary (module/interface/seam/adapter/depth, deletion test, "interface is the test surface"), from `skills/engineering/codebase-design` | MIT | Adapted (review-rubric vocabulary only, no code copied) |
```

## Refinamientos verificados para 010r/s (Manager, 2026-06-17)

Auditoria adversarial de 3 recomendaciones (via `prompts/audit_agent_output.md`). Resultado tras verificar contra el codigo:

- **Inventario de consumidores reproducible (REC#1, VALIDA con scope):** el grep
  manual produjo el falso positivo 7->6 (review_bridge.py). 010r debe documentar
  su inventario con un COMANDO REPRODUCIBLE citado literalmente
  (`grep -rn 'fm.get("triggers")\|trigger_map' scripts/ bus/`), no un grep ad-hoc.
  010r es analysis/cero-codigo: NO implementa un script (eso seria mixed). Si la
  decision concluye que hace falta una GATE PERMANENTE de consumidores, se
  materializa en 010s (ya es codigo) o follow-up. No existe hoy herramienta
  dedicada; `graphify` podria responderlo pero no es gate.
- **Decision hibrido/break-glass documentada (REC#2, VALIDA, mecanismo ya existe):**
  010r DEBE registrar la estrategia elegida + trade-offs + implicacion para 010s
  en el decision_artifact del Manager y en la seccion `Decision Arquitectonica`
  del work_plan. NO hace falta plantilla nueva: el decision_artifact
  (`decision_WOT-<ID>.json`) ya es el canal canonico.
- **Preflight de existencia de entregable (REC#3, RECHAZADA - ya existe):** la
  premisa "un analysis puede cerrar sin producir artefacto" es FALSA hoy.
  `scripts/run_gates_dispatch.py:152` corre `check_deliverables_exist.py` para
  documentation/research/analysis/mixed (exit 1 si falta el deliverable declarado
  en FLT). Barrera viva, verificada. NO se anade a 010r (seria duplicar gate).
  Sub-matiz real (NO blocker de 010r): ese check valida EXISTENCIA, no CONTENIDO;
  la barrera de contenido para analysis vive en review_bridge (deliverable_type
  =analysis), no en check_deliverables_exist. Follow-up de otra naturaleza si
  alguna vez se quiere validar contenido minimo.

## Segunda auditoria adversarial (Manager, 2026-06-17) -- 2 refinamientos + 1 mejora nueva

Verificado en codigo tras pasada de revision:

- **REC#1, salvedad de rigor:** "comando reproducible citado" en markdown es
  evidencia manual, no barrera automatica. Para no quedar en reproducibilidad
  nominal, el MANAGER-REVIEW de 010r debe EJECUTAR el comando una vez y registrar
  exit code + conteo en `execution_log.md`. La automatizacion (gate permanente)
  sigue siendo 010s.
- **REC#2, gate ya vive (refuerza, no anade):** `scripts/validate_ticket_prose.py`
  (regla TP-PROSE-10, lineas 399-413) ya FALLA si falta la seccion
  `## Decision Arquitectonica`. Por tanto 010r no "exige" nada nuevo: solo debe
  USAR esa seccion existente para documentar la decision hibrido/break-glass +
  trade-offs + implicacion para 010s. El `decision_artifact`
  (`bus/decision_parser.py:39`, consumido por review_bridge:2193) es distinto de
  `DEC-*` de contract formation; no confundir.
- **MEJORA NUEVA -- Impact Simulation faltante (--check-contract):** VERIFICADO:
  `scripts/run_gates_dispatch.py:157` corre `discover_skills.py --check-contract`
  (validacion bidireccional prompt<->skill: source_prompt/contract_id/ancla
  inversa) INDEPENDIENTE de deliverable_type. Implicacion: si 010r decide
  rename/adopcion de skills mattpocock, 010s tocara frontmatter
  (source_prompt/contract_id) y DEBE mantener `--check-contract` verde.
  Accion: SERIALIZAR 010r -> 010s (no paralelo) y declarar `--check-contract`
  como gate que 010s no puede romper. Citar en el plan de 010s.

Aprendizaje reusable: antes de proponer "exigir X en un ticket", grep el motor.
Patron recurrente esta sesion (7->6 consumidores, _validate_host_project_prefix,
F1 010g, 2 de 3 REC, y ahora TP-PROSE-10 + --check-contract): el motor ya tiene
mas barreras vivas de las que parece; el valor esta en confirmar cuales existen
antes de construir otra.
### WOT-2026-008g - DEC de vocabulario y naming por rol
- **Prioridad:** Media
- **Scope:** motor/skills-taxonomy
- **Estado:** completed
- **deliverable_type:** documentation
- **Depende de:** WOT-2026-008f, WOT-2026-008d, WOT-2026-008e
- **Objetivo:** congelar una DEC documental que separe backends IA, roles y artefactos; documentar supervisor como runtime; formalizar la regla actor/family para naming futuro.
- **Criterio de salida:** DEC-008G-001 + AGENTS.md actualizados, sin renames ni frontmatter, `discover_skills.py --check-naming` verde y validate 0/0.
### WOT-2026-008h - Rename versionado de 5 prompts orchestrator con shims
- **Prioridad:** Alta
- **Scope:** motor/skills-taxonomy
- **Estado:** completed
- **deliverable_type:** mixed
- **Depende de:** WOT-2026-008g
- **Objetivo:** renombrar `launch_builder.md`, `session_bootstrap.md`, `session_close_chat.md`, `destination_bootstrap.md` y `refactor_bootstrap.md` a sus nombres `orchestrator_*`, manteniendo compatibilidad con stubs y actualizando consumidores vivos.
- **Criterio de salida:** los 5 prompts canonicos nuevos existen, los 5 nombres viejos quedan como stubs, `source_prompt` y consumidores vivos apuntan al nombre canonico, `INDEX.md` y `MANIFEST.distribute` quedan alineados, `--check-naming` + `validate --json` verdes.
### WOT-2026-008k - Formalizar role: auditor en frontmatter de skills auditoras
- **Prioridad:** Alta
- **Scope:** motor/skills-taxonomy
- **Estado:** completed
- **deliverable_type:** mixed
- **Depende de:** WOT-2026-008g
- **Objetivo:** formalizar 
ole: auditor en las skills que son propiedad real del rol auditor, sin renombrar directorios ni mezclar prompts audit_* de familia transversal.
- **Cierre:** cerrado canonico 2026-06-18 (motor fba7a39); role expuesto separado de owner; CONTRACT_OPT_IN_ROLES incluye auditor; suite 3012 passed; validate 0/0.
- **Criterio de salida:** skills auditoras con 
ole: auditor, discovery/catalog/index alineados, pruebas de contract/discovery verdes, validate --json 0/0 y sin tocar bui-self-audit, prompts ni runtime.


| Alta | WOT-2026-008i | Rename atomico de 4 skills manager a manager-* | motor/skills-taxonomy | completed | WOT-2026-008g, WOT-2026-008e, WOT-2026-008h, WOT-2026-008k | session-2026-06-18-role-naming |  <!-- cerrado canonico 2026-06-19: motor b230b61; rename atomico de 4 skills manager-*, trigger_map byte-identico, suite 3013 passed, validate 0/0 --> |
| Alta | WOT-2026-008j | Rename atomico de 4 skills builder a builder-* | motor/skills-taxonomy | completed | WOT-2026-008g, WOT-2026-008h, WOT-2026-008i, WOT-2026-008k | session-2026-06-19-role-naming |

---

## Movido por WOT-2026-012a (corte de 011j ya completed)

Fila de tabla retirada de la cola viva:

| Alta | WOT-2026-011j | Corregir fuente BOM en writer PowerShell y preparar regeneracion limpia de 012a | motor/devex-encoding | completed | WOT-2026-011c | session-2026-06-19-011c-followup | - |

Ficha retirada de la cola viva:

### WOT-2026-011j - Corregir fuente BOM en writer PowerShell y preparar regeneracion limpia de 012a
- **Prioridad:** Alta
- **Scope:** motor/devex-encoding
- **Estado:** completed
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

---

## Traza del corte: ### WOT-2026-012a (conservada integra por contrato)

Copia integra de la ficha del ticket que ejecuto este corte, preservada en el
historico como exige el criterio binario de T-012A-001.

### WOT-2026-012a - Reestructurar backlog: cola viva vs historico + formato parseable
- **Prioridad:** Alta
- **Scope:** system/collab-hygiene
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_destino
- **Depende de:** -.
- **Reactivation:** -.
- **Supersede / Merge decision:** absorbe el objetivo de `WT-2026-250c`.
  Decision `011e <-> 010m` ya tomada: `keep-both-with-boundary`.
  `011e` queda acotado a runner local opt-in sobre subset unitario;
  `010m` conserva el piloto CI/xdist aislado. `011e` no puede congelarse en
  `work_plan.md` si su contrato vuelve a invadir el alcance CI de `010m`.
- **Origen:** session-2026-06-19-backlog-contract.
- **Deuda explicita fuera de scope:** el BOM/mojibake preexistente del propio scripts/launch_agent_terminals.ps1 NO se sanea en WOT-2026-012a; queda como follow-up de WOT-2026-011f (normalizacion de .gitattributes / line endings / PS1 source encoding).
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


---

## Movido por cierre canonico posterior de WOT-2026-012a

Fila retirada de la cola viva:

| Alta | WOT-2026-012a | Reestructurar backlog: cola viva vs historico + formato parseable | system/collab-hygiene | completed | - | session-2026-06-19-backlog-contract | - |

---

## Movido por cierre canonico WOT-2026-012b (COMPLETED 2026-06-20)

| Media | WOT-2026-012b | Gate check_backlog_contract.py sobre cola viva | motor/quality-gates | pending | WOT-2026-012a | session-2026-06-19-backlog-contract | - |

---

## Movido por cierre canonico WOT-2026-011b (COMPLETED 2026-06-21)

| Alta | WOT-2026-011b | Relaunch timeout determinism: fijar BUILDER_START_VERIFY_TIMEOUT_SECONDS en tests de relaunch | motor/test-suite-perf | completed | - | session-2026-06-19-process-debt | - |

### WOT-2026-011b - Relaunch timeout determinism en tests de relaunch
- **Prioridad:** Alta
- **Scope:** motor/test-suite-perf
- **Estado:** completed
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

## Movido por cierre canonico WOT-2026-013a (COMPLETED 2026-06-21)

| Media | WOT-2026-013a | Test de integracion fragil (test_approved_pending) por drift de topologia sandbox (fix test-only) | motor/test-robustness | completed | - | session-2026-06-20-hermes-audit | - |

### WOT-2026-013a - Test de integracion fragil (fix test-only)
- **Prioridad:** Media
- **Scope:** motor/test-robustness
- **Estado:** completed
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
- **Objetivo:** hacer el fixture robusto -> usar AGENT_PROJECT_ROOT real o PYTHONPATH en vez de copiar
  `agent_controller.py` al sandbox, de modo que el test falle solo ante un bug real del controller.
  `--validate-topology` queda explicitamente fuera de scope en `013a` y solo podria salir como follow-up separado
  si el fix test-only no bastara.
- **Files Likely Touched:**
  - repo_motor: `tests/test_controller_integration.py`
- **Criterios binarios:** el test falla SIN el fix solo ante bug real (no por fixture); pasa CON el fix tanto
  aislado como en suite; barrera de regresion que demuestre la diferencia; ruff + run_pytest_safe --level all
  0 failed; validate 0/0.
- **STOP:** si robustecer el fixture exige tocar `.agent/agent_controller.py`, anadir `--validate-topology` o
  reescribir la arquitectura de sandbox fuera del propio test, parar y abrir follow-up separado en vez de ampliar
  scope.
- **Depende de:** -.
- **Descartado de la auditoria de Hermes (ruido, NO accionar):** H-05 settings.json permissions.allow
  (FALSO: el archivo real no lo tiene, guard de portabilidad pasa); H-03/H-06/H-11 (conocidos por diseno);
  confusion motor-vs-destino (artefacto de su clon shallow Linux sin destino).

## Movido por cierre canonico WOT-2026-011g (COMPLETED 2026-06-21)

| Media | WOT-2026-011g | Prompts/politica: explicitar 'loop rapido' vs 'cierre canonico' | motor/protocol-docs | completed | WOT-2026-010c, WOT-2026-010q | session-2026-06-19-improvement-backlog | - |

### WOT-2026-011g - Politica explicita de loop rapido vs cierre canonico
- **Prioridad:** Media
- **Scope:** motor/protocol-docs
- **Estado:** completed
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Reactivation:** -
- **Origen:** session-2026-06-19-improvement-backlog.
- **Problema (VERIFICADO):** la politica de `loop rapido` (reruns focales, checks locales, evidencia diagnostica) frente a `cierre canonico` (suite canonia en HEAD, `validate 0/0`, handoff con eventos reales y cierre Manager) existia repartida entre prompts y docs, pero no quedaba declarada de forma corta y consistente.
- **Objetivo:** dejar una politica explicita y consistente de `loop rapido` vs `cierre canonico` en prompts/documentacion del motor, sin tocar tooling ni gates.
- **Files Likely Touched:**
  - repo_motor: `prompts/orchestrator_launch_builder.md`
  - repo_motor: `prompts/manager_review.md`
  - repo_motor: `prompts/orchestrator_pipeline.md`
  - repo_motor: `QUICKSTART.md`
- **Criterios binarios:** existe una seccion explicita que nombre ambos modos y delimite que evidencia vale para cada uno; `orchestrator_launch_builder.md`, `manager_review.md`, `orchestrator_pipeline.md` y `QUICKSTART.md` quedan alineados; ningun texto tocado permite presentar pytest focal, wall-clock en background o tests verdes aislados como sustituto de suite canonica / handoff / cierre; no se tocan scripts, gates ni codigo; `check_encoding_guard.py` sobre los docs tocados y `validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si para mantener la documentacion veraz hace falta tocar tooling productivo, parar y abrir follow-up de codigo en vez de ampliar `011g`.
- **Depende de:** WOT-2026-010c, WOT-2026-010q.

| Alta | WOT-2026-013b | Hacer parallel-safe `test_project_root_resolution.py` antes de promover xdist por defecto | motor/test-suite-hygiene | absorbed | WOT-2026-011e, WOT-2026-010m | session-2026-06-21-pipeline-prep | WOT-2026-011i |  <!-- absorbed por 011i; premisa familia-unica refutada (CG-WOT-2026-013b.md FINAL) -->

### WOT-2026-013b - Hacer parallel-safe `test_project_root_resolution.py` antes de promover xdist por defecto
- **Prioridad:** Alta
- **Scope:** motor/test-suite-hygiene
- **Estado:** absorbed (premisa refutada; ver CG-WOT-2026-013b.md FINAL)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011e, WOT-2026-010m
- **Reactivation:** -
- **Origen:** session-2026-06-21-pipeline-prep.
- **Problema (VERIFICADO):** el `CG-WOT-2026-013b.md` refuto la premisa original de "3 tests". El rojo xdist reproducido son 11-12 fallos inestables, 11 de ellos concentrados en `tests/unit/test_project_root_resolution.py`, con firma dominante `ImportError: runtime.project_root not in sys.modules` al usar `importlib.reload()` sobre un modulo global compartido. El problema real es la falta de parallel-safety de ese archivo, no la politica del runner.
- **Objetivo:** volver `tests/unit/test_project_root_resolution.py` parallel-safe para que `python scripts/run_pytest_safe.py --level unit --xdist-workers auto` quede verde sin tocar runner, CI, `--dist loadscope`, default xdist ni codigo productivo en `runtime/`.
- **Files Likely Touched:**
  - repo_motor: `tests/unit/test_project_root_resolution.py`
- **Criterios binarios:** la Fase 0 deja en `execution_log.md` el conteo, los nombres y la firma `not in sys.modules`, confirmando que la familia real es `test_project_root_resolution.py`; el diff productivo queda acotado a ese archivo y deja de depender de `importlib.reload()` sobre un modulo global compartido; `python scripts/run_pytest_safe.py --level unit --xdist-workers auto` queda verde y estable en >=2 corridas seguidas; existe demostracion FAIL-sin/PASS-con sobre el rojo real; `python -m pytest tests/unit -q`, `ruff check tests/unit/test_project_root_resolution.py`, `uv run ruff format --check tests/unit/test_project_root_resolution.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si la unica via verde exige tocar `scripts/run_pytest_safe.py`, `--dist loadscope`, la politica default xdist, workflows o `pre_handoff_guard.py`; si el rojo reproducido deja de ser mayoritariamente `test_project_root_resolution.py`; o si volver el archivo parallel-safe exige tocar `runtime/project_root.py`, parar y emitir `CG-WOT-2026-013b.md`.

- **Cierre:** absorbed por WOT-2026-011i. El rojo xdist del subset unit es contencion de reparto cross-archivo (no determinista 12<->37 en 3 corridas), no una familia de tests aislable; la solucion (`--dist loadscope`) pertenece al runner y vive en 011i.

| Media | WOT-2026-011i | Default xdist + `--dist loadscope` para `--level unit` | motor/test-suite-perf | not-pursued | WOT-2026-011e, WOT-2026-010m | session-2026-06-19-improvement-backlog | - |  <!-- not-pursued: loadscope no estabiliza; 3 tests con estado global no aislables por xdist (CG-WOT-2026-011i.md) -->

### WOT-2026-011i - Default xdist + `--dist loadscope` para `--level unit` (absorbe 013b)
- **Prioridad:** Media
- **Scope:** motor/test-suite-perf
- **Estado:** not-pursued (opt-in 011e+010m es el estado final; ver CG-WOT-2026-011i.md)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011e, WOT-2026-010m
- **Reactivation:** -
- **Origen:** session-2026-06-19-improvement-backlog.
- **Problema (VERIFICADO):** `011e` resolvio el opt-in local y `010m` cerro el piloto CI sin contaminar el cierre canonico. `013b` (absorbido aqui; ver `CG-WOT-2026-013b.md`) demostro con 3 corridas que el rojo del subset unit bajo xdist NO es una familia de tests aislable: con reparto por defecto (`--dist load`) el conteo oscila 12<->37 y el archivo dominante cambia entre corridas identicas (cada archivo pasa aislado bajo `-n 8`). Es contencion de reparto cross-archivo, propiedad del runner. La via verde es `--dist loadscope` (agrupa por archivo), que es justo lo que 013b tenia prohibido tocar. Por eso 013b se absorbe y la politica de reparto vive aqui.
- **Objetivo:** convertir `python scripts/run_pytest_safe.py --level unit` en un camino xdist por defecto, AUDITABLE y ESTABLE, usando `--dist loadscope` para eliminar la contencion cross-archivo demostrada por 013b; preservando `--level all` serial, respetando args explicitos y manteniendo un escape estable a serial (`--xdist-workers 1`).
- **Files Likely Touched:**
  - repo_motor: `scripts/run_pytest_safe.py`
  - repo_motor: `tests/unit/test_run_pytest_safe.py`
- **Criterios binarios:** `python scripts/run_pytest_safe.py --level unit` habilita xdist por defecto CON `--dist loadscope` y metadata estable en `last-run.json`; el subset unit queda verde y ESTABLE en >=3 corridas seguidas (refutando el no-determinismo 12<->37 que documento 013b); `python scripts/run_pytest_safe.py --level unit --xdist-workers 1` conserva un camino serial auditable; `python scripts/run_pytest_safe.py --level all` sigue serial; la barrera `tests/unit/test_run_pytest_safe.py` protege el nuevo default, el modo loadscope y el escape a serial; `python -m pytest tests/unit/test_run_pytest_safe.py -q`, `ruff check scripts/run_pytest_safe.py tests/unit/test_run_pytest_safe.py`, `uv run ruff format --check scripts/run_pytest_safe.py tests/unit/test_run_pytest_safe.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si activar el default unitario exige tocar CI, `pre_handoff_guard.py`, el dispatcher o cambiar la semantica de `--level all`; si no existe un escape serial estable con el CLI actual; o si `--dist loadscope` NO estabiliza el subset unit (sigue habiendo rojo no determinista), parar y emitir `CG-WOT-2026-011i.md`.

- **Cierre:** not-pursued. La Fase 0 refuto la premisa loadscope (3 corridas: 3->1->3 failed, set variable). Los 3 flakes (test_upgrade_path_suggestion, test_scan_current_project, test_no_inline_ticket_regex) pasan serial y dependen de estado global del proceso (cwd/git/escaneo), no aislable por politica de reparto xdist. Solucion suficiente: opt-in local (011e) + piloto CI (010m). Follow-up opcional: robustecer esos 3 tests (no contratado).

| Alta | WOT-2026-011h | Barrera de archivado tambien en mark-ready | motor/collab-hygiene | completed | WOT-2026-011a, WOT-2026-011d | session-2026-06-19-improvement-backlog | - |  <!-- completed: motor 79d6a1c (fail-closed en mark-ready ante archive_rename_uncommitted); manager APPROVE 8aa7ca4 -->

### WOT-2026-011h - Barrera de archivado tambien en mark-ready
- **Prioridad:** Alta
- **Scope:** motor/collab-hygiene
- **Estado:** completed (motor 79d6a1c; manager APPROVE)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011a, WOT-2026-011d
- **Reactivation:** -
- **Origen:** session-2026-06-19-improvement-backlog.
- **Problema (VERIFICADO):** `011a` ya cerro fail-closed la ruta de `--session-close` ante `archive_rename_uncommitted`, pero `--mark-ready` sigue auto-archivando `PLAN_/AUDIT_` cerrados desde `.agent/agent_controller.py` y puede dejar el mismo limbo `D old + ?? new` para que el Manager lo reconcilie a mano despues del handoff. La razon estable y la remediacion ya existen; falta cerrar el mismo hueco en el camino de handoff.
- **Objetivo:** hacer que `--mark-ready` falle cerrado cuando su auto-archivado deje `archive_rename_uncommitted`, reutilizando el mismo diagnostico estable y sin introducir auto-commit del archivador.
- **Files Likely Touched:**
  - repo_motor: `.agent/agent_controller.py`
  - repo_motor: `tests/test_agent_controller.py`
  - repo_motor: `tests/test_pre_handoff_guard.py`
  - repo_motor: `tests/unit/test_scope_gate.py`
- **Criterios binarios:** `--mark-ready` bloquea con razon estable `archive_rename_uncommitted` si su auto-archivado deja limbo; el diagnostico conserva origen, destino y remediacion exacta; el caso limpio sigue dejando `READY_FOR_REVIEW` sin falso positivo; existe al menos una barrera FAIL-sin/PASS-con sobre la ruta real de `--mark-ready`; `python -m pytest tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py -q`, `ruff check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `uv run ruff format --check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si la unica forma de cerrar el hueco es auto-commitear el archivador; si la deteccion solo puede expresarse como `dirty tree` generico y no como `archive_rename_uncommitted`; o si reproducir la mutacion real exige tocar `--session-close` otra vez en vez de la ruta de handoff, parar y emitir `CG-WOT-2026-011h.md`.

- **Cierre:** completed. `--mark-ready` ahora falla cerrado ante el limbo `D old + ?? new` del auto-archivado, reutilizando el detector estable `archive_rename_uncommitted` sin auto-commit. Barrera FAIL-sin/PASS-con (test directo del helper + 3 e2e). Suite --level all 3086 passed; validate 0/0; bus CLOSE_CONFIRMED->COMPLETED.

| Alta | WOT-2026-013c | Robustecer 3 tests global-state para ejecucion paralela | motor/test-suite-hygiene | blocked-final | WOT-2026-011e, WOT-2026-010m | session-2026-06-21-post-011h-followup | - |  <!-- blocked-final: cura exige tocar rglob de producto o romper invariante sandbox (CG-WOT-2026-013c.md); sucesor = ticket de producto -->

### WOT-2026-013c - Robustecer 3 tests global-state para ejecucion paralela
- **Prioridad:** Alta
- **Scope:** motor/test-suite-hygiene
- **Estado:** blocked-final (CG-WOT-2026-013c.md; cura en superficie de producto)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011e, WOT-2026-010m
- **Reactivation:** -
- **Origen:** session-2026-06-21-post-011h-followup.
- **Problema (VERIFICADO):** `011i` cerro como `not-pursued` la via de runner/default: los 3 tests persistentes `test_upgrade_path_suggestion`, `test_scan_current_project` y `test_no_inline_ticket_regex` pasan serial y siguen ligados a estado global del proceso/repo (`cwd`, git y escaneo del proyecto vivo). La deuda real ya no es de politica xdist, sino de higiene de tests.
- **Objetivo:** volver esos 3 tests parallel-safe sin tocar `scripts/run_pytest_safe.py`, CI ni el default xdist. El entregable es de aislamiento de tests; cualquier recuperacion futura del default se decide despues, con evidencia nueva.
- **Files Likely Touched:**
  - repo_motor: `tests/unit/test_detect_version.py`
  - repo_motor: `tests/unit/test_project_scanner.py`
  - repo_motor: `tests/unit/test_no_inline_ticket_regex.py`
  - repo_motor: `tests/conftest.py`
- **Criterios binarios:**
  - Los 3 tests citados quedan verdes en serial y tambien verdes juntos bajo `python -m pytest <triple> -q -n 8 --dist load`.
  - El diff productivo queda acotado a superficies de test/fixture; no toca runner, CI, controller ni codigo de producto.
  - Existe al menos una barrera FAIL-sin/PASS-con sobre el rojo real de concurrencia/estado compartido.
  - `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q`, `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q -n 8 --dist load`, `ruff` sobre Python tocado, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si cualquier fix exige tocar `scripts/run_pytest_safe.py`, `quality-gates.yml`, `runtime/`, controller o codigo de producto; si al corregir esos 3 aparece otra familia roja dominante bajo xdist; o si la reproduccion deja de estar anclada en estos tests y pasa a ser deuda de runner otra vez, parar y emitir `CG-WOT-2026-013c.md`.

- **Cierre:** blocked-final via CG-WOT-2026-013c.md. Causa raiz: el rglob de producto (scripts/project_scanner.py, agent_system/scripts/project_paths.py) recorre tests/sandbox/session_<PID> volatil y scandir explota antes del filtro ya-existente. Tests-only no basta: la alternativa solo-conftest (sandbox fuera) volvia verde el triple xdist estable x3 pero rompia test_windows_safe_temp_runtime (10 failed en --level all). Sucesor recomendado: ticket de PRODUCTO acotado a escaneo robusto ante borrados concurrentes (os.walk con poda, o ignorar FileNotFoundError).


## Movido por cierre canonico WOT-2026-013d (COMPLETED 2026-06-21)

| Alta | WOT-2026-013d | Escaneo robusto de proyecto ante borrados concurrentes | motor/project-scan | completed | WOT-2026-013c | session-2026-06-21-013c-product-followup | - |

### WOT-2026-013d - Escaneo robusto de proyecto ante borrados concurrentes
- **Prioridad:** Alta
- **Scope:** motor/project-scan
- **Estado:** completed (motor e251bd7; manager APPROVE)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013c
- **Reactivation:** -
- **Origen:** session-2026-06-21-013c-product-followup.
- **Problema (VERIFICADO):** `013c` demostro que el rojo xdist no nace en una familia aislable de tests, sino en el escaneo de PRODUCTO: `scripts/project_scanner.py` hace `rglob("*.py")` en `_collect_local_modules()` y `rglob("*")` en `scan_project()`, mientras `agent_system/scripts/project_paths.py` hace `rglob(".agent")` en `resolve_paths()`. Los tres recorridos pueden descender a `tests/sandbox/test_runtime/session_*` mientras otros workers borran subarboles, provocando `FileNotFoundError`/`Acceso denegado` antes del filtro de exclusion. Baseline verificado: `tests/sandbox/test_runtime` contiene `session_dirs=566`.
- **Objetivo:** volver robusto el escaneo de proyecto ante borrados concurrentes y ruido de sandbox volatil, sin tocar la politica del runner ni reabrir el default xdist. El entregable es producto + barreras de test que demuestren que el triple rojo historico queda estable bajo xdist.
- **Files Likely Touched:**
  - repo_motor: `scripts/project_scanner.py`
  - repo_motor: `agent_system/scripts/project_paths.py`
  - repo_motor: `tests/unit/test_project_scanner.py`
  - repo_motor: `tests/test_project_paths.py`
  - repo_motor: `tests/unit/test_detect_version.py`
  - repo_motor: `tests/unit/test_no_inline_ticket_regex.py`
  - repo_motor: `tests/conftest.py`
- **Criterios binarios:** los 3 puntos de escaneo verificados (`scripts/project_scanner.py` en `_collect_local_modules` y `scan_project`, `agent_system/scripts/project_paths.py` en `resolve_paths`) quedan robustos frente a subdirectorios que desaparecen durante la travesia; existe limpieza determinista del ruido en `tests/sandbox/test_runtime`, gestionada via fixture/harness en `tests/conftest.py` (el sandbox es efecto colateral controlado, no superficie de edicion manual), y el baseline/post queda registrado en `execution_log.md`; `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` queda verde en al menos 3 corridas consecutivas sobre el mismo host; `python -m pytest tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py -q`, `ruff` sobre Python tocado, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes; el diff productivo queda acotado a escaneo de producto + tests/fixtures declarados, sin tocar runner, CI ni default xdist.
- **STOP:** si la unica cura segura exige tocar `scripts/run_pytest_safe.py`, `quality-gates.yml`, CI o la politica default/opt-in de xdist; si la unica forma de estabilizar el triple verde exige mover el sandbox fuera del arbol o romper la invariante custodiada por `tests/unit/test_windows_safe_temp_runtime.py`; o si la reproduccion deja de concentrarse en las superficies declaradas y reaparece como deuda de runner/global-state ajena, parar y emitir `CG-WOT-2026-013d.md`.

- **Cierre:** completed. `scripts/project_scanner.py` y `agent_system/scripts/project_paths.py` sustituyen los `rglob` crudos por recorridos robustos con poda previa del sandbox volatil; `tests/conftest.py` limpia huerfanos `session_<PID>` al inicio; el triple xdist quedo verde en 3 corridas consecutivas y `run_pytest_safe.py --level all` cerro `3091 passed, 20 skipped, 0 failed` sobre `e251bd7`. Cierre canonico confirmado por bus (`REVIEW_DECISION`, `READY_TO_CLOSE`, `CLOSE_CONFIRMED`, `COMPLETED`, `SUPERVISOR_CLOSED`).



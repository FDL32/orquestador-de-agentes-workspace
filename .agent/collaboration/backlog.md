# Backlog

> Tickets candidatos y planes futuros del workspace.
> No es estado activo: el ticket activo vive en `work_plan.md`.
> Al arrancar un item, se convierte en `work_plan.md`; al cerrarlo, pasa a `CHANGELOG.md`.
> Auditoria 2026-06-09: la tabla "Vista rapida" y las fichas largas se
> reconciliaron contra `CHANGELOG.md`; las fichas conservan contexto historico,
> pero su campo `Estado` no debe contradecir el resumen.
> En esta pasada, `absorbed` tambien cubre follow-ups retirados del backlog
> activo por limpieza documental: no estan pendientes y solo deben reabrirse si
> aparece evidencia nueva.
> Cuando una fila historica no tiene ficha larga propia y un ticket posterior ya
> absorbio su alcance, la tabla rapida se toma como autoridad suficiente para
> cerrarla documentalmente.

## Politica
- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â repo destino real que sirve para desarrollar el motor.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â repo portable con `.git` propio.
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
| Baja | TBD | guard_paths: proteger archivos de estado del workspace | system | absorbed | WT-2026-182 | session-2026-05-30 |
| Baja | TBD | BUILDER_STARTED liveness | system | absorbed | - | session-2026-05-29 |
| Baja | TBD | Flag manual --reset-circuit-breaker | system | absorbed | - | CB-RESET-01 |
| Media | WT-2026-182 | Integracion Repomix para Contexto y Repo-Compare | system/skills | completed | - | session-2026-05-30 |
| Alta | WT-2026-183 | Resiliencia ante Supervisor muerto en CHANGES | system/bus | completed | WT-2026-182 | session-2026-05-30 |
| Baja | WT-2026-181 | Migracion nomenclatura WP->WT + Plan como epica | system/meta | completed | WP-2026-179 | session-2026-05-30 |
| Media | WT-2026-184 | Scaffold de PROJECT.md para repositorios destino | system/templates | completed | WT-2026-183 | session-2026-05-30 |
| Media | WT-2026-185 | Knowledge Layer: Glosario + Microagent + skill_resolver | system/knowledge | completed | WT-2026-184 | session-2026-05-31 |
| Alta | WT-2026-186 | Idempotencia del instalador y contrato de rutas gestionadas | system/install | completed | WT-2026-185 | session-2026-05-31-audit |
| Alta | WT-2026-198 | Idempotencia del instalador y contrato de rutas gestionadas | system/install | absorbed | WT-2026-185 | session-2026-06-01-reopen |
| Critica | WT-2026-199 | Claim atomico de requeue y verificacion de Builder vivo | system/supervisor | completed | WT-2026-198 | session-2026-06-01-hotfix |
| Alta | WT-2026-200 | Launcher/supervisor: resume sin supervisor fresco | system/launcher | absorbed | WT-2026-199 | session-2026-06-01-followup |
| Media | WT-2026-201 | Hardening runtime del launcher tras WT-2026-200 | system/launcher | completed | WT-2026-200 | session-2026-06-01-followup |
| Alta | WT-2026-187 | Portabilidad Modelo B y limpieza legacy | system/portability | completed | WT-2026-186 | session-2026-05-31-audit |
| Media | WT-2026-188 | Modularizacion progresiva de agent_controller.py | system/architecture | completed | WT-2026-187 | session-2026-05-31-audit |
| Alta | WT-2026-189 | Guard anti doble lanzamiento de Builder tras CHANGES | system/bus | completed | WT-2026-187 | session-2026-05-31-hotfix |
| Alta | WT-2026-190 | Rotacion segura de review_queue.md y contrato de memoria | system/hygiene | completed | WT-2026-189 | session-2026-06-01-memory |
| Alta | WT-2026-196 | Manager adaptativo ante blockers repetidos | system/review | completed | WT-2026-190 | session-2026-06-01-review-loop |
| Alta | WT-2026-191 | Migracion determinista de memoria y bootstrap real | system/memory | completed | WT-2026-196 | session-2026-06-01-memory |
| Media | TBD | Inventario y estabilizacion de suite global | system/testing | absorbed | WT-2026-208 | session-2026-06-01-suite |
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
| Alta | WT-2026-215 | Gates Modelo B: operaciones git de tooling resuelven motor_root | system/gates-motor-root | completed | WT-2026-210 | session-2026-06-02-bridge-diff |
| Alta | WT-2026-217 | Pre-check de packaging usa la ruta canonica de transicion al emitir CHANGES | system/bus-transition | absorbed | WT-2026-210 | session-2026-06-02-precheck-transition |
| Baja | WT-2026-213 | Eliminar el doble STATE_CHANGED de --mark-ready | system/bus-events | absorbed | WT-2026-210 | session-2026-06-02-bus-audit |
| Media | WT-2026-206 | Scope gate y cierres manuales en workspace+motor | system/hygiene | absorbed | WT-2026-211 | session-2026-06-02-followup |
| Media | WT-2026-207 | Gobernanza de collaboration legacy en el motor durante session-close | system/hygiene | absorbed | WT-2026-211 | session-2026-06-02-closeout |
| Alta | WT-2026-208 | Estabilizacion de suite global tras transicion workspace+motor | system/testing | completed | WT-2026-211 | session-2026-06-02-suite |
| Media | TBD | Alinear tests legacy de pre-handoff con auto-commit motor-aware | system/testing-hygiene | absorbed | WT-2026-208 | session-2026-06-06-suite-baseline |
| Baja | WT-2026-209 | Sustituir nomenclatura Modelo B por estandar workspace+motor | system/docs | absorbed | WT-2026-232a | session-2026-06-02-terminology |
| Baja | TBD | Repomix falla en Windows por permisos Node.js/globby | system/devx | absorbed | WT-2026-182 | session-2026-05-31 |
| Media | TBD | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip 26.1.2 | system/security-dependencies | absorbed | - | session-2026-06-07-security-followup |
| Media | TBD | Renombrar en sitio 8 tests historicos del motor a nombres funcionales estables | system/testing-hygiene | absorbed | WT-2026-215 | session-2026-06-05-portability |
| Media | WT-2026-218 | Regenerar y commitear memory_rules.md en el motor | system/memory | absorbed | - | session-2026-06-02-memory-bootstrap |
| Media | WT-2026-219 | Bootstrap de memoria garantizado en destinos nuevos | system/memory | absorbed | WT-2026-218 | session-2026-06-02-memory-bootstrap |
| Media | WT-2026-220 | Flujo de promocion upstream de memoria para dogfooding | system/memory | absorbed | WT-2026-219 | session-2026-06-02-memory-bootstrap |
| Alta | WT-2026-221a | Relaunch CEM: root verificado y capsula evidence-linked para Builder | system/agent-launch | completed | WT-2026-208 | session-2026-06-03-builder-autonomy |
| Alta | WT-2026-221b | Manager evidence gate: rechazar review sin bus activo y evidencia minima | system/review-gates | completed | WT-2026-208 | session-2026-06-03-builder-autonomy |
| Media | WT-2026-221c | Scope watch temprano contra Files Likely Touched | system/scope-gate | absorbed | WT-2026-208 | session-2026-06-03-builder-autonomy |
| Media | WT-2026-222 | Higiene de suite: reset determinista del cache de project_root entre tests | system/testing-hygiene | completed | WT-2026-208 | session-2026-06-03-suite-hygiene |
| Alta | WT-2026-223a | Parser central de ticket IDs y contrato de nomenclatura | system/ticket-naming | absorbed | WT-2026-221a | session-2026-06-04-plan-grammar |
| Alta | WT-2026-224a | Supervisor relaunch guard: no spawnear round nuevo con Builder vivo | system/supervisor-relaunch | completed | WT-2026-221a, WT-2026-221b | session-2026-06-04-overlap-guard |
| Alta | WT-2026-225a | Durable projection catch-up cuando el bus va por delante | system/projection-reconcile | completed | WT-2026-214, WT-2026-216, WT-2026-224a | session-2026-06-04-projection-catchup |
| Alta | WT-2026-226a | Unificar evidence seam entre mark-ready y review packet | system/evidence-packaging | completed | WT-2026-221b, WT-2026-225a | session-2026-06-04-evidence-seam |
| Media | WT-2026-227a | Repomix: estado estructurado y diagnostico verificable en review context | system/review-context | completed | WT-2026-182, WT-2026-226a | session-2026-06-04-repomix-observability |
| Alta | WT-2026-228a | Pre-handoff bloquea cambios productivos sin commit en repo_motor | system/pre-handoff-evidence | completed | WT-2026-226a, WT-2026-227a | session-2026-06-04-prehandoff-evidence |
| Alta | WT-2026-229a | Cierre de sesion portable: motor agnostico e historico al destino | system/session-closeout-portability | completed | WT-2026-228a | session-2026-06-05-portable-closeout |
| Alta | WT-2026-230a | Bootstrap de destino: mapa compacto local y arranque guiado desde motor_root | system/destination-bootstrap | completed | WT-2026-184, WT-2026-186, WT-2026-187, WT-2026-215, WT-2026-227a | session-2026-06-05-destination-bootstrap |
| Alta | WT-2026-231a | Pre-handoff commitea repo_motor en topologia motor/destino con scope FLT | system/pre-handoff-commit | completed | WT-2026-228a, WT-2026-215 | session-2026-06-05-builder-commit |
| Alta | WT-2026-232a | mark-ready motor-aware y protocolo portable de topologia motor/destino | system/mark-ready-motor-aware+terminology-builder-bootstrap | completed | WT-2026-231a, WT-2026-226a, WT-2026-215, WT-2026-209 | session-2026-06-05-mark-ready-motor-aware |
| Media | WT-2026-233a | Reapertura humana controlada de tickets terminales | system/bus-recovery | completed | WT-2026-232a | session-2026-06-06-terminal-reopen |
| Media | WT-2026-233b | Idempotencia de Manager tras cierre y reapertura terminal | system/bus-recovery | completed | WT-2026-233a | session-2026-06-06-terminal-reopen-followup |
| Baja | WT-2026-233c | Coleccion aislada de test_manager_approve | system/testing-hygiene | completed | WT-2026-233b | session-2026-06-06-manager-test-isolation |
| Media | WT-2026-234a | Cierre de sesion portable y cuarentena de artefactos con IDs de ticket | system/session-closeout-portability | completed | WT-2026-229a, WT-2026-233c | session-2026-06-06-portability-closeout |
| Critica | WT-2026-235a | Manager review bridge: decisiones autoritativas y CHANGES con blockers | system/review-bridge-decision-contract | completed | WT-2026-204, WT-2026-234a | session-2026-06-07-review-bridge |
| Media | WT-2026-236a | Smoke repo-compare con Orca y SOUL.md para validar flujo externo | system/research-devx | completed | WT-2026-182, WT-2026-227a, WT-2026-235a | session-2026-06-07-repo-compare-smoke |
| Alta | WT-2026-237a | Formalizar fixes de motor emergentes del smoke repo-compare | system/review-closeout-hardening | completed | WT-2026-235a, WT-2026-236a | session-2026-06-07-repo-compare-followup |
| Media | WT-2026-238a | Cierre de sesion y handoff documental post WT-2026-237a | system/session-closeout-hygiene | completed | WT-2026-237a | session-2026-06-08-handoff |
| Alta | WT-2026-239a | Separar protocolo de cierre para tickets documentation vs code | system/documentation-closeout-protocol | absorbed | WT-2026-238a | session-2026-06-08-doc-closeout-followup |
| Media | WT-2026-243a | Cierre de sesion documental, snapshot local y memoria de arranque | system/session-closeout-hygiene | completed | WT-2026-242c | session-2026-06-09-closeout |
| Alta | WT-2026-244a | Formalizar policy de mergeabilidad y review inspirada por FrontierCode | system/review-quality-policy | completed | WT-2026-243a | session-2026-06-09-frontiercode |
| Alta | WT-2026-245a | Cerrar gaps residuales de prefijos de tres letras en bus y review bridge | system/ticket-prefix-compatibility | completed | - | session-2026-06-09-prefix-compat |
| Alta | WT-2026-245b | Corregir checkpoint M3 en topologia Model B entre pre-handoff y mark-ready | system/model-b-checkpoint-topology | completed | WT-2026-245a | session-2026-06-09-model-b-checkpoint |
| Alta | WT-2026-245c | Centralizar el patron canonico de ticket ID en Python y PowerShell | system/ticket-id-pattern-centralization | completed | WT-2026-245b | session-2026-06-09-ticket-id-centralization |
| Alta | WT-2026-246a | Endurecer guard M3 y clarificar recuperacion del Builder | system/mark-ready-m3-hardening | completed | WT-2026-245c | session-2026-06-10-m3-hardening |
| Alta | WT-2026-246b | Idempotencia del closeout del launcher y guard autoritativo post-success | system/launcher-closeout-idempotency | completed | WT-2026-246a | session-2026-06-10-launcher-closeout |
| Media | WT-2026-247a | Higiene de suite: aislamiento de tests y bugs de regex/mock/lock | system/testing-hygiene | completed | WT-2026-245c | session-2026-06-10-preexisting-failures |
| Media | WT-2026-248a | Estabilizar .opencode/opencode.json: restauracion exacta del launcher y guard de integridad en pre-handoff | system/opencode-config-stability | completed | WT-2026-246b | session-2026-06-10-opencode-stability |
| Media | WT-2026-249a | Hardening minimo del contrato CLI: stderr vs returncode | system/cli-output-contract | completed | WT-2026-248a | session-2026-06-10-cli-contract-hardening |
| Media | WT-2026-249b | Excluir BUILDER_BRIEF_ del guard de superficies vivas del workspace | system/pre-handoff-live-surfaces | completed | WT-2026-249a | session-2026-06-11-builder-brief-followup |
| Alta | WT-2026-249c | Review bridge: normalizar parseo de CHANGES y evitar degradacion espuria a INSPECT | system/review-bridge-parser | active | WT-2026-249b | session-2026-06-11-review-bridge-parser |

## WT-2026-236a - Smoke repo-compare con Orca y SOUL.md para validar flujo externo
- **Prioridad:** Media
- **Scope:** system/research-devx
- **Estado:** completed
- **Problema:** el protocolo `repo-compare` debe poder comparar un repo externo
  contra el contexto local, pero el preflight real ya mostro fricciones: MCP
  GitHub con credenciales invalidas, `gh` CLI sin auth, `.agent/runtime/audit/AUDIT.md`
  ausente y `scripts/local_audit.py` no instalado en este `repo_destino`.
- **Objetivo:** usar `stablyai/orca` como target y el post `SOUL.md` como referencia
  secundaria para producir un reporte evidence-linked que separe oportunidades de
  producto y diagnostico del tooling.
- **Criterio:** reporte persistido en `.agent/runtime/compare/`, scoring Orca 0-5,
  3-5 oportunidades o descarte justificado, seccion "Que Ignorar", estado de
  AUDIT/MCP/gh/Repomix documentado y validate final o blocker exacto.
- **Depende de:** WT-2026-182, WT-2026-227a, WT-2026-235a.
- **Origen:** session-2026-06-07-repo-compare-smoke.

## WT-2026-237a - Formalizar fixes de motor emergentes del smoke repo-compare
- **Prioridad:** Alta
- **Scope:** system/review-closeout-hardening
- **Estado:** completed
- **Problema:** `WT-2026-236a` era un ticket `documentation/research`, pero durante
  el relanzamiento real del Builder/Manager obligo a tocar codigo productivo del
  `repo_motor` para reparar flujo y observabilidad: proyecciones de estado,
  closeout, bridge de review, resolucion del agente `manager` y clasificacion de
  transporte NDJSON. El Manager ya reviso el trabajo y devolvio `CHANGES` legitimo
  porque esos cambios de motor quedaron fuera de `Files Likely Touched` del smoke.
- **Objetivo:** abrir un ticket de codigo limpio que absorba formalmente los fixes
  de motor ya introducidos y cierre la deuda de alcance detectada por el review loop.
  El ticket debe convertir un hotfix de sesion en entrega canonica evidence-linked,
  con quality gates de codigo y review packet coherente.

## WT-2026-238a - Cierre de sesion y handoff documental post WT-2026-237a
- **Prioridad:** Media
- **Scope:** system/session-closeout-hygiene
- **Estado:** completed
- **Problema:** `WT-2026-237a` ya deja el sistema tecnico estabilizado, pero la
  sesion acumulo aprendizajes repartidos entre memoria, documentacion durable,
  prompts de auditoria y estado de handoff. Sin un cierre deliberado, el
  siguiente chat arrancara con contexto util pero disperso.
- **Objetivo:** consolidar el cierre de la sesion en un paquete ligero y
  revisable: memoria ya promovida o descartada explicitamente, documentacion
  durable alineada, y una nota de handoff que deje claro que sigue pendiente y
  que ya quedo resuelto.
- **Criterio:** el ticket debe terminar con:
  - decision explicita sobre memoria pendiente (si hay nuevas observaciones o
    si no hace falta promover nada mas);
  - documentacion durable minima actualizada o descartes justificados;
  - handoff corto y canonico para arrancar el siguiente chat sin reabrir
    `WT-2026-237a`;
  - `validate --json` del `repo_destino` sin errores.
- **Depende de:** WT-2026-237a.
- **Origen:** session-2026-06-08-handoff.

## WT-2026-239a - Separar protocolo de cierre para tickets documentation vs code
- **Prioridad:** Alta
- **Scope:** system/documentation-closeout-protocol
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo en
  `repo_destino`. Reabrir solo si reaparece evidencia fresca de que el cierre
  documental sigue rompiendo el ciclo canonico.
- **Problema:** el motor sigue cerrando tickets `documentation` con un protocolo
  demasiado heredado de tickets `code`, lo que provoca `HANDOFF_BLOCKED` por
  checkpoint, commit gates o pre-handoff no adecuados al deliverable real.
- **Objetivo:** introducir una rama de cierre documental para que Builder,
  Manager y Supervisor completen el ciclo sin exigir gates de codigo cuando
  `deliverable_type=documentation`, empezando por un bypass condicional dentro
  del pre-handoff existente.
- **Criterio:** cierre completo Builder -> Manager -> Supervisor para un ticket
  `documentation`, con tests de ciclo real y sin checkpoint/commit manual.
- **Depende de:** WT-2026-238a.
- **Origen:** session-2026-06-08-doc-closeout-followup.
- **Entregas esperadas:**
  - consolidar en el paquete del ticket los fixes ya hechos en `repo_motor` sobre
    `bus/review_bridge.py`, `.agent/agent_controller.py`,
    `scripts/state_projection_sync.py`, `scripts/state_projection_probe.py`,
    `scripts/launch_agent_terminals.ps1` y tests asociados;
  - registrar evidencia de `ruff` + `pytest` para los cambios de motor;
  - documentar que `WT-2026-236a` queda como smoke/documentation con salida a
    `HUMAN_GATE`, y que el codigo se formaliza aqui;
  - decidir si el ticket debe incluir tambien el endurecimiento restante del bridge
    cuando OpenCode emite `stderr` benigno de migracion antes de una `DECISION`
    valida, o dejarlo como follow-up separado si no bloquea.
- **Criterio:** el ticket queda listo cuando el review packet del Manager ya no
  mezcle fixes de motor con un ticket documental; los cambios de `repo_motor`
  estan cubiertos por `Files Likely Touched`, tienen evidencia de quality gates y
  el closeout/review bridge pasan por la ruta canonica sin `transport_failed`
  espurios ni dependencias ocultas del entorno.
- **Dependencias:** WT-2026-235a, WT-2026-236a.
- **Origen:** session-2026-06-07-repo-compare-followup.
- **Notas de alcance inicial:**
  - `state_projection_sync()` con rutas explicitas y formato canonico;
  - `mark-ready` / `validate` sin drift cuando el supervisor no materializa;
  - `non_code_ticket` sin exigir checkpoint de motor imposible por contrato;
  - `_fail_closeout()` en todos los caminos de fallo relevantes;
  - materializacion runtime de `.opencode/agents/manager.md` en `repo_destino`;
  - clasificador de transporte que no confunda NDJSON del review con `auth_failed`.

## TBD - Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip 26.1.2
- **Prioridad:** Media
- **Scope:** system/security-dependencies
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** deuda retirada del backlog activo de
  `repo_destino`; si vuelve a ser prioritaria, debe reaparecer con evidencia
  nueva desde `repo_motor` y el resolver real de `uv`.
- **Problema:** `repo_motor` ignora temporalmente `PYSEC-2026-196` en
  `[tool.pip-audit].ignore-vuln` porque el fix existe en `pip 26.1.2`, pero
  `uv` aun resolvia `pip 26.1.1` en este entorno al cerrar `WT-2026-235a`.
- **Criterio:** cuando `uv lock --upgrade-package pip` pueda fijar
  `pip>=26.1.2`, retirar la excepcion, regenerar lock si aplica y verificar
  `python scripts/pip_audit_project.py` sin vulnerabilidades ignoradas.
- **Evidencia:** `repo_motor` commit `3601312` hizo que el wrapper respete
  `ignore-vuln`; la deuda es retirar la excepcion, no saltarse el gate.
- **Origen:** session-2026-06-07-security-followup.

## WT-2026-233a - Reapertura humana controlada de tickets terminales
- **Prioridad:** Media
- **Scope:** system/bus-recovery
- **Estado:** completed
- **Problema:** el guard de reentrada bloqueaba correctamente cualquier
  `COMPLETED -> IN_PROGRESS`, pero no existia una via humana explicita para reparar
  cierres forzados que no habian pasado por aprobacion canonica del Manager.
- **Entrega:** `--reopen-terminal-ticket` valida ticket activo y estado derivado
  `COMPLETED`, y usa `allow_reentry=True` solo en esa ruta controlada.
- **Evidencia:** commits `1b32205`, `b1ad76a`, `e13bdc5` y `5b3f069`;
  tests focales, `ruff` y hooks limpios.
- **Criterio:** la proteccion sigue activa por defecto y solo el flag humano puede
  reabrir el ticket terminal activo.

## WT-2026-233b - Idempotencia de Manager tras cierre y reapertura terminal
- **Prioridad:** Media
- **Scope:** system/bus-recovery
- **Estado:** completed
- **Problema:** la auditoria posterior a `WT-2026-233a` detecto que
  `StateMachine.derive_state_from_events()` no trataba un `SUPERVISOR_CLOSED`
  aislado como evidencia terminal. Esto rompio la idempotencia historica de
  `--manager-approve`.
- **Entrega:** `SUPERVISOR_CLOSED` deriva ahora `COMPLETED`; un
  `STATE_CHANGED -> IN_PROGRESS` posterior sigue prevaleciendo para la
  reapertura humana. El fixture saludable de `--validate` incluye el contrato
  de prosa y auditoria vigente.
- **Evidencia:** test auditado recuperado, 20 tests focales verdes, `ruff`
  limpio y suite global `2231 passed, 22 skipped`.
- **Criterio:** aprobar de nuevo un ticket cerrado es idempotente; aprobar un
  ticket explicitamente reabierto ejecuta el cierre nuevo; suite global verde.

## WT-2026-233c - Coleccion aislada de test_manager_approve
- **Prioridad:** Baja
- **Scope:** system/testing-hygiene
- **Estado:** completed
- **Problema:** `tests/unit/test_manager_approve.py` insertaba `.agent` en
  `sys.path[0]` despues de la configuracion canonica de `tests/conftest.py`.
  Esto hacia que `.agent/runtime` sombreara `runtime/` del motor y provocaba
  `ModuleNotFoundError: runtime.project_root` al ejecutar el archivo aislado.
- **Entrega:** eliminado el bootstrap local redundante; `conftest.py` conserva
  `repo_motor` antes de `.agent` y expone ambos paquetes.
- **Evidencia:** test auditado aislado `1 passed`, archivo completo `7 passed`,
  familia estado/Manager `25 passed`, suite global `2231 passed, 22 skipped`.
- **Criterio:** `pytest tests/unit/test_manager_approve.py -q` funciona desde
  `repo_motor` sin depender del orden de otros tests.

## WT-2026-235a - Manager review bridge: decisiones autoritativas y CHANGES con blockers
- **Prioridad:** Critica
- **Scope:** system/review-bridge-decision-contract
- **Estado:** completed
- **Problema:** el fallback `text_regex` de `review_bridge.py` puede capturar
  `DECISION: APPROVE/CHANGES` desde plantillas reflejadas del transcript, y
  `CHANGES` puede emitirse con blockers vacios. Eso provoca requeue ciego o,
  peor, falso cierre por approve fantasma.
- **Criterio:** `APPROVE` y `CHANGES` solo desde fuente final autoritativa;
  `CHANGES` requiere estructura completa y blockers no vacios; si no, degradar
  a `INSPECT` con `failure_reason` y sin requeue.
- **Depende de:** WT-2026-204, WT-2026-234a.

## WT-2026-234a - Cierre de sesion portable y cuarentena de artefactos con IDs
- **Prioridad:** Media
- **Scope:** system/session-closeout-portability
- **Estado:** completed
- **Problema:** queda un documento historico versionado con ID de ticket en el
  nombre y aproximadamente 834 MB de residuos locales ignorados. El cierre debe
  distinguir producto, historia y temporales antes de actuar.
- **Criterio:** barrera sobre nombres versionados, documento historico archivado
  con checksum, limpieza tras human gate, memoria propuesta antes de escribir y
  session closeout final sin fallos bloqueantes.
- **Depende de:** WT-2026-229a, WT-2026-233c.

## WT-2026-231a - Pre-handoff commitea repo_motor en topologia motor/destino con scope FLT
- **Prioridad:** Alta
- **Scope:** system/pre-handoff-commit
- **Estado:** completed
- **Problema:** en la topologia motor/destino, el codigo productivo vive en `repo_motor`, pero la ruta de
  commit del pre-handoff todavia asume un unico repo y usa `project_root`/`repo_destino`
  como `cwd`. El guard de WT-2026-228a detecta motor sucio y bloquea antes de que haya
  una accion determinista que commitee la entrega. El resultado recurrente es
  `mark-ready` bloqueado por "No commit evidence" aunque el Builder haya implementado.
- **Objetivo:** convertir el pre-handoff en una decision determinista commit-o-bloquea:
  si todos los cambios productivos del `repo_motor` estan dentro de `Files Likely
  Touched`, el harness hace `git add` + `git commit` en `repo_motor` con el ID del ticket
  y actualiza `checkpoint/review-<ticket>` en el motor; si hay cambios fuera de scope,
  bloquea con lista exacta.
- **Non-goals:** no crear tag en `repo_destino`; no relajar `mark-ready`; no cambiar el
  contrato de `Files Likely Touched`; no dar permisos extra al Builder; no mezclar con
  `WT-2026-230a`.
- **Tests requeridos:** motor sucio dentro de FLT commitea; motor sucio fuera de FLT
  bloquea; ronda vacia sigue bloqueando por falta de evidencia; checkpoint apunta al
  commit de entrega; normalizacion de paths motor-relative evita interseccion vacia;
  hook que modifica archivo staged provoca re-add + segundo commit limpio o bloqueo claro.
- **Criterio:** el ticket que implemente 231a puede cerrarse sin commit manual del Manager
  cuando la entrega productiva este dentro de FLT.
- **Depende de:** WT-2026-228a, WT-2026-215.
- **Origen:** session-2026-06-05-builder-commit
- **Cierre:** completado en `repo_motor` commit `2a0d784`. Queda follow-up:
  `mark-ready` sigue resolviendo scope contra `repo_destino` y requiere
  `--scope-override` legitimo en topologia motor/destino; ver `WT-2026-232a`.

### Deuda TBD - renombre funcional de tests historicos del motor

Objetivo: quitar IDs de ticket del nombre del archivo cuando el test ya valida
comportamiento estable del producto. Los tests no se mueven ni se archivan; solo
se renombran en `tests/` y se actualizan sus referencias.

| Actual | Nombre funcional propuesto | Funcion principal cubierta |
|--------|----------------------------|----------------------------|
| `tests/test_wt_2026_228a_pre_handoff_motor.py` | `tests/test_pre_handoff_motor_productive_changes.py` | barrera pre-handoff sobre cambios productivos sin commit en `repo_motor` |
| `tests/test_wt_2026_221b_evidence_gate.py` | `tests/test_review_packet_evidence_gate.py` | gate de evidencia minima antes de review del Manager |
| `tests/test_wt_2026_221a_relaunch.py` | `tests/test_relaunch_evidence_capsule.py` | capsula evidence-linked y camino valido de relaunch |
| `tests/test_wt_2026_216_launcher_bus_read.py` | `tests/test_launcher_state_from_bus.py` | decision del launcher derivada del bus y fallback controlado |
| `tests/test_wt_2026_214_preflight_reconcile.py` | `tests/test_preflight_reconcile_decision.py` | decision de preflight entre aligned / cleanup / reconcile / abort |
| `tests/test_wt_2026_212_durable_changes.py` | `tests/test_durable_changes_requeue.py` | procesamiento durable de `CHANGES` y requeue garantizado |
| `tests/test_wt_2026_211_write_path.py` | `tests/test_ticket_projection_write_path.py` | write-path canonico y materializacion de proyecciones |
| `tests/test_wp_2026_127.py` | `tests/test_approval_state_revision_and_skill_access.py` | OCC de estado, expiracion de approvals y filtrado de skills por rol |

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
- **Problema:** `REVIEW_DECISION=CHANGES` puede quedar sin consumidor durable si el supervisor reactivo anterior ya no esta vivo. Eso deja tickets huÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rfanos en `READY_FOR_REVIEW` hasta intervenciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n manual o bootstrap tardÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­o.
- **Objetivo:** garantizar que cada `CHANGES` tenga procesamiento durable y produzca relanzamiento o requeue sin depender de que el supervisor anterior siga vivo.
- **Sketch inicial:** reforzar el consumidor de `CHANGES` con una ruta durable y verificable; puede ser supervisor persistente, bootstrap watchdog explÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­cito o disparo controlado de `ticket_supervisor.py --once`, pero debe quedar una sola autoridad observable en el bus.
- **Criterio:** un `REVIEW_DECISION=CHANGES` pendiente se procesa dentro de una ventana acotada sin intervenciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n manual y sin tickets huÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rfanos.
- **Depende de:** WT-2026-211.
- **Cierre:** la ruta canÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³nica queda en `bus/review_bridge.py`: `REVIEW_DECISION=CHANGES` -> `--request-changes` -> `_ensure_durable_changes_consumer(...)` -> `bootstrap()+run_once()` del supervisor. Tests focales y regresiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n de bridge aprobados.

## WT-2026-214 - Protocolo de forced close en preflight para ticket anterior y runtime stale
- **Prioridad:** Alta
- **Scope:** system/preflight-reconcile
- **Estado:** completed
- **Problema:** el launcher ya lee el bus como autoridad primaria para elegir agente, pero el preflight todavÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a no distingue formalmente entre limpiar runtime stale y reconciliar historia en el bus. Eso deja abierta la misma familia de drift que originÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ `WT-2026-205`.
- **Objetivo:** integrar una decisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n de preflight con tres casos explÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­citos:
  - ticket previo terminal -> cleanup local;
  - ticket previo no terminal -> reconciliaciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n canÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³nica;
  - bus ilegible o contradictorio -> aborto.
- **Sketch inicial:** insertar la decisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n entre `Assert-StartupAlignment` / `Repair-StartupSupervisorState` y `Remove-StaleRuntimeArtifacts`, reutilizando el bus como autoridad canÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³nica e invocando `scripts/reconcile_ticket.py` solo cuando el drift no terminal estÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© confirmado.
- **Criterio:** abrir WT-N+1 con runtime stale de WT-N no mezcla historias: limpia si WT-N ya cerrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³, reconcilia si WT-N quedÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ colgado y aborta si no puede decidir con seguridad.
- **Depende de:** WT-2026-210, WT-2026-216.
- **Cierre:** implementacion aprobada y commiteada; cierre canonico emitido en el bus con `scripts/reconcile_ticket.py`; runtime stale de `WT-2026-214` limpiado antes de la migracion fisica del workspace.

## WT-2026-216 - Launcher lee el bus en vez de TURN.md para decidir que agente lanzar
- **Prioridad:** Alta
- **Scope:** system/launcher-bus-read
- **Estado:** completed
- **Problema:** el launcher sigue tomando su decisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n operativa principal desde `TURN.md`. Si esa proyecciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n queda stale aunque el bus refleje el estado correcto, puede relanzar el agente equivocado o no relanzar ninguno.
- **Objetivo:** mover la decisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n de arranque a lectura del bus o de un helper canÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³nico basado en el bus, dejando `TURN.md` como proyecciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n operativa secundaria.
- **Sketch inicial:** introducir una ruta de decisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n bus-read en `launch_agent_terminals.ps1`, con fallback explÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­cito y acotado solo si el bus no puede leerse; cubrir el caso de `TURN.md` stale con tests focales.
- **Criterio:** con bus correcto y `TURN.md` stale, el launcher sigue eligiendo el agente correcto; el rescate durable de `WT-2026-212` pasa a ser fallback excepcional y no camino normal.
- **Depende de:** WT-2026-211.
- **Cierre:** `launch_agent_terminals.ps1` consulta `scripts/get_launcher_state.py` antes de leer `TURN.md`; el helper deriva estado vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a `StateMachine.derive_state_from_events()` y los tests focales del launcher pasan.
- **Nota residual:** el mapeo `TicketState -> (role, action)` estÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ duplicado entre `scripts/get_launcher_state.py` y `bus/supervisor.py`; candidata a ticket de limpieza posterior, no bloqueante.

## WT-2026-215 - Gates Modelo B: operaciones git de tooling resuelven motor_root
- **Prioridad:** Alta
- **Scope:** system/gates-motor-root
- **Estado:** completed
- **Cierre verificado:** bus con `REVIEW_DECISION=approve`, `CLOSE_CONFIRMED`,
  `STATE_CHANGED -> COMPLETED` y `SUPERVISOR_CLOSED`; entrega productiva en
  `f8cd50d` y cierre documental en `e3b3823`.
- **Problema:** varias operaciones git del tooling corren con `cwd=project_root` (el workspace, que NO es repo git) en vez de `motor_root` (`orquestador_de_agentes/`, que SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â es repo y contiene los commits). El resultado es `git diff` vacÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­o y decisiones falsas. Sintoma verificado en esta sesion: el pre-check de packaging del review bridge (`check_review_packet_diff_empty`) reporta "empty review diff" y emite `REVIEW_DECISION=CHANGES` automatico aunque el Builder SI haya commiteado codigo real en el motor. Bloqueo dos ciclos seguidos en `WT-2026-214` sin que el Manager llegara a revisar codigo.
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
- **Nota de simplificacion:** si el motor pasa a ser carpeta hermana del workspace (decision en curso), el principio se vuelve trivial de razonar: no hay repo anidado, el `cwd` de git es siempre el repo del motor sin ambiguedad. La migracion fisica no arregla este bug por si sola ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â el codigo sigue viviendo en el repo del motor ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â pero elimina la confusion conceptual.

## WT-2026-217 - Pre-check de packaging usa la ruta canonica de transicion al emitir CHANGES
- **Prioridad:** Alta
- **Scope:** system/bus-transition
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo tras la
  estabilizacion posterior del bus; reabrir solo con reproduccion nueva.
- **Problema:** cuando el pre-check de packaging del review bridge rechaza un paquete (diff vacio), emite `REVIEW_DECISION=CHANGES` pero NO completa la transicion canonica de estado: no emite `STATE_CHANGED -> IN_PROGRESS`. El ticket queda en `READY_FOR_REVIEW` en el bus con un CHANGES colgante, y el supervisor no puede reencolar (READY_FOR_REVIEW esta en `RELAUNCH_BLOCKED_STATES`). Resultado: sistema atascado que requiere cirugia manual del bus. Verificado en esta sesion (`WT-2026-214`): hubo que emitir `STATE_CHANGED -> IN_PROGRESS` a mano y reiniciar el supervisor para destrabar.
- **Distincion respecto a WT-2026-215:** son bugs independientes. `WT-2026-215` ataca la *causa* del rechazo falso (git en `cwd` equivocado -> diff vacio falso). Este ataca el *hazard de stall*: aunque el diff vacio sea legitimo (Builder que de verdad no commitea), el camino CHANGES del pre-check deja el supervisor colgado. Arreglar `WT-2026-215` reduce la frecuencia del trigger; este elimina el stall cuando el trigger es legitimo.
- **Causa raiz:** el camino CHANGES del pre-check se salta la ruta canonica de transicion. El CHANGES normal del Manager llama a `--request-changes`, que emite `STATE_CHANGED -> IN_PROGRESS` (o HUMAN_GATE) y luego `_ensure_durable_changes_consumer` (`WT-2026-212`). El pre-check emite el `REVIEW_DECISION` directamente sin pasar por esa maquinaria.
- **Sketch:** hacer que el camino CHANGES del pre-check use la MISMA ruta canonica que el CHANGES normal: invocar `--request-changes` (transicion + ApprovalRequest si aplica) y `_ensure_durable_changes_consumer`. Una sola autoridad de transicion, coherente con `WT-2026-211`/`WT-2026-212`.
- **Tests requeridos:** un pre-check que rechaza por diff vacio produce `STATE_CHANGED -> IN_PROGRESS` en el bus; el supervisor reencola sin intervencion manual; no hay doble relaunch; el caso de diff valido no cambia.
- **Criterio:** un rechazo de packaging (falso o legitimo) deja el ticket en estado consistente y reencola al Builder por la ruta durable, sin cirugia manual del bus.
- **Depende de:** WT-2026-210. Relacionado: WT-2026-203 (introdujo el pre-check), WT-2026-212 (ruta canonica de CHANGES), WT-2026-215 (misma region de codigo: pre-check de `review_bridge.py`).

## WT-2026-223a - Parser central de ticket IDs y contrato de nomenclatura
- **Prioridad:** Alta
- **Scope:** system/ticket-naming
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo; la
  deuda solo vuelve si aparece otro incidente real de parsing o autoridad de
  ticket.
- **Problema:** la nomenclatura de tickets y planes sigue repartida en regex locales y comparadores ad hoc. El incidente real de `WT-2026-221a` lo hizo visible: `_ticket_sort_key()` no interpretaba bien sufijos alfanumericos y permitia que un ticket historico menor ganara autoridad en el relaunch. Si el sistema adopta tickets nuevos con sufijo obligatorio (`...a`, `...b`, `...c`), mantener regex dispersas volvera a abrir puntos ciegos en controller, supervisor, session tracking y tests.
- **Decision de contrato:** todo ticket nuevo usa sufijo alfabetico obligatorio y empieza en `a`; el plan usa `PLAN-YYYY-NNN` sin sufijo. Ejemplos canonicos: `PLAN-2026-223`, `WT-2026-223a`, `WT-2026-223b`.
- **Compatibilidad:** lectura legacy permisiva para historico existente sin sufijo (`WT-2026-208`), pero escritura/estado activo en modo estricto para tickets nuevos.
- **Scope minimo:**
  - crear `runtime/ticket_parser.py` como seam unico de parsing/validacion;
  - exponer `parse_ticket_id()`, `ticket_to_plan_id()`, `validate_ticket_id(strict)` y `next_ticket_id()`;
  - reemplazar regex dispersas al menos en `_ticket_sort_key()` y `.agent/agent_controller.py`;
  - introducir validacion de contiguidad `a -> b -> c` y prohibicion de huecos;
  - resolver el prefijo del host desde `PROJECT.md`, con fallback controlado en el motor.
- **Non-goals iniciales:**
  - no automatizar aun la transicion autonoma entre subtickets (`a -> b`);
  - no reescribir `events.jsonl` historicos para forzar sufijos;
  - no convertir este ticket en un rediseÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±o completo del supervisor por planes.
- **Tests requeridos:**
  - IDs validos e invalidos;
  - modo legacy permisivo sin romper historico;
  - `ticket_to_plan_id()` para tickets con y sin sufijo;
  - ordenacion/contiguidad de subtickets (`a`, `b`, `c`);
  - regresion del bug real: un ticket como `WT-2026-221a` no pierde prioridad frente a `WT-2026-183` por parsing defectuoso.
- **Criterio:** el sistema acepta de forma canonica tickets nuevos con sufijo obligatorio, conserva lectura segura del historico legacy y deja de depender de regex locales para validar, comparar o proyectar IDs de ticket/plan.
- **Depende de:** WT-2026-221a. Relacionado: WT-2026-181 (nomenclatura WP->WT), WT-2026-209 (estandar workspace+motor).

## WT-2026-213 - Eliminar el doble STATE_CHANGED de --mark-ready
- **Prioridad:** Baja
- **Scope:** system/bus-events
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** retirado del backlog activo porque el doble
  `STATE_CHANGED` quedo como ruido semantico sin impacto operativo confirmado.
  Reabrir solo si aparece evidencia nueva de que rompe consumidores del bus o
  complica un flujo canonico real.
- **Problema:** `--mark-ready` emite dos eventos `STATE_CHANGED` consecutivos para la misma transicion a `READY_FOR_REVIEW`. Es idempotente en efecto practico (el estado derivado es el mismo), pero ensucia el bus y complica auditorias y cualquier consumidor que asuma unicidad de eventos de transicion.
- **Impacto:** ruido semantico, no fallo operativo. Ningun stall ni drift conocido atribuible a esto. Por eso Baja.
- **Sketch:** identificar los dos emisores en el camino de `--mark-ready` (controller + sync de targets) y dejar una sola emision canonica. Verificar contra `bus/state_machine.py` que no se rompa la derivacion.
- **Tests requeridos:** `--mark-ready` emite exactamente un `STATE_CHANGED -> READY_FOR_REVIEW`; estado derivado intacto; idempotencia de re-ejecucion preservada.
- **Criterio:** una sola transicion canonica por `--mark-ready`; bus sin evento duplicado.
- **Depende de:** WT-2026-210.

## TBD - BUILDER_STARTED liveness
- **Prioridad:** Baja
- **Scope:** system
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** idea retirada del backlog activo. La liveness
  relevante quedo cubierta por tickets posteriores sobre claim atomico,
  verificacion de Builder vivo, relaunch guard y supervisor liveness
  (`WT-2026-199`, `WT-2026-205`, `WT-2026-221a`, `WT-2026-224a`).
- **Problema historico:** se barajo introducir una senal explicita tipo
  `BUILDER_STARTED` para reforzar la observabilidad de arranque.
- **Decision documental:** no abrir trabajo nuevo solo por esta idea mientras no
  exista una reproduccion actual donde las senales ya existentes resulten
  insuficientes.

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
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** deuda retirada del backlog activo por higiene
  documental; reabrir solo si reaparece riesgo operativo real en guardado.
- **Problema:** `guard_paths.py` usa patrones de seguridad (privada, .env) pero no protege archivos de estado del workspace (work_plan.md, execution_log.md). En Modelo B, si el cwd es el motor, el guard no "ve" el workspace ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â work_plan.md puede sobreescribirse accidentalmente. Incidente: WP-2026-178 pisÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ WT-2026-182 en sesiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n 2026-05-30.
- **Sketch:** aÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±adir a `guard_paths.py` una lista de archivos de estado sagrados del workspace resueltos vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a `AGENT_PROJECT_ROOT`; cualquier write a esos paths requiere confirmaciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n explÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­cita.
- **Criterio:** intentar editar `z_scripts/.agent/collaboration/work_plan.md` desde Claude Code muestra alerta de guard y requiere confirmaciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n.
- **Depende de:** WT-2026-182 (completado).

## WT-2026-182 - Integracion Repomix para Context Bootstrapping y Repo-Compare
- **Prioridad:** Media
- **Scope:** system/skills
- **Estado:** completed
- **Problema:** En el arranque, los agentes exploran "a ciegas" perdiendo turnos; ademÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡s, las herramientas de repo-compare son lentas fichero a fichero.
- **Sketch:** 
  1) `repomix-context`: generar `.agent/context/repomix.xml` (con `--compress`) del workspace en arranque y pasarlo como `-f` a los agentes para inyecciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n de contexto Cero-Turno.
  2) `repo-compare`: usar repomix para empaquetar origen + destino en XMLs comprimidos para que el agente reciba ambos de golpe detectando gaps inmediatamente.
- **Criterio:** El agente arranca recibiendo todo el contexto comprimido automÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ticamente (sin overhead notable en repos pequeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±os), y la herramienta de repo-compare empaqueta y compara vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a Repomix.
- **Notas:** Depende de Node.js (que ya estÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ instalado por OpenCode). Ideal usar opciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n `--compress` nativa de Tree-sitter.

## WT-2026-185 - Knowledge Layer: Glosario + Microagent + skill_resolver
- **Prioridad:** Media
- **Scope:** system/knowledge
- **Estado:** completed
- **Problema:** Los agentes carecÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­an de marco canÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³nico de terminologÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a y onboarding; el skill_resolver fallaba silenciosamente ante catÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡logos vacÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­os.
- **Sketch:** actualizar `EmptySkillCatalogError` para mencionar `.agent/microagents/`; crear `agent_system/templates/glossary.md` (14 tÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rminos); crear `templates/microagents/onboarding.md` con triggers y heurÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­sticas de tech stack; integrar en instalador con guard `if not exists`; test unitario del mensaje.
- **Criterio:** excepciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n guÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a al usuario; instalador deposita knowledge docs; `--validate` no emite warning `host-project` tras install.
- **Depende de:** WT-2026-184.
- **Nota post-cierre:** los knowledge docs depositados en `.agent/` raÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­z son vulnerables al prune de `--sync` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ corregido en WT-2026-186.

## WT-2026-186 - Idempotencia del instalador y contrato de rutas gestionadas
- **Prioridad:** Alta
- **Scope:** system/install
- **Estado:** completed
- **Problema:** `scripts/install_agent_system.py --sync` puede podar `.agent/glossary.md` y `.agent/microagents/` en la segunda sincronizacion estricta. Esas rutas se depositan desde `agent_system/templates/`, no existen en `.agent/` fuente y no estan cubiertas por `LOCAL_DIRS`.
- **Decision de semantica:** `glossary.md` y `microagents/` son plantilla-una-vez: el instalador los crea si faltan, luego pertenecen al workspace destino. `--sync` no los sobrescribe, pero tampoco debe podarlos.
- **Sketch:**
  1) Introducir `INSTALLER_MANAGED_PATHS = {"glossary.md", "microagents"}` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â constante separada de `LOCAL_DIRS` con semÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ntica distinta: estas rutas se depositan una vez y luego pertenecen al destino; `--sync` no las poda pero tampoco las sobrescribe. NO usar `is_preserved()` (footgun: bloquearÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a sync si algÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âºn dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a se aÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±aden a la fuente).
  2) Modificar `detect_destination_residues()` para excluir las rutas de `INSTALLER_MANAGED_PATHS` antes de podar.
  3) `copy_tree()`: corregir comportamiento ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â el allowlist se valida por archivo, no solo por directorio raÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­z; `shutil.copytree` sobre un dir parcialmente allowlisted puede meter archivos no permitidos. Alinear docstring con comportamiento real (hoy promete `RuntimeError`, hace `SKIP`+continue).
  4) Eliminar entrada fantasma `BACKUP_VERIFIED.md` de `MANIFEST.workspace` (no existe en fuente ni destino).
- **Tests requeridos:** `install && sync && sync` preserva knowledge docs; sync preserva glosario modificado por usuario; residuo real se poda; archivo no-allowlisted dentro de dir permitido no se copia; dry-run no escribe ni borra pero reporta correctamente; glosario y microagents existentes no se sobrescriben.
- **Criterio:** `--install && --sync && --sync` deja vivos y personalizados los knowledge docs de WT-2026-185, mientras los residuos reales siguen siendo podados.
- **Depende de:** WT-2026-185.

## WT-2026-187 - Portabilidad Modelo B y limpieza legacy
- **Prioridad:** Alta
- **Scope:** system/portability
- **Estado:** completed
- **Problema:** varias rutas y comandos todavia asumen codigo local en el workspace o nombres fijos del motor. Esto debilita Modelo B y deja deuda legacy visible tras la auditoria de cierre.
- **Sketch:**
  1) Extraer `runtime/motor_link.py`: API `resolve_motor_root(project_root)`, `resolve_motor_controller(project_root)`, `resolve_motor_script(project_root, script_name)`. Lee `motor_destination_link.json`. Consumidores: `review_bridge.py`, `prepush_check.py`, `session_closeout.py`.
  2) Portabilidad: corregir `TEMPLATE_ROOT = Path(__file__).resolve().parent.parent` (bug activo: falla si motor se renombra); corregir log de ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©xito en install (usa `PROJECT_AGENT` global, deberÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a usar `project_agent` local).
  3) Portabilidad Modelo B: `prepush_check.py` usa `.agent/agent_controller.py` relativo ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â rompe en destino puro; resolver vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a `motor_link`; mismo problema en `session_closeout.py` (invoca 6+ scripts desde `project_root/scripts/`).
  4) Ampliar `_check_portability()` en `session_closeout.py` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â hoy solo escanea `docs/markdowns/skills/.agent/rules` en `*.md`; no ve `scripts/`, `bus/`, `*.py`, `*.ps1` (los hardcodes de esta auditorÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­a habrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­an sido invisibles).
  5) `.git` check frÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡gil: `pre_handoff_guard.py` devuelve `valid=True` silenciosamente si `.git` no existe en `project_root` (bypass de todos los checks). Decidir: "sin .git ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ skip con warning" vs `git -C <path> rev-parse --is-inside-work-tree`.
  6) Limpieza legacy: eliminar `sync_agent_core.py` (deprecado v9.4.1, nadie lo importa, 35 occ mojibake); `strict_sync` no-op en `sync_agent_system()`; `import shutil` redundante en `copy_knowledge_docs()`.
  7) Mensaje `EmptySkillCatalogError` engaÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±oso (dice "add microagents" pero resolver no las conoce); test superficial de WT-2026-185 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â reemplazar por test que ejerce ruta real de catÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡logo vacÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­o.
  8) DecisiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n explÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­cita: `orquestador.py` usa rutas cwd (`Path(".agent/logs")`, allowlist/denylist) sin migrar a `runtime.project_root` + 9 occ mojibake. ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Legacy o migrar?
  9) Comandos en `AGENTS.md` listan `python .agent/agent_controller.py` sin `--project-root` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â contradice la arquitectura Modelo B documentada en el mismo archivo.
- **Criterio:** los comandos de cierre/calidad funcionan desde workspace destino Modelo B puro; chequeo de portabilidad detecta hardcodes en cÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³digo fuente; no hay bypasses silenciosos en guards de higiene.
- **Depende de:** WT-2026-186.

## WT-2026-188 - Modularizacion progresiva de agent_controller.py
- **Prioridad:** Media
- **Scope:** system/architecture
- **Estado:** completed
- **Problema:** `.agent/agent_controller.py` concentra CLI, validacion, materializacion de estado y orquestacion. Es mantenible hoy, pero su tamano y centralidad elevan el coste de cambio.
- **Non-goal:** no crear codigo bajo `.agent/validators/` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â viola Modelo B (`.agent/` es estado, no codigo del motor). Namespace del motor: `bus/validators/`, `runtime/validators/` o similar segun dependencias reales.
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
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** issue retirado del backlog activo porque no
  bloquea el flujo canonico del `repo_destino`; reabrir solo si vuelve a ser
  limitante.
- **Problema:** `npx repomix` falla con `Permission denied while scanning directory` en `z_scripts` y `orquestador_de_agentes` en Windows. El error ocurre en globby antes de aplicar filtros de include/exclude. PowerShell accede sin problemas; el bloqueo es especÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­fico de Node.js (posiblemente antivirus o Windows Search). Repomix es best-effort y no bloquea el arranque.
- **Sketch:** investigar ACLs con `icacls`, probar desactivar indexaciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n de Windows Search en la carpeta, probar versiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡s reciente de repomix, o como alternativa usar `--working-dir` apuntando a un subdirectorio accesible.
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
- **Estado:** completed
- **Problema:** WT-2026-200 corrigio el bug real de precedencia `-OnlyBuilder` / `-ResumeBuilder`, pero aun quedan mejoras de robustez que conviene aislar para no reabrir un ticket ya cerrable: falta una prueba mas cercana al runtime real desde `bus/supervisor.py:_relaunch_builder()`, algunos tests dependen de asserts textuales sobre el `.ps1`, y el invariante de precedencia vive en codigo/tests pero no en una nota durable cercana al launcher.
- **Sketch:**
  1) AÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±adir un test o eval de integracion ligera que ejerza la invocacion real desde `_relaunch_builder()` hasta `launch_agent_terminals.ps1`.
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
- **Estado:** completed
- **Problema:** los ultimos tickets revelaron deuda estructural en el contrato entre bus, Supervisor, Manager, Builder, controller, bridge, hooks, gates y closeout. Se estan acumulando hotfixes sin mapa completo de fuente canonica, proyecciones, liveness y requeue durable.
- **Sketch:** auditar eventos, actores, writers, transiciones, locks, gates Modelo B y surfaces legacy; separar hechos verificados de inferencias; proponer arquitectura objetivo minima y tickets hijos pequenos.
- **Criterio:** existe mapa de actores/writers, tabla de eventos, invariantes rotas/objetivo, frontera canonico/proyeccion/cache/legacy y backlog hijo para liveness, requeue durable, gates Modelo B y closeout.
- **Depende de:** WT-2026-205.

## WT-2026-206 - Scope gate y cierres manuales en workspace+motor
- **Prioridad:** Media
- **Scope:** system/hygiene
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo tras la
  evolucion posterior del cierre motor-aware; reabrir solo con evidencia nueva.
- **Problema:** los cierres manuales en Modelo B siguen chocando con el scope gate porque el workspace `z_scripts` no es repo git y las rutas reales del motor viven en `orquestador_de_agentes/`. Esto obliga a `--scope-override` y `--force` en operaciones que deberian ser mas mecanicas.
- **Sketch:** resolver de raiz la relacion entre `Files Likely Touched`, motor subdir y proyecto raiz; reducir o eliminar la necesidad de overrides manuales en `--mark-ready` y `--manager-approve` bajo Modelo B.
- **Criterio:** los cierres manuales canonicos en Modelo B pueden completarse sin friccion estructural recurrente del scope gate.
- **Depende de:** WT-2026-210.

## WT-2026-207 - Gobernanza de collaboration legacy en el motor durante session-close
- **Prioridad:** Media
- **Scope:** system/hygiene
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo; la
  ambiguedad residual solo debe volver con evidencia fresca de confusion entre
  collaboration canonica y legacy.
- **Problema:** hoy existen dos superficies de collaboration: la activa en `z_scripts/.agent/collaboration` y una copia legacy/stale en `orquestador_de_agentes/.agent/collaboration`. El `session_closeout` solo opera sobre el workspace activo, por lo que la copia del motor acumula `manager_feedback_*`, `review_queue.md`, `work_plan.md`, `TURN.md` y `execution_log.md` obsoletos sin una politica explicita.
- **Sketch:** decidir y automatizar una de estas dos semanticas: (a) tratar la collaboration del motor como superficie legacy congelada y excluirla del lifecycle operativo; o (b) archivarla/limpiarla explicitamente durante `session-close` cuando `project_root != motor_root`. En ambos casos, dejarlo documentado y testeado para que no vuelva a parecer estado canonico.
- **Criterio:** tras un cierre de sesion, no queda ambiguedad sobre cual collaboration es canonica y la copia del motor no arrastra estado operativo engaÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±oso.
- **Depende de:** WT-2026-210.

## WT-2026-208 - Estabilizacion de suite global tras transicion workspace+motor
- **Prioridad:** Alta
- **Scope:** system/testing
- **Estado:** completed
- **Nota 2026-06-06:** el cierre previo siguio siendo el terminal canonico del bus.
  La correccion tecnica se entrego en `repo_motor` y la suite global quedo verde.
  Tras `WT-2026-233a`, se reabre de forma humana y controlada para completar review
  y cierre canonico por Manager.
  Cierre completado el 2026-06-06 mediante seq 867-871:
  `REVIEW_DECISION approve`, `READY_TO_CLOSE`, `CLOSE_CONFIRMED`, `COMPLETED`
  y `SUPERVISOR_CLOSED`.
- **Problema:** la suite global del motor esta rota de forma amplia tras la transicion a workspace+motor. Verificacion local el 2026-06-02: `46 failed`, `45 errors`, `1742 passed`, `21 skipped` en `uv run pytest orquestador_de_agentes/tests -q`. El informe previo del Builder ya apuntaba el problema, pero el recuento actual muestra que la deuda es mas grande de lo esperado.
- **Patrones observados:**
  1) tests que asumen cwd o rutas del motor (`test_windows_safe_temp_runtime`, `test_run_llm_evals`);
  2) tests que intentan renombrar o ocultar `.agent/` real del repo y fallan por permisos (`test_project_paths`, `test_migrate_legacy_project`, `test_upgrade`);
  3) drift de semantica en estado/cierre (`test_controller_integration`, `test_manager_approve`, `test_mark_ready_idempotency`, `test_ui_state`, `test_completion_checker`);
  4) mojibake y artefactos de encoding (`test_encoding_integrity`, `test_project_map_freshness`);
  5) fallos de sandbox/copias de fixtures en integracion (`test_completion_integration`).
- **Evidencia adicional 2026-06-03:** durante el fix `6ca92f7` se verifico que la suite completa no es una senal util como gate unico tras la reubicacion: `58 failed`, `45 errors`, `1757 passed`, `21 skipped`. Fallos representativos: referencias stale a `z_scripts` en rutas de tests, `.agent/hooks/__init__.py` inexistente en el motor limpio, locks/permisos al intentar renombrar `.agent` real en Windows, y scripts/config LLM no presentes (`scripts/run_llm_evals.py`, `.agent/runtime/llm_evals_config.json`). El fix de CI se valido con el test exacto, `tests/test_supervisor.py` completo (`137 passed`) y pre-push; la suite global requiere estabilizacion separada. Nota: quedo un cambio unstaged no relacionado en `scripts/discover_skills.py` del motor; no se commiteo con el fix.
- **Sketch:** inventariar fallos por familia, distinguir regresiones reales de tests obsoletos, y restaurar una baseline verde compatible con la arquitectura workspace+motor actual. La prioridad es recuperar confianza en la suite antes de seguir acumulando deuda en review/closeout.
- **Criterio:** la suite global vuelve a una baseline estable o, como minimo, queda segmentada en subconjuntos fiables con backlog explicito para el resto.
- **Depende de:** WT-2026-210.
- **Reevaluacion 2026-06-06:** la rotura amplia original ya no existe. El rerun
  previo encontro `2 failed, 2221 passed, 22 skipped`, ambos en
  `tests/test_pre_handoff_motor_productive_changes.py` por drift de expectativas
  frente a WT-2026-231a. La reapertura queda acotada a ese residual.
- **Cierre tecnico residual 2026-06-06:** archivo focal alineado con el contrato
  vigente; `python -m pytest tests/test_pre_handoff_motor_productive_changes.py -q`
  -> `15 passed`; `ruff` limpio; `python -m pytest tests -q` ->
  `2223 passed, 22 skipped, 9 warnings`.
- **Limite del sistema detectado:** `--bootstrap-ticket`, `EventBus.emit()` y
  `--mark-ready` no permiten reabrir un ticket terminal (`COMPLETED`). Si se quiere
  rehacer un cierre verde de forma 100% canonica, hace falta un ticket hijo para
  soporte de reopen o un ticket nuevo que absorba este residual.

## WT-2026-209 - Sustituir nomenclatura Modelo B por estandar workspace+motor
- **Prioridad:** Baja
- **Scope:** system/docs
- **Estado:** absorbed by WT-2026-232a
- **Problema:** el termino `Modelo B` sigue apareciendo en codigo, tests, changelog, AGENTS y prompts, pero ya no describe una opcion vigente. La arquitectura actual es una sola: workspace activo + motor portable separado. Mantener la terminologia antigua mete ruido conceptual y hace parecer que sigue habiendo modos paralelos.
- **Sketch:** inventariar referencias a `Modelo B` / `Model B`, decidir redaccion canonica (`workspace+motor`, `workspace activo`, `motor portable`) y actualizar codigo, docs, tests y mensajes de runtime para usar ese lenguaje de forma uniforme.
- **Criterio:** no quedan referencias activas a `Modelo B` en superficies operativas; la arquitectura se explica con una unica terminologia consistente.
- **Depende de:** WT-2026-232a.
- **Nota:** alcance absorbido por `WT-2026-232a`; no queda como ticket diferido.

## WT-2026-196 - Manager adaptativo ante blockers repetidos
- **Prioridad:** Alta
- **Scope:** system/review
- **Estado:** completed
- **Cierre verificado:** bus con aprobacion Manager, `CLOSE_CONFIRMED`,
  `STATE_CHANGED -> COMPLETED` y `SUPERVISOR_CLOSED`; commits productivos
  `e0f2624`, `719a9e5`, `a84aad6`, `71ccba4`, `1400e89` y `f38724a`.
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
- **Estado:** completed
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
- **Estado:** absorbed by WT-2026-208
- **Problema:** tras cerrar el hotfix del launcher/supervisor, los tests relacionados con los archivos tocados ya pasan (`140 passed`, `ruff` limpio), pero la suite global sigue acumulando decenas de `fails/errors` en modulos no relacionados (`test_audit_rules`, `test_completion_checker`, `test_encoding_integrity`, etc.). Ese frente es independiente del hotfix actual y hoy no esta inventariado de forma util para decidir si bloquea el siguiente ticket o si es deuda preexistente.
- **Sketch:**
  1) Ejecutar la suite completa con captura de resumen por modulo.
  2) Construir un inventario corto de fallos agrupado por archivo/modulo.
  3) Clasificar cada grupo en una de dos cestas: `infraestructura/preexistente` o `regresion del ticket activo`.
  4) Identificar blockers reales para el flujo actual (`WT-2026-191`) frente a deuda de estabilizacion general.
  5) Decidir con evidencia si abrir ticket especifico de estabilizacion de suite o si basta con aislar y corregir solo los blockers del flujo actual.
- **Criterio:** existe un inventario breve, accionable y por modulo de la suite rota; cada grupo de fallos queda clasificado como preexistente o regresion actual; se toma una decision explicita sobre si la estabilizacion global entra antes o despues del siguiente ticket funcional.
- **Depende de:** WT-2026-191.
- **Nota:** alcance absorbido por WT-2026-208; la deuda residual actual se
  mantiene en un TBD focal separado.
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
- **Estado:** completed
- **Cierre verificado:** bus con aprobacion Manager, `CLOSE_CONFIRMED`,
  `STATE_CHANGED -> COMPLETED` y `SUPERVISOR_CLOSED`; entrega productiva
  `a1e704c`.
- **Problema:** cuando el supervisor se cae durante un BUILDER_RELAUNCH_ATTEMPTED, al reiniciar lee el estado proyectado del bus. Si sigue siendo READY_FOR_REVIEW (porque el estado no se resetÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ a IN_PROGRESS antes del crash), despacha al Manager directamente sin relanzar Builder. Observado en WT-2026-192: seq 322 BUILDER_RELAUNCH_ATTEMPTED, seq 323 SUPERVISOR_RESTARTED, seq 324 MANAGER_REVIEWING sin Builder intermedio.
- **Root cause:** el supervisor en startup no distingue entre READY_FOR_REVIEW legÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­timo (Builder terminÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³) y READY_FOR_REVIEW espurio (crash durante relaunch post-CHANGES).
- **Sketch:** al reiniciar, el supervisor comprueba los ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âºltimos N eventos del bus. Si el ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âºltimo REVIEW_DECISION fue CHANGES y no hay BUILDER_EXIT posterior, forzar relaunch de Builder independientemente del estado proyectado. La condiciÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n es:  AND .
- **Tests requeridos:** supervisor reinicia con READY_FOR_REVIEW tras CHANGES sin BUILDER_EXIT ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ lanza Builder, no Manager; supervisor reinicia con READY_FOR_REVIEW legÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­timo (BUILDER_EXIT posterior a REVIEW_DECISION) ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ lanza Manager correctamente; test de regresiÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n del doble-requeue (no debe dispararse).
- **Criterio:** tras reinicio del supervisor, el ciclo CHANGES ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ Builder ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ Manager se ejecuta siempre en orden correcto, incluso si el crash ocurriÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ entre REVIEW_DECISION y BUILDER_EXIT.
- **Depende de:** WT-2026-192.

## TBD - Alinear tests legacy de pre-handoff con auto-commit motor-aware
- **Prioridad:** Media
- **Scope:** system/testing-hygiene
- **Estado:** absorbed by WT-2026-208
- **Problema:** la suite global del motor del 2026-06-06 termina con
  `2 failed, 2221 passed, 22 skipped`. Ambos fallos viven en
  `tests/test_pre_handoff_motor_productive_changes.py` y esperan el contrato
  anterior a WT-2026-231a.
- **Causa verificada:** `test_pre_handoff_blocks_on_motor_dirty` espera retorno
  `1`, pero el contrato vigente auto-commitea cambios productivos incluidos en
  Files Likely Touched y retorna `0`. El caso untracked fuera de scope sigue
  bloqueando correctamente, pero el test exige el mensaje antiguo
  `Uncommitted productive changes` en vez del diagnostico vigente
  `outside Files Likely Touched`.
- **Criterio:** actualizar los dos tests para gobernar el contrato vigente sin
  relajar la barrera fuera de scope; ejecutar el archivo focal y la suite global
  completa hasta obtener baseline verde.
- **Depende de:** WT-2026-231a.
- **Nota:** absorbido por la reapertura controlada de WT-2026-208.

## WT-2026-193 - Redaccion previa en pipeline de memoria persistente
- **Prioridad:** Baja
- **Scope:** system/security
- **Estado:** completed
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
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** deuda retirada del backlog activo de
  `repo_destino`; cualquier trabajo futuro sobre reglas de memoria debe
  relanzarse desde evidencia actual del `repo_motor`.
- **Problema:** el motor no tiene `memory_rules.md`. `install_agent_system.py` ya implementa `sync_memory_rules()` que fusiona wings engine/meta del motor al destino preservando el wing project del destino ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â pero si el motor no tiene `memory_rules.md`, el sync es un no-op y los destinos no reciben reglas portables. Verificado: `git log --oneline -- .agent/runtime/memory/memory_rules.md` devuelve vacio; el archivo no esta en history ni gitignoreado.
- **Causa raiz:** `memory_rules.md` es un artefacto derivado deterministamente de `observations.jsonl` via `memory_consolidate.py`. El motor tiene `observations.jsonl` vivo (35 KB, schema canonico) pero nunca se corrio la consolidacion para generar `memory_rules.md` y commitearlo.
- **Contexto clave (leer antes de ejecutar):**
  - `memory_consolidate.py` tiene flags `--apply` (default dry-run) y modifica `observations.jsonl` (dedupe+filter+archive). NO correr `--apply` sobre el motor sin revisar el dry-run primero.
  - El motor tiene `observations.jsonl` con cambios en working tree (modificado pero no commiteado a 2026-06-02). Verificar `git diff .agent/runtime/memory/observations.jsonl` antes de consolidar.
  - `memory_rules.md` generado contendra wings engine/meta/project derivados de las observaciones del motor. Revisar que las reglas son coherentes antes de commitear.
  - Una vez commiteado en el motor, el siguiente `--sync` en cualquier destino propagara automaticamente las wings engine/meta.
- **Sketch:**
  1) `git -C motor diff .agent/runtime/memory/observations.jsonl` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â entender que cambio.
  2) `python scripts/memory_consolidate.py` (dry-run) desde el motor ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ver que generaria.
  3) `python scripts/memory_consolidate.py --apply` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â generar `memory_rules.md`, `MEMORY.md`, `memory_profile.md`.
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
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo; si
  vuelve, debe abrirse con un caso reproducible sobre un destino nuevo.
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
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo; la
  promocion upstream solo se reabre si vuelve a bloquear el dogfooding real.
- **Problema:** el flujo normal de memoria es downstream (motor -> destino via sync). Pero este workspace es dogfooding: sus tickets mejoran el motor, por lo que genera aprendizajes de wing engine/meta que deberian propagarse al motor, no quedarse solo en el workspace. `memory_upload.md` (prompt canonico en `orquestador_de_agentes/prompts/`) describe inspeccion y propuesta de memoria, pero solo contempla dos destinos: memoria del proyecto y memoria personal de Claude. No menciona promocion al repo motor externo.
- **Contexto clave:**
  - El modelo de wings ya hace la separacion conceptual: `engine`/`meta` = portables al motor; `project` = locales al destino.
  - La promocion debe ser MANUAL con propuesta asistida. No automatica en cierre de ticket (riesgo de contaminar el motor con aprendizajes a medio cocer).
  - La ruta fisica de promocion es: escribir observacion en `orquestador_de_agentes/.agent/runtime/memory/observations.jsonl` + reconsolidar motor (o dejar para siguiente sesion de consolidacion).
  - `memory_upload.md` ya tiene la estructura correcta ("no escribas todavia; primero propÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³n"). Solo necesita un tercer destino posible.
- **Sketch:**
  1) Extender `memory_upload.md` con una seccion "Destinos posibles" que incluya explicitamente: (a) memoria del proyecto destino (`wing: project`), (b) motor externo (`wing: engine` o `meta`, escribe en `orquestador_de_agentes/.agent/runtime/memory/observations.jsonl`), (c) memoria personal de Claude (habitos transversales del usuario).
  2) La propuesta debe incluir el campo `wing` sugerido y el destino recomendado como parte del formato existente.
  3) Si el destino es el motor externo, la propuesta debe mostrar el texto exacto de la observacion en formato canonico (json) lista para insertar manualmente o con confirmacion explicita.
  4) El agente no escribe en el motor sin confirmacion humana explicita.
  5) Opcional: crear `scripts/promote_observation.py --to-motor` como herramienta CLI que automatiza el append a `observations.jsonl` del motor y emite un recordatorio de reconsolidacion pendiente.
- **Criterio:** al usar `memory_upload.md` en este workspace, el agente propone correctamente si un aprendizaje pertenece al proyecto, al motor o a Claude memory; el formato de propuesta incluye wing, destino y texto canonico; la escritura al motor requiere confirmacion humana.
- **Depende de:** WT-2026-219.
- **Origen:** session-2026-06-02-memory-bootstrap

## WT-2026-221a - Relaunch CEM: root verificado y capsula evidence-linked para Builder
- **Prioridad:** Alta
- **Scope:** system/agent-launch
- **Estado:** completed
- **Problema:** tras `REVIEW_DECISION=CHANGES`, el relaunch puede abrir una nueva ventana de Builder sin root operativo verificado y sin continuidad suficiente. Evidencia de la sesion: `BUILDER_RELAUNCH_ATTEMPTED` seq 578 con `builder_launch_unverified` / `verify_signal: none`, coincidente con una ventana rooteada en el motor que no podia leer el estado canonico del destino. Un Builder relanzado asi conserva velocidad, pero pierde memoria y tiende a reconstruir contexto con parches locales.
- **Objetivo:** convertir `WT-2026-221a` en la primera prueba real de CEM v0: el relaunch solo ocurre con topologia verificada y entrega una capsula fresca, evidence-linked y self-service al Builder.
- **Sketch:** antes de lanzar Builder, verificar `AGENT_PROJECT_ROOT`, `repo_motor`, `repo_destino`, bus legible y ticket activo. Si falla, no abrir Builder operativo. Si pasa, generar una capsula CEM desde fuentes canonicas que separe hechos verificados, blockers del Manager, hipotesis y siguiente accion. La capsula se regenera en cada relaunch y no se edita/acumula como estado vivo. El tier de rigor se deriva de paths/superficie tocada, no de la autoevaluacion del Builder.
- **Criterio:** un relaunch con root equivocado queda bloqueado con mensaje accionable; un relaunch valido genera capsula CEM fresh; Builder no puede marcar ready sin responder blockers evidence-linked; hay prueba que reproduce el fallo de topologia tipo seq 578.
- **Depende de:** WT-2026-208.

## WT-2026-221b - Manager evidence gate: rechazar review sin bus activo y evidencia minima
- **Prioridad:** Alta
- **Scope:** system/review-gates
- **Estado:** completed
- **Problema:** aunque el Builder trabaje correctamente, hoy puede llegar a review con un packet que no contiene evidencia productiva visible del ticket activo. En `WT-2026-221a`, el Manager rechazo `seq 602`, `seq 606` y `seq 617` porque el diff visible solo contenia docs/collaboration y no cambios reales del `repo_motor`.
- **Objetivo:** hacer que el Manager rechace o bloquee `READY_FOR_REVIEW` si faltan evidencias minimas del ciclo operativo y del diff/commit del `repo_motor`.
- **Sketch:** en la ruta de review, exigir bus/estado activo del ticket, review packet del ticket correcto, diff/commit productivo del `repo_motor`, tests asociados y clasificacion de docs-only/collaboration-only. Si falta algo, emitir `CHANGES` o bloqueo con razon estructurada.
- **Nota de metodo:** un cambio productivo es admisible si esta gobernado por un test concreto citado por nombre; es sospechoso si no hay test/evidencia que lo justifique.
- **Criterio:** ningun ticket puede llegar a cierre Manager con review packet docs-only/collaboration-only o sin evidencia minima del `repo_motor`, aunque el Builder haya trabajado manualmente.
- **Depende de:** WT-2026-208, WT-2026-221a.

## WT-2026-221c - Scope watch temprano contra Files Likely Touched
- **Prioridad:** Media
- **Scope:** system/scope-gate
- **Estado:** absorbed
- **Nota de cierre 2026-06-09:** follow-up retirado del backlog activo porque
  no hay evidencia reciente de que siga siendo la siguiente deuda prioritaria.
- **Problema:** el scope gate llega tarde, normalmente en `--mark-ready`. Cambios out-of-scope como `scripts/discover_skills.py` pueden vivir durante horas sin alerta.
- **Objetivo:** crear un check barato que compare `git diff --name-only` contra `Files / surfaces likely touched` durante el trabajo, no solo al cierre.
- **Sketch:** exponer un comando tipo `--scope-watch` o script focal que resuelva `motor_root`, lea el work_plan activo y reporte cambios fuera de scope con salida clara para Builder/Manager.
- **Criterio:** un archivo fuera de scope se detecta antes de `READY_FOR_REVIEW` y queda justificado, revertido o separado en ticket propio.
- **Depende de:** WT-2026-208.

## WT-2026-232a - mark-ready motor-aware y protocolo portable de topologia motor/destino
- **Prioridad:** Alta
- **Scope:** system/mark-ready-motor-aware+terminology-builder-bootstrap
- **Estado:** completed
- **Problema:** `WT-2026-231a` corrigio `--pre-handoff` para commitear y tagear
  `repo_motor`, pero `--mark-ready` sigue usando el scope gate historico:
  `parse_files_likely_touched()` resuelve FLT contra `PROJECT_ROOT` y
  `get_changed_files()` mira `repo_destino` cuando este tambien es repo git. Resultado:
  entrega correcta en `repo_motor` commit `2a0d784` necesito `--scope-override` porque
  el gate no vio los paths motor-relative reales.
- **Problema adicional absorbido:** `Modelo B` sigue como etiqueta operativa aunque la
  arquitectura vigente ya es una sola: `repo_motor` portable + `repo_destino`
  operativo. La deuda de `WT-2026-209` y la antigua deuda de paths portables quedan
  incorporadas aqui; no se difieren.
- **Objetivo:** hacer que `--mark-ready` use la misma evidencia motor-aware que
  `--pre-handoff` para la topologia actual:
  - leer FLT como paths motor-relative;
  - comparar contra commit/diff productivo de `repo_motor`;
  - aceptar una entrega correcta sin `--scope-override`;
  - seguir bloqueando rondas vacias o cambios fuera de FLT.
  - normalizar superficies operativas a `topologia motor/destino`;
  - inyectar `repo_motor_root` efimero al Builder sin persistir rutas absolutas locales.
- **Referencias historicas incorporadas:**
  - `WT-2026-206`: scope gate y cierres manuales en workspace+motor.
  - `WT-2026-215`: operaciones git del tooling resuelven `motor_root`.
  - `WT-2026-226a`: seam de evidencia comun entre `mark-ready` y review packet.
  - `WT-2026-228a`: pre-handoff bloquea motor sucio sin commit.
  - `WT-2026-231a`: pre-handoff ya commitea/taggea `repo_motor`; dejo este falso
    positivo en `mark-ready` como deuda explicita.
  - `WT-2026-221c`: scope watch temprano es adyacente, no sustituto.
  - `WT-2026-209`: nomenclatura `Modelo B` absorbida.
- **Sketch:**
  1) Identificar en `.agent/agent_controller.py` el camino exacto de `--mark-ready`:
     `parse_files_likely_touched`, `get_changed_files`, `check_scope_gate`,
     `resolve_evidence` y errores `No Files Likely Touched match git changes`.
  2) Extraer helper motor-aware reutilizable para leer FLT raw y evidencia/diff de
     `repo_motor`, sin resolver contra `PROJECT_ROOT`.
  3) Cuando existe evidencia productiva reciente en `repo_motor` para el ticket activo,
     el scope gate compara `motor-relative` contra `motor-relative`.
  4) Si no hay evidencia en motor, conservar el comportamiento actual de bloqueo por
     falta de implementacion.
  5) Si hay cambios fuera de FLT en motor, bloquear con lista `motor-relative`.
  6) Mantener `--scope-override` solo como escape auditado, no como camino normal.
- **Tests requeridos:**
  - `mark-ready` en topologia motor/destino con commit real en `repo_motor` dentro de
    FLT pasa sin `--scope-override`.
  - `mark-ready` con commit motor fuera de FLT bloquea y lista paths motor-relative.
  - `mark-ready` sin commit/diff productivo sigue bloqueando por no evidence.
  - `parse_files_likely_touched()` legacy no contamina el path motor-aware.
  - regresion de `WT-2026-231a`: pre-handoff sigue commiteando/taggeando.
- **Criterio:** el cierre normal Builder -> pre-handoff -> mark-ready funciona en
  topologia motor/destino sin scope override cuando la entrega productiva esta dentro
  de FLT; validate queda 0/0.
- **Non-goals:** no reescribir historia cerrada completa; no eliminar `--scope-override`.
- **Depende de:** WT-2026-231a, WT-2026-226a, WT-2026-215.
- **Origen:** session-2026-06-05-mark-ready-motor-aware


## WT-2026-222 - Higiene de suite: reset determinista del cache de project_root entre tests
- **Prioridad:** Media
- **Scope:** system/testing-hygiene
- **Estado:** completed
- **Problema:** 	ests/unit/test_project_root_resolution.py pasa aislado pero falla dentro de la suite global por contaminacion de orden/cache en la resolucion de 
untime.project_root. Mientras esto siga asi, la suite global no vuelve a ser una senal fiable y WT-2026-208 queda solo parcialmente estabilizado.
- **Objetivo:** hacer que la resolucion de project_root sea determinista entre tests, ya sea limpiando cache global en fixture/teardown o endureciendo el contrato del modulo para que no fugue estado entre casos.
- **Sketch inicial:** identificar el cache compartido en 
untime.project_root, anadir fixture o helper de reset reutilizable para la familia afectada, y rerun de la suite para demostrar que 	est_project_root_resolution.py deja de variar por orden.
- **Criterio:** 	ests/unit/test_project_root_resolution.py pasa tanto aislado como dentro de la suite global; la clasificacion como "contaminacion de suite" deja de ser necesaria.
- **Depende de:** WT-2026-208.

## WT-2026-243a - Cierre de sesion documental, snapshot local y memoria de arranque
- **Prioridad:** Media
- **Scope:** system/session-closeout-hygiene
- **Estado:** completed
- **Nota de cierre 2026-06-09:** completado documentalmente con actualizacion
  de `PROJECT.md`, `CHANGELOG.md`, `MEMORY.md`, `AUDIT.md` y reconciliacion del
  backlog local.
- **Problema:** tras el cierre tecnico de `WT-2026-242a/b/c`, el siguiente chat
  todavia depende de leer artefactos dispersos para reconstruir contexto:
  `PROJECT.md` estaba en placeholders, faltaba un `.agent/runtime/audit/AUDIT.md`
  local y la memoria de `repo_destino` no registraba explicitamente el valor de
  ese snapshot para arranques rapidos.
- **Objetivo:** consolidar un paquete ligero de cierre de sesion en
  `repo_destino`: documentacion durable actualizada, snapshot de auditoria
  local, revision de versiones/SHAs recientes y mejora de memoria solo en wing
  `project`.
- **Criterio:**
  - `PROJECT.md` y `CHANGELOG.md` actualizados con estado real;
  - `.agent/runtime/audit/AUDIT.md` presente y fresco;
- memoria local con decision explicita y sin promover nada a `repo_motor`;
- `validate --json` del `repo_destino` sin errores ni warnings.
- **Depende de:** WT-2026-242c.
- **Origen:** session-2026-06-09-closeout.

## WT-2026-244a - Formalizar policy de mergeabilidad y review inspirada por FrontierCode
- **Prioridad:** Alta
- **Scope:** system/review-quality-policy
- **Estado:** pending
- **Problema:** `AUDIT_FRONTIERCODE_LEARNINGS.md` ya destila una policy concreta
  a partir de FrontierCode, pero todavia no esta convertida en contrato
  builder-facing. Si se deja solo como audit, el siguiente ciclo puede volver a
  discutir el principio sin aterrizarlo en reglas operativas.
- **Objetivo:** documentar en superficies durables del `repo_destino` una
  policy minima de mergeabilidad: `validate --json` como gate de cierre
  existente con `0 warnings estructurales`, secuencia `allowlist -> gate`,
  reverse-classical solo para bugfixes con etiqueta
  `[NON-REVERSE-CLASSICAL: ...]`, separacion `BLOCKERS`/`NITS`, y
  reconocimiento explicito de `scope discipline` y `code quality /
  conventions`.
- **Criterio:** `PROJECT.md` y `AGENTS.md` reflejan la policy sin crear un gate
  nuevo; el audit consolidado sigue siendo la referencia argumental; el ticket
  cierra con `validate --json` limpio en `repo_destino`.
- **Depende de:** WT-2026-243a.
- **Origen:** session-2026-06-09-frontiercode.



## WT-2026-246a - Endurecer guard M3 y clarificar recuperacion del Builder
- **Prioridad:** Alta
- **Scope:** system/mark-ready-m3-hardening
- **Estado:** completed
- **Problema:** el guard de `--mark-ready` aceptaba checkpoints M3 que todavia
  eran ancestros de `HEAD` pero ya no anclaban el commit actual del `repo_motor`.
  Eso dejaba pasar un handoff con tag obsoleto. Ademas, las instrucciones del
  Builder no eran totalmente consistentes sobre como recuperarse cuando el
  checkpoint estaba stale.
- **Objetivo:** exigir que `checkpoint/review-<ticket>` coincida con el `HEAD`
  actual del `repo_motor`, cubrir la regresion con tests y alinear prompts/skills
  del Builder para que la recuperacion correcta sea relanzar
  `--pre-handoff --json --force`, no usar `--scope-override`.
- **Contexto clave:**
  - la implementacion ya esta precompletada en el arbol de trabajo del motor;
  - `WT-2026-245c` ya esta cerrado y sus superficies de colaboracion no deben
    contaminar el commit productivo de `246a`;
  - si `STATE.md`, `TURN.md` o `execution_log.md` siguen sucios en el motor, el
    scope gate puede bloquear `--mark-ready` aunque la entrega tecnica sea valida.
- **Criterio:** `--mark-ready` bloquea un M3 stale; tests focales verdes;
  `validate --json` limpio; commit visible de `WT-2026-246a`; instrucciones del
  Builder alineadas con la recuperacion canonica.
- **Depende de:** WT-2026-245c.
- **Origen:** session-2026-06-10-m3-hardening.

## WT-2026-246b - Idempotencia del closeout del launcher y guard autoritativo post-success
- **Prioridad:** Alta
- **Scope:** system/launcher-closeout-idempotency
- **Estado:** completed
- **Problema:** el ciclo de `WT-2026-246a` mostro que el Builder puede cerrar
  correctamente (`BUILDER_EXIT` + `STATE_CHANGED -> READY_FOR_REVIEW`) y aun asi
  el launcher volver a ejecutar `--pre-handoff` y `--mark-ready` desde su bloque
  `finally`. El controller contiene el segundo intento como `STALE_BUILDER_ORPHAN`,
  pero el ruido sigue llegando al bus y complica el diagnostico operativo.
- **Objetivo:** hacer idempotente el closeout del launcher para que, antes de
  lanzar `pre-handoff/mark-ready`, consulte el estado autoritativo del ticket y
  salte el closeout si el ticket ya esta en `READY_FOR_REVIEW`, `READY_TO_CLOSE`,
  `HUMAN_GATE` o `COMPLETED`.
- **Contexto clave:**
  - el stale guard del controller funciona y no debe debilitarse;
  - el problema esta en origen: el launcher no sabe que el closeout ya ocurrio;
  - `.opencode/opencode.json` puede quedar modificado por drift de restauracion
    del launcher y `nul` aparece como artefacto untracked del runtime Windows;
  - no existe todavia un flag CLI explicito para consultar el estado autoritativo
    del ticket desde el launcher.
- **Entregables esperados:**
  - exponer un flag CLI explicito en `agent_controller.py` para estado autoritativo
    del ticket (p. ej. `--json-state`);
  - usar ese estado en `Add-BuilderCloseout` para saltar closeout post-success;
  - loggear el skip con `ticket_id`, `round` y `bus_state`;
  - restaurar `.opencode/opencode.json` de forma exacta al finalizar el launcher;
  - limpiar/contener el artefacto `nul` sin mezclarlo con el ticket activo;
  - test de integracion que pruebe doble closeout sin ruido extra de bus.
- **Criterio:** tras un `mark-ready` exitoso, una segunda pasada del `finally`
  no emite `HANDOFF_BLOCKED`, `STALE_BUILDER_ORPHAN` ni un segundo `BUILDER_EXIT`;
  el launcher registra un skip limpio; `.opencode/opencode.json` no queda dirty;
  `nul` no reaparece como untracked; `validate --json` final sin errores.
- **Non-goals:**
  - no tocar la semantica del stale guard del controller;
  - no mover `_release_builder_lock()` fuera del controller;
  - no mezclar este ticket con el problema de autenticacion del Manager.
- **Depende de:** WT-2026-246a.
- **Origen:** session-2026-06-10-launcher-closeout.

## WT-2026-247a - Higiene de suite: aislamiento de tests y bugs de regex/mock/lock
- **Prioridad:** Media
- **Scope:** system/testing-hygiene
- **Estado:** completed
- **Problema:** 7 tests de la suite fallan por dos causas distintas:
  - **Grupo A - Contaminacion de estado real (3 tests):** tests que leen archivos
    reales del workspace (builder_lock.txt con PID de WT-2026-240a,
    execution_log.md con datos de sesion activa). No aislan su entorno.
    - `tests/test_builder_lock.py::test_lock_schema_does_not_contain_pid`
    - `tests/test_review_packet_evidence_gate.py::test_evidence_gate_passes_with_motor_evidence`
    - `tests/test_review_packet_evidence_gate.py::test_integration_gate_passes_with_motor_evidence`
  - **Grupo B - Bugs en el propio test (4 tests):**
    - `tests/test_builder_lock.py::test_lock_schema_contains_required_fields`: regex
      WP-\d{4}-\d+ no matchea prefijo WT-; debe actualizarse al patron canonico.
    - `tests/test_builder_lock.py::test_launcher_does_not_write_pid`: el launcher
      PowerShell todavia escribe campo pid; verificar si es bug real o expectativa
      incorrecta del test antes de corregir.
    - `tests/test_motor_root_gates.py::test_regression_cwd_project_root_breaks_check`:
      mock drift ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â los metodos monkeypatched no tienen efecto en la funcion real.
    - `tests/test_scope_gate.py::test_mark_ready_blocks_on_zero_overlap`:
      `_release_builder_lock` se llama cuando el test espera que no se llame;
      probable bug en el orden de guards.
- **Criterio:** los 7 tests pasan; tests del Grupo A usan tmp_path o fixtures
  aislados; tests del Grupo B con bugs corregidos en logica o expectativa segun
  corresponda; ruff limpio; validate sin errores.
- **Nota:** para el launcher/pid (Grupo B), verificar antes si es un bug real del
  launcher o un cambio de contrato no documentado.
- **Depende de:** WT-2026-245c.
- **Origen:** session-2026-06-10-preexisting-failures.

## WT-2026-248a - Stabilize .opencode/opencode.json: exact launcher restore and integrity guard in pre-handoff
- **Prioridad:** Media
- **Scope:** system/opencode-config-stability
- **Estado:** completed
- **Problema:** el launcher inyecta permisos runtime en `.opencode/opencode.json` y al
  restaurarlo usa escritura PowerShell 5.1 que introduce BOM o drift de serializacion sobre un
  archivo trackeado del `repo_motor`. Ese residuo ensucia git y bloquea `--pre-handoff` en
  tickets no relacionados. El ruido ya aparecio en `WT-2026-246a`, `WT-2026-246b` y
  `WT-2026-247a`.
- **Causa raiz verificada:**
  - `git diff HEAD -- .opencode/opencode.json` muestra un drift minimo tipo `-{` / `+BOM{`.
  - El `finally` interno del launcher restaura con escritura PS5.1 y no garantiza bytes identicos a `HEAD`.
  - El archivo versionado no debe persistir permisos runtime del `repo_destino`.
- **Objetivo:** que al terminar el ciclo del Builder, `.opencode/opencode.json` quede identico
  a `HEAD` sin intervencion manual, tanto en camino feliz como en camino de fallo, sin borrar
  cambios legitimos de configuracion.
- **Alcance:**
  - Paso 1 - Fix raiz en launcher: restauracion byte-exact del archivo original, o un mecanismo equivalente que garantice diff vacio al salir del `finally`.
  - Paso 2 - Guard de integridad en `--pre-handoff`: si `.opencode/opencode.json` sigue dirty y no esta en `Files Likely Touched`, solo autocorregir cuando el diff coincide exactamente con el residuo BOM permitido; si hay cualquier cambio semantico adicional, bloquear.
  - Paso 3 - Tests de regresion y evidencia operativa: cubrir ciclo normal, ciclo abortado/fallido, prueba negativa y visibilidad del stderr de autocorreccion.
- **Files Likely Touched:**
  - `scripts/launch_agent_terminals.ps1`
  - `.agent/agent_controller.py`
  - `tests/test_opencode_config_stability.py`
- **Criterio:** despues de un ciclo completo del launcher, `git diff HEAD -- .opencode/opencode.json` devuelve output vacio en camino feliz y en camino de fallo. `--pre-handoff` deja de bloquear por el drift exacto del launcher, pero sigue bloqueando cambios semanticos no declarados en FLT. Ruff limpio. Tests verdes.
- **Depende de:** WT-2026-246b.

## WT-2026-249a - Hardening minimo del contrato CLI: stderr vs returncode
- **Prioridad:** Media
- **Scope:** system/cli-output-contract
- **Estado:** completed
- **Problema:** algunos consumers externos estan tratando cualquier contenido
  en `stderr` como fallo, pero el controlador mezcla rutas de error fatal
  (`returncode 1`) con rutas de warning no fatal (`returncode 0`) escritas
  tambien a `stderr`. Eso contamina email, CI o wrappers con falsos positivos.
- **Objetivo:** aplicar un hardening minimo del contrato observable:
  - eliminar `stderr + returncode 0` en la rama `stale_builder_orphan`;
  - clasificar el wrapper de `session close` por `returncode`, no por parseo
    textual;
  - cubrir ambos casos con tests focales y validar que `tests/test_agent_controller.py`
    completo sigue verde.
- **Criterio:** stale orphan retorna `0` sin `stderr` ni eventos al bus; session
  close exitoso no propaga `stderr`; session close fallido si lo propaga;
  tests focales, `ruff` y `validate` verdes; commit visible de `WT-2026-249a`.
- **Depende de:** WT-2026-248a.
- **Origen:** session-2026-06-10-cli-contract-hardening.

## WT-2026-249b - Excluir BUILDER_BRIEF_ del guard de superficies vivas del workspace
- **Prioridad:** Media
- **Scope:** system/pre-handoff-live-surfaces
- **Estado:** pending
- **Problema:** durante `WT-2026-249a`, el guard de `--pre-handoff` trato
  `.agent/collaboration/BUILDER_BRIEF_WT-2026-249a.md` como drift fuera de
  scope y genero `HANDOFF_BLOCKED` espurio. El mismo incidente tambien incluyo
  `UPSTREAM_LEARNINGS.md`, pero ambos artefactos no deben resolverse igual.
- **Objetivo:** reconocer `BUILDER_BRIEF_` como superficie viva/no bloqueante
  del workspace, con cobertura de regresion, sin ampliar exclusiones a memoria
  ni tocar `UPSTREAM_LEARNINGS.md`.
- **Criterio:** existe una exclusion unica
  `".agent/collaboration/BUILDER_BRIEF_"`; `BUILDER_BRIEF_WT-*` deja de
  bloquear `--pre-handoff`; `UPSTREAM_LEARNINGS.md` sigue fuera de exclusiones;
  tests focales + `tests/test_agent_controller.py` completos verdes.
- **Depende de:** WT-2026-249a.
- **Origen:** session-2026-06-11-builder-brief-followup.

## WT-2026-249c - Review bridge: normalizar parseo de CHANGES y evitar degradacion espuria a INSPECT
- **Prioridad:** Alta
- **Scope:** system/review-bridge-parser
- **Estado:** pending
- **Problema:** WT-2026-249b llego correctamente a READY_FOR_REVIEW, pero la decision del Manager acabo materializada como INSPECT y el bus cayo en HUMAN_GATE. La evidencia apunta a un bug de parser en us/review_bridge.py: el extractor de json_last_text guarda la primera decision del stream en vez de la ultima, y ademas existe una degradacion deliberada de json_last_text -> INSPECT que puede convertir una review valida en escalado humano.
- **Objetivo:** aislar el fix minimo del parser para que una review valida DECISION: CHANGES no termine como INSPECT por errores de interpretacion del stream NDJSON.
- **Criterio:** verificar primero si el Manager real emite phase:"final_answer" en el caso de 249b; si no lo hace de forma autoritativa, corregir Bug #1 (first-vs-last) y Bug #2 (degradacion de json_last_text) con tests de barrera sobre NDJSON realista. Sin tocar payload estructurado, gent_controller.py, supervisor.py ni reglas de HUMAN_GATE.
- **Depende de:** WT-2026-249b.
- **Origen:** session-2026-06-11-review-bridge-parser.


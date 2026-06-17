# Execution Log: WOT-2026-010h - Propagar prefijo per-project a prompts

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-010h
- **Contract ID:** T-010H-001
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010a` (completed) fijo el glosario de nomenclatura y el gate
  `check_ticket_nomenclature.py`; 010h propaga la regla de prefijo per-project a
  los prompts de arranque/auditoria que aun no la explicitan.
- `WOT-2026-010l` (completed, motor 915d2be) cerro el ciclo anterior; su
  archivado de `STRATEGY_`/`AUDIT_` se ejecuta al arrancar 010h (ver nota de
  arranque).

## Fase 0 - COMPLETED

### Diagnosis (2026-06-17)

**Reference wording in session_bootstrap.md:**
- Line 59: `Ticket prefix: XXX` declarado en el `PROJECT.md` local del destino — contradice el nuevo orden de fuente (AGENTS.md/CLAUDE.md primario, no PROJECT.md)
- Line 62: Validate verifica `Ticket prefix:` — OK como mecanismo de verificacion, no identifica fuente
- Line 88: "namespace local definido en `PROJECT.md`" — misma contradiccion que linea 59

**Gap por prompt:**
| Prompt | Estado pre-cambio | Gap |
|--------|-------------------|-----|
| `session_bootstrap.md` | Lineas 59,88 citan PROJECT.md como fuente (incorrecto segun nuevo contrato) | Corregir fuente primaria a AGENTS.md/CLAUDE.md |
| `destination_bootstrap.md` | 1 mencion parcial (validate dice "prefijo de tickets") | Sin explicacion de fuente real ni distincion WOT-=motor |
| `audit_complete_motor_destination.md` | **0 menciones** | Gap completo sin mencion de prefijo |
| `audit_post_change_system_health.md` | **0 menciones** | Gap completo sin mencion de prefijo |

**Contradiccion preexistente detectada:**
- `session_bootstrap.md` lineas 59, 88: declaran que el prefijo se define en `PROJECT.md`. El nuevo contrato exige que la fuente primaria sea `AGENTS.md`/`CLAUDE.md` autocargado del destino, con `--validate` como verificacion. `PROJECT.md` no debe usarse como fuente primaria de prefijo.

**Ejemplos WP-/WT- legacy existentes (inocuos):**
- `session_bootstrap.md` linea 60: `WP-2026-067` (historial de commit)
- `session_bootstrap.md` linea 100: `WP-2026-120` (historial de commit)
- `audit_complete_motor_destination.md` linea 525: `AUDIT_WT-*`, `AUDIT_WP-*` (referencia de protocolo legacy-compat)
- `audit_post_change_system_health.md` linea 130: `WOT-2026-003d` (referencia ticket motor)
- No se introduciran ejemplos vivos nuevos WP-/WT-.

### Notas de arranque (Manager)

- Premisas re-verificadas read-only por el Manager el 2026-06-17: regex
  per-project vigente en `bus/ticket_id.py`; gap confirmado por grep en los 4
  prompts.
- **Deuda de archivado controlada:** los artefactos `STRATEGY_WOT-2026-010l.md`
  / `AUDIT_WOT-2026-010l.md` siguen vivos porque el archivador excluye el ticket
  activo; ahora que el work_plan apunta a 010h, deben archivarse con
  `scripts/archive_collaboration_artifacts.py` y COMMITEARSE en el mismo arranque
  para no dejar delete+untracked (incidente reconciliado en 010l).
- Preflight esperado para Builder: runtime bootstrap + `validate --json` 0/0
  antes de tocar codigo.

## Fase 1 - COMPLETED

### Cambios realizados (repo_motor, commit 8dbfcda)

| Prompt | Cambio | Lineas |
|--------|--------|--------|
| `prompts/session_bootstrap.md` | Linea 59: `PROJECT.md` -> `AGENTS.md/CLAUDE.md` como fuente primaria; anadido `WOT-` es SOLO motor/dogfooding; se verifica via `--validate`. Linea 88: mismo cambio. | 59, 88 |
| `prompts/destination_bootstrap.md` | Nueva seccion **Regla de prefijo de tickets** tras vocabulario canonico: fuente = AGENTS.md/CLAUDE.md; WOT- = motor; verify via --validate. | 50 |
| `prompts/audit_complete_motor_destination.md` | Nueva linea en Contexto del sistema: regla de prefijo per-project. | 37 |
| `prompts/audit_post_change_system_health.md` | Nueva linea en Donde viven las cosas: regla de prefijo per-project. | 45 |

### Quality gates

- `python scripts/check_ticket_nomenclature.py` -> exit 0. "No active generator uses a legacy prefix." 0 generator, 98 history, 9 legacy-tagged.
- `python scripts/check_encoding_guard.py prompts/session_bootstrap.md prompts/destination_bootstrap.md prompts/audit_complete_motor_destination.md prompts/audit_post_change_system_health.md` -> exit 0, no output (all clean).
- `python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -> exit 0. 0 errors, 1 warning (bus_drift transitorio pre-handoff esperado).
- Ruff: no aplica (ticket sin Python tocado).
- State-leak: silencioso.


Manager approved canonical closeout for WOT-2026-010h
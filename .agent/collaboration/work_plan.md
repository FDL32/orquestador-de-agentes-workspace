# Work Plan: WOT-2026-002c - A2d retirar copias motor-provides + ejecutar decisiones

## Metadata
- **ID:** WOT-2026-002c
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-A2d
- **Titulo:** Retirar del destino las copias motor-provides y ejecutar las decisiones de huerfanos
- **Asignado a:** Builder
- **Severidad:** Alta | **Riesgo:** Alto (blast radius ~168 archivos). Reversible via git.
- **Origen:** WOT-AUDIT-A2 / triage_manifest.md + decisiones WOT-2026-002b

## Decision Arquitectonica
El destino deja de vendorizar el tooling del motor: lo referencia externamente
(host-extends, probado en WOT-2026-002a). La retirada es por BUCKETS en COMMITS
SEPARADOS para reducir blast radius y permitir revert granular. Lo muerto-pero-unico
se ARCHIVA a `_legacy/`; lo motor-provides se hace `git rm` (el motor tiene la copia
canonica). Toda la operacion es `git rm`/`git mv` + commit: recuperable.

## Inventario por bucket
### Bucket 1 - motor-provides -> git rm (163) [FASE 2 HECHA: bf451f2]
- `agent_system/` (113), `skills/` (41), 7 scripts (run_pytest_safe, discover_skills,
  upgrade_agent_system, detect_agent_system_version, test_refactoring_impact,
  test_refactor_kit_portable, test_refactor_kit_performance),
  `tests/test_event_bus_hygiene.py` (1).
- `.agent/README.md`: STOP#3 -> CUSTOMIZADO vs motor -> destino-keep, NO retirado.

### Bucket 2 - archive-legacy -> git mv a _legacy/ (7) [FASE 1 HECHA: 1a2d700]
- 5 scripts del cluster + `tests/test_ticket_007_context_recovery.py` + `.goosehints`.

### Bucket 3 - installer-managed (3) [FASE 3 DIFERIDA -> ver STOP#7]
- `.agent/hooks/pre_compact_hook.py`, `.agent/microagents/onboarding.md`,
  `.agent/glossary.md`. DIFERIDOS a follow-up: el mecanismo de re-sync previsto
  (`install --sync`) re-vendoriza el bundle COMPLETO en el destino (re-crea
  agent_system/ + caches), contradiciendo A2d. Se conservan como destino-keep hasta
  un install host-extends-aware (follow-up de motor).

## Files Likely Touched
- `agent_system/`
- `skills/`
- `scripts/`
- `tests/`
- `_legacy/`
- `orchestrator_pipeline/reports/closeout_WOT-2026-002c.md`
- `.agent/collaboration/execution_log.md`

## Superficies
- **Builder (modifica):** Buckets 1 y 2; `_legacy/`; reporte y `execution_log.md`.
- **Read/inspect only:** `triage_manifest.md`, `orphans_decision_WOT-2026-002b.md`,
  arbol del motor para paridad. NO editar el motor.
- **Manager-only:** doble review adversarial; verificacion de que ningun flujo vivo
  se rompe y de que el destino sigue operando via motor externo.

## Non-goals
- NO tocar el motor (read-only).
- NO retirar destino-keep (.agent/collaboration|runtime|config|audits|docs, .claude,
  docs de identidad de raiz, `.agent/README.md` customizado).
- NO usar `install --sync` para re-provisionar (re-vendoriza el bundle completo).

## Criterios binarios de cierre (alcance: FASE 1 + FASE 2)
- [x] `git ls-files` sin `agent_system/`, `skills/`, los 7 scripts motor-provides,
      `tests/test_event_bus_hygiene.py` (Bucket 1, bf451f2).
- [x] Bucket 2 (7) en `_legacy/` (1a2d700).
- [ ] `agent_controller --validate --project-root .` = 0/0.
- [ ] Clone limpio + motor externo opera SIN las copias retiradas (exit codes reales).
- [ ] Workflow CI no referencia copias retiradas (grep vacio).
- [ ] Bucket 3 diferido y documentado como follow-up de motor (install host-extends-aware).
- [ ] Follow-up de motor (gates-dispatch sin tests locales) creado en backlog.

## STOP / escalado (activados durante la ejecucion)
- **STOP#3 ACTIVADO:** `.agent/README.md` customizado vs motor -> destino-keep, NO retirado.
- **STOP#7 (nuevo, FASE 3):** `install --sync` re-vendoriza el bundle completo
  (re-crea `agent_system/` + caches en el destino) y borro deliverables destino-keep
  en el working tree durante el re-provision. Es la herramienta EQUIVOCADA para
  host-extends. FASE 3 (installer-managed) se DIFIERE: los 3 archivos se conservan como
  destino-keep hasta que el motor ofrezca un install host-extends-aware. Recuperado el
  estado limpio post-FASE-2 via git restore (sin tocar 1a2d700/bf451f2).
- STOP#1/#2: 0 invocadores vivos / paridad de skills OK (FASE 0 limpia).

## Gates (deliverable_type: code; ticket de retirada)
- `agent_controller --validate --project-root .` 0/0.
- Clone limpio + motor externo (install --sync, discover, validate) con exit codes
  reales SIN las copias (host-extends post-retirada).
- Workflow CI: grep sin refs a copias retiradas.
- ruff/pytest-safe contra el destino: N/A (retirada via git rm/mv; sin Python editado;
  tests/ motor-provides retirado -> pytest-local no aplica). Gate de codigo = clone-demo.
- Integridad motor: `check_motor_pristine --check` vs snapshot.

## Riesgos
- Alto blast radius (~163 retirados) pero reversible via git. Mitigacion: commits por
  bucket, FASE 0 de reconciliacion, STOPs duros, verificacion por clone-demo.
- FASE 3 diferida limpiamente (install --sync inadecuado); sin perdida (los 3 archivos
  permanecen).

## Entregables
- Destino sin Bucket 1 (163 motor-provides); `_legacy/` con Bucket 2 (7).
- Bucket 3 conservado (destino-keep) + follow-up de motor documentado.
- `orchestrator_pipeline/reports/closeout_WOT-2026-002c.md` con git ls-files
  antes/despues, clone-demo, el incidente install --sync y los follow-ups.
- Entradas de backlog (scope motor): install host-extends-aware + gates-dispatch sin
  tests locales.

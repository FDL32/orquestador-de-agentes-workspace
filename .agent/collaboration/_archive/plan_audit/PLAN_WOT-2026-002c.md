# PLAN WOT-2026-002c - A2d retirada de copias motor-provides

## Objetivo
Espejo tecnico de `work_plan.md`. Retirar las copias motor-provides del destino por
buckets en commits separados, archivar el set muerto a `_legacy/`, retirar los 3
installer-managed con re-sync, y verificar que el destino sigue operando via motor.

## Pasos de ejecucion
1. **Fase 0 - Reconciliacion (read-only):**
   - Snapshot del motor ya capturado (`motor_before_WOT-2026-002c.json` se crea al inicio).
   - Para cada motor-provides (7 scripts, skills, tests/test_event_bus_hygiene,
     .agent/README.md): `git -C <destino> grep -n "<basename>"` y filtrar invocadores
     que NO sean `agent_system/`, cluster muerto, `_legacy/`, `.claude/settings.local.json`
     (gitignored), ni el CI rediseniado. Si queda invocador vivo trackeado -> STOP#1.
   - Skills: por cada dir/archivo bajo `skills/`, confirmar que existe en
     `<motor>/skills/`. Si alguno no existe en el motor -> STOP#2 (destino-keep).
   - `.agent/README.md`: `diff` vs `<motor>/.agent/README.md`; si customizado -> STOP#3.
   - `pre_compact_hook`: leer `.claude/settings.json`, localizar el wiring de PreCompact;
     determinar si resuelve al hook del motor o al del destino.
2. **Fase 1 - archive-legacy (commit 1):**
   - `mkdir -p _legacy/scripts _legacy/tests`
   - `git mv` los 5 scripts del cluster a `_legacy/scripts/`, `test_ticket_007...` a
     `_legacy/tests/`, `.goosehints` a `_legacy/`.
   - Commit: `chore(WOT-2026-002c): archive dead legacy to _legacy/`.
3. **Fase 2 - motor-provides (commit 2):**
   - `git rm -r agent_system/`; `git rm -r skills/` (si paridad OK); `git rm` los 7
     scripts; `git rm tests/test_event_bus_hygiene.py`; `git rm .agent/README.md` (si no
     customizado).
   - Commit: `feat(WOT-2026-002c): remove motor-provides vendored copies`.
4. **Fase 3 - installer-managed (commit 3):**
   - Si el wiring de PreCompact resuelve al destino: ajustar `.claude/settings.json` para
     que apunte al hook del motor (o a una resolucion que funcione sin la copia del destino).
   - `git rm .agent/hooks/pre_compact_hook.py .agent/microagents/onboarding.md .agent/glossary.md`.
   - `python <MOTOR>/scripts/install_agent_system.py --sync --dest <destino>` para
     re-provisionar onboarding/glossary (verificar que reaparecen como installer-managed).
   - Commit: `feat(WOT-2026-002c): remove installer-managed copies + re-sync`.
5. **Fase 4 - verificacion:**
   - `validate --project-root .` 0/0.
   - Clone limpio del destino + `install --sync` + `discover_skills` + `validate` del
     motor con `AGENT_PROJECT_ROOT=<clone>`; exit codes reales (host-extends sin copias).
   - `grep` del workflow CI: no referencia copias retiradas.
   - `check_motor_pristine --check` vs snapshot.
6. **Fase 5 - follow-up:**
   - Documentar el follow-up de pytest en el closeout.
   - Anadir entrada de backlog (scope motor) para `run_gates_dispatch` sin tests locales.

## Seams / invariantes
- Reversibilidad: `git rm`/`git mv` + commit por bucket. El motor tiene las copias
  canonicas; el set muerto vive en `_legacy/`.
- host-extends: el destino opera con el motor externo (probado en 002a).
- El motor es read-only; toda escritura ejecutable es en el destino o un clone.

## Evidencia esperada
- `git ls-files` antes/despues por bucket.
- exit codes del clone-demo post-retirada.
- validate 0/0; check_motor_pristine limpio.

## STOP
- Ver STOP#1..#6 del work_plan. Cualquier invocador vivo trackeado, skill sin
  equivalente, README customizado, o wiring irresoluble -> NO retirar esa pieza, escalar.

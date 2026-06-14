# AUDIT WOT-2026-002c - A2d retirada de copias motor-provides

## Objetivo del audit
Verificar que la retirada (a) NO rompe ningun flujo vivo trackeado, (b) deja el destino
operando via motor externo, (c) es reversible y por buckets, (d) respeta destino-keep,
y (e) el motor permanece intacto.

## Reglas de revision
- Revisar `git ls-files` real antes/despues, no el relato.
- Confirmar que Fase 0 demostro 0 invocadores vivos trackeados (grep citado) para cada
  pieza retirada por git rm.
- Confirmar que el clone-demo post-retirada opera con exit codes reales.
- Confirmar que el set muerto esta en `_legacy/` (no borrado a tumba) y los 3
  installer-managed se re-provisionan.
- Confirmar que NO se retiro ninguna ruta destino-keep.
- Confirmar motor intacto (`check_motor_pristine`).

## Hallazgos bloqueantes tipicos
- CRITICO: se retiro una copia con invocador vivo trackeado sin equivalente en motor.
- CRITICO: se retiro una ruta destino-keep (.agent/collaboration|runtime|config|audits|
  docs, .claude, docs de identidad de raiz).
- CRITICO: el destino ya NO opera via motor (clone-demo falla por la retirada, no por tests/).
- CRITICO: se toco el motor (check_motor_pristine sucio).
- ALTO: una skill destino-custom (sin equivalente en motor) fue retirada.
- ALTO: pre_compact wiring quedo apuntando a una copia inexistente (PreCompact roto).
- ALTO: onboarding/glossary no se re-provisionaron y quedaron como gap.
- MEDIO: todo en un solo commit (sin revert granular por bucket).

## Evidencia minima esperada
- Fase 0: grep por pieza mostrando invocadores = solo (agent_system/cluster/gitignored/CI-redised) o ninguno.
- `git ls-files` post: sin agent_system/, skills/, 7 scripts, test_event_bus_hygiene, .agent/README.md.
- `_legacy/` con los 7; Bucket 3 retirado + re-sync log.
- Clone-demo: install --sync exit 0, discover exit 0, validate del clone, todos SIN copias.
- validate destino 0/0; check_motor_pristine limpio; CI workflow grep vacio de copias.

## TP Check
TP-01: Fase 0 demostro 0 invocadores vivos trackeados para cada git rm (grep citado). (grep)
TP-02: git ls-files post sin las copias motor-provides del Bucket 1. (git)
TP-03: Bucket 2 (7) archivado a `_legacy/`, no borrado a tumba. (git)
TP-04: Bucket 3 retirado; onboarding/glossary re-provisionados por install --sync. (git/log)
TP-05: pre_compact wiring resuelve al hook del motor (PreCompact no roto). (settings.json)
TP-06: clone-demo post-retirada opera (install/discover/validate exit codes reales). (exit codes)
TP-07: ninguna ruta destino-keep retirada. (git diff)
TP-08: validate 0/0; motor intacto; CI workflow sin refs a copias retiradas. (command/grep)
TP-09: commits separados por bucket (revert granular). (git log)
TP-10: follow-up de motor (gates-dispatch sin tests locales) creado en backlog. (backlog)

## Criterio de rechazo inmediato
- Se rompio un flujo vivo (invocador trackeado sin equivalente).
- Se retiro destino-keep o se toco el motor.
- El clone-demo post-retirada no opera via motor.
- Set muerto borrado a tumba en vez de `_legacy/` sin orden explicita.

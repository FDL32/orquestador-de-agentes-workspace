# STRATEGY_WOT-2026-010i -- Review packet hardening

## Hechos verificados

- `010e` cerro con correcciones reales: commit visible, allowlist revertida,
  `destination_root` usado y tests de fallback honestos.
- Esos fallos llegaron a Manager antes de ser bloqueados por tooling. `010i`
  convierte las lecciones en barreras mecanicas y tests semanticos.
- `010q` ya protege la suite canonica; no duplicar esa responsabilidad.

## Plan tecnico

1. Leer `pre_handoff_guard.py`, `scope_gate.py` y el flujo de `--mark-ready`.
2. Reutilizar parsers existentes para extraer `Forbidden Surfaces`; si falta un
   helper, crearlo en el modulo que ya parsea contrato/scope.
3. Anadir una barrera de handoff que compare diff real contra Forbidden
   Surfaces y falle cerrado con diagnostico claro.
4. Anadir o endurecer la barrera de commit visible para tickets `code` y
   `mixed`, manteniendo excepciones documentales para `analysis`/`research`.
5. Anadir tests semanticos contra `_resolve_destino()` usando un link realista
   con `destination_root` distinto de `motor_root`.
6. Reemplazar cualquier test de fallback que dependa de import/PYTHONPATH por
   observacion directa de la funcion o del efecto de subprocess.
7. Documentar brevemente la regla resultante en
   `docs/protocol/review_packet_hardening_WOT-2026-010i.md`.

## Riesgos

- **Scope creep:** tocar politica de suite o selector focal. Debe quedar fuera.
- **Falso positivo:** Forbidden Surfaces con texto libre mal parseado. Usar una
  ruta por bullet y tests con notas no parseables.
- **Falso verde:** test semantico que solo comprueba que algo retorna, no el
  campo exacto.
- **Bloqueo documental:** no romper tickets `analysis` como `010p`.

## No hacer

- No tocar `run_pytest_safe.py`.
- No activar cache, xdist ni sharding.
- No editar bus manualmente.
- No reabrir cambios funcionales de `010e` salvo para tests de regresion.
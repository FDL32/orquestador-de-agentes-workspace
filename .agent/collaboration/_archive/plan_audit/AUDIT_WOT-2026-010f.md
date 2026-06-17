# AUDIT_WOT-2026-010f -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los Criterios Binarios de `work_plan.md`.

## Barreras (deben fallar sin el fix)

- [ ] `tests/unit/test_pre_handoff_checkpoint.py` existe y sus tests fallan si se
      revierte el fix (barrera real, no cosmetica).
- [ ] `test_pre_handoff_blocks_plan_id_none`: con `**ID:** none`, pre-handoff
      retorna != 0 y NO crea `checkpoint/review-none`. Debe fallar sin el fix
      (hoy el tag se crea).
- [ ] Parametrizado bloquea tambien `N/A`, `""`, `unknown`.
- [ ] `test_pre_handoff_allows_valid_ticket`: con ticket valido, el tag M3 se
      crea (no-regresion verificable).
- [ ] `test_mark_ready_blocks_plan_id_none`: `_handle_mark_ready` con `none` no
      emite eventos de bus (observado en events.jsonl, no mock). FALLA sin el fix.

## Contrato estructural

- [ ] Existe `INVALID_PLAN_IDS` + `is_invalid_plan_id` como fuente unica;
      contiene `"", "n/a", "none", "unknown"` y normaliza `strip().lower()`.
- [ ] Las **17** ubicaciones del guard debil + el guard fuerte (1780) consumen
      el helper. `grep -nE '(plan_id|ticket_id|current_plan_id) == "N/A"'
      agent_controller.py` -> 0 ocurrencias.
- [ ] El fix bloquea ANTES de cualquier efecto (tag, evento, mutacion) en las
      rutas de creacion/mutacion.
- [ ] `scripts/create_checkpoint.py` y `scripts/pre_handoff_guard.py` intactos
      (no reimplementados).

## Limpieza del tag

- [ ] Antes de borrar `checkpoint/review-none`: grep en
      `.agent/runtime/events` + `.agent/collaboration` confirma cero referencias.
- [ ] `git tag -l "checkpoint/review-none"` vacio al cierre.
- [ ] Ningun otro `checkpoint/review-*` valido fue borrado (comparar inventario
      antes/despues).

## Gates de cierre (mixed)

- [ ] Diff/commit productivo del ticket visible y revisable.
- [ ] `ruff check .` exit 0.
- [ ] `run_pytest_safe -- -m "not integration and not slow"` leido hasta `0 failed`.
- [ ] `validate --json --project-root <repo_destino>` exit 0, 0 errors.

## Anti-patrones a rechazar (Manager)

- Mock drift: el test mockea `git tag` en vez de ejercer la ruta real.
- Floor assertion: el test pasa aunque el guard no bloquee de verdad.
- Normalizacion en vez de rechazo: traducir `none` a otro valor en lugar de
  fallar fail-closed (el contrato exige RECHAZO).
- Borrado de tag sin verificar referencias vivas primero.
- Cambio fuera de FLT o mezcla con scope de 010d/010e/010i.

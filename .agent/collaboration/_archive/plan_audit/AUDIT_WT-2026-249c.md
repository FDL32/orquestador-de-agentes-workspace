# AUDIT WT-2026-249c - Review bridge: normalizar parseo de CHANGES y evitar degradacion espuria a INSPECT

## Tipo
code

## Veredicto esperado
APROBADO si el fix corrige el parser minimo del review bridge con barreras reales
sobre el stream NDJSON del caso `249b`, sin abrir scope hacia payloads, rework o
semantica general de `HUMAN_GATE`.

## Checklist de auditoria

### Fase 1 - Diagnostico real
- Verificar en `attempt-2.md` y artefactos asociados si el Manager emitio o no
  `phase:"final_answer"` util para la decision.
- Confirmar en codigo si el bug real del caso es:
  - Bug #1: primera vs ultima decision del stream;
  - escenario residual de `json_last_text` sin `final_answer` util;
  - o ambos.
- Verificar que `WT-2026-249b` ya no sigue vivo en `HUMAN_GATE` antes de activar `249c`.
- Verificar que la activacion canonica de `249c` actualizo `work_plan.md`, `STATE.md`
  y `TURN.md`, no solo el plan largo.

### Fase 2 - Alcance minimo
- El diff productivo debe limitarse a:
  - `bus/review_bridge.py`
  - `tests/test_review_bridge.py`
- Rechazar cambios en:
  - `.agent/agent_controller.py`
  - `bus/supervisor.py`
  - schema de eventos del bus
  - artefactos `REWORK_*` o payload estructurado de `CHANGES`

### Fase 3 - Barreras de regresion
- Debe existir `test_early_inspect_later_changes_returns_changes`.
- Debe existir test del canal realmente observado en `249b`.
- Si el fix toca el escenario residual de `json_last_text`, debe existir
  `test_no_final_answer_text_with_changes_returns_changes`.
- Debe existir `test_final_answer_phase_wins_as_regression` como no regresion del canal
  primario.
- No aceptar tests cosmeticos basados solo en substrings o constantes sin pasar
  por el parser real del bridge.

### Fase 4 - Riesgo de sobrecorreccion
- Si se habilita `json_last_text` como canal valido, revisar que siga habiendo
  una validacion minima o fixture realista que evite parsear ruido del prompt o
  del review packet como decision del Manager.
- Rechazar cualquier intento de resolver el problema cambiando la logica de
  `HUMAN_GATE` en vez del parser.

### Fase 5 - Gates
- `python -m pytest tests/test_review_bridge.py -v`
- `python scripts/run_pytest_safe.py`
- `python -m ruff check bus/review_bridge.py tests/test_review_bridge.py`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers explicitos
- No hay evidencia sobre si `249b` tuvo `final_answer` util, citada con evento o linea
  concreta en `execution_log.md`.
- El diff intenta arreglar `HUMAN_GATE` o `supervisor` en vez del parser.
- Falta test de barrera `INSPECT` temprano + `CHANGES` tardio.
- `WT-2026-249b` sigue vivo en `HUMAN_GATE` y `249c` intenta activarse encima de ese
  estado terminal no resuelto.
- La activacion de `249c` no actualizo canonicamente `work_plan.md`, `STATE.md` y `TURN.md`.
- Se mezclan payload estructurado, rework artifacts o cambios de schema del bus.

## Notas para Manager
- El objetivo no es redisenar el review bridge entero.
- El objetivo es impedir que una review valida `CHANGES` termine materializada
  como `INSPECT` por fallo de parser.
- Si la evidencia demuestra que `json_final_answer` era suficiente en `249b`, el
  fix puede quedarse en Bug #1 con justificacion explicita.

# PLAN WT-2026-249c - Review bridge: normalizar parseo de CHANGES y evitar degradacion espuria a INSPECT

## Metadata
- **ID:** WT-2026-249c
- **Title:** Review bridge: normalizar parseo de `CHANGES` y evitar degradacion espuria a `INSPECT`
- **Scope:** system/review-bridge-parser
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-249b

## Objetivo tecnico
Corregir el parser minimo de `bus/review_bridge.py` para que una review valida del
Manager con `DECISION: CHANGES` no se degrade erroneamente a `INSPECT` y no termine
en `HUMAN_GATE` por un problema de interpretacion del stream NDJSON.

El ticket debe mantenerse pequeno y binario: parser + tests de barrera. No debe
mezclarse con mejoras estructurales del payload, artefactos de rework o redisenos
amplios del review bridge.

## Contexto verificado
- En `WT-2026-249b`, el Builder entrego correctamente a review:
  - `1199 BUILDER_EXIT`
  - `1200`/`1201 STATE_CHANGED -> READY_FOR_REVIEW`
- El problema ocurrio en el review bridge:
  - `1206 MANAGER_REVIEW_ATTEMPT` con `parse_method: "json_last_text"`
  - `1207 REVIEW_DECISION` con `decision: "inspect"`
  - `1208 STATE_CHANGED -> HUMAN_GATE`
- El artefacto `attempt-2.md` conserva texto final del Manager con `DECISION: CHANGES`.
- Hay un bug confirmado en codigo dentro de `bus/review_bridge.py`:
  - Bug #1: `_extract_decision_from_text_events()` guarda la primera decision del
    stream (`if last_decision is None`) en vez de la ultima.
- Existe ademas un escenario residual a investigar en el canal `json_last_text`:
  - si el caso real de `249b` no tuvo `phase:"final_answer"` util, hay que verificar
    si el parser cae a `INSPECT` por leer una decision temprana incorrecta, por no
    encontrar la decision final, o por otra condicion real del stream;
  - el Builder no debe asumir una "politica" separada hasta demostrarla con evidencia
    del artefacto real.
- Antes de fijar el alcance final, el Builder debe verificar en `attempt-2.md` si el
  Manager real emitio eventos `phase:"final_answer"`. Esa evidencia determina si basta
  con Bug #1 o si tambien hay que corregir el escenario residual de `json_last_text`
  para el caso real.
- Antes de lanzar Builder, debe resolverse primero el estado terminal de `WT-2026-249b`
  en el bus. `249c` no debe activarse encima de un `HUMAN_GATE` vivo:
  - si `249b` queda cerrado por decision humana, materializar ese cierre primero;
  - si `249b` debe volver al ciclo, reabrirlo canonicamente antes de pasar a `249c`;
  - solo despues de resolver `249b`, actualizar canonicamente los tres archivos de
    estado del `repo_destino` a `WT-2026-249c`:
    - `work_plan.md` -> contenido activo de `WT-2026-249c` con estado `APPROVED`;
    - `STATE.md` -> `ACTIVE_TICKET: WT-2026-249c` y `STATUS: APPROVED`;
    - `TURN.md` -> `ROL: BUILDER`, `PLAN_ID: WT-2026-249c`, `ACCION: IMPLEMENT_WORK`.
  El cierre, el scope gate y `--validate` leen esas superficies vivas, no solo
  `PLAN_WT-2026-249c.md`.

## Alcance
- Verificar el comportamiento real del stream NDJSON de `249b`.
- Corregir el bug first-vs-last en `_extract_decision_from_text_events()` si aplica.
- Corregir la resolucion final del canal `json_last_text` si la evidencia real muestra
  que el Manager no entrega `final_answer` autoritativo para este caso.
- Anadir tests de barrera del parser sobre NDJSON realista.

## Files Likely Touched
- `bus/review_bridge.py`
- `tests/test_review_bridge.py`

## Read/inspect only
- `.agent/runtime/reviews/WT-2026-249b/attempt-2.md`
- `.agent/runtime/review_packets/WT-2026-249b_attempt-2.md`
- `.agent/runtime/events/events.jsonl`
- `.agent/collaboration/PLAN_WT-2026-249b.md`

## Secuencia de implementacion
1. Inspeccionar `attempt-2.md` y el stream NDJSON asociado para verificar si el Manager
   real emitio `phase:"final_answer"` con decision autoritativa.
2. Confirmar en codigo Bug #1 en `_extract_decision_from_text_events()`:
   - hoy guarda la primera decision encontrada;
   - si la intencion es `last_decision`, debe devolver la ultima.
3. Aplicar regla binaria para el escenario residual de `json_last_text`:
   - si `attempt-2.md` contiene `DECISION: CHANGES` pero no contiene un
     `phase:"final_answer"` util, corregir tambien el escenario residual de
     `json_last_text`;
   - si `attempt-2.md` si contiene `phase:"final_answer"` util, limitar el fix a
     Bug #1 salvo que aparezca evidencia adicional verificable;
   - en el caso residual, demostrar con evidencia si el fallo restante era
     "primera vs ultima", "no decision encontrada" u otra condicion real del
     stream;
   - aplicar el fix minimo necesario para que una decision final valida `CHANGES` o
     `APPROVE` no termine convertida en `INSPECT` en el caso real;
   - no introducir una politica mas amplia de aceptacion de `json_last_text` sin una
     validacion minima o fixture realista que la justifique.
4. Anadir tests de barrera minimos con nombres explicitos:
   - `test_early_inspect_later_changes_returns_changes`:
     stream NDJSON con `DECISION: INSPECT` temprano y `DECISION: CHANGES` tardio ->
     `_parse_opencode_json_decision()` devuelve `CHANGES` con `json_last_text`.
   - `test_no_final_answer_text_with_changes_returns_changes`:
     stream NDJSON realista sin `phase:"final_answer"`, pero con `DECISION: CHANGES`
     al final -> resultado `CHANGES` si el alcance incluye el escenario residual de
     `json_last_text`.
   - `test_final_answer_phase_wins_as_regression`:
     stream con `phase:"final_answer"` autoritativo y decision final `CHANGES` ->
     sigue ganando el canal `json_final_answer` como test de no regresion del canal
     primario, no como barrera nueva principal.
5. Reejecutar los tests focales del review bridge y la suite completa del motor para
   descartar regresiones laterales del parser.
6. Registrar en `execution_log.md` la evidencia exacta:
   - si habia `final_answer`, citando el evento o linea concreta del artefacto real;
   - si se corrigio solo Bug #1 o Bug #1 + escenario residual de `json_last_text`;
   - que prueba barrera falla antes/pasa despues.

## Politica de commit
- Mantener el ticket en parser-only.
- No tocar `agent_controller.py`, `bus/supervisor.py` ni la state machine.
- No introducir payload estructurado de `CHANGES` en este ticket.
- No anadir artefactos `REWORK_*.md` ni cambiar el formato de feedback del Manager.
- No redefinir la semantica de `HUMAN_GATE`; solo evitar que una decision valida se
  degrade a `INSPECT` por fallo de parser.

## Criterios binarios de aceptacion
- Existe evidencia verificable de si `249b` tuvo o no `phase:"final_answer"` util.
- El parser ya no devuelve la primera decision del stream cuando debe devolver la ultima.
- Si el caso real lo necesita, el canal `json_last_text` ya no materializa `INSPECT`
  cuando la decision final valida del Manager era `CHANGES` o `APPROVE`.
- Existe test de barrera para `INSPECT` temprano + `CHANGES` tardio.
- Existe test de barrera para el canal realmente usado en el caso `249b`.
- `ruff check`, `tests/test_review_bridge.py` y la suite completa del motor pasan.

## Riesgos conocidos
- Riesgo de abrir demasiado el parser si se acepta cualquier `json_last_text` sin
  validacion minima.
- Riesgo de confundir texto leido del packet/prompt con decision real del modelo si el
  fixture no es realista.
- Riesgo de mezclar fix urgente de parser con redisenos de payload o rework.

## Non-goals
- No tocar payload estructurado de `CHANGES`.
- No tocar artefactos `manager_feedback_*` o `REWORK_*`.
- No tocar `agent_controller.py`.
- No tocar `supervisor.py`.
- No cambiar reglas de `HUMAN_GATE` fuera del bug de parser.

## Decision Arquitectonica

**Problema:** el bus puede convertir una review valida del Manager en `INSPECT` por un
fallo de interpretacion del stream NDJSON (`json_last_text`), lo que arrastra el ticket a
`HUMAN_GATE` aunque el contenido de la review si era util para Builder.

**Decision:** aislar un fix minimo del parser del review bridge, guiado por evidencia del
caso real de `249b`, y protegerlo con tests de barrera sobre NDJSON realista.

**Consecuencia operativa:** el ciclo Builder -> Manager -> CHANGES vuelve a ser confiable
sin mezclar esta correccion con mejoras estructurales mas amplias.

## Quality Gates
```powershell
python -m pytest tests/test_review_bridge.py -v
python scripts/run_pytest_safe.py
python -m ruff check bus/review_bridge.py tests/test_review_bridge.py
python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Evidencia esperada
- Diff minimo sobre `bus/review_bridge.py`.
- Test que falla antes/pasa despues para `INSPECT` temprano + `CHANGES` tardio.
- Si aplica, test que falla antes/pasa despues para el escenario residual de `json_last_text`.
- Evidencia textual en `execution_log.md` sobre el canal real usado en `249b`, con cita
  del evento o linea relevante del artefacto inspeccionado.
- `ruff` verde y tests del parser verdes.



# AUDIT_WT-2026-235a

## Riesgos Bloqueantes

### CRITICO - falso APPROVE por template reflejado
Bloquear cualquier implementacion donde `text_regex` pueda devolver `APPROVE`.
Un `APPROVE` falso cierra el ticket sin revision real.

### CRITICO - falso CHANGES sin blockers
Bloquear cualquier implementacion donde `CHANGES` pueda emitirse con
`payload.blockers == ""`.

### ALTO - `_validate_changes_structure()` solo observa
El test debe demostrar que una estructura invalida degrada la decision antes de
emitir `REVIEW_DECISION`.

### ALTO - falta de trazabilidad
`REVIEW_DECISION` debe registrar `parse_method`. Si se degrada a `INSPECT`, debe
registrar `failure_reason`.

### MEDIO - scope creep hacia supervisor/event bus
No modificar `supervisor.py` ni `event_bus.py` salvo evidencia nueva. La red de
seguridad del supervisor no es la causa raiz.

### MEDIO - fixture irreal
Los tests deben reproducir la forma real del stream OpenCode/NDJSON o stdout que
contiene la plantilla. No basta con un string artificial que nunca aparece en
produccion.

## TP Check

TP-01: leer `bus/review_bridge.py` y confirmar las rutas `json_final_answer`,
`json_last_text`, `text_regex`.

TP-02: test de plantilla reflejada:
- Contiene `DECISION: APPROVE` y `DECISION: CHANGES`.
- No contiene veredicto final autoritativo.
- Resultado: `INSPECT`.

TP-03: test de NDJSON sin final answer:
- Termina en `tool-calls` o `step_finish`.
- Resultado: `INSPECT`.

TP-04: test de CHANGES invalido:
- Sin `## BLOCKERS` o blockers vacio.
- Resultado: `INSPECT`, `failure_reason=changes_structure_invalid`.

TP-05: test de CHANGES valido:
- Bloque `## BLOCKERS` con al menos una accion concreta.
- Resultado: `CHANGES`, blockers preservados.

TP-06: test de APPROVE valido:
- Procedencia autoritativa.
- Resultado: `APPROVE`.

TP-07: payload final:
- `REVIEW_DECISION.payload.parse_method` existe.
- Si degradado, `failure_reason` existe.

## Comandos de Revision

```powershell
git -C C:\Users\fdl\Proyectos_Python\orquestador_de_agentes show --stat HEAD
python -m pytest tests/test_manager_review_bridge.py -q
python -m ruff check bus/review_bridge.py tests/test_manager_review_bridge.py
python C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Veredicto Previo

`APPROVED`: contrato listo para Builder. El ticket es urgente porque evita tanto
requeue ciego por `CHANGES` vacio como falso cierre por `APPROVE` capturado desde
plantilla.

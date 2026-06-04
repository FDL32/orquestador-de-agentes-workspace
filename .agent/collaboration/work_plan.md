# Work Ticket - WT-2026-227a

## Metadata
- **ID:** WT-2026-227a
- **Title:** Repomix: estado estructurado y diagnostico verificable en review context
- **Scope:** system/review-context
- **Priority:** Media
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-182, WT-2026-226a

## Problema
Durante lanzamientos recientes se observo el warning opaco:
`[repomix] Failed to generate context; continuing without repomix`. El fallo no
bloquea el flujo, pero tampoco deja una razon estructurada que el Manager pueda
auditar sin leer warnings.

La auditoria ubico el seam real en el review bridge, no en el launcher:

- `bus/review_bridge.py:_ensure_repomix_context`;
- `bus/review_bridge.py:_run_opencode_review`: caller que usa
  `repomix_path = self._ensure_repomix_context()` y luego `if repomix_path:`.

El ticket no busca resolver toda la instalacion Windows/Node. Busca que Repomix
sea best-effort, observable y verificable.

## Objetivo
Exponer un estado estructurado de Repomix dentro del review context para que el
Manager vea si Repomix termino `ok`, `failed` o `skipped`, con razon y evidencia
minima (`returncode`, `stderr_tail` o excepcion capturada).

Resultados esperados:
1. Repomix exitoso deja `repomix_status.status == "ok"` y evidencia del
   artefacto o ruta generada;
2. Repomix con `returncode != 0` deja `status == "failed"`, `returncode` y
   `stderr_tail` acotado;
3. Repomix no disponible o excepcion de subprocess deja
   `status == "skipped"` o `status == "failed"` con `reason` claro;
4. el review sigue siendo best-effort: un fallo de Repomix no bloquea al
   Manager;
5. los tests focales del ticket no usan `_mock_repomix_for_tests`.

## Contrato CEM v0
- Contrato antes que fix.
- Evidencia antes que relato.
- Rigor proporcional: toca contexto de review y observabilidad de subprocess.
- Ninguna afirmacion sin artefacto verificable.
- Los cambios fuera de scope quedan prohibidos en este ticket; cualquier hallazgo
  adyacente debe registrarse como deuda o follow-up antes de tocar codigo.

## Decision Arquitectonica
- Repomix sigue siendo best-effort, no gate obligatorio.
- La observabilidad vive en el review context, junto al seam real que invoca
  Repomix.
- La salida estructurada minima es:
  `repomix_status = {status: "ok"|"failed"|"skipped", reason: str, returncode?: int, stderr_tail?: str, output_path?: str}`.
- Los literales de `status` son exactos: `"ok"`, `"failed"` y `"skipped"`.
- El diagnostico queda acotado a resolucion de `npx`, `returncode`, `stderr` y
  excepciones de subprocess. No investigar ACLs, antivirus, Windows Search ni
  instalacion global de Node en este ticket.

## Decision de implementacion minima
- Confirmar en codigo:
  - `bus/review_bridge.py:_ensure_repomix_context`;
  - `bus/review_bridge.py:_run_opencode_review`, caller que hoy espera
    `Path | None` y pasa `-f <path>` si el resultado es truthy;
  - donde se construye el review packet o estructura equivalente.
- Estrategia recomendada: cambiar `_ensure_repomix_context` para devolver
  `(Path | None, repomix_status_dict)` y actualizar `_run_opencode_review` para
  desempaquetar. Queda prohibido devolver solo un dict desde
  `_ensure_repomix_context`, porque `if repomix_path:` pasaria `str(dict)` como
  argumento `-f`.
- Mantener compatibilidad con el flujo existente si Repomix falla.
- Evitar que `warnings.warn` sea la unica evidencia.

## Evidencia minima esperada
El cierre debe dejar, con artefactos verificables:
- seam real confirmado en `bus/review_bridge.py`;
- test de exito con subprocess simulado y `repomix_status.status = ok`;
- test de fallo con `returncode != 0` y `stderr_tail`;
- test de excepcion o `npx` no disponible con `reason` verificable;
- prueba de que el review sigue cuando Repomix falla;
- salida de tests focales;
- salida de `ruff`;
- `agent_controller.py --validate --json --project-root .` sin errores ni
  warnings.

## Non-goals
- No arreglar instalacion global de Node/npm.
- No hacer Repomix obligatorio.
- No mover Repomix al launcher.
- No redisenar el review packet completo.
- No tocar evidence seam de `WT-2026-226a`.
- No usar `_mock_repomix_for_tests` en los tests focales de este ticket.

## Fases
### Fase 0: Diagnostico del camino real
- Confirmar el seam `_ensure_repomix_context`.
- Confirmar el caller `_run_opencode_review` y su uso actual de `Path | None`.
- Confirmar si hoy solo existe `warnings.warn` como evidencia.
- Confirmar como se puede exponer el estado al Manager sin romper el flujo.

### Fase 1: Estado estructurado
- Capturar exito, fallo por returncode y excepcion de subprocess.
- Exponer `repomix_status` con campos acotados.
- Mantener el review best-effort.

### Fase 2: Pruebas
- Test de exito: subprocess devuelve exit 0 y el status queda `ok`.
- Test de fallo: subprocess devuelve exit distinto de 0 y el status queda
  `failed` con `returncode` y `stderr_tail`.
- Test de excepcion o `npx` ausente: status `skipped` o `failed` con `reason`
  verificable.
- Verificar que los tests focales no usan `_mock_repomix_for_tests`.

## Files Likely Touched
- `bus/review_bridge.py`
- `tests/test_manager_review_bridge.py`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-227a.md`
- `.agent/collaboration/AUDIT_WT-2026-227a.md`
- `.agent/collaboration/execution_log.md`

## Seams confirmados
- `bus/review_bridge.py:_ensure_repomix_context`: seam real de invocacion
  Repomix.
- `bus/review_bridge.py:_run_opencode_review`: caller que agrega `-f` cuando
  existe `repomix_path`.
- `tests/test_manager_review_bridge.py:_mock_repomix_for_tests`: mock global que
  no debe cubrir los tests focales nuevos de este ticket.

## Calidad
- Ejecutar tests focales del review bridge.
- Ejecutar al menos un test nuevo que falle sin el fix.
- Ejecutar `ruff check` sobre archivos Python modificados.
- Ejecutar `agent_controller.py --validate --json --project-root .` en el
  `repo_destino` antes de marcar ready.

## TP Check
TP-01: seam real `_ensure_repomix_context` confirmado.
TP-02: `repomix_status` existe con literales exactos de `status`
`"ok"|"failed"|"skipped"`, `reason` y campos opcionales verificables.
TP-03: fallo por `returncode != 0` deja `returncode` y `stderr_tail`.
TP-04: excepcion o `npx` ausente deja razon verificable.
TP-05: el review continua cuando Repomix falla.
TP-06: tests focales del ticket no usan `_mock_repomix_for_tests`.
TP-07: sin scope creep hacia launcher, Node global, evidence seam o bus rounds.

## Criterio binario de salida
- `agent_controller.py --validate --json --project-root .` devuelve 0 errores y
  0 warnings.
- Existe al menos 1 test de exito Repomix `ok`.
- Existe al menos 1 test de fallo Repomix con `returncode` y `stderr_tail`.
- Existe al menos 1 test de excepcion o `npx` ausente.
- El review sigue funcionando sin convertir Repomix en gate obligatorio.

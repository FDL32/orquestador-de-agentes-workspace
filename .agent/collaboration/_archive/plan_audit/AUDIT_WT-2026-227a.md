# AUDIT WT-2026-227a

## Veredicto esperado
No aprobar si Repomix sigue dejando solo un warning opaco sin estado
estructurado verificable.

## Hallazgos bloqueantes a vigilar

### ALTO - Seam equivocado
- Bloquea cambios centrados en el launcher. El seam real es
  `bus/review_bridge.py:_ensure_repomix_context`.

### ALTO - Estado estructurado ausente
- Bloquea si el Manager no puede inspeccionar `repomix_status` o estructura
  equivalente sin leer warnings.
- Bloquea si los literales de `status` no son exactamente `"ok"`, `"failed"` o
  `"skipped"`.

### ALTO - Firma rota en _run_opencode_review
- Bloquea si `_ensure_repomix_context` deja de devolver `Path | None` sin
  actualizar `_run_opencode_review`. Un dict truthy no puede llegar a `-f` como
  `str(dict)`.

### ALTO - Repomix convertido en gate obligatorio
- Bloquea si un fallo de Repomix impide el review sin contrato explicito.

### MEDIO - Diagnostico Windows abierto
- Bloquea investigaciones amplias de ACLs, antivirus, Windows Search o
  instalacion global de Node dentro de este ticket.

### MEDIO - Tests focales cubiertos por mock global
- Bloquea si los tests nuevos usan `_mock_repomix_for_tests` y por tanto no
  ejercitan `_ensure_repomix_context`.

## TP Check
TP-01: seam `_ensure_repomix_context` confirmado.
TP-02: estado estructurado `repomix_status` o equivalente visible con literales
exactos `"ok"`, `"failed"` y `"skipped"`.
TP-03: returncode/stderr capturados en fallo.
TP-04: excepcion de subprocess capturada con razon verificable.
TP-05: review continua cuando Repomix falla.
TP-06: tests focales nuevos no usan `_mock_repomix_for_tests`.
TP-07: sin scope creep hacia launcher, Node global, evidence seam o bus rounds.

## Evidencia requerida para aprobar
- diff del `repo_motor` con cambios productivos en `bus/review_bridge.py`;
- tests focales con nombres visibles en `tests/test_manager_review_bridge.py`;
- `ruff check` sobre archivos Python tocados;
- `agent_controller.py --validate --json --project-root <repo_destino>` con 0
  errores y 0 warnings;
- execution_log con comandos exactos y resultados.

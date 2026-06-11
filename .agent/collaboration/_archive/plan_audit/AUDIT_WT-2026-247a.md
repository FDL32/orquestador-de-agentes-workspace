# AUDIT WT-2026-247a - Higiene de suite: aislamiento de tests y bugs de regex/mock/lock

## Estado
PENDING

## Objetivo de auditoria
Verificar que los 7 fallos de la suite se corrigen sin introducir falsos verdes, separando claramente contaminacion de entorno de bugs/expectativas incorrectas del propio test, y que cualquier cambio en producto queda justificado por contrato observable real.

## TP Check
- TP-01: verificado - el backlog ya descompone el problema en dos familias de fallo con causas distintas.
- TP-02: verificado - el ticket es de codigo/testing, no documental; la evidencia debe ser pytest real y diff revisable.
- TP-03: verificado - el principal riesgo es metodologico: arreglar tests sin contrastar contrato real.
- TP-04: verificado - el caso `pid` requiere decision explicita entre bug real del launcher y expectativa mala del test.
- TP-05: verificado - el ticket debe usar fixtures realistas y seams reales, no mocks drift.
- TP-06: verificado - el TP Check no sustituye gates funcionales ni validacion de entorno.

## Fases de revision

### Fase 1 - Reproduccion
- Verificar que los 7 tests fallan como indica el backlog o que la desviacion esta explicada con evidencia nueva.
- Verificar que cada test se clasifica en Grupo A o Grupo B con causa precisa.

### Fase 2 - Grupo A: aislamiento
- Verificar que los 3 tests contaminados ya no leen `builder_lock.txt`, `execution_log.md` ni otros artefactos vivos del workspace real.
- Verificar que usan `tmp_path`, fixtures o datos controlados y que siguen probando observables reales.

### Fase 3 - Grupo B: expectativa y seams
- Verificar que el regex de `WT-` se alinea con el contrato canonico actual.
- Verificar que el mock drift de `test_motor_root_gates.py` se corrige sobre la seam real usada por produccion.
- Verificar que `test_mark_ready_blocks_on_zero_overlap` refleja el orden de guards real o documenta por que el producto debe cambiar.
- Verificar que el caso `pid` queda resuelto con una decision de contrato, no con un parche ambiguo.

### Fase 4 - No regresion
- Verificar que los fixes no aflojan guardias productivas ni convierten el test en un no-op.
- Verificar ausencia de floor assertions, mocks muertos y asserts cosmeticos.

### Fase 5 - Quality gates
- Verificar exit code 0 de:
  - `pytest tests/test_builder_lock.py tests/test_review_packet_evidence_gate.py tests/test_motor_root_gates.py tests/unit/test_scope_gate.py -v`
  - `ruff check tests/test_builder_lock.py tests/test_review_packet_evidence_gate.py tests/test_motor_root_gates.py tests/unit/test_scope_gate.py`
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers
- Cualquier test "verde" que siga dependiendo de estado real del workspace.
- Cualquier fix basado en mock drift o en cambiar expectativas sin verificar contrato productivo.
- Ambiguedad no resuelta en `test_launcher_does_not_write_pid`.
- Cambios de producto no justificados por evidencia real del contrato.
- Ruff o validate fallan.
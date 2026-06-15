# Work Plan: WOT-2026-009c

## Metadata

- **ID:** WOT-2026-009c
- **Contract ID:** T-009C-001
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-009b (COMPLETED)

## Objetivo

Implementar guardias reciprocas de aislamiento repo_motor/repo_destino que
bloquean contaminacion productiva cruzada en ambos sentidos, con diagnosticos
self-service que distinguen contaminacion_productiva, superficie_operativa_excluida
y scope_externo_no_declarado.

Root cause: pre_handoff_guard.py verifica tree-cleanliness en el proyecto raiz
(destino) pero no inspecciona el repo contrario. Un ticket repo_motor puede
tener cambios productivos en destino (fuera de la excludelist) que pasan sin
bloqueo. Un ticket repo_destino puede tener cambios productivos en motor sin
contrato topology-aware y tampoco hay guardia en run_guard.

## Decision Arquitectonica

El bloqueo de contaminacion cruzada se implementa en el pre-handoff
(pre_handoff_guard.py::run_guard y scripts/delivery_hygiene_check.py), que
ya es el callsite de bloqueo. La observabilidad (warning sin bloqueo) se
anade a _check_scope_for_validate en validate, lo que permite detectar drift
antes del handoff.

Separacion clara de comportamiento por callsite:

  pre_handoff_guard.py (bloqueo):
    - Ticket repo_motor: si hay cambios productivos no-operativos en destino -> valid=False, dirty_tree=True, categoria contaminacion_productiva.
    - Ticket repo_destino: si hay cambios productivos en motor sin contrato topology-aware (FLT ### repo_motor declarado) -> valid=False, categoria contaminacion_productiva.
    - Superficies operativas excluidas -> no bloquean; reportadas como excluded_operational.

  _check_scope_for_validate (observabilidad):
    - Segunda pasada: informa contaminacion_productiva si la hay.
    - Superficies operativas excluidas -> no warnings de contaminacion.

  delivery_hygiene_check.py:
    - Anadir check de contaminacion cruzada como verificacion adicional en
      run_delivery_hygiene_check (no bloquea pre-push si es solo superficie
      operativa; bloquea si hay productiva).

Mensajes distinguen explicitamente:
  - contaminacion_productiva: archivo no-operativo en repo contrario
  - excluded_operational: archivo operativo en repo contrario (excluido, OK)
  - scope_externo_no_declarado: archivo en repo propio fuera de FLT (ya existe)

No se toca state machine ni bus.

## Non-goals

- No tocar TicketState ni eventos de bus.
- No cambiar el comportamiento de mark-ready (motor_uncommitted_productive ya bloquea ahi).
- No implementar 009d.
- No mezclar con 009e (launcher).
- No crear un nuevo script de aislamiento; usar los callsites existentes.

## Diseno tecnico

### Nueva funcion scope_gate.check_cross_root_contamination

```
def check_cross_root_contamination(
    *,
    other_root: Path,
    other_exclude: set[str],
    run_fn=subprocess.run,
) -> dict[str, set[str]]:
    Retorna {"productive": set[str], "operational": set[str]}
    Usa get_changed_files(project_root=other_root, motor_root=None).
    Separa con other_exclude: en operational si excluido, en productive si no.
```

### pre_handoff_guard.py::run_guard

Despues del paso 5 (dirty_files/scope_discrepancy), anadir paso 6:

  Si hay motor_root y motor_root != project_root:
    Leer delivery_authority del work_plan.
    Si repo_motor: check contaminacion en destino (project_root).
    Si repo_destino: check contaminacion en motor (motor_root).
    Archivos productivos en repo contrario -> dirty_files (bloquea).
    Archivos operativos en repo contrario -> excluded_operational (no bloquea).

Anadir al resultado: cross_root_contamination: list[str], excluded_operational: list[str].

### delivery_hygiene_check.py

Anadir funcion check_cross_root_isolation(project_root, motor_root, delivery_authority).
Incluir en run_delivery_hygiene_check como verificacion adicional cuando motor_root != None.
Falla (HygieneResult.passed=False) si hay archivos productivos en repo contrario.

### _check_scope_for_validate (agent_controller.py)

Anadir segunda pasada que llama a check_cross_root_contamination y emite
warnings (no errors) con prefijo contaminacion_productiva: si resultado productive != empty.

## Files Likely Touched

### repo_motor
- .agent/scope_gate.py
- .agent/agent_controller.py
- scripts/pre_handoff_guard.py
- scripts/delivery_hygiene_check.py
- tests/unit/test_scope_gate_isolation.py

## Criterios Binarios

- [ ] check_cross_root_contamination en scope_gate.py existe y pasa tests unitarios.
- [ ] run_guard bloquea (valid=False) cuando hay archivos productivos en repo contrario.
- [ ] run_guard NO bloquea cuando solo hay superficies operativas en repo contrario.
- [ ] _check_scope_for_validate emite warning contaminacion_productiva (no error) si hay archivos productivos en repo contrario.
- [ ] delivery_hygiene_check emite HygieneResult.passed=False si hay contaminacion productiva cruzada.
- [ ] Mensajes distinguen contaminacion_productiva, excluded_operational y scope_externo_no_declarado.
- [ ] Tests bidireccionales: motor con contaminacion en destino, destino con contaminacion en motor.
- [ ] Tests demuestran fallo sin el fix y paso con el fix (barrera real).
- [ ] Fixture multi-root realista con tmp_path/motor + tmp_path/destino con .git en cada uno.
- [ ] ruff check . exit 0.
- [ ] python scripts/run_pytest_safe.py exit 0 (suite completa).
- [ ] Validate destino final 0/0.

## STOP conditions

- Si la implementacion exige cambiar eventos de bus o TicketState: parar y abrir ticket separado.
- Si una guardia bloquea superficies vivas (work_plan, execution_log, STATE, bus runtime) cubiertas por excludelist: ajustar el modelo antes de cerrar.
- Si no hay fixture multi-root realista: no aprobar con mocks monoliticos.
- Si delivery_hygiene_check requiere cambio mayor de interfaz: separar ticket.

## Forbidden Surfaces

- .agent/collaboration/ del motor (seed neutro).
- privada/ y .env.
- bus/state_machine.py.
- events.jsonl editado a mano.

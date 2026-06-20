# execution_log.md -- WOT-2026-013a
## Metadata
- **Ticket:** WOT-2026-013a
- **Estado:** READY_FOR_REVIEW
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-013a.
- Motivo: `011h` no se prepara porque la barrera que pedia ya aparece implementada en `scripts/pre_handoff_guard.py`; `013a` si mantiene un rojo aislado verificable hoy y tiene scope minimizable a test-only.
- Contrato congelado: `T-013A-001`.
- Frontera fijada antes de Builder: `013a` arregla solo `tests/test_controller_integration.py`; tocar `.agent/agent_controller.py` o anadir feature nueva de topologia dispara `CONTRACT_GAP`.
- Runtime bootstrap esperado para Builder: `STATE=IN_PROGRESS`, `TURN=BUILDER/IMPLEMENT`, `work_plan.md` activo en `013a`.
## Premise Re-check requerido al Builder
- Reejecutar `python -m pytest tests/test_controller_integration.py -k approved_pending -q` y registrar el rojo exacto.
- Releer `sandbox()`, `_run()` y `_REAL_CONTROLLER` en `tests/test_controller_integration.py`.
- Confirmar que `.agent/agent_controller.py` permanece read-only salvo evidencia que fuerce `CONTRACT_GAP`.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de empezar la implementacion.
## Restriccion cross-ticket
- `013a` no reabre `011g`, `011h`, `011i` ni la deuda opcional de `--validate-topology`.
- Si el rojo aislado solo se arregla tocando produccion, el ticket para con `CG-WOT-2026-013a.md`.

## BUILDER - WOT-2026-013a - Robustez test_approved_pending (drift topologia sandbox)

### Fase 0 - Diagnostico (VERIFICADO)
- Rojo aislado reproducido: `python -m pytest tests/test_controller_integration.py -k approved_pending -q` -> AssertionError "No JSON en output del controller" (tests/test_controller_integration.py:145). Firma identica al Context Baseline Evidence.
- Drift confirmado: sandbox() (L41-42) COPIA el controller (_REAL_CONTROLLER.read_text -> agent_dir/agent_controller.py) y copia runtime/+bus/. _run() (L48-65) invoca el controller COPIADO (agent_dir/agent_controller.py) con cwd=root. El controller resuelve proyecto via __file__.parent.parent; para la copia en sandbox/.agent/, eso = sandbox/ (sin scripts/prompts) -> no produce JSON -> data is None.
- Causa = fixture/topologia, NO regresion productiva: el controller REAL funciona (verificado abajo). .agent/agent_controller.py leido read-only.
- SEAM VERIFICADO (experimento read-only): controller REAL del motor (.agent/agent_controller.py) + --project-root <sandbox> (SIN copiar) -> rc=0, JSON {role:BUILDER, action_type:IMPLEMENT}. El controller soporta --project-root (doc L21). Este es el fix: ejercer el controller real apuntando al sandbox por --project-root, en vez de copiarlo.
- Scope: fix vive solo en tests/test_controller_integration.py. Sin tocar controller, runtime, bus, --validate-topology.

### Fase 1 - Fix (test-only, controller productivo INTACTO)
- 3 ediciones en tests/test_controller_integration.py:
  (1) _run() invoca _REAL_CONTROLLER (motor) + --project-root str(root) en vez del controller copiado.
  (2) subprocess inline de test_validate_returns_empty_arrays -> mismo patron (real + --project-root).
  (3) sandbox() deja de copiar el controller (controller_src write eliminado): una copia solo reintroduciria el drift __file__.
- .agent/agent_controller.py NO tocado. Sin --validate-topology. Sin runtime/bus/scripts modificados.

### HALLAZGO (no desviacion de scope): el drift afecta a los 3 tests del archivo
- El baseline solo anclo approved_pending (el que Hermes destapo), pero en aislamiento fallaban los 3 (approved_pending, completed, validate) por la MISMA causa raiz (controller copiado). Arreglar el fixture cura los 3 a la vez = cambio minimo correcto (FLT = el archivo entero; el contrato pide "no romper los otros del archivo"). Arreglar solo approved_pending dejaria 2 rojos aislados.

### Fase 2 - Barreras
- FAIL-sin/PASS-con: revertido el archivo a HEAD -> approved_pending aislado FAIL (1 failed); restaurado fix -> 1 passed.
- Anti-falso-verde (test negativo): el controller real DISCRIMINA estados -> APPROVED+PENDING=BUILDER/IMPLEMENT vs COMPLETED+DONE=MANAGER/CREATE_PLAN. El test ejerce el controller real; sus asserts detectarian un bug real, no es atajo del fixture.
- Archivo completo aislado: 3 passed.

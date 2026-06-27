# AUDIT_WOT-2026-014h

## Scope
- Ticket WOT-2026-014h, code, repo_motor.
- Objetivo auditado: mover 5 funciones de scope-verification a scripts/scope_verification.py + reapuntar el test, sin shim (0 consumidores live).

## TP Check
- TP-01: se mueven las 5 funciones (incluyendo snapshot_file_info, el 5o que el test importa), no 4.
- TP-02: tests/test_orquestador_scope.py reapunta imports a scripts.scope_verification y pasa.
- TP-03: busqueda transversal post-extraccion confirma 0 consumidores live de esas funciones desde scripts.orquestador.
- TP-04: orquestador.py NO se borra; adapters Goose/Claw y banner DEPRECATED intactos; NO shim (seria codigo muerto).
- TP-05: cierre con run_pytest_safe --level all + validate.

## Regression Focus
- Falso verde a evitar: mover solo 4 funciones dejando snapshot_file_info en orquestador (el test fallaria o seguiria acoplado).
- No introducir un shim innecesario (codigo muerto) salvo que aparezca un consumidor live real.

## Closing Rule
- No aprobar si quedan consumidores live importando desde scripts.orquestador, si se borra orquestador.py, si se tocan
  los adapters Goose/Claw, si se anade un shim sin consumidor real, o sin el SHA del commit del repo_motor.

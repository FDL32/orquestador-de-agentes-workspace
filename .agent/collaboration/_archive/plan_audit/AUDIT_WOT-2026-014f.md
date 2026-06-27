# AUDIT_WOT-2026-014f

## Scope
- Ticket: WOT-2026-014f
- deliverable_type: code
- delivery_authority: repo_motor
- Objetivo auditado: 1 helper canonico de discovery + 1 de parse en un modulo neutro nuevo;
  3 consumidores importan; sin tercera implementacion real.

## TP Check
- TP-01: firma canonica = la del closeout (filename, *, ticket_id_pattern); hogar canonico =
  scripts/manager_feedback_helpers.py (neutro), NO session_closeout/archival como canonico implicito.
- TP-02: la API publica del CLI extract_ticket_id_from_feedback(filename) se preserva via wrapper delgado.
- TP-03: la barrera primaria es import-identity (mutation-verified), no grep ni conteo cosmetico:
  revertir un consumidor a una copia propia DEBE hacer FALLAR el test.
- TP-04: la politica de SELECCION (_can_prove_close por bus events, ticket_ids del CLI) NO se toca.
- TP-05: el cierre exige run_pytest_safe --level all + validate --json, no solo la bateria focal.

## Regression Focus
- Falso verde a evitar: un test que cuenta defs por nombre via AST pero no demuestra propagacion REAL
  (import-identity) a los 3 consumidores. Tambien: una tercera implementacion real disfrazada de wrapper.

## Closing Rule
- No aprobar si aparece una tercera implementacion real, si se toca la politica de seleccion, si la
  barrera no es mutation-verified por import-identity, o sin el SHA del commit del repo_motor.

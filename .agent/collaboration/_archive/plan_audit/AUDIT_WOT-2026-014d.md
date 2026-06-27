# AUDIT_WOT-2026-014d

## Scope
- Ticket WOT-2026-014d, code, repo_motor.
- Objetivo auditado: re-encodar builder-self-audit/SKILL.md (0 C1) + endurecer encoding_guard por CLASE (rango C1 0x80-0x9F + strict-decode), colateral-cero.

## TP Check
- TP-01: solo se re-encoda builder-self-audit; NO las otras skills; NO se prohibe Latin-1 legitimo.
- TP-02: la barrera es POR CLASE (rango C1 U+0080-U+009F), no una lista negra de bytes concretos.
- TP-03: barrera mutation-verified: reinyectar (i) un codepoint C1 O (ii) un byte UTF-8 invalido hace FALLAR el guard.
- TP-04: CASO NEGATIVO explicito: UTF-8 valido + codepoint C1 PASA strict-decode pero ES flagueado por el rango (strict solo no basta).
- TP-05: cierre con check_encoding_guard verde (blast-radius cero) + run_pytest_safe --level all + validate.

## Regression Focus
- Falso verde a evitar: una barrera que solo prueba strict-decode (no detecta el caso real, que es UTF-8 valido con C1) o
  una lista negra de bytes (gato-y-raton). Tambien: un re-encode que toque contenido sustantivo en vez de solo los marcadores.

## Closing Rule
- No aprobar si se re-encodan otras skills, si se prohibe Latin-1 legitimo, si la barrera no cubre el caso UTF-8-valido-con-C1
  mutation-verified, si check_encoding_guard no queda verde, o sin el SHA del commit del repo_motor.

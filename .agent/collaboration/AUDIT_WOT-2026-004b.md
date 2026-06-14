# AUDIT WOT-2026-004b - Motor: gitleaks seed + politica SHA + fix guard \.git

## Objetivo del audit
Verificar que (a) el guard deja de bloquear `.github/.gitignore/.gitleaks.toml/.gitattributes`
pero SIGUE bloqueando `.git/` interno, (b) el seed portable es generico y no filtra
falsos positivos especificos del destino ni oculta secretos reales, (c) el installer es
no-clobber, (d) hay barrera de test real, y (e) el motor solo cambia en los archivos del ticket.

## Reglas de revision
- Revisar el DIFF real de `guard_paths.py`, no el relato del Builder.
- Ejecutar/leer el test del guard: confirmar que es una barrera (falla con `\.git`,
  pasa con el fix). Rechazar test cosmetico (assert not None) o mock drift (parchear una
  API distinta a la que usa `_is_protected_path`).
- Confirmar empiricamente: payload Write a `.gitleaks.toml` -> permitido; a `.git/config`
  -> bloqueado (exit 2). Citar el comando/salida.
- Leer el seed: useDefault=true; politica por PATH (no regex 40-hex global); SIN
  `sk_live_1234567890` ni el SHA del destino.
- Confirmar no-clobber: con `.gitleaks.toml` previo en dest, el installer no lo pisa.
- `check_motor_pristine --check`: motor_status_new = solo guard_paths.py, el template,
  install_agent_system.py, MANIFEST.distribute y tests. Nada mas.

## Hallazgos bloqueantes tipicos
- CRITICO: el fix abre un agujero (deja de bloquear `.git/` interno o rutas sensibles).
- CRITICO: el seed contiene un allowlist amplio (40-hex global) que ocultaria secretos reales.
- CRITICO: el installer clobberea un `.gitleaks.toml` ya personalizado del destino.
- CRITICO: se toco el `.gitleaks.toml` del destino (004a) desde este ticket.
- ALTO: no hay test de barrera, o el test pasa igual con el patron viejo (no demuestra el fix).
- ALTO: el seed hereda los falsos positivos especificos del destino (no es generico).
- ALTO: ruff/pytest del motor en rojo y se cierra igual.
- MEDIO: `MANIFEST.distribute` no declara el template (el installer copiaria algo no contratado).
- MEDIO: cambios de scope creep en otros patrones del guard sin justificacion CEM.

## Evidencia minima esperada
- Diff `guard_paths.py` con el patron anclado y la normalizacion.
- Salida del test del guard (pass con fix; demostrar fallo con patron viejo: git stash/revert
  puntual o assert documentado).
- `cat agent_system/templates/gitleaks.config.toml`.
- Salida del test de installer no-clobber (presente -> skip; ausente -> copia).
- `ruff` exit 0; `run_pytest_safe` exit 0; `validate` destino 0/0.
- `git -C <motor> show --stat <commit>`; `check_motor_pristine --check` report.

## TP Check
TP-01: Patron `.git` anclado a segmento (no substring); path normalizado antes de matchear. (diff)
TP-02: `.github/`, `.gitignore`, `.gitleaks.toml`, `.gitattributes` -> NO bloqueado. (test/exec)
TP-03: `.git/config` y `.git/<interno>` -> bloqueado exit 2. (test/exec)
TP-04: Test de barrera real (falla con patron viejo, pasa con fix; sin mock drift). (test)
TP-05: Seed generico: useDefault, politica por PATH, sin regexes especificos del destino. (codigo)
TP-06: Installer no-clobber: no pisa `.gitleaks.toml` existente; copia si ausente. (test)
TP-07: `MANIFEST.distribute` declara el template seed. (diff)
TP-08: `.gitleaks.toml` del destino (004a) intacto. (git status destino)
TP-09: ruff 0; run_pytest_safe motor 0; validate destino 0/0. (command/exit_code)
TP-10: commit(s) en repo_motor con WOT-2026-004b; motor_status solo archivos del ticket. (git)

## Criterio de rechazo inmediato
- El guard deja de proteger `.git/` interno o cualquier ruta sensible previa.
- El seed amplia la superficie de ocultacion de secretos (allowlist 40-hex global).
- El installer clobberea config de destino.
- No hay barrera de test que demuestre el fix.
- Se modifico el motor fuera de los archivos del ticket sin justificacion.

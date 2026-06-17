# STRATEGY_WOT-2026-010q -- Suite canonica real en pre-handoff

## Hechos verificados

- `last-run.json` ya expone `level` y `args_mode`; no hace falta cambiar el
  runner para distinguir suite completa de corrida focal.
- `tested_commit_sha == HEAD` solo prueba frescura respecto al commit, no
  cobertura canonica.

## Plan tecnico

1. Localizar la funcion que valida el fresh-green canonico de pytest-safe.
2. Anadir validacion estricta de `level == "all"`.
3. Anadir validacion estricta de `args_mode == "default_discovery"`.
4. Mantener las validaciones existentes de `status`, `exit_code` y SHA.
5. Cubrir con tests barrera:
   - `level="unit"` bloquea.
   - `level="all"` + `args_mode="explicit_args"` bloquea.
   - `level="all"` + `args_mode="default_discovery"` pasa.
6. Verificar que el mensaje de bloqueo es accionable y no obliga a leer codigo.

## Riesgos

- **Falso verde:** aceptar un run focal como suite completa por mirar solo
  exit code y SHA.
- **Sobre-scope:** cambiar `run_pytest_safe.py` o el schema cuando el dato ya
  existe.
- **Diagnostico pobre:** bloquear correctamente pero sin indicar como repararlo.

## No hacer

- No tocar selector focal ni runner.
- No cambiar politica de Manager.
- No introducir cache/paralelizacion.

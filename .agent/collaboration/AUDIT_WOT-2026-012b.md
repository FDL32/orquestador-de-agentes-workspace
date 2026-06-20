# AUDIT_WOT-2026-012b.md

## Preguntas binarias de auditoria
- El gate lee el backlog vivo de `repo_destino` solo via `--project-root` o `AGENT_PROJECT_ROOT`?
- Falla con `exit != 0` cuando faltan root explicito o schema minimo?
- Valida solo la tabla activa y no depende de comentarios HTML ni de prose libre?
- El vocabulario de `Status` y la semantica de `Reactivation` quedan codificados y cubiertos por tests de barrera?
- La integracion en `run_gates_dispatch.py` evita tocar closeout, archivador o barreras de cierre ajenas?
- `ruff`, tests focales, suite aplicable y `validate --json --project-root <repo_destino>` quedan verdes?

## Hallazgos a rechazar
- Cualquier parser que lea el seed del motor o resuelva `backlog.md` relativo al cwd.
- Cualquier fallback pass-open cuando falta `--project-root` o `AGENT_PROJECT_ROOT`.
- Cualquier regla semantica que admita `N/A`, `pendiente` o prosa vaga como `Reactivation` valida.
- Cualquier test que no demuestre FAIL-sin / PASS-con para al menos una barrera nueva.

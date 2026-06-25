## Bloque de cabecera

- **Scope:** post-cambio tras cierre de WOT-2026-013t (+ familia 013 r/s/u/l/v/k, docs runner)
- **Repo motor (HEAD):** a1b99afd87c3d351b6644d0623b47ee128f0987a
- **Repo destino (HEAD):** 1c0a6aede12dce07b4c571e054e3ab36b91fdb69
- **Fecha:** 2026-06-25 21:05 UTC
- **Comandos ejecutados:** collect_system_health.py --mode auto; verificacion manual de last-run.json, validate, ruff, pristine
- **Cobertura declarada:** suite canonica FULL (level=all, default_discovery, serial) verde a HEAD; NO allowlist parcial
- **Limitaciones:** Pasada B sobre evidencia del recolector + re-derivacion por bytes de last-run.json/validate/ruff/pristine

---

## Quality gates (Pasada B, re-derivado por bytes)

| Gate | Evidencia | Exit | Veredicto |
|------|-----------|------|-----------|
| ruff motor | raw/ruff_motor.txt: "All checks passed!" | 0 | VERIFICADO POR BYTES |
| ruff destino | raw/ruff_destino.txt: passed; "No Python files" es by-design (destino solo `.agent/`) | 0 | VERIFICADO POR BYTES |
| validate motor | raw/validate_motor.txt: todos los buckets de errors vacios, warnings {} | 0/0 | VERIFICADO POR BYTES |
| validate destino | raw/validate_destino.txt: 0 errors / 0 warnings, --project-root workspace | 0/0 | VERIFICADO POR BYTES |
| discover_skills --check-contract | raw/discover_skills_contract.txt | 0 | VERIFICADO POR BYTES |
| motor pristine | raw/motor_pristine_snapshot.txt: dirty_before=false @ a1b99af | 0 | VERIFICADO POR BYTES |
| **pytest-safe canonical** | **last-run.json: status=finished, exit_code=0, level=all, args_mode=default_discovery, tested_commit_sha=a1b99af == HEAD** | **0** | **VERIFICADO POR BYTES (NO stale, NO focal, NO false-green)** |

### Anti-false-green (lecciones aplicadas)
- **stale_run / canonical-suite-gate motor-HEAD-vs-destino:** `tested_commit_sha`
  (a1b99af) coincide EXACTO con motor HEAD. No hay desfase. Gate legitimo.
- **focal vs full:** `args_mode=default_discovery`, `focal_selection=null`,
  target `tests/`. Es suite completa, no verde focal.
- **interprete:** suite corrida con el python del sistema (Python312), motor sin
  exportar AGENT_PROJECT_ROOT al workspace -> interprete correcto para ticket
  delivery_authority=repo_motor (regla de dos ejes, docs/RUNNER_INTERPRETER_SEMANTICS.md).
- Suite contada en ejecucion previa de esta sesion: 3200 passed, 20 skipped @ a1b99af.

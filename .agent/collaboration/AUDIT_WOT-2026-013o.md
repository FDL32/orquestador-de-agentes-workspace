# AUDIT_WOT-2026-013o

## Pregunta de auditoria
El cambio deja `observations.jsonl` en `--strict` verde reparando de forma determinista la corrupcion de datos y cerrando explicitamente la decision de contrato sobre dominios, sin promover memoria portable nueva ni tocar consumidores fuera de scope?

## Criterios binarios
- [ ] `validate_observations.py --strict` queda verde sobre `repo_destino/.agent/runtime/memory/observations.jsonl`.
- [ ] Las 14 entradas con `applies_to` corrupto quedan reparadas de forma determinista y con evidencia pre/post.
- [ ] Los 3 errores de `domain` quedan resueltos por decision explicita de contrato, no por fallback silencioso.
- [ ] `scripts/migrate_observations.py` conserva backup/rollback e idempotencia.
- [ ] Existe FAIL-sin/PASS-con para el patron `applies_to <- domain`.
- [ ] `tests/test_migration_bootstrap.py` y `tests/unit/test_validate_observations.py` cubren la reparacion real y la decision de contrato.
- [ ] `python scripts/run_pytest_safe.py --level all` queda verde sobre el commit entregado.
- [ ] `validate --json --project-root <repo_destino>` queda en 0 errors / 0 warnings.
- [ ] El cierre deja explicito que `013o` no inserta nueva memoria portable; la promocion posterior de la observacion diferida de `013n` queda fuera de scope.

## Anti-patrones a rechazar
- reparar el archivo a mano sin barrera reutilizable en migrador/validador/tests
- reinterpretar lineas ambiguas sin evidencia verificable
- resolver `domain` por fallback silencioso o mapeo no documentado
- tocar `bus/memory_loader.py` o memoria portable del motor para compensar una base corrupta
- insertar memoria portable nueva antes del verde estricto

## Evidencia minima esperada en review
- diff productivo del motor dentro de FLT
- diff del archivo `observations.jsonl` del destino con reparacion auditable
- comandos exactos de tests focales y resultado literal
- suite canonica con `tested_commit_sha == HEAD`
- validate 0/0
- explicacion explicita de por que la observacion diferida de `013n` queda fuera de scope en esta ronda

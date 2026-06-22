# work_plan.md -- WOT-2026-013o
## Metadata
- **ID:** WOT-2026-013o
- **Contract ID:** T-013O-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Dejar `repo_destino/.agent/runtime/memory/observations.jsonl` en `--strict` verde separando la reparacion determinista de datos corruptos (`applies_to <- domain`) de la decision explicita de contrato sobre dominios (`collaboration`, `test-performance`), antes de volver a promover memoria portable nueva.
## Non-goals
- No insertar observaciones nuevas en `repo_destino/.agent/runtime/memory/observations.jsonl` durante este ticket.
- No tocar `repo_motor/.agent/runtime/memory/observations.jsonl`, `repo_destino/.agent/runtime/memory/MEMORY.md`, `memory_profile.md` ni `memory_rules.md`.
- No tocar `repo_motor/bus/memory_loader.py` salvo `CONTRACT_GAP`.
- No tocar `repo_motor/scripts/session_close_observations.py`, CI/workflows, `privada/` ni `.env`.
- No reinterpretar semanticamente lineas dudosas sin evidencia verificable.
## Premisas verificadas antes de Builder
- `repo_destino/.agent/runtime/memory/observations.jsonl` falla `python scripts/validate_observations.py --strict --file <obs>` con 17 errores verificados.
- El diagnostico correcto tiene dos clases distintas: 14 entradas tienen corrupcion de datos (`applies_to` contiene etiquetas que son claramente `domain`, como `review-quality`, `planning`, `supervisor`, `preflight`) y 3 entradas usan valores de `domain` fuera del enum canonico (`collaboration`, `test-performance`).
- Ya existe un seam de migracion reutilizable en `scripts/migrate_observations.py` junto con barreras en `tests/test_migration_bootstrap.py`; el trabajo no es inventar una migracion desde cero.
- `bus/memory_loader.py` y `scripts/memory_consolidate.py` son consumidores reales de la base y quedan read-only salvo `CONTRACT_GAP`.
- La observacion diferida de `013n` queda fuera de scope hasta partir de una base `--strict` verde.
## Decision Arquitectonica
`013o` es un ticket `mixed` con autoridad de entrega en `repo_motor`: la reparacion del contrato vive en migrador/validador/schema/tests del motor, mientras la base corrupta a reparar vive en `repo_destino/.agent/runtime/memory/observations.jsonl`. El Builder debe corregir primero la base y el contrato estricto, dejando explicito que no promueve nueva memoria portable en esta ronda.
## Files Likely Touched
### repo_motor
- scripts/migrate_observations.py
- scripts/validate_observations.py
- skills/_shared/ap-schema.md
- tests/test_migration_bootstrap.py
- tests/unit/test_validate_observations.py
### repo_destino
- .agent/runtime/memory/observations.jsonl
- .agent/collaboration/execution_log.md
## Read/inspect only
- bus/memory_loader.py
- scripts/memory_consolidate.py
- prompts/memory_upload.md
- .agent/runtime/memory/MEMORY.md
- .agent/runtime/memory/memory_profile.md
- .agent/audits/system_health/general_audit_20260622_1449/07_adversarial_review.md
## Forbidden Surfaces
- .agent/runtime/memory/observations.jsonl inserciones semanticas nuevas antes del verde estricto
- .agent/runtime/memory/MEMORY.md
- .agent/runtime/memory/memory_profile.md
- .agent/runtime/memory/memory_rules.md
- repo_motor/.agent/runtime/memory/observations.jsonl
- repo_motor/bus/memory_loader.py salvo `CONTRACT_GAP`
- repo_motor/scripts/session_close_observations.py
- CI/workflows
- privada/
- .env
- editar eventos del bus a mano
## Criterios binarios
- `python scripts/validate_observations.py --strict --file <repo_destino>/.agent/runtime/memory/observations.jsonl` termina verde.
- Las 14 entradas con `applies_to` corrupto quedan reparadas de forma determinista, con evidencia pre/post en `execution_log.md` o reporte adjunto.
- Los 3 errores de `domain` quedan resueltos por decision explicita de contrato: o se mapean a dominios canonicos existentes con justificacion verificable, o se amplia el enum canonico en schema+validador+tests. No se permite fallback silencioso.
- `scripts/migrate_observations.py` mantiene backup/rollback e idempotencia; existe al menos una barrera que falla sin el fix y pasa con el fix sobre el patron `applies_to <- domain`.
- `python -m pytest tests/test_migration_bootstrap.py tests/unit/test_validate_observations.py -q -p no:cacheprovider` termina verde.
- `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- El cierre deja explicito que `013o` no inserta nueva memoria portable durante este ticket; cualquier promocion posterior, incluida la observacion diferida de `013n`, queda fuera de scope hasta partir de una base `--strict` verde.
## STOP conditions
- Parar si aparecen mas entradas invalidas de las 17 reportadas y cambian materialmente la premisa.
- Parar si el arreglo de datos deja de ser determinista linea-a-linea.
- Parar si la decision de dominio no puede cerrarse sin redisenar la memoria portable completa.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013o.md` si alguna de las 17 lineas requiere reinterpretacion semantica no verificable, si `collaboration`/`test-performance` fuerzan una reforma amplia de dominios/consumidores fuera de scope, o si la unica salida segura exige tocar `repo_motor/.agent/runtime/memory/observations.jsonl` o `repo_motor/bus/memory_loader.py`.

# Execution Log -- WOT-2026-013o

**Estado:** IN_PROGRESS

## MANAGER - WOT-2026-013o - Bootstrap operativo

Ticket activado para sanear `repo_destino/.agent/runtime/memory/observations.jsonl` antes de promover memoria portable nueva.

Packet activo en repo_destino:
- `OBJ-013O-001` en `repo_charter.md`
- `PLAN-013O-001` en `plan_graph.md`
- `T-013O-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013o.md` y `AUDIT_WOT-2026-013o.md` activos para Builder
- `STRATEGY_WOT-2026-013n.md` y `AUDIT_WOT-2026-013n.md` archivados en `_archive/plan_audit/` por cierre previo

Premisa operativa del Builder:
- reejecutar `validate_observations.py --strict` sobre el archivo real del destino
- separar con evidencia `14 applies_to-corrupt + 3 domain-contract`
- reutilizar el migrador existente en vez de bypass manual
- mantener fuera de scope cualquier insercion de memoria portable nueva, incluida la observacion diferida de `013n`

Baseline verificado antes del bootstrap:
- `validate --json --project-root <repo_destino>` arranco en `0 errors / 0 warnings`
- `observations.jsonl` sigue fallando `--strict` con 17 errores verificados por contrato
- el runtime activo anterior seguia apuntando a `013n COMPLETED`; se materializo packet vivo de `013o` y se emitio `STATE_CHANGED BOOTSTRAP -> IN_PROGRESS` para el ticket correcto

## WOT-2026-013o - Fase 0 (diagnostico adversarial)

Preflight: runtime en WOT-2026-013o/IN_PROGRESS/BUILDER; validate 0/0; bus seq 1294 BOOTSTRAP->IN_PROGRESS real.

Conteo pre-fix: validate_observations.py --strict -> 17 errores (FALLIDA).

Separacion verificada (no relato, leido del archivo real):
- 14 applies_to-corrupt (L6-18,23): applies_to contiene un valor de DOMAIN (review-quality, supervisor, bus, planning, builder-contract, launcher, recovery, preflight, manager). El campo applies_to canonico es {all,code,docs,mixed}. El dato real de applies_to se perdio; reparacion determinista honesta = "mixed" (no inventar code/docs). El domain de esas lineas YA es valido (no se toca).
- 3 domain-contract (L42,51,53): domain fuera del enum.
  - L42 collaboration (backlog reconcile tras rescope) -> delivery-hygiene.
  - L51 collaboration (topologia motor-destino / donde vive backlog) -> bus-architecture.
  - L53 test-performance (conteo provisional suite) -> testing.
  Decision: mapear a dominios canonicos existentes con justificacion (NO ampliar enum: no justifican taxonomia nueva; son sub-casos). Evita CONTRACT_GAP de reforma amplia.

Seam confirmado y DEFECTO encontrado (CEM: evidencia, no relato):
- scripts/migrate_observations.py YA existe (WT-2026-191) con backup/rollback/idempotencia.
- BUG: run_migration loop (l.530) marca "KEPT INTACT" toda entrada con _is_canonical_and_valid (non-strict + domain valido), SIN verificar applies_to valido. Las 14 corruptas tienen domain valido -> quedan intactas con applies_to corrupto -> migrador NO las repara.
- dry-run actual: "Would migrate 3 entries, keep 84 intact" -> las 14 NO se reparan. Confirmado.
- _normalize_applies_to (l.235) SI repara (->mixed) pero solo se llama en _migrate_entry, al que las 14 nunca llegan por la guarda intact.

Plan minimo: (1) corregir la guarda intact para que applies_to invalido fuerce migracion; (2) DOMAIN_MIGRATION_MAP += collaboration/test-performance; (3) barrera FAIL-sin/PASS-con. No tocar consumidores reales. No insertar la observacion diferida de 013n.

## WOT-2026-013o - Fase 1/2 cierre (gates + evidencia)

Productivo motor: commit 132b7c3 (scripts/migrate_observations.py + 2 tests). validate_observations.py y ap-schema.md SIN cambios (decision: mapear, no ampliar enum).

Reparacion del dato vivo (deliverable):
- observations.jsonl del destino es GITIGNORED (runtime L1, no versionado): el deliverable es el estado en disco, evidenciado por --strict, con backup como rollback.
- Pre: validate_observations.py --strict -> 17 errores (FALLIDA).
- migrate_observations.py --file <obs> --apply -> "Migrated 17 entries, kept 70 intact, excluded 0. Validation PASSED."
- Backup: observations.jsonl.bak.20260622180300 (gitignored).
- Post: validate_observations.py --strict -> EXITOSA (0 errores).
- Reparacion verificada por clase: 14 applies_to corruptos -> "mixed" (domain preservado); 3 domain -> delivery-hygiene (L42) / bus-architecture (L51, topic override) / testing (L53).

Gates (comandos exactos, exit codes reales):
- validate_observations.py --strict --file <obs> -> EXITOSA / exit 0.
- python -m pytest tests/test_migration_bootstrap.py tests/unit/test_validate_observations.py -q -p no:cacheprovider -> 101 passed / exit 0 (36 migration incl 4 barreras nuevas + 65 validator incl 3 contrato).
- uv run ruff check <4 archivos> -> All checks passed! / exit 0.
- uv run ruff format --check <4 archivos> -> 4 files already formatted / exit 0.
- python scripts/run_pytest_safe.py --level all -> 3129 passed, 20 skipped / exit 0; tested_commit_sha == HEAD (132b7c3).
- validate --json --project-root <repo_destino> -> 0 errors / 0 warnings.

Barrera FAIL-sin/PASS-con: test_corrupt_applies_to_is_not_kept_intact (FAIL pre-fix: la guarda intact ignoraba applies_to) + test_migration_repairs_corrupt_applies_to (PASS post-fix: --strict verde). Idempotencia y backup/rollback cubiertos.

Fuera de scope (explicito): 013o NO inserta memoria portable nueva; la observacion diferida de 013n queda pendiente para promocion posterior sobre base --strict verde. No se tocaron consumidores reales (memory_loader, memory_consolidate) ni forbidden surfaces.

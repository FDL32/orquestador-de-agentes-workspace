# Execution Log -- WOT-2026-013l

**Estado:** IN_PROGRESS

## Bootstrap operativo -- WOT-2026-013l

Ticket NUEVO activado para introducir retencion local, opt-in y auditable sobre superficies runtime gitignored del repo de dogfooding, manteniendo fuera de scope el historico versionado y el lifecycle de cierre.

Procedencia (VERIFICADO 2026-06-25):
- `WOT-2026-013u` ya cerro canonico en `COMPLETED` y deja el entorno listo para promover el siguiente follow-up de menor riesgo.
- El packet canonico de `013l` vive en `.agent/planning/work_plan_WOT-2026-013l.md`.
- La cola viva conserva `013l` como follow-up actual en la familia 013; `013k` sigue diferido por tocar historico versionado mas delicado.
- Premisa verificada por bytes: `.agent/runtime/reviews/`, `.agent/runtime/review_packets/` y `observations.jsonl.bak.*` estan gitignored/local-only; `events/archive`, `audits/system_health` y `_archive/plan_audit` quedan expresamente fuera de scope.

Bus: bootstrap ejecutado via `--bootstrap-ticket`; el estado activo ya queda en `IN_PROGRESS` para el siguiente Builder loop.

Nota para el Builder:
- El ticket exige una CLI standalone (`scripts/prune_runtime_retention.py`), NO integracion en `session-close` ni cambios sobre productores.
- La barrera principal debe FALLAR si aparece spillover a historico versionado o si `dry-run` borra de verdad.
- `.gitignore`, `MANIFEST.*`, `agent_controller.py`, `bus/**` y productores de runtime quedan fuera de scope.

## Fix de barreras fragiles tras fallo de CI -- WOT-2026-013u (Builder, 2026-06-25)

PROBLEMA (detectado por el push/CI, no por gates locales): las barreras de 013u
acoplaban al estado VIVO del workspace de dogfooding. Usaban
`--project-root <workspace_real>` y aserttaban sobre "does not match active
ticket", que solo aparece si el workspace tiene un ticket activo DISTINTO del
fake. En CI (o con el workspace en otro ticket) el error es
"No active ticket found in work_plan.md" -> 5 barreras FALLARON. Anti-patron de
fixture irreal / acople a estado externo. Causa raiz: diseno de test fragil MIO,
no scope creep ni problema ajeno.

FIX (solo tests; el fix del parser del controller ya era correcto, NO se toco):
- Helper hermetico en las 3 superficies: cada barrera crea su PROPIO
  `tempfile.TemporaryDirectory()` como project-root con un work_plan placeholder
  SIN ticket activo. Cero dependencia del workspace vivo.
- Marker robusto e independiente del estado: "No ticket_id provided". Aparece
  SOLO si el parser no captura el ticket (sintoma pre-fix, emitido ANTES del
  lookup de work_plan). Ausente => ticket parseado (el flujo emite otro error
  downstream, cualquiera que sea). Se elimino la asercion sobre
  "does not match active ticket" (fragil).
- Anadidos 3 controles negativos (`..._without_ticket_reports_missing` /
  `test_ticket_parser_omitted_reports_no_ticket`): con NINGUN ticket, el marker
  SI aparece -> prueba que los positivos no son vacuos.

Verificacion:
- Focal: 136 passed, con el workspace vivo en WOT-2026-013l (NO 013u) -> demuestra
  hermeticidad (ya no depende del ticket activo).
- Mutation-verify: reintroducida la condicion invertida -> las 4 barreras de
  `--ticket` FALLAN; restaurada -> 136 passed.
- 7 node-ids nombrados en el DoD: existen y pasan.
- ruff check + format: limpios.
- Suite canonica al HEAD post-commit: ver last-run.json.

Scope: solo `tests/test_agent_controller.py`, `tests/unit/test_manager_approve.py`,
`tests/unit/test_request_changes_requeue.py` (todas en el FLT).
`.agent/agent_controller.py` NO cambia (su fix ya era correcto).

## Fase 0 - Diagnostico read-only (Builder, 2026-06-25, cwd=repo_motor, HEAD=0dffbf8)

Premisa CONFIRMADA (VERIFICABLE POR BYTES):
- Las 3 superficies objetivo estan gitignored: `.gitignore:39` reviews/, `:40`
  review_packets/, `:70` observations.jsonl.bak.*. Excluidas (comentadas) en
  MANIFEST.distribute/.workspace -> local-only, no portable.
- Productores vivos (read-only en este ticket): review_bridge/review_report
  (reviews+packets), memory_consolidate/migrate_observations (baks). No existe
  politica de retencion dedicada -> deuda local real.
- validate del workspace verde antes de tocar -> higiene local, no reparacion.

Estructura real en repo_destino:
- `.agent/runtime/reviews/`: 108 entradas, cada una es un DIRECTORIO por ticket
  (p.ej. `WP-2026-177/`).
- `.agent/runtime/review_packets/`: 47 ARCHIVOS `<ticket>_attempt-N.md`.
- `.agent/runtime/memory/observations.jsonl.bak.*`: 17 ARCHIVOS con timestamp
  `YYYYMMDDHHMMSS` en el nombre.
- Superficies PROHIBIDAS presentes (nunca tocar): events/archive,
  audits/system_health, collaboration/archive, collaboration/_archive.

Decisiones de diseno (deterministas, conservadoras, dentro del contrato):
- Una raiz fija por superficie; el selector SOLO resuelve candidatos dentro de
  esas 3 raices (rechaza cualquier path que escape -> defensa anti-spillover).
- Retencion: conservar los N mas recientes por mtime (desempate por nombre);
  podar el resto. `--keep-reviews/-packets/-observation-baks <N>`.
- `--dry-run` XOR `--apply` (exactamente uno, explicito); sin modo -> no borra.
- reviews -> rmtree de dir por ticket; packets/baks -> unlink de archivo.

Desviaciones de scope: ninguna. FLT: scripts/prune_runtime_retention.py (nuevo) +
tests/unit/test_prune_runtime_retention.py (nuevo). Forbidden surfaces intactas.

## Fase 1-3 - Implementacion, barreras y gates (Builder, 2026-06-25)

Entregables (FLT, NUEVOS):
- `scripts/prune_runtime_retention.py`: CLI standalone opt-in. Resuelve
  `--project-root`, opera SOLO sobre las 3 superficies fijas (reviews/,
  review_packets/, observations.jsonl.bak.*). Modo explicito `--dry-run` XOR
  `--apply` (mutually_exclusive_group required) -> sin modo no borra. Flags
  `--keep-reviews/-packets/-observation-baks <N>` (defaults conservadores
  20/20/10). Retencion: conserva los N mas recientes por mtime (desempate por
  nombre, determinista); poda el resto. INVARIANTE anti-spillover: cada candidato
  se valida contenido en su raiz fija (`_is_contained` + check de parent);
  cualquier path que escape -> RuntimeError. reviews -> rmtree de dir por ticket;
  packets/baks -> unlink.
- `tests/unit/test_prune_runtime_retention.py`: 9 tests hermeticos (cada uno crea
  su tmp project-root con las 3 superficies + las 4 superficies PROHIBIDAS
  pobladas con entradas viejas para probar que NUNCA se seleccionan).

Tests nombrados en el DoD (los 6, todos verdes):
- TestRuntimeRetentionSelection::test_collects_only_gitignored_runtime_targets
- TestRuntimeRetentionSelection::test_keep_count_prunes_old_review_and_packet_entries
- TestRuntimeRetentionSelection::test_observation_backups_follow_the_same_retention_policy
- TestRuntimeRetentionCLI::test_dry_run_reports_without_deleting
- TestRuntimeRetentionCLI::test_apply_deletes_only_selected_candidates
- TestRuntimeRetentionSafety::test_versioned_history_surfaces_are_never_selected
Extras: test_requires_explicit_mode, test_keep_negative_is_rejected,
test_cli_subprocess_dry_run_is_hermetic.

Evidencia mutation-verified (las 2 barreras criticas del contrato):
- Mute `prune` para que dry-run borre -> test_dry_run_reports_without_deleting FALLA.
- Anadi una 4a Surface apuntando a runtime/events/archive (spillover) ->
  test_versioned_history_surfaces_are_never_selected FALLA (detecta el spillover).
- Restaurado -> 9 passed.

Dry-run real contra el workspace (no borra): identifico 52 candidatos
(reviews/packets/baks); reviews antes=108 despues=108 (cero borrado en dry-run).

Gates (comandos exactos + exit):
- `pytest tests/unit/test_prune_runtime_retention.py -q` -> 9 passed (exit 0).
- `ruff check` (2 archivos) -> All checks passed; `ruff format` -> formatted.
- `validate --json --force --project-root <repo_destino>` -> 0 errors / 0 warnings.
- Suite canonica `run_pytest_safe --level all`: al HEAD post-commit (last-run.json).

Scope: sin creep. Solo los 2 archivos NUEVOS del FLT. Forbidden surfaces
(controller, bus, runtime, productores, gitignore, manifests, historico versionado)
NO tocadas. CLI no cableada a session-close/mark-ready/controller.

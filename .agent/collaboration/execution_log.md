# execution_log.md -- WOT-2026-008f

**Estado:** READY_FOR_REVIEW

## Fase 0 -- Preflight Manager

- WOT-2026-008e cerrado canonicamente y publicado antes de preparar 008f.
- work_plan.md creado para WOT-2026-008f desde T-008F-001.
- STRATEGY_WOT-2026-008f.md y AUDIT_WOT-2026-008f.md creados.
- Objetivo: integrar en un wrapper unico los checks vivos de engranaje motor-destino y lifecycle operativo sin duplicar logica ni mutar un destino real durante las pruebas.
- Pendiente de Builder: baseline Fase 0, implementacion del wrapper, tests de barrera, gates y handoff canonico.
## Builder Fase 0 - Diagnostico + baseline (2026-06-18)

- Preflight verde: validate --json 0/0; STATE=008f/IN_PROGRESS; TURN=BUILDER/008f/IMPLEMENT; work_plan=008f.
- Baseline: check_destino_publish_ready.py --project-root <destino> -> EXIT 0 ("validate 0/0 y STATUS=IN_PROGRESS ... publicable").
- T-008F-001 frozen; 008e COMPLETED; 008c satisfecho (INDEX generado, --check-index verde).
- Seams confirmados (firmas reales):
  1. validate_authority.py: find_all_agent_dirs(root) y is_canonical_authority(path, canonical_root) toman root arbitrario -> delegables por import para destino. main() es CLI-only y hardcodea canonical_root del motor (__file__.parent.parent) -> NO usable para destino. Plan: extraer helper exportable sin tocar main().
  2. check_destino_publish_ready.main(argv) -> int (0 publicable, 1 errores validate, 2 STATUS no publicable, 3 link/arg error). Delego por import + propago exit code; NO reescribo _run_validate.
  3. classify_publication.build_manifest(repo_root, scan_history=True, out_path=None, allow_motor_root=False) -> dict, "never mutates repo". Punto de delegacion para auditoria opt-in (dry-run).
  4. resolve_motor_link(project_root) valida solo clave 'motor_root'. El link real tiene motor_root, destination_root, motor_version, manifest_version. El wrapper valida tambien destination_root (coherente con --project-root) y falla cerrado ante link ausente/invalido.
- Sin desviacion de scope. Sin CONTRACT_GAP: todas las piezas son delegables sin tocar CLI vivo.

## Builder - desviacion de diseno (CEM) sobre validate_authority

- El contrato preveia "extraer helper exportable en validate_authority.py" para la autoridad de destino.
- BLOQUEO REAL: guard_paths.py:31 lista r"auth" como patron protegido -> editar scripts/validate_authority.py es rechazado por el hook de seguridad ("ruta protegida por patron: auth"). No corresponde al Builder desactivar el guard.
- DECISION (cumple el contrato sin tocar el archivo protegido): el wrapper IMPORTA los helpers ya exportables hoy (is_canonical_authority, find_all_agent_dirs, detect_legacy_copies) y construye check_destination_authority() en check_motor_destination_integration.py. Cumple "reutiliza via import, no via main()" con MENOS superficie tocada y sin tocar CLI ni logica central de validate_authority.py.
- Efecto en FLT: scripts/validate_authority.py NO se modifica (queda como Read/inspect de facto). Es mas restrictivo que el plan, no menos. Sin scope creep.

## Builder Fase 1 - Implementacion (2026-06-18)

- Creado scripts/check_motor_destination_integration.py: wrapper con --project-root (obligatorio), --motor-root (opcional), --audit-publication (opt-in). Exit codes 0/1/2/3 documentados.
- Checks en orden (corta en primer fallo): link (motor_root+destination_root coherentes, fail-closed exit 3) -> autoridad destino (helpers de validate_authority por import; backups no son split-brain) -> contexto -> gate pre-push (delega check_destino_publish_ready.main(argv), propaga exit) -> auditoria opt-in (build_manifest dry-run).
- validate_authority.py NO modificado (guard_paths bloquea patron "auth"); helper de autoridad vive en el wrapper por import. Desviacion CEM ya registrada arriba.
- Smoke real: default mode contra el destino real -> EXIT 0 (link/authority/context/gate verdes). Audit path validado (lee tree_secret_scan.findings / history_secret_scan.findings correctamente).
- Creado docs/protocol/motor_destination_integration_WOT-2026-008f.md (uso, exit codes, tabla de reutilizacion, nota validate_authority, limites, reproduccion).

## Builder Fase 2 - Tests + Gates

- tests/test_check_motor_destination_integration.py (NUEVO): 19 tests sobre layouts aislados en tmp_path (sin mutar destino real).
  - TestCheckLink: link ausente, JSON invalido, destination_root incoherente, link coherente.
  - TestCheckAuthority: collab ausente, sin work_plan, canonico OK, backups-no-split-brain, split-brain real (find_all_agent_dirs stubeado porque excluye paths bajo tests/ por diseno).
  - TestRunIntegrationDelegation: propaga 1->CHECK_FAILED, 2->STATUS_NOT_PUBLISHABLE, 3->CHECK_FAILED, 0->OK; link roto corta antes del gate.
  - TestPublicationAuditOptIn: no corre por defecto, corre con flag, falla cerrado ante hallazgo.
  - TestMainCLI: project-root inexistente -> config error; regresion roja->verde.
- Focal: pytest tests/test_check_motor_destination_integration.py -v -> 19 passed.
- ruff check All checks passed; ruff format 2 files unchanged; encoding guard EXIT 0; 0 control chars en archivos tocados.

## Entrega

- Commit motor productivo: a5e4e56 (3 archivos nuevos, +607).
- Pendiente: suite canonica level=all contra HEAD + handoff.

## Builder - Manager CHANGES resueltos (2026-06-18)

Manager veredicto CHANGES, 2 gaps de clasificacion. Ambos corregidos:

### ALTO - auditoria ignoraba blockers no-secret del manifest
- Causa: run_publication_audit solo miraba tree/history_secret_scan.findings -> reportaba "clean" aunque verdict fuera NO_ACEPTAR_TODAVIA (p.ej. MOTOR_ROOT_PUBLICATION_GUARD) sin secretos.
- Fix: ahora evalua manifest["verdict"] contra _PUBLISHABLE_VERDICTS = {LISTO_PARA_PUBLICAR, LISTO_CON_REDACTIONS}; cualquier otro verdict falla cerrado reportando verdict + blocked_reasons (codes) + conteo de secretos.
- Verificado en codigo: _decide_verdict (classify_publication.py:485) tiene 4 verdicts; blocked_reasons incluye MOTOR_ROOT_PUBLICATION_GUARD (L454-480) no-secret.

### MEDIO - motor_root inexistente se degradaba a exit 1 en vez de 3
- Causa: check_link validaba presencia/coherencia textual pero no existencia en disco de motor_root; check_destino_publish_ready devolvia 3 (config) y el wrapper lo remapeaba a 1, contradiciendo su propio contrato de exit codes.
- Fix: check_link valida Path(effective_motor).exists() y falla cerrado (exit 3) en el paso de link, cortando antes del gate.
- Smoke: check_link con motor_root inexistente -> ok=False, "[LINK] motor_root does not exist on disk".

### Tests + gates
- +6 tests (25 total): test_nonexistent_motor_root_fails_at_link, test_nonexistent_motor_root_maps_to_exit_3, y TestPublicationAuditVerdict (clean/redactions pasan, non-secret-blocker falla, secret-finding falla).
- Focal: pytest tests/test_check_motor_destination_integration.py -q -> 25 passed.
- ruff All checks passed; format unchanged; encoding EXIT 0; 0 control chars.
- Commit productivo: 86c6425.
- Pendiente: suite canonica level=all contra HEAD 86c6425 + handoff.

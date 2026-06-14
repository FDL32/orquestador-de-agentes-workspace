# Work Plan: WOT-2026-003d - install/sync: jamas prunear rutas trackeadas del destino

## Metadata
- **ID:** WOT-2026-003d
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Alias historico:** MOTOR-FU-001
- **Titulo:** El residue-prune del instalador nunca borra rutas git-trackeadas del repo_destino
- **Asignado a:** Builder
- **Severidad:** Alta | **Riesgo:** Alto (instalador; toca borrado en working tree). Cierre SOLO a READY_FOR_REVIEW.
- **Depende de:** WOT-2026-002c (completed)
- **Origen:** session-2026-06-13-host-extends; re-scoped 2026-06-14 tras verificacion de premisa.

## ACTUALIZACION DE SCOPE (premisa original parcialmente obsoleta)
Verificacion empirica (`install --sync --dry-run` contra el destino, READ-ONLY):
- **Premisa original "--sync re-vendoriza el bundle completo (re-crea agent_system/)": FALSA hoy.**
  El instalador solo copia `.agent/` bajo el allowlist de `MANIFEST.workspace` (20 rutas) y
  SALTA subrutas no autorizadas de `.agent/` (hooks, rules, council, templates...). No copia
  `agent_system/`/`skills/`/`scripts/`. (El no-clobber de `.gitleaks.toml` de 004b se ve activo.)
- **Riesgo real actual: `--sync` strict (default) prunea `.agent/docs/`**, que contiene
  deliverables destino-keep TRACKEADOS: `orphans_decision_WOT-2026-002b.md`,
  `triage_manifest.md`, `resource_precedence.md`. Evidencia: dry-run -> "Residues selected for
  cleanup (automatic (strict)): 1 -> docs"; `git ls-files .agent/docs` no vacio.

## Nuevo contrato (canonico)
El residue-prune del instalador solo puede actuar sobre residuos NO TRACKEADOS por git en el
repo_destino. JAMAS borra una ruta trackeada por git, este o no en `MANIFEST.workspace`. Esto
protege `.agent/docs/` hoy y cualquier futuro deliverable destino-keep que el manifiesto aun
no conozca. Fail-safe: si no se puede determinar el estado git-trackeado, NO prunear.

## Decision Arquitectonica
Se corrige el chokepoint de prune (`prune_residues`) en lugar de abrir un modo nuevo de instalacion o ampliar `MANIFEST.workspace` para un caso puntual. La decision protege cualquier superficie destino-keep trackeada por git, no solo `.agent/docs/`, y mantiene intacta la deteccion de residuos untracked. El criterio es fail-safe: si el instalador no puede determinar el estado git-trackeado, no borra.

## Files Likely Touched (repo_motor)
scripts/install_agent_system.py
tests/unit/test_install_agent_system.py

## Read/inspect only
- `MANIFEST.workspace` (allowlist; no se modifica).
- `detect_destination_residues`, `prune_residues` (chokepoint de prune).

## Manager-only / Revision
- Revision adversarial INDEPENDIENTE obligatoria (code + alto blast radius + politica FALLBACK).
- Cierre SOLO a READY_FOR_REVIEW. NO `manager-approve`. NO push. Espera revision independiente.

## Non-goals
- NO re-introducir un modo host-extends amplio (premisa de re-vendor obsoleta).
- NO modificar `MANIFEST.workspace` ni la logica de copia (`copy_tree`).
- NO cambiar la deteccion de residuos para untracked (deben seguir detectandose).
- NO anadir dependencias (git via subprocess; subprocess ya importado).

## Criterios binarios de cierre (a READY_FOR_REVIEW)
- [ ] `prune_residues` excluye del prune toda ruta git-trackeada del destino (strict E interactivo).
- [ ] Mensaje auditable `[SKIP] residue is git-tracked...` por cada ruta protegida.
- [ ] Fail-safe: si no se puede determinar tracked (git ausente), NO prunear (warning).
- [ ] Residuo UNTRACKED se sigue detectando y se prunea normalmente.
- [ ] Test barrera: destino con `.agent/docs/*.md` TRACKEADO + un residuo untracked; verificar
      que `.agent/docs` NO se selecciona/prunea y el untracked SI.
- [ ] `ruff` limpio; `run_pytest_safe` motor verde; encoding 0.
- [ ] Commit en repo_motor con WOT-2026-003d. Ticket queda READY_FOR_REVIEW (no cerrado).

## STOP / escalado
- Si el guard pudiera bloquear un prune legitimo de untracked, parar y acotar.
- Si la deteccion de "tracked" no es fiable en algun entorno, preferir fail-safe (no borrar).

## Gates (deliverable_type: code)
- `ruff check`/`format --check` sobre los .py tocados.
- `python scripts/run_pytest_safe.py` (cwd=motor) incluyendo el test nuevo.
- `check_encoding_guard.py`; `check_motor_pristine --check` vs snapshot.

## Entregables
- `install_agent_system.py` con guard git-tracked en el prune (+ helpers).
- Test de barrera en `tests/unit/test_install_agent_system.py`.
- Evidence packet para revision independiente (diff, dry-run antes/despues, gates).
- `orchestrator_pipeline/reports/readyforreview_WOT-2026-003d.md` (no closeout: queda abierto).


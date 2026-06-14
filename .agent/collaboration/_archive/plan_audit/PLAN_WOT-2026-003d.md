# PLAN WOT-2026-003d - never prune git-tracked destino paths

## Pasos (todo en repo_motor)
1. `scripts/install_agent_system.py`:
   - Añadir `_git_tracked_relpaths(repo_root) -> set[str] | None`: si `repo_root/.git` no
     existe -> set() (no repo, nada trackeado). Si existe -> `git -C repo_root ls-files -z`;
     en FileNotFoundError/OSError o returncode!=0 -> None (no determinable).
   - Añadir `_filter_git_tracked_residues(repo_root, agent_dir, residues) -> (safe, protected)`:
     si tracked is None -> ([], list(residues)) + warning (fail-safe: no prunear). Si set,
     un residuo `rel` esta protegido si su ruta repo-relativa (`(agent_dir/rel).relative_to(repo_root)`)
     esta en tracked o algun tracked empieza por `repo_rel + "/"`.
   - En `prune_residues`: antes de seleccionar, filtrar con el helper; imprimir
     `[SKIP] residue is git-tracked (destino-keep), not pruning: <rel>` por protegido;
     continuar solo con los safe.
2. `tests/unit/test_install_agent_system.py`: test barrera (git init en tmp dest, `.agent/docs/x.md`
   trackeado + `.agent/junk/y.txt` untracked; `prune_residues(..., dry_run=False, interactive=False)`;
   assert docs NO removido y junk SI). + test fail-safe (sin .git -> set vacio -> prune normal;
   y simular git ausente si es factible -> protege todo).
3. Gates: ruff, run_pytest_safe, encoding. Commit WOT-2026-003d. mark-ready (READY_FOR_REVIEW). NO approve. NO push.

## Seams / invariantes
- `prune_residues` es el unico chokepoint (strict + interactivo). Guard ahi cubre ambos.
- Fail-safe: incertidumbre -> no borrar.
- Deteccion de residuos intacta (untracked se sigue viendo).

## Evidencia esperada
- Diff; dry-run antes (prunea docs) / despues (skip docs git-tracked); test barrera verde; suite verde.

## STOP
- Ver work_plan. Cierre solo READY_FOR_REVIEW.

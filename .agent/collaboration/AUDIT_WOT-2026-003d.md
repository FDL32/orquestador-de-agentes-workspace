# AUDIT WOT-2026-003d - never prune git-tracked destino paths

## Objetivo
Verificar que el residue-prune nunca borra rutas git-trackeadas del destino, con fail-safe
ante incertidumbre, sin romper el prune de untracked ni la deteccion.

## Reglas de revision (INDEPENDIENTE, alto blast radius)
- Revisar el diff real; re-derivar; no fiarse del relato.
- Confirmar que el guard esta en el chokepoint (`prune_residues`), cubre strict E interactivo.
- Confirmar fail-safe: tracked indeterminado -> NO prunear.
- Confirmar que el test barrera USA un repo git real (git init/add/commit en tmp), no un mock
  de git (evitar mock drift). Debe fallar con el codigo viejo (sin guard) y pasar con el nuevo.
- Confirmar que un residuo untracked SI se prunea (no se sobre-protege).
- `check_motor_pristine`: motor_status_new = solo install_agent_system.py + test.

## Hallazgos bloqueantes tipicos
- CRITICO: el guard no cubre el modo strict (default) -> sigue borrando destino-keep.
- CRITICO: fail-safe invertido (incertidumbre -> borra).
- ALTO: el test mockea git en vez de usar un repo real (mock drift; no prueba el contrato).
- ALTO: el guard sobre-protege y deja de prunear untracked legitimo.
- MEDIO: deteccion de residuos rota (untracked ya no se ve).

## TP Check
TP-01: guard en `prune_residues`; cubre strict e interactivo. (diff)
TP-02: ruta git-trackeada (`.agent/docs`) NO se prunea; mensaje [SKIP] auditable. (test/exec)
TP-03: residuo untracked SI se prunea. (test)
TP-04: fail-safe: git ausente/indeterminado -> no prunea (warning). (test/diff)
TP-05: test barrera con repo git real; falla con codigo viejo, pasa con nuevo. (test)
TP-06: ruff 0; run_pytest_safe motor verde; encoding 0; commit WOT-2026-003d; READY_FOR_REVIEW (no cerrado). (command/git)

## Criterio de rechazo inmediato
- Sigue pruneando tracked; o fail-safe invertido; o test con mock de git; o cierre del ticket
  sin revision independiente.

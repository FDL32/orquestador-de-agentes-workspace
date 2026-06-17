# AUDIT_WOT-2026-010h -- Criterios de auditoria

## Contrato estructural

- [ ] El diff se limita a los 4 prompts declarados + artefactos de colaboracion.
      Cero cambios en codigo, runtime, bus o gates.
- [ ] No se toca `bus/ticket_id.py`, `QUICKSTART.md`, `INTERACTION_MODES.md` ni
      prompts/artefactos de 010g.

## Evidencia minima

- [ ] Cada uno de los 4 prompts (`session_bootstrap.md`,
      `destination_bootstrap.md`, `audit_complete_motor_destination.md`,
      `audit_post_change_system_health.md`) declara explicitamente que el
      `<PREFIX>` se lee del contrato del repo activo
      (`AGENTS.md`/`CLAUDE.md`), verificado via `agent_controller --validate`.
- [ ] `WOT-` aparece descrito SOLO como prefijo del motor/dogfooding, no
      universal, en cada prompt tocado.
- [ ] Los 4 prompts no se contradicen entre si (Manager cruza la formulacion).
- [ ] No hay ejemplos vivos nuevos con `WP-`/`WT-` (revisar diff linea a linea).
- [ ] `python scripts/check_ticket_nomenclature.py` pasa.
- [ ] `python scripts/check_encoding_guard.py <md tocados>` exit 0.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
      termina 0 errors / 0 warnings.

## Anti-patrones a rechazar

- Regla de prefijo redefinida en paralelo con palabras distintas por prompt.
- Ejemplo vivo que use `WP-`/`WT-` como plantilla (no historia/etiquetado).
- Afirmar que el prefijo se valida por una linea de `PROJECT.md` en vez de via
  `--validate`.
- Scope creep a documentacion general o a 010g.
- Cierre citado sin evidencia literal del gate de nomenclatura + encoding +
  validate 0/0.

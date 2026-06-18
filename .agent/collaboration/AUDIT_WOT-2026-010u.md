# Audit Checklist: WOT-2026-010u

## Blockers

- El fix auto-commitea sin accion explicita del usuario/flujo de cierre.
- El fix borra artefactos historicos en vez de preservar rename.
- No hay test con git real para delete+untracked hacia `_archive/plan_audit/`.
- El diagnostico no da comando de remediacion accionable.
- El guard bloquea archivos que no son `STRATEGY_`, `PLAN_` o `AUDIT_` cerrados.
- `validate --json` no termina 0/0.

## Acceptance Checks

- Test rojo/verde demuestra el limbo y el bloqueo.
- Razon estable: `archive_rename_uncommitted` o equivalente documentado.
- Mensaje self-service incluye old path, new path y `git add -- <old> <new>`.
- No cambia bus ni dependencias.
- Documentacion del protocolo existe.

## Manager adversarial checks

- Simular un archivo no relacionado en `_archive/plan_audit/`: no debe disparar.
- Simular solo un delete sin copia archivada: debe reportarse como dirty normal, no como rename incompleto.
- Revisar que `_archive/` siga permitido como superficie historica, pero el par delete+untracked no quede invisible.
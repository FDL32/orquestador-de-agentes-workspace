# Execution Log WOT-2026-005a

**Estado:** IN_PROGRESS

## Metadata

- **ID:** WOT-2026-005a
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** EXECUTE

## Resumen

- Pipeline orquestado (FALLBACK_SIN_TASK_TOOL). Doc ticket: añadir a
  `prompts/memory_upload.md` la decision obligatoria de destino de memoria (privada vs
  portable motor vs portable destino) + regla de drift de schema. Scope motor.

## Ejecucion Builder

FALLBACK_SIN_TASK_TOOL. Orquestador como Builder via Bash (motor file). Doc ticket.

### Cambio (`prompts/memory_upload.md`)
- Nueva seccion `## Decisión de destino de memoria (obligatoria antes de escribir)`:
  tabla de 3 destinos (Claude privada / portable motor / portable destino) con
  portabilidad/validabilidad, + 4 reglas binarias (declarar destino; evidencia por destino;
  promocion a observations.jsonl solo con schema + consumidor real, si no `NO PROMOVIBLE`;
  decidir promover-o-no lo privado).
- Subseccion `### Drift de schema en observations.jsonl`: prohibido añadir portables nuevas
  sobre schema en drift sin ticket de migracion.

### Gates / evidencia
- `check_encoding_guard.py prompts/memory_upload.md`: exit 0 (acentos preservados).
- `validate --project-root .` (destino): 0 errores.
- `check_motor_pristine --check`: solo `prompts/memory_upload.md` cambia.
- 3 criterios binarios presentes (grep: Decisión de destino / NO PROMOVIBLE / Drift de schema).

### Commit (repo_motor)
- (ver commit docs WOT-2026-005a)

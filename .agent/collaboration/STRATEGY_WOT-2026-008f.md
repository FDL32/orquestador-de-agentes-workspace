# STRATEGY_WOT-2026-008f.md

## Enfoque

1. Baseline read-only: confirmar `008e` COMPLETED, `008c` como premisa tecnica satisfecha, ejecutar `validate --json`, `check_destino_publish_ready.py` y leer `destination_context.py`, `classify_publication.py`, `validate_authority.py` poniendo foco explicito en que `validate_authority.main()` es CLI-only y que `check_destino_publish_ready` reutilizable hoy entra por `main(argv)`.
2. Crear `scripts/check_motor_destination_integration.py` como wrapper unico con `--project-root` obligatorio y `--motor-root` opcional.
3. Mantener dos modos separados: modo operativo por defecto y auditoria de primera publicacion solo con flag explicito.
4. Delegar en checks existentes siempre que sea viable; si hace falta extraer helpers pequenos desde scripts vivos, hacerlo sin duplicar semantica ni cambiar su contrato CLI. En `validate_authority.py`, extraer helper exportable para destino sobre `is_canonical_authority(...)` y `find_all_agent_dirs(...)` sin tocar `main()`. En `check_destino_publish_ready.py`, delegar por `main(argv)` y propagar exit code; extraer helper solo si hace falta estructura adicional.
5. Cubrir con tests de integracion livianos sobre fixtures/tmp: link roto, publish-ready failure, autoridad/manifest incompatible y publication audit opcional. Para auditoria de primera publicacion, el punto de delegacion preferente es `classify_publication.build_manifest(...)`.
6. Si se tocan prompts, limitarlo a anadir una referencia minima al wrapper nuevo; no reescribir flujo operativo ni auditorias existentes.
7. Documentar exit codes, comandos de reproduccion y limites del wrapper en un artefacto puntual.

## Tests esperados

- `tests/test_check_motor_destination_integration.py` (nuevo): wrapper verde en fixture valida y fail-closed en link roto.
- `tests/test_check_motor_destination_integration.py` (nuevo): propaga fallo de `check_destino_publish_ready` sin duplicar su diagnostico central.
- `tests/test_check_motor_destination_integration.py` (nuevo): el modo de auditoria de publicacion solo corre con flag explicito.
- Ajustes minimos en `tests/test_destination_context.py`, `tests/test_prepush_check.py` o `tests/test_classify_publication.py` solo si el wrapper necesita helpers existentes hoy no exportados.
- Focal real sobre archivos tocados.

## Riesgos

- Duplicar logica ya viva en `check_destino_publish_ready.py` o `classify_publication.py`: bloquear.
- Cambiar la logica central o el contrato CLI de scripts envueltos en vez de extraer helpers exportables: bloquear.
- Convertir un gate operativo en un scan historico obligatorio: bloquear.
- Probar guards escribiendo en un destino real: bloquear.
- Abrir scope a instalador/launcher sin necesidad: bloquear.

## Gates

- `python -m pytest tests/test_check_motor_destination_integration.py -v` mas focales reales derivados
- `ruff check` y `ruff format --check` sobre Python tocado
- `python scripts/check_encoding_guard.py <archivos tocados>`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0
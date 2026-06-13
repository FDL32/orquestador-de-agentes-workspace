# PLAN WOT-AUDIT-CI - CI del destino portable bajo host-extends

## Objetivo
Espejo tecnico de `work_plan.md`. Redefinir `.github/workflows/quality-gates.yml`
para validar el estado `.agent/` del destino usando el motor publico via checkout,
sin depender de copias locales de `scripts/`/`tests/`/`skills/`.

## Pasos de ejecucion
1. Leer el workflow actual y confirmar los gates que dependen de copias locales.
2. Reescribir el workflow:
   - paso checkout del destino (existente);
   - paso checkout del motor publico `FDL32/orquestador-de-agentes` en `_motor/`;
   - paso setup-python 3.10;
   - paso validate canonico: `python _motor/.agent/agent_controller.py --validate --json --project-root .` con `AGENT_PROJECT_ROOT=${{ github.workspace }}`;
   - conservar `Workflow reference check` (self-contained);
   - retirar `compileall scripts tests` y la validacion discovery sobre copias locales.
3. Ajustar `paths:` del trigger para no depender de `scripts/**`/`skills/**` (que
   desapareceran), manteniendo `.agent/**` y el propio workflow.
4. Validar YAML localmente (`yaml.safe_load`).
5. Commit + push; verificar el run real con `gh run`.

## Seams / invariantes
- El controller del motor resuelve sus imports relativos a su ubicacion + lee
  estado via `--project-root .` (ya probado localmente todo el dia).
- El motor es PUBLICO: checkout sin secretos.
- El gate canonico del destino es `--validate` (0 errors / 0 warnings).

## Evidencia esperada
- `gh run view <id> --json conclusion` = `success` para el commit del push.
- `yaml.safe_load` sin excepcion.
- validate local 0/0.

## STOP
- Si el validate del motor en Actions requiere deps no presentes: anadir install
  minimo; si no se puede, BLOCKED con log del run. No cerrar en verde fabricado.

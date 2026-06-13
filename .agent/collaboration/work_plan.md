# Work Plan: WOT-AUDIT-CI - CI del destino portable bajo host-extends

## Metadata
- **ID:** WOT-AUDIT-CI
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Titulo:** Redefinir el CI del destino para que no dependa de copias locales del motor
- **Asignado a:** Builder
- **Repo de autoridad:** repo_destino
- **Severidad:** Alta | **Riesgo:** Medio (toca CI vivo de main; verificable por push real)
- **Origen:** WOT-AUDIT-A2 / triage_manifest.md (bucket ci-portability-blocker)

## Objetivo
`.github/workflows/quality-gates.yml` hoy corre `compileall scripts tests` y
`discover_skills.py` sobre copias locales del motor. GitHub Actions hace checkout
SOLO del destino; tras A2d esas copias no existiran y el CI quedaria vacuo o roto.
Redefinir el CI para que valide lo que el destino POSEE (estado `.agent/`) usando
el motor traido como checkout, sin depender de copias vendorizadas.

## Decision Arquitectonica
El motor `FDL32/orquestador-de-agentes` es PUBLICO: Actions puede hacer
`actions/checkout` del motor sin secretos. El CI del destino debe: (1) checkout
del destino, (2) checkout del motor en `_motor/`, (3) correr el gate canonico del
destino `python _motor/.agent/agent_controller.py --validate --json --project-root .`
con `AGENT_PROJECT_ROOT=<workspace>`. Se retira `compileall scripts tests` y la
validacion de discovery sobre copias locales (dejan de existir tras A2d). Se
conserva el `Workflow reference check` (es self-contained). Asi el CI deja de ser
bloqueante de A2d y valida estado real del destino via motor.

## Files Likely Touched
- `.github/workflows/quality-gates.yml`

## Superficies
- **Builder (modifica):** `.github/workflows/quality-gates.yml`; `execution_log.md`.
- **Read/inspect only:** `triage_manifest.md`, controller del motor. NO editar el motor.
- **Manager-only:** review + verificacion del run real via `gh run`.

## Non-goals
- No eliminar copias legacy (eso es A2d).
- No tocar el motor.
- No anadir secretos (el motor es publico; checkout sin token).
- No cambiar el contenido de `.agent/` para "pasar" el validate.

## Criterios binarios de cierre
- [ ] `quality-gates.yml` no referencia `scripts/`/`tests/`/`skills/` locales del destino.
- [ ] El workflow hace checkout del motor (publico) y corre el validate del motor
      con `--project-root .` y `AGENT_PROJECT_ROOT` del workspace.
- [ ] YAML valido (parsea con `yaml.safe_load`).
- [ ] Run real del CI tras push: `gh run` del commit muestra `conclusion=success`.
- [ ] `agent_controller --validate --project-root <destino>` local 0/0.

## STOP / escalado
1. Si el run real falla por una causa fuera del scope del CI (p.ej. el validate
   del motor necesita deps no instaladas en Actions): registrar el fallo real,
   anadir el `pip install`/`uv` minimo necesario, y si no se puede, marcar BLOCKED
   con el log del run (no cerrar en verde).
2. No fabricar "CI pasa": la evidencia es el `gh run ... --json conclusion`.

## Gates (deliverable_type: code; sin Python tocado)
- YAML parse: `python -c "import yaml; yaml.safe_load(open('.github/workflows/quality-gates.yml'))"`.
- `agent_controller --validate --project-root <destino>` 0/0 (local).
- Run real del CI: `gh run list`/`gh run view` del commit del push.
- ruff/pytest: N/A (no se toca Python; politica condicional -> salto auditable).

## Riesgos
- Medio. Un workflow roto deja un run rojo en main (visible, fix-forward).
  Mitigacion: YAML validado localmente + verificacion del run real antes de cerrar.

## Entregables
- `.github/workflows/quality-gates.yml` redefinido + evidencia de `gh run` success.

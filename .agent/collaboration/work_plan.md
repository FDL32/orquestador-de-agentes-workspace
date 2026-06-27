# Plan de Trabajo: WOT-2026-014i

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014i
- **Estado:** COMPLETED
- **Titulo:** Bump de GitHub Actions a versiones no-Node20 en workflows del motor y del workspace
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Prioridad:** Baja
- **Depende de:** -
- **Objective-Link:** OBJ-014I-001
- **Plan-Link:** PLAN-014I-001
- **Builder clarification budget:** 0 (versiones objetivo fijadas; regla 2-commits fijada)

## Objetivo
Subir las action-pins marcadas como Node-20-deprecated a su primer major no-Node20, en los workflows de
AMBOS repos, sin cambiar la logica de los jobs. Verificacion del objetivo (que comando/test lo demuestra): cada YAML tocado parsea (python -c yaml.safe_load),
validate --json del workspace en 0 errors / 0 warnings, run_pytest_safe del motor exit 0; la evidencia PRIMARIA
(workflow verde post-push SIN anotacion Node-20) es Manager-only y se obtiene en el push (gateado a OK humano). Ver DoD.

## Regla cross-repo CONGELADA: 1 ticket = 2 commits
Este ticket toca DOS repos. Se cierra con DOS commits: uno en repo_motor (.github/workflows del motor) y
uno en repo_destino/workspace (.github/workflows del workspace). El workspace NO esta vendorizado por el motor.

## Versiones objetivo CONGELADAS (verificadas que existen via API)
- actions/checkout@v4 -> @v5
- actions/setup-python@v5 -> @v6
- actions/upload-artifact@v4 -> @v5
- astral-sh/setup-uv@v5 -> @v6
(primer major no-Node20 de cada action; minimiza breaking changes vs saltar a latest v7/v8).

## Premise (VERIFICADO en codigo)
- Motor .github/workflows: security-audit.yml, quality-gates.yml, monthly-deps-bump.yml usan checkout@v4,
  astral-sh/setup-uv@v5, actions/setup-python@v5.
- Workspace .github/workflows: security-audit.yml (checkout@v4, setup-python@v5, upload-artifact@v4),
  quality-gates.yml (checkout@v4 x2, setup-python@v5).
- La anotacion Node-20 aparece en los runs; FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 (motor) lo enmascara hoy.

## Premise Re-check (cwd=repo_motor, solo lectura)
grep -rn "uses:" .github/workflows/ ; grep -rn "uses:" C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.github\workflows\
Condicion de arranque: las pins v4/v5 siguen en ambos repos.

## Decision Arquitectonica
- Sustituir SOLO el tag de version en cada `uses:` (checkout@v4->v5, setup-python@v5->v6, upload-artifact@v4->v5,
  setup-uv@v5->v6). NO cambiar steps, env, ni logica de jobs.
- Revisar si FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 sigue siendo necesario tras el bump: dejarlo si alguna action
  restante lo requiere; solo retirarlo si se confirma que ninguna lo necesita (en duda, conservarlo: el bump
  no depende de retirarlo).
- Cada YAML debe seguir parseando correctamente (estructura intacta).

## Files Likely Touched
Motor (repo_motor):
- .github/workflows/security-audit.yml
- .github/workflows/quality-gates.yml
- .github/workflows/monthly-deps-bump.yml
Workspace (repo_destino):
- .github/workflows/security-audit.yml
- .github/workflows/quality-gates.yml

## Read/inspect only
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- La LOGICA / steps / env de los jobs: no se tocan (solo el tag de version de cada uses:).
- El step de gitleaks (ya migrado al CLI OSS en 2d69d57): no se re-toca.
- FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: no retirarlo sin confirmar que ninguna action restante lo necesita.
- Codigo Python, bus/**, runtime/**, .agent/** operativo: prohibidos.
- nuevas dependencias: prohibidas.

## Gates canonicos del ticket (mixed, YAML/CI)
- LOCAL (Builder): cada YAML tocado parsea (estructura valida); validate --json del workspace en 0/0.
- ruff/pytest NO son evidencia principal de cierre (no se toca Python); run_pytest_safe del motor solo confirma
  que el motor sigue verde (no cambia por YAML).
- MANAGER-only / POST-PUSH (gateado a OK humano): cada workflow afectado corre verde y SIN anotacion Node-20.
  Esta es la evidencia PRIMARIA del cierre; se obtiene tras el push.

## Non-goals
- NO cambiar la logica ni los steps de ningun job.
- NO re-tocar gitleaks.
- NO retirar FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 sin confirmacion.

## CONTRACT_GAP / STOP
- Si alguna version objetivo no existe o introduce un breaking change evidente en la estructura del job.
- Si retirar FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 fuese necesario para el bump (no deberia).
-> emitir CG-WOT-2026-014i.md y PARAR.

## DoD (binario)
- [ ] Las 5 superficies (3 workflows motor + 2 workspace) tienen las pins bumpeadas (checkout@v5, setup-python@v6, upload-artifact@v5, setup-uv@v6); NINGUN otro cambio en los jobs.
- [ ] Cada YAML tocado parsea correctamente (estructura valida).
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] python scripts/run_pytest_safe.py --level all del motor -> exit 0 (sin cambios por YAML), tested_commit_sha == HEAD del motor tras el commit motor.
- [ ] DOS commits: uno en repo_motor (mensaje WOT-2026-014i) y uno en repo_destino (mensaje WOT-2026-014i).
- [ ] EVIDENCIA PRIMARIA (Manager-only, post-push, GATEADA): cada workflow afectado corre verde y sin anotacion Node-20. Se completa tras el push (OK humano).
- [ ] la evidencia de cierre cita los SHA de los DOS commits (motor + workspace).

## Handoff
Builder: bump en ambos repos, sintaxis YAML + validate locales, run_pytest_safe del motor, y DOS commits
(motor + workspace). NO --pre-handoff/--mark-ready, NO push. El Manager (post-push gateado) valida CI verde.

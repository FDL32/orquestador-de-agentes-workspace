# Execution Log WOT-AUDIT-A2a

**Estado:** IN_PROGRESS

## Metadata

- **ID:** WOT-AUDIT-A2a
- **deliverable_type:** documentation
- **Rol activo:** MANAGER
- **Accion:** CREATE_PLAN

## Resumen

- Manager redacto `work_plan.md` para WOT-AUDIT-A2a (subfase documentation de
  WOT-AUDIT-A2: host-extends/motor-provides).
- Alcance: documentar la regla de precedencia de recursos (host .agent -> motor
  read-only -> nunca legacy) y mapear los comandos del destino que apuntan a
  copias locales hacia su equivalente del motor externo. SIN mover/borrar nada.
- Evidencia de mapeo recolectada el 2026-06-13 a HEAD destino `13ee7e1` / motor
  `704939f` (ver tabla en work_plan.md).
- Bus inicializado con `--bootstrap-ticket` (STATE_CHANGED -> IN_PROGRESS).

## Hallazgos divergentes registrados como STOP para A2b

- `scripts/test_refactor_kit_performance.py`: existe como copia local en el
  destino pero NO tiene equivalente en el motor -> escalar (gap de capacidad o
  reclasificar como extension del host).
- `agent_system/refactor-kit/install_refactor_kit.py`: entrada allowlist stale
  (ruta hyphen inexistente; el motor lo tiene bajo `refactor_kit/` underscore).

## Pendiente (Builder)

- Crear `repo_destino/.agent/docs/resource_precedence.md` con la decision
  arquitectonica + tabla de mapeo. Cierre con linea artefacto+gate.

## Builder - diagnostico antes del cambio

- Seams confirmados en codigo del motor:
  - `runtime/project_root.py` resuelve el root por `AGENT_PROJECT_ROOT`.
  - `scripts/run_pytest_safe.py` no expone `--project-root`; usa el resolver
    central y acepta `--status`.
  - `scripts/local_audit.py` no expone `--project-root`; solo acepta `--json`
    y `--quick`.
  - `scripts/discover_skills.py` no expone `--project-root`; su host-first
    discovery depende de `cwd/.agent/skills`.
- Evidencia runtime confirmada desde `cwd=repo_destino`:
  - `python <repo_motor>/scripts/discover_skills.py --json` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
  - `python <repo_motor>/scripts/run_pytest_safe.py --status` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
  - `python <repo_motor>/scripts/local_audit.py --json --quick` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
- Desviacion de scope detectada y contenida:
  - el `work_plan.md` usa la forma abreviada `--project-root <repo_destino>` en
    la tabla de equivalencias, pero esa interfaz no existe hoy para al menos
    `run_pytest_safe.py`, `discover_skills.py` y `local_audit.py`. El
    entregable A2a documenta la forma invocable real sin modificar el scope del
    ticket ni tocar A2b.
- Artefacto creado:
  - `repo_destino/.agent/docs/resource_precedence.md`
- Gate final:
  - Doc `.agent/docs/resource_precedence.md` creado. Validate: exit 0, 0 errors,
    1 warning (`TP-STRUCT-01` esperado; `AUDIT_*` con `TP Check` pertenece al
    review artefact del Manager y no a A2a).

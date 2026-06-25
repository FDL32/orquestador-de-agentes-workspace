# Plan de Trabajo: WOT-2026-013t

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013t
- **Estado:** APPROVED
- **Titulo:** Deduplicar UpgradeManager (upgrade.py vs upgrade_agent_system.py) / binding shutil independiente
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Alta
- **Depende de:** WOT-2026-013r
- **Objective-Link:** OBJ-013T-001
- **Plan-Link:** PLAN-013T-001
- **Builder clarification budget:** 0 (el ticket fija owner canonico, FLT, barreras, surfaces prohibidas y el criterio binario de salida; no deja decisiones de arquitectura abiertas)

## Objetivo
Reemplazar las dos implementaciones editables de `UpgradeManager` por un solo owner efectivo, mantener `scripts/upgrade.py` como entrypoint publico documentado, preservar `scripts/upgrade_agent_system.py` solo como compatibilidad explicita si hiciera falta, y dejar el seam de copia (`copytree`/`copy2`) inequ?voco para que las barreras del upgrade fallen sin el fix real.

## Premise
`013r` resolvio el falso verde inmediato de `tests/unit/test_upgrade.py`, pero cerro su DoD por enmienda porque el criterio literal era inalcanzable dentro del Paso 1: `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` al hacer ambos `import shutil`, y ademas el repo conserva dos forks casi identicos de `UpgradeManager`. La realidad verificada hoy sigue siendo dual: `README.md:104` declara canonico `scripts/upgrade.py`, `tests/integration/test_lifecycle_integration.py` importa `scripts.upgrade.UpgradeManager`, y `tests/unit/test_upgrade.py` importa `scripts.upgrade_agent_system.UpgradeManager`. Mientras existan dos owners efectivos o un seam ambiguo de copia, el contrato de pruebas y la documentacion seguiran pudiendo divergir.

## Premise Re-check (cwd=repo_motor, solo lectura)
```
rg -n "Canonical upgrade scripts|upgrade.py|upgrade_agent_system.py" README.md DISTRIBUTION_GUIDE.md UPGRADE_GUIDE.md
rg -n "from scripts.upgrade import UpgradeManager|from scripts.upgrade_agent_system import UpgradeManager|patch\("scripts\.upgrade|patch\("scripts\.upgrade_agent_system" tests/integration/test_lifecycle_integration.py tests/unit/test_upgrade.py
rg -n "import shutil|copytree|copy2|class UpgradeManager|ProjectPathsResolver|DoctorAgentSystem" scripts/upgrade.py scripts/upgrade_agent_system.py
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- `README` sigue declarando canonico `scripts/upgrade.py`;
- el repo aun tiene dos modulos de upgrade con `class UpgradeManager` propia o cuerpo casi duplicado;
- la superficie de tests/documentacion sigue partida entre ambos forks;
- `validate` del workspace sigue en `0 errors / 0 warnings` antes de tocar nada.
Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
La salida de menor ambiguedad es fijar un owner unico de la logica de upgrade y dejar el otro modulo como wrapper/compatibilidad explicita, no mantener dos clases paralelas que requieran disciplina manual para no divergir. En esta ronda, el owner de implementacion permanece en `scripts/upgrade_agent_system.py` (ya integra `ProjectPathsResolver` y `DoctorAgentSystem`, y es la superficie unitaria focal actual); `scripts/upgrade.py` debe quedar como entrypoint publico documentado que reexporta o delega de forma controlada al owner unico. Ademas, el owner unico debe bindear `copytree`/`copy2` de forma que el target correcto sea inequ?voco y la barrera fail-sin-fix no dependa del accidente de un `shutil` compartido.

## Plan - secuencia minima FIJA
### Paso 1 - fijar owner unico de UpgradeManager
- Mover la logica productiva de `UpgradeManager` a un solo owner efectivo y eliminar la segunda clase editable divergente del par `upgrade.py` / `upgrade_agent_system.py`.
- `scripts/upgrade.py` debe seguir siendo la via canonica documentada, pero no puede conservar una segunda clase editable divergente.
- Si hace falta compatibilidad CLI con `upgrade_agent_system.py`, que sea explicita y pequena; no se admite mantener dos cuerpos de logica paralelos.

### Paso 2 - seam de copia inequ?voco
- El owner unico debe exponer un seam de copia (`copytree`/`copy2`) que permita distinguir sin ambiguedad el target correcto del equivocado.
- La barrera debe demostrar que romper la copia en el owner real hace fallar la prueba focal, y que el wrapper/documented entrypoint no reintroduce una segunda ruta mutable.

### Paso 3 - alinear contrato publico y tests
- Alinear README y superficies de test con el owner unico decidido.
- Mantener `scripts/upgrade.py` como entrypoint documentado para el operador.
- La suite no puede terminar con docs diciendo un owner y tests ejercitando otro sin explicitar compatibilidad.

## Files Likely Touched (relativos a repo_motor)
- `scripts/upgrade.py`
- `scripts/upgrade_agent_system.py`
- `tests/unit/test_upgrade.py`
- `tests/integration/test_lifecycle_integration.py`
- `README.md`

Aclaraciones (no parte de las rutas):
- `scripts/upgrade.py`: entrypoint publico canonico; debe dejar de ser fork editable si hoy aun lo es.
- `scripts/upgrade_agent_system.py`: owner unico de implementacion o wrapper legado explicito; no puede quedar ambigua su autoridad.
- `tests/unit/test_upgrade.py`: barreras estructurales contra duplicacion + seam de copia equivocado.
- `tests/integration/test_lifecycle_integration.py`: alinear import surface publica con el owner/wrapper final.
- `README.md`: reflejar la relacion real entre entrypoint publico y owner de implementacion.

## Forbidden Surfaces
- `repo_motor/scripts/rollback.py`, `repo_motor/scripts/detect_version.py`, `repo_motor/scripts/doctor_agent_system.py`, `repo_motor/agent_system/scripts/project_paths.py`: read-only por defecto; solo tocarlos si el diff demuestra necesidad directa del owner unico.
- `repo_motor/.agent/**`, `repo_motor/bus/**`, `repo_motor/runtime/**`: fuera de scope; 013t no toca lifecycle, bus ni cierre canonico.
- `repo_motor/docs/KNOWN_FAILURE_PATTERNS.md`: read-only en esta ronda; ya describe FP-012 como contexto, no es entregable del fix.
- nuevas dependencias, migraciones masivas de guias o retirada de compat legacy fuera del par `upgrade.py` / `upgrade_agent_system.py`: prohibido.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/unit/test_upgrade.py -q
python -m pytest tests/integration/test_lifecycle_integration.py -q
python -m ruff check scripts/upgrade.py scripts/upgrade_agent_system.py tests/unit/test_upgrade.py tests/integration/test_lifecycle_integration.py
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO reabrir 013r ni cambiar su cierre historico.
- NO redisenar el flujo completo de install/upgrade/rollback mas alla de fijar owner unico y seam verificable.
- NO mezclar este ticket con memoria, closeout, bus o runner.
- NO retirar de golpe comandos, imports, guias o referencias operativas de `upgrade_agent_system.py` si aun se necesita compatibilidad explicita en esta ronda.

## CONTRACT_GAP / STOP
- Si fijar un owner unico obliga a tocar `rollback.py`, `detect_version.py`, `doctor_agent_system.py` o `ProjectPathsResolver` de forma no prevista y sustantiva.
- Si la compatibilidad publica de `scripts/upgrade.py` no puede preservarse sin una migracion documental mucho mas amplia que README + tests declarados.
- Si la barrera fail-sin-fix solo puede demostrarse reescribiendo de forma amplia la estrategia de testing del upgrade.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013t.md` y PARA.

## DoD (binario, comandos exactos)
- [x] `python -m pytest tests/unit/test_upgrade.py::TestUpgradeMockTargetBarrier::test_patch_target_is_the_module_the_sut_imports -q` pasa y deja verificado un owner unico coherente con el modulo realmente ejercitado.
- [x] `python -m pytest tests/unit/test_upgrade.py::TestUpgradeMockTargetBarrier::test_backup_propagates_real_copytree_failure tests/unit/test_upgrade.py::TestUpgradeMockTargetBarrier::test_backup_invokes_real_copies_count -q` pasa; romper `copytree` en el owner real hace FALLAR la prueba focal sin el fix.
- [x] `python -m pytest tests/integration/test_lifecycle_integration.py -q` pasa y mantiene la superficie publica `from scripts.upgrade import UpgradeManager` operativa tras la deduplicacion.
- [x] `python -m pytest tests/unit/test_upgrade.py -q` pasa y, si se reintroduce una segunda clase editable divergente entre `upgrade.py` y `upgrade_agent_system.py`, la barrera de owner unico FALLA.
- [x] `python -m ruff check scripts/upgrade.py scripts/upgrade_agent_system.py tests/unit/test_upgrade.py tests/integration/test_lifecycle_integration.py` -> `All checks passed`.
- [x] `python scripts/check_encoding_guard.py README.md` -> exit 0.
- [x] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [x] `python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013t`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.

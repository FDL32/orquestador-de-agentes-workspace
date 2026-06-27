# Plan de Trabajo: WOT-2026-014e

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-014e
- **Estado:** COMPLETED
- **Titulo:** Unificar lectura de motor_root en runtime.motor_link
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014E-001
- **Plan-Link:** PLAN-014E-001
- **Builder clarification budget:** 0 (la premisa, el seam, la barrera primaria
  y los non-goals ya fijan el cambio minimo sin decisiones abiertas)

## Objetivo
Hacer que `scripts/run_gates_dispatch.py` y
`scripts/check_destino_publish_ready.py` dejen de reimplementar la lectura de
`motor_root` desde `motor_destination_link.json` y consuman como unica fuente de
verdad `runtime.motor_link.resolve_motor_root`, preservando localmente solo la
precedencia `arg > env > link`.

## Premise
`runtime/motor_link.py` ya es el helper canonico para resolver el `repo_motor`
desde el link del workspace y devuelve `Path(motor_root).resolve()`. Pese a
ello, hoy existen dos lectores duplicados: `scripts/run_gates_dispatch.py`
reabre el JSON en `resolve_motor_root_path()` y aplica `.resolve()`, mientras
`scripts/check_destino_publish_ready.py` reabre el mismo JSON en
`_resolve_motor_root()` pero retorna `candidate` sin `.resolve()`. Esa
divergencia silenciosa demuestra que el seam se bifurco: un cambio de topologia
obliga a recordar las copias de `run_gates_dispatch.py` y `check_destino_publish_ready.py` en vez de editar un solo helper canonico.

## Premise Re-check (cwd=repo_motor, solo lectura)
```powershell
rg -n "resolve_motor_root|resolve_motor_link|motor_destination_link|destination_root" runtime/motor_link.py scripts/run_gates_dispatch.py scripts/check_destino_publish_ready.py scripts/check_deliverables_exist.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

Condicion de arranque (VERIFICABLE):
- `runtime/motor_link.py` sigue exponiendo `resolve_motor_root(project_root) ->
  Path | None` y el retorno canonico resuelve la ruta.
- `scripts/run_gates_dispatch.py` y `scripts/check_destino_publish_ready.py`
  todavia contienen logica propia para abrir `motor_destination_link.json`.
- `scripts/check_destino_publish_ready.py` sigue teniendo al menos una rama que
  devuelve `motor_root` sin `.resolve()`.
- `scripts/check_deliverables_exist.py` ya demuestra que el import del helper
  canonico es viable en este runtime.
- `validate` del workspace sigue en `0 errors / 0 warnings`.

Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo o
tests.

## Decision Arquitectonica
El contrato del ticket congela una sola fuente de verdad para `motor_root`:
`runtime.motor_link.resolve_motor_root`.

Regla de implementacion:
- los consumidores pueden conservar un wrapper local solo para aplicar la
  precedencia `arg > env > link`;
- el wrapper local NO puede reabrir `motor_destination_link.json`;
- la semantica `Path | None` del helper canonico se conserva;
- si un consumidor exige ampliar el contrato a `destination_root` o a otra
  clave del JSON, eso queda fuera de este ticket.

Consecuencias:
- `runtime/motor_link.py` es autoridad read-only salvo que la barrera del test
  necesite exponer mejor el comportamiento ya existente.
- el fix debe quedar acotado a los dos consumidores duplicados.
- `destination_root` NO se unifica en esta ronda.

## Plan - secuencia minima fija
### Paso 1 - reconfirmar seam y consumidores
- Confirmar en codigo que solo `scripts/run_gates_dispatch.py` y
  `scripts/check_destino_publish_ready.py` reabren el JSON para `motor_root`.
- Confirmar en tests cuales son los mejores archivos para blindar:
  `tests/unit/test_motor_link.py`, `tests/unit/test_run_gates_dispatch.py` y/o
  `tests/unit/test_check_destino_publish_ready.py`.

### Paso 2 - redirigir la resolucion al helper canonico
- Reemplazar la relectura del JSON por imports desde `runtime.motor_link`.
- Conservar localmente solo la precedencia `arg > env > link`.
- No introducir un segundo helper ad-hoc ni otro parser del mismo JSON.

### Paso 3 - barrera mutation-verified
- Anadir o ajustar tests dentro de los archivos unitarios existentes para cubrir
  simultaneamente:
  - `resolve_motor_root()` normaliza un `motor_root` sin resolver.
  - `check_destino_publish_ready` consume el helper canonico y no devuelve una
    ruta cruda sin `.resolve()`.
  - `run_gates_dispatch` deja de contener una relectura divergente del JSON.
- Verificar explicitamente el fail-sin-fix: reinyectar una copia local que
  retorne el path sin normalizar debe hacer FALLAR la barrera.

### Paso 4 - gates focales y cierre
- Ejecutar la bateria focal del ticket.
- Registrar evidencia literal en `execution_log.md`.
- Preparar el commit productivo del `repo_motor` con `WOT-2026-014e` en el
  mensaje.

## Files Likely Touched (relativos a repo_motor)
- `scripts/run_gates_dispatch.py`
- `scripts/check_destino_publish_ready.py`
- `tests/unit/test_motor_link.py`
- `tests/unit/test_run_gates_dispatch.py`
- `tests/unit/test_check_destino_publish_ready.py`

Aclaraciones (no parte de las rutas):
- `runtime/motor_link.py`: autoridad read-only para este ticket; solo se toca si
  aparece una necesidad estrictamente derivada de la barrera del test.
- el Builder puede modificar dos o tres de los tests unitarios ya listados, pero`r`n  NO crear una suite paralela nueva para el mismo seam.

## Read/inspect only
- `runtime/motor_link.py`
- `scripts/check_deliverables_exist.py`
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md`
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\AUDIT_WOT-2026-014e.md`

## Forbidden Surfaces
- `runtime/motor_link.py` fuera del contrato actual del helper: prohibido
  ampliar la API a `resolve_destination_root` o cambiar el tipo de retorno para
  adaptarlo a un consumidor concreto.
- consumidores de `destination_root`: `scripts/encoding_post_write_hook.py`,`r`n  `scripts/destination_context.py` y `scripts/install_agent_system.py` quedan`r`n  read-only; este ticket no abre ningun lector adicional de claves distintas del`r`n  link.
- gates y consumers ya alineados con el helper canonico:
  `scripts/check_deliverables_exist.py`, `scripts/delivery_hygiene_check.py`,
  `scripts/prepush_check.py`, `scripts/closeout_steps/**`, `scripts/session_closeout.py`
  quedan fuera de scope salvo lectura.
- launcher, review bridge, bus y runtime del `repo_destino`:
  `scripts/launch_agent_terminals.ps1`, `bus/**`, `repo_destino/.agent/**`
  quedan prohibidos en esta ronda.
- nuevas dependencias, parser alternativo de `motor_destination_link.json`,
  cambios sobre `destination_root` o sobre la politica de topologia del sistema:
  prohibidos.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```powershell
python -m pytest tests/unit/test_motor_link.py tests/unit/test_run_gates_dispatch.py tests/unit/test_check_destino_publish_ready.py -q
python -m ruff check scripts/run_gates_dispatch.py scripts/check_destino_publish_ready.py tests/unit/test_motor_link.py tests/unit/test_run_gates_dispatch.py tests/unit/test_check_destino_publish_ready.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO tocar `destination_root` ni unificar aqui consumidores que leen otras
  claves del link.
- NO editar `scripts/encoding_post_write_hook.py` ni
  `scripts/check_motor_destination_integration.py`.
- NO crear un helper duplicado intermedio como parche.
- NO convertir el contrato de `resolve_motor_root` de `Path | None` a
  `always-Path`; los consumidores deben adaptarse al helper, no al reves.

## CONTRACT_GAP / STOP
- Si el fix exige cambiar la semantica del helper canonico mas alla de
  `motor_root`.
- Si aparece un consumidor adicional de `motor_root` no inventariado que obliga
  a ampliar `Files Likely Touched`.
- Si la barrera solo puede expresarse creando una suite paralela nueva en vez`r`n  de modificar los tests unitarios existentes ya listados en FLT.
- Si un consumidor no puede aceptar `Path | None` sin ampliar el ticket hacia un
  refactor transversal de topologia.
-> emitir `CG-WOT-2026-014e.md` y PARAR.

## DoD (binario, comandos exactos)
- [ ] `python -m pytest tests/unit/test_motor_link.py tests/unit/test_run_gates_dispatch.py tests/unit/test_check_destino_publish_ready.py -q` pasa.
- [ ] `scripts/run_gates_dispatch.py` y `scripts/check_destino_publish_ready.py`
  importan `resolve_motor_root` de `runtime.motor_link` y ya no reabren
  `motor_destination_link.json` para leer `motor_root`.
- [ ] Existe una barrera automatica donde una ruta `motor_root` no resuelta se
  normaliza via el helper canonico y, al reintroducir una copia local que
  devuelve el path crudo, esa barrera FALLA.
- [ ] Ninguna ruta de codigo tocada retorna `motor_root` sin `.resolve()`.
- [ ] `python -m ruff check scripts/run_gates_dispatch.py scripts/check_destino_publish_ready.py tests/unit/test_motor_link.py tests/unit/test_run_gates_dispatch.py tests/unit/test_check_destino_publish_ready.py`
  -> `All checks passed`.
- [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json` con
  `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
  -> `0 errors / 0 warnings`.
- [ ] La evidencia de cierre cita el SHA del commit del `repo_motor` que
  contiene el fix.

## Handoff
Commit productivo en `repo_motor` (mensaje con `WOT-2026-014e`), suite
canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. No hacer push
hasta OK humano.
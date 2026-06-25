# Plan de Trabajo: WOT-2026-013u

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013u
- **Estado:** COMPLETED
- **Titulo:** Arreglar parser CLI de closeout/review para que respete --ticket y alinee el help
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Alta
- **Depende de:** -
- **Objective-Link:** OBJ-013U-001
- **Plan-Link:** PLAN-013U-001
- **Builder clarification budget:** 0 (el ticket fija parser, help, superficies, test files y politica de backward-compat; no deja decisiones abiertas de producto)

## Objetivo
Corregir el parser de `agent_controller.py` para que las acciones que aceptan ticket (`--manager-approve`, `--request-changes`, `--reopen-terminal-ticket`) respeten `--ticket <id>` de forma consistente, sin romper la compatibilidad posicional ya usada en cierres previos, y con ayuda/mensajes alineados al comportamiento real.

## Premise
Existe un drift verificable entre el contrato CLI documentado y el parser real del controller: el help y `Control flags` anuncian `--ticket <ticket>` como forma soportada para acciones de closeout/review, pero la rama de parseo comun en `.agent/agent_controller.py` contiene una condicion invertida y por ello no asigna `ticket_id` cuando `--ticket` se usa correctamente. Como efecto, `--manager-approve --ticket <id>` falla con `No ticket_id provided`, mientras la forma posicional `--manager-approve <id>` si entra al flujo. Ademas, `--reopen-terminal-ticket` aparece en el help como flag sin `<ticket>` aunque su parser intenta consumir uno.

## Premise Re-check (cwd=repo_motor, solo lectura)
```
python .agent/agent_controller.py -h
rg -n -e "--manager-approve <ticket>|--request-changes <ticket>|--reopen-terminal-ticket|--ticket <ticket>|Parse --ticket|idx \\+ 1 >= len\\(sys\\.argv\\)|elif \\\"--manager-approve\\\"|elif \\\"--request-changes\\\"|elif \\\"--reopen-terminal-ticket\\\"" .agent/agent_controller.py
rg -n "test_agent_controller_help_lists_critical_flags|_handle_manager_approve|_handle_request_changes|_handle_reopen_terminal_ticket" tests/test_agent_controller.py tests/unit/test_manager_approve.py tests/unit/test_request_changes_requeue.py
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- el help expone `--manager-approve <ticket>` y `--request-changes <ticket>`, mientras `--reopen-terminal-ticket` aparece sin `<ticket>`;
- la rama `if "--ticket" in sys.argv:` usa una condicion invertida (`idx + 1 >= len(sys.argv)`) y por eso no asigna `ticket_id` cuando `--ticket` tiene valor valido;
- existen superficies de test ya versionadas para cubrir `manager-approve`, `request-changes` y `reopen-terminal-ticket` sin crear una familia paralela de tests.
Si esta premisa read-only no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
La solucion debe ser de parser/contrato CLI, no un workaround ad hoc para `manager-approve`. El controller ya expone `--ticket` como control flag comun; el fix correcto es hacer que esa ruta funcione de verdad para todas las acciones que la aceptan, conservar la via posicional existente por backward-compat y alinear el `-h`/mensajes/tests al contrato unificado.

## Plan - secuencia minima FIJA
### Paso 1 - parser comun de ticket
- Corregir el parseo de `--ticket` en `.agent/agent_controller.py` para que capture el valor cuando existe y falle con diagnostico claro cuando falte.
- Mantener compatibilidad con las formas posicionales actuales de `--manager-approve <ticket>`, `--request-changes <ticket>` y `--reopen-terminal-ticket <ticket>`; este ticket NO depreca la via posicional.

### Paso 2 - ayuda y mensajes coherentes
- Alinear `-h` y los mensajes `No ticket_id provided` al contrato real del parser.
- `--reopen-terminal-ticket` no puede seguir anunciandose como flag sin ticket si exige uno para actuar.
- El help final debe reflejar ambas formas soportadas: posicional y `--ticket`.

### Paso 3 - barreras de regresion
- Anadir/ajustar tests que cubran ambas formas validas (posicional y `--ticket`) y el caso negativo sin ticket.
- La barrera debe probar el parser/distribucion real del controller, no solo invocar handlers internos con strings hardcodeados.
- La barrera de `reopen-terminal-ticket` se fija en `tests/test_agent_controller.py`; no queda a eleccion del Builder moverla a otro archivo.

## Files Likely Touched (relativos a repo_motor)
- `.agent/agent_controller.py`
- `tests/test_agent_controller.py`
- `tests/unit/test_manager_approve.py`
- `tests/unit/test_request_changes_requeue.py`

Aclaraciones (no parte de las rutas):
- `.agent/agent_controller.py`: parser de `--ticket`, help y mensajes de error de acciones con ticket.
- `tests/test_agent_controller.py`: pruebas de ayuda, dispatch CLI real y barrera de `reopen-terminal-ticket`.
- `tests/unit/test_manager_approve.py`: cobertura de `--manager-approve` via parser real o helper compartido.
- `tests/unit/test_request_changes_requeue.py`: paridad para `--request-changes`.

## Forbidden Surfaces
- `repo_motor/bus/**` y `repo_motor/runtime/**`: fuera de scope; no cambiar semantica del bus, estados ni cascadas de closeout.
- `repo_motor/scripts/run_pytest_safe.py`: gate canonico read-only; este ticket no toca politica de cierre.
- migracion completa a `argparse` o rediseno amplio del `main()` del controller: prohibido en esta ronda.
- `repo_motor/prompts/**` y `repo_motor/skills/**`, salvo una referencia puntual del help del controller si quedara rotundamente incoherente; por defecto no tocar.
- `repo_destino/.agent/runtime/events/events.jsonl` y demas superficies vivas del bus: nunca editar a mano.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/test_agent_controller.py -q
python -m pytest tests/unit/test_manager_approve.py -q
python -m pytest tests/unit/test_request_changes_requeue.py -q
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO cambiar la semantica de closeout del bus ni las cascadas de eventos.
- NO redisenar `manager-approve`, `request-changes` o `reopen-terminal-ticket` mas alla del contrato de parseo/ayuda.
- NO mezclar este ticket con `013t` ni con mejoras de `upgrade`.
- NO tocar prompts ajenos salvo que el propio help del controller exija alinear una referencia directa.

## CONTRACT_GAP / STOP
- Si alguna accion consume deliberadamente un contrato CLI distinto y documentado que haga imposible unificar `--ticket` sin romper backward-compat.
- Si corregir el parser obliga a reestructurar de forma amplia el `main()` del controller o a migrar toda la CLI a argparse en esta ronda.
- Si aparecen mas consumidores de `--ticket` con contratos incompatibles fuera de `manager-approve` / `request-changes` / `reopen-terminal-ticket`.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013u.md` y PARA.

## DoD (binario, comandos exactos)
- [x] `python -m pytest tests/test_agent_controller.py::test_agent_controller_help_lists_critical_flags -q` pasa y el help resultante refleja la forma posicional y la forma `--ticket` para las acciones con ticket, incluyendo `--reopen-terminal-ticket`.
- [x] `python -m pytest tests/unit/test_manager_approve.py::TestManagerApprove::test_complete_cascade_emitted tests/unit/test_manager_approve.py::TestManagerApproveCLIContract::test_manager_approve_accepts_ticket_flag -q` pasa; con la condicion invertida del parser reintroducida, `tests/unit/test_manager_approve.py::TestManagerApproveCLIContract::test_manager_approve_accepts_ticket_flag` FALLA.
- [x] `python -m pytest tests/unit/test_request_changes_requeue.py::test_request_changes_accepts_ticket_flag tests/unit/test_request_changes_requeue.py::test_request_changes_positional_ticket_still_supported -q` pasa con cobertura explicita de `--request-changes --ticket` y de la forma posicional.
- [x] `python -m pytest tests/test_agent_controller.py::test_reopen_terminal_ticket_accepts_ticket_flag tests/test_agent_controller.py::test_ticket_parser_reads_control_flag_before_positional_fallback -q` pasa; con la condicion invertida del parser reintroducida, `tests/test_agent_controller.py::test_ticket_parser_reads_control_flag_before_positional_fallback` FALLA.
- [x] La forma posicional existente (`--manager-approve WOT-TEST-001`, `--request-changes WOT-TEST-001`, `--reopen-terminal-ticket WOT-TEST-001`) sigue funcionando; no se rompe ni se depreca en silencio.
- [x] `python -m ruff check .agent/agent_controller.py tests/test_agent_controller.py tests/unit/test_manager_approve.py tests/unit/test_request_changes_requeue.py` -> `All checks passed`.
- [x] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [x] `python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013u`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.


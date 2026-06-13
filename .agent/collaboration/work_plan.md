# Work Plan: WOT-AUDIT-A2a - Resolucion de recursos por precedencia (host-extends/motor-provides)

## Metadata
- **ID:** WOT-AUDIT-A2a
- **Estado:** READY_TO_START
- **deliverable_type:** documentation
- **Titulo:** Documentar y mapear la resolucion de recursos del destino por precedencia
- **Asignado a:** Builder
- **Repo de autoridad:** repo_destino
- **Severidad:** Media | **Riesgo:** Bajo (solo documentacion; cero file-moves)
- **Origen:** WOT-AUDIT-A2 (subfase A2a) en `_legacy/general_audit_20260613/03_tickets.md`

## Objetivo
Producir un documento canonico del `repo_destino` que (1) fije la regla de
precedencia de recursos host-extends/motor-provides y (2) mapee cada comando
del destino que hoy apunta a una COPIA LOCAL a su equivalente invocable del
motor externo. A2a NO mueve ni borra archivos: solo documenta y mapea para
habilitar A2b/A2c/A2d posteriores.

## Decision Arquitectonica
El destino no debe contener copias versionadas de prompts/skills/scripts del
motor: referencia el motor externo y usa sus capacidades canonicas sin
modificarlas. Orden de precedencia para resolver un recurso (skill, prompt,
script, tool):

1. **Host/local del destino** -- `repo_destino/.agent/{skills,prompts,tools}/`.
   Extensiones y overrides propios. Maxima prioridad.
2. **Motor (read-only)** -- `repo_motor/{skills,prompts,scripts}/`, invocado con
   `AGENT_PROJECT_ROOT=<repo_destino>` (y `cwd=<repo_destino>` donde el flujo lo
   exija; ver tabla). Fuente canonica; nunca se edita desde el destino.
3. **Copias legacy** -- `repo_destino/{scripts,skills,agent_system}/`. Estado
   transitorio de dogfooding; objetivo final = desaparecer (A2d). **Nunca** es
   resolucion valida una vez exista el equivalente del motor.

Override de una skill del motor = crear una propia en `.agent/skills/` con otro
nombre u override documentado; jamas editar la del motor.

## Mapeo de comandos del destino -> equivalente del motor (evidencia A2a)
Fuente: `.claude/settings.local.json`. Verificado por `git ls-files` (destino) y
`test -f` (motor) el 2026-06-13 a HEAD destino `13ee7e1` / motor `704939f`.

> Correccion de review (Manager, verificada): estos 3 scripts del motor NO
> exponen `--project-root`. La propagacion de root real es la env var
> `AGENT_PROJECT_ROOT` (via `runtime/project_root.py:resolve_project_root`), y
> algunos flujos dependen ademas de `cwd=<repo_destino>` (host-first discovery,
> guard-paths). La forma invocable real y evidenciada vive en el entregable
> `.agent/docs/resource_precedence.md`, que es la autoridad para A2b.

| Comando actual (settings.local.json) | Copia local en destino | Existe en motor | Equivalente propuesto (A2b) |
|---|---|---|---|
| `python scripts/run_pytest_safe.py` | TRACKED | si | `AGENT_PROJECT_ROOT=<repo_destino>` + `cwd=<repo_destino>` + `python <repo_motor>/scripts/run_pytest_safe.py` (sin `--project-root`) |
| `python scripts/discover_skills.py --json` | TRACKED | si | `AGENT_PROJECT_ROOT=<repo_destino>` + `cwd=<repo_destino>` + `python <repo_motor>/scripts/discover_skills.py --json` (host-first depende de `cwd`; sin `--project-root`) |
| `python scripts/local_audit.py --quick` | AUSENTE (no es copia) | si | `AGENT_PROJECT_ROOT=<repo_destino>` + `python <repo_motor>/scripts/local_audit.py --json --quick` (sin `--project-root`; no hay copia que archivar) |
| `python scripts/test_refactor_kit_performance.py` | TRACKED | **SI** (motor `tests/test_refactor_kit_performance.py`, lo corre la suite) | CORRECCION 2026-06-13: la afirmacion original "sin equivalente" fue gap de verificacion (solo se miro `scripts/`). La copia del destino es el mismo test (diff solo en BOM, una linea `# ruff: noqa: PERF203` y el newline final); no hay gap de capacidad. A2b retira la copia stale + entrada de allowlist; la suite del motor preserva cobertura. NO es STOP. |
| `agent_system/refactor-kit/install_refactor_kit.py` | AUSENTE (ruta hyphen inexistente) | motor tiene `agent_system/refactor_kit/` (underscore) | entrada allowlist **stale/muerta** -> ver STOP/escalado #2 |

## Superficies (contrato documentation por tipo)
- **Builder (entregable, debe crear):**
  - `repo_destino/.agent/docs/resource_precedence.md` -- nuevo. Contiene la
    Decision Arquitectonica (3 niveles) y la tabla de mapeo de arriba con su
    evidencia (fecha, HEADs, metodo de verificacion).
- **Read/inspect only (contexto, NO cuentan como entregable):**
  - `.claude/settings.local.json` (fuente de comandos)
  - `_legacy/general_audit_20260613/03_tickets.md` (ticket padre A2)
  - `MANIFEST.workspace`, `AGENTS.md` (contrato de portabilidad, solo lectura)
- **Manager-only (gate, no lo ejecuta el Builder):**
  - revision de coherencia del doc contra el contrato host-extends/motor-provides.

## Non-goals
- No `git mv` ni borrado de ninguna copia legacy (eso es A2d).
- No tocar `.claude/settings.local.json` (eso es A2b).
- No editar prompts/skills/scripts del motor.
- No reapuntar ni limpiar `test_refactor_kit_performance.py` ni su entrada de
  allowlist (eso es A2b); A2a solo documenta el hallazgo (ya corregido: no es
  un gap de capacidad del motor).

## Criterios binarios de cierre
- [ ] Existe `repo_destino/.agent/docs/resource_precedence.md` con: regla de
      precedencia de 3 niveles + tabla de mapeo completa (5 comandos).
- [ ] El doc declara explicitamente los hallazgos para A2b: la correccion del
      falso STOP del perf-test (el motor SI tiene el test en `tests/`) y la
      entrada stale de allowlist (`refactor-kit` hyphen). Ninguno bloquea A2b.
- [ ] El doc registra fecha y HEADs de verificacion (destino `13ee7e1`, motor `704939f`).
- [ ] `execution_log.md` cierra con una linea que combina artefacto + gate final,
      p.ej.: `Doc .agent/docs/resource_precedence.md creado. Validate: exit 0, 0 errors, 0 warnings.`
- [ ] `agent_controller.py --validate --project-root <destino>` exit 0 (sin
      regresion por el work_plan/log nuevos). Exit real (last-run/json), no pipe.

## STOP / escalado
1. ~~**`test_refactor_kit_performance.py` sin equivalente en el motor.**~~
   RESUELTO / NO ES STOP (corregido 2026-06-13): el motor SI tiene el test en
   `tests/test_refactor_kit_performance.py`, ejecutado por la suite
   (`run_pytest_safe.py`). La verificacion original solo miro `scripts/`. A2b
   retira la copia stale del destino y su entrada de allowlist; no requiere
   decision de capacidad del motor.
2. **Entrada allowlist stale `agent_system/refactor-kit/install_refactor_kit.py`.**
   La ruta con hyphen no existe en el destino; el motor lo tiene bajo
   `agent_system/refactor_kit/` (underscore). Es una entrada muerta de allowlist.
   **Documentar; su limpieza pertenece a A2b, no a A2a.**
3. Si al redactar el doc aparece cualquier comando adicional que apunte a copia
   local sin equivalente claro del motor: anadir fila + STOP, no improvisar fix.

## Gates (deliverable_type: documentation)
- `agent_controller.py --validate --project-root <destino>` exit 0.
- Deliverable existence check: `.agent/docs/resource_precedence.md` existe.
- NO se exige pytest/ruff/pip-audit (no toca codigo).

## Riesgos
- Bajo. Solo crea un doc nuevo + actualiza superficies de colaboracion.
- A2b no tiene bloqueos de capacidad: el supuesto STOP del perf-test era un gap
  de verificacion (el motor SI tiene el test en `tests/`). Los dos hallazgos
  para A2b son limpieza (retirar copia stale + arreglar entrada de allowlist).

## Entregables
- `repo_destino/.agent/docs/resource_precedence.md` (doc canonico de precedencia + mapeo).

# work_plan.md -- WOT-2026-010v

## Metadata

- **ID:** WOT-2026-010v
- **Contract ID:** T-010V-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Endurecer `scripts/check_encoding_guard.py` y su fuente compartida
`scripts/encoding_guard.py` para detectar control chars ASCII `<32`
no-whitespace en archivos de texto (`\x00`, `\x07`, `\x0b`, `\x0c`, etc.),
preservando como validos `\t`, `\n`, `\r` y CRLF, sin ampliar el alcance a
binarios ni rehacer el hook de Bash/heredoc.

## Non-goals

- No interceptar Bash/heredoc en v1.
- No tocar bus, runtime o `validate`.
- No ampliar el guard a binarios o ficheros fuera de `TEXT_EXTENSIONS`.
- No introducir allowlists nuevas.
- No reescribir artefactos historicos ya cerrados.
- No tocar dependencias.

## Premisas verificadas antes de Builder

- `WOT-2026-010e` esta COMPLETED y ya comparte deteccion entre
  `check_encoding_guard.py` y `encoding_post_write_hook.py` via
  `scripts.encoding_guard`.
- `WOT-2026-008j` cerro con un blocker real de `execution_log.md` corrupto por
  control chars; el fix fue manual porque el guard no los detectaba.
- El detector actual cubre BOM, mojibake y `?` intra-palabra, pero no control
  chars ASCII `<32` no-whitespace.
- `scripts/encoding_post_write_hook.py` reutiliza `file_issues()` y por tanto
  hereda cualquier mejora hecha en `scripts/encoding_guard.py`.
- Existen tests vivos en `tests/test_encoding_integrity.py` y
  `tests/unit/test_encoding_post_write_hook.py` que pueden blindar la regresion
  sin crear una suite paralela.

## Decision Arquitectonica

La correccion debe vivir en `scripts/encoding_guard.py` como fuente de verdad
compartida. `scripts/check_encoding_guard.py` y el hook post-write deben
consumir ese comportamiento, no duplicarlo. El ticket no cambia el gap v1 de
Bash/heredoc ni la frontera de ficheros texto; solo blinda una clase de
corrupcion ya observada en artefactos textuales.

## Files Likely Touched

### repo_motor

- `scripts/encoding_guard.py`
- `scripts/check_encoding_guard.py`
- `scripts/encoding_post_write_hook.py`
- `tests/test_encoding_integrity.py`
- `tests/unit/test_encoding_post_write_hook.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `AGENTS.md`
- `backlog.md`
- `ticket_contracts.md`
- historicos de `008f` y `008j` en `execution_log.md`
- `bus/runtime/events`

## Forbidden Surfaces

- Interceptar Bash/heredoc o cambiar el gap v1 de shell.
- Escanear binarios o ampliar `TEXT_EXTENSIONS` sin necesidad contractual.
- Introducir allowlists nuevas.
- Tocar `validate`, bus, runtime o eventos.
- Tocar dependencias.

## Criterios binarios

- `scripts/check_encoding_guard.py <archivo>` falla cerrado ante control chars
  ASCII `<32` no-whitespace en archivos de texto.
- `\t`, `\n`, `\r` y CRLF legitimos no disparan falso positivo.
- La deteccion vive en `scripts/encoding_guard.py` y el hook post-write la
  hereda sin un detector paralelo.
- Existe al menos un test de regresion en `tests/test_encoding_integrity.py`
  para el CLI guard por ruta explicita.
- Existe al menos un test de regresion en
  `tests/unit/test_encoding_post_write_hook.py` que demuestra fallo del hook
  ante control chars en archivo textual.
- Los tests previos de BOM/mojibake/question-mark siguen verdes.
- `python -m pytest tests/test_encoding_integrity.py tests/unit/test_encoding_post_write_hook.py -v` pasa.
- `ruff check`, `uv run ruff format --check`, `python scripts/run_pytest_safe.py --level all`
  y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-010v.md` y parar si la correccion exige interceptar
Bash/heredoc, cambiar la semantica de allowlist, escanear binarios o introducir
una segunda fuente de verdad distinta de `scripts.encoding_guard`.

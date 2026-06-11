# AUDIT WT-2026-245c - Centralizar patron canonico de ticket ID

## Estado
APPROVED

## Objetivo de auditoria
Verificar que la centralizacion del patron de ticket ID reduce duplicacion real sin introducir un mecanismo cruzado incorrecto entre Python y PowerShell.

## TP Check
- TP-01: verificado - la secuencia es unica: localizar duplicacion, centralizar Python, consolidar PowerShell, validar.
- TP-02: verificado - los observables son concretos: nuevo modulo canonico, diff de consumidores, tests y exit codes.
- TP-03: verificado - `Files Likely Touched` enumera las superficies esperadas de Python, PowerShell y tests.
- TP-04: verificado - el patron objetivo es explicito: `(?:WP|WT|[A-Z]{3})-\d{4}-[A-Za-z0-9]+`.
- TP-05: verificado - PLAN y AUDIT describen la misma separacion entre runtimes.
- TP-06: verificado - el TP Check no sustituye gates funcionales.
- TP-07: verificado - se prohibe crear modulos importables dentro de `prompts/`.

## Fases de revision

### Fase 1 - Duplicacion real
- Verificar evidencia de regex duplicadas en `bus/review_bridge.py`, `bus/supervisor.py`, `launch_agent_terminals.ps1` y, si aplica, `agent_controller.py`.

### Fase 2 - Implementacion
- Verificar que `bus/ticket_id.py` existe y contiene la fuente canonica Python.
- Verificar que PowerShell usa `$script:TicketIdPattern` o helper local equivalente dentro del mismo `.ps1`.
- Verificar que el diff no intenta compartir el mismo modulo entre runtimes.
- Verificar que `scripts/validate_ticket_prose.py` entra deliberadamente para soportar `AUDIT_[A-Z][A-Z][A-Z]-*.md`.

### Fase 3 - Regresion
- Verificar que `tests/unit/test_ticket_prefix_compat.py` sigue cubriendo `WP-*`, `WT-*` y `CTL-*`.
- Verificar que `tests/unit/test_launcher_powershell_syntax.py` cubre la lectura del patron equivalente en PowerShell y que el patron matchea `CTL-2026-001a`.
- Verificar que no aparece `prompts/ticket_parser.py` ni equivalente mal ubicado.

### Fase 4 - Quality gates
- Verificar exit code 0 de `ruff`, `pytest tests/unit/test_ticket_prefix_compat.py tests/unit/test_launcher_powershell_syntax.py -q` y `validate --json --project-root ...`.

## Blockers
- No existe `bus/ticket_id.py` como fuente canonica Python.
- El diff crea un modulo importable en `prompts/`.
- PowerShell intenta depender directamente de un modulo Python.
- `validate_ticket_prose.py` queda fuera del contrato pese a que soporta `AUDIT_<XXX>-*.md`.
- Cualquiera de los quality gates falla.

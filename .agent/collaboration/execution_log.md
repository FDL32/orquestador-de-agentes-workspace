# execution_log.md -- WOT-2026-011c

## Metadata

- **Ticket:** WOT-2026-011c
**Estado:** COMPLETED
- **deliverable_type:** research
- **delivery_authority:** repo_destino

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-011c`.
- Motivo: `WOT-2026-012a` quedo en `CONTRACT_BLOCKED` y su desbloqueo recomendado
  pasa por identificar la fuente del BOM/control-char antes de tocar fix alguno.
- Hechos verificados antes del handoff:
  - `T-011C-001` esta congelado en `.agent/planning/ticket_contracts.md`.
  - `WOT-2026-012a` queda preservado en backlog como `blocked` y su evidencia de
    bloqueo se conserva en `CG-WOT-2026-012a.md` + snapshot de `execution_log`.
  - `validate --json --project-root <repo_destino>` esta en 0 errors / 0 warnings
    al arrancar `011c`.
- Pendiente de Builder:
  1. medir bytes/BOM en surfaces vivas vs HEAD;
  2. trazar escritores sin modificarlos;
  3. emitir `bom_source_audit_WOT-2026-011c.md`;
  4. validar reporte limpio y parar sin fix.

## Manager Bootstrap

- Packet materializado para `WOT-2026-011c`.
- `work_plan.md`, `STRATEGY_WOT-2026-011c.md` y `AUDIT_WOT-2026-011c.md`
  quedan alineados al mismo contrato frozen.
- El runtime deja `012a` preservado en `CONTRACT_BLOCKED` dentro del backlog y el
  bus historico, pero activa `011c` como ticket de trabajo corriente.
- `execution_log.md` queda reinicializado en `IN_PROGRESS` para arranque directo
  del Builder.

## BUILDER - WOT-2026-011c - BOM/control-char SOURCE audit (spike research)

### Fase 0 - Baseline (VERIFICADO con bytes)
- BOM working-tree pero NO en HEAD: work_plan, TURN, backlog, execution_log, ticket_contracts.
- Sin BOM (working ni HEAD): STATE, notifications, review_queue (proyectadas por controller Python).
- Control chars 0x07/0x0B/0x08 en HEAD:backlog offsets 176852/177183/177215, region historica.
  Comandos: git show HEAD:<f> | byte-check; open(f,'rb').read()[:3].

### Fase 1 - Trazado de escritores (read-only, NINGUNO modificado)
- agent_controller.py:write_file (L1052) escribe encoding="utf-8" SIN BOM -> no es fuente.
- build_llms/discover_skills/local_audit usan utf-8-sig solo para LEER -> no son fuente.
- launch_agent_terminals.ps1 L1803-1804 (WT-2026-248a) documenta: "Set-Content -Encoding UTF8
  ALWAYS prepends the UTF-8 BOM"; usa Set-Content -Encoding UTF8 (L1440) + Out-File -Encoding UTF8 (L1904).
- Confirmacion empirica BOM (temp file, repo intacto): powershell Set-Content -Encoding UTF8 -> EF BB BF.
- Confirmacion empirica control chars: printf 'prompts \audit_* \validate \bui-self' produce
  EXACTAMENTE \x07udit \x0balidat \x08ui-self (mismos bytes, mismo contexto). Reproducido 1:1.

### Fase 2 - Hallazgo (DOS fuentes distintas, ambas VERIFICADAS)
- Fuente BOM: PowerShell 5.1 Set-Content/Out-File -Encoding UTF8 (default BOM). VERIFICADO.
- Fuente control chars: backslash-escape interpretation (\a \v \b) por printf/shell sobre texto
  con \audit/\validate/\bui Windows-style. NO es encoding/BOM. VERIFICADO.
- Reporte durable: .agent/runtime/audit/bom_source_audit_WOT-2026-011c.md (104 lineas, limpio).
- Follow-up recomendado (NO aplicado): `WOT-2026-011j` para fijar writer PowerShell BOM-safe
  en superficies vivas y sanear los 3 control chars historicos de `HEAD:backlog`; tras ese
  fix, `012a` puede regenerar snapshot/historico limpio y reintentar su handoff canonico.
- INFERENCIA RAZONABLE acotada: no se instrumento el writer PS en vivo (contrato read-only); la
  atribucion "via PowerShell" se apoya en discriminante controller-vs-resto + mecanismo empirico.
- STOP respetado: identificado y parado; NINGUN fix aplicado; NINGUN writer modificado.

### Nota viva (evidencia del propio hallazgo)
- execution_log.md reaparecio con BOM tras el bootstrap del runtime a 011c, pese a que
  010v/012a lo habian limpiado. Es exactamente Fuente 1 del reporte: un write mediado por
  PowerShell -Encoding UTF8 re-inyecta BOM en superficies vivas. Re-limpiado (superficie propia, FLT).


Manager approved canonical closeout for WOT-2026-011c
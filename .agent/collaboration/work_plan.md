# Plan de Trabajo: WOT-2026-013s

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo. Redactado contra
> `prompts/audit_cf_ticket_contract.md` y `prompts/orchestrator_launch_builder.md`.

> **Procedencia (importante):** este ticket nace porque `WOT-2026-013o` cerro
> COMPLETED en el bus apuntando al `observations.jsonl` del **repo_destino**
> (que estaba limpio), dejando SIN sanear el del **repo_motor** (168 errores
> --strict, VERIFICADO 2026-06-25). 013o es terminal y NO se reabre; el
> saneamiento real del MOTOR se trata como ticket NUEVO `WOT-2026-013s`.

## Metadata
- **ID:** WOT-2026-013s
- **Estado:** APPROVED
- **Titulo:** Saneamiento estricto de observations.jsonl del repo_motor (sucesor de 013o, target corregido)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Alta
- **Depende de:** WOT-2026-013n (cerrado)
- **Reemplaza/corrige a:** WOT-2026-013o (COMPLETED contra target equivocado: repo_destino en vez de repo_motor)
- **Objective-Link:** desbloquear la promocion de memoria portable del motor
  (FP-012 y futuros) dejando `observations.jsonl` en `--strict` verde.
- **Plan-Link:** backlog del workspace (familia 013).

## Objetivo
Dejar `repo_motor/.agent/runtime/memory/observations.jsonl` en
`validate_observations.py --strict` EXIT 0, reparando el schema drift de forma
determinista y auditable, sin reinterpretar contenido factual (`signal`).

## Orden de ejecucion
`WOT-2026-013s` se ejecuta ANTES que `WOT-2026-013r`. El ticket
`WOT-2026-013r` NO se arranca hasta que `013s` cierre verde, porque `013s`
desbloquea el schema de memoria portable que `013r` necesita para promover
aprendizajes como FP-012 sin ampliar deuda.

## Premise Re-check (autoridad reproducible; NO conteos fijos)
**Regla contractual:** la autoridad del estado es la salida de
`validate_observations.py --strict`, no un numero del plan. Captura el conteo
real al arrancar y trabaja contra ese output. Los valores de referencia abajo
son orientativos (medidos 2026-06-25), NO criterio de cierre.

Desde cwd=`repo_motor`, antes de tocar codigo:
```
git rev-parse --short HEAD
python scripts/validate_observations.py --strict --file .agent/runtime/memory/observations.jsonl ; echo "EXIT $?"
python -c "import sys; sys.path.insert(0,'scripts'); import migrate_observations as m, json; from pathlib import Path; found={json.loads(l)['domain'] for l in Path('.agent/runtime/memory/observations.jsonl').read_text(encoding='utf-8').splitlines() if l.strip() and json.loads(l).get('domain') and json.loads(l)['domain'] not in m.VALID_DOMAINS}; print('uncovered_by_MAP:', sorted(found - set(m.DOMAIN_MIGRATION_MAP)))"
```
Estado esperado al arrancar (referencia orientativa, usa el output real):
- `validate --strict` -> EXIT 1, errores en 3 ejes (`applies_to`, `domain`,
  `source`). Referencia: ~168 errores; usa el conteo real, no este numero.
- `uncovered_by_MAP` -> lista NO vacia (referencia: architecture, audit, engine,
  engine-runtime, meta, review-bridge, security, session-closeout,
  supervisor-behavior).

### Condiciones de arranque (corrige el CONTRACT_GAP discutible)
- Si `validate --strict` ya da **EXIT 0** -> el ticket ya fue absorbido por otro
  cambio: PARA y emite CONTRACT_GAP (`ticket_already_satisfied`).
- Si `uncovered_by_MAP == []` PERO `validate --strict` SIGUE FALLANDO -> el
  trabajo se redujo al Eje A (datos): CONTINUA solo con Eje A; re-evalua si hace
  falta ampliar el enum. NO es gap.
- Si `validate --strict` falla Y `uncovered_by_MAP` no es vacio -> ticket
  completo (Eje A + Eje B), caso esperado.

## Decision Arquitectonica
La decision central es como tratar los dominios no-enum del MOTOR: **mapear a un
dominio canonico existente** (preferido) vs **ampliar el enum canonico**.
- Preferir MAPEAR (poblar `DOMAIN_MIGRATION_MAP`) cuando el dominio no-enum es un
  sub-caso semantico de uno canonico (precedente 013o: `collaboration` ->
  `delivery-hygiene`, `test-performance` -> `testing`). Mas barato, no toca el
  contrato de schema ni `ap-schema.md`, no propaga a destinos via sync.
- Ampliar el ENUM (en `validate_observations.py` + `ap-schema.md`) SOLO si un
  dominio no tiene equivalente canonico honesto y representa una categoria
  estable que merece existir en el contrato portable. Tiene blast radius mayor
  (toca el schema que se propaga a cada destino instalado via sync) -> requiere
  justificacion fuerte y barrera/doc.
- Invariante: ninguna decision "a ojo"; cada mapeo o ampliacion lleva comentario
  justificante. Si ningun camino es honesto sin redisenar la taxonomia -> CONTRACT_GAP.

## Plan de Implementacion (2 ejes separados)
### Eje A - reparacion determinista de datos (la cubre el migrador)
`applies_to` (arrays/no-enum), `source` ausente, `timestamp`/`ts` -> reglas
cerradas WT-2026-191 del migrador. NO requiere decision.

### Eje B - decision de taxonomia de dominios (el trabajo real, requiere criterio)
Poblar `DOMAIN_MIGRATION_MAP` en `scripts/migrate_observations.py` con un mapeo
EXPLICITO y JUSTIFICADO (comentario inline) de cada dominio de
`uncovered_by_MAP` a un dominio canonico de `VALID_DOMAINS` (`builder-contract,
bus-architecture, config-schema, delivery-hygiene, integration-tests,
protocol-handlers, review-quality, security-gates, testing`), O ampliar el enum
en `validate_observations.py` + `skills/_shared/ap-schema.md` si un dominio no
tiene equivalente honesto. No mapear "a ojo".

## Invocacion canonica UNICA (sin auto-detect ambiguo)
Desde cwd=`repo_motor`:
```
# 1. Previsualizar (sin --apply = dry-run):
python scripts/migrate_observations.py --file .agent/runtime/memory/observations.jsonl
# 2. Aplicar (crea backup, idempotente, restaura+aborta si valida mal):
python scripts/migrate_observations.py --apply --file .agent/runtime/memory/observations.jsonl
# 3. Verificar:
python scripts/validate_observations.py --strict --file .agent/runtime/memory/observations.jsonl
```

## Evidencia before/after (capturar en execution_log)
```
# ANTES (en Premise Re-check): guardar el EXIT y conteo de validate --strict.
# DESPUES (post --apply): re-correr validate --strict y registrar EXIT 0.
git diff --stat .agent/runtime/memory/observations.jsonl   # diff revisable (archivo TRACKED)
```

## Files Likely Touched

Rutas relativas a `repo_motor` (delivery_authority=repo_motor). Una ruta
parseable por bullet, sin comentarios inline; las aclaraciones van debajo.

### repo_motor
- `scripts/migrate_observations.py`
- `scripts/validate_observations.py`
- `skills/_shared/ap-schema.md`
- `.agent/runtime/memory/observations.jsonl`
- `tests/unit/test_migrate_observations.py`

Aclaraciones (no parte de las rutas):
- `scripts/migrate_observations.py`: poblar DOMAIN_MIGRATION_MAP / TOPIC_OVERRIDE (Eje B) + endurecer guard keep-intact (Eje A residual).
- `scripts/validate_observations.py`: SOLO si se amplia el enum (no se amplio).
- `skills/_shared/ap-schema.md`: SOLO si se amplia el enum (no se amplio).
- `.agent/runtime/memory/observations.jsonl`: datos migrados; TRACKED -> diff revisable en handoff.
- `tests/unit/test_migrate_observations.py`: NUEVO; barreras de guard, mapeo Eje B, impact, LF y rollback.

## Non-goals
- NO tocar `repo_destino` (su observations.jsonl esta limpio; 0 entradas drift).
- NO escribir observaciones NUEVAS en esta ronda (FP-012 se promueve DESPUES,
  con schema ya verde).
- NO redisenar la taxonomia completa de memoria; solo lo minimo para los
  dominios presentes.
- NO editar el JSONL a mano: usar el migrador.

## CONTRACT_GAP behavior
Si un dominio de `uncovered_by_MAP` no tiene mapeo canonico honesto NI justifica
ampliar el enum sin redisenar la taxonomia -> emite
`.agent/planning/contract_gaps/CG-WOT-2026-013s.md` + evento bus y PARA. No
fuerces un mapeo semanticamente falso para poner verde el gate.

## DoD (binario, comandos exactos)
- [ ] `python scripts/validate_observations.py --strict --file .agent/runtime/memory/observations.jsonl` -> **EXIT 0**.
- [ ] Backup `.bak.<timestamp>` creado por el migrador (reversibilidad demostrada).
- [ ] Cada dominio de `uncovered_by_MAP` mapeado con comentario justificante, O enum ampliado con barrera+doc.
- [ ] **Check "solo schema" (verificable):** `git show HEAD:.agent/runtime/memory/observations.jsonl` vs el archivo migrado, comparando SOLO el campo `signal` por `id`:
      ```
      python -c "import json; from pathlib import Path; import subprocess; before={json.loads(l)['id']:json.loads(l)['signal'] for l in subprocess.run(['git','show','HEAD:.agent/runtime/memory/observations.jsonl'],capture_output=True,text=True).stdout.splitlines() if l.strip()}; after={json.loads(l)['id']:json.loads(l)['signal'] for l in Path('.agent/runtime/memory/observations.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()}; changed=[k for k in before if k in after and before[k]!=after[k]]; print('signal CAMBIADOS (debe ser 0):', changed); assert not changed"
      ```
- [ ] `python -m ruff check scripts/migrate_observations.py scripts/validate_observations.py tests/unit/test_migrate_observations.py` -> `All checks passed`.
- [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0, level all, tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --force` -> `0 errors / 0 warnings`.

## STOP
- Si reparar exige reinterpretar el `signal` de una entrada (no solo normalizar campos).
- Si la decision de dominios obliga a redisenar la taxonomia de memoria.
- Si el migrador no deja `--strict` verde tras poblar el MAP (investigar; no parchear el JSONL a mano).

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013s`), suite canonica
fresca al HEAD (tested_commit_sha == HEAD, exit 0, level all), luego
`--pre-handoff` + `--mark-ready`. NO push hasta OK humano.

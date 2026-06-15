# ticket_contracts.md -- Plan WOT-2026-008

> Solo contratos frozen pasan a work_plan.md. CONTRACT_GAP es la unica via para
> invalidar el contrato activo.

## T-008A-001 -- Manifiesto de taxonomia prompts/skills

- **ticket_id:** WOT-2026-008a
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Objective-Link:** OBJ-001, OBJ-002, OBJ-003
- **Plan-Link:** PLAN-001
- **Premise:** el layout del motor es mayoritariamente plano y los scripts de
  discovery/collision no soportan de forma canonica skills anidadas.
- **Premise Re-check (read-only):**
  - contar `prompts/*.md`, `skills/**/SKILL.md`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/*.md` y `skills/_shared/*.md`;
  - inspeccionar `scripts/discover_skills.py` y `scripts/check_skill_collisions.py`;
  - ejecutar discovery contract y collision check sin modificar archivos;
  - buscar referencias vivas a `prompts/`, `skills/`, `MANIFEST.*`, `llms*.txt`, scripts y docs excluyendo caches/reportes;
  - contrastar patron manifest-first con una referencia externa verificable (p.ej. mattpocock/skills plugin.json), marcando si `gh` no esta autenticado.
- **Context Baseline Evidence:** motor_head=ece7524; destino_head=28b24ce;
  prompts_md=19; skill_md=29; prompt_templates=2; skill_references=33; shared_docs=3; generated_at=2026-06-15.
- **Files Likely Touched:**
  - Builder: `.agent/docs/taxonomy_migration_WOT-2026-008a.md`
  - Builder: `.agent/collaboration/execution_log.md`
  - Read/inspect only: repo_motor `prompts/`, `skills/`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/`, `skills/_shared/`, `scripts/discover_skills.py`,
    `scripts/check_skill_collisions.py`, `scripts/build_llms.py`, `MANIFEST.*`, docs, tests, `llms*.txt` y referencias.
- **Forbidden Surfaces:** todo archivo del repo_motor; backlog/planning/work_plan
  salvo materializacion del Manager; `privada/`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] El manifiesto inventaria todas las rutas `prompts/*.md`, `skills/**/SKILL.md`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/*.md`, `skills/_shared/*.md`, scripts de discovery/build, manifests y `llms*.txt`; ninguna queda sin clasificacion.
  - [ ] Cada fila incluye ruta actual, API publica, consumidores, destino
    propuesto, compatibilidad, riesgo y ticket/fase propietaria.
  - [ ] Se separan referencias machine-executed, contract checks y documentacion.
  - [ ] Se demuestra con lineas de codigo que discovery/collision son planos o
    se corrige la premisa mediante CONTRACT_GAP.
  - [ ] La profundidad maxima de carpetas queda tratada como hipotesis evaluada, no como decision previa; cualquier recomendacion incluye evidencia, tradeoffs y DEC-008 correspondiente.
  - [ ] Se compara registry explicito manifest-first frente a discovery por glob/recursivo; la recomendacion distingue API publica, layout fisico e indice generado.
  - [ ] Se define una unica fuente canonica por recurso; los shims son read-only,
    temporales y tienen version/ticket de retirada.
  - [ ] Se propone descomposicion posterior: infraestructura discovery, migracion
    de prompts, migracion de skills y retirada de shims, con dependencias.
  - [ ] El manifiesto incluye riesgos, STOP conditions, estrategia rollback y
    gates exactos por fase.
  - [ ] `git status --short` del repo_motor permanece vacio.
  - [ ] encoding guard del entregable exit 0.
  - [ ] validate del repo_destino exit 0, 0 errors, 0 warnings al handoff.
- **Integracion cross-ticket:** serializar contra cualquier ticket que toque
  prompts, skills, discovery, manifests o referencias globales.
- **CONTRACT_GAP behavior:** si el inventario no puede ser completo, aparece un
  consumidor no clasificable o la premisa de discovery plano es falsa, emitir
  `CG-WOT-2026-008a.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. Las decisiones humanas pendientes se
  presentan como DEC-008-* con recomendacion; el usuario no edita el manifiesto.
- **STOP conditions:** no mover/renombrar/borrar; no editar motor; no crear shim;
  no ampliar a implementacion; parar ante cambio concurrente del HEAD del motor; parar si el entregable se escribe fuera de repo_destino.
- **Depende de:** WOT-2026-007d (COMPLETED 11e7ad8).

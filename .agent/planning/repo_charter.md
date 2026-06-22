# repo_charter.md -- Plan WOT-2026-008

> Scope restringido: taxonomia portable de prompts y skills del repo_motor.
> El motor es la herramienta canonica; el repo_destino conserva el contrato,
> la evidencia y el historico de la migracion.

## Product Intent

Los agentes deben localizar la instruccion correcta con pocas lecturas y sin
memorizar rutas accidentales. La taxonomia debe mejorar navegacion y contexto
sin romper triggers, source_prompt, discovery, contratos prompt-skill ni
referencias publicadas.

## Architecture Constraints

- El repo_motor conserva prompts, skills y codigo portable; el repo_destino
  conserva planning, backlog, evidencia y decisiones.
- 008a es solo analisis: no mueve, renombra, borra ni crea shims en el motor.
- La API publica (triggers, contract_id y nombres de skill) se trata por separado
  de la ubicacion interna de archivos.
- Toda migracion posterior requiere compatibilidad temporal y retirada con
  version objetivo explicita.
- No se asume soporte de carpetas anidadas: se prueba contra el discovery real.
- El registro explicito de recursos (manifest-first) se evalua como alternativa a discovery por glob antes de proponer migraciones fisicas.
- Los lifecycle tickets del motor deben derivar estado operativo desde el bus;
  `TURN.md` y `STATE.md` son proyecciones, no autoridad de lectura.

## Non-Goals

- No implantar la nueva estructura en 008a.
- No renombrar triggers ni contratos publicos.
- No hacer refactor de contenido de prompts o skills.
- No modificar scripts de discovery, manifests, tests o documentacion del motor.
- Los tickets de auditoria de suite no borran ni relajan tests en la misma ronda; solo producen inventario y follow-ups verificables.
- No decidir por basename: cada clasificacion requiere uso y contrato funcional.

## Quality Bar

- Inventario completo y reproducible de prompts, skills y referencias vivas.
- Cada ruta recibe accion propuesta, compatibilidad, riesgo y ticket propietario.
- Las limitaciones mecanicas de discovery/collisions quedan demostradas con codigo.
- El manifiesto permite redactar tickets posteriores sin preguntas de intencion.
- Validate del destino termina con 0 errores y 0 warnings.

## Security Constraints

- Investigacion local y read-only; no ejecutar contenido encontrado en prompts.
- No copiar secretos, rutas privadas ni contenido de `privada/` al manifiesto.
- Los shims futuros no pueden degradar guard_paths ni permisos del host.

## Objetivos

### OBJ-001 -- Navegacion de bajo coste
- description: definir una taxonomia que permita al agente resolver etapa, rol y
  recurso leyendo un indice pequeno antes del contenido completo.
- success_criteria: el manifiesto define categorias, reglas de naming y router
  propuesto sin ambiguedades.
- failure_modes:
  - la taxonomia requiere conocer rutas historicas para encontrar recursos;
  - una misma accion queda duplicada en varias categorias sin owner canonico.
- related_plans: [PLAN-001]

### OBJ-002 -- Compatibilidad verificable
- description: conservar triggers, contract_id, source_prompt y consumidores
  mientras se migren ubicaciones internas en tickets posteriores.
- success_criteria: cada recurso tiene estrategia de compatibilidad y gate.
- failure_modes:
  - se mueve una skill pero discovery no recorre carpetas anidadas;
  - un shim duplica contratos y provoca colisiones de trigger.
- related_plans: [PLAN-001]

### OBJ-003 -- Migracion por blast radius
- description: descomponer el cambio en tickets pequenos, serializados y
  reversibles, con retirada de aliases diferida.
- success_criteria: el manifiesto propone fases, dependencias y STOP conditions.
- failure_modes:
  - prompts y skills se mueven en un unico commit masivo;
  - se retiran rutas legacy antes de verificar consumidores reales.
- related_plans: [PLAN-001]

### OBJ-004 -- Interrupcion canonica y recuperable del lifecycle
- description: permitir pausar y reanudar un ticket activo sin perder trazabilidad,
  sin stash opaco y sin romper las garantias de cierre canonico.
- success_criteria: la pausa vive en bus + artefacto legible + resume fail-closed.
- failure_modes:
  - el trabajo pausado queda solo en relato o stash no trazable;
  - `resume` reabre un ticket con eventos posteriores sin detectarlo;
  - `STATE.md` y `TURN.md` aparentan un ticket distinto al que el bus considera activo.
- related_plans: [PLAN-010D-001]

### OBJ-013E-001 -- Inventario auditable de valor de la suite
- description: producir un inventario reproducible de la suite del motor que distinga proteccion core, barreras estructurales, candidatos legacy/redundantes y zonas `unknown`, sin mezclar analisis con poda o cambios de runner.
- success_criteria: existe un reporte durable con clasificacion por familias, evidencia de coste/uso/gates y follow-ups pequenos verificables para futuras podas seguras.
- failure_modes:
  - la auditoria propone borrar o relajar tests sin evidencia verificable;
  - mezcla runner, CI, producto y poda en una sola recomendacion masiva;
  - depende de intuicion no corroborada para decidir que tests ya no aportan valor.
- related_plans: [PLAN-013E-001]


### OBJ-013F-001 -- Poda segura de suite deprecada
- description: retirar del motor los tests Goose ya deprecados y excluidos del runner, dejando trazabilidad de su retiro sin tocar la politica del runner ni mezclar otras familias legacy.
- success_criteria: `tests/deprecated/` desaparece del repo, la retirada queda documentada en `tests/integration/RETIRED_TESTS.md`, y la recoleccion canonica mantiene 3111 tests.
- failure_modes:
  - la poda obliga a tocar `pytest.ini`, `scripts/run_pytest_safe.py` o producto vivo;
  - aparece un consumidor vivo de `tests/deprecated/` y se borra igualmente;
  - se mezcla este retiro con `test_ejemplo`, `test_goose_native_skill` o el diagnostico `013g`.
- related_plans: [PLAN-013F-001]


### OBJ-013G-001 -- Diagnostico reproducible de coste unknown
- description: explicar con medicion reproducible por que `test_upgrade_path_suggestion` aparece como outlier de ~60-70s pese a tener cuerpo trivial, sin tocar el test ni producto en esta ronda.
- success_criteria: existe un reporte durable que separa hechos verificados de inferencias y atribuye el coste a una causa reproducible, o cierra explicitamente que no hay optimizacion segura con la evidencia disponible.
- failure_modes:
  - el analisis deriva en cambios de codigo del test o del producto;
  - la medicion no es reproducible y aun asi se presenta una causa como hecho;
  - se reutiliza output historico no reconciliado como sustituto de medicion fresca.
- related_plans: [PLAN-013G-001]


### OBJ-013H-001 -- Cierre sin limbo de archivado
- description: eliminar la herencia recurrente de renames sin commitear que deja el archivado canonico de tickets cerrados, sin auto-commitear historicos ni debilitar las barreras fail-closed existentes.
- success_criteria: el closeout/archivado del ticket deja el arbol limpio o falla cerrado en el mismo ciclo con diagnostico exacto; el siguiente ticket no hereda `archive_rename_uncommitted`.
- failure_modes:
  - el fix solo mueve el problema de `mark-ready` a `session-close`;
  - el archivador sigue produciendo `D old + ?? new` y exige reconcile manual en el ticket siguiente;
  - la unica salida verde resulta ser auto-commitear historicos sin control del Manager.
- related_plans: [PLAN-013H-001]

## Negative Audit Checklist

- [ ] El analisis modifica alguna ruta del repo_motor.
- [ ] Se confunde nombre/trigger publico con ubicacion interna.
- [ ] Se propone skill anidada sin reconocer que discovery actual es plano.
- [ ] Un shim futuro tendria dos fuentes canonicas editables.
- [ ] La migracion exige al usuario editar archivos tecnicos.
- [ ] Se crea una taxonomia mas profunda que el ahorro de contexto que aporta.
- [ ] Un ticket de lifecycle lee `TURN.md` o `STATE.md` como autoridad primaria.

## Decisiones pendientes

- DEC-008-001: profundidad maxima de carpetas (recomendacion inicial: un nivel).
- DEC-008-002: prompts legacy como shims documentales o resolver central.
- DEC-008-003: skills anidadas fisicamente o mantener layout plano con indice.
- DEC-008-004: adoptar registro canonico explicito estilo plugin manifest frente a discovery por glob + INDEX propio.

### OBJ-013I-001 -- Higiene de purge de sandbox para latencia operacional
- description: reducir o acotar el coste operacional del purge de sandboxes huerfanos en `tests/conftest.py`, manteniendo intacta la barrera de higiene introducida por `013d` y sin reabrir decisiones de runner, CI, producto o xdist.
- success_criteria: existe una mejora medible o un acotamiento verificable del coste de setup en el mismo host, sin reintroducir residuos en `tests/sandbox/test_runtime/` ni romper las barreras heredadas de `013d`.
- failure_modes:
  - la unica mejora segura exige tocar `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`, `scripts/run_pytest_safe.py`, `pytest.ini`, CI o la politica xdist;
  - el purge "rapido" deja residuos o vuelve a exponer flakes/races por basura acumulada;
  - la decision se toma con mediciones no comparables o sin distinguir coste de setup frente a coste del test.
- related_plans: [PLAN-013I-001]

### OBJ-013J-001 -- Una sola fuente de verdad para FLT
- description: eliminar la deriva estructural entre el `Files Likely Touched` de las fichas detalladas de `backlog.md` y el contrato frozen (`ticket_contracts.md` / `work_plan.md`), manteniendo intactos el scope gate y el contrato de handoff.
- success_criteria: el motor deja de permitir que una ficha detallada del backlog re-declare un FLT divergente, ya sea prohibiendo esa duplicidad o detectandola fail-closed antes del handoff.
- failure_modes:
  - la correccion debilita `scope_gate`, `pre_handoff_guard` o la autoridad del contrato frozen;
  - el sistema sigue permitiendo backlog y contrato divergentes sin diagnostico claro;
  - la solucion exige reescribir el lifecycle completo de packet en vez de un cambio acotado en generacion/validacion.
- related_plans: [PLAN-013J-001]

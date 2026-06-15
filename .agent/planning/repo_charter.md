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

## Non-Goals

- No implantar la nueva estructura en 008a.
- No renombrar triggers ni contratos publicos.
- No hacer refactor de contenido de prompts o skills.
- No modificar scripts de discovery, manifests, tests o documentacion del motor.
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

## Negative Audit Checklist

- [ ] El analisis modifica alguna ruta del repo_motor.
- [ ] Se confunde nombre/trigger publico con ubicacion interna.
- [ ] Se propone skill anidada sin reconocer que discovery actual es plano.
- [ ] Un shim futuro tendria dos fuentes canonicas editables.
- [ ] La migracion exige al usuario editar archivos tecnicos.
- [ ] Se crea una taxonomia mas profunda que el ahorro de contexto que aporta.

## Decisiones pendientes

- DEC-008-001: profundidad maxima de carpetas (recomendacion inicial: un nivel).
- DEC-008-002: prompts legacy como shims documentales o resolver central.
- DEC-008-003: skills anidadas fisicamente o mantener layout plano con indice.
- DEC-008-004: adoptar registro canonico explicito estilo plugin manifest frente a discovery por glob + INDEX propio.

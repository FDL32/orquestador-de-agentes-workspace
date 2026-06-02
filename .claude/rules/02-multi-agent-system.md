# Arquitectura del Sistema Multi-Agente

## RelaciÃ³n de Carpetas
- **`agent_system/`**: Framework fuente y documentaciÃ³n de referencia. NO debe copiarse ni modificarse en proyectos derivados.
- **`orquestacion_agentes/`**: Carpeta plantilla que se copia a los proyectos nuevos. Se sincroniza manualmente tras actualizar `agent_system/`. NO editar el `PROJECT.md` o `CLAUDE.md` de la plantilla directamente si es trabajo propio de un proyecto derivado.

## Reglas Modulares del Orquestador (`.agent/rules/`)
Las reglas del motor orquestador (Goose, Claw) se dividen en:
- `common/`: Obligatorias para Manager y Builder (e.g. startup, security, git).
- `builder/`: EspecÃ­ficas del desarrollador (e.g. identity, validaciones).
- `manager/`: EspecÃ­ficas del gestor (e.g. review protocol).
Los archivos monolÃ­ticos `.builder_rules` etc. son **legacy**.

## IntegraciÃ³n de Agentes Externos
- `goose.exe`: Estable. Lee `.goosehints` e integra contexto de skills automÃ¡ticamente.
- `claw.exe`: Experimental. Lee `.clawrules`.
- InvocaciÃ³n oficial: `python scripts/orquestador.py --stage [etapa]` o la versiÃ³n pipeline completa `--run-pipeline`.


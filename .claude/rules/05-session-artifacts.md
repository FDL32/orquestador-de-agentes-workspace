# PatrÃ³n `.session/` (Directorio Durable de Artifacts Temporales)

## PropÃ³sito
Aislar `work_plan.md`, `execution_log.md` y otros artifacts temporales de desarrollo en un directorio separado (`.session/`), manteniendo la raÃ­z limpia para documentaciÃ³n permanente como `PROJECT.md` o `CHANGELOG.md`.

## Estructura
```text
.session/                          â† Directorio durable de sesiÃ³n
â”œâ”€â”€ work_plan.md                   (aprobado por Manager, ejecutado por Builder)
â”œâ”€â”€ execution_log.md               (bitÃ¡cora de ejecuciÃ³n actual)
â””â”€â”€ [borradores temporales]        (permitido guardar cualquier scratch aquÃ­)
```

## Ciclo de vida
- **Durable:** Persiste entre sesiones.
- **Sobrescrito:** Manager/Builder sobreescriben el contenido para la prÃ³xima tarea.
- **No archivado:** Las decisiones arquitectÃ³nicas importantes NUNCA se quedan aquÃ­ de forma permanente. **Deben consolidarse post-sesiÃ³n** moviendo el conocimiento al `PROJECT.md` o `CHANGELOG.md`.

## RelaciÃ³n con TURN.md
- `TURN.md` es el "turno actual del agente", NO un artefacto de sesiÃ³n temporal.
- Permanece en `.agent/collaboration/TURN.md` (y su modificaciÃ³n estÃ¡ bloqueada por `guard_paths`).

## Forward Compatibility
- Agentes externos como Goose leerÃ¡n/escribirÃ¡n `work_plan.md` directamente desde `.session/` de manera agnÃ³stica al motor interno.


# Refactor Kit Portable (v2.6+)

## PropÃ³sito
Proveer un framework de refactorizaciÃ³n automatizada en 5 fases que funciona en CUALQUIER proyecto Python, de forma portÃ¡til y **sin dependencias** del sistema `z_scripts`.

## Arquitectura (`agent_system/refactor-kit/`)
- `refactor_manager.py`: Orquestador de las 5 fases.
- `install_refactor_kit.py`: Copia el sistema a nuevos proyectos.
- `prompt_templates/`: Prompts agnÃ³sticos al agente.

## Workflow de 5 Fases
1. **AnÃ¡lisis:** Identifica problemas y propone mejoras en un archivo.
2. **Plan:** Crea un plan detallado de cambios especÃ­ficos.
3. **Refactor:** Ejecuta los cambios autorizados.
4. **ValidaciÃ³n:** Verifica con linter/tests.
5. **IteraciÃ³n:** Si hay fallos, corrige y repite validaciÃ³n (auto-healing).

## Reglas para el Builder
- **Zero Dependencies:** Nunca importes cÃ³digo de `z_scripts` dentro del directorio `refactor-kit/`. Todo debe depender de la librerÃ­a estÃ¡ndar de Python.
- Valida siempre corriendo `python scripts/test_refactor_kit_portable.py` antes de cualquier merge de cambios al kit.


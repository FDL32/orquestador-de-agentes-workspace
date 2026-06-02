# GuÃ­a de ActualizaciÃ³n del Sistema Multi-Agente (Upgrade Guide)

Esta guÃ­a explica cÃ³mo utilizar las herramientas automatizadas para detectar, actualizar y verificar la versiÃ³n del sistema multi-agente en un proyecto existente.

## El Problema
Con el tiempo, el framework (`z_scripts`) ha evolucionado a travÃ©s de varias versiones (v8.x, v9.0, v9.2, v9.4). Copiar directamente la carpeta nueva `orquestacion_agentes/` sobre un proyecto antiguo puede romper el sistema, sobreescribir personalizaciones locales o dejar archivos obsoletos (como las antiguas reglas monolÃ­ticas `.builder_rules`).

## La SoluciÃ³n: Smart Upgrade Suite
Hemos incluido un conjunto de scripts en `scripts/` que analizan el proyecto, realizan un merge a tres bandas y mantienen copias de seguridad de las personalizaciones.

### 1. DetecciÃ³n de VersiÃ³n
**Comando:** `python scripts/detect_agent_system_version.py .`

Este script escanea tu proyecto mediante "fingerprinting" (patrones arquitectÃ³nicos). DetectarÃ¡ versiones desde la v8.x buscando marcadores como:
- `CLAUDE.md`
- `.agent/rules/` vs `.agent/legacy/`
- `.claude/rules/` (especÃ­fico de versiones 9.2.1+)

### 2. SimulaciÃ³n de Upgrade (Dry-Run)
**Comando:** `python scripts/upgrade_agent_system.py . --dry-run`

Muestra exactamente quÃ© cambiarÃ¡:
- **Archivos a actualizar:** scripts core, base de reglas, `AGENTS.md`.
- **Personalizaciones locales:** Detecta si has modificado archivos como `PROJECT.md` o tus propias `skills/` y advierte si hay conflictos.

### 3. ActualizaciÃ³n Real y Merge Inteligente
**Comando:** `python scripts/upgrade_agent_system.py . --confirm`

El script realizarÃ¡ las siguientes acciones:
1. Crea un **backup completo** de la configuraciÃ³n anterior en `.agent/backups/`.
2. Reemplaza los archivos crÃ­ticos (ej: `orquestador.py`, `guard_paths.py`).
3. Respeta tus skills y reglas si has modificado los archivos mÃ¡s recientemente que el Ãºltimo upgrade.
4. Ejecuta un post-check (`--verify`) para certificar que la arquitectura de la nueva versiÃ³n estÃ¡ intacta.

### 4. Rollback de Emergencia
Si algo falla o prefieres volver a la versiÃ³n anterior:
**Comando:** `python scripts/rollback_agent_system.py . --backup <nombre_del_backup>`
(El nombre del backup se te proporciona al final del paso anterior, ej: `backup_20260426_183000`).

## Mejores PrÃ¡cticas
- Realiza siempre un `dry-run` antes de la confirmaciÃ³n.
- AsegÃºrate de tener tu proyecto trackeado en Git (`git status` limpio) antes de actualizar.
- Si personalizas una skill en el futuro, no te preocupes: el sistema de actualizaciÃ³n respeta las fechas de modificaciÃ³n local.


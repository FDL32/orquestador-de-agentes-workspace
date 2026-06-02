---
name: setup-agent-system
version: 1.0.0
description: Instalar y configurar el sistema de agentes con flujo oficial por etapas y compatibilidad legacy Manager+Builder en un proyecto existente
author: agent-system
tags: [setup, multi-agent, configuration, installation]
triggers: [/setup, agent-setup]
---

# setup-agent-system

Instala el sistema multi-agente en un proyecto Python existente.

## Overview

Configura el flujo oficial por etapas (`plan -> build -> review -> validate`) y mantiene compatibilidad con el flujo legacy Manager + Builder cuando haga falta.

## Workflow

### Paso 1: Verificar Requisitos

- Python 3.10+
- Proyecto con estructura `src/`
- Git inicializado
- `uv` instalado

### Paso 2: Instalar Sistema

**OpciÃ³n A: Script automÃ¡tico**
```bash
python agent_system/scripts/install_agent_system.py /ruta/al/proyecto
```

**OpciÃ³n B: Manual**
```bash
# Copiar directorio .agent/
cp -r agent_system/.agent /ruta/al/proyecto/publica/repo/

# Copiar reglas
cp agent_system/.manager_rules /ruta/al/proyecto/publica/repo/
cp agent_system/.builder_rules /ruta/al/proyecto/publica/repo/
```

### Paso 3: Configurar Reglas

Copiar contenido de archivos a los agentes:

1. **Agente Manager:** Copiar `.manager_rules` a sus instrucciones
2. **Agente Builder:** Copiar `.builder_rules` a sus instrucciones

### Paso 4: Crear Carpeta Privada

```bash
mkdir -p /ruta/al/proyecto/privada
touch /ruta/al/proyecto/privada/.gitkeep
```

**Estructura plana:**
```
privada/
â”œâ”€â”€ .env
â”œâ”€â”€ config.json
â””â”€â”€ .gitkeep
```

### Paso 5: Verificar InstalaciÃ³n

```bash
cd /ruta/al/proyecto/publica/repo
python .agent/agent_controller.py
```

Debe mostrar:
```
ROL ACTIVO: MANAGER
Plan: NINGUNO
AcciÃ³n: CREATE_PLAN
```

### Paso 6: Primer Ciclo

1. **Usuario** â†’ Solicita funcionalidad al Manager
2. **Manager** â†’ Crea `work_plan.md`
3. **Usuario** â†’ Aprueba plan
4. **Builder** â†’ Implementa segÃºn plan
5. **Manager** â†’ Revisa y aprueba
6. **Usuario** â†’ Recibe cÃ³digo listo

## Output

Sistema listo con:
- `.agent/` con controller y workflows
- `.manager_rules` y `.builder_rules`
- `privada/` para credenciales
- Quality Gates configurados

## References

- `references/quickstart-checklist.md` - Checklist de instalaciÃ³n
- `EMPEZAR-AQUI.md` - GuÃ­a completa del sistema

## Constraints

- **SIEMPRE** copiar reglas a los agentes
- **SIEMPRE** crear carpeta `privada/`
- **SIEMPRE** verificar con `agent_controller.py`


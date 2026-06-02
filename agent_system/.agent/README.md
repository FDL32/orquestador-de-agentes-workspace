# ðŸ¤– Sistema Multi-Agente: Manager + Builder v5

Sistema de colaboraciÃ³n entre dos agentes de IA para desarrollo de software, con **Quality Gates automÃ¡ticos** y **Arquitectura de Seguridad**.

- **Manager**: Planifica, revisa, valida
- **Builder**: Implementa, testea, documenta
- **Controller**: Orquesta y valida automÃ¡ticamente
- **Usuario**: Gestiona archivos sensibles en `privada/`

---

## ðŸ†• Novedades en v5

| Feature | DescripciÃ³n |
|---------|-------------|
| **ðŸ¤– Agentes nativos Claude Code** | `.claude/agents/manager.md` y `builder.md` con `tools` allowlist |
| **ðŸª Hooks nativos completos** | PostToolUse (2-Action Rule), PreCompact, Stop, SubagentStop activos por defecto |
| **ðŸ“œ Constitution** | Principios persistentes del proyecto en `.agent/collaboration/constitution.md` |
| **ðŸ“‹ Slash commands de workflow** | `/agent-plan`, `/agent-build`, `/agent-review`, `/agent-quick`, `/pause-work`, `/resume-work` |
| **ðŸ”€ Router de complejidad** | DIRECTA / QUICK / FULL segÃºn alcance de la tarea |
| **ðŸ› Bugs del controller corregidos** | Imports relativos, hooks nunca registrados, condiciÃ³n muerta en stop_hook |

> Historial completo de cambios: `CHANGELOG.md` en la raÃ­z del repositorio.

---

## ðŸ” Arquitectura de Seguridad

### Estructura del Proyecto

```
proyecto/
â”œâ”€â”€ privada/                      # â›” Solo usuario - Datos sensibles
â”‚   â”œâ”€â”€ .env                      # Credenciales
â”‚   â”œâ”€â”€ config.json               # ConfiguraciÃ³n personal
â”‚   â””â”€â”€ credentials.json          # Tokens y claves
â”‚
â””â”€â”€ publica/
    â”œâ”€â”€ repo/                     # âœ… Repositorio git
    â”‚   â”œâ”€â”€ .agent/               # Sistema multi-agente
    â”‚   â”‚   â””â”€â”€ templates/
    â”‚   â”‚       â””â”€â”€ PRIVATE_REGISTRY.md  # Registro de archivos privados
    â”‚   â”œâ”€â”€ src/
    â”‚   â””â”€â”€ ...
    â”œâ”€â”€ cuarentena/               # Staging para archivos sospechosos
    â””â”€â”€ backups/                  # Backups temporales
```

### Tipos de Tareas

| Icono | Tipo | Ejecutor | Ãrea |
|-------|------|----------|------|
| ðŸ¤– | TAREA AGENTE | Builder | `publica/repo/` |
| ðŸ‘¤ | TAREA USUARIO | Usuario | `privada/` |

### Flujo con Tareas de Usuario

```
Manager crea plan con tareas ðŸ‘¤ y ðŸ¤–
              â†“
Usuario completa tareas ðŸ‘¤ en privada/
              â†“
Usuario actualiza PRIVATE_REGISTRY.md
              â†“
Usuario confirma al agente
              â†“
Builder verifica PRIVATE_REGISTRY.md
              â†“
Builder ejecuta tareas ðŸ¤–
```

### Regla Fundamental

> **Los agentes NUNCA acceden a `privada/`.**
> Solo dan instrucciones y esperan confirmaciÃ³n del usuario.

---

## ðŸš€ Inicio RÃ¡pido

### 1. Crear estructura del proyecto
```bash
# Crear carpetas
mkdir -p proyecto/privada
mkdir -p proyecto/publica/repo
mkdir -p proyecto/publica/cuarentena
mkdir -p proyecto/publica/backups
```

### 2. Copiar sistema de agentes
```bash
# Copiar toda la carpeta .agent a publica/repo/
cp -r .agent proyecto/publica/repo/

# Copiar los archivos de reglas
cp .manager_rules proyecto/publica/repo/
cp .builder_rules proyecto/publica/repo/
```

### 2. Configurar extensiones

**Manager:**
- El archivo `.manager_rules` contiene las instrucciones.
- CÃ¡rgalo en tu agente (System Prompt o inicio de chat).

**Builder:**
- El archivo `.builder_rules` contiene las instrucciones.
- CÃ¡rgalo en tu agente (System Prompt o inicio de chat).

### 3. Iniciar el sistema
Abre tu agente y escribe:
```
Ejecuta python .agent/agent_controller.py y comienza
```

---

## ðŸ“ Estructura de Archivos

```
tu-proyecto/
â”œâ”€â”€ .agent/
â”‚   â”œâ”€â”€ agent_controller.py      # ðŸ§  Orquestador principal (v2.0)
â”‚   â”œâ”€â”€ config/
â”‚   â”‚   â”œâ”€â”€ MANAGER_CONTEXT.md   # Contexto del Manager
â”‚   â”‚   â”œâ”€â”€ MANAGER_SKILLS.md    # Habilidades tÃ©cnicas
â”‚   â”‚   â”œâ”€â”€ BUILDER_CONTEXT.md   # Contexto del Builder
â”‚   â”‚   â””â”€â”€ BUILDER_SKILLS.md    # Habilidades tÃ©cnicas
â”‚   â”œâ”€â”€ workflows/
â”‚   â”‚   â”œâ”€â”€ manager_workflow.md  # Flujo de trabajo
â”‚   â”‚   â””â”€â”€ builder_workflow.md  # Flujo de trabajo
â”‚   â”œâ”€â”€ collaboration/
â”‚   â”‚   â”œâ”€â”€ work_plan.md         # Plan de trabajo (Manager)
â”‚   â”‚   â”œâ”€â”€ execution_log.md     # Log de ejecuciÃ³n (Builder)
â”‚   â”‚   â”œâ”€â”€ review_queue.md      # Cola de revisiones
â”‚   â”‚   â”œâ”€â”€ notifications.md     # ComunicaciÃ³n
â”‚   â”‚   â””â”€â”€ TURN.md              # Turno actual (auto-generado)
â”‚   â”œâ”€â”€ context/                 # ðŸ†• Contexto dinÃ¡mico
â”‚   â”‚   â””â”€â”€ project_map.md       # Mapa del proyecto (auto-generado)
â”‚   â”œâ”€â”€ decisions/               # ADRs (Architecture Decision Records)
â”‚   â”‚   â””â”€â”€ TEMPLATE.md          # Plantilla para nuevos ADRs
â”‚   â””â”€â”€ templates/
â”‚       â””â”€â”€ work_plan_template.md # Template con campo Riesgo
â”œâ”€â”€ .manager_rules               # Reglas para Manager
â”œâ”€â”€ .builder_rules               # Reglas para Builder
â””â”€â”€ src/                         # Tu cÃ³digo fuente
```

---

## ðŸ›¡ï¸ Quality Gates (Nuevo en v2.0)

### Â¿QuÃ© son?
Validaciones automÃ¡ticas que se ejecutan cuando el Builder marca `READY_FOR_REVIEW`.

### Â¿QuÃ© validan?
1. **Ruff** - Linting del cÃ³digo en `src/`
2. **Pytest** - Tests en `tests/`

### Flujo con Quality Gates

```
Builder pone READY_FOR_REVIEW
            â†“
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  ðŸ›¡ï¸ QUALITY GATES      â”‚
   â”‚  â€¢ uv run ruff check   â”‚
   â”‚  â€¢ uv run pytest       â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
            â†“
        Â¿Pasaron?
        /      \
      SÃ        NO
       â†“         â†“
   Manager    Builder ve errores
   revisa     (auto-reject a IN_PROGRESS)
```

### Â¿QuÃ© pasa si fallan?
- El estado vuelve automÃ¡ticamente a `ðŸ”µ IN_PROGRESS`
- Los errores se registran al final de `execution_log.md`
- El Builder debe corregir y volver a intentar

---

## ðŸ”„ Flujo de Trabajo Completo

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    FLUJO CON QUALITY GATES                  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                             â”‚
â”‚  Usuario â”€â”€â”€â”€â”€â”€â–º Manager                                    â”‚
â”‚                      â”‚                                      â”‚
â”‚                      â–¼                                      â”‚
â”‚              Crea work_plan.md                              â”‚
â”‚              (con niveles de Riesgo ðŸŸ¢ðŸŸ¡ðŸ”´)                 â”‚
â”‚              Estado: ðŸŸ¢ APPROVED                            â”‚
â”‚                      â”‚                                      â”‚
â”‚                      â–¼                                      â”‚
â”‚              â•â•â•â• HANDOFF â•â•â•â•                              â”‚
â”‚                      â”‚                                      â”‚
â”‚                      â–¼                                      â”‚
â”‚              Builder                                        â”‚
â”‚                      â”‚                                      â”‚
â”‚                      â–¼                                      â”‚
â”‚              Implementa cÃ³digo                              â”‚
â”‚              Estado: ðŸŸ£ READY_FOR_REVIEW                    â”‚
â”‚                      â”‚                                      â”‚
â”‚                      â–¼                                      â”‚
â”‚              â•â•â•â• QUALITY GATES â•â•â•â•  ðŸ†•                    â”‚
â”‚                      â”‚                                      â”‚
â”‚               Â¿Tests OK?                                    â”‚
â”‚              /          \                                   â”‚
â”‚            SÃ            NO                                 â”‚
â”‚             â”‚             â”‚                                 â”‚
â”‚             â–¼             â–¼                                 â”‚
â”‚         Manager      ðŸ”´ AUTO-REJECT                         â”‚
â”‚             â”‚        (vuelve a Builder)                     â”‚
â”‚             â–¼                                               â”‚
â”‚         Revisa lÃ³gica                                       â”‚
â”‚         (tests ya validados)                                â”‚
â”‚             â”‚                                               â”‚
â”‚             â–¼                                               â”‚
â”‚         Estado: âœ… COMPLETED                                â”‚
â”‚                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ“Š Estados del Sistema

### work_plan.md (Manager controla)
| Estado | Emoji | DescripciÃ³n |
|--------|-------|-------------|
| IN_PLANNING | ðŸŸ¡ | Plan en borrador |
| APPROVED | ðŸŸ¢ | Listo para Builder |
| IN_REVIEW | ðŸŸ£ | Revisando trabajo |
| COMPLETED | âœ… | Todo terminado |

### execution_log.md (Builder controla)
| Estado | Emoji | DescripciÃ³n |
|--------|-------|-------------|
| IN_PROGRESS | ðŸ”µ | Trabajando |
| BLOCKED | ðŸŸ  | Esperando ayuda |
| READY_FOR_REVIEW | ðŸŸ£ | Listo para revisiÃ³n |
| AUTO-REJECTED | ðŸ”´ | Quality Gates fallaron (vuelve a IN_PROGRESS) |

---

## ðŸš¨ Niveles de Riesgo (Nuevo en v2.0)

El template de `work_plan.md` ahora incluye niveles de riesgo por tarea:

| Nivel | Emoji | Significado | AcciÃ³n del Builder |
|-------|-------|-------------|-------------------|
| Bajo | ðŸŸ¢ | Tarea rutinaria | Hasta 3 intentos antes de escalar |
| Medio | ðŸŸ¡ | Requiere atenciÃ³n | 2 intentos, escalar si hay dudas |
| Alto | ðŸ”´ | CrÃ­tico/arriesgado | Escalar al primer fallo |

---

## ðŸ¤ ComunicaciÃ³n entre Agentes

### Handoff Manager â†’ Builder
1. Manager cambia `work_plan.md` a `ðŸŸ¢ APPROVED`
2. Manager aÃ±ade notificaciÃ³n en `notifications.md`
3. Usuario abre Builder y dice "continÃºa"

### Handoff Builder â†’ Manager (con Quality Gates)
1. Builder cambia `execution_log.md` a `ðŸŸ£ READY_FOR_REVIEW`
2. Builder ejecuta `python .agent/agent_controller.py`
3. **Si tests pasan:** Manager recibe el turno
4. **Si tests fallan:** Builder ve errores y corrige

### EscalaciÃ³n Builder â†’ Manager
1. Builder documenta problema en `execution_log.md`
2. Builder aÃ±ade escalaciÃ³n a `review_queue.md`
3. Builder cambia estado a `ðŸŸ  BLOCKED`
4. Usuario abre Manager para resolver

---

## ðŸ’¡ Comandos Ãštiles

### Verificar Estado (ejecuta Quality Gates si aplica)
```bash
python .agent/agent_controller.py
```

### Saltar Quality Gates (para debugging)
```bash
python .agent/agent_controller.py --skip-gates
```

### Output en JSON
```bash
python .agent/agent_controller.py --json
```

### Output Ejemplo (v2.0)
```
ðŸ—ºï¸  Generando mapa del proyecto...

ðŸ›¡ï¸  Ejecutando Quality Gates automÃ¡ticos...
   ðŸ“‹ Ejecutando Ruff...
   ðŸ§ª Ejecutando Pytest...
   âœ… PASSED

============================================================
ðŸŒ€ SISTEMA MULTI-AGENTE v2.0 - ESTADO ACTUAL
============================================================

ðŸ§  **ROL ACTIVO:** MANAGER (Manager)
ðŸ“‹ **Plan:** WP-2025-001
ðŸ“Š **Estado Plan:** ðŸŸ¢ APPROVED
ðŸ“ **Estado Log:** ðŸŸ£ READY_FOR_REVIEW

ðŸš€ **MISIÃ“N:**
   Builder completÃ³ WP-2025-001. âœ… Quality Gates pasados. Revisa lÃ³gica.

ðŸ“‚ **CONTEXTO:**
   1. .agent/config/MANAGER_CONTEXT.md
   2. .agent/config/MANAGER_SKILLS.md
   3. .agent/workflows/manager_workflow.md
   4. .agent/context/project_map.md

------------------------------------------------------------
ðŸ’¡ MANAGER: Lee los archivos de contexto y ejecuta la misiÃ³n
============================================================
```

---

## âš ï¸ SoluciÃ³n de Problemas

### "No es mi turno"
- Ejecuta `agent_controller.py` para ver quiÃ©n debe actuar
- Abre el agente correcto

### "Estado UNKNOWN"
- Revisa que los archivos .md tengan el formato correcto
- Busca la lÃ­nea `**Estado:**` con el emoji correspondiente

### "uv no estÃ¡ instalado"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Quality Gates fallan pero quiero continuar"
```bash
python .agent/agent_controller.py --skip-gates
```
âš ï¸ Usar con precauciÃ³n - el Manager recibirÃ¡ cÃ³digo sin validar.

### "No hay directorio src/"
El Quality Gate requiere `src/`. CrÃ©alo o usa `--skip-gates`.

---

## ðŸ“‹ Tips para Uso Efectivo

1. **Siempre ejecuta el controller** al inicio de cada interacciÃ³n
2. **Respeta el sistema de turnos** - El controller sabe quiÃ©n debe actuar
3. **ConfÃ­a en los Quality Gates** - Si fallan, hay errores reales que corregir
4. **Usa los niveles de riesgo** - Escala temprano en tareas ðŸ”´
5. **Revisa el project_map** - Te da una foto actualizada del proyecto

---

## ðŸ“¦ Requisitos

- Python 3.10+
- `uv` instalado y en PATH
- `ruff` como dependencia dev (`uv add --dev ruff`)
- `pytest` como dependencia dev (`uv add --dev pytest`)

---

## ðŸ“š Lecciones Aprendidas

> Ver archivo completo: `docs/05-TROUBLESHOOTING.md`

### Errores Comunes a Evitar

| Error | Consecuencia | SoluciÃ³n |
|-------|--------------|----------|
| Solo verificar `src/` en ruff | Errores en `tests/` pasan desapercibidos | Usar `ruff check src/ tests/` |
| Aprobar sin verificar manualmente | Errores llegan a producciÃ³n | Seguir checklist completa |
| Confiar solo en el controller | El controller puede tener bugs | VerificaciÃ³n manual adicional |
| No leer todos los archivos modificados | CÃ³digo problemÃ¡tico pasa la revisiÃ³n | Revisar cada archivo listado |

### Checklist del Manager (Obligatoria)

Antes de aprobar cualquier trabajo:

```bash
# 1. Quality Gates automÃ¡ticos
python .agent/agent_controller.py

# 2. Linting COMPLETO (src/ + tests/)
uv run ruff check src/ tests/

# 3. Tests
uv run pytest tests/ -v
```

**Solo aprobar si TODO pasa.**

---

## ðŸ‘¤ Protocolo de Acciones de Usuario

### CuÃ¡ndo el Agente Solicita AcciÃ³n

Cuando el plan incluye una tarea ðŸ‘¤, el agente mostrarÃ¡:

```markdown
---
## ðŸ‘¤ ACCION REQUERIDA DEL USUARIO

### Archivo a crear
- **Nombre:** `credentials.json`
- **UbicaciÃ³n:** `privada/credentials.json`

### Contenido (copiar y pegar)
{contenido JSON/ENV para copiar}

### Campos a personalizar
{tabla con campos y valores}

### Pasos
1. Crear archivo en privada/
2. Personalizar con tus datos
3. Actualizar PRIVATE_REGISTRY.md
4. Confirmar al agente

### â³ Esperando confirmaciÃ³n...
---
```

### CÃ³mo Confirmar

DespuÃ©s de crear el archivo, escribir al agente:
```
He creado credentials.json en privada/ y actualizado PRIVATE_REGISTRY.md
```

### PRIVATE_REGISTRY.md

Este archivo en `.agent/templates/PRIVATE_REGISTRY.md` permite:
- Documentar quÃ© archivos existen en `privada/`
- Verificar que el usuario completÃ³ las tareas
- Los agentes lo leen para confirmar configuraciÃ³n

---

## ðŸ“„ Licencia

Libre para uso personal y comercial.

---

*Sistema Multi-Agente v5 - Con Arquitectura de Seguridad y Hooks Nativos*

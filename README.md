# z_scripts — Workspace de desarrollo

Directorio raíz de trabajo. Contiene herramientas Python de programación y gestión de proyectos con agentes IA.

El estado operacional (tickets, planes, memoria) vive en `.agent/`:
- Workspace activo: `z_scripts/.agent/collaboration/`
- Motor del sistema: `orquestador_de_agentes/`

---

## Proyectos

| Proyecto | Descripción | Docs |
|---|---|---|
| `orquestador_de_agentes/` | Motor multi-agente Manager/Builder portable. Gestiona el ciclo completo de implementación con control de calidad, memoria persistente y revisión automática. | [QUICKSTART](orquestador_de_agentes/QUICKSTART.md) · [README](orquestador_de_agentes/README.md) |

---

## Cómo arrancar

El motor es code-only. El workspace (tickets, estado, memoria) se apunta con `AGENT_PROJECT_ROOT`:

```powershell
# Trabajar en este workspace (desarrollo del motor)
$env:AGENT_PROJECT_ROOT = "C:\Users\fdl\Proyectos_Python\z_scripts"
python orquestador_de_agentes\.agent\agent_controller.py --validate

# Trabajar en un proyecto destino
$env:AGENT_PROJECT_ROOT = "C:\ruta\a\mi_proyecto"
python orquestador_de_agentes\.agent\agent_controller.py --validate
```

Para el flujo completo de desarrollo, leer: [QUICKSTART](orquestador_de_agentes/QUICKSTART.md)

---

## Estructura

```
z_scripts/
├── orquestador_de_agentes/   ← motor portable (code-only)
├── .agent/                   ← workspace de z_scripts (tickets, memoria, config)
│   ├── collaboration/        ← plans, work_plan.md, backlog.md
│   ├── runtime/memory/       ← observations.jsonl, MEMORY.md
│   └── config/               ← agents.json, motor_destination_link.json
└── README.md                 ← este archivo
```

Cada proyecto destino tiene su propio `.agent/` con la misma estructura.
El motor nunca se copia: se referencia externamente via `AGENT_PROJECT_ROOT`.

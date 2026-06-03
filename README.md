# orquestador_de_agentes_workspace

Repositorio destino de dogfooding del motor multi-agente Manager/Builder.

Funciona como cualquier `repo_destino` del motor, pero su carga principal son
tickets para mejorar el propio motor (`orquestador_de_agentes/`).

El estado operacional (tickets, planes, memoria) vive en `.agent/`:
- Estado activo: `.agent/collaboration/`
- Memoria del proyecto: `.agent/runtime/memory/`
- Motor externo: `orquestador_de_agentes/` (repo separado, enlazado via `motor_destination_link.json`)

---

## Topologia

```
C:\Users\fdl\Proyectos_Python\
├── orquestador_de_agentes\          ← repo_motor (fuente canonica, repo git propio)
└── orquestador_de_agentes_workspace\ ← repo_destino / este repo (repo git propio)
```

Regla: operaciones git del tooling corren en `repo_motor`. Estado de tickets vive aqui.

---

## Como arrancar

El motor es externo. El estado se configura via `motor_destination_link.json` (generado por el instalador):

```powershell
# Validar estado del sistema
python orquestador_de_agentes\.agent\agent_controller.py --validate --project-root .

# Sincronizar herramientas instaladas desde el motor
python scripts\install_agent_system.py --sync

# Vista previa del sync
python scripts\install_agent_system.py --sync --dry-run
```

Para el flujo completo de desarrollo con tickets, leer:
- `orquestador_de_agentes/QUICKSTART.md`
- `orquestador_de_agentes/INTERACTION_MODES.md`

---

## Estructura

```
orquestador_de_agentes_workspace\
├── .agent\                  ← estado operativo de este destino
│   ├── collaboration\       ← tickets, work_plan, STATE, TURN, backlog
│   ├── runtime\memory\      ← observaciones y memoria del proyecto
│   └── config\              ← config del destino (motor_destination_link gitignored)
├── agent_system\            ← copia instalada del framework (sincronizable)
├── scripts\                 ← utilidades instaladas del motor
├── skills\                  ← micro-habilidades instaladas del motor
├── tests\                   ← tests de este destino
└── .claude\                 ← config Claude Code (rules, settings)
```

---

## Vocabulario

| Termino | Descripcion |
|---------|-------------|
| `repo_motor` | `orquestador_de_agentes/` — motor portable, fuente canonica |
| `repo_destino` | Este repositorio — estado operativo del proyecto |
| `workspace_activo` | Raiz con `.agent/` desde la que corre el ticket (= este repo) |
| `entorno_multi_root` | IDE con ambos repos abiertos simultaneamente |

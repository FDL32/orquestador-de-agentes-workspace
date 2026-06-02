# Agent Runtime README

Este directorio contiene la superficie operativa portable del sistema de agentes
para este workspace. Los archivos de estado vivos estan bajo
`.agent/collaboration/`; la memoria persistente vive bajo `.agent/runtime/memory/`.

## Comandos requeridos

### Ejecutar tests de forma segura

```powershell
python scripts/run_pytest_safe.py
```

Usa este wrapper para lanzar la suite con las protecciones del proyecto en vez de
invocar `pytest` directamente desde flujos automatizados.

### Validar estado del sistema

```powershell
python .agent/agent_controller.py --validate
```

En Modelo B, cuando el controller vive en el motor portable, usa la ruta del motor
y pasa el workspace explicito:

```powershell
python orquestador_de_agentes/.agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\z_scripts
```

## Reglas de higiene

- No edites manualmente `review_queue.md`; la rotacion automatica offline vive en `session_closeout.py`.
- No cargues `events.jsonl`, `review_queue.md` ni `manager_feedback_*` completos en bootstrap.
- No escribas secretos, tokens ni rutas privadas en memoria persistente.

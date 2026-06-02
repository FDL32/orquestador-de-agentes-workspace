Ejecuta el siguiente comando y muestra el resultado interpretado:

```bash
python .agent/agent_controller.py
```

Si el comando falla (porque no estÃ¡s dentro de un proyecto con el sistema instalado), muestra en su lugar:

- El turno actual segÃºn `collaboration/TURN.md` si existe
- Las fases del `collaboration/work_plan.md` con su estado (completadas / pendientes)
- Cualquier notificaciÃ³n pendiente en `collaboration/notifications.md`

Interpreta el output: indica claramente quiÃ©n tiene el turno (Manager o Builder), quÃ© fase estÃ¡ activa y cuÃ¡l es el siguiente paso recomendado.


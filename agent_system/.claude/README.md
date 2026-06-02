# ConfiguraciÃ³n del Proyecto Agent System

## ðŸŽ¯ Al Iniciar SesiÃ³n

**OBLIGATORIO en cada mensaje:**

```bash
python .agent/agent_controller.py
```

Luego:
1. âœ… Si dice `ROL ACTIVO: [TU_ROL]` â†’ **Es tu turno, continÃºa**
2. âŒ Si dice `ROL ACTIVO: [OTRO_ROL]` â†’ **NO es tu turno, informa al usuario**

---

## ðŸŽ­ Identifica Tu Rol

### Manager
- **Leer**: `.agent_common_rules.md` + `.manager_rules`
- **Contexto**: `.agent/config/MANAGER_CONTEXT.md`
- **Archivo principal**: `work_plan.md`

### Builder
- **Leer**: `.agent_common_rules.md` + `.builder_rules`
- **Contexto**: `.agent/config/BUILDER_CONTEXT.md`
- **Archivo principal**: `execution_log.md`

---

## ðŸ“ Archivos Clave

| Archivo | PropÃ³sito | QuiÃ©n lo edita |
|---------|-----------|----------------|
| `.agent_common_rules.md` | Reglas comunes | Leer ambos |
| `.manager_rules` | Reglas del Manager | Leer Manager |
| `.builder_rules` | Reglas del Builder | Leer Builder |
| `work_plan.md` | Plan de trabajo | Manager escribe |
| `execution_log.md` | Log de ejecuciÃ³n | Builder escribe |
| `review_queue.md` | Escalaciones | Ambos |
| `notifications.md` | ComunicaciÃ³n | Ambos |
| `TURN.md` | Control de turno | Solo lectura |

---

## â±ï¸ LÃ­mites de SesiÃ³n

ðŸ›‘ **STOP si:**
- â° Llevas **>2 horas** en el mismo plan
- ðŸ“ Has tocado **>5 archivos** diferentes
- ðŸ”„ Has modificado el **mismo archivo >3 veces**

**Protocolo:**
```bash
python .agent/agent_controller.py --check-completion
```

Si >80% completo â†’ Terminar y entregar
Si <80% completo â†’ Documentar estado, commit WIP, cerrar sesiÃ³n

---

## ðŸ” Seguridad

```
proyecto/
â”œâ”€â”€ privada/              # â›” NUNCA acceder - Solo usuario
â”‚   â”œâ”€â”€ .env
â”‚   â””â”€â”€ credentials.json
â”‚
â””â”€â”€ publica/repo/         # âœ… Tu Ã¡rea de trabajo
    â”œâ”€â”€ .agent/
    â””â”€â”€ src/
```

**Tipos de tareas:**
- ðŸ¤– TAREA AGENTE â†’ Builder implementa directamente
- ðŸ‘¤ TAREA USUARIO â†’ Dar instrucciones y ESPERAR confirmaciÃ³n

---

## ðŸš€ Comandos Ãštiles

```bash
# Estado actual
python .agent/agent_controller.py

# Recuperar sesiÃ³n (>2h)
python .agent/agent_controller.py --recover

# Verificar completitud
python .agent/agent_controller.py --check-completion

# Modo estricto (CI/CD)
python .agent/agent_controller.py --strict

# Saltar Quality Gates (debug)
python .agent/agent_controller.py --skip-gates
```

---

## âš™ï¸ ConfiguraciÃ³n de este Proyecto

- **MÃ¡ximo archivos rastreados**: 10
- **LÃ­mite de sesiÃ³n**: 2 horas
- **Quality Gates**: ruff + pytest (automÃ¡ticos)
- **Hook System**: pre-action, post-tool (2-Action Rule), stop (Completion Verification)

---

*Sistema Multi-Agente v5 - Con Hook System, Quality Gates y Agentes Nativos*


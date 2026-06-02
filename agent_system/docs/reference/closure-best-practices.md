# Closure Best Practices â€” Reference Guide

CÃ³mo cerrar profesionalmente un proyecto sin crear overhead arquitectÃ³nico innecesario.

## Context

Tras completar fases de desarrollo (Fase 1, Fase 2, etc), un proyecto necesita:
- Documentar decisiones para auditorÃ­a futura
- Limpiar archivos temporales
- Mantener raÃ­z limpia y enfocada

**Reto:** Hacerlo sin crear overhead (`.agent/history/`, `PHASE*_LESSONS.md`, etc).

---

## âœ… Pattern: Simple & Auditable

### 1. MEMORY.md â€” Single Source of Truth

Archivo Ãºnico con lecciones arquitectÃ³nicas transversales.

**Contenido:**
```markdown
# z_scripts Memory â€” Lecciones ArquitectÃ³nicas v9.0+

## Decisiones Clave (Session April 2026)

### 1. Session Artifacts Pattern
**Decision:** Separar artifacts temporales (.session/) vs permanentes (PROJECT.md)
**Why:** Mantener raÃ­z limpia + preservar context entre sesiones
**Trade-off:**
- âœ… RaÃ­z limpia y enfocada
- âŒ Ciclo de vida complejo

### 2. [Decision Name]
...

## ValidaciÃ³n y Testing Methodology

**Critical Learning:** No confiar en builder claims.
**PatrÃ³n:** Grep â†’ Read â†’ Execute

## Stack Stability

**Python 3.10+ strict:**
- pathlib obligatorio
- typing explÃ­cito

## Recommendations for Phase 4+

[GuÃ­a para futuras sesiones]
```

**Ventajas:**
- âœ… Centralizado
- âœ… Institucional (futuras sesiones)
- âœ… Searchable (grep -n "Decision\|Trade-off\|Why")
- âœ… Escalable (agregar decisiones)

### 2. CHANGELOG.md â€” Decisiones + Bugs por VersiÃ³n

Cada versiÃ³n documenta decisiones clave y bugs encontrados.

**Estructura (v9.2 example):**
```markdown
## v9.2 - 2026-04-26 â€” Fase 3 Completada: Multi-Agent Skills Discovery

### Resumen Ejecutivo
v9.2 cierra Fase 3 con 5 tickets completados y sistema production-ready.

### Decisiones Clave

1. **Skill Executor Dual Mode** â€” Goose (external) + --skill (direct)
   - **Why:** MÃ¡xima flexibilidad sin forzar dependencia
   - **Trade-off:** Dos canales â†” AgnÃ³stico a runtime
   - **Reference:** CLAUDE.md secciÃ³n 3f

2. **Trigger_map AgnÃ³stico a Engine** â€” Goose + Claw comparten contexto
   - **Why:** Arquitectura escalable para N engines
   - **Trade-off:** Central dependency â†” DRY source of truth
   - **Reference:** CLAUDE.md secciÃ³n 3g

### Bugs Found & Fixed (VerificaciÃ³n Independiente)

| Bug | Ticket | SÃ­ntoma | Fix | Impact |
|-----|--------|---------|-----|--------|
| Recursive pytest | TICKET-001 | 217 "passed" falsos | Mock subprocess | 52 actual tests |
| Unicode â†’ | TICKET-004 | UnicodeEncodeError | ASCII -> | Windows compatible |

### ValidaciÃ³n Independent

- âœ… Grep â€” Verified changes exist
- âœ… Read â€” Verified correctness
- âœ… Execute â€” Verified functionality
```

**Ventajas:**
- âœ… Auditable (grep -n "Decisiones\|Bug")
- âœ… Escalable (cada versiÃ³n agrega secciones)
- âœ… Single source of truth (no duplicaciÃ³n)

---

## âŒ Anti-Patterns to Avoid

### 1. Over-Engineering HistÃ³rico

```
.agent/history/
  â”œâ”€ closed-tickets/
  â”‚   â”œâ”€ TICKET-001.md
  â”‚   â”œâ”€ TICKET-002.md
  â”‚   â””â”€ ...
  â””â”€ lessons/
      â””â”€ PHASE2_LESSONS.md
```

**Problema:**
- Overhead innecesario
- Duplica informaciÃ³n de CHANGELOG + git
- DifÃ­cil de mantener
- No escalable

**SoluciÃ³n:** Confiar en git + CHANGELOG

### 2. Duplicate MEMORY.md + PHASE*_LESSONS.md

```
PHASE2_LESSONS.md (400 lÃ­neas)
MEMORY.md (400 lÃ­neas)
```

**Problema:**
- InformaciÃ³n duplicada
- DifÃ­cil de mantener sincronizado
- Developer confundido: Â¿cuÃ¡l es la fuente de verdad?

**SoluciÃ³n:** Un Ãºnico archivo MEMORY.md

### 3. Mantener .session/_closed/

```
.session/_closed/
  â”œâ”€ TICKET-001.md
  â”œâ”€ TICKET-002.md
  â””â”€ ...
```

**Problema:**
- Datos histÃ³ricos en artifacts (no pertenece)
- Ocupan espacio en raÃ­z
- No es auditable (confÃ­a en tickets, no en CHANGELOG)

**SoluciÃ³n:** Eliminar. CHANGELOG es la auditorÃ­a.

---

## Implementation Checklist

Antes de cerrar fase:
```bash
# 1. Crear MEMORY.md
if [ ! -f MEMORY.md ]; then
  echo "# Lecciones ArquitectÃ³nicas" > MEMORY.md
fi

# 2. Mejorar CHANGELOG.md
# Agregar secciones:
# - ### Decisiones Clave
# - ### Bugs Found & Fixed
# - ### ValidaciÃ³n Independent

# 3. Identificar archivos temporales
find . -maxdepth 2 \( -name "PHASE*_LESSONS.md" -o -name "*TEMP*" -o -name "*draft*" \)

# 4. Limpiar
rm -f PHASE*_LESSONS.md
rm -rf .session/_closed/

# 5. Verificar
python -m pytest tests/ -q  # Debe pasar
```

---

## PatrÃ³n de AdopciÃ³n

Todos los nuevos proyectos heredan automÃ¡ticamente este protocolo via instalador:
```bash
python agent_system/scripts/install_agent_system.py /new/project
    â†“
Copia .agent/rules/common/closure-protocol.md automÃ¡ticamente
    â†“
Developer sigue protocolo al cerrar fases
```

---

## ValidaciÃ³n Post-Closure

```bash
# 1. MEMORY.md existe y tiene decisiones
grep -c "Decision\|Why\|Trade-off" MEMORY.md  # â‰¥ 5 lÃ­neas

# 2. CHANGELOG.md tiene secciones
grep -c "Decisiones Clave\|Bugs Found" CHANGELOG.md  # â‰¥ 2

# 3. No hay duplicaciÃ³n
test ! -f PHASE*_LESSONS.md && echo "âœ… No duplicaciÃ³n"

# 4. .session/ limpio
ls -la .session/ | grep -c "_closed" || echo "âœ… Clean"

# 5. Tests pasan
python -m pytest tests/ -q  # Debe pasar sin regresiones
```

---

## References

- Closure Protocol (rule) â€” `.agent/rules/common/closure-protocol.md`
- MEMORY.md â€” Lecciones arquitectÃ³nicas
- CHANGELOG.md â€” AuditorÃ­a versiÃ³n por versiÃ³n
- Git log â€” Trace de commits
- Grep â€” BÃºsqueda rÃ¡pida

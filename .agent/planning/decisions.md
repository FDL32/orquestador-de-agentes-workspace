# decisions.md -- WOT-2026-010d preparation

### DEC-010D-001 -- Autoridad de lectura del lifecycle de pausa/reanudacion

- **tier:** T1a
- **status:** accepted
- **decided_by:** user
- **options:** [A] bus como autoridad y markdown como proyeccion | [B] markdown como autoridad primaria
- **recommendation:** [A] porque la memoria `bus-first-read-authority` y el contrato de 010d exigen recuperacion cross-session sin drift.
- **evidence:** backlog WOT-2026-010d + observacion `obs-bus-read-01`
- **impact:** [B] permitiria reanudar con drift entre bus y proyecciones.
- **reversibility:** baja
- **invalidates:** T-010D-001 si se revierte; cualquier test de pause/resume basado en bus.
- **supersedes:** -
- **date:** 2026-06-16

---

### DEC-010D-002 -- Alcance v1: una sola pausa activa

- **tier:** T1a
- **status:** accepted
- **decided_by:** user
- **options:** [A] una pausa activa global en v1 | [B] pausas anidadas o multiples
- **recommendation:** [A] porque reduce blast radius en controller, bus, guardas y resume fail-closed.
- **evidence:** backlog WOT-2026-010d
- **impact:** [B] exige coordinacion adicional de ownership, merge y restauracion.
- **reversibility:** media
- **invalidates:** tests y criterios de "pausa unica" en T-010D-001.
- **supersedes:** -
- **date:** 2026-06-16

---

### DEC-010D-003 -- Mantener ACTIVE_TICKET durante la pausa

- **tier:** T1a
- **status:** accepted
- **decided_by:** user
- **options:** [A] conservar `ACTIVE_TICKET` y proyectar `STATUS: PAUSED` | [B] vaciar el ticket activo durante la pausa
- **recommendation:** [A] porque evita tickets zombie y preserva la trazabilidad del trabajo interrumpido.
- **evidence:** backlog WOT-2026-010d
- **impact:** [B] rompe las comprobaciones de handoff y la lectura del estado pausado.
- **reversibility:** baja
- **invalidates:** contrato de `paused/<ticket>.json`, tests de state projection y pre-handoff.
- **supersedes:** -
- **date:** 2026-06-16

---

### DEC-010D-004 -- Persistencia sin diff: `stash_ref=null`

- **tier:** T2
- **status:** accepted
- **decided_by:** agent-default
- **options:** [A] `stash_ref=null` cuando no hay diff | [B] crear stash vacio por simetria
- **recommendation:** [A] porque evita artefactos engañosos y mantiene el JSON semanticamente preciso.
- **evidence:** backlog WOT-2026-010d
- **impact:** [B] introduce ruido y una fuente falsa de restauracion.
- **reversibility:** alta
- **invalidates:** tests de no-stash y parsing de artefacto.
- **supersedes:** -
- **date:** 2026-06-16
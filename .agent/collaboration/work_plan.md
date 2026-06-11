# Work Plan: WT-2026-251a - Centralizar ticket-ID regex + prefijos 2-3 letras

## Metadata
- **ID:** WT-2026-251a
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Titulo:** Centralizar ticket-ID regex y extender a prefijos de 2-3 letras
- **Asignado a:** Builder

## Objetivo
Eliminar inline `(?:WP|WT)-` patterns dispersos en 8 modulos del motor.
Extender bus/ticket_id.py para soportar prefijos de 3 letras (WOT, CTL, etc.).
Asegurar int() safety en NUMERIC_SUFFIX_PATTERN y NEXT_TICKET_PATTERN.

## Decision Arquitectonica
`bus/ticket_id.py` es la unica autoridad para reconocer y construir IDs de
ticket. Los consumidores importan sus patrones y helpers en lugar de mantener
regex locales, de modo que ampliar el prefijo a 2-3 letras preserve una sola
semantica y una unica barrera de regresion.

## Non-goals
- No migrar el prefijo operativo del `repo_destino`; corresponde a
  `WT-2026-251b`.
- No cambiar el formato de ano, bloque numerico ni sufijo alfabetico.
- No modificar estados del bus ni semantica de cierre de tickets.

## Criterios de Exito
- [x] bus/ticket_id.py: NUMERIC_SUFFIX_PATTERN y NEXT_TICKET_PATTERN extended to 3-letter
- [x] 8 consumidores migrados a imports canonicos
- [x] bus/supervisor.py _next_ticket_id usa fullmatch para evitar partial match en sufijos alfa
- [x] tests/unit/test_migrated_ticket_patterns.py: cobertura 2-letter + 3-letter por modulo
- [x] tests/unit/test_no_inline_ticket_regex.py: test-barrera scanning inline patterns
- [x] 573 suite passes, ruff clean
- [x] Commit edbad61 en repo_motor

## Entregables
- Commit: edbad619ec157808fb870483ea7bba1d984a6bdd (WT-2026-251a)

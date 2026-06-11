# AUDIT_WT-2026-244a

## Riesgos Bloqueantes

### CRITICO - crear un gate nuevo en vez de endurecer el existente
Si el ticket introduce una capa nueva de "mergeability" paralela a
`validate --json`, duplica burocracia y contradice el audit base.

### ALTO - reverse-classical vuelve a quedar como regla universal
Si la politica no distingue bugfixes de tests de contrato/cobertura, reabre la
friccion que el propio audit ya habia corregido.

### ALTO - gate endurecido sin allowlist previa
Si el texto exige `0 warnings estructurales` sin dejar explicita la secuencia
`allowlist -> gate`, la politica queda subjetiva o se implementa al reves.

### ALTO - scope discipline y code quality quedan otra vez implicitos
Si la documentacion solo endurece `validate` pero no reconoce `Files Likely
Touched`, `non-goals` y convenciones del codebase como parte de mergeabilidad,
pierde dos ejes centrales de FrontierCode.

## TP Check

TP-01: `PROJECT.md` formaliza `validate --json` como gate de cierre existente, sin gate paralelo. Verificacion: existe una seccion durable en `PROJECT.md` que menciona `0 errors`, `0 warnings estructurales` y la secuencia `allowlist -> gate`.

TP-02: la regla `[NON-REVERSE-CLASSICAL: ...]` queda builder-facing y limitada a tests de contrato/cobertura. Verificacion: `AGENTS.md` contiene la etiqueta literal y la acota a casos donde no aplique reverse-classical por no ser bugfix.

TP-03: `BLOCKERS` y `NITS` quedan definidos con criterios binarios minimos. Verificacion: la documentacion enumera al menos fallos de `validate --json`, bugfix sin evidencia suficiente y `scope creep` como `BLOCKERS`, y legibilidad o refactors no necesarios como `NITS`.

TP-04: `scope discipline` y `code quality / conventions` aparecen explicitamente como parte del criterio de mergeabilidad. Verificacion: la documentacion menciona `Files Likely Touched`, `non-goals` y seguimiento de patrones del codebase o justificacion de patrones nuevos.

TP-05: `validate --json` del `repo_destino` queda sin errores. Verificacion: el comando canonico termina con `errors: {}`.

## Veredicto Previo

`APPROVED`

## Addendum - Auditoria Bus y Recuperacion

### Checklist complementario del framework

- `§6 CHANGES`: no aplica en esta incidencia concreta, porque el ciclo termino en
  `INSPECT` y escalo a `HUMAN_GATE`; no hubo una transicion canonica
  `REVIEW_DECISION=CHANGES` que auditar en este ticket.
- `Idle timeout`: no es calculable de forma estricta por la inversion temporal
  observada entre `seq 1052` y eventos posteriores, pero las senales
  indirectas apuntan a idle timeout probable:
  - `supervisor_lock.txt` ausente tras el ciclo;
  - no hay `SUPERVISOR_RESTARTED` entre `seq 1052` y `seq 1072`;
  - la transicion a `READY_FOR_REVIEW` usa `source=mark-ready`.
- `Requeue claims`: no existe claim activo para `WT-2026-244a`, pero el
  directorio `.agent/runtime/requeue_claims/` conserva claims stale de tickets
  anteriores (`WT-2026-193`, `WT-2026-198`, `WT-2026-203`, `WT-2026-205`,
  `WT-2026-221b`, `WT-2026-224a`, `WT-2026-225a`, `WT-2026-232a`,
  `WT-2026-234a`, `WT-2026-235a`, `WT-2026-236a`). No bloquearon este ciclo,
  pero conviene tratarlos como deuda operativa porque podrian interferir en
  supresiones de requeue futuras si el consumo durable vuelve a degradarse.

### Lectura consolidada

La recuperacion del ticket sigue siendo `RECUPERABLE` con confianza `ALTA`. La
parte no resuelta no es drift del bus, sino cierre operativo incompleto del
ciclo `INSPECT -> HUMAN_GATE`, mas la deuda lateral de claims stale que el
framework recomienda vigilar aunque no pertenezcan al ticket activo.

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

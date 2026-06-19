# STRATEGY_WOT-2026-011c.md

## Enfoque

`011c` no arregla nada: explica el origen. El trabajo se centra en observar
bytes, historia git y rutas reales de escritura sobre `.agent/collaboration/`
para separar tres capas: sintoma actual, writer concreto y mecanismo de
inyeccion. En cuanto eso quede demostrado, el spike se detiene.

## Fase 0 - Baseline verificable

1. Medir con bytes el subconjunto con BOM en working tree y sin BOM en HEAD.
2. Confirmar que `HEAD:backlog.md` ya contiene los 3 control chars historicos.
3. Registrar en `execution_log.md` los comandos exactos y el baseline.

## Fase 1 - Trazado de escritores

1. Inspeccionar rutas de escritura relevantes (`launch_agent_terminals.ps1`,
   hooks, controller, proyecciones) SIN modificarlas.
2. Correlacionar cada writer con el patron observado: BOM recurrente,
   superficies afectadas y superficies no afectadas.
3. Si el host parece determinante, probarlo con evidencia observacional,
   no con cambio de codigo.

## Fase 2 - Reporte y parada

1. Escribir `bom_source_audit_WOT-2026-011c.md` con hallazgos separados por
   `VERIFICADO` / `INFERENCIA RAZONABLE`.
2. Proponer el follow-up de fix, si procede.
3. Ejecutar encoding guard sobre el reporte y `validate` final.
4. Parar sin intentar fix.

## Riesgos a vigilar

- Convertir el spike en fix encubierto.
- Confundir un sintoma de host con un bug de negocio del repo.
- Presentar una hipotesis probable como fuente confirmada.
- Tocar superficies vivas para esconder el sintoma en vez de explicarlo.

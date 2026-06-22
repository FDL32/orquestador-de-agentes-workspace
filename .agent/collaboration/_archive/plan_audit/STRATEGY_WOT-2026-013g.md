# STRATEGY_WOT-2026-013g -- Diagnostico reproducible de `test_upgrade_path_suggestion`

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `010j` y `010p` ya midieron a `test_upgrade_path_suggestion` como outlier de ~59-70s.
- `013e` lo dejo explicitamente como `unknown` y follow-up analitico, no como fix de codigo.
- El cuerpo visible del test es trivial; la hipotesis de coste debe probarse con medicion y no con lectura superficial.
- El deliverable del ticket es documental (`analysis`), no diff de codigo.

## Plan tecnico

1. Releer la evidencia previa durable:
   - `docs/test_performance/test_performance_baseline.md`
   - `docs/test_performance/test_performance_variance.md`
   - `docs/test_performance/test_suite_audit_WOT-2026-013e.md`
2. Releer el test focal y su contexto inmediato:
   - `tests/unit/test_detect_version.py`
3. Medir en foreground, con comandos reproducibles y comparables, por ejemplo:
   - archivo completo `tests/unit/test_detect_version.py`
   - test focal `tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion`
   - si hace falta, clase completa `TestVersionDetection`
4. Separar en el reporte:
   - [V] hechos medidos (duraciones, patron de atribucion, orden relativo)
   - [I] inferencias sobre setup de clase/modulo, import-time o escaneo indirecto
5. Redactar el reporte durable en `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` con una conclusion binaria:
   - optimizacion local sugerida, o
   - `sin optimizacion segura` con evidencia suficiente
6. Cerrar `execution_log.md` con la linea contractual de artefacto + validate.

## Riesgos y antidotos

- **Convertir analisis en fix prematuro:** mantener `tests/unit/test_detect_version.py` y producto en `Forbidden Surfaces`.
- **Confundir output historico con evidencia fresca:** usar 010j/010p como baseline, no como sustituto de medicion actual.
- **Inferencia presentada como hecho:** etiquetar cada conclusion sustantiva como [V] o [I].
- **Ruido de background:** medir en foreground y registrar comandos exactos.

## No hacer

- No editar el test ni producto.
- No proponer optimizacion sin una atribucion razonablemente reproducible.
- No presentar pytest focal verde como cierre canonico del ticket; el gate final sigue siendo reporte + validate.

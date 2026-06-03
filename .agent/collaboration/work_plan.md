# Work Ticket - WT-2026-208

## Metadata
- **ID:** WT-2026-208
- **Title:** Estabilizacion de suite global tras transicion workspace+motor
- **Scope:** system/testing
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-211

## Problema
La suite global del motor dejo de ser una senal fiable tras la transicion a workspace+motor.
La evidencia actual combina varias familias distintas: rutas stale a `z_scripts`, tests que
renombran `.agent` real del repo en Windows, assets limpios del motor que ya no existen,
drift de semantica en estado/cierre, mojibake y tests de integracion con fixtures/copias
que asumian otra topologia.

El riesgo principal de este ticket no es solo tecnico sino metodologico: intentar bajar el
contador de fallos con parches rapidos, skips amplios o ajustes locales que tapan sintomas
sin corregir el contrato real del sistema.

## Decision Arquitectonica
- La suite global NO se trata como un unico bloque opaco; se trabaja por familias de fallos.
- El Builder debe avanzar de forma secuencial, cerrando una familia antes de abrir la siguiente.
- Cada fix debe empujar el contrato objetivo de workspace+motor; no reintroducir rutas o
  heuristicas legacy solo para poner tests en verde.
- No promover hotfixes como solucion estable si no dejan clara la deuda estructural o el
  ticket hijo que la absorberia.
- Los re-runs completos de la suite sirven como verificacion de convergencia, no como unica
  herramienta de diagnostico.
- Si una pasada deja dudas sobre causalidad o mezcla dos familias, el Builder debe cerrar esa pasada
  con evidencia y abrir una nueva, no seguir encadenando fixes opacos.

## Non-goals
- No arreglar el ticket con `skip`, `xfail` o relajacion de asserts sin causa raiz verificada.
- No parchear codigo productivo con rutas `z_scripts` o supuestos de repo anidado.
- No mezclar en este ticket una barrida completa de nomenclatura historica (`WT-2026-209`).
- No convertir `discover_skills.py` ni otros cambios sueltos no relacionados en parte del scope.

## Fases
### Fase 0: Baseline e inventario
- Reproducir la suite global desde el motor con comando canonico.
- Agrupar fallos por familias y fijar un baseline inicial con recuento y modulos afectados.
- Confirmar que los fallos actuales siguen encajando en las familias ya observadas.

### Fase 1: Paths, roots y assets faltantes
- Corregir tests y helpers que asumen rutas stale (`z_scripts`) o topologia previa.
- Corregir referencias a assets/archivos que ya no forman parte del motor limpio.
- Cerrar primero la familia de `run_llm_evals`, rutas del controller y tests que dependen del repo antiguo.

### Fase 2: Manipulacion de `.agent` real y permisos Windows
- Sustituir patrones de rename/hide sobre `.agent` real del repo por sandboxes/copias seguras.
- El objetivo es que los tests no dependan de renombrar superficies reales ni de permisos inestables.

### Fase 3: Drift de semantica en estado y closeout
- Revisar tests que fallan porque el contrato del sistema cambio de verdad.
- Ajustar codigo o tests segun el contrato canonico actual, no segun expectativas legacy.

### Fase 4: Encoding y superficies mojibake
- Corregir archivos o expectativas de tests donde haya mojibake real.
- No tocar contenido historico fuera del scope salvo que rompa una superficie operativa o un test vigente.

### Fase 5: Convergencia y segunda pasada
- Reejecutar la suite global.
- Si aun quedan familias accionables, hacer una segunda pasada secuencial y cerrar otra familia completa.
- Si la segunda pasada descubre una subfamilia distinta, abrir una tercera pasada breve antes del cierre.
- No marcar READY_FOR_REVIEW mientras quede una familia entera claramente abordable dentro del scope.

### Fase 6: Cierre con residuals explicitados
- Reejecutar la suite completa y los subconjuntos tocados.
- Si quedara algun residual, debe quedar clasificado: regresion real, deuda separada o bloqueo externo.
- Actualizar backlog/CHANGELOG si se deriva deuda nueva o se absorbe deuda previa.

## Files / surfaces likely touched
### Code / tests expected
- `tests/`
- `tests/unit/`
- `runtime/`
- `scripts/`

### Documentation / control surfaces
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-208.md`
- `.agent/collaboration/AUDIT_WT-2026-208.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Calidad
- Comando baseline/final de suite global en el motor:
  - `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests -q`
- Comando de ruff para superficies tocadas:
  - `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check <files>`
- Verificacion minima por pasada:
  - re-run del subconjunto tocado;
  - recuento actualizado de la familia;
  - nota corta de por que el fix corrige contrato y no solo sintoma.
- Prohibido cerrar el ticket sin al menos un re-run completo de `pytest tests -q` al final.

## TP Check
TP-01: existe baseline inicial de la suite con familias agrupadas, no solo una lista plana de fallos.
TP-02: al menos una primera pasada cierra por completo una familia coherente de fallos.
TP-03: no se introducen rutas legacy ni parches de corto plazo sin contrato claro.
TP-04: los tests que manipulaban `.agent` real dejan de depender de renames/permisos fragiles del repo vivo.
TP-05: los fallos de paths/assets se alinean con la topologia workspace+motor actual.
TP-06: la suite completa se reejecuta y su resultado final queda documentado con evidencia.
TP-07: cualquier residual queda clasificado y documentado, no escondido bajo skips amplios.

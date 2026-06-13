# AUDIT WOT-2026-002a - Demo de clone limpio post-A2d

## Objetivo del audit
Verificar que el demo prueba CAPACIDAD real (el destino opera sin las copias legacy
usando el motor externo), con exit codes reales, sin tocar el destino real ni el motor,
y que cualquier dependencia detectada se documenta en vez de ocultarse.

## Reglas de revision
- Revisar exit codes reales en el reporte, no el relato del Builder.
- Confirmar que el "stripping" se hizo en el CLONE, no en el destino real.
- Confirmar que las invocaciones usan el motor externo, no las copias del clone.
- Confirmar que el destino real quedo intacto salvo el reporte, y el motor limpio.

## Hallazgos bloqueantes tipicos
- CRITICO: el demo modifica el destino real (git status del destino con cambios fuera de reports/).
- CRITICO: el demo toca el motor (check_motor_pristine sucio).
- CRITICO: se reporta "pasa" sin exit codes reales (relato, no evidencia).
- ALTO: pytest contra el clone colecciona 0 tests y se declara verde vacuo.
- ALTO: install --sync falla sin las copias y se cierra igual (falso des-riesgo de A2d).
- MEDIO: las herramientas se invocan desde las copias del clone, no desde el motor (no prueba host-extends).

## Evidencia minima esperada
- Tabla en el reporte: comando exacto | exit code | artefacto.
- `git -C <destino real> status --short` antes/despues: sin cambios salvo reports/.
- `check_motor_pristine --check` JSON: motor limpio, HEAD sin cambios.
- `motor_destination_link.json` del clone tras install (contenido o exit code del install).
- validate del destino real 0/0.

## TP Check
TP-01: el clone se creo en ruta temporal y el destino real no se modifico (salvo reports/). (git status)
TP-02: las copias legacy se retiraron en el CLONE para simular post-A2d. (log del demo)
TP-03: install --sync corrio con exit code real; link regenerado o fallo documentado. (exit code)
TP-04: discover_skills / run_pytest_safe / validate corrieron contra el clone via motor externo con exit codes reales. (exit codes)
TP-05: pytest no es verde vacuo (coleccion real reportada). (salida pytest)
TP-06: el motor quedo intacto (`check_motor_pristine --check`) y el destino real 0/0. (report + validate)
TP-07: cada claim del reporte tiene etiqueta de evidencia con artefacto concreto. (reporte)

## Criterio de rechazo inmediato
- El demo mutó el destino real o el motor.
- No hay exit codes reales que respalden los criterios.
- Se declaro A2d des-riesgado pese a un fallo de install/herramienta sin documentar.
- pytest verde por coleccion vacia presentado como prueba de capacidad.

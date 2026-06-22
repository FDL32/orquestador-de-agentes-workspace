# 07 - Pasada adversarial

## Bloque de cabecera

- **Scope:** claims `VERIFICADO` / `INFERIDO` / `NO VERIFICADO`
- **Repo motor (HEAD):** `f48191f6983f58ceeeef75b1401acf66d5620fc3`
- **Repo destino (HEAD):** `935907c38cd6456ba42e6e63a1462c82c4e77647`
- **Fecha:** `2026-06-22 16:49`
- **Comandos ejecutados:** ver `00_scope.md` y `findings.json`
- **Cobertura declarada:** Pasada B humana sobre collector output + git + validate + session-close
- **Limitaciones:** no se reejecuto `run_pytest_safe.py` manualmente fuera del collector

## Claims re-derivados

1. `El cierre de sesion fue canonico y verde real.`
   - Resultado: `VERIFICADO EN DOCUMENTACION` y `VERIFICADO EN BUS`
   - Evidencia: `session_close_report.md` = `Overall: PASS`; `validate` final `0/0` despues de `reconcile_ticket.py`.

2. `El bus_drift post-close era transitorio, no deuda persistente.`
   - Resultado: `VERIFICADO EN BUS`
   - Evidencia: warning observado tras el archive, luego desaparecido tras reconciliacion canonica y nueva validacion.

3. `El motor quedo limpio y sincronizado.`
   - Resultado: `VERIFICADO EN GIT`
   - Evidencia: `git -C <motor> status -sb` -> `## main...origin/main`.

4. `El destino esta sano; lo unico pendiente es commitear artefactos de esta pasada.`
   - Resultado: `VERIFICADO EN GIT`
   - Evidencia: dirty tree acotado a `INDEX.md`, memoria consolidada y `general_audit_20260622_1449/`.

5. `La carpeta nueva de auditoria es publicable tal cual.`
   - Resultado: `NO VERIFICADO`
   - Evidencia adversarial: `classify_publication.py` bloquea el repo completo por findings historicos ajenos. La carpeta nueva parece texto inocuo, pero el gate global no permite afirmar publicabilidad total sin lectura manual adicional o clasificacion por ruta.

## Falso verde / root equivocado / drift

- No se detecto falso verde del cierre: el PASS del reporte se contrasto contra `validate 0/0` vivo.
- Se descarto root equivocado: todos los comandos operativos usaron `--project-root <destino>`.
- Se descarto drift persistente del bus: el warning intermedio desaparecio por la via canonica prevista.

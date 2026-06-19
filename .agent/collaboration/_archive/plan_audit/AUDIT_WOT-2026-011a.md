# AUDIT_WOT-2026-011a.md

## Checklist de aceptacion

- [ ] `--session-close` detecta el estado `archive_rename_uncommitted` en el
      mismo cierre que lo genera, no en el ticket siguiente.
- [ ] La deteccion reutiliza la barrera canonica existente o una extension
      estrictamente compatible; no crea una segunda fuente de verdad divergente.
- [ ] El fallo del closeout nombra origen, destino y el comando exacto de
      reconcile (`git add -- ... && git commit -m "chore: reconcile archival rename"`).
- [ ] El ticket no introduce auto-commit del archivador ni borrado destructivo
      de artefactos archivados.
- [ ] Existe una prueba de regresion que falla sin el fix y pasa con el fix en
      la ruta real de `session_closeout` o `closeout_steps/archival`.
- [ ] `ruff`, tests focales, `run_pytest_safe` y `validate` quedan verdes.

## TP Check

- TP-01: verificado - el ticket ataca una sola brecha: el closeout deja pasar
  el limbo aunque `010u` ya lo detecta mas tarde.
- TP-02: verificado - la barrera binaria se puede observar con `session-close`,
  `pytest`, `ruff` y `validate`.
- TP-03: verificado - el scope productivo se concentra en closeout/runtime y
  tests asociados; no hay rediseno de politica global.
- TP-04: verificado - el criterio de salida no acepta "warn aceptable": el
  closeout debe fallar cerrado o reconciliar auditablemente.
- TP-05: verificado - `work_plan`, `STRATEGY` y este `AUDIT` comparten el
  mismo contrato: detectar en el punto de mutacion, sin auto-commit.

## Anti-patrones a rechazar

- Convertir `011a` en un auto-commit silencioso del archivador.
- Resolver el sintoma solo en `validate` o `pre_handoff_guard` otra vez.
- Sustituir el diagnostico especifico por un simple `dirty tree` o `git clean`.
- Tocar bus/runtime events manualmente para aparentar un cierre limpio.
- Reconciliar deletes historicos a mano dentro del test en vez de probar la
  ruta real de closeout.

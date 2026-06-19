# AUDIT_WOT-2026-012a.md

## Checklist de aceptacion

- [ ] `backlog.md` activo queda como cola viva y deja de mezclar estados
      terminales con trabajo operativo.
- [ ] La tabla activa es parseable y contiene `Reactivation` como columna
      obligatoria del schema.
- [ ] `Reactivation` usa `-` solo donde el contrato lo permite; `deferred` y
      `completed-partial` declaran trigger estructurado valido.
- [ ] El historico se mueve por bloques logicos auditables y conserva integra la
      seccion `### WOT-2026-012a`.
- [ ] Existe snapshot pre-corte y evidencia mecanica del movimiento
      (conteo de filas terminales y fichas `###` movidas).
- [ ] La decision `011e <-> 010m` permanece resuelta como
      `keep-both-with-boundary` sin reabrir el alcance CI dentro de `011e`.
- [ ] `python scripts/check_encoding_guard.py` y
      `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
      quedan verdes.

## TP Check

- TP-01: verificado - el ticket ataca una sola brecha: backlog vivo mezclado
  con historico y formato no suficientemente parseable.
- TP-02: verificado - el resultado es observable por diff, snapshot,
  conteos antes/despues y `validate`.
- TP-03: verificado - el scope productivo queda en `repo_destino`; el gate en
  `repo_motor` se difiere a `012b`.
- TP-04: verificado - el contrato falla cerrado si el corte exige tocar el
  archivador del closeout o si la semantica depende de HTML comments.
- TP-05: verificado - `work_plan`, `STRATEGY` y este `AUDIT` comparten el mismo
  contrato: formato primero, gate despues.

## Anti-patrones a rechazar

- Convertir `012a` en un cambio de runtime (`session-close`, `mark-ready`,
  archivador, bus).
- Hacer el corte del historico linea a linea sin bloques logicos.
- Aceptar `Reactivation` vaga o semiestructurada solo para "pasar" la tabla.
- Borrar fichas `###` sin evidencia de a donde fueron.
- Reescribir la decision `011e <-> 010m` en pleno ticket sin abrir contrato
  nuevo.

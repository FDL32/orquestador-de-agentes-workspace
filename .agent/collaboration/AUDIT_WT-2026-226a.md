# AUDIT WT-2026-226a

## Veredicto esperado
Bloquear implementaciones que creen un segundo gate paralelo o permitan al
review packet producir `empty review diff` con commit valido del ticket en
`repo_motor`.

## Hallazgos bloqueantes a vigilar

### CRITICO - Se duplica el gate en vez de unificar evidencia
- Bloquea la introduccion de otra barrera independiente no consumida por
  `mark-ready` y por el review packet.
- Bloquea tambien alojar el helper compartido en `.agent/`, porque el bridge no
  debe importar ni subprocesar el controller para resolver evidencia.
- Bloquea alojarlo en `bus/utils.py`, porque ese modulo esta reservado a helpers
  puros sin estado ni I/O.

### CRITICO - Helper fuera de bus/evidence.py
- Bloquea la entrega si el seam compartido de evidencia no vive en
  `bus/evidence.py`.

### CRITICO - Commits del ticket siguen ocultos por working tree sucio
- Bloquea un `_get_motor_diff_files` o reemplazo que hace early-return y deja de
  mirar commits recientes del ticket con working tree sucio.

### ALTO - No hay test de regresion del caso 225a
- Bloquea la entrega sin test con commit del ticket en `repo_motor` y working
  tree sucio simultaneo.

### ALTO - No hay paridad entre consumidores
- Bloquea la entrega cuando `mark-ready` y review packet siguen usando criterios
  distintos para decidir evidencia productiva.

### MEDIO - Camino bus-context-null sin diagnostico
- Exigir diagnostico explicito: el reason string de `WT-2026-225a` apunta al
  camino diff-seam como inferencia razonable. El camino `bus-context-null` en
  `classify_review_packet` debe quedar registrado como deuda si no se aborda.

### MEDIO - Shape de evidencia sin separacion motor/destino
- Bloquea regresiones de clasificacion del bridge: la evidencia debe exponer
  `motor_files` y `destination_files` separados, ademas de
  `has_productive_evidence`.

### BAJO - Fixture git irreal
- Exigir repos git reales en `tmp_path` siguiendo el patron `init_git_repo` de
  `tests/test_pre_handoff_guard.py`; no mockear subprocess de git.

### MEDIO - Scope creep hacia rounds o locks
- Marcar cambios en `builder_lock`, relaunch, `_builder_alive()` o nomenclatura
  como fuera de scope salvo justificacion explicita.

## TP Check
TP-01: diagnostico identifica las rutas reales de evidencia en controller y
bridge.
TP-02: existe seam compartido en `bus/evidence.py` para resolver evidencia del
ticket.
TP-03: commits recientes del ticket en `repo_motor` se incluyen aunque el
working tree este sucio.
TP-04: `mark-ready` y review packet coinciden semanticamente para el mismo
fixture (`has_productive_evidence` True/False).
TP-05: caso sin diff ni commit verificable sigue bloqueado/rechazado.
TP-06: packet no produce `empty review diff` cuando existe evidencia valida del
ticket.
TP-07: sin scope creep hacia rounds, locks, relaunch o nomenclatura.

## Evidencia requerida para aprobar
- `git show` o diff equivalente del `repo_motor` con archivos productivos del
  ticket;
- tests focales con nombres visibles;
- tests anadidos en `tests/test_agent_controller.py` y
  `tests/test_review_bridge.py`;
- tests con repos git reales en `tmp_path`, sin mockear subprocess de git;
- `ruff check` sobre archivos Python tocados;
- `agent_controller.py --validate --json --project-root <repo_destino>` con 0
  errores y 0 warnings;
- `execution_log.md` con comandos exactos y resultados.

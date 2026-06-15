# 03 - Auditoria de integracion motor+destino

## Bloque de cabecera

- **Scope:** integracion motor+destino, gates cruzados, host-extends, CI
- **Fecha auditada:** 20260615_2141
- **Auditor:** Claude Sonnet 4.6, doble pasada adversarial

---

## Pasada A — Verificacion determinista

### A1. motor_destination_link.json

- El destino tiene .agent/config/motor_destination_link.json apuntando al motor.
- check_destino_publish_ready.py resuelve el motor desde este link cuando --motor-root se omite.
- Test test_resolves_motor_from_link_json verifica esta ruta.
- Veredicto: VERIFICADO (via tests).

### A2. guard_paths hook — integracion cruzada

- .claude/settings.json del destino tiene el hook portable que resuelve guard_paths.py del motor via motor_destination_link.json.
- Si el link no existe o el motor no resuelve, el hook falla cerrado (exit 2).
- Verificado en WOT-2026-003b (cd0ecfb): cwd=destino, fail-closed.
- Veredicto: VERIFICADO.

### A3. CI del destino (quality-gates.yml)

- El workflow corre validate-state (agent_controller --validate) via checkout del motor.
- WOT-2026-003f: corre check_claude_settings_portability.py contra .claude/settings.json.
- No depende de scripts/ ni tests/ locales del destino (host-extends).
- Veredicto: VERIFICADO (via commits de sesion anterior).

### A4. Gate pre-push (check_destino_publish_ready.py)

- Nuevo en 009f. Exit 0=publicable, exit 1=drift bloquea, exit 2=APPROVED avisa, exit 3=error config.
- 8 tests cubren los cuatro casos: drift, APPROVED, READY_FOR_REVIEW, COMPLETED, motor-missing, validate-error, link-json.
- Documentado en orchestrator_pipeline.md con snippet CI.
- Veredicto: VERIFICADO.

### A5. Validate cruzado (motor valida destino)

- raw/validate_destino.txt: agent_controller.py del motor corre con --project-root=destino.
- Exit 0, 0/0. Los manifests se leen desde el destino; el codigo validador viene del motor.
- Veredicto: VERIFICADO.

---

## Pasada B — Refutacion adversarial

### B1. check_destino_publish_ready.py en CI — esta en el workflow?

El gate existe y tiene tests, pero no se verifico en esta sesion si ya esta integrado
en .github/workflows/quality-gates.yml del destino.
El prompt orchestrator_pipeline.md incluye el snippet de CI pero es documental.
Si el workflow no tiene el paso, el gate no corre en CI automatico.
Veredicto: NO VERIFICADO — recomendacion: verificar integracion en quality-gates.yml.

### B2. guard_paths cwd hardening — funciona en este contexto?

La sesion demostro que el hook funciona correctamente: bloqueo writes desde motor cwd
(error guard_paths: fuera del repo). El hook falla cerrado como se espera.
Veredicto: VERIFICADO empiricamente en esta sesion.

### B3. Suite de integracion motor+destino

No existe una suite de tests de integracion cruzada (motor corriendo contra destino real).
Los tests de 009f usan stubs (patch.object) en vez del controlador real.
El comportamiento real de la integracion se verifica via validate + manual run, no via CI automatico.
Veredicto: GAP CONOCIDO. No es nuevo; la integracion se verifica en cada ticket via validate.

### B4. FLT parser consolidacion (009d) — consumidores alineados?

Los tres consumidores (motor_checkpoint.py, pip_audit_policy.py, graph_context.py) delegaron
a scope_gate.parse_flt_raw_buckets. Los 64 tests focales cubrieron FLT plano y namespaced.
No se verifico via re-ejecucion en el momento del audit (last-run.json no encontrado en motor).
El estado del repo es coherente (commit 43e80bb, motor limpio).
Veredicto: INFERIDO-POSITIVO.

### B5. Reciprocal isolation guards (009c) — efectivos?

check_cross_root_contamination en scope_gate.py detecta archivos productivos en repo no-authority.
8 tests en test_scope_gate_isolation.py cubren los casos. Motor commit a020afd.
El guard en destino cierra el otro extremo (destino no escribe en motor salvo si es authority).
Veredicto: VERIFICADO via tests y commit.

---

## Resumen integracion

| Area | Estado | Notas |
|------|--------|-------|
| motor_destination_link.json | VERIFICADO | Resolucion automatica funcionando |
| guard_paths cruzado | VERIFICADO | Fail-closed empiricamente confirmado |
| CI destino | VERIFICADO | validate-state + settings portability |
| Gate pre-push en CI | NO VERIFICADO | Snippet en docs; integracion en workflow pendiente de verificar |
| FLT parser 009d | INFERIDO-POSITIVO | Commit limpio, tests 64/64 en execution_log |
| Reciprocal isolation 009c | VERIFICADO | 8 tests + commit a020afd |
| Suite integracion cruzada | GAP CONOCIDO | Solo stubs, no integration tests reales |
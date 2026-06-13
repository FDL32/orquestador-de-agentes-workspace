# PLAN WOT-2026-002b - Decision de los 10 huerfanos

## Objetivo
Espejo tecnico de `work_plan.md`. Por cada huerfano, reunir evidencia de invocacion
viva (motor + destino) y emitir decision: promote-to-motor / destino-keep /
archive-legacy. Entregable: doc de decisiones. No mueve ni borra nada.

## Pasos de ejecucion
1. Leer `.agent/docs/triage_manifest.md` (notas preliminares del bucket huerfano).
2. Para cada uno de los 10 huerfanos, en este orden:
   - grep del basename (sin extension y con ella) en el DESTINO:
     `git -C <destino> grep -n <basename>` y en CI/.github, prompts, skills, hooks.
   - grep del basename en el MOTOR:
     `git -C <motor> grep -n <basename>` (confirmar ausencia de equivalente).
   - Para scripts: comprobar si algun entrypoint vivo (CI, otro script, skill,
     agent_controller) los invoca. Para docs/hooks: si algun wiring los carga.
   - Clasificar segun rubrica congelada (dominio vs tooling vs muerto).
3. Casos con nota especifica:
   - `state_drift.py`: el triage dice que su rol vive en `agent_controller --validate`.
     Confirmar si hay invocacion viva; si no, candidato a archive (superado).
   - `test_ticket_007_context_recovery.py`: confirmar si el feature/experimento existe
     vivo en el destino. Si no hay ni feature ni invocacion -> no es dominio real.
   - `.goosehints`: deprecado WT-2026-254a -> archive con cita.
   - `pre_compact_hook.py`: confirmar si hay wiring de pre-compact que lo cargue en el
     destino (framework generico -> motor; integracion host -> keep).
4. Escribir `.agent/docs/orphans_decision_WOT-2026-002b.md` con la tabla de decisiones
   y la lista de barreras para A2d (los que NO se pueden archivar sin reconciliar).
5. Cierre: validate 0/0, encoding guard, commit en el destino con `WOT-2026-002b`.

## Seams / invariantes
- analysis: NO se mueve ni borra ningun huerfano (eso es A2d).
- Equivalencia funcional, no por basename.
- "sin hits" debe ser sin hits en motor Y destino (citar ambos).

## Evidencia esperada
- Por huerfano: lineas de grep (archivo:linea) o "sin hits en motor ni destino".
- Decision con la rubrica aplicada y la determinacion de dominio.
- validate 0/0.

## STOP
- Huerfano que resulta dominio real del destino -> destino-keep, corrige "dominio
  vacio" del manifiesto. Es hallazgo, no fallo.
- Huerfano con invocacion viva sin equivalente en motor -> no archivar; barrera A2d.
- Evidencia ambigua -> `dudoso` + decision conservadora (no archivar).

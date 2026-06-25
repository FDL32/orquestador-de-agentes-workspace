# Execution Log -- WOT-2026-013r

**Estado:** READY_FOR_REVIEW

## Bootstrap operativo -- WOT-2026-013r

Ticket NUEVO activado para cerrar el falso verde de `tests/unit/test_upgrade.py`
descrito en FP-012, sin tocar todavia el flujo de upgrade ni la memoria portable.

Procedencia (VERIFICADO 2026-06-25):
- `WOT-2026-013s` ya cerro canonico en `COMPLETED` y desbloqueo este sucesor.
- El packet canonico de `013r` vive en
  `.agent/planning/work_plan_WOT-2026-013r.md`.
- La cola viva conserva `013r` como siguiente ticket de alta prioridad en la
  familia 013.

Bus: pendiente de re-bootstrap para `WOT-2026-013r` via `--bootstrap-ticket`.
Estado pre-bootstrap preservado por git en el cierre de `013s`; las superficies
vivas del workspace se regeneran con el controller, no a mano.

Nota para el Builder:
- El paso 1 del packet es FIJO: repuntar los 8 patches de
  `scripts.upgrade.shutil.*` a `scripts.upgrade_agent_system.shutil.*` y anadir
  barrera fail-sin-fix en `tests/unit/test_upgrade.py`.
- `scripts/upgrade.py` y `scripts/upgrade_agent_system.py` quedan fuera de
  scope en esta primera pasada; solo se escalan si el paso 1 no basta.

## Fase 0 - Diagnostico (Builder, 2026-06-25, cwd=repo_motor, HEAD=38e65c9)

Seams confirmados (FP-012, VERIFICADO EN CODIGO):
- `tests/unit/test_upgrade.py:12` importa `UpgradeManager` de `scripts.upgrade_agent_system`.
- 8 patches a `scripts.upgrade.shutil.*` en lineas 46,47,83,84,112,113,204,205.
- `scripts/upgrade_agent_system.py` usa `shutil.copytree/copy2` en 148,151,199,202
  (con `import shutil` module-level en la linea 16).
- El fork `scripts/upgrade.py` tiene su propio `shutil.copytree/copy2` (124,127,179,182).
- Suite focal HOY: `python -m pytest tests/unit/test_upgrade.py -q` -> 18 passed (falso verde).

HALLAZGO RELEVANTE (matiz que refina FP-012, verificado por experimento):
- `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` -> **True**. Ambos
  modulos hacen `import shutil`, asi que comparten el MISMO objeto modulo `shutil`
  (cache de `sys.modules`). Por eso `patch("scripts.upgrade.shutil.copytree")` SI
  intercepta las llamadas del SUT (call_count=8 == len(CRITICAL_PATHS)), aunque el
  SUT no importe `scripts.upgrade`.
- Implicacion: el bug de FP-012 es de **target de patch incorrecto/fragil** (higiene),
  NO de dos objetos `shutil` distintos. Repuntar el string del patch al modulo
  realmente importado es la correccion honesta; pero el DoD "revertir el fix ->
  pytest FALLA" NO se cumple como diferencia entre dos shutil distintos.
- DECISION (con aprobacion humana, dentro del Paso 1, sin abrir Paso 2): construir
  la barrera fail-sin-fix por BINDING CORRECTO: (a) repuntar los 8 patches a
  `scripts.upgrade_agent_system.shutil.*`; (b) barrera que monkeypatchea
  copytree/copy2 a `raise` en el shutil del modulo del SUT y verifica que el flujo
  propaga el error; (c) assert explicito de que el modulo parcheado coincide con
  `UpgradeManager.__module__` (el realmente importado), de modo que apuntar a un
  modulo que el SUT NO usa deje pasar las copias y delate el drift.

Desviaciones de scope: ninguna. `scripts/upgrade.py` y `scripts/upgrade_agent_system.py`
NO se tocan (Paso 1). FLT operativo: `tests/unit/test_upgrade.py`.

## Fase 1 + Fase 2 - Implementacion, barrera y gates (Builder, 2026-06-25)

Cambios en `tests/unit/test_upgrade.py` (FLT, repo_motor):
- 8 patches repuntados: `scripts.upgrade.shutil.*` -> `scripts.upgrade_agent_system.shutil.*`
  (el modulo que el SUT realmente importa). Conteo verificado: wrong=0, right=11
  (8 originales + 3 en la barrera nueva).
- Clase nueva `TestUpgradeMockTargetBarrier` con 3 barreras:
  - `test_patch_target_is_the_module_the_sut_imports`: assert de binding correcto
    (`UpgradeManager.__module__ == "scripts.upgrade_agent_system"`).
  - `test_backup_propagates_real_copytree_failure`: monkeypatch copytree a raise
    en el shutil del modulo del SUT -> el flujo de backup propaga el error
    (`pytest.raises`), probando que las copias destructivas son reales.
  - `test_backup_invokes_real_copies_count`: copytree+copy2 call_count ==
    len(CRITICAL_PATHS) y > 0 (cobertura real, no pasiva).

Evidencia FAIL-sin-fix (mutation test, reproducible):
- Mute el assert de binding al fork viejo (`"scripts.upgrade"`) -> 
  `pytest ...::test_patch_target_is_the_module_the_sut_imports` -> **1 failed**
  (AssertionError: `- scripts.upgrade / + scripts.upgrade_agent_system`).
- Restaure el archivo correcto -> 21 passed.

Matiz honesto sobre el DoD "revertir el fix -> FALLA": verifique por experimento
que `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` (mismo objeto
modulo compartido via sys.modules). Por eso revertir SOLO el string de los 8
patches NO cambia el comportamiento de copia (siguen interceptando por el shutil
compartido). La barrera honesta que SI distingue el target correcto del
incorrecto es la de BINDING: los dos forks definen clases `UpgradeManager`
DISTINTAS (`scripts.upgrade.UpgradeManager is scripts.upgrade_agent_system.UpgradeManager`
-> False), y el SUT importado vive en `scripts.upgrade_agent_system`. Decision
tomada con aprobacion humana, dentro del Paso 1 (sin tocar codigo productivo ni
abrir el Paso 2 de deduplicacion).

Gates (comandos exactos + exit):
- `python -m pytest tests/unit/test_upgrade.py -q` -> 21 passed (exit 0).
- `python -m ruff check tests/unit/test_upgrade.py` -> All checks passed (exit 0).
- `uv run ruff format --check tests/unit/test_upgrade.py` -> 1 file already formatted (exit 0).
- `agent_controller --validate --json --force --project-root <repo_destino>` -> 0 errors / 0 warnings.
- Suite canonica `run_pytest_safe --level all`: se ejecuta al HEAD post-commit (ver last-run.json).

Scope: sin creep. `scripts/upgrade.py` y `scripts/upgrade_agent_system.py` NO
tocados. `README.md` NO tocado (Paso 2 no acometido). Paso 2 no requerido: el
Paso 1 demuestra la barrera honesta sin necesidad de deduplicar forks.

## CONTRACT_GAP -- WOT-2026-013r (tras CHANGES del Manager, 2026-06-25)

El Manager devolvio CHANGES con un unico bloqueo CENTRAL y CORRECTO: el DoD
binario linea 102 exige "revertir el fix de los patches -> 
`pytest tests/unit/test_upgrade.py -q` FALLA", y en un worktree pre-fix (38e65c9)
la suite sigue verde (18 passed). Eso es falso-verde segun el criterio escrito.

Diagnostico (verificado por experimento 3x, no relato):
- `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` -> True (objeto
  modulo compartido). Parchear cualquiera de los dos modulos parchea el MISMO
  atributo -> el repunte del target es FISICAMENTE INDISTINGUIBLE en runtime.
- Por tanto el DoD literal NO es satisfacible en el Paso 1 (sin tocar codigo
  productivo). La unica via es dar binding shutil independiente a cada fork /
  deduplicar -> Paso 2, que el packet marca como "requiere reaprobacion humana".

Decision (con aprobacion humana): emitir CONTRACT_GAP y PARAR, sin reescribir el
DoD ni acometer el Paso 2 sin reaprobacion. Artefactos:
- `.agent/planning/contract_gaps/CG-WOT-2026-013r.md` (gap + evidencia + 3 vias).
- Follow-up `WOT-2026-013t` registrado en `backlog.md` (fila + ficha; superficie
  fija que exige el work_plan lineas 59-65) para el Paso 2 (dedup de forks).
- Escalacion canonica a HUMAN_GATE via `--escalate-human-gate`.

Entrega del Paso 1 (verificada, queda como base si se aprueba 013t o se enmienda
el DoD): 8 patches repuntados al modulo importado (wrong=0), barrera de binding
mutation-verified, 21 passed focal, ruff OK, validate 0/0, suite canonica al HEAD
8e84a25 exit 0, commit motor 8e84a25.

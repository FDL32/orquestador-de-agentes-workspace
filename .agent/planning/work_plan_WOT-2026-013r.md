# Plan de Trabajo: WOT-2026-013r

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo. Fuente de verdad del
> problema: FP-012 en `repo_motor/docs/KNOWN_FAILURE_PATTERNS.md` (este packet
> referencia FP-012, no reproduce toda la explicacion).

## Metadata
- **ID:** WOT-2026-013r
- **Estado:** APPROVED
- **Titulo:** Corregir mock-drift de test_upgrade.py + cerrar duplicacion UpgradeManager
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Alta
- **Depende de:** WOT-2026-013s (sucesor de 013o; 013o cerro contra target equivocado)
- **Objective-Link:** cerrar el falso verde sobre operacion destructiva de
  upgrade (FP-012).

## Objetivo
Eliminar el falso verde de `test_upgrade.py` de forma verificable, con barrera
fail-sin-fix que demuestre que las copias reales del codigo bajo test se
interceptan.

## Premise Re-check (cwd=repo_motor)
```
git rev-parse --short HEAD
rg -n "from scripts\\.upgrade_agent_system import|patch\\(\"scripts\\.upgrade\\.shutil" tests/unit/test_upgrade.py
rg -n "shutil\\.copytree|shutil\\.copy2" scripts/upgrade_agent_system.py
```
Condicion de arranque (VERIFICADO POR BYTES 2026-06-25): `test_upgrade.py:12`
importa `UpgradeManager` de `scripts.upgrade_agent_system` pero parchea
`scripts.upgrade.shutil.*` (8 ocurrencias: 46,47,83,84,112,113,204,205) -> NO
intercepta `shutil.copytree`/`copy2` reales (`upgrade_agent_system.py:148,151,
199,202`). Detalle completo y causa raiz: FP-012. Si no reproduce, PARA.

## Decision Arquitectonica
El enfoque correcto en `013r` es corregir primero la barrera de test sobre el
modulo realmente importado (`scripts.upgrade_agent_system`) y demostrar el rojo
sin fix en `tests/unit/test_upgrade.py`, sin tocar aun el codigo productivo de
upgrade. Esta via minimiza blast radius: ataca el falso verde documentado en
FP-012, preserva intacto el flujo de install/upgrade mientras no haya evidencia
de un bug de producto y deja la deduplicacion `upgrade.py` vs
`upgrade_agent_system.py` como escalado explicito solo si el paso 1 no alcanza.

## Plan - secuencia minima FIJA (no es eleccion libre)
### Paso 1 (OBLIGATORIO PRIMERO) - repuntar patches + barrera
- Cambiar los 8 `patch("scripts.upgrade.shutil.*")` ->
  `patch("scripts.upgrade_agent_system.shutil.*")` (el modulo realmente
  importado) en `tests/unit/test_upgrade.py`.
- Anadir en ese mismo archivo (EXISTE; VERIFICADO EN CODIGO) una barrera
  fail-sin-fix: un test que monkeypatchee `copytree`/`copy2` reales a `raise` y
  confirme que el flujo de upgrade los invoca (la suite debe FALLAR sin el fix
  del patch y pasar con el).

### Paso 2 (SOLO SI el paso 1 no basta) - deduplicacion, requiere reaprobacion
- Solo si tras el paso 1 la duplicacion `upgrade.py` vs `upgrade_agent_system.py`
  impide una solucion honesta (ambiguedad real de cual es canonico), NO unifiques
  los forks en este ticket: registra un follow-up explicito y ESCALA.
- **Superficie donde se registra el follow-up (fija):**
  `orquestador_de_agentes_workspace/.agent/collaboration/backlog.md` como ticket
  derivado nuevo con el siguiente ID libre de la familia 013 (p.ej.
  `WOT-2026-013t`; NO `013s`, que ya existe y es la dependencia de este ticket),
  con referencia a FP-012; opcionalmente una nota en
  `repo_motor/docs/KNOWN_FAILURE_PATTERNS.md` (FP-012, seccion "Tickets
  relacionados"). No vale "lo registre" sin una de estas superficies.

## Files Likely Touched (relativos a repo_motor)
- `tests/unit/test_upgrade.py`  (EXISTE -> repuntar 8 patches + barrera fail-sin-fix)
- `README.md`                   (SOLO si el paso 2 se acomete con reaprobacion; si no, NO tocar)

Non-goal de superficie: `scripts/upgrade.py` y `scripts/upgrade_agent_system.py`
NO se tocan en el paso 1; solo en el paso 2 con reaprobacion humana explicita.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
# Loop rapido (diagnostico, primer ciclo):
python -m pytest tests/unit/test_upgrade.py -q
# Cierre canonico (antes de handoff):
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO tocar memoria portable en esta ronda (promocion de FP-012 a
  `observations.jsonl` se evalua DESPUES de 013s, con schema verde).
- NO redisenar el flujo install/upgrade.
- NO unificar los forks sin reaprobacion (paso 2).

## CONTRACT_GAP / STOP
- Si unificar forks obligaria a redisenar el flujo completo de install/upgrade
  del motor (instalacion, sync y upgrade), en vez de corregir el falso verde
  aislado de `test_upgrade.py`.
- Si la correccion depende de reinterpretar no-verificablemente cual
  `UpgradeManager` es canonico.
- Si se intenta mezclar este fix con la migracion de schema de 013s.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013r.md` + evento bus y PARA.

## DoD (binario, comandos exactos)

> **Enmienda (2026-06-25, reaprobacion humana; ver CG-WOT-2026-013r):** el DoD
> original exigia "revertir el fix de los patches -> pytest FALLA". Verificado 3x
> que `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` (objeto
> modulo compartido) -> repunte del target FISICAMENTE INDISTINGUIBLE; criterio
> NO satisfacible en Paso 1 sin codigo productivo (Paso 2). Se enmienda al
> aprendizaje real y verificable: **binding correcto** (el patch apunta al modulo
> que el SUT importa), mutation-verified. Dedup de forks = deuda OPCIONAL
> (WOT-2026-013t), no requisito de cierre.

- [x] **Barrera de binding demostrada (mutation-verified):** mutar el assert de
      `UpgradeManager.__module__` al fork viejo (`scripts.upgrade`) ->
      `pytest ...::test_patch_target_is_the_module_the_sut_imports -q` **FALLA**;
      con el valor correcto (`scripts.upgrade_agent_system`) -> pasa. La barrera
      real-copy (`copytree`->raise en el shutil del SUT) propaga el error.
- [x] Los 8 patches apuntan a `scripts.upgrade_agent_system.shutil.*` (el modulo importado).
- [x] `python -m ruff check tests/unit/test_upgrade.py` -> `All checks passed`.
- [x] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0, level all, tested_commit_sha == HEAD`.
- [x] `python .agent/agent_controller.py --validate --json --force` -> `0 errors / 0 warnings`.
- [x] Follow-up de deduplicacion en la superficie fija (backlog): `WOT-2026-013t`, deuda OPCIONAL (no bloquea cierre de 013r).

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013r`), suite canonica
fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.

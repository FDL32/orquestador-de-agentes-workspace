# 07 - Pasada adversarial (Pasada B)

## Bloque de cabecera
- **Scope:** auditoria adversarial del codigo nuevo de la sesion 2026-06-14
- **Repo motor (HEAD):** 3df6620
- **Repo destino (HEAD):** 905480e
- **Fecha:** 20260614_2027
- **Cobertura:** WOT-2026-004b/003e/003f/005a-d/006a/006b/003d (todo el codigo nuevo)
- **Metodo:** re-derivacion por codigo/test + counterexamples; no se acepta relato.

## Claims auditados (cada uno re-derivado)

| Claim | Verificacion adversarial | Resultado |
|---|---|---|
| 004b guard `.git` anclado, no bloquea `.github/.gitleaks.toml/.gitignore` | probes `_is_protected_path` (repo_root tmp): lookalikes block=False, `.git/` block=True, `privada` block=True | VERIFICADO |
| 003e `has_local_tests` salta pytest solo sin tests | counterexample: motor->True, dir vacio->False, `tests/` con solo conftest.py->False | VERIFICADO |
| 003d prune nunca borra tracked | worktree ba52a86 (pre-fix): 2 tests nuevos FALLAN; tree actual 45 passed (barrera real) | VERIFICADO |
| 003d fail-safe | test monkeypatch `_git_tracked_relpaths->None`: pruned==[], residue vive | VERIFICADO |
| 006a pytest.ini barrera return-not-none | suite 2633 passed, 0 warnings PytestReturnNotNoneWarning (si un test devolviera no-None, fallaria) | VERIFICADO |
| 006b encoding guard explicit-path + BOM | fichero BOM real -> "UTF-8 BOM detected", exit!=0; ruta limpia -> exit 0 | VERIFICADO |
| Gates colector (ruff/validate/discover/pristine motor+destino) | findings.json: todos exit_code 0, ok True | VERIFICADO |
| pytest-safe | last-run.json exit 0; focal 45 passed re-ejecutado | VERIFICADO |

## Hallazgos

### MEDIO (resuelto en esta pasada) - BOM en artefacto de sesion
- `orchestrator_pipeline/reports/readyforreview_WOT-2026-003d.md` tenia UTF-8 BOM
  (PowerShell Out-File por defecto). Detectado por el guard 006b ya endurecido.
  ACCION: BOM stripped en esta pasada; re-verificado exit 0. Artefacto gitignored:
  sin impacto en commits. Los otros 16 .md de reportes estan limpios.

### BAJO (latente, ahora cerrado) - falso-verde de evidencia de encoding
- Antes de 3df6620, `check_encoding_guard.py <archivo>` IGNORABA el argv y solo miraba
  staged. Por eso varios "encoding 0" del pipeline sobre closeouts gitignored eran
  hueco (median staged, no el archivo). 006b lo arregla. Re-verificados TODOS los
  closeouts con el guard corregido: limpios (tras strip del BOM).

### Observacion - 3df6620 fuera de scope de 003d
- Mejora real y testeada, pero pertenece a otro subsistema. Trazada como WOT-2026-006b.

## Veredicto global

**APROBADO CON NITS.** Todo el codigo nuevo funciona segun contrato, con barreras reales
(no false-greens). El unico defecto material (BOM en artefacto) se corrigio en la pasada.
El gap de evidencia de encoding queda cerrado por 006b y re-verificado. Sin criticos
automaticos; degraded=False; ambos repos limpios; validate 0/0 motor y destino.

## Follow-ups (no bloqueantes)
- Higiene: conservar vs compactar las 4 auditorias system_health (1044/1738/1739/2027).
- 004b: el allowlist por PATH del seed gitleaks incluye `.agent/runtime/` (amplio); aceptable
  para seed generico; los destinos pueden afinar.

# Audit: WOT-2026-008b - Discovery/frontmatter hardening

## TP Check (True Positive Checklist)

El Manager verifica estos criterios contra evidencia real, no contra el relato del Builder.

### Barrera BOM (criterio mas critico)

- [ ] **TP-1 (CRITICO):** Existe un test que FALLA con el codigo actual (BOM silencioso)
      y PASA con el fix. Evidencia: comando exacto + exit codes antes y despues.
      Si el test solo pasa en estado limpio pero no falla sin el fix, NO es TP.
- [ ] **TP-2:** `discover_skills.py` con fix descubre 29/29 SKILL.md. Evidencia:
      salida de `python scripts/discover_skills.py --json | python -c "import sys,json; print(len(json.load(sys.stdin)))"`.
- [ ] **TP-3:** `discover_skills.py --check-contract` devuelve exit != 0 si hay
      skills con BOM invisible. Evidencia: test o comando reproducible.

### Paridad discovery/collision

- [ ] **TP-4:** `check_skill_collisions.py` y `discover_skills.py` usan semantica
      compatible para BOM/frontmatter. Si difieren, la diferencia esta documentada
      con justificacion en el codigo, no solo en prose.

### BOM barrido

- [ ] **TP-5:** El barrido BOM esta documentado en `execution_log.md` con rutas
      exactas. La ausencia de otros BOMs es un resultado, no un supuesto.
- [ ] **TP-6:** `skills/man-review-implementation/SKILL.md` ya no tiene BOM.
      Evidencia: `python -c "b=open('skills/man-review-implementation/SKILL.md','rb').read(3); print(b.hex())"` != `efbbbf`.

### DECs

- [ ] **TP-7:** `docs/decisions/DEC-008B-001-registry-model.md` existe en disco
      con al menos 4 opciones y una decision explicitamente declarada.
      INFERENCIA de suficiencia no valida: el Manager lee el archivo.
- [ ] **TP-8:** `docs/decisions/DEC-008B-002-discovery-triggers.md` existe en
      disco con decision explicitamente declarada.

### Matriz de ghosts

- [ ] **TP-9:** La matriz allowlist vs triggers esta derivada de fuentes vivas
      (no de memoria ni de la evidencia pre-Builder de este plan). El Builder
      re-ejecuta la derivacion tras el fix BOM para capturar cualquier cambio.
- [ ] **TP-10:** `/review` NO fue retirado de la allowlist.
- [ ] **TP-11:** Noise (`/deepseek-v4-flash`, `/gpt-5`) esta identificado y
      documentado. Si el Builder los retira de `agents.json`, debe ser decision
      explicita con justificacion, no efecto colateral.

### Gates

- [ ] **TP-12:** `ruff check .` en repo_motor: exit 0. Comando literal registrado.
- [ ] **TP-13:** Tests focales de discovery/collision/encoding: exit 0. Comando
      literal con lista de tests registrada.
- [ ] **TP-14:** `validate --json --project-root <destino>`: 0 errors / 0 warnings.
- [ ] **TP-15:** Commit productivo en repo_motor con `WOT-2026-008b` en el mensaje.

## STOP Conditions (para Manager)

Si cualquiera de estas condiciones se activa, emitir CHANGES:

1. **STOP-1:** El test de BOM solo pasa en estado limpio pero no falla sin el fix.
2. **STOP-2:** `discover_skills.py` sigue devolviendo 28/29 tras el fix.
3. **STOP-3:** El Builder movio, renombro o creo carpetas de skills.
4. **STOP-4:** El Builder implemento un `registry.json` operativo con dispatch.
5. **STOP-5:** El Builder creo aliases runtime o shims.
6. **STOP-6:** `/review` fue retirado de la allowlist.
7. **STOP-7:** Las DECs no existen como archivos en disco o son solo prose sin decision.
8. **STOP-8:** Cualquier gate reportado sin exit code literal.
9. **STOP-9:** El Builder toco superficies de 008c/008d/008e/008f.
10. **STOP-10:** `validate` final != 0/0.

## Checklist adversarial (Revision 2)

Para la segunda revision, el Manager debe intentar refutar el cierre:

- El test de TP-1: ¿realmente falla sin el fix? Reproducir manualmente si es posible.
- Los commits tocan solo `Files Likely Touched` del plan? `git show --stat <commit>`.
- ¿Hay scope creep escondido en el diff (nuevas features, refactors no declarados)?
- ¿Las DECs son decisiones reales o solo enumeraciones sin conclusion?
- ¿El barrido BOM uso bytes reales o solo text-mode (que consumiria el BOM sin reportarlo)?
- ¿La matriz de ghosts se re-derivo post-fix o copio la del plan?

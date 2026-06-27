# AUDIT_WOT-2026-014g

## Scope
- Ticket WOT-2026-014g, code, repo_motor.
- Objetivo auditado: name==dir en 6 skills + gate name==dir en discover_skills, sin tocar dispatch ni reglas existentes.

## TP Check
- TP-01: solo cambia el frontmatter name (y titulo solo si no coincidia ya); carpetas/triggers/dispatch intactos.
- TP-02: el gate vive en discover_skills._check_skill_names y compara el name del frontmatter con skill_dir.name.
- TP-03: barrera mutation-verified: fixture con name != carpeta hace FALLAR el gate; sin el gate pasa silenciosamente.
- TP-04: NO se hace canonico el name corto; reglas kebab-case/actor-first (DEC-008D-001) intactas.
- TP-05: cierre con run_pytest_safe --level all + validate.

## Nota de charter
- Conflicto aparente con el Non-Goal "No modificar scripts de discovery" resuelto como 008-plan-scoped (ver work_plan).
  Deuda documental del charter, no del ticket; no bloquea pero queda registrado como follow-up.

## Regression Focus
- Falso verde a evitar: un test que verifica que las 6 skills estan alineadas pero NO prueba que el gate FALLA
  ante un name != dir (un gate que no bloquea no cuenta).

## Closing Rule
- No aprobar si se hace canonico el name corto, si se tocan dispatch/triggers/reglas existentes, si el gate no es
  mutation-verified, o sin el SHA del commit del repo_motor.

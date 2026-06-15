# 04 - Quality gates

## Bloque de cabecera

- **Scope:** ruff / validate / pytest-safe / motor pristine / skills contract
- **Fecha auditada:** 20260615_2141
- **Auditor:** Claude Sonnet 4.6

---

## Resultados de gates

| Gate | Target | Exit code | Estado |
|------|--------|-----------|--------|
| ruff_motor | repo_motor | 0 | PASS |
| validate_motor | repo_motor | 0 (0/0) | PASS |
| ruff_destino | repo_destino | 0 (sin archivos Python) | PASS / N/A |
| validate_destino | repo_destino | 0 (0/0) | PASS |
| motor_pristine | repo_motor | 0 | PASS |
| discover_skills_contract | repo_motor | 0 | PASS |
| pytest_safe_last_run | repo_motor | 0 | PASS parcial |

## Caveats documentados

1. ruff_destino: exit 0 con 0 archivos Python (esperado en host-extends). No es red flag.
2. pytest_safe_last_run: suite = allowlist parcial (~28/147 archivos de test). Exit 0 real
   pero cobertura total no garantizada.
3. Pip-audit: no corre en collector; aplica politica condicional por deliverable_type.
   009d/009e/009f no tocan pyproject.toml ni uv.lock, por lo que pip-audit es skip auditable.
   Estado actual de PYSEC-2026-196: excepcion activa por uv bloqueado en pip<26.1.2 (blocker externo).

## Veredicto

Quality gates pasan en todos los ejes medidos con las limitaciones documentadas.
No hay gates en rojo al momento de la auditoria.
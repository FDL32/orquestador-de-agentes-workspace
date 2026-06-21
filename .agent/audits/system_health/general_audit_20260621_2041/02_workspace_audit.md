# 02 - Auditoria del repo_destino

## Bloque de cabecera

- **Scope:** salud del destino
- **Repo motor (HEAD):** <MOTOR_ROOT> @ e251bd7c1e09c5ad698bdc3102754f2694c0afcb
- **Repo destino (HEAD):** <DESTINO_ROOT> @ 619c571895c9e19155322b10787067aa56f2b74d
- **Fecha:** 20260621_2041
- **Modo:** full
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/audit_post_change_system_health.md.

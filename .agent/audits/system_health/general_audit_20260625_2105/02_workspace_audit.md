# 02 - Auditoria del repo_destino

## Bloque de cabecera

- **Scope:** salud del destino
- **Repo motor (HEAD):** <MOTOR_ROOT> @ a1b99afd87c3d351b6644d0623b47ee128f0987a
- **Repo destino (HEAD):** <DESTINO_ROOT> @ 1c0a6aede12dce07b4c571e054e3ab36b91fdb69
- **Fecha:** 20260625_2105
- **Modo:** auto
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/audit_post_change_system_health.md.

# 03 - Auditoria de integracion

## Bloque de cabecera

- **Scope:** motor+destino
- **Repo motor (HEAD):** <MOTOR_ROOT> @ ff05b8db4ed67b81f1ebc538dcab0266b48b76e9
- **Repo destino (HEAD):** <DESTINO_ROOT> @ 53e3e65b9535d20674bbdb80035f255f032b8dfc
- **Fecha:** 20260614_1738
- **Modo:** full
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/audit_post_change_system_health.md.

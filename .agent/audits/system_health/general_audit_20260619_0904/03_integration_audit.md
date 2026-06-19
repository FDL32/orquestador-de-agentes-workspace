# 03 - Auditoria de integracion

## Bloque de cabecera

- **Scope:** motor+destino
- **Repo motor (HEAD):** <MOTOR_ROOT> @ 6e55f86eb19824cc4a6f94a9a5a951c8156229f7
- **Repo destino (HEAD):** <DESTINO_ROOT> @ 44c7ed314cb345392fe78c7f4f3567af7046de7e
- **Fecha:** 20260619_0904
- **Modo:** auto
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/audit_post_change_system_health.md.

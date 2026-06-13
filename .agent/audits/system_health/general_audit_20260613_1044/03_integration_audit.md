# 03 - Auditoria de integracion

## Bloque de cabecera

- **Scope:** motor+destino
- **Repo motor (HEAD):** <MOTOR_ROOT> @ c4f2ae84460a100d23c2cc47df8c50096d51f88d
- **Repo destino (HEAD):** <DESTINO_ROOT> @ 17813a59340593164248d544a4ab7eef5be28dd1
- **Fecha:** 20260613_1044
- **Modo:** full
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/system_health_audit.md.

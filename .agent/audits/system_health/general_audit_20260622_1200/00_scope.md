# 00 - Scope y topologia

## Bloque de cabecera

- **Scope:** topologia y baseline del sistema
- **Repo motor (HEAD):** <MOTOR_ROOT> @ 222da7798c044bbf1692a17a835194c5a7614b68
- **Repo destino (HEAD):** <DESTINO_ROOT> @ eaf13219e1be5f1208bcd4b9e88502dc65f24bbe
- **Fecha:** 20260622_1200
- **Modo:** auto
- **Comandos ejecutados:** ver findings.json y raw/
- **Cobertura declarada:** Pasada A determinista. pytest-safe via last-run.json (exit real, no pipe). Si la suite es allowlist parcial, NO es verde global.
- **Limitaciones:** recoleccion determinista (Pasada A). El juicio adversarial
  (Pasada B) lo completa el agente. Este archivo es un esqueleto.

---

> Esqueleto generado por collect_system_health.py (system-health-collector/v0). El agente debe
> rellenar los hallazgos aplicando prompts/audit_post_change_system_health.md.

## Alcance de versionado (system-health-audit v0)

- **Versionables:** `*.md` + `findings.json` + `INDEX.md`.
- **NO versionable:** `raw/` (gitignored por contrato del prompt; v0 solo relativiza
  roots motor/destino, no sanea $USERPROFILE/hostname/timings -> deuda v1).
- **classify_publication.py** (2026-06-22, exit 1): verdict global del repo
  `BLOQUEADO_POR_SECRETO`, pero los 2 findings son falsos positivos AJENOS a esta
  auditoria (`.gitleaks.toml` = config del propio detector; `_backups/.../anti-patterns.md`
  = ejemplos didacticos en backup historico). La carpeta de auditoria solo aparece en
  `git_status` como untracked; NO contiene secretos. El commit de artefactos esta acotado
  a esta carpeta + INDEX.md (verificado con `git add -n`).

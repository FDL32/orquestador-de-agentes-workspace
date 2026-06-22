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

## Nota anti-re-triage (falsos positivos de classify_publication) y exclusion consciente de raw/

Para evitar volver a triarlo en futuras auditorias:

- **2 falsos positivos de `classify_publication.py` (2026-06-22), NO afectan al artefacto versionado:**
  1. `.gitleaks.toml` -> `evidence: secret_pattern`. Es el fichero de CONFIGURACION del propio
     detector gitleaks; contiene patrones regex de deteccion, no secretos. El detector se detecta a si mismo.
  2. `_backups/agent_system.backup.2026-04-30/docs/reference/anti-patterns.md` -> `secret_pattern`.
     Doc didactico de anti-patrones en un backup historico; contiene EJEMPLOS de secretos hardcodeados
     para ensenar que NO hacer. Falso positivo didactico en arbol de backup.
  - Ambos son ruido preexistente del repo de dogfooding, AJENOS a esta carpeta de auditoria.
    El verdict global `BLOQUEADO_POR_SECRETO` NO lo introduce este commit y NO bloquea el versionado
    de los artefactos de auditoria (que no contienen secretos).

- **`raw/` inspeccionado y excluido CONSCIENTEMENTE (no solo "no staged"):**
  `git check-ignore` confirma que `raw/` esta gitignored por el `.gitignore` que el recolector deja
  en la carpeta (contrato system-health-audit v0). Se verifico ademas que ningun archivo bajo `raw/`
  entra en los commits a publicar (`git log origin/main..HEAD --name-only | grep raw/` -> vacio).
  Exclusion deliberada: v0 solo relativiza roots motor/destino; `raw/` puede filtrar
  $USERPROFILE/hostname/timings (deuda v1), por eso se mantiene fuera del arbol versionado.

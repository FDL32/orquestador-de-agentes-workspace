# Plan de Trabajo: WOT-2026-014d

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014d
- **Estado:** APPROVED
- **Titulo:** Re-encodar builder-self-audit/SKILL.md a UTF-8 limpio + endurecer encoding_guard al rango C1 0x80-0x9F
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Alta
- **Depende de:** -
- **Objective-Link:** OBJ-014D-001
- **Plan-Link:** PLAN-014D-001
- **Builder clarification budget:** 0 (blast-radius resuelto; alcance fijado)

## Objetivo
(a) Re-encodar skills/builder-self-audit/SKILL.md a UTF-8 limpio: corregir los 4 codepoints de control C1
(U+0085, U+008C, U+0092, U+0094) a su caracter intencional (marcadores OK/Error/separador coherentes con
el resto de skills sanas del ecosistema). (b) Endurecer scripts/encoding_guard.py con una BARRERA POR CLASE
(no lista negra de bytes): (i) flaguear TODO codepoint de control C1 (U+0080-U+009F) en el texto decodificado;
(ii) anadir decode('utf-8', errors='strict') como capa complementaria para bytes UTF-8 invalidos.
Verificacion del objetivo: barrera mutation-verified en tests/ (ver DoD) + check_encoding_guard verde tras el re-encode.

## Blast-radius (RESUELTO empiricamente por orquestacion)
Consultado el propio guard (encoding_guard.collect_scope_set / is_in_scope): de los 284 archivos en scope,
EXACTAMENTE 1 tiene codepoints C1: skills/builder-self-audit/SKILL.md (el target). El backup
(.agent/backups/...) esta is_excluded; los otros archivos con C1 (agent_system/refactor_kit/*, tests/0X-*.md)
NO matchean ningun GLOB_PATTERN del guard. Por tanto endurecer el rango C1 es COLATERAL-CERO: tras re-encodar
builder-self-audit, el guard escanea su scope y encuentra 0 C1 -> verde. NO se necesita allowlist ni limpieza
colateral; NO se amplia el alcance a otros archivos.

## Premise (VERIFICADO en codigo)
- skills/builder-self-audit/SKILL.md decodifica como UTF-8 VALIDO (0 U+FFFD) pero contiene los codepoints C1
  U+0085, U+008C, U+0092, U+0094 (validos-pero-erroneos) en los marcadores de los Pasos 1-7.
- scripts/encoding_guard.py: find_control_chars (~L123) solo flaguea ASCII control <32; SUSPICIOUS_CODEPOINTS
  (~L28) = {0x00C3,0x00C2,0x00E2,0x00F0,0x0102,0xFFFD} NO incluye el rango C1, asi que el guard pasa en verde
  sobre la corrupcion actual (drift silencioso).

## Premise Re-check (cwd=repo_motor, solo lectura)
python -c "t=open('skills/builder-self-audit/SKILL.md',encoding='utf-8').read(); print(sorted({hex(ord(c)) for c in t if 0x80<=ord(c)<=0x9F}))"
python scripts/check_encoding_guard.py; echo exit=$?
Condicion de arranque: builder-self-audit sigue con C1; el guard pasa verde (no chequea C1 aun).

## Decision Arquitectonica
- Endurecer encoding_guard por CLASE: anadir un chequeo que flaguee cualquier codepoint en U+0080-U+009F en el
  texto decodificado (no una lista de bytes concretos). Integrarlo en la ruta de deteccion (find_control_chars o
  un find_c1_controls hermano, reportado en el tercer elemento de file_issues junto a los control chars existentes).
- Anadir decode('utf-8', errors='strict') como capa COMPLEMENTARIA para bytes UTF-8 invalidos (otra clase).
- PRECISION: builder-self-audit es UTF-8 valido con C1 -> strict SOLO no lo detecta; el chequeo de rango C1 si.
- NO prohibir Latin-1 legitimos (letras): solo el rango de CONTROL C1.
- Re-encodar builder-self-audit: mapear cada C1 a su marcador intencional cotejando como rinden esos marcadores
  las skills sanas (sin corrupcion). NO inventar; igualar el ecosistema.

## Files Likely Touched (relativos a repo_motor)
- skills/builder-self-audit/SKILL.md
- scripts/encoding_guard.py
- tests/unit/test_encoding_guard_c1.py

Aclaraciones: solo se re-encoda builder-self-audit (NO las otras skills). El guard gana el chequeo de rango C1 +
strict-decode; no se tocan las reglas de mojibake/path-bullet existentes salvo extension aditiva.

## Read/inspect only
- scripts/check_encoding_guard.py
- otras skills sanas (para cotejar marcadores intencionales), read-only
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- NO re-encodar las otras 30 skills ni normalizar lineas en blanco del ecosistema.
- NO prohibir Latin-1 supplement legitimo (letras acentuadas); solo el rango de CONTROL C1 (U+0080-U+009F).
- Las reglas existentes del guard (mojibake SUSPICIOUS_CODEPOINTS, path-bullet, ASCII control): read-only salvo
  extension aditiva del nuevo chequeo.
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal
python -m pytest tests/unit/test_encoding_guard_c1.py -q
python scripts/check_encoding_guard.py
python -m ruff check scripts/encoding_guard.py tests/unit/test_encoding_guard_c1.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO re-encodar otras skills.
- NO prohibir Latin-1 legitimo.
- NO una lista negra de bytes concretos (la barrera es por CLASE).

## CONTRACT_GAP / STOP
- Si re-encodar builder-self-audit a marcadores limpios no puede hacerse sin tocar contenido sustantivo (mas alla
  de los marcadores corruptos).
- Si endurecer el rango C1 flaguea algun OTRO archivo in-scope (el blast-radius dice que no, pero si aparece, PARAR
  y reportar en vez de allowlistear a ciegas).
-> emitir CG-WOT-2026-014d.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] skills/builder-self-audit/SKILL.md: 0 codepoints C1 (U+0080-U+009F); marcadores corregidos al caracter intencional, coherentes con el resto de skills.
- [ ] BARRERA PRIMARIA (mutation-verified): tras endurecer el guard, check_encoding_guard / file_issues FALLA si se reinyecta (i) cualquier codepoint C1 (U+0080-U+009F) O (ii) un byte UTF-8 invalido.
- [ ] CASO NEGATIVO EXPLICITO: una cadena que ES UTF-8 valido pero contiene un codepoint C1 (p.ej. U+0094) PASA decode('utf-8',errors='strict') y AUN ASI es flagueada por el chequeo de rango (demuestra que strict solo NO basta).
- [ ] El guard ANTES del fix deja pasar el caso real de builder-self-audit; el endurecido lo bloquea (mutation-verified contra el archivo real o un fixture identico).
- [ ] python scripts/check_encoding_guard.py -> exit 0 (verde) sobre el repo tras el re-encode (blast-radius cero confirmado).
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD.
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014d), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.

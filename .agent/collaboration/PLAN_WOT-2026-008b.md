# Plan Tecnico: WOT-2026-008b

## Problema raiz (VERIFICADO en vivo, 2026-06-16)

`discover_skills.py` abre `SKILL.md` en modo texto sin `utf-8-sig`, por lo que
el BOM (`\xef\xbb\xbf`) se convierte en el primer caracter del contenido y el
parser YAML/frontmatter devuelve `NO_FRONTMATTER`. La skill queda invisible.

`check_skill_collisions.py` usa una ruta distinta (probablemente `utf-8-sig` o
`errors='ignore'`), por lo que ve la skill correctamente y no detecta colision.

El resultado es **falso verde estructural**: `--check-contract` puede pasar con
exit 0 aunque una skill critica sea invisible al discovery.

## Estrategia tecnica

### Fase 1: Fix BOM en discover_skills.py (atomico, verificable)

1. Localizar la apertura de archivos en `scripts/discover_skills.py`.
2. Cambiar `open(path)` o `open(path, 'r')` a `open(path, 'r', encoding='utf-8-sig')`.
   Esto hace que Python consuma el BOM silenciosamente si existe, sin fallar si no existe.
3. Verificar que `check_skill_collisions.py` usa la misma semantica; si no, alinear
   o documentar la diferencia con justificacion.
4. Verificar y alinear `check_encoding_guard.py` si su cobertura de BOM es parcial.

### Fase 2: Fix BOM en man-review-implementation/SKILL.md

Reescribir el archivo sin BOM. La forma mas segura en Python:
```python
content = open(path, 'rb').read()
if content.startswith(b'\xef\xbb\xbf'):
    open(path, 'wb').write(content[3:])
```
Verificar post-fix: `open(path,'rb').read(3) != b'\xef\xbb\xbf'`.

### Fase 3: Test de regresion (obligatorio, no opcional)

Crear test que:
1. Crea un `SKILL.md` temporal con BOM valido en frontmatter.
2. Ejecuta `discover_skills.py` contra ese directorio temporal.
3. Afirma que la skill NO es invisible (aparece en la lista descubierta).
4. Afirma que `--check-contract` devuelve exit != 0 si hay skills invisibles.

El test debe **fallar con el codigo actual** y **pasar con el fix**. Si no falla
sin el fix, el test no es evidencia valida de la barrera.

### Fase 4: Barrido BOM completo

Escanear `skills/**/SKILL.md` y `prompts/*.md` con:
```python
open(p, 'rb').read(3) == b'\xef\xbb\xbf'
```
Documentar resultado con rutas exactas en el execution_log.

**Resultado conocido pre-Builder:**
- `skills/man-review-implementation/SKILL.md`: BOM presente.
- Otros SKILL.md: ninguno con BOM (verificado 2026-06-16).
- prompts/*.md: ninguno con BOM (verificado 2026-06-16).

### Fase 5: Clasificacion de ghosts (matriz allowlist)

Partiendo de la evidencia pre-Builder derivada:

| Trigger | Estado | Clasificacion probable |
|---|---|---|
| `/review` | BOM-casualty | `BOM-casualty` — NO retirar de allowlist |
| `/implement` | Cubierto por skill | OK (bui-implement-from-plan: /implement) |
| `/audit` | Cubierto por skill | OK (audit-pipeline, audit-git-publication) |
| `/compare` | Cubierto por skill | OK (repo-compare: /compare) |
| `/debug` | Cubierto por skill | OK (systematic-debugging: /debug) |
| `/tdd` | Cubierto por skill | OK (test-driven-development: /tdd) |
| `/refactor` | Cubierto por skill | OK (refactor-manager: /refactor) |
| `/schedule` | Cubierto por skill | OK (session-close-observations) |
| `/inspect` | Cubierto por skill | OK (man-review: /inspect) |
| `/archive` | NO en ningun frontmatter | Clasificar: `retired` o `pending-skill` |
| `/fix` | NO en ningun frontmatter | Clasificar: `retired` o `pending-skill` |
| `/impl` | NO en ningun frontmatter | Alias de `/implement`? Verificar |
| `/orchestrate` | NO en ningun frontmatter | Clasificar: `retired` o `pending-skill` |
| `/report` | NO en ningun frontmatter | Clasificar: `retired` o `pending-skill` |
| `/test` | NO en ningun frontmatter | Alias de `/tdd`? Verificar |
| `/validate` | NO en ningun frontmatter | Clasificar: `retired` o `pending-skill` |
| `/deepseek-v4-flash` | Backend noise | Eliminar de allowlist |
| `/gpt-5` | Backend noise | Eliminar de allowlist |

El Builder debe verificar cada ghost contra commits/docs historicos antes de
clasificar como `retired`.

### Fase 6: Cerrar DECs

Crear en `docs/decisions/`:
- `DEC-008B-001-registry-model.md`: decision sobre modelo de registry.
- `DEC-008B-002-discovery-triggers.md`: decision sobre modelo de discovery.

Cada DEC debe tener: contexto, opciones comparadas, decision, razon, fecha y
efecto en tickets pendientes (008c/d/e).

## Orden de implementacion recomendado

1. Test de regresion (Fase 3) — primero, para validar el fix.
2. Fix `discover_skills.py` (Fase 1).
3. Fix BOM `man-review-implementation` (Fase 2).
4. Verificar test pasa con fix, fallo sin fix (evidencia de barrera).
5. Barrido BOM completo (Fase 4).
6. Clasificacion ghosts (Fase 5).
7. DECs (Fase 6).
8. Gates: `ruff check .`, tests focales, `--check-contract`, validate 0/0.

## Baseline

- Motor HEAD pre-Builder: verificar con `git log --oneline -1` al arrancar.
- Destino HEAD pre-Builder: verificar con `git -C <destino> log --oneline -1`.
- Validate pre-Builder: 0/0 (VERIFICADO 2026-06-16).

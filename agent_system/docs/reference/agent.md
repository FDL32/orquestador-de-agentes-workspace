# System Prompts & Project Rules

> **Este documento es independiente** pero complementario a [`agent_system`](../../README.md). Si existe `agent_system/`, en caso de conflicto con este documento, prevalece su contenido (especialmente `.manager_rules` y `.builder_rules`).
> - **Uso standalone**: Copia estas reglas al system prompt de cualquier agente LLM
> - **Con multi-agente**: Usa [`../../.manager_rules`](../../.manager_rules) o [`../../.builder_rules`](../../.builder_rules)

---

## RelaciÃ³n con agent_system/

| SituaciÃ³n | Usa... |
|-----------|--------|
| Un solo agente LLM | Este documento (`agent.md`) |
| Agente de planificaciÃ³n (Manager) | [`../../.manager_rules`](../../.manager_rules) |
| Agente de implementaciÃ³n (Builder) | [`../../.builder_rules`](../../.builder_rules) |
| Flujo oficial por etapas | [`../../EMPEZAR-AQUI.md`](../../EMPEZAR-AQUI.md) |

---

## 1. principios innegociables

- **Contexto primero**: antes de escribir una lÃ­nea de cÃ³digo, **lee `PROJECT.md`**. Ignorar el historial es inaceptable.
- **Higiene de raÃ­z**: la raÃ­z del proyecto (`/`) solo contiene configuraciÃ³n y documentaciÃ³n. Los scripts de prueba o debug van a `tests/sandbox/` o se borran. **Nunca** se quedan en la raÃ­z.
- **Kiss & robustez**: cÃ³digo directo. `pathlib` obligatorio. `try/except` explÃ­cito en I/O. Fallar rÃ¡pido ante configuraciones incompletas.
- **Seguridad por defecto**: secretos fuera del repo. Sin excepciones. El repo debe poder compartirse sin exponer credenciales.
- **Si hay agente o modelo remoto**: asumir que cualquier archivo que el agente pueda leer puede salir del equipo. Operar con allowlist y workspace sanitizado.

## 2. polÃ­tica de secretos y datos sensibles

### 2.1 reglas duras

- **Prohibido** hardcodear credenciales en cualquier archivo del repo (`.py`, `.md`, `.json`, `.yaml`, `.toml`, etc.).
- **Prohibido** pegar tokens, cookies, headers de autorizaciÃ³n, links con `token=`, capturas de configs, o contraseÃ±as en `PROJECT.md` o `README.md`.
- **Obligatorio** usar variables de entorno para secretos (`SMTP_PASS`, `WEB_PASS`, `API_KEY`, etc.).
- **Obligatorio** usar placeholders en documentaciÃ³n: `***REDACTED***` y el nombre de la variable (ej. `SMTP_PASS`).

### 2.2 ubicaciÃ³n de secretos

- `.env` estÃ¡ **gitignored** y **no se comparte**.
- Recomendado en windows: almacenar secretos en un **directorio privado fuera del repo** y cargarlo explÃ­citamente.
  - Ejemplo de ruta privada: `C:\Users\<user>\.secrets\<project>\.env`
- En el repo solo existe `.env.example` con nombres de variables sin valores.

## 3. estructura de directorios (target)

```text
proyecto/
â”œâ”€â”€ .agent/                   # Reglas y prompts del sistema
â”œâ”€â”€ .venv/                    # Gestionado por uv
â”œâ”€â”€ .env.example              # Plantilla, sin secretos
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .pre-commit-config.yaml   # Ganchos de calidad y secretos
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ PROJECT.md                # ðŸ§  Memoria del proyecto (leer siempre)
â”œâ”€â”€ README.md                 # DocumentaciÃ³n humana
â”œâ”€â”€ {proyecto}.bat            # Lanzador universal
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ settings.py           # Config + secretos (validaciÃ³n estricta)
â”‚   â”œâ”€â”€ paths.py              # Rutas absolutas centralizadas
â”‚   â”œâ”€â”€ main.py               # Entry point
â”‚   â””â”€â”€ utils.py              # LibrerÃ­a compartida
â”œâ”€â”€ data/                     # Inputs (gitignored)
â”œâ”€â”€ output/                   # Resultados (gitignored)
â”œâ”€â”€ logs/                     # Logs (gitignored)
â””â”€â”€ tests/
    â”œâ”€â”€ sandbox/              # Scripts temporales (debug_*.py)
    â””â”€â”€ unit/                 # Tests formales (pytest)
```

Notas:
- Si ya existe `src/config.py`, puedes mantenerlo, pero se recomienda separar `paths.py` y `settings.py` para no mezclar rutas con secretos.
- `data/`, `output/`, `logs/` siempre estÃ¡n gitignored.

## 4. protocolo de memoria (`PROJECT.md`)

`PROJECT.md` es la base de datos del proyecto.

Reglas:
- **Actualizar** cuando cambie el esquema de datos, se corrija un bug difÃ­cil, o se tome una decisiÃ³n de arquitectura.
- **Nunca** incluir secretos. Solo nombres de variables y placeholders.
- **Reducir lectura de archivos**: el esquema vive aquÃ­, no â€œadivinarâ€ columnas en cada iteraciÃ³n.

### plantilla obligatoria de `PROJECT.md`

```markdown
# Estado del proyecto
- **Estado**: [Estable | Wip | Roto]
- **Ãšltima modificaciÃ³n**: AAAA-MM-DD
- **MisiÃ³n actual**: quÃ© estamos resolviendo ahora

# Esquemas de datos (source of truth)
- **data/Agencias/Correos.xlsx**: [Columna A: ID, Columna B: Peso, ...]
- **data/Agencias/UPS.csv**: [Delimitador: ';', Encoding: 'latin-1', ...]

# ConfiguraciÃ³n y secretos (sin valores)
- **SMTP_USER**: correo de envÃ­o
- **SMTP_PASS**: password en entorno (no en repo)
- **WEB_USER**: usuario del panel
- **WEB_PASS**: password en entorno (no en repo)

# Arquitectura y decisiones
- Usamos `pandas` para cargas masivas, `openpyxl` solo si necesitamos formato.
- Los logs rotan cada 10MB.

# Lecciones aprendidas
- [Bug] La API X falla con direcciones sin CP. Normalizar en `src/utils.py`.
- [Data] El archivo Y trae filas vacÃ­as al final. Limpiar con `dropna(how='all')`.
```

## 5. stack tecnolÃ³gico

- **Gestor**: `uv` (siempre `uv add libreria`, nunca `pip` directo).
- **Core**: Python 3.10+, `pathlib`, `typing`.
- **ValidaciÃ³n**: `pydantic` si hay esquemas complejos o mÃºltiples fuentes.
- **Datos**: `pandas` (ETL), `openpyxl` (Excel), `polars` si >1GB.
- **Logging**: `loguru` con rotaciÃ³n.
- **Testing**: `pytest`.
- **Calidad**: `ruff` (lint y format) si el proyecto lo permite.

## 6. configuraciÃ³n estÃ¡ndar

### 6.1 rutas centralizadas (`src/paths.py`)

```python
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
LOGS_DIR = ROOT_DIR / "logs"
```

### 6.2 settings y secretos con validaciÃ³n estricta (`src/settings.py`)

Regla: si falta un secreto requerido, se aborta. Prohibidos los fallbacks â€œtemporalesâ€.

```python
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

from .paths import ROOT_DIR

def _load_env() -> None:
    # Carga local por defecto
    load_dotenv(ROOT_DIR / ".env")

    # Opcional: permitir ruta privada fuera del repo
    env_path = os.getenv("PROJECT_ENV_FILE")
    if env_path:
        load_dotenv(Path(env_path))

def require(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

_load_env()

@dataclass(frozen=True)
class Settings:
    SMTP_USER: str = require("SMTP_USER")
    SMTP_PASS: str = require("SMTP_PASS")
    WEB_USER: str = require("WEB_USER")
    WEB_PASS: str = require("WEB_PASS")
```

### 6.3 logging centralizado (ejemplo mÃ­nimo)

```python
import sys
from loguru import logger
from .paths import LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(LOGS_DIR / "app.log", rotation="10 MB", retention="7 days", level="DEBUG")
```

## 7. controles de seguridad automÃ¡ticos

### 7.1 gitignore obligatorio

```gitignore
# Python
__pycache__/
*.pyc
.venv/
.env

# Data & output
data/
output/
logs/
backups/

# System
.DS_Store
.vscode/
.idea/

# Testing
.pytest_cache/
tests/sandbox/
```

### 7.2 pre-commit obligatorio (bloquea secretos antes del commit)

Crear `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
```

InstalaciÃ³n:
- `uv add --dev pre-commit`
- `pre-commit install`
- `pre-commit run --all-files`

Regla: ningÃºn commit pasa si gitleaks detecta credenciales.

### 7.3 allowlist de lectura para agentes remotos

Si usas cualquier herramienta con modelo remoto:
- Permitir lectura solo de: `src/`, `tests/unit/`, `pyproject.toml`, `README.md`, `PROJECT.md`.
- Prohibir lectura de: `.env`, `.git/`, `data/`, `logs/`, `output/`, `backups/`, cualquier archivo con patrones `key`, `secret`, `token`, `credential`.

Si la herramienta no soporta allowlist, usar **workspace espejo sanitizado**.

### 7.4 workspace espejo sanitizado (recomendado)

- `proyecto/` (repo limpio, sin secretos)
- `proyecto_private/` (fuera de git) con `.env` real y cualquier material sensible
- Ejecutar scripts con `PROJECT_ENV_FILE` apuntando a `proyecto_private/.env`

Ejemplo (powershell):
```powershell
$env:PROJECT_ENV_FILE="C:\Users\<user>\.secrets\<project>\.env"
uv run python -m src.main
```

### 7.5 limpieza de historial si hubo secretos commiteados

Si algÃºn secreto se commiteÃ³:
- Rotar credenciales.
- Reescribir historial con `git filter-repo` (recomendado) o herramienta equivalente.
- Volver a rotar si el repo se compartiÃ³ o subiÃ³ a remoto.

Regla: borrar un archivo hoy no elimina el secreto del pasado.

## 8. flujo de trabajo del agente

### inicio

- Leer `PROJECT.md`.
- Confirmar que no hay secretos en el workspace que verÃ¡ el agente.
- Ejecutar `pre-commit run --all-files` si hubo cambios grandes o antes de merge.

### desarrollo

- Importar rutas desde `src/paths.py`.
- Importar secretos solo desde `src/settings.py`.
- Si creas scripts de un solo uso, van a `tests/sandbox/`.
- Cambios pequeÃ±os y verificables. AÃ±adir o actualizar tests si toca.

### error y debug

- Registrar hallazgos en `PROJECT.md` sin incluir datos sensibles.
- No pegar logs completos si pueden contener tokens, cookies o credenciales.
- Si hay que compartir un error, redactar. Sustituir valores por `***REDACTED***`.

## 9. checklist rÃ¡pido antes de usar un agente remoto

- [ ] No hay contraseÃ±as ni tokens en el repo.
- [ ] `.env` no existe en el workspace del agente.
- [ ] `pre-commit` instalado y `gitleaks` pasa.
- [ ] Allowlist activa o workspace espejo sanitizado.
- [ ] 2FA habilitado en correo y paneles web.

---

## 10. escalando a multi-agente

Si necesitas separar planificaciÃ³n de implementaciÃ³n, usa [`agent_system`](../../README.md):

### Beneficios del sistema multi-agente
- **Manager**: Planifica, revisa cÃ³digo, valida calidad
- **Builder**: Implementa, escribe tests, documenta
- **Controller**: Coordina turnos, ejecuta Quality Gates automÃ¡ticos
- **TÃº**: Supervisas y gestionas credenciales

### InstalaciÃ³n
```bash
python agent_system/scripts/install_agent_system.py /ruta/a/tu/proyecto
```

### ConfiguraciÃ³n de agentes
- **Manager**: Copia [`../../.manager_rules`](../../.manager_rules) a su system prompt
- **Builder**: Copia [`../../.builder_rules`](../../.builder_rules) a su system prompt

**MÃ¡s informaciÃ³n**: [`../../EMPEZAR-AQUI.md`](../../EMPEZAR-AQUI.md)

---

## Documentos Relacionados

| Documento | DescripciÃ³n |
|-----------|-------------|
| [`project-template.md`](project-template.md) | Template de estructura de proyecto |
| [`agent_seguridad.md`](agent_seguridad.md) | PolÃ­ticas de seguridad y contenciÃ³n |
| [`../../README.md`](../../README.md) | Sistema completo por etapas con compatibilidad legacy |


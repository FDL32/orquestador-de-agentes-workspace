# Template de Proyecto con Arquitectura de Seguridad

> **Este documento es independiente** pero complementario a [`agent_system`](../../README.md).
> - **Uso standalone**: Aplica esta estructura a cualquier proyecto Python con datos sensibles
> - **Con multi-agente**: Instala [`agent_system`](../../EMPEZAR-AQUI.md) para el flujo oficial por etapas

---

## RelaciÃ³n con agent_system/

| Necesitas... | Usa... |
|--------------|--------|
| Solo estructura segura de carpetas | Este documento |
| Solo reglas para un agente LLM | [`agent.md`](agent.md) |
| Solo polÃ­ticas de seguridad | [`agent_seguridad.md`](agent_seguridad.md) |
| Flujo oficial por etapas | [`../../EMPEZAR-AQUI.md`](../../EMPEZAR-AQUI.md) |

---

## Estructura de Carpetas

```text
Proyecto_Root/
â”œâ”€â”€ privada/                      # FUERA del workspace del LLM (estructura PLANA)
â”‚   â”œâ”€â”€ .env                      # Credenciales reales
â”‚   â”œâ”€â”€ config.json               # Config con rutas personales
â”‚   â”œâ”€â”€ sender_config.json        # Datos de empresa
â”‚   â””â”€â”€ remitente.json            # Otros datos sensibles
â”‚
â”œâ”€â”€ publica/                      # Workspace del LLM
â”‚   â”œâ”€â”€ repo/                     # Repositorio git
â”‚   â”‚   â”œâ”€â”€ .agent/                # Sistema multi-agente (opcional)
â”‚   â”‚   â”‚   â””â”€â”€ collaboration/      # Ver: agent_system/EMPEZAR-AQUI.md
â”‚   â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ config.py
â”‚   â”‚   â”‚   â”œâ”€â”€ settings.py
â”‚   â”‚   â”‚   â””â”€â”€ main.py
â”‚   â”‚   â”œâ”€â”€ data/
â”‚   â”‚   â”‚   â””â”€â”€ .gitkeep
â”‚   â”‚   â”œâ”€â”€ output/
â”‚   â”‚   â”‚   â””â”€â”€ .gitkeep
â”‚   â”‚   â”œâ”€â”€ logs/
â”‚   â”‚   â”‚   â””â”€â”€ .gitkeep
â”‚   â”‚   â”œâ”€â”€ tools/
â”‚   â”‚   â”‚   â””â”€â”€ pre_commit_check.py
â”‚   â”‚   â”œâ”€â”€ tests/
â”‚   â”‚   â”œâ”€â”€ .env.example
â”‚   â”‚   â”œâ”€â”€ .gitignore
â”‚   â”‚   â”œâ”€â”€ agent.md              # Reglas LLM (tomar de docs/reference/)
â”‚   â”‚   â”œâ”€â”€ agent_seguridad.md    # Seguridad (tomar de docs/reference/)
â”‚   â”‚   â”œâ”€â”€ PROJECT.md
â”‚   â”‚   â”œâ”€â”€ README.md
â”‚   â”‚   â””â”€â”€ pyproject.toml
â”‚   â”‚
â”‚   â”œâ”€â”€ {nombre_proyecto}.bat     # Lanzador universal (auto-generado)
â”‚   â”œâ”€â”€ cuarentena/
â”‚   â”‚   â””â”€â”€ .gitkeep
â”‚   â””â”€â”€ backups/
â”‚       â””â”€â”€ .gitkeep
```

---

## Archivos de Configuracion

### `.gitignore`

```gitignore
# ============================================
# SEGURIDAD - SECRETOS Y CREDENCIALES
# ============================================
.env
.env.*
*.pem
*.key
*.p12
*.kdbx
*.ovpn
*.rdp
*.ppk

# Configuracion con datos personales
config.json

# Datos de empresa reales (crear .example para cada uno)
data/sender_config.json
data/**/remitente.json
data/user_settings.json

# Scripts de debug con credenciales
debug_*.py
tests/poc_*.py

# ============================================
# PYTHON Y ENTORNO
# ============================================
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
.Python
*.egg-info/
dist/
build/

# ============================================
# CARPETAS DE SALIDA (con .gitkeep)
# ============================================
/output/*
!/output/.gitkeep
/logs/*
!/logs/.gitkeep
/backups/*
!/backups/.gitkeep

# ============================================
# IDE Y SISTEMA
# ============================================
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
desktop.ini

# ============================================
# CACHE DE HERRAMIENTAS
# ============================================
.pytest_cache/
.ruff_cache/
.mypy_cache/
```

---

### `.env.example`

```env
# Configuracion de API
API_BASE_URL=https://tu-tienda.com/api
API_KEY=tu_api_key_aqui
API_SECRET=tu_api_secret_aqui

# Configuracion de email (opcional)
SMTP_HOST=smtp.tuservidor.com
SMTP_PORT=587
SMTP_USER=tu_email@dominio.com
SMTP_PASSWORD=tu_password_aqui

# Rutas personalizadas (opcional)
OUTPUT_FOLDER=./output
```

---

## Codigo Fuente

### `src/config.py`

```python
"""Rutas centralizadas del proyecto."""
from pathlib import Path

# Rutas base
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent                          # publica/repo/
PRIVATE_DIR = ROOT_DIR.parent.parent / "privada"   # privada/ (estructura plana)

# Rutas del proyecto
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
LOGS_DIR = ROOT_DIR / "logs"

# Crear carpetas si no existen
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
```

---

### `src/settings.py`

```python
"""Configuracion y secretos con busqueda en cascada.

Busqueda en cascada:
1. privada/{nombre_archivo} - Estructura PLANA, busca por nombre
2. publica/repo/{ruta_completa} - Datos del repositorio
3. publica/repo/{ruta_completa}.example - Plantilla de ejemplo
"""
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from .config import PRIVATE_DIR, ROOT_DIR


def _load_env() -> None:
    """Carga archivos .env con busqueda en cascada."""
    # 1. Variable de entorno explicita
    env_path = os.getenv("PROJECT_ENV_FILE")
    if env_path:
        load_dotenv(Path(env_path))
        return

    # 2. Carpeta privada (estructura PLANA)
    private_env_path = PRIVATE_DIR / ".env"
    if private_env_path.exists():
        load_dotenv(private_env_path)
        return

    # 3. Raiz del proyecto
    project_env_path = ROOT_DIR / ".env"
    if project_env_path.exists():
        load_dotenv(project_env_path)


def get_config_file_path(filename: str) -> Path:
    """Obtiene ruta de archivo con busqueda en cascada.

    privada/ es PLANA: busca por nombre de archivo, no por ruta.

    Ejemplo:
        get_config_file_path("data/sender_config.json")
        -> Busca: privada/sender_config.json
        -> Luego: publica/repo/data/sender_config.json
        -> Luego: publica/repo/data/sender_config.example.json
    """
    # Extraer solo el nombre del archivo (sin ruta)
    name = Path(filename).name

    # 1. Buscar en privada/ (estructura PLANA)
    private_config_path = PRIVATE_DIR / name
    if private_config_path.exists():
        return private_config_path

    # 2. Buscar en repo/ (ruta completa)
    project_path = ROOT_DIR / filename
    if project_path.exists():
        return project_path

    # 3. Buscar .example
    example_path = ROOT_DIR / f"{filename}.example"
    if example_path.exists():
        return example_path

    return ROOT_DIR / filename


def load_json_config(filename: str) -> Dict[str, Any]:
    """Carga archivo JSON con busqueda en cascada."""
    config_path = get_config_file_path(filename)
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def require(name: str) -> str:
    """Obtiene variable de entorno requerida o lanza error."""
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v


_load_env()


@dataclass(frozen=True)
class Settings:
    """Configuracion del sistema. Personalizar segun proyecto."""
    API_BASE_URL: str = os.getenv("API_BASE_URL", "")
    API_KEY: str = os.getenv("API_KEY", "")
    # Descomentar si se necesitan variables requeridas:
    # SMTP_USER: str = require("SMTP_USER")
    # SMTP_PASS: str = require("SMTP_PASS")
```

---

### `src/main.py`

```python
"""Entry point del proyecto."""
from loguru import logger

from .config import LOGS_DIR, ROOT_DIR
from .settings import Settings

# Configurar logging
LOGS_DIR.mkdir(exist_ok=True)
logger.add(LOGS_DIR / "app.log", rotation="10 MB", retention="7 days", level="DEBUG")


def main() -> None:
    """Funcion principal."""
    logger.info("Iniciando aplicacion...")
    logger.info(f"Directorio raiz: {ROOT_DIR}")

    settings = Settings()
    logger.info(f"API URL: {settings.API_BASE_URL or '(no configurada)'}")

    # TODO: Implementar logica principal

    logger.info("Aplicacion finalizada.")


if __name__ == "__main__":
    main()
```

---

## Herramientas de Seguridad

### `tools/pre_commit_check.py`

```python
#!/usr/bin/env python3
"""
Verificacion de seguridad pre-commit.
Ejecutar antes de hacer push a GitHub.

IMPORTANTE: Personalizar PATTERNS_SENSIBLES con datos de tu empresa.
"""
import re
import subprocess
import sys
from pathlib import Path

# ============================================
# PERSONALIZAR ESTOS PATRONES POR PROYECTO
# ============================================
PATTERNS_SENSIBLES = [
    # Patrones genericos (mantener siempre)
    (r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]", "API Key"),
    (r"password\s*[:=]\s*['\"][^'\"]+['\"]", "Password"),
    (r"token\s*[:=]\s*['\"][^'\"]+['\"]", "Token"),
    (r"secret\s*[:=]\s*['\"][^'\"]+['\"]", "Secret"),

    # Patrones especificos de empresa (PERSONALIZAR)
    # (r"tu_empresa", "Nombre empresa real"),
    # (r"@tuempresa\.com", "Email empresa real"),
    # (r"ES[A-Z]\d{8}", "CIF/NIF espanol"),
    # (r"\d{9}", "Telefono real"),
]

ARCHIVOS_PROHIBIDOS = [
    ".env",
    "config.json",
    "data/sender_config.json",
    "data/user_settings.json",
]


def verificar_git_status():
    """Verifica que archivos sensibles no esten staged."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    staged = result.stdout.strip().split("\n")

    problemas = []
    for archivo in ARCHIVOS_PROHIBIDOS:
        if archivo in staged:
            problemas.append(f"BLOQUEADO: {archivo} esta en staging")

    return problemas


def escanear_contenido():
    """Busca patrones sensibles en archivos staged."""
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    diff = result.stdout

    problemas = []
    for pattern, descripcion in PATTERNS_SENSIBLES:
        if re.search(pattern, diff, re.IGNORECASE):
            problemas.append(f"DETECTADO: {descripcion}")

    return problemas


if __name__ == "__main__":
    print("Verificacion de seguridad pre-commit...")

    problemas = verificar_git_status() + escanear_contenido()

    if problemas:
        print("\nCOMMIT BLOQUEADO - Problemas de seguridad:")
        for p in problemas:
            print(f"   - {p}")
        sys.exit(1)

    print("Verificacion pasada - OK para commit")
    sys.exit(0)
```

---

### `.git/hooks/pre-commit`

```bash
#!/bin/sh
python tools/pre_commit_check.py
```

---

## Documentacion

### `pyproject.toml`

```toml
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Descripcion del proyecto"
requires-python = ">=3.10"
dependencies = [
    "loguru>=0.7.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.4.0",
    "pre-commit>=3.7.0",
]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]
ignore = ["E501"]
```

---

### `PROJECT.md` (plantilla)

```markdown
# Estado del proyecto
- **Estado**: [Estable | WIP | Roto]
- **Ultima modificacion**: AAAA-MM-DD
- **Mision actual**: que estamos resolviendo ahora

# Esquemas de datos (source of truth)
- **data/archivo.json**: [Descripcion de campos]

# Configuracion y secretos (sin valores)
- **API_KEY**: Clave de API (en .env)
- **SMTP_USER**: Correo de envio (en .env)

# Arquitectura y decisiones
- Usamos busqueda en cascada para configs (privada/ -> repo/ -> .example)
- Logs rotan cada 10MB

# Lecciones aprendidas
- [Bug] Descripcion del bug y solucion
```

---

## Checklist de Nuevo Proyecto

### Configuracion Inicial
- [ ] Crear estructura de carpetas (privada/, publica/repo/, cuarentena/)
- [ ] Copiar .gitignore
- [ ] Copiar src/config.py y src/settings.py
- [ ] Crear .env.example con variables del proyecto
- [ ] Crear pyproject.toml

### Seguridad
- [ ] Personalizar PATTERNS_SENSIBLES en pre_commit_check.py
- [ ] Instalar hook pre-commit
- [ ] Verificar que privada/ no esta en el workspace de VS Code

### Documentacion
- [ ] Crear PROJECT.md con estado inicial
- [ ] Tomar agent.md y agent_seguridad.md desde `agent_system/docs/reference/` (si usa LLM)
- [ ] Instalar agent_system/ (si usa flujo oficial por etapas o compatibilidad legacy)

### Verificacion Pre-Push
```bash
# Buscar datos sensibles
grep -ri "nombre_empresa" src/ data/ tests/
grep -ri "ES[A-Z][0-9]" src/ data/ tests/

# Ejecutar verificacion
python tools/pre_commit_check.py

# Verificar git status
git status
```

---

## Comandos Utiles

```bash
# Crear entorno virtual
uv venv

# Instalar dependencias
uv sync

# Ejecutar proyecto
uv run python -m src.main

# Ejecutar tests
uv run pytest

# Lint
uv run ruff check src/

# Instalar pre-commit hooks
uv run pre-commit install
```

---

## IntegraciÃ³n con Sistema Multi-Agente (Opcional)

Si quieres usar el flujo oficial por etapas:

```bash
# Desde z_scripts/agent_system/
python scripts/install_agent_system.py /ruta/a/tu/proyecto
```

Esto aÃ±ade:
- `.agent/` con el controller y archivos de colaboraciÃ³n
- `.manager_rules` y `.builder_rules` para configurar los agentes
- Quality Gates automÃ¡ticos (tests, linting)

**MÃ¡s informaciÃ³n**: [`../../EMPEZAR-AQUI.md`](../../EMPEZAR-AQUI.md)

---

## Documentos Relacionados

| Documento | DescripciÃ³n |
|-----------|-------------|
| [`agent.md`](agent.md) | Reglas y prompts para agentes LLM |
| [`agent_seguridad.md`](agent_seguridad.md) | PolÃ­ticas de seguridad y contenciÃ³n |
| [`../../README.md`](../../README.md) | Sistema completo por etapas con compatibilidad legacy |


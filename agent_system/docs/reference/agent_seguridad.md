# Seguridad del Workspace y ContenciÃ³n de Secretos

> **Este documento es independiente** pero complementario a [`agent_system`](../../README.md).
> Si existe `agent_system/`, en caso de conflicto con este documento, **prevalece el contenido de `agent_system/`** (especialmente `.manager_rules` y `.builder_rules`).
> - **Uso standalone**: Aplica estas polÃ­ticas a cualquier proyecto con agentes LLM
> - **Con multi-agente**: El sistema ya incluye estas reglas en `.manager_rules` y `.builder_rules`

---

## RelaciÃ³n con agent_system/

| Documento | DescripciÃ³n |
|-----------|-------------|
| Este documento | PolÃ­ticas de seguridad detalladas (referencia) |
| [`../03-SEGURIDAD.md`](../03-SEGURIDAD.md) | Resumen de seguridad para usuarios |
| [`../../.manager_rules`](../../.manager_rules) | Incluye reglas de seguridad para el Manager |
| [`../../.builder_rules`](../../.builder_rules) | Incluye reglas de seguridad para el Builder |

---

## objetivo
Este documento define un cinturÃ³n de seguridad para cualquier llm o agente que trabaje con este proyecto. Objetivos:
- evitar que credenciales (correo, webs, tokens, cookies, claves) vivan dentro del repo
- aislar material sensible fuera del workspace que indexa el llm
- habilitar una zona de cuarentena donde el llm pueda aparcar archivos sospechosos
- reducir exposiciÃ³n por logs, handoffs, escalations y mapas de proyecto

## regla 0
Asumir que cualquier texto que el agente pueda leer puede salir del equipo. No hay excepciones.

## decisiÃ³n operativa
- se mantienen tres zonas funcionales: repo, cuarentena, privada
- se agrupan bajo dos carpetas madre dentro del proyecto:
  - `publica/` (visible para el llm y editable por el agente)
  - `privada/` (fuera del workspace del llm, solo para el usuario)
- estrategia de seguridad: 
  - si se detectan seÃ±ales de secretos en el repo, se mueven a cuarentena y se avisa
  - no se bloquea el flujo automÃ¡ticamente, pero se exige revisiÃ³n humana periÃ³dica de cuarentena

## arquitectura de carpetas

### estructura final simplificada
```text
Proyecto_Root/
â”œâ”€â”€ publica/                      # carpeta de trabajo (workspace de VS Code)
â”‚   â”œâ”€â”€ repo/                     # proyecto git. solo cÃ³digo y docs sin secretos
â”‚   â”‚   â”œâ”€â”€ .env.example
â”‚   â”‚   â”œâ”€â”€ config.example.json
â”‚   â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”‚   â””â”€â”€ settings.py       # â­ BÃºsqueda en cascada
â”‚   â”‚   â””â”€â”€ data/
â”‚   â”‚       â”œâ”€â”€ sender_config.example.json
â”‚   â”‚       â””â”€â”€ Agencias/*/remitente.example.json
â”‚   â”œâ”€â”€ cuarentena/               # staging. el llm puede escribir aquÃ­
â”‚   â””â”€â”€ backups/                  # opcional. gitignored
â”‚
â””â”€â”€ privada/                      # fuera del workspace. ESTRUCTURA PLANA
    â”œâ”€â”€ .env                      # Credenciales reales
    â”œâ”€â”€ config.json               # Config con rutas personales
    â”œâ”€â”€ sender_config.json        # Datos de empresa
    â””â”€â”€ remitente.json            # Datos de remitente
```

### principio de simplicidad
La carpeta `privada/` es **PLANA** (sin subdirectorios). Todos los archivos sensibles van directamente en `privada/`. El cÃ³digo busca por **nombre de archivo**:

1. `privada/{nombre_archivo}` â†’ Datos reales (ej: `privada/sender_config.json`)
2. `publica/repo/{ruta_completa}` â†’ Datos del repo
3. `publica/repo/{ruta_completa}.example` â†’ Plantilla

## definiciones operativas

### quÃ© es sensible
Cualquier archivo o fragmento que contenga:
- passwords, pass, pwd, token, api_key, secret, bearer, authorization, cookie
- urls con credenciales: `https://user:pass@host`
- claves: `BEGIN ... PRIVATE KEY`, `.pem`, `.key`, `.p12`, `.kdbx`
- credenciales de correo, paneles web, marketplaces, ftp, ssh, db, smtp
- **datos de empresa/cliente**: nombre real, CIF/NIF, direcciÃ³n fÃ­sica, telÃ©fono, email corporativo
- **identificadores en cÃ³digo** que revelen identidad: `MailEmpresaReal`, `configCliente`, URLs de tienda

### quÃ© NO es sensible pero debe verificarse
- Identificadores genÃ©ricos: `MailRemitente`, `configSender`, `get_sender_email()`
- URLs placeholder: `https://tu-tienda.com/api`
- Datos de ejemplo: `Tu Empresa S.L.`, `Calle Principal 123`, `ESB00000000`

### patrones y extensiones de alto riesgo
Extensiones comunes donde aparecen secretos:
`.env`, `.pem`, `.key`, `.p12`, `.kdbx`, `.ovpn`, `.rdp`, `.ppk`, `.sqlite`, `.log`, `.txt`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.py`

Nombres comunes:
`secrets`, `private`, `password`, `cred`, `token`, `cookies`, `auth`, `login`, `accounts`, `keys`, `backup`

## reglas para llm y agentes (pÃ©galas al inicio de cualquier sesiÃ³n)
### prohibiciones
- prohibido abrir, leer, listar o inferir contenido de:
  - `publica/cuarentena/` (salvo para mover y registrar metadatos)
  - `privada/` completo
  - `.env`, `.env.*`, `.git/`, `.venv/`, `data/`, `logs/`, `output/`
- prohibido pedir al usuario que pegue credenciales, tokens, cookies o capturas con datos sensibles
- prohibido incluir valores sensibles en:
  - `work_plan.md`, `execution_log.md`, `review_queue.md`, `notifications.md`
- prohibido pegar logs completos si podrÃ­an contener auth, cookies o passwords

### reglas de redacciÃ³n
Si hay que referirse a algo sensible:
- sustituir valores por `***REDACTED***`
- conservar solo metadatos: nombre de variable, ruta relativa, tipo de secreto (smtp, web, api)

## estrategia "repo limpio"

### reglas duras
- cero secretos en `publica/repo`
- cero identificadores de empresa en cÃ³digo (usar genÃ©ricos)
- `.env` real no vive en el repo. solo existe `.env.example` sin valores
- cada archivo sensible tiene su `.example` correspondiente
- si una credencial o dato de empresa aparece en cÃ³digo o docs, se considera incidente operativo

### bÃºsqueda en cascada obligatoria

El cÃ³digo DEBE usar funciones de bÃºsqueda en cascada para leer configuraciÃ³n:

```python
# En src/settings.py
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent  # publica/repo/
PRIVATE_DIR = ROOT_DIR.parent.parent / "privada"   # privada/ (PLANA)

def get_config_file_path(filename: str) -> Path:
    """Busca archivo de configuraciÃ³n en cascada.

    privada/ es PLANA: busca por nombre de archivo, no por ruta.
    """
    # Extraer solo el nombre del archivo
    name = Path(filename).name

    # 1. privada/{nombre} - estructura plana
    private_path = PRIVATE_DIR / name
    if private_path.exists():
        return private_path

    # 2. publica/repo/{ruta_completa}
    repo_path = ROOT_DIR / filename
    if repo_path.exists():
        return repo_path

    # 3. publica/repo/{ruta}.example
    example_path = ROOT_DIR / f"{filename}.example"
    if example_path.exists():
        return example_path

    return repo_path  # FallarÃ¡ al leer

def get_sender_email() -> str:
    """Obtiene email del remitente desde config."""
    # Pide "data/sender_config.json" pero busca "sender_config.json" en privada/
    config = load_json_config("data/sender_config.json")
    return config.get("sender", {}).get("email", "")
```

### uso en cÃ³digo

```python
# MAL âŒ
email = "info@empresareal.es"
field_name = "MailEmpresaReal"

# BIEN âœ…
from .settings import get_sender_email
email = get_sender_email()
field_name = "MailRemitente"
```

### ejecuciÃ³n
El cÃ³digo busca automÃ¡ticamente en `privada/config/`:
```powershell
# Desde publica/repo/
uv run python -m src.main
```

## acciones automatizables

### paso 1. crear carpetas
Ejecuta desde `Codigo_python/`:

```powershell
New-Item -ItemType Directory -Force -Path ".\publica\repo" | Out-Null
New-Item -ItemType Directory -Force -Path ".\publica\cuarentena" | Out-Null
New-Item -ItemType Directory -Force -Path ".\publica\backups" | Out-Null
New-Item -ItemType Directory -Force -Path ".\privada" | Out-Null

"OK: estructura creada"
```

### paso 2. gitignore robusto (dentro de `publica/repo`)
En `publica/repo/.gitignore` asegurar:

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

# ConfiguraciÃ³n con datos personales
config.json

# Datos de empresa reales (cada uno tiene .example)
data/sender_config.json
data/**/remitente.json
data/user_settings.json
data/listado_productos.xlsx

# Scripts de debug con credenciales
debug_*.py
tests/poc_*.py

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
# PYTHON Y CACHE
# ============================================
__pycache__/
*.pyc
.venv/
.pytest_cache/
.ruff_cache/
.mypy_cache/

# ============================================
# IDE Y SISTEMA
# ============================================
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Nota: `.gitignore` evita commits. no evita lectura por llm. el aislamiento real lo da el workspace.

### paso 3. escaneo y mover a cuarentena (opciÃ³n A, sin bloqueo)
Crear `publica/repo/tools/security_quarantine.ps1` (ejecutar desde `publica/repo`):

```powershell
param(
  [string]$RepoRoot = (Get-Location).Path
)

# carpeta cuarentena estÃ¡ fuera del repo, pero dentro de publica
$cuarentena = (Resolve-Path "$RepoRoot\..\cuarentena").Path
New-Item -ItemType Directory -Force -Path $cuarentena | Out-Null

# extensiones a revisar (texto y configs mÃ¡s comunes)
$exts = @("*.env","*.md","*.txt","*.json","*.yaml","*.yml","*.toml","*.ini","*.cfg","*.py","*.log")

# regex de alta seÃ±al (no muestra valores)
$patterns = @(
  "(?i)\b(password|passwd|pass|pwd)\s*[:=]",
  "(?i)\b(api[_-]?key|secret|token)\s*[:=]",
  "(?i)\bauthorization\s*[:=]\s*(bearer\s+)?",
  "(?i)\bcookie\s*[:=]",
  "https?://[^\s/:]+:[^\s@]+@",
  "BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"
)

$hits = @()

foreach ($ext in $exts) {
  Get-ChildItem -Path $RepoRoot -Recurse -File -Filter $ext -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\\.git\\" -and $_.FullName -notmatch "\\.venv\\" } |
    ForEach-Object {
      try {
        $content = Get-Content -LiteralPath $_.FullName -Raw -ErrorAction Stop
        foreach ($p in $patterns) {
          if ($content -match $p) { $hits += $_.FullName; break }
        }
      } catch {}
    }
}

$hits = $hits | Sort-Object -Unique

if ($hits.Count -eq 0) {
  Write-Host "OK: no se detectaron secretos evidentes."
  exit 0
}

Write-Host "AVISO: se detectaron archivos con seÃ±ales de secretos. moviendo a cuarentena:"
foreach ($f in $hits) {
  $rel = $f.Substring($RepoRoot.Length).TrimStart("\\")
  $dest = Join-Path $cuarentena $rel
  New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
  Move-Item -LiteralPath $f -Destination $dest -Force
  Write-Host " - moved: $rel"
}

Write-Host ""
Write-Host "pendiente: revisar publica\cuarentena y mover lo sensible a privada\vault manualmente."
exit 2
```

### paso 4. revisiÃ³n humana de cuarentena
Regla:
- todo lo sensible confirmado se mueve desde `publica/cuarentena` a `privada/` (estructura plana)
- el repo debe quedarse con placeholders, nombres de variables y `.env.example`
- no ejecutar nada leyendo secretos desde cuarentena

## integraciÃ³n con el sistema multi-agente

> **Nota**: Si usas [`agent_system`](../../README.md), estas reglas ya estÃ¡n incluidas en
> `.manager_rules` y `.builder_rules`. Esta secciÃ³n es referencia para entender el diseÃ±o.

### responsabilidad del controller ([`agent_controller.py`](../../.agent/agent_controller.py))
- generar `project_map` solo desde `publica/repo`
- ignorar `publica/cuarentena`, `publica/backups` y cualquier ruta fuera del repo
- incluir un aviso si existe contenido en `publica/cuarentena` (pendiente de revisiÃ³n)

### responsabilidad del manager ([`.manager_rules`](../../.manager_rules))
- no aprobar work plans que introduzcan credenciales en el repo
- exigir redacciÃ³n de logs y metadatos sin valores

### responsabilidad del builder ([`.builder_rules`](../../.builder_rules))
- no pegar logs completos si pueden contener auth o cookies
- no usar identificadores que revelen nombre de empresa/cliente
- usar funciones de bÃºsqueda en cascada para leer configs
- crear archivos `.example` para cada config sensible
- si el builder detecta un secreto o dato de empresa en el repo:
  - mover archivo a `privada/` (estructura plana, no cuarentena)
  - crear versiÃ³n `.example` con datos ficticios
  - refactorizar cÃ³digo para usar bÃºsqueda en cascada
  - notificar en `notifications.md` con ruta y tipo de seÃ±al (sin valor)

## checklist operativo (diario)
- [ ] VS Code abierto en `Codigo_python/publica` o en workspace limitado. nunca en `Codigo_python`
- [ ] `publica/repo` sin `.env` real ni contraseÃ±as en cÃ³digo o docs
- [ ] `tools/security_quarantine.ps1` ejecutado antes de usar agentes remotos en repos con cambios
- [ ] `publica/cuarentena` revisada y vaciada con periodicidad (ideal: diaria)
- [ ] 2fa activo en correo y paneles web

## checklist pre-publicaciÃ³n (antes de subir a GitHub)

### verificaciÃ³n de datos sensibles
```bash
# Buscar nombre de empresa (personalizar)
grep -ri "nombre_empresa_real" src/ data/ tests/

# Buscar CIF/NIF
grep -ri "ES[A-Z][0-9]{8}" src/ data/ tests/

# Buscar direcciones
grep -ri "calle_real" src/ data/ tests/

# Buscar telÃ©fonos (9 dÃ­gitos)
grep -ri "[0-9]{9}" src/ data/ tests/
```

### verificaciÃ³n de estructura
- [ ] Cada archivo sensible tiene su `.example`
- [ ] `src/settings.py` usa bÃºsqueda en cascada
- [ ] No hay identificadores con nombre de empresa en cÃ³digo
- [ ] `.gitignore` excluye todos los archivos sensibles
- [ ] `tools/pre_commit_check.py` personalizado con patrones de la empresa
- [ ] Hook pre-commit instalado

### verificaciÃ³n final
```bash
# Ejecutar verificaciÃ³n de seguridad
python tools/pre_commit_check.py

# Verificar git status
git status  # No debe mostrar archivos sensibles

# Simular lo que se subirÃ­a
git diff --cached --name-only
```

## lecciones aprendidas

### errores comunes detectados
1. **Identificadores en cÃ³digo**: Usar `MailEmpresaReal` en lugar de `MailRemitente`
2. **URLs hardcodeadas**: Dejar URL real en documentaciÃ³n o tests
3. **Datos en tests**: Usar datos reales de empresa en tests unitarios
4. **Email templates**: Incluir nombre de empresa en plantillas
5. **JSON de configuraciÃ³n**: Olvidar crear versiÃ³n `.example`

### soluciÃ³n sistemÃ¡tica
1. Buscar patrones con grep ANTES de cualquier commit
2. Usar bÃºsqueda en cascada para TODA configuraciÃ³n
3. Crear `.example` INMEDIATAMENTE al crear archivo sensible
4. Renombrar identificadores a versiones genÃ©ricas

---

## instalaciÃ³n del sistema multi-agente

Si quieres usar el flujo oficial por etapas con estas politicas de seguridad integradas:

```bash
python agent_system/scripts/install_agent_system.py /ruta/a/tu/proyecto
```

Esto crea la estructura `publica/` + `privada/` automÃ¡ticamente y configura:
- Quality Gates con verificaciÃ³n de seguridad
- Reglas de seguridad en `.manager_rules` y `.builder_rules`
- Protocolo de escalaciÃ³n si se detectan secretos

**MÃ¡s informaciÃ³n**: [`../../EMPEZAR-AQUI.md`](../../EMPEZAR-AQUI.md)

---

## Documentos Relacionados

| Documento | DescripciÃ³n |
|-----------|-------------|
| [`project-template.md`](project-template.md) | Template de estructura de proyecto |
| [`agent.md`](agent.md) | Reglas y prompts para agentes LLM |
| [`../../README.md`](../../README.md) | Sistema completo por etapas con compatibilidad legacy |
| [`../03-SEGURIDAD.md`](../03-SEGURIDAD.md) | Resumen de seguridad para usuarios |


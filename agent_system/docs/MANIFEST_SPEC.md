# MANIFEST_SPEC.md - EspecificaciÃ³n TÃ©cnica del Sistema de Manifiestos

## IntroducciÃ³n

Esta especificaciÃ³n define el contrato tÃ©cnico para los manifiestos del sistema multiagente. Los manifiestos aseguran consistencia, detecciÃ³n automÃ¡tica y upgrade seguro entre proyectos y versiones del sistema.

- **VersiÃ³n mÃ­nima del sistema**: 8.0 (soporte inicial de manifiestos).
- **UbicaciÃ³n**: `.agent/project_manifest.toml` y `.agent/.version_manifest.json`.
- **Autoridad**: `.agent` gobierna todos los aspectos; conflictos se resuelven priorizando el manifest.

## project_manifest.toml

Contrato estable del proyecto. Define configuraciÃ³n canÃ³nica, rutas y dependencias. No se modifica con upgrades del sistema.

### Campos y Tipos

| Campo | Tipo | Obligatorio | DescripciÃ³n | Validaciones |
|-------|------|-------------|-------------|--------------|
| [project] | SecciÃ³n | SÃ­ | InformaciÃ³n bÃ¡sica del proyecto | |
| project.name | String | SÃ­ | Nombre del proyecto | AlfanumÃ©rico, sin espacios especiales |
| project.version | String | SÃ­ | VersiÃ³n semÃ¡ntica del proyecto | Formato SemVer (e.g., "1.0.0") |
| project.description | String | No | DescripciÃ³n breve | MÃ¡ximo 200 caracteres |
| [paths] | SecciÃ³n | SÃ­ | Rutas canÃ³nicas | Todas relativas al root |
| paths.root | String | SÃ­ | Directorio raÃ­z | Siempre "." |
| paths.agent_dir | String | SÃ­ | Directorio del sistema agente | Siempre ".agent" |
| paths.claude_dir | String | No | Directorio de integraciÃ³n Claude | ".claude" por defecto |
| paths.scripts_dir | String | No | Directorio de scripts | "scripts" por defecto |
| paths.tests_dir | String | No | Directorio de tests | "tests" por defecto |
| paths.src_dir | String | No | Directorio fuente | "src" por defecto |
| [dependencies] | SecciÃ³n | No | Dependencias del proyecto | |
| dependencies.python | String | No | VersiÃ³n mÃ­nima de Python | Formato ">=3.10" |
| dependencies.frameworks | Array<String> | No | Frameworks principales | Lista de nombres |
| [security] | SecciÃ³n | SÃ­ | ConfiguraciÃ³n de seguridad | |
| security.allowlist | Array<String> | SÃ­ | Rutas permitidas | Patrones glob (e.g., ["scripts/", "src/"]) |
| security.denylist | Array<String> | SÃ­ | Rutas bloqueadas | Patrones glob (e.g., ["privada/", ".env"]) |
| [metadata] | SecciÃ³n | No | Metadatos opcionales | |
| metadata.created_at | String | No | Fecha de creaciÃ³n | Formato ISO 8601 |
| metadata.updated_at | String | No | Fecha de Ãºltima actualizaciÃ³n | Formato ISO 8601 |

### Validaciones Generales

- Todos los paths son relativos al root del proyecto.
- No incluir rutas absolutas ni personales.
- No incluir secretos, tokens o credenciales.
- Array<String> para listas, con elementos no vacÃ­os.
- Strings sin caracteres de control.

### Valores Permitidos

- project.version: SemVer vÃ¡lido.
- paths.root: Siempre ".".
- paths.agent_dir: Siempre ".agent".
- security.allowlist/denylist: Patrones vÃ¡lidos para pathlib.glob.

## .version_manifest.json

Estado tÃ©cnico del sistema instalado. Registra versiones, status y confidence. Actualizado automÃ¡ticamente por herramientas.

### Campos y Tipos

| Campo | Tipo | Obligatorio | DescripciÃ³n | Validaciones |
|-------|------|-------------|-------------|--------------|
| agent_core_version | String | SÃ­ | VersiÃ³n del nÃºcleo agente | SemVer |
| template_version | String | SÃ­ | VersiÃ³n de la plantilla | SemVer |
| status | String | SÃ­ | Estado del sistema | Valores: "canonical", "recovered", "unknown" |
| confidence | String | SÃ­ | Nivel de certidumbre | Valores: "high", "medium", "low", "recovered_from_markers" |
| last_updated | String | SÃ­ | Timestamp de Ãºltima actualizaciÃ³n | ISO 8601 con timezone |
| components | Object | SÃ­ | Versiones de componentes | |
| components.agent_controller | String | SÃ­ | VersiÃ³n del controlador | SemVer |
| components.hooks | String | SÃ­ | VersiÃ³n de hooks | SemVer |
| components.rules | String | SÃ­ | VersiÃ³n de reglas | SemVer |
| markers_validated | Boolean | SÃ­ | Si markers legacy fueron validados | true/false |
| drift_detected | Boolean | SÃ­ | Si se detectÃ³ drift | true/false |

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "agent_core_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "template_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "status": {
      "type": "string",
      "enum": ["canonical", "recovered", "unknown"]
    },
    "confidence": {
      "type": "string",
      "enum": ["high", "medium", "low", "recovered_from_markers"]
    },
    "last_updated": {
      "type": "string",
      "format": "date-time"
    },
    "components": {
      "type": "object",
      "properties": {
        "agent_controller": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "hooks": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "rules": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        }
      },
      "required": ["agent_controller", "hooks", "rules"]
    },
    "markers_validated": {
      "type": "boolean"
    },
    "drift_detected": {
      "type": "boolean"
    }
  },
  "required": [
    "agent_core_version",
    "template_version",
    "status",
    "confidence",
    "last_updated",
    "components",
    "markers_validated",
    "drift_detected"
  ]
}
```

### Validaciones Generales

- Todas las versiones en formato SemVer (e.g., "1.0.0").
- last_updated en formato ISO 8601 con timezone (e.g., "2026-04-28T21:42:57+02:00").
- No incluir rutas absolutas ni secretos.
- Status y confidence separados: status indica estado, confidence indica certidumbre.

### Valores Permitidos

- status: "canonical" (instalaciÃ³n estÃ¡ndar), "recovered" (reparado), "unknown" (no determinado).
- confidence: "high" (alta certidumbre), "medium", "low", "recovered_from_markers" (origen no-canÃ³nico).

## Reglas de Autoridad

### Para Rutas

- project_manifest.toml prevalece: Cualquier detecciÃ³n heurÃ­stica debe coincidir.
- Discrepancias = drift: Reportar como WARNING, sugerir repair.
- Repair solo con --confirm: Actualiza status a "recovered", confidence a "recovered_from_markers".

### Para Status y Confidence

- Solo herramientas autorizadas (upgrade, doctor --repair-manifest, migrate) pueden modificar.
- Status refleja estado real del sistema.
- Confidence refleja origen y validaciÃ³n de la informaciÃ³n.
- Cambios auditados en execution_log.md con timestamp.

### Autoridad General

- .agent es autoridad Ãºnica para manifests y estado tÃ©cnico.
- .claude consume pero no modifica.
- Conflicto: Priorizar .agent; regenerar .claude si diverge.

## Compatibilidad Futura

- **VersiÃ³n mÃ­nima**: Sistema 8.0 soporta manifiestos; versiones anteriores usan markers legacy.
- **Backward compatibility**: Manifests antiguos vÃ¡lidos si cumplen schema mÃ­nimo.
- **Forward compatibility**: Nuevos campos opcionales; herramientas ignoran desconocidos.
- **Upgrade path**: doctor_agent_system.py detecta versiones, upgrade_agent_system.py migra schema.
- **Deprecation**: Campos obsoletos marcados en changelog; removidos en versiones mayores.

## Ejemplos

### project_manifest.toml Completo

```toml
[project]
name = "mi_proyecto"
version = "1.0.0"
description = "Proyecto multiagente de ejemplo"

[paths]
root = "."
agent_dir = ".agent"
claude_dir = ".claude"
scripts_dir = "scripts"
tests_dir = "tests"
src_dir = "src"

[dependencies]
python = ">=3.10"
frameworks = ["fastapi", "pydantic"]

[security]
allowlist = ["scripts/", "src/"]
denylist = ["privada/", ".env"]

[metadata]
created_at = "2026-04-28T21:42:57+02:00"
updated_at = "2026-04-28T21:42:57+02:00"
```

### .version_manifest.json Completo

```json
{
  "agent_core_version": "8.2",
  "template_version": "1.0",
  "status": "canonical",
  "confidence": "high",
  "last_updated": "2026-04-28T21:42:57+02:00",
  "components": {
    "agent_controller": "1.0.0",
    "hooks": "1.0.0",
    "rules": "1.0.0"
  },
  "markers_validated": true,
  "drift_detected": false
}
```

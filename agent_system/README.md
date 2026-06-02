# Sistema Multi-Agente

> Desarrollo asistido por agentes con Goose como runtime y orquestacion por etapas.

## Estado actual

El sistema recomendado ya no es solo el ciclo manual `Manager -> Builder`.
El flujo oficial es:

`plan -> build -> review -> validate`

Se ejecuta mediante `scripts/orquestador.py` usando:
- `--stage` para una etapa
- `--run-pipeline` para la secuencia completa

El flujo clasico Manager/Builder sigue disponible, pero queda como compatibilidad para proyectos antiguos o sesiones manuales.

## Inicio rapido

```powershell
# Instalar en un proyecto
python scripts/install_agent_system.py C:\ruta\al\proyecto

# Verificar el stage build sin ejecutar
cd C:\ruta\al\proyecto
python scripts/orquestador.py --stage build --query "Implementa el ticket activo" --dry-run

# Pipeline completo
python scripts/orquestador.py --run-pipeline --query "Implementa y valida el ticket activo" --progress

# Ejecutar skill directamente (v2.4+)
python scripts/orquestador.py --skill /implement --query "Implementa la funcionalidad requerida"
```

## Skills Disponibles

**13 micro-skills reutilizables** por rol:

### Builder Skills

| Skill | DescripciÃ³n | Triggers |
|-------|-------------|----------|
| `bui-implement-from-plan` | Ejecutar plan aprobado | `/implement`, `implement` |
| `bui-run-quality-gates` | ValidaciÃ³n completa (ruff, pytest) | `/gates`, `/quality`, `quality-gates` |
| `bui-self-audit` | AuditorÃ­a pre-completitud | `/audit`, `self-audit` |

### Manager Skills

| Skill | DescripciÃ³n | Triggers |
|-------|-------------|----------|
| `man-create-work-plan` | Crear plan con alcance | `/plan`, `create-plan` |
| `man-review-implementation` | Revisar cambios | `/review`, `code-review` |
| `man-resolve-escalation` | Resolver bloqueos | `/escalate`, `escalation` |

### Meta & Setup Skills

| Skill | DescripciÃ³n | Triggers |
|-------|-------------|----------|
| `create-agent-skill` | Crear nueva micro-skill | `/create-skill`, `skill-create` |
| `graphify` | Generar mapas del proyecto | `/graphify`, `graph`, `map` |
| `scaffold-python-project` | Crear proyecto Python | `/scaffold`, `new-project` |
| `setup-agent-system` | Instalar agentes | `/setup`, `agent-setup` |
| `secure-existing-project` | Asegurar proyecto | `/secure`, `security` |
| `version-changelog` | Actualizar changelog | `/changelog`, `version` |
| `project-finalize` | Cerrar proyecto | `/finalize`, `close` |

### Invocar Skills

**Option 1: Via Goose (tools completos)**
```bash
python scripts/orquestador.py --engine goose --query "Implementa el plan"
```

**Option 2: Via CLI (workflow reference)**
```bash
python scripts/orquestador.py --skill /implement --query "..."
```

**Option 3: Ver lista completa**
```bash
python scripts/discover_skills.py --goose      # Lista triggers
python scripts/discover_skills.py --markdown   # Tabla para docs
```

---

## Principios

- Goose es el runtime unico.
- El modelo se resuelve por etapa via `GOOSE_MODEL`.
- Los modelos adicionales se registran en `.agent/known_models.json`.
- La seguridad depende del perfil derivado por etapa:
  - `readonly`
  - `write-scoped`
  - `readonly-diff`
  - `exec-only`

## Documentacion principal

- [EMPEZAR-AQUI.md](EMPEZAR-AQUI.md)
- [docs/00-INDICE.md](docs/00-INDICE.md)
- [docs/01-INSTALACION.md](docs/01-INSTALACION.md)
- [docs/02-GUIA-COMPLETA.md](docs/02-GUIA-COMPLETA.md)
- [docs/03-SEGURIDAD.md](docs/03-SEGURIDAD.md)
- [docs/04-FAQ.md](docs/04-FAQ.md)

## Tests Windows-Safe

`agent_system` incluye un kit reutilizable para estabilizar `pytest` en Windows.

Incluye:
- plantillas para `tests/conftest.py` y `tests/_temp_runtime.py`
- runner `scripts/run_pytest_safe.py`
- `install_tests.py` para proyectos existentes
- `scaffold_tests.py` para proyectos nuevos
- smoke test para validar el runtime temporal

Uso rapido:

```powershell
# Proyecto existente
python scripts/install_tests.py C:\ruta\proyecto

# Proyecto nuevo
python scripts/scaffold_tests.py C:\ruta\proyecto

# Validacion recomendada en el proyecto destino
python scripts\run_pytest_safe.py tests\unit\test_windows_safe_temp_runtime.py -q -p no:cacheprovider
```

Documentacion:
- [docs/tests/INDEX.md](docs/tests/INDEX.md)
- [docs/tests/README.md](docs/tests/README.md)
- [docs/tests/IMPLEMENTACION.md](docs/tests/IMPLEMENTACION.md)
- [docs/tests/RESUMEN.md](docs/tests/RESUMEN.md)

## Compatibilidad legacy

El sistema clasico de agentes separados sigue existiendo:
- Manager crea el plan
- Builder implementa
- Manager revisa

Pero la documentacion prioriza ya el orquestador v2.5 por etapas.

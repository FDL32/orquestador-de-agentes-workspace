# Guia de Instalacion

## Requisitos

- Python 3.10+
- Goose CLI configurado
- proyecto con workspace accesible

## Instalacion

```powershell
python scripts/install_agent_system.py C:\ruta\al\proyecto
```

Esto instala:
- `.agent/`
- `.claude/`
- reglas base
- `scripts/orquestador.py`
- `scripts/run_pytest_safe.py`
- `.agent_allowlist.json`
- `.agent_denylist.json`
- `.agent/known_models.json`

## Verificacion inicial

```powershell
cd C:\ruta\al\proyecto
python scripts/orquestador.py --stage build --query "Implementa el ticket activo" --dry-run
```

Debe resolver:
- stage
- mode
- risk
- security profile
- modelo pedido
- modelo efectivo

## Known models

Edita `.agent/known_models.json` si quieres registrar modelos adicionales.

Ejemplo:

```json
[
  "claude-sonnet-4-6",
  "claude-haiku-4-5",
  "kilo-code",
  "codex"
]
```


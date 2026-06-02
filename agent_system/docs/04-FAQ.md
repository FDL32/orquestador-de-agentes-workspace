# FAQ

## Como empiezo

Usa:

```powershell
python scripts/orquestador.py --stage build --query "Implementa el ticket activo" --dry-run
```

## Como ejecuto todo el flujo

```powershell
python scripts/orquestador.py --run-pipeline --query "Implementa y valida el ticket activo" --progress
```

## Por que usa fallback de modelo

Porque el modelo pedido no esta en `.agent/known_models.json`.

## Como evito fallback

1. AÃ±ade el modelo a `.agent/known_models.json`
2. o usa `--strict-model` para fallar si no existe

## Como veo progreso

- `--stream`
- `--progress`

## El flujo Manager/Builder ha desaparecido

No. Sigue por compatibilidad, pero la documentacion oficial prioriza el flujo por etapas.


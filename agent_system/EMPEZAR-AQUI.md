# Empieza Aqui

> Lee esto en 2 minutos. Si solo sigues un flujo, sigue el de etapas.

## Que es esto

Un sistema para trabajar con agentes de forma segura y repetible.

Flujo oficial:

`plan -> build -> review -> validate`

Runtime:
- `goose`

Modelo:
- se resuelve por etapa via `GOOSE_MODEL`

## Primer uso

### 1. Instala el sistema

```powershell
python scripts/install_agent_system.py C:\ruta\al\proyecto
```

### 2. Ve al proyecto

```powershell
cd C:\ruta\al\proyecto
```

### 3. Comprueba configuracion

```powershell
python scripts/orquestador.py --stage build --query "Implementa el ticket activo" --dry-run
```

Debes ver:
- `stage`
- `mode`
- `risk`
- `security`
- `requested_model`
- `resolved_model`

### 4. Ejecuta el pipeline

```powershell
python scripts/orquestador.py --run-pipeline --query "Implementa y valida el ticket activo" --progress
```

### 5. Ejecuta skills directamente (v2.4+)

```powershell
# Ejecutar skill especÃ­fica
python scripts/orquestador.py --skill /implement --query "Implementa la funcionalidad requerida"

# Ver skills disponibles
python scripts/discover_skills.py --goose
```

## Que necesita el ticket

Antes de delegar `build` o `validate`, el ticket debe incluir:
- `Archivos permitidos`
- `Criterios de aceptacion`
- `Verificacion obligatoria`

## Modelos conocidos

El sistema consulta:

`.agent/known_models.json`

Ejemplo:

```json
[
  "claude-sonnet-4-6",
  "claude-haiku-4-5",
  "kilo-code",
  "codex"
]
```

Si el modelo pedido no existe:
- con `--strict-model`: falla
- sin `--strict-model`: usa `fallback_model`

## Observabilidad

- `--stream`: salida en vivo del runtime
- `--progress`: heartbeat y archivos tocados

## Legacy

Si mantienes un proyecto antiguo, todavia puedes usar el flujo manual Manager/Builder.
Pero para proyectos nuevos, usa el flujo por etapas.


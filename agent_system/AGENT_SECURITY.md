# AGENT_SECURITY.md

## Objetivo

Aplicar minimo privilegio a un flujo de agentes por etapas.

## Flujo oficial

`plan -> build -> review -> validate`

Cada etapa deriva:
- `mode`
- `risk`
- `security_profile`
- `GOOSE_MODEL`

## Reglas duras

- Nunca tocar secretos ni `.env`.
- Nunca escribir fuera del workspace.
- Nunca ejecutar comandos destructivos sin aprobacion humana.
- Nunca asumir que un MCP externo es seguro por defecto.

## Perfiles de seguridad

### plan
- `mode`: `research`
- `security_profile`: `readonly`

### build
- `mode`: `write`
- `security_profile`: `write-scoped`

### review
- `mode`: `research`
- `security_profile`: `readonly-diff`

### validate
- `mode`: `validate`
- `security_profile`: `exec-only`

## Modelos

Los modelos conocidos o permitidos se registran en:

`.agent/known_models.json`

Si un modelo no existe:
- `--strict-model` fuerza error
- sin `--strict-model` se usa `fallback_model`

## Observabilidad

- `--stream`
- `--progress`

Mejoran visibilidad, no permisos.


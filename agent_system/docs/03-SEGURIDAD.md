# Guia de Seguridad

## Principio

Seguridad por minimo privilegio y por etapa.

## Etapas y permisos

- `plan`: solo lectura
- `build`: escritura acotada al ticket
- `review`: solo lectura del diff y artefactos
- `validate`: ejecucion de quality gates

## Controles

- `.agent_allowlist.json`
- `.agent_denylist.json`
- `.agent/known_models.json`
- hooks de Claude Code

## Modelos

El modelo se resuelve por etapa.

Si no existe en `.agent/known_models.json`:
- `--strict-model` falla
- sin `--strict-model` usa fallback

## Observabilidad segura

- `--stream`
- `--progress`

Solo muestran actividad. No amplian permisos ni contexto.


# Guia Completa

## Flujo oficial

`plan -> build -> review -> validate`

### plan
- define alcance
- riesgos
- criterios de aceptacion

### build
- implementa solo el ticket
- escribe solo dentro de `Archivos permitidos`

### review
- revisa diff, consistencia y gaps

### validate
- ejecuta `Verificacion obligatoria`
- decide si el ticket puede cerrarse

## Ejemplos

```powershell
python scripts/orquestador.py --stage plan --query "Define el ticket activo"
python scripts/orquestador.py --stage build --query "Implementa el ticket activo" --stream
python scripts/orquestador.py --stage review --query "Revisa el ticket activo"
python scripts/orquestador.py --stage validate --query "Valida el ticket activo" --progress
```

Pipeline:

```powershell
python scripts/orquestador.py --run-pipeline --query "Implementa y valida el ticket activo"
```

Skills directas (v2.4+):

```powershell
# Ejecutar skill especÃ­fica
python scripts/orquestador.py --skill /implement --query "Implementa la funcionalidad"

# Ver triggers disponibles
python scripts/discover_skills.py --goose
```

## Legacy

El flujo Manager/Builder manual sigue vivo para proyectos antiguos, pero ya no es la ruta principal.


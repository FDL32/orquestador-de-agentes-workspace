Ejecuta los Quality Gates del proyecto en este orden y muestra el resultado de cada paso:

```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
pytest tests/unit/ -v
```

Si algÃºn paso falla:
- Muestra el error completo
- Explica la causa mÃ¡s probable
- Propone la correcciÃ³n concreta (no solo "revisa el error")

Si todos pasan, confirma con un resumen: N tests pasados, 0 errores ruff, formato correcto.

Nota: Si `tests/unit/` no existe, usa `pytest tests/ -v` como fallback. Si no hay tests, indica que el proyecto carece de cobertura.


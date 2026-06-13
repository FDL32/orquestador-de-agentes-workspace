# AUDIT WOT-AUDIT-CI - CI portable bajo host-extends

## Objetivo del audit
Verificar que el CI del destino deja de depender de copias locales del motor y
valida estado real del destino via motor publico, con evidencia de run real.

## Reglas de revision
- Revisar el YAML real, no el relato.
- Confirmar que no quedan gates sobre `scripts/`/`tests/`/`skills/` locales.
- Confirmar que el run real (gh) cierra en success, no asumirlo.
- Confirmar que no se anadieron secretos ni se toco el motor.

## Hallazgos bloqueantes tipicos
- CRITICO: el run real falla y se cierra el ticket igual (falso verde).
- CRITICO: el CI sigue dependiendo de copias locales (no desbloquea A2d).
- ALTO: validate del motor en Actions sin deps -> run rojo no diagnosticado.
- MEDIO: `paths:` del trigger aun ata el CI a `scripts/**`.

## Evidencia minima esperada
- `gh run view <id> --json conclusion,headSha` = success en el commit del push.
- `yaml.safe_load` del workflow sin error.
- validate local 0/0.
- diff del workflow mostrando retirada de compileall/discovery local.

## TP Check
TP-01: el workflow no referencia copias locales de scripts/tests/skills. (diff)
TP-02: hace checkout del motor publico y corre el validate canonico. (diff)
TP-03: YAML valido por `yaml.safe_load`. (command)
TP-04: run real del CI = success, verificado por `gh run`. (gh json)
TP-05: motor intacto (`check_motor_pristine --check`) y sin secretos nuevos. (report)

## Criterio de rechazo inmediato
- No hay run real success que respalde el cambio.
- El CI sigue compilando/descubriendo copias locales.
- Se cerro con run rojo sin diagnostico ni BLOCKED.

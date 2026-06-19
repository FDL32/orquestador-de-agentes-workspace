# STRATEGY_WOT-2026-010v.md

## Enfoque

Ticket corto de hardening. La clase de fallo ya esta demostrada: control chars
ASCII no imprimibles pueden colarse en artefactos textuales y pasar el guard
hasta handoff. La correccion debe ser minima y compartida: detectar la clase de
byte en `scripts.encoding_guard.py` y demostrar que tanto el CLI guard como el
hook post-write reaccionan sin romper casos legitimos de whitespace.

## Fase 0 - Confirmacion de seams

1. Confirmar en codigo que `check_encoding_guard.py` y
   `encoding_post_write_hook.py` consumen `file_issues()` desde
   `scripts.encoding_guard.py`.
2. Capturar baseline de tests existentes en:
   - `tests/test_encoding_integrity.py`
   - `tests/unit/test_encoding_post_write_hook.py`
3. Releer el bloque de `AGENTS.md` sobre encoding y anotar que el gap v1 de
   Bash/heredoc NO entra en scope.
4. Registrar en `execution_log.md` la evidencia del problema (`008j` y `008f`)
   y el alcance exacto del fix.

## Fase 1 - Implementacion minima

1. Anadir deteccion de control chars ASCII `<32` no-whitespace en
   `scripts/encoding_guard.py`.
2. Hacer que `file_issues()` exponga ese hallazgo de forma reutilizable para el
   CLI guard y el hook.
3. Actualizar `scripts/check_encoding_guard.py` solo en lo necesario para
   reportar el nuevo tipo de error con diagnostico claro.
4. No tocar `scripts/encoding_post_write_hook.py` salvo que una prueba muestre
   que necesita una adaptacion minima para reflejar el nuevo issue.

## Fase 2 - Barreras

Deben existir barreras que prueben:
- FAIL del CLI guard por ruta explicita con un archivo textual que contiene
  `\x0b`, `\x0c` o `\x00`.
- FAIL del hook post-write sobre un archivo textual con el mismo problema.
- PASS de archivos con `\t`, `\n`, `\r` y CRLF legitimos.
- No regresion de BOM/mojibake/question-mark.

## Riesgos a vigilar

- Marcar CRLF o tabs validos como corrupcion.
- Duplicar logica entre el guard CLI y el hook.
- Expandir el ticket a shell/Bash o binarios por comodidad.

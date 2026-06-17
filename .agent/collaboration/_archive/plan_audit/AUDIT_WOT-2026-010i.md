# AUDIT_WOT-2026-010i -- Criterios de auditoria

## Contrato estructural

- [ ] El diff productivo se limita a barreras de handoff/review packet, parsers
      de contrato reutilizables, tests focales y una nota documental puntual.
- [ ] No cambia `run_pytest_safe.py`, cache, xdist, sharding ni selector focal.
- [ ] No convierte tickets documentales puros en tickets que exigen commit de
      codigo si no tocaron codigo.

## Evidencia minima

- [ ] Test rojo->verde: ruta en `Forbidden Surfaces` bloquea handoff.
- [ ] Test rojo->verde: ticket `code` o `mixed` sin commit visible bloquea.
- [ ] Test positivo: ticket `analysis` sin codigo tocado conserva cierre
      documental con deliverables existentes.
- [ ] Test semantico: `_resolve_destino()` devuelve `destination_root` cuando el
      link declara `motor_root` y `destination_root` diferentes.
- [ ] Test de fallback: observa el fallback real o su efecto, no un truco de
      entorno que el codigo anula internamente.
- [ ] Diagnosticos incluyen ruta/campo y remediacion.
- [ ] `ruff check` sobre Python tocado pasa.
- [ ] Tests focales derivados del diff pasan.
- [ ] `check_encoding_guard.py` pasa sobre archivos tocados.
- [ ] `validate --json --project-root <repo_destino>` termina 0/0.

## Anti-patrones a rechazar

- Reimplementar parsers de FLT/Forbidden Surfaces con regex incompatible.
- Bloquear cualquier dirty tree durante iteracion normal en vez de handoff.
- Mockear git/subprocess cuando el contrato visible exige git real.
- Dar por probado `destination_root` sin afirmar el valor exacto retornado.
- Mezclar este ticket con `010l` o con mejoras de performance.
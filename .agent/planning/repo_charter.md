# repo_charter.md -- WOT-2026-007f scope

> Scope restringido: este charter cubre la integracion runtime de CONTRACT_GAP
> en bus/controller (007f). Charter del motor completo vive en AGENTS.md + PROJECT.md.

## Product Intent

El motor debe poder representar en el bus que un Builder encontro un gap de
contrato bloqueante -- sin cerrar falsamente el ticket y con un handoff claro
de vuelta a Contract Formation. El Builder emite el gap; el sistema lo proyecta
en STATE.md/TURN.md; el Manager ve una accion concreta; --validate detecta
proyecciones incoherentes.

### OBJ-001 -- Representacion operativa de gaps de contrato

- **Descripcion:** cuando el Builder detecta una premisa falsa, superficie
  prohibida necesaria o criterio de aceptacion inalcanzable, puede emitir un
  evento CONTRACT_GAP que bloquea el ticket sin cerrarlo y genera una entrada
  en contract_gaps/CG-TICKET_ID.md.
- **failure_modes:**
  - Builder cierra falsamente el ticket en lugar de emitir el gap (el bus no
    tiene el evento; validate acepta un cierre que deberia estar bloqueado).
  - El gap queda solo en archivo sin evento de bus: --validate no puede
    detectar la incoherencia.
  - El Manager no ve accion concreta: el gap existe pero TURN.md no lo
    refleja y el ticket queda en limbo.
  - El gap se usa como escape hatch para evitar implementar requisitos
    dificiles sin evidencia de premisa falsa real.

## Architecture Constraints

- Bus append-only: events.jsonl nunca se edita a mano.
- Sin dependencias nuevas: stdlib + stack existente del motor.
- --validate permanece determinista: 0 errors para estados validos,
  fallo explicito para proyecciones incoherentes.
- La nueva transicion de estado es reversible: un ticket bloqueado por
  CONTRACT_GAP puede reabrirse tras actualizar el contrato.
- El payload del evento CONTRACT_GAP NO debe contener datos sensibles del
  proyecto destino (solo ticket_id, gap_type, path al archivo CG-*.md).

## Non-Goals

- No UI para gaps de contrato.
- No reparacion automatica del contrato.
- No propagacion cross-ticket de gaps en runtime (scope futuro).
- No cambiar el schema de contract_gaps/CG-*.md (ya definido en 007c).
- No tocar el flujo de tickets que NO usan Contract Formation.

## Quality Bar

- Tests cubren: premise_false, forbidden_surface_needed, missing_acceptance.
- --validate falla con mensaje claro si hay evento CONTRACT_GAP sin archivo
  CG-*.md correspondiente o si hay archivo CG-*.md sin evento de bus.
- Ningun test existente regresiona (suite verde post-007f).

## Security Constraints

- El payload del evento en events.jsonl referencia solo el path del archivo
  CG-*.md, no su contenido (que puede tener premisas sensibles).
- guard_paths cubre events.jsonl; el Builder no edita el bus a mano.
- Sin tokens, credenciales ni rutas absolutas del destino en los artefactos.

## Negative Audit Checklist

- [ ] El nuevo evento CONTRACT_GAP crea un deadlock de maquina de estados
      (el ticket no puede salir de BLOCKED sin intervencion manual indefinida)?
- [ ] El nuevo estado permite al Builder saltarse la revision del Manager
      (usa CONTRACT_GAP para cerrar sin review)?
- [ ] El gap recording escribe contenido sensible de premisas directamente
      en events.jsonl en lugar de referenciar el archivo CG-*.md?
- [ ] Un Builder puede usar CONTRACT_GAP como escape hatch ante requisitos
      dificiles sin evidencia verificable de premisa falsa?

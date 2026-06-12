---
name: project-finalize
version: 1.0.0
description: Cierre profesional de un proyecto con auditoria, limpieza, documentacion, versionado y verificacion final sin romper el flujo Manager -> Builder
author: agent-system
tags: [closeout, cleanup, documentation, release, governance]
triggers: [/finalize, close]
---

# project-finalize

Orquesta el cierre profesional de un proyecto o fase importante. Sirve para
dejar el repo limpio, documentado, versionado y listo para entrega, handoff o
mantenimiento.

## Overview

Activa esta skill cuando:
- El usuario dice "cierra el proyecto", "dejalo listo para entrega" o pide una limpieza final
- El Builder ya termino una implementacion importante y toca consolidar
- Hace falta alinear codigo, documentacion, version y artefactos antes de marcar DONE

### Regla de compatibilidad

- Usa `work_plan.md` como plan activo.
- No introduzcas `work_plan_cierre.md` como plan operativo salvo que tambien
  actualices controller, hooks, prompts y validadores que hoy dependen de
  `work_plan.md`.
- Si quieres trazabilidad adicional, crea `closeout_report.md` o archiva una
  copia final del plan, pero el carril operativo sigue siendo `work_plan.md`.

## Workflow

### Paso 1: Elegir modo de cierre

Usa `references/closeout-modes.md` para escoger entre:
- `DELIVERY` - Entrega profesional de algo que seguira vivo
- `RELEASE` - Publicacion de una version
- `HANDOFF` - Traspaso a otra persona o equipo
- `ARCHIVE` - Cierre o fin de vida

Identifica desde el inicio que aprobaciones humanas haran falta:
- borrados relevantes
- cambios estructurales
- bump de version
- tags o release
- archivado

### Paso 2: Manager crea el plan de cierre

Usa `references/closeout-plan-template.md`.

El plan debe incluir, como minimo:
1. Auditoria
2. Limpieza
3. Documentacion
4. Versionado / release readiness
5. Verificacion final

Todo lo que quede fuera de alcance va a `backlog.md`, no a TODOs ocultos.

### Paso 3: Builder ejecuta la auditoria

Auditar:
- archivos temporales, logs, debug y scripts locales
- codigo o docs muertos
- `TODO`, `FIXME`, ejemplos viejos y configuracion obsoleta
- riesgo de secrets y estado de `.env.example`
- deriva documental entre README, PROJECT, CLAUDE, docs de agentes y comandos
- estado de version, changelog y notas de release
- consistencia entre manifests y lockfiles
- huecos de mantenimiento: LICENSE, SECURITY, CONTRIBUTING, CODEOWNERS, soporte

Clasificar hallazgos en:
- `must-fix`
- `recommended`
- `defer-to-backlog`

### Paso 4: Manager revisa la auditoria

El Manager decide que entra en alcance y que se difiere.

Cualquier borrado de archivos, cambio estructural o riesgo de perdida de
contexto necesita aprobacion explicita antes de ejecutarse.

### Paso 5: Builder ejecuta la limpieza

- Eliminar artefactos temporales o locales si es seguro
- Podar scripts, ejemplos o docs obsoletos
- Normalizar estructura y nombres
- Ajustar `.gitignore` u otros ignores
- Verificar que no queden secrets, credenciales o rutas personales
- Preservar scaffolding deliberado; no borrar por intuicion

### Paso 6: Builder sincroniza documentacion

Actualizar solo lo que aplique de verdad:
- `README.md`
- `PROJECT.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- reglas o docs de agentes
- resumen de arquitectura / ADR / limitaciones conocidas / migraciones
- instrucciones de run, test, install, deploy, rollback o handoff

Para repos compartidos o publicos, revisar tambien el checklist de
`references/closeout-checklist.md`.

### Paso 7: Builder prepara versionado y release readiness

- Reutilizar `version-changelog` para SemVer y CHANGELOG
- El tipo de bump lo valida el Manager
- El bump, tag o release requieren aprobacion humana en el punto adecuado
- Si hubo cambios incompatibles o deprecaciones, documentarlos de forma visible

### Paso 8: Builder cubre trust y governance

Aplicar solo cuando la madurez del proyecto lo justifique:
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `CITATION.cff` si el software debe citarse
- SBOM para software distribuible
- artifact attestation / provenance para builds publicadas
- estado de mantenimiento: `active`, `maintenance-only` o `archived`

### Paso 9: Builder hace la verificacion final

- Ejecutar `bui-run-quality-gates`
- Ejecutar `bui-self-audit`
- Hacer smoke test de instalacion o ejecucion en entorno limpio si es viable
- Verificar documentacion contra comandos, rutas y outputs reales
- Registrar evidencia final en `execution_log.md`

### Paso 10: Manager cierra

El Manager relee archivos cambiados, valida aprobaciones humanas, comprueba
coherencia entre docs y version, y marca el plan `COMPLETED`.

Si el proyecto termina o cambia de manos, dejar explicito:
- estado de mantenimiento
- backlog pendiente
- decision de handoff o archivado

## Output Format

1. `work_plan.md` actualizado y completado
2. `execution_log.md` con hallazgos, acciones y evidencia
3. `closeout_report.md` opcional como resumen permanente del cierre
4. Documentacion y metadatos sincronizados
5. `notifications.md` con handoffs o aprobaciones si aplica

## References

- `references/closeout-modes.md` - Modos de cierre y cuando usarlos
- `references/closeout-plan-template.md` - Esqueleto del plan de cierre
- `references/closeout-checklist.md` - Checklist minimo, recomendado y avanzado
- `../version-changelog/SKILL.md` - Versionado y changelog
- `../bui-self-audit/SKILL.md` - Auditoria obligatoria del Builder
- `../bui-run-quality-gates/SKILL.md` - Quality gates finales
- `../man-review-implementation/SKILL.md` - Revision final del Manager

## Constraints

- **NO** usar `work_plan_cierre.md` como plan activo sin actualizar antes el tooling
- **NO** borrar archivos o mover estructura por intuicion
- **NO** cerrar sin documentar que queda fuera de alcance y que va a backlog
- **SIEMPRE** dejar explicito el estado de mantenimiento al cerrar
- **SIEMPRE** pedir aprobacion humana para bump, tag, release o archivado
- **SIEMPRE** verificar que la documentacion describe el estado real del repo


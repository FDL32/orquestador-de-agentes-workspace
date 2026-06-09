# AUDIT_FRONTIERCODE_LEARNINGS

**Tipo de output auditado:** propuesta arquitectonica / aprendizaje de benchmark
**Fecha:** 2026-06-09
**Auditor:** análisis escéptico sobre análisis de FrontierCode
**Modo:** Solo lectura. No implante nada.

---

## 1. Veredicto

**APROBADO CON NITS** — El análisis extrae aprendizajes reales del benchmark FrontierCode y la propuesta de acción es proporcionada. Hay tres claims que merecen matiz, pero ninguno invalida la dirección general.

**Cobertura actual frente a FrontierCode:** el documento aterriza bien tres ejes (`mergeability`, `test correctness` vía reverse-classical acotado, y claridad del contrato), pero todavía deja parcialmente fuera dos dimensiones muy relevantes para este sistema: `scope discipline` y `code quality / codebase conventions`.

---

## 2. Hallazgos

### ALTO — "Reverse-classical como regla general" sobre-generaliza

**Claim auditado:** "todo test nuevo debe demostrar que captura el comportamiento roto o justificar por qué es cobertura de regresión suficiente".

**Evidencia:** FrontierCode usa reverse-classical como una métrica dentro de un benchmark, no como regla de desarrollo diario. En un flujo real, hay tests de contrato, tests de integración y tests de humo que no tienen un "estado roto" previo.

**Riesgo:** Si se aplica como regla obligatoria, cada test nuevo requeriría un diff temporal para demostrar fallo, lo que añade fricción sin valor proporcional para tests de contrato o cobertura documental.

**Corrección exacta:** Reformular como: "para tests que corrigen un bug identificado, el test debe fallar sobre la base rota o al menos quedar justificado explícitamente como regresión real. Para tests de contrato o cobertura nueva, basta con justificación explícita en el commit o execution_log."

**Etiqueta:** VERIFICADO EN REFERENCIA EXTERNA
**Clasificación CEM:** C (deriva de fixture) — se toma una métrica de benchmark como regla de producción sin ajuste contextual.
**Bloquea:** No. Es un matiz, no un error.

---

### MEDIO — "Mergeability > correctness" necesita definición operativa

**Claim auditado:** "no cerrar tickets solo con pytest verde".

**Evidencia:** Correcto como principio. Pero en nuestro sistema ya existe `validate --json` que cubre estado canónico, y el Manager review ya evalúa diff, scope y estilo. El riesgo real no es "falta de mergeability gate" sino que el gate existente (`validate`) a veces se salta o se acepta con warnings.

**Riesgo:** Añadir otro concepto abstracto sin mecanismo concreto puede generar fricción sin mejora real.

**Corrección exacta:** En lugar de crear un gate nuevo, reforzar el existente: `validate --json` debe exigir `0 errors` y `0 warnings estructurales` para APROBADO. El TP-PROSE-10 de la tercera ronda es un ejemplo de warning que debería haber bloqueado. Antes de implementar el gate, hace falta una definición operativa de qué warnings bloquean y cuáles no.

**Etiqueta:** INFERENCIA RAZONABLE
**Clasificación CEM:** A (regresión de contrato) — el contrato de validate ya existe, solo falta ejecutarlo con disciplina.
**Bloquea:** No.

---

### BAJO — "Tareas más cortas" malinterpreta el aprendizaje real: el eje es inferencia de intención, no longitud

**Claim auditado:** "tareas más concisas y menos sobreespecificadas".

**Evidencia:** FrontierCode usa tareas sintéticas de 1 párrafo. Nuestros work_plan son más largos porque incluyen contexto de integración (dependencias, non-goals, quality gates, files likely touched). La longitud no es el problema; la claridad del contrato sí.

**Riesgo:** Acortar prompts sin reemplazar la información necesaria puede aumentar ambigüedad y ciclos de revisión.

**Corrección exacta:** No acortar por decreto, sino estructurar mejor: separar contrato (objetivo + criterios) de contexto (dependencias, histórico). El contrato debe caber en 5 líneas; el contexto puede ser más largo. El aprendizaje transferible de FrontierCode no es "menos texto" sino "más capacidad del agente para inferir intención correcta del maintainer con menos andamiaje explícito".

**Etiqueta:** INFERENCIA RAZONABLE
**Clasificación CEM:** D (entorno) — el problema no es el prompt sino cómo se estructura la información.
**Bloquea:** No.

---

### MEDIO — Scope discipline del benchmark ya existe parcialmente, pero no se reconoce ni se endurece

**Claim auditado:** el documento no recoge explícitamente el eje `scope discipline` de FrontierCode.

**Evidencia:** FrontierCode mide que el patch toque solo lo necesario, sin archivos no relacionados ni refactors colaterales. En este sistema ya existen `Files Likely Touched`, `non-goals` y review de diff/scope por parte del Manager, que son análogos claros a ese eje.

**Riesgo:** Si no se reconoce esta fortaleza ni se la incluye en el análisis, el documento transmite que todo son gaps y pierde una oportunidad de reforzar una barrera que ya tenemos.

**Corrección exacta:** Añadir una sección explícita que diga: "FrontierCode confirma que nuestro uso de `Files Likely Touched` y `non-goals` es la barrera correcta para `scope discipline`; la mejora no es inventar otra, sino mantenerla temprana, auditable y vinculada al review."

**Etiqueta:** INFERENCIA RAZONABLE
**Clasificación CEM:** A (regresión de contrato) — la barrera existe, pero no está siendo tratada como parte central del criterio de mergeabilidad.
**Bloquea:** No.

---

### MEDIO — Code quality / codebase conventions aparece solo de forma implícita

**Claim auditado:** el documento no extrae el eje `code quality / codebase conventions` como aprendizaje diferenciado.

**Evidencia:** FrontierCode no se queda en tests y lint; también pregunta si el cambio sigue patrones del codebase y sería mergeable para maintainers reales. En este sistema, el Manager ya revisa diff, estilo y alcance, pero no hay una formulación explícita del tipo "no introducir patrones nuevos sin justificación" o "seguir convenciones locales del repo".

**Riesgo:** La revisión puede seguir capturando esto de forma tácita, pero sin contrato explícito es más difícil auditar consistencia entre reviews.

**Corrección exacta:** Añadir como mejora documental una regla del estilo: "Además de pasar gates mecánicos, el cambio debe seguir patrones existentes del codebase o justificar explícitamente cualquier patrón nuevo introducido."

**Etiqueta:** INFERENCIA RAZONABLE
**Clasificación CEM:** C (deriva de fixture) — una parte de la calidad queda al gusto del reviewer sin contrato suficientemente explícito.
**Bloquea:** No.

---

## 3. Qué haría ahora

Tres cambios concretos y pequeños:

1. **Endurecer `validate --json` como gate de cierre existente.** Añadir a `PROJECT.md` o al review packet: "APROBADO requiere `validate --json` con `0 errors` y `0 warnings estructurales`. Warnings de contrato, estado canónico o prose canónica (ej. `TP-PROSE`) sí bloquean. Advisories externos o warnings no estructurales se documentan como `NITs`."
   - **Secuencia operativa obligatoria:** primero definir una allowlist corta de warnings no bloqueantes; después endurecer el gate. No al revés.

2. **Añadir regla de tests al `launch_builder.md` (o al `work_plan.md` como sección estándar):** "Si el ticket corrige un bug, el test nuevo debe fallar sobre la base rota (reverse-classical). Si es test de contrato o cobertura, registrar en `execution_log.md` la etiqueta `[NON-REVERSE-CLASSICAL: <razón breve>]`."

3. **Separar `BLOCKERS` de `NITS` en el review packet.** En `MANAGER_REVIEW_*.md`, añadir secciones:
   - `BLOCKERS`: errores en `validate --json`, tests que no pasan o no demuestran el bug si es bugfix, evidencia insuficiente del cambio productivo, y scope creep.
   - `NITS`: legibilidad, refactors no necesarios y mejoras de estilo que no rompen gates.
   Esto ya se hace implícitamente; hacerlo explícito reduce ruido.

4. **Reconocer y reforzar fortalezas ya alineadas con FrontierCode.**
   - `Files Likely Touched` + `non-goals` como equivalente práctico de `scope discipline`.
   - `AGENTS.md` y reglas de calidad como repo guidelines comparables al contexto que FrontierCode entrega al agente.
   - Manager review sobre diff/evidencia como base parcial del eje `code quality`.

---

## 4. Qué NO haría

- **No crear un gate nuevo y separado.** Ya tenemos `validate --json` + `pytest` + `ruff` + Manager review. Añadir otro gate sin eliminar redundancia es ruido.

- **No imponer reverse-classical como regla universal.** Para tests de contrato puro (como el lock enriquecido de WT-2026-242c), la justificación en el commit es suficiente.

- **No acortar work_plan por decreto.** Mejorar estructura, no reducir contenido.

- **No introducir todavía un sistema complejo de severidades en `validate --json`.** Mientras la lista de warnings no bloqueantes sea corta, una allowlist explícita es más simple y proporcional.

---

## 5. Aprendizaje reusable

**Aprendizaje candidato a memoria:** FrontierCode refuerza que mergeabilidad = corrección + alcance limpio + tests que demuestran el bug + estilo consistente. En nuestro sistema, `validate --json` ya cubre gran parte del cierre canónico; falta endurecerlo a `0 warnings estructurales` sin inventar un gate nuevo.

**Barrera candidata:** Un hook pre-mark-ready que exija `validate --json` con `0 errors` y `0 warnings estructurales`, con allowlist explícita para advisories no bloqueantes de herramientas externas. La secuencia correcta es: definir allowlist -> endurecer gate.

**Ticket follow-up sugerido:** WT-2026-NNN — Documentar política de warnings bloqueantes en `validate --json` y formalizar la regla reverse-classical solo para tests de bugfix.

---

## 6. Checklist escéptico aplicado

### Claims verificables

| Claim | Evidencia esperada | Estado |
|-------|--------------------|--------|
| FrontierCode mide mergeability, no solo correctness | Blog post de cognition.ai: "Introducing FrontierCode" | VERIFICADO EN REFERENCIA EXTERNA |
| Reverse-classical es una métrica de benchmark, no regla de producción | FrontierCode paper describe métricas: correctness, regression safety, mechanical cleanliness, test quality, scope discipline, code quality | VERIFICADO EN REFERENCIA EXTERNA |
| Nuestro validate --json a veces pasa con warnings | execution_log.md WT-2026-242b muestra warnings TP-PROSE en validate --json que no bloquearon | VERIFICADO EN DOCUMENTACION |
| Manager review ya evalúa diff, scope y estilo | MANAGER_REVIEW_WT-2026-*.md existentes muestran evaluación de scope y diff | VERIFICADO EN DOCUMENTACION |
| `validate --json` no expone hoy criticidad estructural en su schema | Los warnings actuales se consumen como strings sin metadato de severidad en la documentación auditada | INFERENCIA RAZONABLE |

### Diff, scope y artefactos

No hay cambios de código propuestos. Esta es una auditoría documental sobre una propuesta de aprendizaje.

### Tests y gates

No aplica directamente. La propuesta no introduce tests nuevos, solo sugiere mejoras de proceso.

### Producción vs tests

No aplica. La propuesta es sobre proceso, no sobre código productivo.

### Estado canonico y bus

No aplica. La propuesta no modifica el estado del sistema operativo.

### Autonomia del Builder

La propuesta respeta la autonomía del Builder: no introduce barreras nuevas, solo endurece las existentes y documenta reglas de testing. El riesgo de fricción es bajo porque los cambios son documentales, no operativos.

### Barrera automatica

La barrera candidata (`validate --json` con `0 warnings estructurales`) ya existe parcialmente; solo falta definir qué warnings bloquean y hacerlos efectivamente bloqueantes. Esto es un endurecimiento de barrera existente, no una barrera nueva.

---

## 6b. Fortalezas ya cubiertas

Comparado con FrontierCode, este sistema ya tiene varias piezas bien alineadas que conviene reconocer explícitamente como línea base:

- **Scope discipline:** `Files Likely Touched` y `non-goals` ya cumplen la función principal del eje `scope`.
- **Repo guidelines:** `AGENTS.md`, `PROJECT.md` y reglas locales ya dan al agente contexto de lint, tests y estilo, análogo al benchmark.
- **Mechanical cleanliness:** los quality gates (`ruff`, `pytest`, `validate --json`) ya materializan una parte clara del eje de limpieza mecánica.
- **Review de diff y evidencia:** el Manager ya inspecciona diff, scope y señales de cambio productivo, cubriendo parcialmente `code quality / conventions`.

La oportunidad no es reconstruir estas barreras desde cero, sino endurecerlas donde todavía son implícitas o no bloqueantes.

**Anclaje de evidencia:** estas fortalezas se apoyan en los claims verificables de §6 (`Manager review`, `validate --json`, y guidelines locales). No son auto-reporte aislado, sino lectura resumida de esa evidencia.

---

## 7. Clasificacion CEM resumen

| Hallazgo | Clase CEM | Subtipo | Impacto de fallo | Barrera existente | Barrera faltante |
|----------|-----------|---------|------------------|-------------------|------------------|
| Reverse-classical sobre-generalizado | C (deriva de fixture) | Fixture irreal aplicado como regla | Proceso | N/A | Justificación explícita en commit |
| Mergeability necesita definición operativa | A (regresión de contrato) | Gate ausente | Proceso | validate --json | Warnings estructurales como bloqueante |
| Inferencia de intención del agente mal reducida a "prompts más cortos" | D (entorno-infraestructura) | Entorno | Proceso | work_plan.md estructurado | Separar contrato de contexto y exigir mejor inferencia con menos andamiaje |
| Scope discipline ya existe, pero no se reconoce ni se endurece | A (regresión de contrato) | Barrera implícita no tratada como criterio central | Proceso | `Files Likely Touched`, `non-goals`, review de diff/scope | Reconocerla como parte explícita del criterio de mergeabilidad |
| Code quality / conventions queda solo implícito en review | C (deriva de fixture) | Criterio tácito dependiente del reviewer | Proceso | Manager review sobre diff/evidencia | Regla explícita sobre seguir patrones del codebase o justificar patrones nuevos |
| Warnings críticos sin definición operativa | A (regresión de contrato) | Contrato incompleto | Proceso | validate --json | Allowlist o clasificación simple de warnings no bloqueantes |

---

## 8. Conclusión

La propuesta es sólida y los tres cambios concretos propuestos (endurecer `validate`, regla de reverse-classical para bugfixes, separar `BLOCKERS`/`NITS`) son mejoras tangibles de bajo coste. No hay riesgo de falso verde ni scope creep conceptual. La única dependencia operativa pendiente es definir qué warnings bloquean antes de endurecer el gate.

**Evidencia principal:** VERIFICADO EN DOCUMENTACION — los warnings `TP-PROSE` en `validate --json` de `WT-2026-242b` demuestran que el gate actual no bloquea por warnings, validando el claim de "endurecer validate".

**Riesgo residual bajo:** La propuesta no introduce código nuevo, solo documenta mejores prácticas existentes. El riesgo de fricción es mínimo si la política de warnings bloqueantes se implementa con una allowlist pequeña de warnings no estructurales en vez de con severidades complejas desde el primer día.

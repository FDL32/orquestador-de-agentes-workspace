#!/usr/bin/env powershell
# Script de limpieza para deployment v5
# Uso: .\scripts\clean_for_deployment.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA PARA DEPLOYMENT v5" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path $PSScriptRoot -Parent
$CollabDir = Join-Path $ProjectRoot ".agent\collaboration"

Write-Host "Directorio del proyecto: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

Write-Host "PASO 1: Eliminando artefactos de sesion..." -ForegroundColor Yellow
$PathsToRemove = @(
    (Join-Path $CollabDir ".tool_counter.json"),
    (Join-Path $CollabDir ".session_state.json"),
    (Join-Path $CollabDir "findings.md"),
    (Join-Path $CollabDir "archive")
)

$RemovedCount = 0
foreach ($PathToRemove in $PathsToRemove) {
    if (Test-Path $PathToRemove) {
        Remove-Item -LiteralPath $PathToRemove -Recurse -Force
        Write-Host "  Eliminado: $PathToRemove" -ForegroundColor Green
        $RemovedCount++
    }
}

if ($RemovedCount -eq 0) {
    Write-Host "  No habia artefactos de sesion" -ForegroundColor Gray
}
Write-Host ""

Write-Host "PASO 2: Reseteando archivos de colaboracion..." -ForegroundColor Yellow

$FilesToWrite = @{
    "work_plan.md" = @"
# Plan de Trabajo

## Metadata
- **ID:** N/A
- **Estado:** N/A
- **Creado por:** [Pendiente]
- **Fecha:** [Pendiente]

---

## Objetivo

No hay plan activo. El Manager debe crear uno.

---

Para crear un nuevo plan:
1. Ejecuta: `python .agent/agent_controller.py`
2. Sigue las instrucciones del Manager
"@
    "execution_log.md" = @"
# Log de Ejecucion

## Metadata
- **Plan ID:** N/A
- **Estado:** N/A
- **Ejecutado por:** [Pendiente]
- **Inicio:** [Pendiente]

---

No hay ejecucion activa.

---

Para iniciar una sesion:
1. Verifica que es tu turno: `python .agent/agent_controller.py`
2. Sigue las instrucciones del workflow correspondiente
"@
    "review_queue.md" = @"
# Cola de Revision

No hay items pendientes de revision.

---

Para anadir una escalacion:
1. Documenta el problema en `execution_log.md`
2. Anade la escalacion aqui siguiendo el formato del workflow
"@
    "notifications.md" = @"
# Registro de Notificaciones

---

No hay notificaciones pendientes.

---

*Sistema Multi-Agente v5*
"@
    "TURN.md" = @"
# TURNO ACTUAL

**Ultima actualizacion:** [Pendiente]

---

## Agente Activo

| Campo | Valor |
|-------|-------|
| **ROL** | **MANAGER** |
| **Plan ID** | NINGUNO |
| **Accion** | CREATE_PLAN |

---

## Instruccion

> No hay plan activo. Crea un nuevo `work_plan.md`

---

## Archivos a Leer

1. `.manager_rules` (Contexto del rol)
2. `.agent/workflows/manager_workflow.md` (Flujo de trabajo)
3. `.agent/context/project_map.md` (Estructura)

---

## Estado del Sistema

| Archivo | Estado |
|---------|--------|
| work_plan.md | N/A |
| execution_log.md | N/A |

---

*Generado por agent_controller.py v5*
"@
    "STATE.md" = @"
# STATE - Estado Activo del Proyecto

> Snapshot operativo del plan en curso.
> Lo escribe principalmente el Manager y lo consulta el Builder.

---

## Plan activo

- **ID:** NINGUNO
- **Estado actual:** N/A
- **Fase actual:** N/A

---

## Ultimo progreso documentado

- **Ultimo task en execution_log.md:** N/A

---

## Contexto para la proxima sesion

- **Proximo paso recomendado:** Ejecutar `python .agent/agent_controller.py`
- **Archivos que mirar primero:** `work_plan.md`, `TURN.md`, `STATE.md`
- **Notas:** No hay plan activo en este momento.
"@
    "backlog.md" = @"
# Backlog de Mejoras y Hallazgos

> Registro de ideas colaterales y deuda tecnica detectada durante la ejecucion.
> Este archivo no sustituye al plan activo ni debe bloquearlo.

---

## Ideas colaterales

- [Fecha] [Idea detectada durante implementacion o review]

---

## Mejoras tecnicas detectadas

- [Fecha] [Mejora tecnica concreta, fuera del alcance del plan activo]

---

## Deuda tecnica identificada

- [Fecha] [Deuda tecnica, impacto y posible seguimiento]

---

## Regla de uso

- Anade aqui solo items fuera del alcance inmediato del `work_plan.md` activo.
- Nunca bloquees el plan activo por items del backlog.
- Si un item pasa a ser prioritario, el Manager debe promoverlo a un nuevo `work_plan.md`.
"@
}

foreach ($FileName in $FilesToWrite.Keys) {
    $TargetPath = Join-Path $CollabDir $FileName
    $FilesToWrite[$FileName] | Set-Content -LiteralPath $TargetPath -Encoding UTF8
    Write-Host "  Reseteado: $FileName" -ForegroundColor Green
}
Write-Host ""

Write-Host "PASO 3: Verificando integridad del sistema..." -ForegroundColor Yellow

$RequiredFiles = @(
    ".agent\agent_controller.py",
    ".agent\hooks\__init__.py",
    ".agent\hooks\pre_action_hook.py",
    ".agent\hooks\post_tool_hook.py",
    ".agent\hooks\stop_hook.py",
    ".agent\hooks\pre_compact_hook.py",
    ".agent\hooks\native_stop_hook.py",
    ".agent\hooks\subagent_stop_hook.py",
    ".agent\session_tracker.py",
    ".agent\completion_checker.py",
    ".agent\config\hooks_config.json",
    ".agent\templates\findings_template.md",
    ".agent\templates\bat_launcher_gui.template",
    ".agent\templates\bat_launcher_cli.template",
    ".builder_rules",
    ".manager_rules",
    "EMPEZAR-AQUI.md",
    "README.md",
    "scripts\install_agent_system.py",
    "skills\bui-self-audit\SKILL.md",
    "skills\bui-run-quality-gates\SKILL.md"
)

$MissingFiles = @()
foreach ($RelativePath in $RequiredFiles) {
    $AbsolutePath = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path $AbsolutePath)) {
        $MissingFiles += $RelativePath
        Write-Host "  FALTA: $RelativePath" -ForegroundColor Red
    }
}

if ($MissingFiles.Count -eq 0) {
    Write-Host "  Todos los archivos core estan presentes" -ForegroundColor Green
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE LIMPIEZA" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Artefactos eliminados: $RemovedCount" -ForegroundColor Green
Write-Host "Archivos de colaboracion reseteados: $($FilesToWrite.Count)" -ForegroundColor Green
Write-Host ""

if ($MissingFiles.Count -eq 0) {
    Write-Host "SISTEMA LISTO PARA COPIAR" -ForegroundColor Green
    Write-Host ""
    Write-Host "La carpeta fuente esta limpia y lista para copiar o pegar en un proyecto nuevo." -ForegroundColor White
    exit 0
}

Write-Host "VERIFICAR ANTES DE COPIAR" -ForegroundColor Yellow
Write-Host "Faltan archivos esenciales del sistema." -ForegroundColor Yellow
exit 1

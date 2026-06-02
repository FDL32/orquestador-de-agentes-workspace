# Anti-Patterns Reference: Karpathy Principles for z_scripts

**Basado en:** Andrej Karpathy's observations + z_scripts context  
**Audiencia:** Builder agents (y cualquier agente que necesite entrenar en design decisions)  
**Referencia:** Complementa `.builder_rules` â€” Behavioral Guidelines section

---

## IntroducciÃ³n

Este documento proporciona ejemplos **antes/despuÃ©s** de anti-patterns comunes que los agentes cometen.
Cada ejemplo muestra:
1. âŒ **Lo que NO hacer** (anti-patrÃ³n)
2. âœ… **Lo que SÃ hacer** (soluciÃ³n simple)
3. **Por quÃ©** funciona la soluciÃ³n
4. **SeÃ±ales de alerta** para detectarlo

---

## 1ï¸âƒ£ Think Before Coding: Hidden Assumptions

**Contexto:** Usuario pide "agregar feature de export de usuarios"

### âŒ Lo Que NO Hacer (Asume Silenciosamente)

```python
# Builder asume todo sin preguntar
def export_users(format='json'):
    """Export all users to a file."""
    users = db.query(User).all()  # Asume: todos los usuarios
    
    if format == 'json':
        with open('users.json', 'w') as f:  # Asume: ubicaciÃ³n
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    
    return f"Exported {len(users)} users"
```

**Problemas:**
- Â¿Exportar TODOS? Â¿Privacidad? Â¿PaginaciÃ³n?
- Â¿Guardar en raÃ­z? Â¿Permisos?
- Â¿Estos campos? Â¿Hay datos sensibles?
- Sin tests. Sin criterio de Ã©xito claro.

### âœ… Lo Que SÃ Hacer (Surfacear Asunciones Primero)

```python
# Builder pregunta ANTES de asumir
[DECISION POINT - Builder en execution_log.md:]

"Usuario pide 'agregar feature de export'. Asunciones detectadas:

1. Scope: Â¿Exportar quÃ©?
   - Todos los usuarios (riesgo de privacidad)
   - Usuario actual
   - Filtro por rango de fechas
   â†’ Pregunta al usuario antes de asumir

2. Formato: Â¿A dÃ³nde?
   - Endpoint API (return JSON)
   - Archivo en servidor (ruta segura)
   - Email al usuario
   â†’ Aclarar antes de implementar

3. Campos: Â¿QuÃ© incluir?
   - Solo pÃºblicos (id, nombre)
   - Con datos sensibles (password hashes) â€” NO
   - Con auditorÃ­a (timestamps de cambios)
   â†’ Revisar schema antes de codificar

Propuesta: Implementar endpoint `/api/v1/users/me/export?format=json`
que retorna solo los datos del usuario autenticado, JSON puro.
Â¿Es lo que necesitas?"
```

**Por quÃ© funciona:**
- Evita 20 lÃ­neas de cÃ³digo innecesario
- Alinea expectativas ANTES de coding
- Documenta decisiones en el log

### ðŸš¨ SeÃ±ales de Alerta

- [ ] Escribiste 50+ lÃ­neas sin confirmar scope
- [ ] Empezaste a codificar sin re-leer el plan
- [ ] No documentaste tus asunciones en execution_log.md

---

## 2ï¸âƒ£ Simplicity First: Over-abstraction

**Contexto:** Usuario pide "calcular descuentos"

### âŒ Lo Que NO Hacer (Strategy Pattern para un caso)

```python
# Builder sobre-ingenieriza
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)

# Uso: 30+ lÃ­neas de setup para calcular 10% de descuento
```

**Problemas:**
- 50 lÃ­neas para una funciÃ³n de 1 lÃ­nea
- 5 clases cuando no hay 5 casos de uso
- Dificultad de testing (mocking layers)
- Mantenimiento de cÃ³digo innecesario

### âœ… Lo Que SÃ Hacer (Simple, Extensible DespuÃ©s)

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. Percent should be 0-100."""
    return amount * (percent / 100)

# Uso:
discount = calculate_discount(100.0, 10.0)  # â†’ 10.0
```

**Por quÃ© funciona:**
- 2 lÃ­neas vs 50 lÃ­neas
- FÃ¡cil de testear
- FÃ¡cil de entender
- Si despuÃ©s necesitas Strategy pattern (cuando tengas 3+ tipos de descuento), refactoriza entonces

### ðŸš¨ SeÃ±ales de Alerta

- [ ] Escribiste una clase cuando una funciÃ³n habrÃ­a bastado
- [ ] Usaste patrÃ³n de diseÃ±o para UN caso de uso
- [ ] El mismo archivo fue modificado 3+ veces (parcheo)
- [ ] Hay mÃ©todos/clases que "podrÃ­an ser Ãºtiles despuÃ©s"

---

## 3ï¸âƒ£ Surgical Changes: Drive-by Refactoring

**Contexto:** Plan dice "AÃ±ade logging a la funciÃ³n upload_file"

### âŒ Lo Que NO Hacer (Refactor Colateral)

```diff
+ import logging
+ logger = logging.getLogger(__name__)

- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
+     logger.info(f"Uploading {file_path} to {destination}")
+     
      try:
-         with open(file_path, 'rb') as f:
-             data = f.read()
-         
-         response = requests.post(destination, files={'file': data})
-         
-         if response.status_code == 200:
-             return True
-         else:
-             return False
+         with open(file_path, "rb") as f:
+             data = f.read()
+         response = requests.post(destination, files={"file": data})
+         success = response.status_code == 200
+         
+         if success:
+             logger.info(f"Upload successful: {file_path}")
+         else:
+             logger.error(f"Upload failed: {file_path}, status={response.status_code}")
+         
+         return success
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f"Upload error for {file_path}: {e}")
          return False
```

**Cambios NO solicitados:**
- CambiÃ³ quotes (' â†’ ")
- AÃ±adiÃ³ type hints (no pedidos)
- AÃ±adiÃ³ docstring
- RefactorizÃ³ lÃ³gica de return (no necesario)
- ReformateÃ³ lÃ­neas

### âœ… Lo Que SÃ Hacer (Solo Logging, Estilo Original)

```diff
+ import logging
+ logger = logging.getLogger(__name__)

  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
              data = f.read()
          
          response = requests.post(destination, files={'file': data})
          
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

**Solo cambios necesarios:**
- Import logging
- logger.info/error/exception calls
- Mantiene quotes originales, spacing, lÃ³gica

### ðŸš¨ SeÃ±ales de Alerta

- [ ] El diff incluye cambios cosmÃ©ticos ademÃ¡s del fix
- [ ] Reformateaste lÃ­neas "for clarity"
- [ ] Eliminaste cÃ³digo pre-existente sin preguntar
- [ ] Tu commit toca 5+ archivos no relacionados

---

## 4ï¸âƒ£ Goal-Driven Execution: Test-First Verification

**Contexto:** Plan dice "Corregir bug en sorting cuando hay duplicados"

### âŒ Lo Que NO Hacer (Fijar Sin Reproducir)

```python
# Builder "corrige" sin verificar el bug
def sort_scores(scores):
    """Sort scores descending, with tie-breaking."""
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Problema: Â¿CuÃ¡l era el bug exactamente? Â¿Test confirmando que estÃ¡ arreglado?
```

### âœ… Lo Que SÃ Hacer (Test-First)

```python
# Step 1: Escribir test que REPRODUCE el bug
def test_sort_with_duplicate_scores():
    """Test sorting when multiple items have same score."""
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    
    # El bug: orden no determinÃ­stica para duplicados
    # Ejecutar varias veces, deberÃ­a ser consistente
    result = sort_scores(scores)
    
    # Verificar: orden estable
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90
    # Tie-breaker: Alice antes que Bob (nombre alfabÃ©tico)
    assert result[0]['name'] == 'Alice'
    assert result[1]['name'] == 'Bob'

# Ejecutar: âŒ FALLA (reproduce el bug)

# Step 2: Implementar fix
def sort_scores(scores):
    """Sort by score descending, then name ascending for ties."""
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Ejecutar: âœ… PASA

# Step 3: Verificar estabilidad (ejecutar 10 veces)
for i in range(10):
    assert sort_scores(scores)[0]['name'] == 'Alice'
    # âœ… Consistente todas las veces
```

**Por quÃ© funciona:**
- Test **reproduce** el bug (paso 1)
- Fix **pasa** el test (paso 2)
- VerificaciÃ³n de **estabilidad** (paso 3)
- Criterio de Ã©xito **verificable** y **observable**

### ðŸš¨ SeÃ±ales de Alerta

- [ ] Tu criterio de "hecho" es "parece funcionar"
- [ ] No escribiste tests, solo "probaste manualmente"
- [ ] El plan dice "refactoriza" pero no hay antes/despuÃ©s verificable

---

## 5ï¸âƒ£ z_scripts EspecÃ­ficos: guard_paths.py Violation

**Contexto:** Plan dice "Guardar configuraciÃ³n en .env"

### âŒ Lo Que NO Hacer (Ignorar guard_paths)

```python
# Builder ignora el hook guard_paths.py
from pathlib import Path

def save_config(api_key, db_password):
    config = {
        'API_KEY': api_key,
        'DB_PASSWORD': db_password,
    }
    
    # âŒ ANTI-PATTERN: Escribir .env directamente
    config_file = Path('.env')
    config_file.write_text(json.dumps(config))
```

**Problema:**
- El hook `guard_paths.py` **bloquea** escrituras a `.env`
- z_scripts usa arquitectura de 3 zonas (privada/, publica/)
- Esto expone secretos en el repo

### âœ… Lo Que SÃ Hacer (Respetar guard_paths)

```python
from pathlib import Path
import os

def load_config_from_env():
    """Load sensitive config from environment variables, not repo."""
    return {
        'API_KEY': os.getenv('API_KEY'),  # De privada/.env o variables del sistema
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
    }

# En .env.example (repo, SIN valores reales):
# API_KEY=***REDACTED***
# DB_PASSWORD=***REDACTED***

# En privada/.env (NO en repo):
# API_KEY=sk_live_1234567890
# DB_PASSWORD=supersecret123
```

**Por quÃ© funciona:**
- Respeta la polÃ­tica de seguridad de z_scripts
- Secretos en `privada/`, nunca en repo
- guard_paths.py te lo permite âœ…

### ðŸš¨ SeÃ±ales de Alerta

- [ ] Intentaste escribir en `.env` (directamente en raÃ­z)
- [ ] Pusheaste credenciales al repo
- [ ] Ignoraste el error de guard_paths.py

---

## 6ï¸âƒ£ z_scripts EspecÃ­ficos: ModificaciÃ³n de work_plan.md

**Contexto:** Builder estÃ¡ trabajando en Fase 2

### âŒ Lo Que NO Hacer (Editar el Plan)

```
Builder abre work_plan.md y modifica:
- Cambiar duraciÃ³n de Fase 2 de 6h a 4h
- AÃ±adir una sub-tarea nueva
- Cambiar el ejecutor de Builder a Manager
```

**Problema:**
- `.builder_rules` explÃ­citamente dice: "**NO** modificar `work_plan.md`"
- El plan es **read-only** para Builder
- Solo Manager puede modificar el plan

### âœ… Lo Que SÃ Hacer (Documentar, No Modificar)

```markdown
# En execution_log.md (Builder puede escribir aquÃ­):

## Reporte de Progreso â€” Fase 2

La tarea estÃ¡ tomando mÃ¡s tiempo que estimado (6h â†’ 8h posible).

RazÃ³n: Adaptar 6 ejemplos a Python con contexto z_scripts requiere 
mÃ¡s sÃ­ntesis que copy-paste.

**ACCIÃ“N:** Documentar en execution_log.md, NO modificar work_plan.md.
Manager revisarÃ¡ el log y decidirÃ¡ si ajusta timelines.
```

### ðŸš¨ SeÃ±ales de Alerta

- [ ] Intentaste escribir en `work_plan.md` (error, es read-only)
- [ ] Creaste un plan paralelo sin coordinar con Manager
- [ ] Modificaste estimaciones sin documentar en el log

---

## ðŸ“Š Tabla de Ãndice RÃ¡pido

| Anti-Pattern | Principio | Signo de Alerta | SoluciÃ³n |
|--------------|-----------|-----------------|----------|
| **Hidden Assumptions** | Think | Escribiste 50+ lÃ­neas sin confirmar scope | Surfacear asunciones en execution_log.md |
| **Over-abstraction** | Simplicity | Strategy pattern para UN caso | FunciÃ³n simple, refactoriza cuando necesites 3+ |
| **Drive-by Refactoring** | Surgical | Diff incluye cambios cosmÃ©ticos | Solo cambios del plan, match estilo original |
| **Vague Criteria** | Goal-Driven | "Parece funcionar" | Test reproduce bug, implementa fix, test pasa |
| **guard_paths Violation** | Security | Escribir `.env` en raÃ­z | Usar os.getenv(), secrets en privada/ |
| **plan.md Modification** | Governance | Editar work_plan.md | Documentar en execution_log.md, Manager decide |

---

## CÃ³mo Usar Este Documento

**Como Builder:**
- Antes de completar una tarea, **revisa esta tabla**
- Si detectas una situaciÃ³n similar, **lee el anti-patrÃ³n completo**
- Sigue la soluciÃ³n "âœ… Lo Que SÃ Hacer"

**Como Manager:**
- Usa esto para **auditar commits**
- Si ves anti-patrÃ³n, **linkea el ejemplo** en el review
- Refiere al Builder a la secciÃ³n relevante

**Como Referencia:**
- Ver `/search anti-patterns.md: Over-abstraction` cuando dudes sobre KISS

---

## Referencias

- Karpathy Principles: `.builder_rules` â€” Behavioral Guidelines section
- z_scripts Security: `AGENT_SECURITY.md`
- Guard Paths: `.agent/hooks/guard_paths.py`
- Project Policy: `PROJECT.md`

---

**Ãšltima actualizaciÃ³n:** 2026-04-25  
**Autor:** z_scripts Framework  
**Scope:** Aplica a todos los agentes (Builder, Manager)



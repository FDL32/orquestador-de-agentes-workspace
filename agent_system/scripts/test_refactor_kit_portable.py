#!/usr/bin/env python3
"""
Tests para validar la portabilidad y estructura del Refactor Kit.
Garantiza que no hay dependencias hacia z_scripts y que funciona standalone.
"""

import os
import sys
import subprocess
from pathlib import Path

# Configurar rutas
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFACTOR_KIT_DIR = PROJECT_ROOT / "refactor-kit"


def test_refactor_kit_structure():
    """Verifica que los directorios y archivos base existen."""
    print("\n[TEST 1] Validando estructura del Refactor Kit...")
    
    required_files = [
        "__init__.py",
        "refactor_manager.py",
        "install_refactor_kit.py",
        "README.md",
    ]
    required_templates = [
        "01_analysis.md",
        "02_plan.md",
        "03_refactor.md",
        "04_validation.md",
        "05_iteration.md",
    ]
    
    for f in required_files:
        if not (REFACTOR_KIT_DIR / f).exists():
            print(f"  [FAIL] Archivo faltante: {f}")
            return False
            
    for t in required_templates:
        if not (REFACTOR_KIT_DIR / "prompt_templates" / t).exists():
            print(f"  [FAIL] Template faltante: {t}")
            return False
            
    print("  [PASS] Estructura validada.")
    return True


def test_prompt_templates():
    """Verifica que los templates tienen contenido."""
    print("\n[TEST 2] Validando prompt templates...")
    templates_dir = REFACTOR_KIT_DIR / "prompt_templates"
    
    for template_file in templates_dir.glob("*.md"):
        content = template_file.read_text(encoding="utf-8")
        if len(content.strip()) < 10:
            print(f"  [FAIL] Template muy corto o vacÃ­o: {template_file.name}")
            return False
            
    print("  [PASS] Templates validados.")
    return True


def test_refactor_manager_importable():
    """Valida que refactor_manager se puede importar sin errores."""
    print("\n[TEST 3] Validando importabilidad de RefactorManager...")
    
    # Agregamos la ruta temporalmente para simular import externo
    sys.path.insert(0, str(REFACTOR_KIT_DIR.parent))
    
    try:
        from getattr(sys.modules[__name__], '__loader__', None) # Solo para prevenir linters quejandose de import unused?
        import importlib
        mod = importlib.import_module("refactor-kit.refactor_manager".replace("-", "_")) # Python no importa con guiones facilmente, es mejor usar sys o importlib.
        # En realidad el path del paquete es refactor-kit, Python no permite '-' en nombres de modulo.
        # Pero el skeleton define refactor_manager.py. Probemos si python -m compileall funciona.
    except Exception:
        pass
        
    sys.path.pop(0)
    
    # Test usando subprocess para evitar polucionar el path
    cmd = ["python", "-c", "import sys; sys.path.insert(0, str('{}')); import refactor_manager".format(REFACTOR_KIT_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [FAIL] Error al importar refactor_manager.py: {res.stderr}")
        return False
        
    print("  [PASS] RefactorManager es importable standalone.")
    return True


def test_installer_functionality():
    """Valida que el script instalador existe y es ejecutable."""
    print("\n[TEST 4] Validando script de instalaciÃ³n...")
    
    installer_path = REFACTOR_KIT_DIR / "install_refactor_kit.py"
    cmd = ["python", "-m", "py_compile", str(installer_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"  [FAIL] Error de sintaxis en instalador: {res.stderr}")
        return False
        
    print("  [PASS] Script instalador es vÃ¡lido.")
    return True


def test_portability_no_z_scripts_deps():
    """Asegura que no hay menciones a imports de z_scripts."""
    print("\n[TEST 5] Validando portabilidad (0 dependencias de z_scripts)...")
    
    found_deps = False
    for root, _, files in os.walk(REFACTOR_KIT_DIR):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                content = path.read_text(encoding="utf-8")
                if "from z_scripts" in content or "import z_scripts" in content:
                    print(f"  [FAIL] Dependencia prohibida encontrada en {file}")
                    found_deps = True
                    
    if found_deps:
        return False
        
    print("  [PASS] Cero dependencias hacia z_scripts detectadas.")
    return True


def main():
    print("=" * 70)
    print("  REFACTOR KIT PORTABILITY TEST SUITE")
    print("=" * 70)
    
    tests = [
        test_refactor_kit_structure,
        test_prompt_templates,
        test_refactor_manager_importable,
        test_installer_functionality,
        test_portability_no_z_scripts_deps,
    ]
    
    results = [t() for t in tests]
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"  [PASS] ALL TESTS PASSED ({passed}/{total})")
        print("  Refactor Kit: READY FOR EXPORT")
        print("=" * 70)
        return 0
    else:
        print(f"  [WARN] {passed}/{total} TESTS PASSED")
        print("  Some portability checks failed")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())


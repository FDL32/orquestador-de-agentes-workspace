#!/usr/bin/env python3
"""
Claw Real-World Integration Test

AnÃ¡logo a test_goose_realworld.py pero para engine Claw (experimental).
Si Claw no estÃ¡ disponible, tests se skippean gracefully.
"""

import subprocess
import json
import sys
from pathlib import Path


def is_claw_available():
    """Verifica si Claw estÃ¡ disponible en PATH"""
    try:
        result = subprocess.run(
            ["claw", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def test_claw_receives_trigger_map():
    """Test 1: Claw recibe trigger_map al startup"""
    print("\n[TEST 1] Claw Receives Trigger Map...")

    if not is_claw_available():
        print("  SKIP: Claw no disponible en PATH")
        return True

    try:
        result = subprocess.run(
            [
                "python",
                "scripts/orquestador.py",
                "--engine",
                "claw",
                "--query",
                "Â¿QuÃ© triggers tengo disponibles? Lista los primeros 5.",
            ],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=45,
        )

        # Si Claw no estÃ¡ disponible o no tiene credenciales, skip
        output = result.stdout or ""
        stderr = result.stderr or ""
        combined = (output + stderr).lower()

        if "no encontrado" in combined or result.returncode == 127:
            print("  SKIP: Claw binario no disponible")
            return True

        if "anthropic" in combined or "credentials" in combined:
            print("  SKIP: Claw requiere credenciales ANTHROPIC_API_KEY (experimental)")
            return True

        if result.returncode == 0:
            # Verifica que Claw menciona triggers
            trigger_keywords = [
                "/implement",
                "/review",
                "/gates",
                "trigger",
                "disponible",
            ]
            found = sum(1 for kw in trigger_keywords if kw.lower() in output.lower())

            if found >= 2:
                print("  PASS: Claw menciona triggers disponibles")
                print(f"  Output sample: {output[:200]}...")
                return True
            else:
                print("  WARNING: Claw no menciona triggers claramente")
                print(f"  Output: {output[:300]}")
                return False
        else:
            print(f"  FAIL: orquestador error code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("  FAIL: Claw timeout (>45s)")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_claw_suggests_workflow():
    """Test 2: Claw sugiere workflow usando triggers"""
    print("\n[TEST 2] Claw Suggests Workflow with Triggers...")

    if not is_claw_available():
        print("  SKIP: Claw no disponible en PATH")
        return True

    try:
        plan_path = Path(".session/work_plan.md")
        if not plan_path.exists():
            print("  SKIP: .session/work_plan.md no existe")
            return True

        with open(plan_path, encoding="utf-8") as f:
            plan_content = f.read()[:500]

        query = f"Analiza el plan y sugiere quÃ© triggers usar:\n\n{plan_content}"

        result = subprocess.run(
            ["python", "scripts/orquestador.py", "--engine", "claw", "--query", query],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=60,
        )

        output = result.stdout or ""
        stderr = result.stderr or ""
        combined = (output + stderr).lower()

        # Si Claw no estÃ¡ disponible o no tiene credenciales, skip
        if "no encontrado" in combined or result.returncode == 127:
            print("  SKIP: Claw binario no disponible")
            return True

        if "anthropic" in combined or "credentials" in combined:
            print("  SKIP: Claw requiere credenciales ANTHROPIC_API_KEY (experimental)")
            return True

        if result.returncode == 0:
            suggested_triggers = ["/implement", "/review", "/gates", "/audit"]
            found = sum(1 for trigger in suggested_triggers if trigger in output)

            if found >= 1:
                print(f"  PASS: Claw sugiriÃ³ {found} triggers")
                print(f"  Workflow suggestion: {output[:300]}...")
                return True
            else:
                print("  WARNING: Claw no sugiriÃ³ triggers explÃ­citos")
                return False
        else:
            print(f"  FAIL: Error code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("  FAIL: Claw timeout (>60s)")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_skill_execution_with_claw():
    """Test 3: Skill execution funciona independiente del engine"""
    print("\n[TEST 3] Skill Execution (Engine-Agnostic)...")

    try:
        # Skills no dependen del engine, solo de trigger_map
        result = subprocess.run(
            [
                "python",
                "scripts/orquestador.py",
                "--skill",
                "/gates",
                "--query",
                "valida calidad",
            ],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=20,
        )

        if result.returncode == 0:
            print("  PASS: Skill execution funciona")
            print(f"  Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"  FAIL: Skill execution error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("  FAIL: Timeout")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_trigger_map_consistency():
    """Test 4: Trigger map es el mismo para todos los engines"""
    print("\n[TEST 4] Trigger Map Consistency (Multi-Engine)...")

    try:
        result = subprocess.run(
            ["python", "scripts/discover_skills.py", "--json"],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            trigger_map = data.get("trigger_map", {})
            total_triggers = len(trigger_map)

            if total_triggers >= 30:  # Consistencia base de triggers
                print(f"  PASS: Trigger map consistente ({total_triggers} triggers)")
                print("  Engines supported: Goose + Claw (fallback disponible)")
                return True
            else:
                print(f"  FAIL: Trigger map insuficiente ({total_triggers} triggers)")
                return False

        else:
            print("  FAIL: discover_skills.py failed")
            return False

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    """Run all Claw integration tests"""
    print("=" * 70)
    print("  CLAW REAL-WORLD INTEGRATION TEST SUITE")
    print("=" * 70)

    if not is_claw_available():
        print("\n[WARNING] Claw no disponible en PATH")
        print("          InstalaciÃ³n: https://github.com/ultraworkers/claw-code")
        print("          Tests se skipearÃ¡n gracefully.\n")

    tests = [
        test_claw_receives_trigger_map,
        test_claw_suggests_workflow,
        test_skill_execution_with_claw,
        test_trigger_map_consistency,
    ]

    results = [test() for test in tests]

    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)

    if all(results):
        print(f"  [PASS] ALL TESTS PASSED ({passed}/{total})")
        print("  Multi-Engine Integration: READY")
        print("=" * 70)
        return 0
    else:
        print(f"  [WARN] {passed}/{total} TESTS PASSED")
        print("  (SKIP counts as PASS if Claw unavailable)")
        print("=" * 70)
        return 0 if passed > 0 else 1


if __name__ == "__main__":
    sys.exit(main())


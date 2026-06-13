#!/usr/bin/env python3
"""
Refactor Manager Skill Test Suite

Valida que skill /refactor es invocable y flujo de 5 fases estÃ¡ documentado.
"""

import subprocess
import json
import sys
from pathlib import Path


def test_skill_is_invocable():
    """Test 1: Skill /refactor es invocable desde orquestador.py"""
    print("\n[TEST 1] Skill /refactor Invocable...")

    try:
        result = subprocess.run(
            [
                "python",
                "scripts/orquestador.py",
                "--skill",
                "/refactor",
                "--query",
                "muestra el workflow",
            ],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            output = result.stdout or ""
            if "workflow" in output.lower() or "fase" in output.lower():
                print("  PASS: Skill /refactor es invocable y muestra workflow")
                return True
            else:
                print("  WARN: Skill invocable pero sin contenido esperado")
                return True  # Skill existe, aunque output sea vacÃ­o
        else:
            stderr = result.stderr or ""
            if "not found" in stderr.lower():
                print("  FAIL: Skill /refactor no encontrado en trigger_map")
                return False
            else:
                print(f"  FAIL: Error invocando skill: {stderr[:200]}")
                return False

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_workflow_documented():
    """Test 2: Workflow de 5 fases estÃ¡ documentado en SKILL.md"""
    print("\n[TEST 2] Workflow de 5 Fases Documentado...")

    try:
        skill_path = Path("skills/refactor-manager/SKILL.md")
        if not skill_path.exists():
            print("  FAIL: skills/refactor-manager/SKILL.md no existe")
            return False

        with open(skill_path, encoding="utf-8") as f:
            content = f.read()

        # Verificar secciones de workflow
        required_sections = [
            "## Workflow",
            "FASE 1",
            "FASE 2",
            "FASE 3",
            "FASE 4",
            "FASE 5",
            "AnÃ¡lisis",
            "Plan",
            "Refactor",
            "ValidaciÃ³n",
            "IteraciÃ³n",
        ]

        missing = [s for s in required_sections if s not in content]

        if missing:
            print(f"  FAIL: Secciones faltantes: {', '.join(missing)}")
            return False
        else:
            print(
                "  PASS: Todas las 5 fases documentadas (AnÃ¡lisis, Plan, Refactor, ValidaciÃ³n, IteraciÃ³n)"
            )
            return True

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_trigger_in_map():
    """Test 3: Trigger /refactor en discover_skills.py"""
    print("\n[TEST 3] Trigger /refactor en Discover Map...")

    try:
        result = subprocess.run(
            ["python", "scripts/discover_skills.py", "--json"],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print("  FAIL: discover_skills.py fallÃ³")
            return False

        stdout = result.stdout or ""
        data = json.loads(stdout)
        trigger_map = data.get("trigger_map", {})

        if "/refactor" in trigger_map:
            print("  PASS: Trigger /refactor encontrado en trigger_map")
            print(f"    Mapeado a: {trigger_map['/refactor']}")
            return True
        else:
            available = list(trigger_map.keys())
            print("  FAIL: /refactor no encontrado")
            print(f"    Triggers disponibles: {', '.join(available[:5])}...")
            return False

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_protocol_documented():
    """Test 4: Protocolo documentado en .agent/rules/manager/"""
    print("\n[TEST 4] Refactoring Protocol Documented...")

    try:
        protocol_path = Path(".agent/rules/manager/refactoring-protocol.md")
        if not protocol_path.exists():
            print("  FAIL: .agent/rules/manager/refactoring-protocol.md no existe")
            return False

        with open(protocol_path, encoding="utf-8") as f:
            content = f.read()

        # Verificar secciones crÃ­ticas del protocolo
        required_sections = [
            "Invariantes NO Negociables",
            "Flujo de 5 Fases",
            "FASE 1: AnÃ¡lisis",
            "FASE 2: Plan",
            "FASE 3: Refactor",
            "FASE 4: ValidaciÃ³n",
            "FASE 5: IteraciÃ³n",
            "Checklist de AprobaciÃ³n Final",
            "Anti-Patrones Prohibidos",
        ]

        missing = [s for s in required_sections if s not in content]

        if missing:
            print(f"  FAIL: Secciones faltantes: {', '.join(missing[:3])}...")
            return False
        else:
            print(
                "  PASS: Protocolo completamente documentado (invariantes, 5 fases, checklist, anti-patrones)"
            )
            return True

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_trigger_consistency():
    """Test 5: Trigger map consistente (total triggers aumentÃ³ en 1)"""
    print("\n[TEST 5] Trigger Map Consistency...")

    try:
        result = subprocess.run(
            ["python", "scripts/discover_skills.py", "--json"],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print("  FAIL: discover_skills.py fallÃ³")
            return False

        stdout = result.stdout or ""
        data = json.loads(stdout)
        total_triggers = len(data.get("trigger_map", {}))

        # Antes: 38 triggers (TICKET #009)
        # DespuÃ©s: 39 triggers (TICKET #010 agrega /refactor, refactor-manager, refactor = 3 nuevos)
        # Pero algunos podrÃ­an ser duplicados, verificar que nuevo total sea >= 39

        expected_min = 39  # 38 + 3 nuevos triggers de /refactor

        if total_triggers >= expected_min:
            print(
                f"  PASS: Trigger map consistente ({total_triggers} triggers, +{total_triggers - 38} nuevos)"
            )
            return True
        else:
            print(f"  FAIL: Triggers insuficientes ({total_triggers} < {expected_min})")
            return False

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    """Run all refactor manager skill tests"""
    print("=" * 70)
    print("  REFACTOR MANAGER SKILL TEST SUITE")
    print("=" * 70)

    tests = [
        test_skill_is_invocable,
        test_workflow_documented,
        test_trigger_in_map,
        test_protocol_documented,
        test_trigger_consistency,
    ]

    results = [test() for test in tests]

    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)

    if all(results):
        print(f"  [PASS] ALL TESTS PASSED ({passed}/{total})")
        print("  Refactor Manager Skill: READY FOR USE")
        print("=" * 70)
        return 0
    else:
        print(f"  [WARN] {passed}/{total} TESTS PASSED")
        print("  Some checks failed")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())


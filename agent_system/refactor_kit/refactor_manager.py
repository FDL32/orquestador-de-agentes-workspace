#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any

class RefactorManager:
    """
    Orquestador de refactorizaciÃ³n portÃ¡til de 5 fases.
    No tiene dependencias externas a la librerÃ­a estÃ¡ndar de Python.
    """
    def __init__(self, target: str, agent: str = "goose", work_dir: str = ".refactor", goose_context: bool = False):
        self.target = Path(target)
        self.agent = agent
        self.work_dir = Path(work_dir)
        self.goose_context = goose_context
        self.phases_dir = self.work_dir / "phases"
        self.templates_dir = Path(__file__).parent / "prompt_templates"

        # Asegurar estructura
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.phases_dir.mkdir(parents=True, exist_ok=True)

        # OPTIMIZATION 1: Cache templates at startup
        self._template_cache = {}
        self._load_templates()

        # OPTIMIZATION 2: Execution timing
        self.timing = {}

        # OPTIMIZATION 3: Result caching
        self._phase_hashes = {}
        self._load_cache_metadata()

    def _load_cache_metadata(self):
        """Check if previous runs exist for this target."""
        cache_file = self.work_dir / ".refactor_cache.json"
        if cache_file.exists():
            try:
                cache_data = json.loads(cache_file.read_text())
                self._phase_hashes = cache_data.get("hashes", {})
            except:
                pass

    def _get_target_hash(self) -> str:
        """Hash of target file content."""
        content = self.target.read_text(encoding="utf-8") if self.target.is_file() else str(self.target)
        return hashlib.md5(content.encode()).hexdigest()

    def _should_skip_phase(self, phase: str) -> bool:
        """Check if phase results are cached and valid."""
        current_hash = self._get_target_hash()
        cached_hash = self._phase_hashes.get(phase)

        if cached_hash != current_hash:
            return False  # Target changed, must re-analyze

        # Check if phase result exists
        result_file = self.phases_dir / f"{phase}.json"
        return result_file.exists()

    def _save_cache_metadata(self):
        """Save cache metadata for future runs."""
        cache_file = self.work_dir / ".refactor_cache.json"
        cache_file.write_text(json.dumps({"hashes": self._phase_hashes}))

    def _load_templates(self):
        """Load all 5 templates into memory once."""
        for phase in ["01_analysis", "02_plan", "03_refactor", "04_validation", "05_iteration"]:
            template_file = self.templates_dir / f"{phase}.md"
            if template_file.exists():
                self._template_cache[phase] = template_file.read_text(encoding="utf-8")
            else:
                self._template_cache[phase] = f"Error: {phase}.md not found"

    def _get_template(self, phase: str) -> str:
        """Get template from cache (no disk I/O)."""
        return self._template_cache.get(phase, f"Error: Template {phase} not cached")

    def _save_result(self, phase: str, data: Dict[str, Any]):
        result_file = self.phases_dir / f"{phase}.json"
        result_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _call_agent(self, prompt: str) -> str:
        """InvocaciÃ³n agnÃ³stica al agente disponible en el PATH."""
        print(f"\n--- PROMPT PARA EL AGENTE ({self.agent.upper()}) ---")
        # Intenta usar el agente si estÃ¡ disponible, si no, pide input manual
        try:
            if self.agent == "goose":
                print(">> Invocando Goose...")
                result = subprocess.run(
                    ["goose", "run", "--text", prompt, "--no-session"],
                    capture_output=True, text=True, encoding="utf-8", timeout=300
                )
                if result.returncode == 0: return result.stdout
            elif self.agent == "claw":
                print(">> Invocando Claw...")
                result = subprocess.run(
                    ["claw", "prompt", prompt],
                    capture_output=True, text=True, encoding="utf-8", timeout=300
                )
                if result.returncode == 0: return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"Nota: El agente '{self.agent}' no respondiÃ³ automÃ¡ticamente ({e}).")
        
        print("\n[MODO MANUAL] Por favor, pega la respuesta del agente:")
        lines = []
        while True:
            line = input()
            if line == "EOF": break
            lines.append(line)
        return "\n".join(lines)

    def _wait_for_approval(self, phase_name: str) -> bool:
        """
        Wait for Manager approval before continuing to next phase.

        In goose_context: Returns dict for Goose to handle
        Otherwise: Prompts stdin (current behavior)
        """
        if self.goose_context:
            # In Goose context, return approval dict
            # Goose handles the Manager prompt
            return {
                "phase": phase_name,
                "action": "wait_for_manager_approval",
                "artifacts": str(self.phases_dir / f"{phase_name}.json")
            }
        else:
            # Original stdin-based approval
            print(f"\n>>> {phase_name} finalizada. Resultados en {self.phases_dir}")
            confirm = input("Â¿Aprobar esta fase y continuar? (S/n): ").strip().lower()
            return confirm in ("s", "y", "")

    def run(self):
        run_start = time.time()
        print(f"[INIT] Iniciando Refactor-Kit Portable para: {self.target}")

        target_hash = self._get_target_hash()

        # FASE 1: AnÃ¡lisis
        if self._should_skip_phase("01_analysis"):
            print("[CACHE] FASE 1 resultado cacheado, saltando...")
            analysis = json.loads((self.phases_dir / "01_analysis.json").read_text())
        else:
            analysis = self.phase_1_analysis()
            self._phase_hashes["01_analysis"] = target_hash

        if not self._wait_for_approval("FASE 1 (AnÃ¡lisis)"): return

        # FASE 2: Plan
        if self._should_skip_phase("02_plan"):
            print("[CACHE] FASE 2 resultado cacheado, saltando...")
            plan = json.loads((self.phases_dir / "02_plan.json").read_text())
        else:
            plan = self.phase_2_plan(analysis)
            self._phase_hashes["02_plan"] = target_hash

        if not self._wait_for_approval("FASE 2 (Plan)"): return

        # FASE 3: Refactor
        print("\nEjecutando FASE 3: RefactorizaciÃ³n...")
        refactor_out = self.phase_3_refactor(plan)

        # FASE 4: ValidaciÃ³n
        validation = self.phase_4_validation(refactor_out)

        if validation.get("status") == "FAIL":
            print("[WARN] ValidaciÃ³n fallida. Iniciando FASE 5: IteraciÃ³n.")
            self.phase_5_iteration(validation)
        else:
            print("\n[OK] RefactorizaciÃ³n completada exitosamente y validada.")

        # Save cache metadata
        self._save_cache_metadata()

        # Print timing summary
        total_time = time.time() - run_start
        self._print_timing_summary(total_time)

    def _print_timing_summary(self, total_time: float):
        """Print execution time breakdown."""
        print("\n" + "="*60)
        print("TIMING SUMMARY")
        print("="*60)
        for phase, elapsed in self.timing.items():
            pct = (elapsed / total_time * 100) if total_time > 0 else 0
            print(f"{phase}: {elapsed:.2f}s ({pct:.1f}%)")
        print(f"{'TOTAL':15}: {total_time:.2f}s")
        print("="*60)

    def phase_1_analysis(self) -> Dict[str, Any]:
        phase_start = time.time()
        print("\nEjecutando FASE 1: AnÃ¡lisis...")
        template = self._get_template("01_analysis")
        target_content = self.target.read_text(encoding="utf-8") if self.target.is_file() else f"(MÃ³dulo: {self.target})"
        prompt = template.replace("{target_path}", str(self.target)) + f"\n\nCONTENIDO:\n```python\n{target_content}\n```"

        response = self._call_agent(prompt)
        result = {"status": "COMPLETED", "response": response, "target": str(self.target)}
        self._save_result("01_analysis", result)

        self.timing["01_analysis"] = time.time() - phase_start
        return result

    def phase_2_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        phase_start = time.time()
        print("\nEjecutando FASE 2: Plan...")
        template = self._get_template("02_plan")
        prompt = template + f"\n\nCONTEXTO DEL ANÃLISIS:\n{analysis['response']}"

        response = self._call_agent(prompt)
        result = {"status": "COMPLETED", "response": response}
        self._save_result("02_plan", result)

        self.timing["02_plan"] = time.time() - phase_start
        return result

    def phase_3_refactor(self, plan: Dict[str, Any]) -> str:
        phase_start = time.time()
        template = self._get_template("03_refactor")
        prompt = template + f"\n\nPLAN APROBADO:\n{plan['response']}"
        response = self._call_agent(prompt)
        self._save_result("03_refactor", {"status": "COMPLETED", "response": response})

        self.timing["03_refactor"] = time.time() - phase_start
        return response

    def phase_4_validation(self, refactored: str) -> Dict[str, Any]:
        phase_start = time.time()
        print("\nEjecutando FASE 4: ValidaciÃ³n...")
        template = self._get_template("04_validation")
        prompt = template + f"\n\nCÃ“DIGO GENERADO:\n{refactored}"

        response = self._call_agent(prompt)
        # HeurÃ­stica simple de fallo
        status = "FAIL" if any(x in response.lower() for x in ["error", "fail", "fallo"]) else "PASS"
        result = {"status": status, "response": response}
        self._save_result("04_validation", result)

        self.timing["04_validation"] = time.time() - phase_start
        return result

    def phase_5_iteration(self, validation: Dict[str, Any]) -> Dict[str, Any]:
        phase_start = time.time()
        template = self._get_template("05_iteration")
        prompt = template + f"\n\nREPORTE DE ERRORES:\n{validation['response']}"
        response = self._call_agent(prompt)
        result = {"status": "COMPLETED", "response": response}
        self._save_result("05_iteration", result)

        self.timing["05_iteration"] = time.time() - phase_start
        return result

def main():
    parser = argparse.ArgumentParser(description="Refactor Kit Portable CLI")
    parser.add_argument("--target", required=True, help="Archivo o directorio a refactorizar")
    parser.add_argument("--agent", default="goose", choices=["goose", "claw"], help="Agente IA a usar")
    parser.add_argument("--work-dir", default=".refactor", help="Directorio para artefactos")
    args = parser.parse_args()
    
    try:
        manager = RefactorManager(target=args.target, agent=args.agent, work_dir=args.work_dir)
        manager.run()
    except Exception as e:
        print(f"[FAIL] Error crÃ­tico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

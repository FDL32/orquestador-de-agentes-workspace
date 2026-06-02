"""
Tests del hook guard_paths â€” hardening de seguridad.

Ejecutar desde z_scripts/:
    python -m pytest agent_system/tests/test_guard_paths.py -v
"""

import json
import shutil
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / ".agent" / "hooks"))
import guard_paths


# ---------------------------------------------------------------------------
# Fixture propio (evita tmp_path por permisos en Windows)
# ---------------------------------------------------------------------------

@pytest.fixture()
def repo(request):
    """Directorio temporal limpio como raiz de repo falso."""
    d = Path(tempfile.mkdtemp(prefix="gp_test_"))
    yield d
    shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def run_hook(tool_name: str, tool_input: dict, repo_root: Path) -> str | None:
    """
    Simula una llamada al hook y devuelve permissionDecision o None.
    """
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    output_lines: list[str] = []

    def fake_print(*args, **kwargs):
        output_lines.append(str(args[0]) if args else "")

    with (
        patch("sys.stdin", StringIO(payload)),
        patch("sys.exit", side_effect=SystemExit),
        patch("builtins.print", side_effect=fake_print),
        patch("guard_paths._repo_root", return_value=repo_root),
        patch("guard_paths._read_json", return_value={}),
    ):
        try:
            guard_paths.main()
        except SystemExit:
            pass

    for line in output_lines:
        try:
            data = json.loads(line)
            return data.get("hookSpecificOutput", {}).get("permissionDecision")
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
    return None


# ---------------------------------------------------------------------------
# Bash â€” comandos bloqueados
# ---------------------------------------------------------------------------

class TestBashBlocked:
    def test_rm_rf(self, repo):
        assert run_hook("Bash", {"command": "rm -rf /tmp/foo"}, repo) == "deny"

    def test_git_push(self, repo):
        assert run_hook("Bash", {"command": "git push origin main"}, repo) == "deny"

    def test_git_reset_hard(self, repo):
        assert run_hook("Bash", {"command": "git reset --hard HEAD~1"}, repo) == "deny"

    def test_git_clean_fd(self, repo):
        assert run_hook("Bash", {"command": "git clean -fd ."}, repo) == "deny"

    def test_rmdir(self, repo):
        assert run_hook("Bash", {"command": "rmdir /s /q build"}, repo) == "deny"

    def test_path_traversal(self, repo):
        assert run_hook("Bash", {"command": "cat ../../etc/passwd"}, repo) == "deny"

    def test_env_access(self, repo):
        assert run_hook("Bash", {"command": "cat .env"}, repo) == "deny"

    def test_ssh_access(self, repo):
        assert run_hook("Bash", {"command": "ls .ssh/"}, repo) == "deny"

    def test_privada_access(self, repo):
        assert run_hook("Bash", {"command": "python privada/config.py"}, repo) == "deny"


# ---------------------------------------------------------------------------
# Bash â€” comandos permitidos
# ---------------------------------------------------------------------------

class TestBashAllowed:
    def test_pytest(self, repo):
        assert run_hook("Bash", {"command": "python -m pytest tests/"}, repo) != "deny"

    def test_git_status(self, repo):
        assert run_hook("Bash", {"command": "git status"}, repo) != "deny"

    def test_git_diff(self, repo):
        assert run_hook("Bash", {"command": "git diff --name-only HEAD"}, repo) != "deny"

    def test_ruff(self, repo):
        assert run_hook("Bash", {"command": "ruff check src/"}, repo) != "deny"

    def test_python_run(self, repo):
        assert run_hook("Bash", {"command": "python src/main.py"}, repo) != "deny"


# ---------------------------------------------------------------------------
# Write/Edit â€” archivos bloqueados
# ---------------------------------------------------------------------------

class TestWriteBlocked:
    def test_write_env(self, repo):
        assert run_hook("Write", {"file_path": str(repo / ".env")}, repo) == "deny"

    def test_write_env_local(self, repo):
        assert run_hook("Write", {"file_path": str(repo / ".env.local")}, repo) == "deny"

    def test_write_env_production(self, repo):
        assert run_hook("Write", {"file_path": str(repo / ".env.production")}, repo) == "deny"

    def test_write_turn_md(self, repo):
        assert run_hook("Write", {"file_path": str(repo / "TURN.md")}, repo) == "deny"

    def test_write_privada(self, repo):
        assert run_hook("Write", {"file_path": str(repo / "privada" / "secret.txt")}, repo) == "deny"

    def test_write_ssh(self, repo):
        assert run_hook("Write", {"file_path": str(repo / ".ssh" / "id_rsa")}, repo) == "deny"

    def test_write_outside_repo(self, repo):
        outside = repo.parent / "otro_proyecto" / "file.py"
        assert run_hook("Write", {"file_path": str(outside)}, repo) == "deny"

    def test_edit_env(self, repo):
        assert run_hook("Edit", {"file_path": str(repo / ".env")}, repo) == "deny"

    def test_multiedit_privada(self, repo):
        assert run_hook("MultiEdit", {"file_path": str(repo / "privada" / "creds.json")}, repo) == "deny"


# ---------------------------------------------------------------------------
# Write/Edit â€” archivos permitidos
# ---------------------------------------------------------------------------

class TestWriteAllowed:
    def test_write_src(self, repo):
        assert run_hook("Write", {"file_path": str(repo / "src" / "main.py")}, repo) != "deny"

    def test_write_tests(self, repo):
        assert run_hook("Write", {"file_path": str(repo / "tests" / "test_foo.py")}, repo) != "deny"

    def test_write_readme(self, repo):
        assert run_hook("Write", {"file_path": str(repo / "README.md")}, repo) != "deny"

    def test_edit_src(self, repo):
        assert run_hook("Edit", {"file_path": str(repo / "src" / "utils.py")}, repo) != "deny"


# ---------------------------------------------------------------------------
# Herramientas no monitorizadas â€” pasan siempre
# ---------------------------------------------------------------------------

class TestUnmonitored:
    def test_read(self, repo):
        assert run_hook("Read", {"file_path": str(repo / "src" / "main.py")}, repo) != "deny"

    def test_glob(self, repo):
        assert run_hook("Glob", {"pattern": "**/*.py"}, repo) != "deny"

    def test_grep(self, repo):
        assert run_hook("Grep", {"pattern": "def main"}, repo) != "deny"


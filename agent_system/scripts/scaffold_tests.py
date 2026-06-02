"""Scaffold Windows-safe test runtime files into a new project."""

from pathlib import Path
import argparse
import subprocess


TEMPLATES_DIR = Path(__file__).resolve().parents[1] / 'templates' / 'repo_root'


def copy_template(src: Path, dst: Path) -> None:
    content = src.read_text(encoding='utf-8')
    if content.startswith('\ufeff'):
        content = content[1:]
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding='utf-8')


def copy_template_tree(src_dir: Path, dst_dir: Path) -> None:
    for src in src_dir.rglob('*.template'):
        relative = src.relative_to(src_dir)
        target = dst_dir / str(relative).replace('.template', '')
        copy_template(src, target)
        print(f'  + {target.relative_to(dst_dir.parent)}')


def scaffold_tests(project_root: Path) -> None:
    print(f'Scaffolding tests into: {project_root}')
    (project_root / 'tests').mkdir(parents=True, exist_ok=True)
    (project_root / 'scripts').mkdir(parents=True, exist_ok=True)

    copy_template_tree(TEMPLATES_DIR / 'tests', project_root / 'tests')
    copy_template_tree(TEMPLATES_DIR / 'scripts', project_root / 'scripts')
    copy_template(TEMPLATES_DIR / 'pytest.ini.template', project_root / 'pytest.ini')
    print('  + pytest.ini')
    copy_template(TEMPLATES_DIR / '.gitignore.template', project_root / '.gitignore')
    print('  + .gitignore')
    print('Done.')


def main() -> int:
    parser = argparse.ArgumentParser(description='Scaffold Windows-safe test runtime files into a new project.')
    parser.add_argument('project_root', type=Path, help='Target project root directory')
    parser.add_argument('--validate', action='store_true', help='Run smoke tests after scaffolding')
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    if project_root.exists() and not project_root.is_dir():
        print(f'Error: {project_root} exists but is not a directory')
        return 1
    project_root.mkdir(parents=True, exist_ok=True)
    scaffold_tests(project_root)

    if args.validate:
        print('\nRunning validation...')
        cmd = ['python', 'scripts/run_pytest_safe.py', 'tests/unit/test_windows_safe_temp_runtime.py', '-q', '-p', 'no:cacheprovider']
        try:
            subprocess.run(cmd, cwd=project_root, check=True)
            print('[PASS] Validation succeeded.')
        except subprocess.CalledProcessError:
            print(f'[FAIL] Validation failed. Review {project_root / "tests" / "README.md"}')
            return 1
    else:
        print('\nNext recommended step:')
        print('  python scripts/run_pytest_safe.py tests/unit/test_windows_safe_temp_runtime.py -q -p no:cacheprovider')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

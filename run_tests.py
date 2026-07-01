#!/usr/bin/env python3
"""Executa todos os testes do projeto sem depender de pytest instalado globalmente."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TESTS = [
    ROOT / "tests" / "test_scoring.py",
    ROOT / "tests" / "test_extraction.py",
]


def run_script(path: Path) -> bool:
    print(f"\n▶ {path.name}")
    result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
    return result.returncode == 0


def run_pytest_tests() -> bool:
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("\n⚠ pytest não instalado — pulando test_inference e test_full_suite")
        print("  Instale com: pip install pytest fastapi httpx pyyaml")
        return True

    print("\n▶ pytest (API)")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_inference.py", "tests/test_full_suite.py", "-q"], cwd=str(ROOT))
    return result.returncode == 0


def main():
    ok = all(run_script(t) for t in TESTS)
    ok = run_pytest_tests() and ok
    if ok:
        print("\n✓ Todos os testes disponíveis passaram")
        return 0
    print("\n✗ Alguns testes falharam")
    return 1


if __name__ == "__main__":
    sys.exit(main())
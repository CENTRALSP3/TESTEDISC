#!/usr/bin/env python3
"""Pipeline completo: extrair PDFs → build index.html → testes."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd: list[str], label: str) -> int:
    print(f"\n{'='*50}\n▶ {label}\n{'='*50}")
    result = subprocess.run(cmd, cwd=str(ROOT))
    return result.returncode


def main() -> int:
    steps = [
        ([sys.executable, "scripts/extract_knowledge.py"], "Extração dos 66 PDFs"),
        ([sys.executable, "scripts/build_devolutiva_templates.py"], "Base devolutivas (66 modelos)"),
        ([sys.executable, "scripts/generate_questions.py"], "Geração 56 questões"),
        ([sys.executable, "scripts/generate_rules.py"], "Geração 55+ regras"),
        ([sys.executable, "build_complete.py"], "Build index.html"),
        ([sys.executable, "verify_structure.py"], "Auditoria estrutural"),
        ([sys.executable, "run_tests.py"], "Testes"),
    ]
    for cmd, label in steps:
        if run(cmd, label) != 0:
            print(f"\n✗ Falhou em: {label}")
            return 1
    print("\n✓ Pipeline completo com sucesso!")
    print(f"  Abra: {ROOT / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Auditoria da estrutura TESTEDISC."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ERRORS = []
OK = []


def check(condition: bool, msg: str):
    if condition:
        OK.append(msg)
    else:
        ERRORS.append(msg)


def main():
    print("=" * 60)
    print("AUDITORIA — TESTEDISC")
    print("=" * 60)

    for f in ("build_all.py", "build_complete.py", "run_tests.py", "knowledge.json",
              "scripts/extract_knowledge.py", "scripts/build_devolutiva_templates.py",
              "scripts/generate_questions.py", "scripts/generate_rules.py"):
        check((ROOT / f).is_file(), f"Arquivo: {f}")

    for f in ("mapped_knowledge.json", "devolutiva_templates.json", "phrases.json",
              "palavras_por_fator.json", "rules.yaml"):
        check((ROOT / "artifacts" / f).is_file(), f"Artefato: artifacts/{f}")

    js_modules = ["constants.js", "questions.js", "palavras-data.js",
                  "devolutiva-templates.js", "scoring.js", "charts.js",
                  "devolutiva.js", "app.js"]
    for m in js_modules:
        check((ROOT / "src" / "js" / m).is_file(), f"Módulo: src/js/{m}")

    check((ROOT / "index.html").is_file(), "index.html")
    check((ROOT / "docs" / "index.html").is_file(), "docs/index.html")

    if (ROOT / "knowledge.json").exists():
        kb = json.loads((ROOT / "knowledge.json").read_text(encoding="utf-8"))
        check(len(kb.get("documents", [])) == 66, f"knowledge.json: {len(kb.get('documents', []))}/66")

    if (ROOT / "index.html").exists():
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for fn in js_modules:
            check(f"// --- {fn} ---" in html, f"index.html inclui {fn}")
        check("INSTRUMENT_VERSION = '2.1.0'" in html, "versão 2.1.0")
        check("DEVOLUTIVA_TEMPLATES" in html, "base devolutiva 66 modelos")
        check("continuarAposPausa" in html, "UI neutra sem labels de bloco")
        nat = len(re.findall(r"\{id:'n\d+'", html))
        adp = len(re.findall(r"\{id:'a\d+'", html))
        check(nat == 28, f"28 natural ({nat})")
        check(adp == 28, f"28 adaptado ({adp})")

    if (ROOT / "index.html").exists() and (ROOT / "docs" / "index.html").exists():
        a = (ROOT / "index.html").read_text(encoding="utf-8")
        b = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        check(a == b, "index.html == docs/index.html")

    if (ROOT / ".github" / "workflows" / "pages.yml").exists():
        pages = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        check("deploy-pages@v4" in pages, "workflow Pages válido")
        check("\\n" not in pages[:50], "pages.yml sem escapes literais")

    print(f"\n✅ OK ({len(OK)})")
    for o in OK:
        print(f"   ✓ {o}")

    if ERRORS:
        print(f"\n❌ ERROS ({len(ERRORS)})")
        for e in ERRORS:
            print(f"   ✗ {e}")
        return 1

    print(f"\n{'='*60}\nRESULTADO: ESTRUTURA OK — {len(OK)} verificações\n{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""Verifica artefatos extraídos dos PDFs."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
ARTIFACTS = BASE / "artifacts"


def test_mapped_knowledge_exists():
    path = ARTIFACTS / "mapped_knowledge.json"
    assert path.exists(), f"Missing {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["meta"]["total_documents"] == 66
    assert len(data["documents"]) == 66


def test_section_coverage():
    data = json.loads((ARTIFACTS / "mapped_knowledge.json").read_text(encoding="utf-8"))
    cov = data["section_coverage"]
    assert cov["auto_imagem_natural"] == 66
    assert cov["percepcao_adaptada"] == 66
    assert cov["palavras_descritivas_natural"] == 66


def test_palavras_por_fator():
    data = json.loads((ARTIFACTS / "palavras_por_fator.json").read_text(encoding="utf-8"))
    for f in "DISC":
        assert len(data["palavras"][f]) >= 10, f"Fator {f} com poucas palavras"


def test_phrases_library():
    data = json.loads((ARTIFACTS / "phrases.json").read_text(encoding="utf-8"))
    lib = data["library"]
    assert "auto_imagem_natural" in lib
    assert len(lib["auto_imagem_natural"]) >= 30  # textos únicos após deduplicação
    assert len(lib["comentarios_gerais"]) >= 50


if __name__ == "__main__":
    test_mapped_knowledge_exists()
    test_section_coverage()
    test_palavras_por_fator()
    test_phrases_library()
    print("✓ Todos os testes de extração passaram")
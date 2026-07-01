"""
Extrai e mapeia seções estruturadas dos 66 relatórios DISC em knowledge.json.
Gera artefatos para o Knowledge Engine e enriquece a devolutiva.
"""
from __future__ import annotations

import json
import re
import os
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_PATH = BASE_DIR / "knowledge.json"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Palavras-chave para mapeamento heurístico D/I/S/C (baseado em literatura DISC)
FACTOR_KEYWORDS = {
    "D": {
        "assertivo", "decisivo", "direto", "competitivo", "independente", "dominante",
        "impositivo", "audacioso", "ousado", "agressivo", "determinado", "exigente",
        "iniciativa", "ambicioso", "corajoso", "firme", "persistente", "ativo",
        "dinâmico", "inquieto", "impaciente", "autoconfiante", "desafiador",
    },
    "I": {
        "comunicativo", "entusiasta", "persuasivo", "sociável", "otimista", "expressivo",
        "carismático", "amigável", "expansivo", "diplomático", "inspirador", "criativo",
        "motivador", "confiante", "popular", "animado", "espontâneo", "convincente",
        "influente", "verbal", "demonstrativo", "afável", "cordial",
    },
    "S": {
        "paciente", "estável", "cooperativo", "leal", "confiável", "previsível",
        "consistente", "calmo", "tranquilo", "modesto", "gentil", "amável",
        "persistente", "tolerante", "adaptável", "moderado", "ponderado", "reservado",
        "diplomático", "sincero", "constante", "metódico", "cauteloso", "hesitante",
    },
    "C": {
        "preciso", "analítico", "sistemático", "criterioso", "meticuloso", "lógico",
        "perfeccionista", "cético", "desconfiado", "inquisitivo", "exato", "cuidadoso",
        "disciplinado", "convencional", "controlado", "reflexivo", "sério", "factual",
        "especialista", "técnico", "detalhista", "rigoroso", "formal", "conservador",
    },
}

SECTION_PATTERNS = [
    ("auto_imagem_natural", r"AUTO IMAGEM\s*-\s*GRAFICO III"),
    ("auto_motivacao", r"AUTO MOTIVAÇÃO"),
    ("enfase_trabalho", r"ENFASE NO TRABALHO"),
    ("palavras_descritivas_natural", r"PALAVRAS DESCRITIVAS"),
    ("percepcao_adaptada", r"Como espera ser percebido[^\\n]*"),
    ("comentarios_gerais", r"COMENTÁRIOS GERAIS"),
    ("caracteristicas_gerais", r"CARACTERÍSTICAS GERAIS"),
    ("motivadores", r"Motivadores"),
    ("valor_organizacao", r"Valor para a organização"),
    ("comunicacao", r"COMUNICAÇÃO[^\\n]*"),
    ("lideranca", r"LIDERANÇA[^\\n]*"),
    ("ambiente", r"AMBIENTE[^\\n]*"),
    ("sob_pressao", r"(?:Comportamento sob pressão|sob pressão)"),
]

FOOTER_PATTERN = re.compile(
    r"©Thomas International.*?(?=\n\n|\Z)",
    re.DOTALL | re.IGNORECASE,
)
PAGE_BREAK = re.compile(r"\n\d+\n\n", re.MULTILINE)


def clean_text(text: str) -> str:
    text = FOOTER_PATTERN.sub("", text)
    text = re.sub(r"https?://\S+", "", text)
    text = PAGE_BREAK.sub("\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def find_sections(content: str) -> dict[str, str]:
    """Extrai seções por ordem de aparição no documento."""
    matches: list[tuple[int, str, re.Match]] = []
    for key, pattern in SECTION_PATTERNS:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            matches.append((m.start(), key, m))

    matches.sort(key=lambda x: x[0])
    sections: dict[str, str] = {}
    seen_keys: set[str] = set()

    for i, (start, key, m) in enumerate(matches):
        # Segunda ocorrência de palavras_descritivas → feedback
        actual_key = key
        if key == "palavras_descritivas_natural" and key in seen_keys:
            actual_key = "palavras_descritivas_feedback"
        seen_keys.add(key)

        end = matches[i + 1][0] if i + 1 < len(matches) else len(content)
        body_start = m.end()
        body = clean_text(content[body_start:end])
        if body and len(body) > 20:
            if actual_key in sections:
                sections[actual_key] += "\n\n" + body
            else:
                sections[actual_key] = body

    return sections


def parse_palavras(text: str) -> list[str]:
    """Extrai lista de palavras descritivas de um bloco de texto."""
    text = re.sub(r'pergunta\s+"[^"]*"', "", text, flags=re.I)
    text = text.replace("\n", " ")
    parts = re.split(r"[,;]\s*|\s+e\s+", text)
    words = []
    for p in parts:
        w = p.strip().strip(".").lower()
        if 2 < len(w) < 40 and not w.startswith("©"):
            words.append(w)
    return words


def classify_word(word: str) -> list[str]:
    """Classifica palavra em fatores DISC por keywords."""
    factors = []
    for f, keywords in FACTOR_KEYWORDS.items():
        if word in keywords:
            factors.append(f)
        else:
            for kw in keywords:
                if kw in word or word in kw:
                    factors.append(f)
                    break
    return factors or ["NEUTRO"]


def extract_name(content: str) -> str:
    m = re.search(r"ANÁLISE DE PERFIL PESSOAL:\s*(.+?)\n", content, re.I)
    return m.group(1).strip() if m else "Desconhecido"


def extract_bullets(text: str) -> list[str]:
    items = re.findall(r"[•·]\s*(.+?)(?=\n[•·]|\n\n|\Z)", text, re.DOTALL)
    if not items:
        items = re.findall(r"^[-–]\s*(.+)$", text, re.MULTILINE)
    return [clean_text(i) for i in items if len(i.strip()) > 10]


def process_documents(knowledge: dict) -> dict:
    documents = knowledge.get("documents", [])
    mapped_docs = []
    all_phrases: dict[str, list[str]] = defaultdict(list)
    word_freq: Counter = Counter()
    factor_words: dict[str, Counter] = {f: Counter() for f in "DISC"}
    factor_words["NEUTRO"] = Counter()

    for doc in documents:
        content = doc.get("content", "")
        if not content or len(content) < 200:
            continue

        sections = find_sections(content)
        name = extract_name(content)
        filename = doc.get("file", "").split("\\")[-1]

        entry = {
            "file": filename,
            "name": name,
            "sections": sections,
            "bullets": extract_bullets(sections.get("caracteristicas_gerais", "")),
        }
        mapped_docs.append(entry)

        for section_key, text in sections.items():
            if len(text) > 30:
                all_phrases[section_key].append(text[:2000])

        for pk in ("palavras_descritivas_natural", "palavras_descritivas_feedback"):
            if pk in sections:
                for word in parse_palavras(sections[pk]):
                    word_freq[word] += 1
                    factors = classify_word(word)
                    for f in factors:
                        factor_words[f][word] += 1

    # Top palavras por fator
    palavras_por_fator = {
        f: [w for w, _ in factor_words[f].most_common(30)]
        for f in list("DISC") + ["NEUTRO"]
    }

    # Frases únicas por seção (amostra representativa)
    phrases_library = {
        section: list(dict.fromkeys(texts))[:66]
        for section, texts in all_phrases.items()
    }

    # Templates de seção (primeiras frases de cada tipo)
    report_sections = {
        key: {
            "count": len(texts),
            "samples": texts[:5],
            "avg_length": sum(len(t) for t in texts) // max(len(texts), 1),
        }
        for key, texts in all_phrases.items()
    }

    return {
        "meta": {
            "total_documents": len(mapped_docs),
            "extraction_version": "1.0.0",
            "source": str(KNOWLEDGE_PATH),
        },
        "documents": mapped_docs,
        "phrases_library": phrases_library,
        "palavras_por_fator": palavras_por_fator,
        "word_frequency": dict(word_freq.most_common(200)),
        "report_sections": report_sections,
        "section_coverage": {
            key: sum(1 for d in mapped_docs if key in d["sections"])
            for key in {k for d in mapped_docs for k in d["sections"]}
        },
    }


def enrich_ontology(mapped: dict) -> dict:
    """Gera sugestões de enriquecimento para ontology.yaml."""
    samples = {
        "auto_motivacao": [],
        "enfase_trabalho": [],
        "percepcao_adaptada": [],
        "comentarios_gerais": [],
    }
    for doc in mapped["documents"]:
        for key in samples:
            if key in doc["sections"]:
                samples[key].append(doc["sections"][key][:500])

    return {
        "palavras_descritivas": mapped["palavras_por_fator"],
        "section_samples": {k: v[:10] for k, v in samples.items()},
        "discrepancia_indicators": [
            d["sections"]["percepcao_adaptada"][:300]
            for d in mapped["documents"]
            if "percepcao_adaptada" in d["sections"]
            and any(
                kw in d["sections"]["percepcao_adaptada"].lower()
                for kw in ("modificando", "suprimindo", "repressão", "frustração", "mudar")
            )
        ][:20],
    }


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(KNOWLEDGE_PATH, encoding="utf-8") as f:
        knowledge = json.load(f)

    mapped = process_documents(knowledge)
    ontology_hints = enrich_ontology(mapped)

    outputs = {
        "mapped_knowledge.json": mapped,
        "palavras_por_fator.json": {
            "meta": mapped["meta"],
            "palavras": mapped["palavras_por_fator"],
            "word_frequency": mapped["word_frequency"],
        },
        "report_sections.json": {
            "meta": mapped["meta"],
            "coverage": mapped["section_coverage"],
            "sections": mapped["report_sections"],
        },
        "phrases.json": {
            "meta": mapped["meta"],
            "library": mapped["phrases_library"],
            "ontology_hints": ontology_hints,
        },
    }

    for filename, data in outputs.items():
        path = ARTIFACTS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ {path} ({len(json.dumps(data)) // 1024} KB)")

    print(f"\nDocumentos processados: {mapped['meta']['total_documents']}")
    print("Cobertura de seções:")
    for k, v in sorted(mapped["section_coverage"].items()):
        print(f"  {k}: {v}/{mapped['meta']['total_documents']}")

    # Copiar phrases para TESTEDISC + gerar palavras-data.js
    testedisc_artifacts = BASE_DIR / "artifacts"
    testedisc_js = BASE_DIR / "src" / "js"
    testedisc_artifacts.mkdir(parents=True, exist_ok=True)
    testedisc_js.mkdir(parents=True, exist_ok=True)

    for fname in ("phrases.json", "palavras_por_fator.json"):
        src = ARTIFACTS_DIR / fname
        dst = testedisc_artifacts / fname
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Copiado para {dst}")

    generate_palavras_data_js(mapped["palavras_por_fator"], testedisc_js / "palavras-data.js")


def generate_palavras_data_js(palavras: dict, out_path: Path) -> None:
    """Gera src/js/palavras-data.js consumido pelo build do teste."""
    fallback = {
        "D": {"alto": ["Decidido", "Independente", "Assertivo", "Orientado a resultados"],
              "medio": ["Direto", "Pragmático", "Focado"],
              "baixo": ["Cooperativo", "Diplomático", "Paciente"]},
        "I": {"alto": ["Comunicativo", "Entusiasta", "Persuasivo", "Sociável"],
              "medio": ["Expressivo", "Otimista", "Engajador"],
              "baixo": ["Reservado", "Reflexivo", "Seletivo"]},
        "S": {"alto": ["Estável", "Paciente", "Confiável", "Cooperativo"],
              "medio": ["Consistente", "Leal", "Acolhedor"],
              "baixo": ["Dinâmico", "Adaptável", "Ágil"]},
        "C": {"alto": ["Analítico", "Preciso", "Sistemático", "Criterioso"],
              "medio": ["Metódico", "Organizado", "Detalhista"],
              "baixo": ["Flexível", "Intuitivo", "Pragmático"]},
    }
    content = (
        "// Gerado automaticamente por scripts/extract_knowledge.py\n"
        f"const PALAVRAS_PDF = {json.dumps(palavras, ensure_ascii=False, indent=2)};\n"
        f"const PALAVRAS_FALLBACK = {json.dumps(fallback, ensure_ascii=False, indent=2)};\n"
    )
    out_path.write_text(content, encoding="utf-8")
    print(f"✓ Gerado {out_path}")


if __name__ == "__main__":
    main()
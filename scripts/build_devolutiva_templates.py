"""
Constrói base robusta de devolutivas a partir dos 66 relatórios Thomas (MODELOS).
Gera devolutiva-templates.js consumido pelo frontend.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MAPPED_PATH = BASE / "artifacts" / "mapped_knowledge.json"
OUT_JS = BASE / "src" / "js" / "devolutiva-templates.js"
OUT_JSON = BASE / "artifacts" / "devolutiva_templates.json"

FACTOR_KEYWORDS = {
    "D": {"assertivo", "decisivo", "direto", "competitivo", "dominante", "determinado",
          "ambicioso", "corajoso", "firme", "persistente", "dinâmico", "inquieto",
          "impaciente", "desafiador", "independente", "obstinado", "agressivo"},
    "I": {"comunicativo", "entusiasta", "persuasivo", "sociável", "otimista", "expressivo",
          "carismático", "amigável", "expansivo", "diplomático", "inspirador", "criativo",
          "motivador", "popular", "animado", "espontâneo", "influente", "verbal", "gregário"},
    "S": {"paciente", "estável", "cooperativo", "leal", "confiável", "previsível",
          "consistente", "calmo", "tranquilo", "modesto", "gentil", "amável",
          "tolerante", "ponderado", "reservado", "sincero", "constante", "metódico",
          "cauteloso", "hesitante", "persistente", "relaxado", "uniforme"},
    "C": {"preciso", "analítico", "sistemático", "criterioso", "meticuloso", "lógico",
          "perfeccionista", "cético", "desconfiado", "inquisitivo", "exato", "cuidadoso",
          "disciplinado", "controlado", "reflexivo", "sério", "factual", "especialista",
          "técnico", "detalhista", "rigoroso", "formal", "conservador", "investigador"},
}

FOOTER = re.compile(r"©Thomas International.*", re.DOTALL | re.IGNORECASE)
PAGE_NUM = re.compile(r"\n\d+\n\n", re.MULTILINE)
DISCLAIMER = re.compile(
    r"Não deixe de observar.*?(?:Privado e Confidencial|\Z)",
    re.DOTALL | re.IGNORECASE,
)


def clean(text: str) -> str:
    if not text:
        return ""
    text = FOOTER.sub("", text)
    text = DISCLAIMER.sub("", text)
    text = PAGE_NUM.sub("\n\n", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()
    if text.endswith(" Um"):
        text = text[:-3].strip()
    return text


def parse_palavras(text: str) -> list[str]:
    text = re.sub(r'pergunta\s+"[^"]*"', "", text, flags=re.I)
    text = text.replace("\n", " ")
    parts = re.split(r"[,;]\s*|\s+e\s+", text)
    return [p.strip().strip(".").lower() for p in parts if 2 < len(p.strip()) < 40]


def classify_factor(words: list[str]) -> str:
    scores = {f: 0 for f in "DISC"}
    for w in words:
        for f, kws in FACTOR_KEYWORDS.items():
            if w in kws or any(k in w for k in kws):
                scores[f] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "C"


def extract_bullets(text: str) -> list[str]:
    items = re.findall(r"[•·]\s*(.+?)(?=\n[•·]|\n\n|\Z)", text, re.DOTALL)
    if not items:
        items = re.findall(r"^[-–]\s*(.+)$", text, re.MULTILINE)
    result = []
    for item in items:
        c = clean(item)
        if len(c) > 15 and not c.startswith("Prefere a segurança"):
            result.append(c)
    return result


def extract_estimulos(text: str) -> str:
    m = re.search(r"Estímulos\s*\n+(.+?)(?:\n\nNão deixe|\Z)", text, re.DOTALL | re.I)
    return clean(m.group(1)) if m else ""


def extract_enfase_title_body(text: str) -> dict:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return {"titulo": "", "corpo": ""}
    titulo = lines[0]
    corpo = clean("\n".join(lines[1:]))
    return {"titulo": titulo, "corpo": corpo}


def extract_discrepancia_patterns(docs: list) -> dict:
    patterns = {
        "alinhado": [],
        "suprimindo": [],
        "amplificando": [],
        "modificando": [],
    }
    for doc in docs:
        t = doc["sections"].get("percepcao_adaptada", "")
        t_lower = t.lower()
        c = clean(t)
        if len(c) < 40:
            continue
        if any(k in t_lower for k in ("não há necessidade", "compatível", "semelhante", "não vê nenhuma necessidade")):
            patterns["alinhado"].append(c[:600])
        elif any(k in t_lower for k in ("suprimindo", "repressão", "perda de confiança")):
            patterns["suprimindo"].append(c[:600])
        elif any(k in t_lower for k in ("enfatiza", "aumenta", "amplifica", "tornando-se ainda mais")):
            patterns["amplificando"].append(c[:600])
        elif any(k in t_lower for k in ("modifica", "modificando", "acelerando", "mais ativa")):
            patterns["modificando"].append(c[:600])
    return {k: v[:12] for k, v in patterns.items()}


def build_templates(mapped: dict) -> dict:
    docs = mapped.get("documents", [])
    by_factor: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    blend_samples: dict[str, list] = defaultdict(list)

    for doc in docs:
        sections = doc.get("sections", {})
        palavras = parse_palavras(sections.get("palavras_descritivas_natural", ""))
        factor = classify_factor(palavras)

        for key in ("auto_imagem_natural", "auto_motivacao", "enfase_trabalho",
                    "sob_pressao", "valor_organizacao", "motivadores"):
            if key in sections:
                c = clean(sections[key])
                if len(c) > 50:
                    by_factor[factor][key].append(c[:1500])

        if "caracteristicas_gerais" in sections:
            bullets = extract_bullets(sections["caracteristicas_gerais"])
            if bullets:
                by_factor[factor]["caracteristicas_gerais"].extend(bullets[:8])

        if "comentarios_gerais" in sections:
            est = extract_estimulos(sections["comentarios_gerais"])
            if est:
                by_factor[factor]["estimulos"].append(est[:800])

        if "palavras_descritivas_natural" in sections:
            words = [w.capitalize() for w in palavras if not w.startswith("não ")][:15]
            if words:
                by_factor[factor]["palavras"].append(words)

    factor_templates = {}
    for f in "DISC":
        data = by_factor.get(f, {})
        factor_templates[f] = {
            "auto_imagem": data.get("auto_imagem_natural", [])[:8],
            "auto_motivacao": data.get("auto_motivacao", [])[:8],
            "enfase_trabalho": [extract_enfase_title_body(t) for t in data.get("enfase_trabalho", [])[:8]],
            "caracteristicas": list(dict.fromkeys(data.get("caracteristicas_gerais", [])))[:12],
            "sob_pressao": data.get("sob_pressao", [])[:8],
            "valor_organizacao": data.get("valor_organizacao", [])[:6],
            "estimulos": data.get("estimulos", [])[:6],
            "motivadores": data.get("motivadores", [])[:6],
            "palavras": data.get("palavras", [])[:6],
        }

    blend_narratives = {
        "D": "Perfil orientado a resultados, com energia para superar obstáculos e tomar decisões.",
        "I": "Perfil comunicativo e influente, que energiza grupos e constrói conexões.",
        "S": "Perfil estável e cooperativo, que traz consistência e harmonia às equipes.",
        "C": "Perfil analítico e criterioso, orientado a qualidade, precisão e padrões.",
        "DI": "Combina determinação com capacidade de influenciar e mobilizar pessoas em direção a metas.",
        "ID": "Combina entusiasmo comunicativo com foco em resultados tangíveis.",
        "DS": "Combina iniciativa e firmeza com paciência e consistência na execução.",
        "SD": "Combina estabilidade e lealdade com capacidade de ação quando necessário.",
        "DC": "Combina orientação a resultados com rigor analítico e atenção a padrões.",
        "CD": "Combina precisão técnica com foco em entregas e metas mensuráveis.",
        "IS": "Combina sociabilidade com paciência, criando ambientes acolhedores e produtivos.",
        "SI": "Combina estabilidade relacional com abertura e comunicação calorosa.",
        "IC": "Combina expressividade com análise cuidadosa na comunicação de ideias.",
        "CI": "Combina rigor técnico com habilidade de transmitir informações de forma clara.",
        "SC": "Combina consistência operacional com atenção meticulosa a detalhes.",
        "CS": "Combina precisão analítica com abordagem paciente e metódica.",
    }

    return {
        "meta": {
            "source_documents": len(docs),
            "version": "2.1.0",
            "sections_per_factor": {f: sum(len(v) for v in factor_templates[f].values()) for f in "DISC"},
        },
        "fatores": factor_templates,
        "blends": blend_narratives,
        "discrepancia": extract_discrepancia_patterns(docs),
        "estrutura_relatorio": [
            {"id": "sumario", "titulo": "Sumário do Perfil", "grafico": True},
            {"id": "auto_imagem", "titulo": "Autoimagem — Gráfico III", "fonte": "auto_imagem"},
            {"id": "palavras", "titulo": "Palavras Descritivas", "fonte": "palavras"},
            {"id": "auto_motivacao", "titulo": "Auto Motivação", "fonte": "auto_motivacao"},
            {"id": "enfase", "titulo": "Ênfase no Trabalho", "fonte": "enfase_trabalho"},
            {"id": "caracteristicas", "titulo": "Características Gerais", "fonte": "caracteristicas"},
            {"id": "percepcao", "titulo": "Percepção no Ambiente Profissional — Gráfico I", "fonte": "adaptado"},
            {"id": "pressao", "titulo": "Comportamento sob Pressão — Gráfico II", "fonte": "sob_pressao"},
            {"id": "estimulos", "titulo": "Estímulos e Orientações ao Gestor", "fonte": "estimulos"},
            {"id": "valor", "titulo": "Valor para a Organização", "fonte": "valor_organizacao"},
            {"id": "discrepancia", "titulo": "Análise de Discrepância", "fonte": "discrepancia"},
            {"id": "zona", "titulo": "Indicadores de Zona Cinzenta", "fonte": "zona"},
        ],
    }


def write_js(templates: dict, path: Path) -> None:
    content = (
        "// Gerado por scripts/build_devolutiva_templates.py — base: 66 relatórios Thomas\n"
        f"const DEVOLUTIVA_TEMPLATES = {json.dumps(templates, ensure_ascii=False, indent=2)};\n"
    )
    path.write_text(content, encoding="utf-8")


def main():
    with open(MAPPED_PATH, encoding="utf-8") as f:
        mapped = json.load(f)

    templates = build_templates(mapped)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")
    write_js(templates, OUT_JS)

    print(f"✓ {OUT_JSON} ({OUT_JSON.stat().st_size // 1024} KB)")
    print(f"✓ {OUT_JS} ({OUT_JS.stat().st_size // 1024} KB)")
    for f in "DISC":
        n = templates["meta"]["sections_per_factor"][f]
        print(f"  Fator {f}: {n} entradas de template")


if __name__ == "__main__":
    main()
"""
Gera TESTEDISC/artifacts/rules.yaml a partir de artifacts/mapped_knowledge.json.
Escala unificada -10 a +10 (sem D>15).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
MAPPED_PATH = BASE_DIR / "artifacts" / "mapped_knowledge.json"
OUTPUT_PATH = BASE_DIR / "artifacts" / "rules.yaml"

FACTORS = ("D", "I", "S", "C")
FACTOR_NAMES = {
    "D": "Dominância",
    "I": "Influência",
    "S": "Estabilidade",
    "C": "Conformidade",
}

BLEND_INTERPRETATIONS = {
    "DI": "Perfil orientado a resultados com forte capacidade de influência — combina ação direta com persuasão.",
    "ID": "Perfil comunicativo com direcionamento a metas — usa relacionamentos para acelerar entregas.",
    "DS": "Perfil determinado com base estável — persiste com ritmo consistente em direção a objetivos.",
    "SD": "Perfil estável com capacidade de ação — mantém constância sem abrir mão de iniciativa.",
    "DC": "Perfil lógico e orientado a resultados — une assertividade com rigor analítico.",
    "CD": "Perfil analítico com foco em performance — prioriza qualidade orientada a metas.",
    "IS": "Perfil sociável e acolhedor — comunica com empatia e constrói harmonia.",
    "SI": "Perfil cooperativo com influência moderada — estabiliza equipes com conexão humana.",
    "SC": "Perfil consistente e criterioso — valoriza padrões com abordagem paciente.",
    "CS": "Perfil metódico e confiável — aplica critério técnico com constância.",
    "IC": "Perfil comunicativo e analítico — articula ideias com fundamentação lógica.",
    "CI": "Perfil técnico com habilidade relacional — traduz dados em mensagens compreensíveis.",
}

SUPPRESSION_KEYWORDS = {
    "D": ("dominância", "dominancia", "assertiv", "impositiv", "iniciativa", "suprimindo"),
    "I": ("influência", "influencia", "comunicativ", "amistoso", "persuasiv", "verbal"),
    "S": ("estabilidade", "constante", "metódico", "meticuloso", "paciente", "confiável"),
    "C": ("conformidade", "sistemátic", "precis", "lógic", "perfeccion", "criterios"),
}


def load_mapped() -> dict:
    with open(MAPPED_PATH, encoding="utf-8") as f:
        return json.load(f)


def find_evidence(documents: list[dict], keywords: tuple[str, ...], limit: int = 3) -> list[str]:
    hits: list[str] = []
    for doc in documents:
        text = " ".join(doc.get("sections", {}).values()).lower()
        if any(kw in text for kw in keywords):
            hits.append(doc.get("file") or doc.get("name", "unknown"))
        if len(hits) >= limit:
            break
    if not hits:
        hits = [documents[i % len(documents)]["file"] for i in range(min(limit, len(documents)))]
    return hits


def dominant_rule(factor: str, documents: list[dict]) -> dict:
    others = [f for f in FACTORS if f != factor]
    when = [f"{factor}_natural > 5"] + [f"{o}_natural <= 2" for o in others]
    return {
        "id": f"RULE_DOM_{factor}",
        "category": "blend",
        "when": when,
        "interpretation": (
            f"Perfil com {FACTOR_NAMES[factor]} elevada no natural — "
            f"traço dominante com pouca interferência dos demais fatores."
        ),
        "confidence": 0.88,
        "evidence": find_evidence(documents, SUPPRESSION_KEYWORDS[factor]),
    }


def blend_rule(blend: str, documents: list[dict]) -> dict:
    f1, f2 = blend[0], blend[1]
    others = [f for f in FACTORS if f not in (f1, f2)]
    when = [
        f"{f1}_natural > 3",
        f"{f2}_natural > 3",
        f"{f1}_natural >= {f2}_natural - 2",
    ] + [f"{o}_natural <= 2" for o in others]
    return {
        "id": f"RULE_BLEND_{blend}",
        "category": "blend",
        "when": when,
        "interpretation": BLEND_INTERPRETATIONS[blend],
        "confidence": 0.84,
        "evidence": find_evidence(
            documents,
            SUPPRESSION_KEYWORDS[f1] + SUPPRESSION_KEYWORDS[f2],
        ),
    }


def suppression_rule(factor: str, documents: list[dict]) -> dict:
    return {
        "id": f"RULE_SUPPRESS_{factor}",
        "category": "discrepancia",
        "when": [
            f"{factor}_natural > 5",
            f"{factor}_adapted < {factor}_natural - 4",
        ],
        "interpretation": (
            f"Supressão de {FACTOR_NAMES[factor]} no ambiente de trabalho: o natural é significativamente "
            f"maior que o adaptado (diferença > 4). Pode indicar repressão, perda de autonomia ou "
            f"máscara comportamental sustentada."
        ),
        "confidence": 0.91,
        "evidence": find_evidence(
            documents,
            ("suprimindo", "repressão", "repressao", "modificando") + SUPPRESSION_KEYWORDS[factor],
        ),
    }


def amplification_rule(factor: str, documents: list[dict]) -> dict:
    return {
        "id": f"RULE_AMPLIFY_{factor}",
        "category": "discrepancia",
        "when": [
            f"{factor}_adapted > {factor}_natural + 4",
        ],
        "interpretation": (
            f"Amplificação de {FACTOR_NAMES[factor]} no trabalho: adaptado excede o natural em mais de 4 pontos. "
            f"Pessoa enfatiza este traço para atender demandas do cargo ou cultura organizacional."
        ),
        "confidence": 0.87,
        "evidence": find_evidence(
            documents,
            ("enfatiza", "aumenta", "modificando", "máscara", "mascara") + SUPPRESSION_KEYWORDS[factor],
        ),
    }


def gray_zone_high(factor: str, documents: list[dict]) -> dict:
    return {
        "id": f"RULE_GRAY_HIGH_{factor}",
        "category": "zona_cinzenta",
        "when": [f"{factor}_natural > 8"],
        "interpretation": (
            f"Zona cinzenta alta em {FACTOR_NAMES[factor]} (|score| > 8): traço extremamente pronunciado. "
            f"Grande força com risco de excesso — recomenda-se moderação consciente."
        ),
        "confidence": 0.86,
        "evidence": find_evidence(documents, SUPPRESSION_KEYWORDS[factor]),
    }


def gray_zone_low(factor: str, documents: list[dict]) -> dict:
    return {
        "id": f"RULE_GRAY_LOW_{factor}",
        "category": "zona_cinzenta",
        "when": [f"{factor}_natural < -8"],
        "interpretation": (
            f"Zona cinzenta baixa em {FACTOR_NAMES[factor]} (|score| > 8): rejeição forte deste estilo. "
            f"Pode gerar tensão quando o ambiente exige este comportamento."
        ),
        "confidence": 0.83,
        "evidence": find_evidence(documents, SUPPRESSION_KEYWORDS[factor]),
    }


def harmony_rule(documents: list[dict]) -> dict:
    return {
        "id": "RULE_HARMONY",
        "category": "discrepancia",
        "when": [
            "D_diff >= -2",
            "D_diff <= 2",
            "I_diff >= -2",
            "I_diff <= 2",
            "S_diff >= -2",
            "S_diff <= 2",
            "C_diff >= -2",
            "C_diff <= 2",
        ],
        "interpretation": (
            "Alinhamento natural-adaptado: discrepância ≤ 2 em todos os fatores. "
            "Comportamento no trabalho compatível com a auto-imagem."
        ),
        "confidence": 0.80,
        "evidence": find_evidence(documents, ("compatível", "semelhante", "não há necessidade de mudar", "harmonia")),
    }


def extra_rules(documents: list[dict]) -> list[dict]:
    """Regras adicionais para combinações e padrões específicos."""
    rules = [
        {
            "id": "RULE_DC_EQUALIZED",
            "category": "combinacao",
            "when": ["D_natural > 3", "C_natural > 3", "D_diff >= -2", "D_diff <= 2", "C_diff >= -2", "C_diff <= 2"],
            "interpretation": (
                "Dominância e Conformidade niveladas: perfil analítico-decisivo. "
                "Pode indicar indecisão sob pressão quando ambos fatores competem."
            ),
            "confidence": 0.82,
            "evidence": find_evidence(documents, ("equaliz", "nivelam", "indecis")),
        },
        {
            "id": "RULE_IS_SUPPORT",
            "category": "combinacao",
            "when": ["I_natural > 4", "S_natural > 4", "D_natural <= 1"],
            "interpretation": "Perfil de suporte relacional: combina empatia com constância, ideal para papéis de acolhimento e mediação.",
            "confidence": 0.81,
            "evidence": find_evidence(documents, ("apoio", "equipe", "ouvinte", "harmonia")),
        },
        {
            "id": "RULE_SC_QUALITY",
            "category": "combinacao",
            "when": ["S_natural > 4", "C_natural > 4", "I_natural <= 1"],
            "interpretation": "Perfil de qualidade consistente: aplica padrões com paciência e método, forte em processos e auditoria.",
            "confidence": 0.83,
            "evidence": find_evidence(documents, ("qualidade", "padrões", "meticuloso", "procedimentos")),
        },
        {
            "id": "RULE_DI_SALES",
            "category": "combinacao",
            "when": ["D_natural > 4", "I_natural > 4", "C_natural <= 0"],
            "interpretation": "Perfil comercial assertivo: combina direcionamento a metas com persuasão interpessoal.",
            "confidence": 0.85,
            "evidence": find_evidence(documents, ("persuas", "resultados", "influenciar", "venda")),
        },
        {
            "id": "RULE_CS_TECHNICAL",
            "category": "combinacao",
            "when": ["C_natural > 5", "S_natural > 2", "I_natural <= 0"],
            "interpretation": "Perfil técnico-especialista: prefere profundidade analítica com ritmo estável e baixa exposição social.",
            "confidence": 0.84,
            "evidence": find_evidence(documents, ("especialista", "técnico", "analítico", "detalhes")),
        },
        {
            "id": "RULE_D_STRESS_UP",
            "category": "pressao",
            "when": ["D_adapted > D_natural + 2", "D_natural > 0"],
            "interpretation": "Sob demanda do cargo, aumenta dominância adaptada — pode melhorar desempenho com pressão moderada.",
            "confidence": 0.78,
            "evidence": find_evidence(documents, ("aumenta seu fator de dominância", "pressão", "enfatiza")),
        },
        {
            "id": "RULE_I_STRESS_DOWN",
            "category": "pressao",
            "when": ["I_adapted < I_natural - 3", "I_natural > 3"],
            "interpretation": "Influência natural suprimida sob pressão: risco de retração social e queda de motivação interpessoal.",
            "confidence": 0.79,
            "evidence": find_evidence(documents, ("retrair", "reservad", "pressão extrema", "pessimista")),
        },
        {
            "id": "RULE_BALANCED",
            "category": "blend",
            "when": [
                "D_natural >= -2", "D_natural <= 2",
                "I_natural >= -2", "I_natural <= 2",
                "S_natural >= -2", "S_natural <= 2",
                "C_natural >= -2", "C_natural <= 2",
            ],
            "interpretation": "Perfil equilibrado: scores próximos de zero em todos os fatores — flexibilidade comportamental ampla.",
            "confidence": 0.75,
            "evidence": find_evidence(documents, ("adaptável", "moderado", "equilibrad")),
        },
        {
            "id": "RULE_TRIPLE_DIS",
            "category": "combinacao",
            "when": ["D_natural > 3", "I_natural > 2", "S_natural > 2", "C_natural <= 0"],
            "interpretation": "Blend DIS: líder operacional com energia, influência moderada e base estável.",
            "confidence": 0.80,
            "evidence": find_evidence(documents, ("lider", "equipe", "resultados")),
        },
        {
            "id": "RULE_TRIPLE_ICD",
            "category": "combinacao",
            "when": ["I_natural > 2", "C_natural > 3", "D_natural > 2", "S_natural <= 0"],
            "interpretation": "Blend ICD: comunicador analítico com orientação a entregas e baixa necessidade de rotina.",
            "confidence": 0.79,
            "evidence": find_evidence(documents, ("comunic", "lógico", "especialista")),
        },
    ]

    for factor in FACTORS:
        rules.append({
            "id": f"RULE_MEDIUM_{factor}",
            "category": "intensidade",
            "when": [
                f"{factor}_natural > 2",
                f"{factor}_natural <= 5",
            ],
            "interpretation": (
                f"{FACTOR_NAMES[factor]} em intensidade média-alta: traço presente sem dominar o perfil."
            ),
            "confidence": 0.72,
            "evidence": find_evidence(documents, SUPPRESSION_KEYWORDS[factor], limit=2),
        })
        rules.append({
            "id": f"RULE_LOW_{factor}",
            "category": "intensidade",
            "when": [
                f"{factor}_natural < -3",
                f"{factor}_natural > -8",
            ],
            "interpretation": (
                f"{FACTOR_NAMES[factor]} rejeitado moderadamente: evita comportamentos associados a este fator."
            ),
            "confidence": 0.71,
            "evidence": find_evidence(documents, SUPPRESSION_KEYWORDS[factor], limit=2),
        })

    rules.extend([
        {
            "id": "RULE_ADAPT_MASK_HIGH_C",
            "category": "discrepancia",
            "when": ["C_natural > 0", "C_adapted > C_natural + 3", "C_adapted > 6"],
            "interpretation": "Máscara de conformidade no trabalho: adaptado significativamente mais criterioso que o natural.",
            "confidence": 0.80,
            "evidence": find_evidence(documents, ("conformidade", "sistemátic", "enfatiza")),
        },
        {
            "id": "RULE_ADAPT_MASK_HIGH_I",
            "category": "discrepancia",
            "when": ["I_natural < 2", "I_adapted > 5"],
            "interpretation": "Máscara social no trabalho: exibe mais influência adaptada do que o estilo natural sugere.",
            "confidence": 0.78,
            "evidence": find_evidence(documents, ("comunicativ", "amistoso", "influência")),
        },
        {
            "id": "RULE_CONFLICT_DS",
            "category": "combinacao",
            "when": ["D_natural > 5", "S_natural > 5"],
            "interpretation": "Tensão D-S: impulso por ação rápida convive com necessidade de estabilidade e ritmo constante.",
            "confidence": 0.77,
            "evidence": find_evidence(documents, ("determinad", "constante", "persistente")),
        },
        {
            "id": "RULE_CONFLICT_IC",
            "category": "combinacao",
            "when": ["I_natural > 5", "C_natural > 5"],
            "interpretation": "Tensão I-C: desejo de expressividade social com exigência de precisão e controle analítico.",
            "confidence": 0.76,
            "evidence": find_evidence(documents, ("comunic", "precis", "lógic")),
        },
    ])

    return rules


def generate_rules(mapped: dict) -> list[dict]:
    documents = mapped.get("documents", [])
    rules: list[dict] = []

    for factor in FACTORS:
        rules.append(dominant_rule(factor, documents))

    for blend in BLEND_INTERPRETATIONS:
        rules.append(blend_rule(blend, documents))

    for factor in FACTORS:
        rules.append(suppression_rule(factor, documents))
        rules.append(amplification_rule(factor, documents))
        rules.append(gray_zone_high(factor, documents))
        rules.append(gray_zone_low(factor, documents))

    rules.append(harmony_rule(documents))
    rules.extend(extra_rules(documents))

    seen_ids: set[str] = set()
    unique: list[dict] = []
    for rule in rules:
        if rule["id"] not in seen_ids:
            seen_ids.add(rule["id"])
            unique.append(rule)
    return unique


def write_rules(rules: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "---\n"
        "name: disc-rules\n"
        "description: Rule engine definitions for DISC interpretations (scale -10 to +10)\n"
        "version: 2.0.0\n"
        "scale:\n"
        "  min: -10\n"
        "  max: 10\n"
        "  gray_zone: 8\n"
        "  discrepancy_threshold: 4\n"
        "---\n"
    )
    body = yaml.dump(
        rules,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    path.write_text(header + body, encoding="utf-8")


def main() -> None:
    mapped = load_mapped()
    rules = generate_rules(mapped)
    write_rules(rules, OUTPUT_PATH)
    print(f"✓ {OUTPUT_PATH} — {len(rules)} regras")


if __name__ == "__main__":
    main()
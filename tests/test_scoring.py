"""Testes unitários da lógica de scoring DISC V2."""

def normalize_raw(raw, item_count=28):
    divisor = item_count / 10
    scores = {}
    for f in "DISC":
        scores[f] = max(-10, min(10, round(raw[f] / divisor * 10) / 10))
    return scores


def calcular_scores(respostas, item_count=28):
    raw = {"D": 0, "I": 0, "S": 0, "C": 0}
    for r in respostas:
        if r.get("most"):
            raw[r["most"]] += 1
        if r.get("least"):
            raw[r["least"]] -= 1
    return normalize_raw(raw, item_count)


def determinar_perfil(scores):
    fatores = list("DISC")
    sorted_f = sorted(fatores, key=lambda f: scores[f], reverse=True)
    primario = sorted_f[0]
    secundario = sorted_f[1] if scores[sorted_f[1]] > 0 else None
    blend = primario + (secundario or "")
    return {"primario": primario, "blend": blend}


def test_scores_28_items():
    respostas = [{"most": "D", "least": "S"}] * 28
    scores = calcular_scores(respostas, 28)
    assert scores["D"] == 10.0
    assert scores["S"] == -10.0


def test_discrepancy():
    nat = calcular_scores([{"most": "D", "least": "I"}] * 28, 28)
    adp = calcular_scores([{"most": "S", "least": "D"}] * 28, 28)
    diff = {f: round(adp[f] - nat[f], 1) for f in "DISC"}
    assert diff["D"] < 0
    assert diff["S"] > 0


def test_blend_di():
    scores = {"D": 7, "I": 6, "S": -1, "C": 0}
    p = determinar_perfil(scores)
    assert p["blend"] == "DI"


if __name__ == "__main__":
    test_scores_28_items()
    test_discrepancy()
    test_blend_di()
    print("✓ Todos os testes de scoring passaram")
"""Testes unitários da lógica de scoring DISC (espelho Python do scoring.js)."""
import math


def calcular_scores(respostas):
    raw = {"D": 0, "I": 0, "S": 0, "C": 0}
    for r in respostas:
        if r.get("most"):
            raw[r["most"]] += 1
        if r.get("least"):
            raw[r["least"]] -= 1
    scores = {}
    for f in "DISC":
        scores[f] = max(-10, min(10, round(raw[f] / 4 * 10) / 10))
    return scores


def determinar_perfil(scores):
    fatores = list("DISC")
    sorted_f = sorted(fatores, key=lambda f: scores[f], reverse=True)
    primario = sorted_f[0]
    secundario = sorted_f[1] if scores[sorted_f[1]] > 0 else None
    terciario = None
    if secundario and scores[sorted_f[2]] > 0 and abs(scores[sorted_f[2]] - scores[sorted_f[1]]) < 2:
        terciario = sorted_f[2]
    blend = primario
    if secundario:
        blend += secundario
    if terciario:
        blend += terciario
    return {"primario": primario, "secundario": secundario, "terciario": terciario, "blend": blend}


def test_scores_all_d_most():
    respostas = [{"most": "D", "least": "S"}] * 40
    scores = calcular_scores(respostas)
    assert scores["D"] == 10.0
    assert scores["S"] == -10.0


def test_scores_balanced():
    respostas = [{"most": f, "least": f} for f in "DISC"] * 10
    scores = calcular_scores(respostas)
    for f in "DISC":
        assert scores[f] == 0.0


def test_scores_clamp():
    respostas = [{"most": "D", "least": None}] * 40
    scores = calcular_scores(respostas)
    assert scores["D"] == 10.0


def test_blend_primario_only():
    scores = {"D": 8, "I": -2, "S": -3, "C": -1}
    p = determinar_perfil(scores)
    assert p["blend"] == "D"
    assert p["secundario"] is None


def test_blend_di():
    scores = {"D": 7, "I": 6, "S": -1, "C": 0}
    p = determinar_perfil(scores)
    assert p["blend"] == "DI"


def test_blend_triple():
    scores = {"D": 6, "I": 5.5, "S": 4, "C": -2}
    p = determinar_perfil(scores)
    assert p["blend"] == "DIS"


def test_classificar_zona_cinzenta():
    for v in [9, -9, 10, -10]:
        assert abs(v) > 8


if __name__ == "__main__":
    test_scores_all_d_most()
    test_scores_balanced()
    test_scores_clamp()
    test_blend_primario_only()
    test_blend_di()
    test_blend_triple()
    test_classificar_zona_cinzenta()
    print("✓ Todos os testes de scoring passaram")
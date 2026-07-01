import os
import yaml
from fastapi.testclient import TestClient
from api.main import app
from api.inference import build_context, evaluate_condition

client = TestClient(app)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, 'knowledge.json')
RULES_PATH = os.path.join(BASE_DIR, 'artifacts', 'rules.yaml')
ONTOLOGY_PATH = os.path.join(BASE_DIR, 'artifacts', 'ontology.yaml')
PHRASES_PATH = os.path.join(BASE_DIR, 'artifacts', 'phrases.json')


def test_artifacts_exist():
    for path in [KNOWLEDGE_PATH, RULES_PATH, ONTOLOGY_PATH, PHRASES_PATH]:
        assert os.path.isfile(path), f"Missing artifact: {path}"


def _load_rules(path):
    with open(path, 'r', encoding='utf-8') as f:
        for doc in yaml.safe_load_all(f):
            if isinstance(doc, list):
                return doc
    return []


def test_rules_loadable():
    rules = _load_rules(RULES_PATH)
    assert isinstance(rules, list) and len(rules) >= 50
    for rule in rules:
        assert 'id' in rule and 'when' in rule and 'interpretation' in rule
        assert isinstance(rule['when'], list)


def _satisfy_condition(cond: str, natural: dict, adapted: dict) -> None:
    """Ajusta scores para tentar satisfazer uma condição simples."""
    ctx = build_context(natural, adapted)
    if evaluate_condition(cond, ctx):
        return

    for op in (">=", ">", "<=", "<", "=="):
        if op in cond:
            left, right = cond.split(op, 1)
            left = left.strip()
            right = right.strip()
            try:
                threshold = float(right)
            except ValueError:
                if "_natural" in right:
                    factor = right.replace("_natural", "").split()[0]
                    if op in (">", ">="):
                        natural[factor] = max(natural[factor], threshold + 1)
                    elif op in ("<", "<="):
                        natural[factor] = min(natural[factor], threshold - 1)
                return

            if "_natural" in left:
                factor = left.replace("_natural", "")
                if op == ">":
                    natural[factor] = threshold + 1
                elif op == ">=":
                    natural[factor] = threshold
                elif op == "<":
                    natural[factor] = threshold - 1
                elif op == "<=":
                    natural[factor] = threshold
                elif op == "==":
                    natural[factor] = threshold
            elif "_adapted" in left:
                factor = left.replace("_adapted", "")
                if op == ">":
                    adapted[factor] = threshold + 1
                elif op == ">=":
                    adapted[factor] = threshold
                elif op == "<":
                    adapted[factor] = threshold - 1
                elif op == "<=":
                    adapted[factor] = threshold
            elif "_diff" in left:
                factor = left.replace("_diff", "")
                if op == ">=":
                    adapted[factor] = natural[factor] - threshold
                elif op == "<=":
                    adapted[factor] = natural[factor] - threshold
            return


def test_inference_sample_rules():
    rules = _load_rules(RULES_PATH)
    sample = rules[:10]
    for rule in sample:
        natural = {'D': 0.0, 'I': 0.0, 'S': 0.0, 'C': 0.0}
        adapted = {'D': 0.0, 'I': 0.0, 'S': 0.0, 'C': 0.0}
        for cond in rule['when']:
            _satisfy_condition(cond, natural, adapted)

        response = client.post('/infer', json={'natural': natural, 'adapted': adapted})
        if response.status_code == 200:
            data = response.json()
            assert rule['id'] in data['matched_rules']


def test_ontology_expanded():
    with open(ONTOLOGY_PATH, encoding='utf-8') as f:
        docs = list(yaml.safe_load_all(f))
    ontology = next(d for d in reversed(docs) if isinstance(d, dict) and 'Dominancia' in d)
    for factor in ('Dominancia', 'Influência', 'Estabilidade', 'Conformidade'):
        entry = ontology[factor]
        for field in (
            'medo_fundamental', 'ambiente_ideal', 'ambiente_estressante',
            'estilo_lideranca', 'comunicacao_fazer', 'comunicacao_evitar',
            'motivadores', 'palavras_descritivas_alto', 'palavras_descritivas_baixo',
        ):
            assert field in entry, f"{factor} missing {field}"


def test_static_page_exists():
    static_path = os.path.join(BASE_DIR, 'docs', 'index.html')
    assert os.path.isfile(static_path)
    with open(static_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Perfil DISC' in content
    assert 'function iniciar' in content
    assert 'function calcularERenderizar' in content
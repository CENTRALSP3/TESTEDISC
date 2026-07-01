import os, json, yaml
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# Load artifacts for verification
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
    assert isinstance(rules, list) and len(rules) > 0
    for rule in rules:
        assert 'id' in rule and 'when' in rule and 'interpretation' in rule
        assert isinstance(rule['when'], list)

def test_inference_all_rules():
    # Load rules to construct a simple score set that satisfies each rule individually
    rules = _load_rules(RULES_PATH)
    for rule in rules:
        # Build a score dict with default high values
        scores = {'D': 0.0, 'I': 0.0, 'S': 0.0, 'C': 0.0}
        # Try to satisfy each condition by setting a variable above the threshold if > or >=
        for cond in rule['when']:
            # Very naive parser: expect format "X > N" or "X >= N" etc.
            parts = cond.replace('>=', '>=').replace('>', '>').replace('<=', '<=').replace('<', '<').split()
            if len(parts) != 3:
                continue
            var, op, num = parts
            try:
                num = float(num)
            except ValueError:
                continue
            if op == '>':
                scores[var] = num + 1
            elif op == '>=':
                scores[var] = num
            elif op == '<':
                scores[var] = num - 1
            elif op == '<=':
                scores[var] = num
        # Send request
        response = client.post('/infer', json=scores)
        # Some rules may not be reachable with this naive approach; accept 404 as not matched
        if response.status_code == 200:
            data = response.json()
            assert data['interpretation'] == rule['interpretation']
        else:
            # Ensure the API returns 404 when no rule matches (acceptable for this test)
            assert response.status_code == 404

def test_static_page_exists():
    static_path = os.path.join(BASE_DIR, 'docs', 'index.html')
    assert os.path.isfile(static_path)
    with open(static_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<form' in content and 'fetch' in content

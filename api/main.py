import os, json, yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Determine the repository root (one level up from this file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Paths to knowledge artifacts
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge.json")
ONTOLOGY_PATH = os.path.join(BASE_DIR, "artifacts", "ontology.yaml")
RULES_PATH = os.path.join(BASE_DIR, "artifacts", "rules.yaml")
PHRASES_PATH = os.path.join(BASE_DIR, "artifacts", "phrases.json")

def load_yaml_rules(path: str) -> list:
    """Carrega rules.yaml suportando frontmatter YAML multi-documento."""
    with open(path, "r", encoding="utf-8") as f:
        for doc in yaml.safe_load_all(f):
            if isinstance(doc, list):
                return doc
    return []


def load_yaml_ontology(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        docs = list(yaml.safe_load_all(f))
    for doc in reversed(docs):
        if isinstance(doc, dict) and "Dominancia" in doc:
            return doc
    return docs[-1] if docs else {}


# Load data at startup (fails fast if missing)
with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)
ONTOLOGY = load_yaml_ontology(ONTOLOGY_PATH)
RULES = load_yaml_rules(RULES_PATH)
with open(PHRASES_PATH, "r", encoding="utf-8") as f:
    PHRASES = json.load(f)

app = FastAPI(title="DISC Inference API", version="1.0.0")

# Serve the UI page at the root URL
from fastapi.responses import FileResponse

@app.get("/", response_class=FileResponse)
def serve_ui():
    return FileResponse(os.path.join(BASE_DIR, "docs", "index.html"))

class Scores(BaseModel):
    D: float
    I: float
    S: float
    C: float

def condition_holds(condition: str, scores: Scores) -> bool:
    """Very small safe evaluator for simple numeric comparisons.
    Supports >, >=, <, <=, == with float literals.
    """
    # map variable names to actual numbers
    expr = condition.replace("D", str(scores.D))\
                     .replace("I", str(scores.I))\
                     .replace("S", str(scores.S))\
                     .replace("C", str(scores.C))
    try:
        return bool(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        return False

@app.post("/infer")
def infer(scores: Scores):
    matched = []
    for rule in RULES:
        when = rule.get("when", [])
        if all(condition_holds(cond, scores) for cond in when):
            matched.append(rule)
    if not matched:
        raise HTTPException(status_code=404, detail="No matching rule found")
    # Pick the rule with highest confidence
    best = max(matched, key=lambda r: r.get("confidence", 0))
    return {
        "profile": best.get("id", "UNKNOWN"),
        "interpretation": best.get("interpretation"),
        "confidence": best.get("confidence"),
        "evidence": best.get("evidence", []),
        "matched_rules": [r.get("id") for r in matched],
    }

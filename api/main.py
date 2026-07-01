"""
API FastAPI do TESTEDISC V2 — inferência segura, coleta anônima e resultados compartilhados.
"""
from __future__ import annotations

import json
import os
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.database import Database
from api.inference import FACTORS, infer_profile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge.json")
ONTOLOGY_PATH = os.path.join(BASE_DIR, "artifacts", "ontology.yaml")
RULES_PATH = os.path.join(BASE_DIR, "artifacts", "rules.yaml")
PHRASES_PATH = os.path.join(BASE_DIR, "artifacts", "phrases.json")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
INDEX_PATH = os.path.join(DOCS_DIR, "index.html")


def load_yaml_rules(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for doc in yaml.safe_load_all(f):
            if isinstance(doc, list):
                return doc
    return []


def load_yaml_ontology(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        docs = list(yaml.safe_load_all(f))
    for doc in reversed(docs):
        if isinstance(doc, dict) and "Dominancia" in doc:
            return doc
    return docs[-1] if docs else {}


with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)
ONTOLOGY = load_yaml_ontology(ONTOLOGY_PATH)
RULES = load_yaml_rules(RULES_PATH)
with open(PHRASES_PATH, "r", encoding="utf-8") as f:
    PHRASES = json.load(f)

db = Database()

app = FastAPI(title="DISC Inference API", version="2.0.0")


class FactorScores(BaseModel):
    D: float = Field(..., ge=-10, le=10)
    I: float = Field(..., ge=-10, le=10)
    S: float = Field(..., ge=-10, le=10)
    C: float = Field(..., ge=-10, le=10)


class InferRequest(BaseModel):
    natural: FactorScores
    adapted: FactorScores
    share: bool = False


class ResponseItem(BaseModel):
    session_id: str | None = None
    block: str | None = None
    question_id: str | None = None
    most_factor: str | None = None
    least_factor: str | None = None
    responses: list[dict[str, Any]] | None = None


@app.get("/", response_class=FileResponse)
def serve_ui():
    if not os.path.isfile(INDEX_PATH):
        raise HTTPException(status_code=404, detail="UI not found")
    return FileResponse(INDEX_PATH)


if os.path.isdir(DOCS_DIR):
    app.mount("/docs", StaticFiles(directory=DOCS_DIR), name="docs")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "rules_loaded": len(RULES),
        "ontology_factors": list(ONTOLOGY.keys()),
    }


@app.get("/ontology")
def get_ontology():
    return ONTOLOGY


@app.get("/rules/meta")
def rules_meta():
    return {"count": len(RULES), "ids": [r.get("id") for r in RULES]}


@app.post("/infer")
def infer(payload: InferRequest):
    natural = payload.natural.model_dump()
    adapted = payload.adapted.model_dump()

    result = infer_profile(RULES, natural, adapted)
    if not result.get("profile"):
        raise HTTPException(status_code=404, detail="No matching rule found")

    response = {
        "profile": result["profile"],
        "interpretation": result["interpretation"],
        "confidence": result["confidence"],
        "evidence": result.get("evidence", []),
        "matched_rules": result.get("matched_rules", []),
        "category": result.get("category"),
        "scores": {
            "natural": result["natural"],
            "adapted": result["adapted"],
            "diff": result["diff"],
        },
    }

    if payload.share:
        result_hash = db.save_shared_result(natural, adapted, inference=response)
        response["share_hash"] = result_hash
        response["share_url"] = f"/result/{result_hash}"

    return response


@app.post("/responses")
def collect_responses(payload: ResponseItem):
    saved_ids: list[int] = []

    if payload.responses:
        for item in payload.responses:
            row = {**item}
            if payload.session_id and "session_id" not in row:
                row["session_id"] = payload.session_id
            saved_ids.append(db.save_response(row))
    else:
        saved_ids.append(
            db.save_response({
                "session_id": payload.session_id,
                "block": payload.block,
                "question_id": payload.question_id,
                "most_factor": payload.most_factor,
                "least_factor": payload.least_factor,
            })
        )

    return {"saved": len(saved_ids), "ids": saved_ids}


@app.get("/analytics")
def analytics():
    return db.get_analytics()


@app.get("/result/{result_hash}")
def get_result(result_hash: str):
    row = db.get_shared_result(result_hash)
    if not row:
        raise HTTPException(status_code=404, detail="Result not found")
    return row
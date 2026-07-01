"""
Persistência SQLite para respostas anônimas e resultados compartilhados.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "data", "testedisc.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    session_id TEXT,
    block TEXT,
    question_id TEXT,
    most_factor TEXT,
    least_factor TEXT,
    payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shared_results (
    hash TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    natural_scores_json TEXT NOT NULL,
    adapted_scores_json TEXT NOT NULL,
    inference_json TEXT,
    payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_responses_created ON responses(created_at);
CREATE INDEX IF NOT EXISTS idx_responses_session ON responses(session_id);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA_SQL)

    def save_response(self, payload: dict[str, Any]) -> int:
        created_at = utc_now()
        session_id = payload.get("session_id")
        block = payload.get("block")
        question_id = payload.get("question_id")
        most_factor = payload.get("most_factor")
        least_factor = payload.get("least_factor")

        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO responses (
                    created_at, session_id, block, question_id,
                    most_factor, least_factor, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at,
                    session_id,
                    block,
                    question_id,
                    most_factor,
                    least_factor,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            return int(cur.lastrowid)

    def save_shared_result(
        self,
        natural: dict[str, float],
        adapted: dict[str, float],
        inference: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        result_hash: str | None = None,
    ) -> str:
        result_hash = result_hash or uuid4().hex[:16]
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO shared_results (
                    hash, created_at, natural_scores_json,
                    adapted_scores_json, inference_json, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    result_hash,
                    utc_now(),
                    json.dumps(natural, ensure_ascii=False),
                    json.dumps(adapted, ensure_ascii=False),
                    json.dumps(inference, ensure_ascii=False) if inference else None,
                    json.dumps(extra, ensure_ascii=False) if extra else None,
                ),
            )
        return result_hash

    def get_shared_result(self, result_hash: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM shared_results WHERE hash = ?",
                (result_hash,),
            ).fetchone()
        if not row:
            return None
        return {
            "hash": row["hash"],
            "created_at": row["created_at"],
            "natural": json.loads(row["natural_scores_json"]),
            "adapted": json.loads(row["adapted_scores_json"]),
            "inference": json.loads(row["inference_json"]) if row["inference_json"] else None,
            "payload": json.loads(row["payload_json"]) if row["payload_json"] else None,
        }

    def get_analytics(self) -> dict[str, Any]:
        with self._connect() as conn:
            total_responses = conn.execute("SELECT COUNT(*) FROM responses").fetchone()[0]
            total_shared = conn.execute("SELECT COUNT(*) FROM shared_results").fetchone()[0]
            sessions = conn.execute(
                "SELECT COUNT(DISTINCT session_id) FROM responses WHERE session_id IS NOT NULL"
            ).fetchone()[0]
            by_block = {
                row["block"] or "unknown": row["cnt"]
                for row in conn.execute(
                    "SELECT block, COUNT(*) AS cnt FROM responses GROUP BY block"
                ).fetchall()
            }
            by_factor = {
                "most": {},
                "least": {},
            }
            for row in conn.execute(
                "SELECT most_factor AS f, COUNT(*) AS cnt FROM responses "
                "WHERE most_factor IS NOT NULL GROUP BY most_factor"
            ).fetchall():
                by_factor["most"][row["f"]] = row["cnt"]
            for row in conn.execute(
                "SELECT least_factor AS f, COUNT(*) AS cnt FROM responses "
                "WHERE least_factor IS NOT NULL GROUP BY least_factor"
            ).fetchall():
                by_factor["least"][row["f"]] = row["cnt"]
            latest = conn.execute(
                "SELECT created_at FROM responses ORDER BY id DESC LIMIT 1"
            ).fetchone()

        return {
            "total_responses": total_responses,
            "total_shared_results": total_shared,
            "unique_sessions": sessions,
            "responses_by_block": by_block,
            "responses_by_factor": by_factor,
            "latest_response_at": latest[0] if latest else None,
        }
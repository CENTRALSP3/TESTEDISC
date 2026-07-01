"""
Motor de inferência seguro para regras DISC.
Suporta variáveis D/I/S/C, natural/adapted/diff e operadores >, >=, <, <=, ==.
Não utiliza eval().
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Union

FACTORS = ("D", "I", "S", "C")

COMPARISON_OPS = (">=", "<=", "==", ">", "<")

TOKEN_RE = re.compile(
    r"(?P<NUM>-?\d+(?:\.\d+)?)"
    r"|(?P<VAR>D_natural|I_natural|S_natural|C_natural"
    r"|D_adapted|I_adapted|S_adapted|C_adapted"
    r"|D_diff|I_diff|S_diff|C_diff"
    r"|[DISC])"
    r"|(?P<OP>[+\-])"
    r"|(?P<SKIP>\s+)"
)

Expr = Union["NumExpr", "VarExpr", "BinExpr"]


class ParseError(ValueError):
    """Erro de parsing de condição."""


@dataclass(frozen=True)
class NumExpr:
    value: float


@dataclass(frozen=True)
class VarExpr:
    name: str


@dataclass(frozen=True)
class BinExpr:
    left: Expr
    op: str
    right: Expr


def build_context(natural: dict[str, float], adapted: dict[str, float]) -> dict[str, float]:
    """Monta contexto de variáveis a partir dos scores natural e adaptado."""
    ctx: dict[str, float] = {}
    for f in FACTORS:
        n = float(natural[f])
        a = float(adapted[f])
        ctx[f"{f}_natural"] = n
        ctx[f"{f}_adapted"] = a
        ctx[f"{f}_diff"] = n - a
        ctx[f] = n
    return ctx


def tokenize(expression: str) -> list[tuple[str, str]]:
    pos = 0
    tokens: list[tuple[str, str]] = []
    while pos < len(expression):
        match = TOKEN_RE.match(expression, pos)
        if not match:
            raise ParseError(f"Token inválido em: {expression[pos:pos + 20]!r}")
        if match.lastgroup != "SKIP":
            kind = "NUM" if match.group("NUM") else "VAR" if match.group("VAR") else "OP"
            tokens.append((kind, match.group(kind)))
        pos = match.end()
    return tokens


def _parse_term(tokens: list[tuple[str, str]], idx: int) -> tuple[Expr, int]:
    if idx >= len(tokens):
        raise ParseError("Expressão incompleta")

    kind, value = tokens[idx]
    if kind == "NUM":
        node: Expr = NumExpr(float(value))
        idx += 1
    elif kind == "VAR":
        node = VarExpr(value)
        idx += 1
    else:
        raise ParseError(f"Termo inválido: {value}")

    while idx < len(tokens) and tokens[idx][0] == "OP":
        op = tokens[idx][1]
        idx += 1
        right_kind, right_val = tokens[idx]
        if right_kind == "NUM":
            right: Expr = NumExpr(float(right_val))
        elif right_kind == "VAR":
            right = VarExpr(right_val)
        else:
            raise ParseError(f"Operando inválido após {op}")
        node = BinExpr(node, op, right)
        idx += 1

    return node, idx


def parse_expression(expression: str) -> Expr:
    """Parseia expressão aritmética simples (+/-)."""
    tokens = tokenize(expression.strip())
    if not tokens:
        raise ParseError("Expressão vazia")
    result, idx = _parse_term(tokens, 0)
    if idx != len(tokens):
        raise ParseError(f"Tokens extras na expressão: {expression!r}")
    return result


def evaluate_expression(expr: Expr, context: dict[str, float]) -> float:
    if isinstance(expr, NumExpr):
        return expr.value
    if isinstance(expr, VarExpr):
        if expr.name not in context:
            raise ParseError(f"Variável desconhecida: {expr.name}")
        return float(context[expr.name])
    left = evaluate_expression(expr.left, context)
    right = evaluate_expression(expr.right, context)
    if expr.op == "+":
        return left + right
    if expr.op == "-":
        return left - right
    raise ParseError(f"Operador aritmético inválido: {expr.op}")


def split_comparison(condition: str) -> tuple[str, str, str]:
    """Divide condição em (esquerda, operador, direita)."""
    for op in COMPARISON_OPS:
        idx = condition.find(op)
        if idx == -1:
            continue
        left = condition[:idx].strip()
        right = condition[idx + len(op):].strip()
        if left and right:
            return left, op, right
    raise ParseError(f"Comparação inválida: {condition!r}")


def evaluate_condition(condition: str, context: dict[str, float]) -> bool:
    """Avalia uma condição contra o contexto de scores."""
    left_expr, op, right_expr = split_comparison(condition.strip())
    left_val = evaluate_expression(parse_expression(left_expr), context)
    right_val = evaluate_expression(parse_expression(right_expr), context)

    if op == ">":
        return left_val > right_val
    if op == ">=":
        return left_val >= right_val
    if op == "<":
        return left_val < right_val
    if op == "<=":
        return left_val <= right_val
    if op == "==":
        return left_val == right_val
    raise ParseError(f"Operador desconhecido: {op}")


def rule_matches(rule: dict[str, Any], context: dict[str, float]) -> bool:
    """Retorna True se todas as condições da regra forem satisfeitas."""
    conditions = rule.get("when", [])
    if not isinstance(conditions, list):
        return False
    try:
        return all(evaluate_condition(cond, context) for cond in conditions)
    except (ParseError, KeyError, TypeError):
        return False


def infer_profile(
    rules: list[dict[str, Any]],
    natural: dict[str, float],
    adapted: dict[str, float],
) -> dict[str, Any]:
    """Executa inferência e retorna perfil, regras correspondentes e contexto."""
    context = build_context(natural, adapted)
    matched = [r for r in rules if rule_matches(r, context)]

    result: dict[str, Any] = {
        "natural": {f: context[f"{f}_natural"] for f in FACTORS},
        "adapted": {f: context[f"{f}_adapted"] for f in FACTORS},
        "diff": {f: context[f"{f}_diff"] for f in FACTORS},
        "matched_rules": [r.get("id", "UNKNOWN") for r in matched],
        "matched_count": len(matched),
    }

    if not matched:
        result.update({
            "profile": None,
            "interpretation": None,
            "confidence": 0.0,
            "evidence": [],
        })
        return result

    best = max(matched, key=lambda r: float(r.get("confidence", 0)))
    result.update({
        "profile": best.get("id", "UNKNOWN"),
        "interpretation": best.get("interpretation"),
        "confidence": float(best.get("confidence", 0)),
        "evidence": best.get("evidence", []),
        "category": best.get("category"),
    })
    return result
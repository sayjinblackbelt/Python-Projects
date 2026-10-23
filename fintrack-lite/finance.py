"""Funções de domínio para o FinTrack Lite."""
from __future__ import annotations

import pandas as pd

COLUMNS = ["date", "type", "description", "category", "amount", "payment_method"]
VALID_TYPES = {"Receita", "Despesa"}


def normalize_transactions(data: pd.DataFrame) -> pd.DataFrame:
    """Valida e normaliza os campos principais de uma tabela de transações."""
    missing = set(COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}")

    result = data[COLUMNS].copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    result["type"] = result["type"].astype(str).str.strip()
    result["description"] = result["description"].fillna("").astype(str).str.strip()
    result["category"] = result["category"].fillna("Sem categoria").astype(str).str.strip()
    result["payment_method"] = result["payment_method"].fillna("Não informado").astype(str).str.strip()
    result["amount"] = pd.to_numeric(result["amount"], errors="coerce")

    if result["date"].isna().any():
        raise ValueError("Existem datas inválidas.")
    if not result["type"].isin(VALID_TYPES).all():
        raise ValueError("O tipo deve ser Receita ou Despesa.")
    if result["description"].eq("").any():
        raise ValueError("A descrição não pode ficar vazia.")
    if result["amount"].isna().any() or (result["amount"] <= 0).any():
        raise ValueError("Os valores devem ser números maiores que zero.")

    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    return result


def summarize_transactions(data: pd.DataFrame) -> dict[str, float]:
    """Calcula receitas, despesas e saldo a partir das transações."""
    if data.empty:
        return {"income": 0.0, "expenses": 0.0, "balance": 0.0}

    amounts = pd.to_numeric(data["amount"], errors="coerce").fillna(0)
    types = data["type"]
    income = float(amounts[types == "Receita"].sum())
    expenses = float(amounts[types == "Despesa"].sum())
    return {"income": income, "expenses": expenses, "balance": income - expenses}


def monthly_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Retorna receitas, despesas e saldo agrupados por mês."""
    if data.empty:
        return pd.DataFrame(columns=["month", "income", "expenses", "balance"])

    frame = data.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["month"] = frame["date"].dt.to_period("M").astype(str)
    frame["income_value"] = frame["amount"].where(frame["type"] == "Receita", 0)
    frame["expense_value"] = frame["amount"].where(frame["type"] == "Despesa", 0)
    result = frame.groupby("month", as_index=False).agg(
        income=("income_value", "sum"),
        expenses=("expense_value", "sum"),
    )
    result["balance"] = result["income"] - result["expenses"]
    return result

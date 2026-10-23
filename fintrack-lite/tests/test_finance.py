import pandas as pd
import pytest

from finance import monthly_summary, normalize_transactions, summarize_transactions


def sample_data():
    return pd.DataFrame([
        {"date": "2026-01-01", "type": "Receita", "description": "Salário", "category": "Salário", "amount": 1000, "payment_method": "Pix"},
        {"date": "2026-01-02", "type": "Despesa", "description": "Mercado", "category": "Alimentação", "amount": 250, "payment_method": "Débito"},
    ])


def test_summary_calculates_income_expenses_and_balance():
    result = summarize_transactions(sample_data())
    assert result == {"income": 1000.0, "expenses": 250.0, "balance": 750.0}


def test_empty_summary_returns_zeroes():
    result = summarize_transactions(pd.DataFrame(columns=["type", "amount"]))
    assert result == {"income": 0.0, "expenses": 0.0, "balance": 0.0}


def test_normalize_rejects_non_positive_amounts():
    data = sample_data()
    data.loc[0, "amount"] = 0
    with pytest.raises(ValueError, match="maiores que zero"):
        normalize_transactions(data)


def test_monthly_summary_groups_by_month():
    result = monthly_summary(sample_data())
    assert len(result) == 1
    assert result.iloc[0]["month"] == "2026-01"
    assert result.iloc[0]["balance"] == 750

"""Reusable data-cleaning functions for DataClean Mini."""
import re

import pandas as pd


def normalize_column_names(df):
    """Return a copy with normalized, unique snake_case column names."""
    result = df.copy()
    normalized = []
    used = set()
    for index, column in enumerate(result.columns):
        name = re.sub(r"[^a-zA-Z0-9]+", "_", str(column).strip().lower()).strip("_")
        name = name or "coluna"
        candidate = name
        suffix = 2
        while candidate in used:
            candidate = f"{name}_{suffix}"
            suffix += 1
        used.add(candidate)
        normalized.append(candidate)
    result.columns = normalized
    return result


def trim_text_values(df):
    """Trim leading/trailing whitespace in text cells without changing missing values."""
    result = df.copy()
    for column in result.select_dtypes(include=["object", "string"]).columns:
        result[column] = result[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    return result


def missing_values_report(df):
    """Return a report with missing counts and percentages for each column."""
    total = len(df)
    report = pd.DataFrame({
        "coluna": df.columns,
        "valores_ausentes": [int(df[column].isna().sum()) for column in df.columns],
        "percentual_ausente": [
            round(float(df[column].isna().sum() / total * 100), 2) if total else 0.0
            for column in df.columns
        ],
    })
    return report


def clean_dataframe(df, normalize_columns=True, trim_text=True, drop_duplicates=True):
    """Apply selected cleaning steps and return a new DataFrame."""
    result = df.copy()
    if normalize_columns:
        result = normalize_column_names(result)
    if trim_text:
        result = trim_text_values(result)
    if drop_duplicates:
        result = result.drop_duplicates().reset_index(drop=True)
    return result

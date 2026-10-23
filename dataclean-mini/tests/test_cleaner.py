import pandas as pd

from cleaner import clean_dataframe, missing_values_report, normalize_column_names, trim_text_values


def test_normalizes_column_names_and_makes_them_unique():
    frame = pd.DataFrame([[1, 2, 3]], columns=[" Nome Completo ", "Nome-Completo", "!!!"])
    result = normalize_column_names(frame)
    assert list(result.columns) == ["nome_completo", "nome_completo_2", "coluna"]


def test_trims_text_without_changing_missing_values():
    frame = pd.DataFrame({"name": [" Ana ", None], "amount": [1, 2]})
    result = trim_text_values(frame)
    assert result.loc[0, "name"] == "Ana"
    assert pd.isna(result.loc[1, "name"])


def test_missing_values_report_calculates_counts_and_percentages():
    frame = pd.DataFrame({"a": [1, None, 3, None], "b": ["x", "y", "z", "w"]})
    report = missing_values_report(frame)
    assert report.loc[0, "valores_ausentes"] == 2
    assert report.loc[0, "percentual_ausente"] == 50.0
    assert report.loc[1, "valores_ausentes"] == 0


def test_clean_dataframe_drops_duplicates_and_preserves_original():
    frame = pd.DataFrame({" Nome ": [" Ana ", " Ana "], "Valor": [10, 10]})
    result = clean_dataframe(frame)
    assert len(result) == 1
    assert list(result.columns) == ["nome", "valor"]
    assert frame.iloc[0, 0] == " Ana "


def test_can_disable_cleaning_steps():
    frame = pd.DataFrame({" Name ": [" Ana ", " Ana "]})
    result = clean_dataframe(frame, normalize_columns=False, trim_text=False, drop_duplicates=False)
    assert list(result.columns) == [" Name "]
    assert len(result) == 2
    assert result.iloc[0, 0] == " Ana "

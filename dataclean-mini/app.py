"""DataClean Mini — inspect and clean CSV files."""
from pathlib import Path

import pandas as pd
import streamlit as st

from cleaner import clean_dataframe, missing_values_report

st.set_page_config(page_title="DataClean Mini", page_icon="🧹", layout="wide")
st.title("🧹 DataClean Mini")
st.caption("Explore, limpe e exporte CSVs sem alterar o arquivo original.")

uploaded = st.file_uploader("Envie um arquivo CSV", type=["csv"])
if uploaded is not None:
    try:
        original = pd.read_csv(uploaded)
    except Exception as error:
        st.error("Não foi possível ler o CSV: " + str(error))
        st.stop()
else:
    st.info("Você pode começar com a base fictícia de demonstração ou enviar seu próprio CSV.")
    original = pd.read_csv(Path(__file__).parent / "sample_dirty.csv")

if original.empty and len(original.columns) == 0:
    st.warning("O CSV não contém colunas para analisar.")
    st.stop()

st.subheader("Dados originais")
metric_cols = st.columns(3)
metric_cols[0].metric("Linhas", len(original))
metric_cols[1].metric("Colunas", len(original.columns))
metric_cols[2].metric("Duplicatas", int(original.duplicated().sum()))
st.dataframe(original.head(100), use_container_width=True)

st.subheader("Valores ausentes")
report = missing_values_report(original)
if report["valores_ausentes"].sum() == 0:
    st.success("Nenhum valor ausente encontrado.")
else:
    st.dataframe(report, hide_index=True, use_container_width=True)

st.subheader("Operações de limpeza")
col1, col2, col3 = st.columns(3)
normalize = col1.checkbox("Padronizar nomes das colunas", value=True)
trim = col2.checkbox("Remover espaços extras", value=True)
deduplicate = col3.checkbox("Remover linhas duplicadas", value=True)

cleaned = clean_dataframe(
    original,
    normalize_columns=normalize,
    trim_text=trim,
    drop_duplicates=deduplicate,
)

st.subheader("Prévia dos dados limpos")
st.caption(f"{len(original) - len(cleaned)} linha(s) removida(s) pelas opções selecionadas.")
st.dataframe(cleaned.head(100), hide_index=True, use_container_width=True)
csv_bytes = cleaned.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Baixar CSV limpo",
    data=csv_bytes,
    file_name="dataclean_mini_cleaned.csv",
    mime="text/csv",
)

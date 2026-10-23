from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from finance import COLUMNS, monthly_summary, normalize_transactions, summarize_transactions

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_FILE = DATA_DIR / "transactions.csv"
SAMPLE_FILE = APP_DIR / "sample_transactions.csv"

st.set_page_config(page_title="FinTrack Lite", page_icon="💸", layout="wide")


def load_transactions() -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        try:
            return normalize_transactions(pd.read_csv(DATA_FILE))
        except (ValueError, pd.errors.ParserError, UnicodeDecodeError):
            st.error("Não foi possível ler data/transactions.csv. Confira o arquivo antes de continuar.")
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)


def save_transactions(data: pd.DataFrame) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data[COLUMNS].to_csv(DATA_FILE, index=False, encoding="utf-8")


def brl(value: float) -> str:
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


if "transactions" not in st.session_state:
    st.session_state.transactions = load_transactions()

st.title("💸 FinTrack Lite")
st.caption("Controle financeiro pessoal simples, local e transparente.")
st.info("Os lançamentos são armazenados em CSV na pasta do projeto. Não informe dados bancários, senhas ou informações sensíveis.")

transactions = st.session_state.transactions.copy()
tab_dashboard, tab_add, tab_history, tab_data = st.tabs(
    ["📊 Visão geral", "➕ Novo lançamento", "📒 Histórico", "📁 Dados"]
)

with tab_dashboard:
    if transactions.empty:
        st.subheader("Seu controle começa aqui")
        st.write("Adicione uma receita ou despesa na aba **Novo lançamento** para visualizar seus indicadores.")
    else:
        month_options = sorted(pd.to_datetime(transactions["date"]).dt.strftime("%Y-%m").unique(), reverse=True)
        selected_month = st.selectbox("Período", ["Todos os meses"] + month_options)
        view = transactions.copy()
        if selected_month != "Todos os meses":
            view = view[pd.to_datetime(view["date"]).dt.strftime("%Y-%m") == selected_month]

        totals = summarize_transactions(view)
        c1, c2, c3 = st.columns(3)
        c1.metric("Receitas", brl(totals["income"]))
        c2.metric("Despesas", brl(totals["expenses"]))
        c3.metric("Saldo", brl(totals["balance"]))

        left, right = st.columns(2)
        with left:
            st.subheader("Despesas por categoria")
            expenses = view[view["type"] == "Despesa"].groupby("category", as_index=False)["amount"].sum()
            if expenses.empty:
                st.caption("Ainda não há despesas nesse período.")
            else:
                st.bar_chart(expenses.set_index("category")["amount"])
        with right:
            st.subheader("Evolução mensal")
            monthly = monthly_summary(transactions)
            if monthly.empty:
                st.caption("Sem dados suficientes para montar o gráfico.")
            else:
                st.line_chart(monthly.set_index("month")[["income", "expenses", "balance"]])

with tab_add:
    st.subheader("Registrar movimentação")
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date_value = col1.date_input("Data")
        transaction_type = col2.selectbox("Tipo", ["Despesa", "Receita"])
        description = st.text_input("Descrição", placeholder="Ex.: mercado, salário, transporte")
        col3, col4 = st.columns(2)
        category = col3.selectbox(
            "Categoria",
            ["Alimentação", "Moradia", "Transporte", "Saúde", "Educação", "Lazer", "Salário", "Serviços", "Outros"],
        )
        amount = col4.number_input("Valor (R$)", min_value=0.01, value=10.00, step=1.00, format="%.2f")
        payment_method = st.selectbox("Forma de pagamento", ["Pix", "Débito", "Crédito", "Dinheiro", "Transferência", "Outro"])
        submitted = st.form_submit_button("Salvar lançamento", type="primary")

    if submitted:
        if not description.strip():
            st.error("Informe uma descrição para o lançamento.")
        else:
            new_row = pd.DataFrame([{
                "date": date_value.isoformat(),
                "type": transaction_type,
                "description": description.strip(),
                "category": category,
                "amount": float(amount),
                "payment_method": payment_method,
            }])
            updated = pd.concat([transactions, new_row], ignore_index=True)
            try:
                updated = normalize_transactions(updated)
                save_transactions(updated)
                st.session_state.transactions = updated
                st.success("Lançamento salvo.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))

with tab_history:
    st.subheader("Lançamentos registrados")
    if transactions.empty:
        st.caption("Nenhum lançamento cadastrado ainda.")
    else:
        filter_type = st.multiselect("Filtrar por tipo", ["Receita", "Despesa"], default=["Receita", "Despesa"])
        filter_category = st.multiselect("Filtrar por categoria", sorted(transactions["category"].unique()))
        filtered = transactions[transactions["type"].isin(filter_type)]
        if filter_category:
            filtered = filtered[filtered["category"].isin(filter_category)]
        display = filtered.copy()
        display["date"] = pd.to_datetime(display["date"]).dt.strftime("%d/%m/%Y")
        display["amount"] = display["amount"].map(brl)
        st.dataframe(display.rename(columns={
            "date": "Data", "type": "Tipo", "description": "Descrição",
            "category": "Categoria", "amount": "Valor", "payment_method": "Pagamento",
        }), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Excluir lançamento")
        choices = {
            f"{row.date} · {row.type} · {row.description} · {brl(row.amount)}": idx
            for idx, row in transactions.iterrows()
        }
        selected_label = st.selectbox("Selecione um registro", list(choices))
        confirm_delete = st.checkbox("Confirmo que desejo excluir este lançamento.")
        if st.button("Excluir selecionado", disabled=not confirm_delete):
            updated = transactions.drop(index=choices[selected_label]).reset_index(drop=True)
            save_transactions(updated)
            st.session_state.transactions = updated
            st.success("Lançamento excluído.")
            st.rerun()

with tab_data:
    st.subheader("Importar e exportar")
    st.write("Exporte seus dados para backup ou importe um CSV com as colunas exigidas.")
    st.download_button(
        "⬇️ Baixar CSV dos lançamentos",
        data=transactions[COLUMNS].to_csv(index=False).encode("utf-8"),
        file_name="fintrack_lancamentos.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("Importar CSV", type=["csv"])
    if uploaded is not None:
        try:
            imported = normalize_transactions(pd.read_csv(uploaded))
            st.write(f"Prévia: {len(imported)} lançamento(s).")
            st.dataframe(imported, use_container_width=True, hide_index=True)
            if st.button("Adicionar lançamentos importados"):
                combined = pd.concat([transactions, imported], ignore_index=True)
                combined = normalize_transactions(combined)
                save_transactions(combined)
                st.session_state.transactions = combined
                st.success("Importação concluída.")
                st.rerun()
        except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as error:
            st.error(f"Arquivo inválido: {error}")

st.divider()
st.caption("FinTrack Lite · Projeto de portfólio educacional. Não é consultoria financeira.")

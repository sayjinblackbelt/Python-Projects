"""TaskFlow Python — a small Streamlit task manager."""
from datetime import date

import pandas as pd
import streamlit as st

from task_store import add_task, delete_task, init_db, list_tasks, update_task_status

st.set_page_config(page_title="TaskFlow Python", page_icon="✅", layout="wide")
st.title("✅ TaskFlow Python")
st.caption("Organize suas tarefas com simplicidade. Os dados são salvos localmente.")

init_db()

all_tasks = list_tasks()
pending = sum(task["status"] == "Pendente" for task in all_tasks)
completed = sum(task["status"] == "Concluída" for task in all_tasks)
overdue = sum(
    task["status"] == "Pendente" and task["due_date"] and task["due_date"] < date.today().isoformat()
    for task in all_tasks
)

metric_cols = st.columns(3)
metric_cols[0].metric("Pendentes", pending)
metric_cols[1].metric("Concluídas", completed)
metric_cols[2].metric("Atrasadas", overdue)

tab_tasks, tab_new = st.tabs(["Minhas tarefas", "Nova tarefa"])

with tab_tasks:
    filters = st.columns(2)
    status_filter = filters[0].selectbox("Status", ["Todas", "Pendente", "Concluída"])
    priority_filter = filters[1].selectbox("Prioridade", ["Todas", "Alta", "Média", "Baixa"])
    tasks = list_tasks(status_filter, priority_filter)

    if not tasks:
        st.info("Nenhuma tarefa encontrada. Crie uma na aba **Nova tarefa**.")
    else:
        for task in tasks:
            with st.container(border=True):
                cols = st.columns([5, 2, 2, 2])
                cols[0].markdown("**" + task["title"] + "**")
                if task["description"]:
                    cols[0].caption(task["description"])
                due = task["due_date"] if task["due_date"] else "Sem prazo"
                cols[1].write("Prazo: " + due)
                cols[2].write("Prioridade: " + task["priority"])
                cols[3].write(task["status"])
                action_cols = st.columns([1, 1, 5])
                next_status = "Concluída" if task["status"] == "Pendente" else "Pendente"
                action_label = "Concluir" if task["status"] == "Pendente" else "Reabrir"
                if action_cols[0].button(action_label, key="toggle_" + str(task["id"])):
                    update_task_status(task["id"], next_status)
                    st.rerun()
                if action_cols[1].button("Excluir", key="delete_" + str(task["id"])):
                    delete_task(task["id"])
                    st.rerun()

with tab_new:
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Título *", max_chars=120)
        description = st.text_area("Descrição (opcional)")
        priority = st.selectbox("Prioridade", ["Média", "Alta", "Baixa"])
        due_date = st.date_input("Prazo (opcional)", value=None)
        submitted = st.form_submit_button("Adicionar tarefa")
    if submitted:
        try:
            normalized_date = due_date.isoformat() if due_date else ""
            add_task(title, description, priority, normalized_date)
            st.success("Tarefa adicionada.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

"""QuizLab — multiple-choice quiz application."""
import streamlit as st

from quiz_engine import load_questions, score_answers

st.set_page_config(page_title="QuizLab", page_icon="🧠", layout="wide")
st.title("🧠 QuizLab")
st.caption("Teste seus conhecimentos de Python. Escolha uma alternativa para cada pergunta.")

try:
    questions = load_questions()
except (OSError, ValueError) as error:
    st.error("Não foi possível carregar o quiz: " + str(error))
    st.stop()

with st.form("quiz_form"):
    answers = {}
    for question in questions:
        st.subheader(str(question["id"]) + ". " + question["question"])
        answers[question["id"]] = st.radio(
            "Selecione uma alternativa",
            question["options"],
            index=None,
            key="question_" + str(question["id"]),
            label_visibility="collapsed",
        )
    submitted = st.form_submit_button("Corrigir respostas", type="primary")

if submitted:
    unanswered = [question for question in questions if answers[question["id"]] is None]
    if unanswered:
        st.warning("Responda a todas as perguntas antes de corrigir. Faltam: " + str(len(unanswered)) + ".")
    else:
        result = score_answers(questions, answers)
        st.divider()
        st.header("Seu resultado")
        left, middle, right = st.columns(3)
        left.metric("Acertos", str(result["correct"]) + " / " + str(result["total"]))
        middle.metric("Percentual", str(result["percentage"]) + "%")
        right.metric("Questões", result["total"])
        st.progress(result["percentage"] / 100)
        for item in result["results"]:
            with st.container(border=True):
                st.markdown(("✅ " if item["is_correct"] else "❌ ") + "**" + item["question"] + "**")
                st.write("Sua resposta: " + str(item["selected"]))
                if not item["is_correct"]:
                    st.write("Resposta correta: " + item["answer"])
                st.caption(item["explanation"])

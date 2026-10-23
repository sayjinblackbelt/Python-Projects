import json

import pytest

from quiz_engine import load_questions, score_answers


def sample_questions():
    return [
        {
            "id": 1,
            "question": "Tipo de texto?",
            "options": ["str", "int"],
            "answer": "str",
            "explanation": "str representa texto.",
        },
        {
            "id": 2,
            "question": "Palavra-chave de função?",
            "options": ["def", "loop"],
            "answer": "def",
            "explanation": "def define funções.",
        },
    ]


def test_loads_demo_questions():
    questions = load_questions()
    assert len(questions) >= 5
    assert all(question["answer"] in question["options"] for question in questions)


def test_scores_all_correct_answers():
    result = score_answers(sample_questions(), {1: "str", 2: "def"})
    assert result["correct"] == 2
    assert result["total"] == 2
    assert result["percentage"] == 100.0


def test_scores_incorrect_and_missing_answers():
    result = score_answers(sample_questions(), {1: "int"})
    assert result["correct"] == 0
    assert result["percentage"] == 0.0
    assert result["results"][1]["selected"] is None


def test_rejects_empty_question_file(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="lista de perguntas"):
        load_questions(path)


def test_rejects_answer_not_in_options(tmp_path):
    path = tmp_path / "questions.json"
    questions = sample_questions()
    questions[0]["answer"] = "float"
    path.write_text(json.dumps(questions), encoding="utf-8")
    with pytest.raises(ValueError, match="precisa existir"):
        load_questions(path)

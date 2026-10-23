"""Core functions for loading and scoring multiple-choice quizzes."""
import json
from pathlib import Path


DEFAULT_QUESTIONS_PATH = Path(__file__).parent / "data" / "questions.json"


def load_questions(path=DEFAULT_QUESTIONS_PATH):
    """Load and validate questions from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        questions = json.load(file)
    if not isinstance(questions, list) or not questions:
        raise ValueError("O arquivo deve conter uma lista de perguntas.")
    seen_ids = set()
    for question in questions:
        required = {"id", "question", "options", "answer", "explanation"}
        if not isinstance(question, dict) or not required.issubset(question):
            raise ValueError("Cada pergunta deve conter id, question, options, answer e explanation.")
        if question["id"] in seen_ids:
            raise ValueError("Os IDs das perguntas devem ser únicos.")
        seen_ids.add(question["id"])
        if not isinstance(question["options"], list) or len(question["options"]) < 2:
            raise ValueError("Cada pergunta deve ter pelo menos duas alternativas.")
        if question["answer"] not in question["options"]:
            raise ValueError("A resposta correta precisa existir entre as alternativas.")
    return questions


def score_answers(questions, answers):
    """Score a mapping of question IDs to selected option text."""
    if not questions:
        raise ValueError("Não há perguntas para avaliar.")
    correct = 0
    results = []
    for question in questions:
        selected = answers.get(question["id"])
        is_correct = selected == question["answer"]
        correct += int(is_correct)
        results.append({
            "id": question["id"],
            "question": question["question"],
            "selected": selected,
            "answer": question["answer"],
            "is_correct": is_correct,
            "explanation": question["explanation"],
        })
    total = len(questions)
    return {
        "correct": correct,
        "total": total,
        "percentage": round(correct / total * 100, 1),
        "results": results,
    }

import pytest

from task_store import (
    add_task,
    delete_task,
    init_db,
    list_tasks,
    update_task_status,
    validate_task,
)


def test_add_and_list_tasks(tmp_path):
    db_path = tmp_path / "tasks.db"
    init_db(db_path)
    task_id = add_task("Estudar Python", "Praticar funções", "Alta", "2026-11-01", db_path)
    tasks = list_tasks(db_path=db_path)
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Estudar Python"
    assert tasks[0]["priority"] == "Alta"
    assert tasks[0]["status"] == "Pendente"


def test_validation_rejects_empty_title():
    with pytest.raises(ValueError, match="obrigatório"):
        validate_task("   ")


def test_validation_rejects_invalid_priority():
    with pytest.raises(ValueError, match="Prioridade inválida"):
        validate_task("Tarefa", "Urgente")


def test_update_status_and_filter(tmp_path):
    db_path = tmp_path / "tasks.db"
    init_db(db_path)
    task_id = add_task("Ler documentação", db_path=db_path)
    assert update_task_status(task_id, "Concluída", db_path)
    assert list_tasks("Pendente", db_path=db_path) == []
    assert list_tasks("Concluída", db_path=db_path)[0]["id"] == task_id


def test_delete_task(tmp_path):
    db_path = tmp_path / "tasks.db"
    init_db(db_path)
    task_id = add_task("Tarefa temporária", db_path=db_path)
    assert delete_task(task_id, db_path)
    assert list_tasks(db_path=db_path) == []
    assert not delete_task(task_id, db_path)

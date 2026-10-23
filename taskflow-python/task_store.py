"""SQLite persistence and validation for TaskFlow Python."""
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent / "data" / "tasks.db"


def _connect(db_path=DEFAULT_DB_PATH):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path=DEFAULT_DB_PATH):
    """Create the tasks table when it does not exist."""
    with _connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Média',
                due_date TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Pendente',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def validate_task(title, priority="Média", due_date=""):
    """Validate task fields and return normalized values."""
    normalized_title = str(title).strip()
    if not normalized_title:
        raise ValueError("O título da tarefa é obrigatório.")
    if len(normalized_title) > 120:
        raise ValueError("O título deve ter no máximo 120 caracteres.")
    if priority not in ("Baixa", "Média", "Alta"):
        raise ValueError("Prioridade inválida.")
    normalized_due_date = str(due_date or "").strip()
    return normalized_title, priority, normalized_due_date


def add_task(title, description="", priority="Média", due_date="", db_path=DEFAULT_DB_PATH):
    """Insert a task and return its ID."""
    title, priority, due_date = validate_task(title, priority, due_date)
    with _connect(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
            (title, str(description or "").strip(), priority, due_date),
        )
        return cursor.lastrowid


def list_tasks(status="Todas", priority="Todas", db_path=DEFAULT_DB_PATH):
    """Return tasks as dictionaries, newest first."""
    query = "SELECT * FROM tasks"
    conditions = []
    params = []
    if status in ("Pendente", "Concluída"):
        conditions.append("status = ?")
        params.append(status)
    if priority in ("Baixa", "Média", "Alta"):
        conditions.append("priority = ?")
        params.append(priority)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY CASE status WHEN 'Pendente' THEN 0 ELSE 1 END, id DESC"
    with _connect(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def update_task_status(task_id, status, db_path=DEFAULT_DB_PATH):
    """Update a task's status."""
    if status not in ("Pendente", "Concluída"):
        raise ValueError("Status inválido.")
    with _connect(db_path) as connection:
        cursor = connection.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (status, int(task_id))
        )
        return cursor.rowcount > 0


def delete_task(task_id, db_path=DEFAULT_DB_PATH):
    """Delete a task and report whether a row was removed."""
    with _connect(db_path) as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (int(task_id),))
        return cursor.rowcount > 0

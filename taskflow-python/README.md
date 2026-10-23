# TaskFlow Python ✅

Aplicação de gerenciamento de tarefas desenvolvida em Python e Streamlit, com persistência local em SQLite. Projeto de portfólio para praticar CRUD, organização de dados, filtros, validação e testes automatizados.

## Funcionalidades

- Criar tarefas com título, descrição, prioridade e prazo opcional.
- Visualizar tarefas pendentes e concluídas.
- Filtrar por status e prioridade.
- Marcar tarefas como concluídas ou reabrir tarefas.
- Excluir tarefas.
- Persistir os dados em um banco SQLite local.

## Tecnologias

- Python 3.9+
- Streamlit
- SQLite (biblioteca padrão do Python)
- Pytest

## Executar no macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

No Windows PowerShell, ative o ambiente com `.venv\\Scripts\\Activate.ps1`.

O banco de dados é criado localmente em `data/tasks.db`. Esse arquivo é ignorado pelo Git; não envie dados pessoais ao repositório.

## Estrutura

```text
taskflow-python/
├── app.py
├── task_store.py
├── requirements.txt
├── .gitignore
├── README.md
└── tests/
    └── test_task_store.py
```

## Objetivo de aprendizagem

Demonstrar operações CRUD (criar, consultar, atualizar e excluir), persistência SQLite, separação entre interface e regras de dados e testes automatizados.

## Próximas melhorias

- Editar tarefas existentes.
- Criar etiquetas e projetos.
- Adicionar lembretes.
- Exportar tarefas para CSV.

Projeto educacional de portfólio; os dados ficam armazenados localmente.
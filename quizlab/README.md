# QuizLab 🧠

Aplicação de quizzes de múltipla escolha feita com Python e Streamlit. O projeto pratica leitura de JSON, lógica de pontuação, validação de respostas, interface web e testes automatizados.

## Funcionalidades

- Carregar perguntas de um arquivo JSON.
- Exibir perguntas com alternativas de múltipla escolha.
- Calcular pontuação e percentual de acertos.
- Mostrar feedback por pergunta após o envio.
- Separar a lógica do quiz da interface.
- Testar a lógica com Pytest.

## Tecnologias

- Python 3.9+
- Streamlit
- Pytest
- JSON (biblioteca padrão do Python)

## Executar no macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

No Windows PowerShell, ative o ambiente com `.venv\\Scripts\\Activate.ps1`.

## Personalizar as perguntas

Edite `data/questions.json`. Cada pergunta deve ter `id`, `question`, `options`, `answer` e `explanation`. O campo `answer` deve corresponder exatamente a uma das alternativas.

## Estrutura

```text
quizlab/
├── app.py
├── quiz_engine.py
├── requirements.txt
├── data/
│   └── questions.json
├── tests/
│   └── test_quiz_engine.py
├── .gitignore
└── README.md
```

## Objetivo de aprendizagem

Demonstrar separação de responsabilidades, leitura de dados estruturados, funções puras para avaliação e testes automatizados.

Projeto educacional de portfólio.
# DataClean Mini 🧹

Aplicação web para explorar e limpar arquivos CSV com Python, Pandas e Streamlit. Projeto de portfólio focado em qualidade de dados, tratamento de valores ausentes, padronização de colunas e remoção de duplicatas.

## Funcionalidades

- Carregar CSV próprio ou usar a base de demonstração.
- Visualizar amostra e dimensões do conjunto de dados.
- Inspecionar valores ausentes por coluna.
- Padronizar nomes de colunas.
- Remover espaços extras de textos.
- Remover linhas duplicadas.
- Exportar o resultado limpo para CSV.
- Testar as funções de limpeza com Pytest.

## Tecnologias

- Python 3.9+
- Pandas
- Streamlit
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

## Base de demonstração

O arquivo `sample_dirty.csv` contém dados fictícios com espaços extras, linhas duplicadas e valores ausentes para demonstrar as operações de limpeza.

## Estrutura

```text
dataclean-mini/
├── app.py
├── cleaner.py
├── requirements.txt
├── sample_dirty.csv
├── tests/
│   └── test_cleaner.py
├── .gitignore
└── README.md
```

## Objetivo de aprendizagem

Praticar exploração de dados, transformações com Pandas, validação de arquivos tabulares e exportação de dados tratados.

A aplicação não sobrescreve o arquivo original: o resultado limpo é disponibilizado como um novo download. Projeto educacional de portfólio.
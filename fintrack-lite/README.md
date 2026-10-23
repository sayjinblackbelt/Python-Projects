# FinTrack Lite 💸

Aplicação web de controle financeiro pessoal desenvolvida em Python. O projeto demonstra manipulação de dados, validação, persistência em CSV, visualização de indicadores e testes automatizados.

## Funcionalidades

- Registro de receitas e despesas com data, categoria e forma de pagamento.
- Indicadores de receitas, despesas e saldo por período.
- Gráficos de despesas por categoria e evolução mensal.
- Histórico com filtros e exclusão de lançamentos.
- Importação e exportação de CSV para backup.
- Validação de campos e valores.
- Testes automatizados das funções de domínio.

## Tecnologias

- Python 3.9 ou superior
- Streamlit
- Pandas
- Pytest

## Executar localmente

Abra o terminal dentro desta pasta e execute:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abrirá o painel no navegador. Os lançamentos criados ficam em `data/transactions.csv`, arquivo local ignorado pelo Git para evitar publicar dados pessoais.

## Dados de demonstração

O arquivo `sample_transactions.csv` contém apenas lançamentos fictícios. Para testar com esses dados, importe-o pela aba **Dados**. O aplicativo não carrega esses exemplos automaticamente.

## Testes

Com as dependências instaladas, execute:

```bash
pytest -q
```

## Estrutura

```text
fintrack-lite/
├── app.py
├── finance.py
├── requirements.txt
├── sample_transactions.csv
├── tests/
│   └── test_finance.py
├── .gitignore
└── README.md
```

## Próximas melhorias

- Editar lançamentos existentes.
- Planejamento de orçamento por categoria.
- Exportação de relatórios em Excel.
- Autenticação e banco de dados para implantação multiusuário.

## Aviso

Projeto educacional para fins de portfólio. Não é uma ferramenta de aconselhamento financeiro. Evite inserir dados bancários, senhas ou outras informações sensíveis.

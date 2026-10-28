# NEXA PrivacyGuard

Ferramenta de linha de comando, desenvolvida em Python, para identificar e mascarar padrões que podem conter dados sensíveis em textos.

## Objetivo

O NEXA PrivacyGuard ajuda a reduzir a exposição acidental de informações pessoais ou credenciais antes de compartilhar um texto.

O processamento é feito localmente: o programa não envia o conteúdo analisado para serviços externos.

## Funcionalidades

- Identificação de endereços de e-mail.
- Detecção de CPFs com validação dos dígitos verificadores.
- Classificação de sequências com formato de CPF, mas com dígitos inválidos, como `CPF_SUSPEITO`.
- Identificação de números de telefone brasileiros em formatos reconhecidos.
- Detecção de possíveis tokens associados a campos como `api_key`, `access_token` e `secret`.
- Mascaramento dos valores identificados.
- Testes automatizados com pytest.

## Requisitos

- Python 3.10 ou superior.
- pytest para executar os testes.

O programa utiliza a biblioteca padrão do Python durante a execução. O pytest é necessário apenas para executar os testes.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/sayjinblackbelt/Python-Projects.git
cd Python-Projects/nexa-privacyguard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
```

## Como usar

Execute:

```bash
python main.py
```

Digite ou cole o texto que deseja analisar. Para finalizar a entrada, digite `FIM` em uma linha separada.

O programa informa a quantidade de ocorrências, as categorias identificadas e apresenta o texto mascarado.

### Exemplo de entrada

```text
Contato: exemplo@teste.com
CPF: 123.456.789-00
Telefone: (19) 98765-4321
api_key=abcDEF123456xyz
FIM
```

### Exemplo de saída mascarada

```text
Contato: [EMAIL]
CPF: [CPF_SUSPEITO]
Telefone: [TELEFONE]
api_key=[TOKEN]
```

Os dados acima são exemplos fictícios para demonstração.

## Testes

Com o ambiente virtual ativado, execute:

```bash
python -m pytest -v
```

## Limitações e privacidade

- A ferramenta identifica padrões conhecidos e não garante detectar todos os dados pessoais, segredos ou credenciais.
- A validação do CPF verifica os dígitos verificadores, mas não confirma existência, situação cadastral ou titularidade.
- A detecção de tokens depende dos formatos e nomes de campos reconhecidos.
- Revise o resultado antes de compartilhar o texto.
- O processamento local não substitui controles de segurança, gestão de segredos ou uma revisão de privacidade.
- Não utilize dados pessoais reais nos testes ou exemplos públicos.

## Licença

A licença do projeto ainda precisa ser definida antes da publicação.

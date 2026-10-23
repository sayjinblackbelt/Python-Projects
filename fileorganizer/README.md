# FileOrganizer

Organizador de arquivos por extensão, com Python, `pathlib`, `shutil` e uma interface Streamlit.

## Funcionalidades

- Analisa os arquivos que estão diretamente dentro de uma pasta escolhida.
- Classifica arquivos em Imagens, Documentos, Áudio, Vídeos, Arquivos compactados e Outros.
- Mostra um plano de organização antes de mover qualquer arquivo.
- Evita sobrescrever arquivos quando já existe um nome igual no destino.
- Exige confirmação explícita antes de executar as movimentações.
- Inclui testes automatizados com pastas temporárias.

## Requisitos

- Python 3.9 ou superior

## Executar no macOS

Na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Como usar

1. Copie o caminho completo da pasta que deseja organizar, por exemplo `/Users/seu_usuario/Downloads`.
2. Cole o caminho no campo da aplicação e clique em **Analisar pasta**.
3. Revise o plano e as pastas de destino.
4. Marque a confirmação e clique em **Organizar arquivos** para executar.

A aplicação não move arquivos automaticamente: primeiro apresenta uma prévia. Ela organiza apenas arquivos diretamente na pasta selecionada; não percorre subpastas. Recomenda-se testar primeiro com uma pasta de exemplo e manter cópias de segurança de arquivos importantes.

## Categorias

- Imagens: PNG, JPG, JPEG, GIF, WEBP, SVG, HEIC
- Documentos: PDF, DOC, DOCX, TXT, ODT, XLS, XLSX, CSV, PPT, PPTX
- Áudio: MP3, WAV, AAC, M4A, OGG, FLAC
- Vídeos: MP4, MOV, MKV, AVI, WEBM
- Arquivos compactados: ZIP, RAR, 7Z, TAR, GZ
- Outros: extensões não mapeadas e arquivos sem extensão

## Estrutura

```text
fileorganizer/
├── app.py
├── organizer.py
├── requirements.txt
├── README.md
└── tests/
    └── test_organizer.py
```

# API de Upload e Download de Arquivos

API desenvolvida em Python com Flask para receber arquivos, armazenar seus dados em um banco SQLite e permitir o download dos arquivos enviados.

## Funcionalidades

- Envio de arquivos por meio de uma requisição HTTP `POST`.
- Download de arquivos por meio de uma requisição HTTP `GET`.
- Registro dos arquivos enviados no banco de dados SQLite.
- Validação das extensões e do tamanho dos arquivos.
- Limite de **30 KB por arquivo**.

## Tecnologias

- Python
- Flask
- SQLite
- Gunicorn (servidor usado na publicação)

## Estrutura do projeto

```text
projeto_api/
├── controllers/
│   ├── download_controller.py
│   └── upload_controller.py
├── database/
│   └── db.py
├── models/
│   ├── download_model.py
│   └── upload_model.py
├── routes/
│   ├── download_route.py
│   └── upload_route.py
├── uploads/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 ou superior.
- pip.

## Como executar localmente

1. Abra a pasta do projeto no VS Code.
2. Crie e ative um ambiente virtual:

   **Windows (PowerShell):**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows (Prompt de Comando):**

   ```bat
   py -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a API:

   ```bash
   python app.py
   ```

5. Acesse `http://127.0.0.1:5000/` no navegador. A rota `/health` pode ser usada para verificar se a API está ativa.

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Apresenta informações básicas da API. |
| GET | `/health` | Verifica o estado da aplicação. |
| POST | `/uploads/upload` | Envia um arquivo. |
| GET | `/downloads/download/<nome_do_arquivo>` | Baixa um arquivo enviado. |

### Como enviar um arquivo

No Postman ou Insomnia:

1. Selecione o método `POST`.
2. Informe a URL `http://127.0.0.1:5000/uploads/upload`.
3. Abra **Body > form-data**.
4. Crie um campo chamado `file`, alterando o tipo para **File**.
5. Escolha um arquivo e envie a requisição.

Extensões aceitas: `png`, `jpg`, `jpeg`, `gif`, `pdf` e `txt`.

O tamanho máximo é de 30 KB por arquivo. Se o envio for concluído, a resposta informa o nome do arquivo e o caminho de download.

### Como baixar um arquivo

Use o método `GET` e acesse:

```text
http://127.0.0.1:5000/downloads/download/NOME_DO_ARQUIVO
```

Troque `NOME_DO_ARQUIVO` pelo nome retornado no envio.

## Publicação no Render

1. Envie todos os arquivos do projeto para um repositório GitHub.
2. No Render, crie um **New Web Service** e conecte o repositório.
3. Configure:

   - **Language/Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. Clique para criar o serviço e aguarde o deploy.
5. Teste a URL pública do serviço, acrescentando `/` ou `/health`.

### Armazenamento no Render

O sistema de arquivos padrão de um Web Service do Render é temporário. Para manter os arquivos enviados e o banco SQLite entre deploys e reinicializações, configure um **Persistent Disk** no serviço, com ponto de montagem `/var/data`, e adicione estas variáveis de ambiente:

```text
UPLOAD_FOLDER=/var/data/uploads
DATABASE_PATH=/var/data/database.db
```

Sem um disco persistente (ou outro armazenamento externo), os arquivos e o banco gravados localmente podem ser perdidos em um novo deploy ou reinicialização. Verifique no Render a disponibilidade e as condições do Persistent Disk para o plano escolhido.

## Observações

- O modo debug fica desativado por padrão.
- O banco SQLite é criado automaticamente quando a aplicação inicia.
- Não envie o ambiente virtual (`.venv`), arquivos de banco, uploads privados ou o arquivo `.env` para o GitHub.

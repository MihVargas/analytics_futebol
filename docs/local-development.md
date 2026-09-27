# Desenvolvimento local

Este guia configura um PostgreSQL local com Docker e executa a ingestão, as transformações dbt e o dashboard.

## Requisitos

- Python 3.12 ou compatível com as dependências instaladas.
- Docker com suporte a `docker compose` (ou uma instância PostgreSQL disponível).
- Token de API da [football-data.org](https://www.football-data.org/client/register).

## Preparar o ambiente

Na raiz do repositório:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Preencha `FOOTBALL_API_TOKEN` no `.env`. O arquivo `.env` é ignorado pelo Git; não versione tokens nem senhas reais.

## Iniciar o PostgreSQL

```bash
docker compose up -d postgres
docker compose ps
```

O serviço escuta em `localhost:5432` e mantém os dados no volume `postgres_data`. Os valores locais de exemplo são `dbanalytics` (banco), `football` (usuário) e `football` (senha). Eles podem ser alterados no `.env`; mantenha sincronizados `POSTGRES_*`, `PG_*` e a URL `POSTGRES_URL`.

Para parar o serviço sem apagar os dados:

```bash
docker compose down
```

Para apagar também o volume e todos os dados locais:

```bash
docker compose down -v
```

## Executar o pipeline

Com o ambiente virtual ativado e o PostgreSQL pronto:

```bash
python run_pipeline.py
```

O script roda a extração (`extraction.py`), depois `dbt run` e `dbt test` dentro de `dbt_project/`. O `dlt` grava no schema `football_raw`; o dbt lê essas tabelas e materializa as tabelas finais no schema `analytics`.

Também é possível executar as etapas separadamente:

```bash
python extraction.py
cd dbt_project
dbt debug
dbt run
dbt test
```

`dbt debug` valida a conexão e o perfil antes da transformação. O perfil usa `PG_HOST`, `PG_USER` e `PG_PASSWORD` e define banco `dbanalytics`, porta `5432` e schema `analytics` em `dbt_project/profiles.yml`.

## Iniciar o dashboard

Volte à raiz do projeto e rode:

```bash
streamlit run dash.py
```

O app conecta usando `POSTGRES_URL`, consulta os modelos `analytics.fct_matches` e `analytics.champion_curse`, e a view `analytics.stg_standings`. Se nenhuma tabela estiver disponível, execute primeiro o pipeline.

## Configuração do banco remoto

Para usar um PostgreSQL gerenciado, configure `POSTGRES_URL` com a URL de conexão aceita pelo driver PostgreSQL do dlt/SQLAlchemy e defina `PG_HOST`, `PG_USER` e `PG_PASSWORD` para o dbt. O banco deve se chamar `dbanalytics`, salvo ajuste correspondente no `profiles.yml`.

## Variáveis de ambiente

| Variável | Usada por | Descrição |
| --- | --- | --- |
| `FOOTBALL_API_TOKEN` | `extraction.py` | Token de acesso à API football-data.org |
| `POSTGRES_URL` | dlt e dashboard | URL de conexão ao PostgreSQL |
| `PG_HOST` | dbt | Host do banco |
| `PG_USER` | dbt | Usuário do banco |
| `PG_PASSWORD` | dbt | Senha do banco |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker Compose | Credenciais usadas na inicialização do container local |

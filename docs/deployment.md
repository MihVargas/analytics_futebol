# Execução automatizada e deploy

## GitHub Actions

O workflow `.github/workflows/pipeline.yml` executa `python run_pipeline.py` em execução manual (`workflow_dispatch`) e em agenda diária. Para a execução automatizada, configure estes GitHub Actions secrets:

- `PG_HOST`
- `PG_USER`
- `PG_PASSWORD`
- `FOOTBALL_API_TOKEN`
- `POSTGRES_URL`

O workflow atualmente injeta as três variáveis `PG_*` no processo do pipeline. Como a extração e o dashboard também requerem suas próprias credenciais, `FOOTBALL_API_TOKEN` precisa ser passado ao step e `POSTGRES_URL` deve estar disponível para `extraction.py`. Inclua esses dois secrets em `env` no workflow antes de esperar que a execução em CI funcione.

O agendamento do GitHub Actions usa UTC. O cron definido é `30 16 * * *` (16:30 UTC); ajuste a expressão cron se quiser outro horário.

## Dashboard no Render

O `render.yaml` descreve um serviço web Python que inicia `streamlit run dash.py --server.port $PORT`. O serviço precisa da variável `POSTGRES_URL` apontando para o banco que contém os schemas `football_raw` e `analytics`. A configuração atual não cria um banco PostgreSQL; configure uma instância separada e adicione a URL nas variáveis do serviço.

Para publicar o dashboard:

1. Conecte o repositório ao Render e crie o serviço definido pelo Blueprint.
2. Cadastre `POSTGRES_URL` como variável secreta no serviço.
3. Execute o pipeline contra a mesma instância PostgreSQL antes de abrir o dashboard.

O health check está configurado em `/_stcore/health`.

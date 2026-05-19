# Task 3 — Consultas analíticas e dashboard com Athena, Glue e Jupyter

Este projeto organiza a Task 3 fora de um único notebook.

Ele cria o **database no AWS Glue Data Catalog**, registra as tabelas externas em Parquet no Athena/Glue e executa as consultas e o dashboard interativo no Jupyter.

## Estrutura

```text
task3_athena_dashboard_project/
├── .env.example
├── requirements.txt
├── README.md
├── scripts/
│   ├── 01_create_glue_database.py
│   ├── 02_create_athena_tables.py
│   ├── 03_validate_athena_tables.py
│   └── run_all_setup.py
├── sql/
│   ├── create_dim_customers.sql
│   ├── create_dim_products.sql
│   ├── create_dim_dates.sql
│   ├── create_dim_countries.sql
│   ├── create_fact_orders.sql
│   └── queries_task3.sql
├── src/
│   └── task3/
│       ├── __init__.py
│       ├── config.py
│       ├── athena.py
│       └── dashboard.py
└── notebooks/
    └── task3_consultas_dashboard.ipynb
```

## Pré-requisitos

1. Ter credenciais AWS válidas no ambiente.
2. Ter os dados Parquet da Task 2 gravados no S3, separados por pasta:

```text
s3://SEU_BUCKET/SEU_PREFIXO/dim_customers/
s3://SEU_BUCKET/SEU_PREFIXO/dim_products/
s3://SEU_BUCKET/SEU_PREFIXO/dim_dates/
s3://SEU_BUCKET/SEU_PREFIXO/dim_countries/
s3://SEU_BUCKET/SEU_PREFIXO/fact_orders/
```

3. Ter um bucket/prefixo para resultados do Athena:

```text
s3://SEU_BUCKET/athena-results/
```

## Instalação

```bash
pip install -r requirements.txt
```

Copie o `.env.example` para `.env` e ajuste os valores:

```bash
cp .env.example .env
```

Exemplo:

```env
AWS_REGION=us-east-1
GLUE_DATABASE=classicmodels_star_schema
DATA_S3_BASE_PATH=s3://meu-bucket/task2/star-schema
ATHENA_S3_OUTPUT=s3://meu-bucket/athena-results/
```

## Execução do setup

Você pode executar tudo de uma vez:

```bash
python scripts/run_all_setup.py
```

Ou por etapas:

```bash
python scripts/01_create_glue_database.py
python scripts/02_create_athena_tables.py
python scripts/03_validate_athena_tables.py
```

## Execução do dashboard

Abra:

```text
notebooks/task3_consultas_dashboard.ipynb
```

Execute as células em ordem.

## Observação sobre nomes

Este projeto usa exatamente as tabelas e colunas exigidas na Task 2:

- `fact_orders`
- `dim_customers`
- `dim_products`
- `dim_dates`
- `dim_countries`

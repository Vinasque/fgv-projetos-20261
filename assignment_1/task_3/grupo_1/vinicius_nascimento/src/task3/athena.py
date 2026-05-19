from __future__ import annotations

from pathlib import Path
import time

import boto3
import awswrangler as wr
import pandas as pd

from task3.config import get_settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql"


def get_boto3_session() -> boto3.Session:
    settings = get_settings()
    return boto3.Session(region_name=settings.aws_region)


def read_sql_file(filename: str) -> str:
    path = SQL_DIR / filename
    return path.read_text(encoding="utf-8")


def render_sql_template(sql: str) -> str:
    settings = get_settings()
    base = settings.normalized_data_s3_base_path

    replacements = {
        "{{GLUE_DATABASE}}": settings.glue_database,
        "{{DATA_S3_BASE_PATH}}": base,
        "{{DIM_CUSTOMERS_PATH}}": f"{base}/dim_customers/",
        "{{DIM_PRODUCTS_PATH}}": f"{base}/dim_products/",
        "{{DIM_DATES_PATH}}": f"{base}/dim_dates/",
        "{{DIM_COUNTRIES_PATH}}": f"{base}/dim_countries/",
        "{{FACT_ORDERS_PATH}}": f"{base}/fact_orders/",
    }

    for key, value in replacements.items():
        sql = sql.replace(key, value)

    return sql


def athena_read(sql: str) -> pd.DataFrame:
    settings = get_settings()
    session = get_boto3_session()
    return wr.athena.read_sql_query(
        sql=sql,
        database=settings.glue_database,
        s3_output=settings.athena_s3_output,
        boto3_session=session,
    )


def athena_execute(sql: str) -> str:
    settings = get_settings()
    session = get_boto3_session()
    client = session.client("athena")

    response = client.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": settings.glue_database},
        ResultConfiguration={"OutputLocation": settings.athena_s3_output},
    )

    query_execution_id = response["QueryExecutionId"]

    while True:
        result = client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result["QueryExecution"]["Status"]["State"]

        if status in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            if status != "SUCCEEDED":
                reason = result["QueryExecution"]["Status"].get("StateChangeReason", "Sem detalhe")
                raise RuntimeError(f"Consulta Athena terminou com status {status}: {reason}")
            return query_execution_id

        time.sleep(2)


def create_glue_database() -> None:
    settings = get_settings()
    session = get_boto3_session()
    glue = session.client("glue")

    try:
        glue.get_database(Name=settings.glue_database)
        print(f"Database já existe no Glue: {settings.glue_database}")
    except glue.exceptions.EntityNotFoundException:
        glue.create_database(
            DatabaseInput={
                "Name": settings.glue_database,
                "Description": "Database do esquema estrela classicmodels para a Task 3.",
            }
        )
        print(f"Database criado no Glue: {settings.glue_database}")


def create_all_external_tables() -> None:
    table_scripts = [
        "create_dim_customers.sql",
        "create_dim_products.sql",
        "create_dim_dates.sql",
        "create_dim_countries.sql",
        "create_fact_orders.sql",
    ]

    for filename in table_scripts:
        sql = render_sql_template(read_sql_file(filename))
        print(f"Executando {filename}...")
        athena_execute(sql)
        print(f"OK: {filename}")


def validate_tables() -> pd.DataFrame:
    validation_sql = """
    SELECT 'dim_customers' AS table_name, COUNT(*) AS row_count FROM dim_customers
    UNION ALL
    SELECT 'dim_products' AS table_name, COUNT(*) AS row_count FROM dim_products
    UNION ALL
    SELECT 'dim_dates' AS table_name, COUNT(*) AS row_count FROM dim_dates
    UNION ALL
    SELECT 'dim_countries' AS table_name, COUNT(*) AS row_count FROM dim_countries
    UNION ALL
    SELECT 'fact_orders' AS table_name, COUNT(*) AS row_count FROM fact_orders
    """
    return athena_read(validation_sql)

CREATE EXTERNAL TABLE IF NOT EXISTS {{GLUE_DATABASE}}.dim_customers (
    customer_id INT,
    customer_name STRING,
    contact_name STRING,
    city STRING,
    country STRING
)
STORED AS PARQUET
LOCATION '{{DIM_CUSTOMERS_PATH}}'

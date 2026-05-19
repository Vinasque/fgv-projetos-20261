CREATE EXTERNAL TABLE IF NOT EXISTS {{GLUE_DATABASE}}.dim_products (
    product_id STRING,
    product_name STRING,
    product_line STRING,
    product_vendor STRING
)
STORED AS PARQUET
LOCATION '{{DIM_PRODUCTS_PATH}}'

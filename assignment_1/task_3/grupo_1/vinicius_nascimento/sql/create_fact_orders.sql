CREATE EXTERNAL TABLE IF NOT EXISTS {{GLUE_DATABASE}}.fact_orders (
    order_id INT,
    customer_id INT,
    product_id STRING,
    order_date_key INT,
    country_key INT,
    quantity_ordered INT,
    price_each DOUBLE,
    sales_amount DOUBLE
)
STORED AS PARQUET
LOCATION '{{FACT_ORDERS_PATH}}'

CREATE EXTERNAL TABLE IF NOT EXISTS {{GLUE_DATABASE}}.dim_dates (
    date_key INT,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION '{{DIM_DATES_PATH}}'

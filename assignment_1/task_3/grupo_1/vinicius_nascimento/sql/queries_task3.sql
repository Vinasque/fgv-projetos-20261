-- 4.2 Consulta exploratória em dim_products
SELECT
    product_id,
    product_name,
    product_line,
    product_vendor
FROM dim_products
LIMIT 20;

-- 4.3 Vendas totais por país
SELECT
    dim_countries.country,
    SUM(fact_orders.sales_amount) AS total_sales
FROM fact_orders
JOIN dim_countries
    ON fact_orders.country_key = dim_countries.country_key
GROUP BY dim_countries.country
ORDER BY total_sales DESC
LIMIT 10;

-- 4.4 Base detalhada para dashboard
SELECT
    dim_dates.full_date,
    dim_products.product_line,
    dim_products.product_name,
    dim_countries.country,
    SUM(fact_orders.sales_amount) AS total_sales
FROM fact_orders
JOIN dim_products
    ON fact_orders.product_id = dim_products.product_id
JOIN dim_countries
    ON fact_orders.country_key = dim_countries.country_key
JOIN dim_dates
    ON fact_orders.order_date_key = dim_dates.date_key
GROUP BY
    dim_dates.full_date,
    dim_products.product_line,
    dim_products.product_name,
    dim_countries.country;

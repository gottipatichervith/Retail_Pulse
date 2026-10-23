-- Task A: Product Ranking

SELECT
    product_id,
    SUM(net_amount) AS net_sales,
    ROW_NUMBER() OVER (
        ORDER BY SUM(net_amount) DESC
    ) AS sales_rank
FROM order_items
GROUP BY product_id
ORDER BY net_sales DESC;

SELECT
    product_id,
    SUM(net_amount) AS net_sales,

    ROW_NUMBER() OVER (
        ORDER BY SUM(net_amount) DESC
    ) AS row_number_rank,

    RANK() OVER (
        ORDER BY SUM(net_amount) DESC
    ) AS rank_value,

    DENSE_RANK() OVER (
        ORDER BY SUM(net_amount) DESC
    ) AS dense_rank_value

FROM order_items
GROUP BY product_id
ORDER BY net_sales DESC;

WITH product_sales AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.net_amount) AS net_sales
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.store_id, oi.product_id
)
SELECT
    store_id,
    product_id,
    net_sales,
    RANK() OVER (
        PARTITION BY store_id
        ORDER BY net_sales DESC
    ) AS sales_rank
FROM product_sales
ORDER BY store_id, sales_rank;

WITH product_sales AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.net_amount) AS net_sales
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.store_id, oi.product_id
),
ranked_products AS (
    SELECT
        store_id,
        product_id,
        net_sales,
        RANK() OVER (
            PARTITION BY store_id
            ORDER BY net_sales DESC
        ) AS sales_rank
    FROM product_sales
)
SELECT store_id,product_id,net_sales,sales_rank
FROM ranked_products
WHERE sales_rank <= 3
ORDER BY store_id, sales_rank;

-- Task B: Running Sales Totals
SELECT
    o.order_date,
    SUM(oi.net_amount) AS daily_net_sales,
    SUM(SUM(oi.net_amount)) OVER (
        ORDER BY o.order_date
    ) AS cumulative_net_sales
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.order_date
ORDER BY o.order_date;

SELECT
    o.store_id,
    o.order_date,
    SUM(oi.net_amount) AS daily_net_sales,
    SUM(SUM(oi.net_amount)) OVER (
        PARTITION BY o.store_id
        ORDER BY o.order_date
    ) AS cumulative_net_sales
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.store_id, o.order_date
ORDER BY o.store_id, o.order_date;

-- Task C: Month-over-Month Sales
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS sales_month,
        SUM(oi.net_amount) AS net_sales
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY sales_month
)
SELECT
    sales_month,
    net_sales,
    LAG(net_sales) OVER (
        ORDER BY sales_month
    ) AS previous_month_sales
FROM monthly_sales
ORDER BY sales_month;

WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS sales_month,
        SUM(oi.net_amount) AS net_sales
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY sales_month
),
monthly_comparison AS (
    SELECT
        sales_month,
        net_sales,
        LAG(net_sales) OVER (
            ORDER BY sales_month
        ) AS previous_month_sales
    FROM monthly_sales
)
SELECT
    sales_month,
    net_sales,
    previous_month_sales,
    net_sales - previous_month_sales AS absolute_change,
    CASE
        WHEN previous_month_sales IS NULL
             OR previous_month_sales = 0
        THEN NULL
        ELSE
            (net_sales - previous_month_sales)
            * 100.0 / previous_month_sales
    END AS percentage_change
FROM monthly_comparison
ORDER BY sales_month;

-- Task D: Product Performance
WITH product_sales AS (
    SELECT
        product_id,
        SUM(net_amount) AS net_sales
    FROM order_items
    GROUP BY product_id
)

SELECT
    product_id,
    net_sales,
    ROUND(
        net_sales * 100.0
        / SUM(net_sales) OVER (),
        2
    ) AS contribution_percentage
FROM product_sales
ORDER BY net_sales DESC;

WITH product_sales AS (
    SELECT
        product_id,
        SUM(net_amount) AS net_sales
    FROM order_items
    GROUP BY product_id
),
product_contribution AS (
    SELECT
        product_id,
        net_sales,
        net_sales * 100.0
            / SUM(net_sales) OVER () AS contribution_percentage
    FROM product_sales
),
product_cumulative AS (
    SELECT
        product_id,
        net_sales,
        contribution_percentage,
        SUM(contribution_percentage) OVER (
            ORDER BY net_sales DESC
        ) AS cumulative_percentage
    FROM product_contribution
)

SELECT
    product_id,
    net_sales,
    ROUND(contribution_percentage, 2) AS contribution_percentage,
    ROUND(cumulative_percentage, 2) AS cumulative_percentage
FROM product_cumulative
ORDER BY net_sales DESC;


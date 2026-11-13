
-- RetailPulse Week 3
-- Create daily product-store demand dataset

DROP VIEW IF EXISTS v_forecasting_daily_sales;

CREATE VIEW v_forecasting_daily_sales AS

WITH RECURSIVE date_calendar(sales_date) AS (

    SELECT MIN(order_date)
    FROM orders
    WHERE status = 'Completed'

    UNION ALL

    SELECT DATE(sales_date, '+1 day')
    FROM date_calendar
    WHERE sales_date < (
        SELECT MAX(order_date)
        FROM orders
        WHERE status = 'Completed'
    )
),

daily_sales AS (

    SELECT
        o.order_date AS sales_date,
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS daily_quantity

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.status = 'Completed'

    GROUP BY
        o.order_date,
        o.store_id,
        oi.product_id
)

SELECT
    dc.sales_date,
    i.product_id,
    i.store_id,
    COALESCE(ds.daily_quantity, 0) AS daily_quantity

FROM date_calendar dc

CROSS JOIN inventory i

LEFT JOIN daily_sales ds
    ON ds.sales_date = dc.sales_date
    AND ds.product_id = i.product_id
    AND ds.store_id = i.store_id

ORDER BY
    dc.sales_date,
    i.store_id,
    i.product_id;

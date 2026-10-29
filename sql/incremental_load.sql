-- RetailPulse
-- Use Case 8: Pipeline Automation & Incremental Loading
--
-- Purpose:
-- SQL statements used by the pipeline to identify existing
-- order-item records and support incremental insert/update logic.
--
-- Business key:
--     order_id + product_id
--
-- Why?
--     An order can contain multiple products, so order_id alone
--     must not be treated as the unique order-item key.

-- ============================================================
-- 1. Find an existing order item
-- ============================================================
-- Used by the Python pipeline to check whether a record already
-- exists in the database.

SELECT
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    gross_amount,
    net_amount
FROM order_items
WHERE order_id = ?
  AND product_id = ?;


-- ============================================================
-- 2. Insert a new order item
-- ============================================================
-- Used when the business key does not already exist.

INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    gross_amount,
    net_amount
)
VALUES (?, ?, ?, ?, ?, ?, ?);


-- ============================================================
-- 3. Update an existing order item
-- ============================================================
-- Used when the business key already exists but one or more
-- values have changed.

UPDATE order_items
SET
    quantity = ?,
    unit_price = ?,
    discount = ?,
    gross_amount = ?,
    net_amount = ?
WHERE order_id = ?
  AND product_id = ?;


-- ============================================================
-- 4. Check whether the incoming record is identical
-- ============================================================
-- If all values match the existing database record,
-- the pipeline can safely skip the record.

SELECT COUNT(*) AS identical_record
FROM order_items
WHERE order_id = ?
  AND product_id = ?
  AND quantity = ?
  AND unit_price = ?
  AND discount = ?
  AND gross_amount = ?
  AND net_amount = ?;


-- ============================================================
-- 5. Count order items
-- ============================================================
-- Useful for validation after incremental loading.

SELECT COUNT(*) AS total_order_items
FROM order_items;


-- ============================================================
-- 6. Check for duplicate business keys
-- ============================================================
-- There should be no duplicate order_id + product_id combinations
-- in the database because this combination is the primary key.

SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
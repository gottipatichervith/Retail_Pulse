CREATE TABLE order_items (
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    discount REAL NOT NULL CHECK (discount >= 0),
    gross_amount REAL NOT NULL CHECK (gross_amount >= 0),
    net_amount REAL NOT NULL CHECK (net_amount >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
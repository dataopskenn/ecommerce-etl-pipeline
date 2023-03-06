DROP TABLE IF EXISTS user_staging.orders;
CREATE TABLE  user_staging.orders(
    order_id                BIGINT NOT NULL CONSTRAINT orders_pk PRIMARY KEY,
    customer_id             BIGINT NOT NULL,
    order_date              DATE NOT NULL,
    product_id              BIGINT NOT NULL,
    unit_price              BIGINT NOT NULL,
    quantity                BIGINT NOT NULL,
    total_price             BIGINT NOT NULL
    --CONSTRAINT product_fk FOREIGN KEY (product_id) REFERENCES user_staging.reviews (product_id)
    -- This key could not be created because the product_id key is not unique in this table
);

INSERT INTO user_staging.orders(
	order_id, customer_id, order_date, product_id, unit_price, quantity, total_price
)
VALUES (
    s, s, s, s, s, s, s
);
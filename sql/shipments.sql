DROP TABLE IF EXISTS username_staging.shipment_deliveries;
CREATE TABLE username_staging.shipment_deliveries (
    shipment_id BIGINT CONSTRAINT shipment_pk PRIMARY KEY,
    order_id                BIGINT,
    shipment_date           DATE,
    delivery_date           DATE,
    CONSTRAINT orders_fk FOREIGN KEY (order_id) REFERENCES username_staging.orders (order_id)
);
    -- The below part of this query could not be executed as a result of data quality issues. 
    -- The SQLAlchemy module of python was used to do this insertion as a result of psycopg2's failure due to data quality issues
    --INSERT INTO username_staging.shipment_deliveries(
	--shipment_id, order_id, shipment_date, delivery_date)
	--VALUES(%s, %s, %s, %s)

    --ALTER TABLE username_staging.shipment_deliveries ALTER COLUMN shipment_date TYPE DATE,
    --ALTER COLUMN delivery_date TYPE DATE;
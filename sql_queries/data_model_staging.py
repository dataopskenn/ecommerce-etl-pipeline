"""
-- =======================================================================================
-- Description:	ALTER Order Table Query
-- =======================================================================================
"""

orders_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_staging.orders
        ALTER COLUMN order_id TYPE BIGINT USING order_id::BIGINT,
        ADD CONSTRAINT order_date_dt_fk FOREIGN KEY (order_date) REFERENCES user_staging.dim_dates (calendar_dt)--,
        --ADD CONSTRAINT product_fk FOREIGN KEY (product_id) REFERENCES user_staging.dim_products (product_id),
        --ADD CONSTRAINT customer_fk FOREIGN KEY (customer_id) REFERENCES user_staging.dim_customers (customer_id);

    """
)


"""
-- =======================================================================================
-- Description:	ALTER Reviews Table Query
-- =======================================================================================
"""

reviews_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_staging.reviews
        --ADD CONSTRAINT product_fk FOREIGN KEY (product_id) REFERENCES user_staging.dim_products (product_id)

    """
)


"""
-- =======================================================================================
-- Description:	ALTER Shipment Table Query
-- =======================================================================================
"""

shipments_table_model = (
    
    """
    ALTER TABLE user_staging.shipment_deliveries
        ADD CONSTRAINT shipment_pk PRIMARY KEY (shipment_id),
        --ALTER COLUMN shipment_id        TYPE BIGINT USING shipment_id::BIGINT,
        --ALTER COLUMN order_id           TYPE BIGINT USING order_id::BIGINT,
        --ALTER COLUMN shipment_date      TYPE DATE USING shipment_date::DATE,
        --ALTER COLUMN delivery_date      TYPE DATE USING delivery_date::DATE,
        ADD CONSTRAINT order_fk FOREIGN KEY (order_id) REFERENCES user_staging.orders (order_id),
        ADD CONSTRAINT shipment_date_dt_fk FOREIGN KEY (shipment_date) REFERENCES user_staging.dim_dates (calendar_dt),
        ADD CONSTRAINT delivery_date_dt_fk FOREIGN KEY (delivery_date) REFERENCES user_staging.dim_dates (calendar_dt)

    """
)


"""
-- =======================================================================================
-- Description:	ALTER dim_dates Table Query
-- =======================================================================================
"""

dim_dates_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_staging.dim_dates

    """
)


dim_customers_table_model = (

    """
    ALTER TABLE IF EXISTS user_staging.dim_customers
        --ADD CONSTRAINT postal_code_fk FOREIGN KEY (postal_code) REFERENCES user_staging.dim_addresses (postal_code)

    """
)


"""
-- =======================================================================================
-- Description:	ALTER dim_addresses Table Query
-- =======================================================================================
"""

dim_addresses_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_staging.dim_addresses

    """
)


"""
-- =======================================================================================
-- Description:	ALTER dim_products Table Query
-- =======================================================================================
"""

dim_products_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_staging.dim_products

    """
)



staging_data_model_queries = [
    orders_table_model,
    # reviews_table_model,
    shipments_table_model,
    # dim_dates_table_model
    # dim_customers_table_model,
    # dim_addresses_table_model,
    # dim_products_table_model
]
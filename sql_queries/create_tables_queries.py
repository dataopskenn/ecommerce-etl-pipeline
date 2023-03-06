"""
-- =======================================================================================
-- Description:	CREATE Order Table Queries
-- =======================================================================================
"""

orders_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.orders
    (
        order_id                BIGINT NOT NULL CONSTRAINT orders_pk PRIMARY KEY,
        customer_id             BIGINT NOT NULL, --REFERENCES user_staging.dim_customers (customer_id),
        order_date              DATE NOT NULL, --REFERENCES user_staging.dim_dates (calendar_dt),
        product_id              BIGINT NOT NULL, -- REFERENCES user_staging.dim_products (product_id),
        unit_price              BIGINT NOT NULL,
        quantity                BIGINT NOT NULL,
        total_price             BIGINT NOT NULL
    )
    
    """
)


"""
-- =======================================================================================
-- Description:	CREATE Reviews Table Queries
-- =======================================================================================
"""

reviews_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.reviews
    (
        review                  BIGINT NOT NULL,
        product_id              BIGINT NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE Shipment Table Queries
-- =======================================================================================
"""

shipments_table = (
    
    """
    CREATE TABLE user_staging.shipment_deliveries 
    (
        shipment_id             BIGINT CONSTRAINT shipment_pk PRIMARY KEY,
        order_id                BIGINT REFERENCES user_staging.orders (order_id),
        shipment_date           TEXT,
        delivery_date           TEXT
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE dim_dates Table Queries
-- =======================================================================================
"""

dim_dates_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.dim_dates
    (
        calendar_dt              DATE NOT NULL CONSTRAINT dim_dates_pk PRIMARY KEY,
        year_num                 BIGINT NOT NULL,
        month_of_the_year_num    BIGINT NOT NULL,
        day_of_month_num         BIGINT NOT NULL,
        day_of_week_num          BIGINT NOT NULL,
        weekend_indr             BOOLEAN NOT NULL,
        public_holiday           BOOLEAN NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE dim_customers Table Queries
-- =======================================================================================
"""

dim_customers_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.dim_customers
    (
        customer_id                    BIGINT NOT NULL CONSTRAINT customer_pk PRIMARY KEY,
        customer_name                  TEXT NOT NULL,
        postal_code                    BIGINT NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE dim_addresses Table Queries
-- =======================================================================================
"""

dim_addresses_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.dim_addresses
    (
        postal_code                 BIGINT NOT NULL CONSTRAINT postal_code_pk PRIMARY KEY,
        country                     TEXT NOT NULL,
        region                      TEXT NOT NULL,
        state                       TEXT NOT NULL,
        address                     TEXT NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE dim_products Table Queries
-- =======================================================================================
"""

dim_products_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_staging.dim_products
    (
        product_id                   BIGINT NOT NULL CONSTRAINT product_pk PRIMARY KEY,
        product_category             TEXT NOT NULL,
        product_name                 BIGINT NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE agg_public_holiday Table Queries
-- =======================================================================================
"""


agg_public_holiday_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_analytics.agg_public_holiday
    (
        ingestion_date            DATE NOT NULL,
        tt_order_hol_jan          BIGINT NOT NULL,
        tt_order_hol_feb          BIGINT NOT NULL,
        tt_order_hol_mar          BIGINT NOT NULL,
        tt_order_hol_apr          BIGINT NOT NULL,
        tt_order_hol_may          BIGINT NOT NULL,
        tt_order_hol_jun          BIGINT NOT NULL,
        tt_order_hol_jul          BIGINT NOT NULL,
        tt_order_hol_aug          BIGINT NOT NULL,
        tt_order_hol_sep          BIGINT NOT NULL,
        tt_order_hol_oct          BIGINT NOT NULL,
        tt_order_hol_nov          BIGINT NOT NULL,
        tt_order_hol_dec          BIGINT NOT NULL
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE agg_shipments Table Queries
-- =======================================================================================
"""

agg_shipments_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_analytics.agg_shipments
    (
        ingestion_date              DATE NOT NULL,
        tt_late_shipments           BIGINT,
        tt_undelivered_items        BIGINT
    )

    """
)


"""
-- =======================================================================================
-- Description:	CREATE best_performing_product Table Queries
-- =======================================================================================
"""

best_performing_product_table = (
    
    """
    CREATE TABLE IF NOT EXISTS user_analytics.best_performing_product
    (
    product_id                TEXT NOT NULL,
    ingestion_date              DATE NOT NULL,
    most_ordered_day            DATE NOT NULL,
    is_public_holiday           BOOLEAN NOT NULL,
    tt_review_points            BIGINT NOT NULL,
    pct_one_star_review         DOUBLE PRECISION NOT NULL,
    pct_two_star_review         DOUBLE PRECISION NOT NULL,
    pct_three_star_review       DOUBLE PRECISION NOT NULL,
    pct_four_star_review        DOUBLE PRECISION NOT NULL,
    pct_five_star_review        DOUBLE PRECISION NOT NULL,
    pct_early_shipments         DOUBLE PRECISION NOT NULL,
    pct_late_shipments          DOUBLE PRECISION NOT NULL,
    pct_undelivered_items       DOUBLE PRECISION NOT NULL
    )

    """
)


create_queries = [
    orders_table,
    reviews_table,
    shipments_table,
    dim_dates_table,
    agg_public_holiday_table,
    agg_shipments_table,
    best_performing_product_table,
    dim_customers_table,
    dim_addresses_table,
    dim_products_table
]
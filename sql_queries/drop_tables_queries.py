"""
-- =======================================================================================
-- Description:	DROP Order Table Queries
-- =======================================================================================
"""

drop_orders_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.orders CASCADE
    
    """
)


"""
-- =======================================================================================
-- Description:	DROP Reviews Table Queries
-- =======================================================================================
"""

drop_reviews_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.reviews CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP Shipment Table Queries
-- =======================================================================================
"""

drop_shipments_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.shipment_deliveries CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP dim_dates Table Queries
-- =======================================================================================
"""

drop_dim_dates_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.dim_dates CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP dim_customers Table Queries
-- =======================================================================================
"""

drop_dim_customers_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.dim_customers CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP dim_addresses Table Queries
-- =======================================================================================
"""

drop_dim_addresses_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.dim_addresses CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP dim_products Table Queries
-- =======================================================================================
"""

drop_dim_products_table = (
    
    """
    DROP TABLE IF EXISTS user_staging.dim_products CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP agg_public_holiday Table Queries
-- =======================================================================================
"""


drop_agg_public_holiday_table = (
    
    """
    DROP TABLE IF EXISTS user_analytics.agg_public_holiday CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP agg_shipments Table Queries
-- =======================================================================================
"""

drop_agg_shipments_table = (
    
    """
    DROP TABLE IF EXISTS user_analytics.agg_shipments CASCADE

    """
)


"""
-- =======================================================================================
-- Description:	DROP best_performing_product Table Queries
-- =======================================================================================
"""

drop_best_performing_product_table = (
    
    """
    DROP TABLE IF EXISTS user_analytics.best_performing_product CASCADE

    """
)


drop_queries = [
    drop_orders_table,
    drop_reviews_table,
    drop_shipments_table,
    drop_dim_dates_table,
    drop_dim_customers_table,
    drop_dim_addresses_table,
    drop_dim_products_table,
    drop_agg_public_holiday_table,
    drop_agg_shipments_table,
    drop_best_performing_product_table
]
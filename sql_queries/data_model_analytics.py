"""
-- =======================================================================================
-- Description:	ALTER agg_public_holiday Table Queries
-- =======================================================================================
"""


agg_public_holiday_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_analytics.agg_public_holiday
        ADD CONSTRAINT holiday_date_fk FOREIGN KEY (ingestion_date) REFERENCES user_staging.dim_dates (calendar_dt)

    """
)


"""
-- =======================================================================================
-- Description:	ALTER agg_shipments Table Queries
-- =======================================================================================
"""

agg_shipments_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_analytics.agg_shipments
        ADD CONSTRAINT agg_shipments_date_fk FOREIGN KEY (ingestion_date) REFERENCES user_staging.dim_dates (calendar_dt)

    """
)


"""
-- =======================================================================================
-- Description:	ALTER best_performing_product Table Queries
-- =======================================================================================
"""

best_performing_product_table_model = (
    
    """
    ALTER TABLE IF EXISTS user_analytics.best_performing_product
        --ADD CONSTRAINT bppt_product_fk FOREIGN KEY (product_name) REFERENCES user_staging.dim_products (product_name)
        ADD CONSTRAINT bppt_date_fk FOREIGN KEY (ingestion_date) REFERENCES user_staging.dim_dates (calendar_dt),
        ADD CONSTRAINT bppt_most_ordered_date_fk FOREIGN KEY (most_ordered_day) REFERENCES user_staging.dim_dates (calendar_dt)

    """
)


analytics_data_model_queries = [
    agg_public_holiday_table_model,
    agg_shipments_table_model,
    best_performing_product_table_model
]
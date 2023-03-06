"""
-- =======================================================================================
-- Description:	CREATE agg_shipments Table Queries
-- =======================================================================================
"""

agg_shipments_table = (
    """
    --DROP TABLE IF EXISTS user_analytics.agg_shipments;
    CREATE TABLE IF NOT EXISTS user_analytics.agg_shipments
    (
        ingestion_date              DATE NOT NULL,
        tt_late_shipments           BIGINT NOT NULL,
        tt_undelivered_items        BIGINT NOT NULL
    );

    INSERT INTO user_analytics.agg_shipments
    WITH large_ship AS (SELECT *
						FROM user_staging.orders as o
						LEFT JOIN user_staging.shipment_deliveries AS ship
					 	ON o.order_id = ship.order_id)
    SELECT 
        CURRENT_DATE AS ingestion_date,
        (SELECT 
        COUNT(*) 
        FROM large_ship 
        WHERE EXTRACT(DAY FROM shipment_date - order_date) >= 6 
        AND delivery_date IS NULL) AS tt_late_shipments,
        (SELECT 
        COUNT(*) 
        FROM large_ship 
        WHERE EXTRACT (DAY FROM NOW() - order_date) >= 15 
        AND delivery_date IS NULL 
        AND shipment_date IS NULL) AS tt_undelivered_items;
    """)

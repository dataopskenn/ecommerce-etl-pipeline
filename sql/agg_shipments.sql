-- =======================================================================================
-- Description:	CREATE agg_shipments Table Queries
-- =======================================================================================

DROP TABLE IF EXISTS user_analytics.agg_shipments;
CREATE TABLE IF NOT EXISTS user_analytics.agg_shipments(
    ingestion_date              DATE NOT NULL,
    tt_late_shipments           BIGINT NOT NULL,
    tt_undelivered_items        BIGINT NOT NULL
    );

INSERT INTO user_analytics.agg_shipments
    WITH large_ship AS (
	SELECT *
	FROM user_staging.orders as o
	LEFT JOIN user_staging.shipment_deliveries AS ship
	ON o.order_id = ship.order_id),
	late_df AS(
	SELECT
		foo.order_date,
		COUNT(*) AS tt_late_shipments
	FROM (SELECT
			order_date,
			COUNT(*) AS late_shipments
		FROM large_ship 
		WHERE EXTRACT(DAY FROM shipment_date - order_date) >= 6 AND delivery_date IS NULL
		GROUP BY order_date) AS foo
	GROUP BY order_date
	ORDER BY foo.order_date),
	undelivered_df AS (
	SELECT
		fooo.order_date,
		COUNT(*) AS tt_undelivered_items
	FROM (SELECT
			order_date,
			COUNT(*) 
		FROM large_ship 
		WHERE EXTRACT (DAY FROM NOW() - order_date) >= 15
		AND delivery_date IS NULL AND shipment_date IS NULL
		GROUP BY order_date) AS fooo
	GROUP BY order_date
	ORDER BY fooo.order_date)
    SELECT 
        udf.order_date AS ingestion_date,
        ldf.tt_late_shipments,
        udf.tt_undelivered_items
    FROM undelivered_df udf
    LEFT JOIN late_df ldf ON udf.order_date = ldf.order_date;
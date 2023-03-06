"""
-- =======================================================================================
-- Description:	CREATE best_performing_product Table Queries
-- =======================================================================================
"""

best_performing_product_table = (
       """
	--DROP TABLE IF EXISTS user_analytics.best_performing_product;
    CREATE TABLE IF NOT EXISTS user_analytics.best_performing_product
    (
    product_name                TEXT NOT NULL,
    ingestion_date              DATE NOT NULL,
    most_ordered_day            DATE NOT NULL,
    is_public_holiday           BOOLEAN NOT NULL,
    tt_review_points            BIGINT,
    pct_one_star_review         DOUBLE PRECISION,
    pct_two_star_review         DOUBLE PRECISION,
    pct_three_star_review       DOUBLE PRECISION,
    pct_four_star_review        DOUBLE PRECISION,
    pct_five_star_review        DOUBLE PRECISION,
    pct_early_shipments         DOUBLE PRECISION,
    pct_late_shipments          DOUBLE PRECISION,
    pct_undelivered_items       DOUBLE PRECISION
    );

    INSERT INTO  user_analytics.best_performing_product
    WITH large_ship AS (
	SELECT *
	FROM user_staging.orders AS o
	LEFT JOIN user_staging.shipment_deliveries AS ship
	ON o.order_id = ship.order_id),
	shipments AS (
		SELECT
			CURRENT_DATE AS ingestion_date,
			ROUND(tt_late_shipments/total_shipments::NUMERIC,4)*100 As pct_late_shipments,				  
			ROUND(tt_early_shipments/total_shipments::NUMERIC,4)*100 AS pct_early_shipments,				  
			ROUND(tt_undelivered_items/total_shipments::NUMERIC,4)*100 AS pct_undelivered_items
		FROM(SELECT(
				SELECT COUNT(*) FROM large_ship) AS total_shipments,
				(SELECT COUNT(*) FROM large_ship WHERE EXTRACT(DAY FROM shipment_date - order_date) >= 6 
				AND delivery_date IS NULL) AS tt_late_shipments,
				(SELECT COUNT(*) FROM large_ship WHERE EXTRACT(DAY FROM shipment_date - order_date) < 6) AS tt_early_shipments,
				(SELECT COUNT(*) FROM large_ship WHERE EXTRACT (DAY FROM NOW() - order_date) >= 15 AND delivery_date IS NULL 
				AND shipment_date IS NULL) AS tt_undelivered_items
				GROUP BY tt_late_shipments, tt_early_shipments) AS foo
		ORDER BY pct_late_shipments, pct_early_shipments, pct_undelivered_items),
 	pct AS (
	SELECT
		product_id,
		tt_reviews,
		ROUND(tt_one_star_review/tt_reviews::NUMERIC,4)*100 AS pct_tt_one_star_review,
		ROUND(tt_two_star_review/tt_reviews::NUMERIC,4)*100 AS pct_tt_two_star_review,
		ROUND(tt_three_star_review/tt_reviews::NUMERIC,4)*100 AS pct_tt_three_star_review,
		ROUND(tt_four_star_review/tt_reviews::NUMERIC,4)*100 AS pct_tt_four_star_review,
		ROUND(tt_five_star_review/tt_reviews::NUMERIC,4)*100 AS pct_tt_five_star_review
	FROM(SELECT 
		 	DISTINCT(r.product_id) AS product_id,
			SUM(r.review) AS tt_review_points,
			COUNT(*) as tt_reviews,
			SUM(CASE WHEN r.review = 1 THEN 1 ELSE 0 END) tt_one_star_review,
			SUM(CASE WHEN r.review = 2 THEN 1 ELSE 0 END) tt_two_star_review,
			SUM(CASE WHEN r.review = 3 THEN 1 ELSE 0 END) tt_three_star_review,
			SUM(CASE WHEN r.review = 4 THEN 1 ELSE 0 END) tt_four_star_review,
			SUM(CASE WHEN r.review = 5 THEN 1 ELSE 0 END) tt_five_star_review
		FROM user_staging.reviews r
		GROUP BY product_id) AS pct_reviews_table
	ORDER BY product_id
),
	product AS (
	SELECT 
		DISTINCT(o.product_id) AS product_id,
		CURRENT_DATE AS ingestion_date,
		o.order_date AS most_ordered_date,
		d.public_holiday AS is_public_holiday
	FROM user_staging.orders o
	LEFT JOIN user_staging.dim_dates d ON d.calendar_dt = o.order_date
	GROUP BY o.product_id, most_ordered_date, is_public_holiday
	HAVING MAX(o.quantity) = (SELECT MAX(o.quantity) FROM user_staging.orders o)
)
SELECT 
	product.product_id,
	product.ingestion_date,
	most_ordered_date,
	is_public_holiday,
	tt_reviews,
	pct_tt_one_star_review,
	pct_tt_two_star_review,
	pct_tt_three_star_review,
	pct_tt_four_star_review,
	pct_tt_five_star_review,
	pct_early_shipments,
	pct_late_shipments,
	pct_undelivered_items
FROM product
LEFT JOIN pct ON pct.product_id = product.product_id
LEFT JOIN shipments ON shipments.ingestion_date = product.ingestion_date
    """)

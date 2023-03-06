"""
-- =======================================================================================
-- Description:	INSERT INTO Order Table Queries
-- =======================================================================================
"""

insert_orders_table = (
    
    """
    INSERT INTO user_staging.orders
    (
	    order_id, customer_id, order_date, product_id, unit_price, quantity, total_price
    )
    VALUES 
    (
        %s, %s, %s, %s, %s, %s, %s
    )
    
    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO Reviews Table Queries
-- =======================================================================================
"""

insert_reviews_table = (
    
    """
    INSERT INTO user_staging.reviews
    (
	    review, product_id
    )
    VALUES
    (
        %s, %s
    )

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO Shipment Table Queries
-- =======================================================================================
"""

insert_shipments_table = (
    
    """
    INSERT INTO user_staging.shipment_deliveries 
    (
        shipment_id, order_id, shipment_date, delivery_date
    )
	VALUES
    (
        %s, %s, %s, %s
    )

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO dim_customers Table Queries
-- =======================================================================================
"""

insert_dim_customers_table = (
    
    """
    INSERT INTO user_staging.dim_customers 
    (
        customer_id, customer_name, postal_code
    )
	VALUES
    (
        %s, %s, %s
    )

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO dim_addresses Table Queries
-- =======================================================================================
"""

insert_dim_addresses_table = (
    
    """
    INSERT INTO user_staging.dim_addresses 
    (
        postal_code, country, region, state, address
    )
	VALUES
    (
        %s, %s, %s, %s
    )

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO dim_products Table Queries
-- =======================================================================================
"""

insert_dim_products_table = (
    
    """
    INSERT INTO user_staging.dim_customers 
    (
        product_id, product_category, product_name
    )
	VALUES
    (
        %s, %s, %s
    )

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO dim_dates Table Queries
-- =======================================================================================
"""

insert_dim_dates_table = (
    
    """
    INSERT INTO user_staging.dim_dates
    SELECT 
       datum AS calendar_dt,
       EXTRACT(YEAR FROM datum) AS year_num,
       EXTRACT(MONTH FROM datum) AS month_of_the_year_num,
       EXTRACT(DAY FROM datum) AS day_of_month_num,
       EXTRACT(ISODOW FROM datum) AS day_of_week_num,
       CASE
           WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE
           ELSE FALSE
           END AS weekend_indr,
        CASE
        WHEN EXTRACT(MONTH FROM datum) = 1 AND EXTRACT(DAY FROM datum) = 1 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum+1) = 1 AND EXTRACT(DAY FROM datum) = 1 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 10 AND EXTRACT(DAY FROM datum) = 1 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 12 AND EXTRACT(DAY FROM datum) = 24 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 12 AND EXTRACT(DAY FROM datum) = 25 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 12 AND EXTRACT(DAY FROM datum) = 26 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 12 AND EXTRACT(DAY FROM datum) = 31 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 5 AND EXTRACT(DAY FROM datum) = 29 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 6 AND EXTRACT(DAY FROM datum) = 12 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 5 AND EXTRACT(DAY FROM datum) = 1 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5) 
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 4 AND EXTRACT(DAY FROM datum) = 2 AND EXTRACT(YEAR FROM datum) = 2021 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 4 AND EXTRACT(DAY FROM datum) = 5 AND EXTRACT(YEAR FROM datum) = 2021 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 4 AND EXTRACT(DAY FROM datum) = 15 AND EXTRACT(YEAR FROM datum) = 2022 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 4 AND EXTRACT(DAY FROM datum) = 18 AND EXTRACT(YEAR FROM datum) = 2022 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 7 AND EXTRACT(DAY FROM datum) = 20 AND EXTRACT(YEAR FROM datum) = 2021 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        WHEN EXTRACT(MONTH FROM datum) = 7 AND EXTRACT(DAY FROM datum) = 10 AND EXTRACT(YEAR FROM datum) = 2022 AND EXTRACT(ISODOW FROM datum) IN (1, 2, 3, 4, 5)
            THEN TRUE
        ELSE FALSE
        END as public_holiday

    FROM (SELECT '2021-01-01'::DATE + SEQUENCE.DAY AS datum
        FROM GENERATE_SERIES(0, 29219) AS SEQUENCE (DAY)
        GROUP BY SEQUENCE.DAY) DQ
    ORDER BY 1;

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO agg_public_holiday Table Queries
-- =======================================================================================
"""


insert_agg_public_holiday_table = (
    
    """
    INSERT INTO user_analytics.agg_public_holiday
    WITH large_order AS (
        SELECT *
        FROM user_staging.orders as o
        LEFT JOIN user_staging.dim_dates AS dim ON o.order_date = dim.calendar_dt)
    SELECT 
    CURRENT_DATE AS ingestion_date,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 1 AND public_holiday = true) As tt_order_hol_jan,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 2 AND public_holiday = true) AS tt_order_hol_feb,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 3 AND public_holiday = true) AS tt_order_hol_mar,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 4 AND public_holiday = true) AS tt_order_hol_apr,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 5 AND public_holiday = true) AS tt_order_hol_may,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 6 AND public_holiday = true) AS tt_order_hol_jun,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 7 AND public_holiday = true) AS tt_order_hol_jul,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 8 AND public_holiday = true) AS tt_order_hol_aug,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 9 AND public_holiday = true) AS tt_order_hol_sep,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 10 AND public_holiday = true) AS tt_order_hol_oct,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 11 AND public_holiday = true) AS tt_order_hol_nov,
    (SELECT 
        COUNT(*) 
        FROM large_order 
        WHERE month_of_the_year_num = 12 AND public_holiday = true) AS tt_order_hol_dec;

    --FROM (SELECT '2021-01-01'::DATE + SEQUENCE.DAY AS datum
    --    FROM GENERATE_SERIES(0, 29219) AS SEQUENCE (DAY)
    --    GROUP BY SEQUENCE.DAY) DQ
    --ORDER BY 1;

    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO agg_shipments Table Queries
-- Modify this table to show data ordered by the order_date and not the NOW()
-- =======================================================================================
"""

insert_agg_shipments_table = (
    
    """
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
    LEFT JOIN late_df ldf ON udf.order_date = ldf.order_date


    """
)


"""
-- =======================================================================================
-- Description:	INSERT INTO best_performing_product Table Queries
-- =======================================================================================
"""

insert_best_performing_product_table = (
    
    """
    INSERT INTO  user_analytics.best_performing_product
WITH large_ship AS (
    SELECT *
	FROM user_staging.orders AS o
	LEFT JOIN user_staging.shipment_deliveries AS ship
	ON o.order_id = ship.order_id),
    shipments AS (
        SELECT
			CURRENT_DATE AS ingestion_date,
			ROUND(
				tt_late_shipments/total_shipments::NUMERIC,4
				)*100 As pct_late_shipments,				  
			ROUND(
				tt_early_shipments/total_shipments::NUMERIC,4
				)*100 AS pct_early_shipments,				  
			ROUND(
				tt_undelivered_items/total_shipments::NUMERIC,4
				)*100 AS pct_undelivered_items
		FROM(SELECT(
				SELECT COUNT(*) FROM large_ship) AS total_shipments,
				(SELECT COUNT(*) FROM large_ship 
				WHERE EXTRACT(DAY FROM shipment_date - order_date) >= 6 
				AND delivery_date IS NULL) AS tt_late_shipments,
				(SELECT COUNT(*) FROM large_ship 
				WHERE EXTRACT(DAY FROM shipment_date - order_date) < 6) AS tt_early_shipments,
				(SELECT COUNT(*) FROM large_ship 
				WHERE EXTRACT (DAY FROM NOW() - order_date) >= 15 AND delivery_date IS NULL 
				AND shipment_date IS NULL) AS tt_undelivered_items
				GROUP BY tt_late_shipments, tt_early_shipments) AS foo
		ORDER BY pct_late_shipments, pct_early_shipments, pct_undelivered_items),
 	pct AS (
        SELECT
        product_id,
		tt_reviews,
		ROUND(
			tt_one_star_review/tt_reviews::NUMERIC,4
			)*100 AS pct_tt_one_star_review,
		ROUND(
			tt_two_star_review/tt_reviews::NUMERIC,4
			)*100 AS pct_tt_two_star_review,
		ROUND(
			tt_three_star_review/tt_reviews::NUMERIC,4
			)*100 AS pct_tt_three_star_review,
		ROUND(
			tt_four_star_review/tt_reviews::NUMERIC,4
			)*100 AS pct_tt_four_star_review,
		ROUND(
			tt_five_star_review/tt_reviews::NUMERIC,4
			)*100 AS pct_tt_five_star_review
	FROM(SELECT 
		 	DISTINCT(r.product_id) AS product_id,
			SUM(r.review) AS tt_review_points,
			COUNT(*) as tt_reviews,
			SUM(
				CASE WHEN r.review = 1 
				THEN 1 ELSE 0 END) tt_one_star_review,
			SUM(
				CASE WHEN r.review = 2 
				THEN 1 ELSE 0 END) tt_two_star_review,
			SUM(
				CASE WHEN r.review = 3 
				THEN 1 ELSE 0 END) tt_three_star_review,
			SUM(
				CASE WHEN r.review = 4 
				THEN 1 ELSE 0 END) tt_four_star_review,
			SUM(
				CASE WHEN r.review = 5 
				THEN 1 ELSE 0 END) tt_five_star_review
		FROM user_staging.reviews r
		GROUP BY product_id) AS pct_reviews_table
	ORDER BY product_id),
	product AS (
	SELECT 
		DISTINCT(o.product_id) AS product_id,
		CURRENT_DATE AS ingestion_date,
		o.order_date AS most_ordered_date,
		d.public_holiday AS is_public_holiday
	FROM user_staging.orders o
	LEFT JOIN user_staging.dim_dates d ON d.calendar_dt = o.order_date
	GROUP BY o.product_id, most_ordered_date, is_public_holiday
	HAVING MAX(o.quantity) = (SELECT MAX(o.quantity) FROM user_staging.orders o))
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

    """
)

export_public_holiday_to_s3 = (

    """
    SELECT * 
    FROM aws_s3.query_export_to_s3('SELECT * FROM user_analytics.agg_public_holiday', 
    aws_commons.create_s3_uri(
        'd2b-internal-assessment-bucket', 
        'analytics_export/user/agg_public_holiday.csv', 
        'eu-central-1', options :='format csv, HEADER true')
   );
    """
)

export_best_performing_product_to_s3 = (

    """
    SELECT * 
    FROM aws_s3.query_export_to_s3('SELECT * FROM user_analytics.best_performing_product.csv', 
    aws_commons.create_s3_uri(
        'd2b-internal-assessment-bucket', 
        'analytics_export/user/best_performing_product.csv', 
        'eu-central-1', options :='format csv, HEADER true')
   );
    """
)

export_agg_shipments_to_s3 = (

    """
    SELECT * 
    FROM aws_s3.query_export_to_s3('SELECT * FROM user_analytics.agg_shipments', 
    aws_commons.create_s3_uri(
        'd2b-internal-assessment-bucket', 
        'analytics_export/user/agg_shipments.csv', 
        'eu-central-1', options :='format csv, HEADER true')
   );
    """
)


install_aws_commons = (
    """
    DROP EXTENSION aws_s3;
    DROP EXTENSION aws_commons;
    CREATE EXTENSION aws_s3 CASCADE;

    """
)


export_queries = [
    # install_aws_commons,
    export_public_holiday_to_s3,
    export_agg_shipments_to_s3,
    export_best_performing_product_to_s3
]
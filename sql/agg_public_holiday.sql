-- =======================================================================================
-- Description:	CREATE agg_public_holiday Table Queries
-- =======================================================================================

DROP TABLE IF EXISTS user_analytics.agg_public_holiday;
CREATE TABLE IF NOT EXISTS user_analytics.agg_public_holiday(
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
    );

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
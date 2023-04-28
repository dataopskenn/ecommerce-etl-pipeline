CREATE TABLE IF NOT EXISTS username_staging.dim_dates
    (
        calendar_dt              DATE NOT NULL CONSTRAINT dim_dates_pk PRIMARY KEY,
        year_num                 BIGINT NOT NULL,
        month_of_the_year_num    BIGINT NOT NULL,
        day_of_month_num         BIGINT NOT NULL,
        day_of_week_num          BIGINT NOT NULL,
        weekend_indr             BOOLEAN NOT NULL,
        public_holiday           BOOLEAN NOT NULL
    );
    
ALTER TABLE username_staging.dim_dates
OWNER to postgres;
INSERT INTO username_staging.dim_dates
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

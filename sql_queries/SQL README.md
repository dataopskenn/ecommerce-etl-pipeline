# File Description

<p align="center">
<img src = "../images/data model.png" alt="Data2Bots LinkedIn Logo" width="100%" height="100%" />
</p>


## filename: [schema_query.py](/sql_queries/schema_query.py)
This fie contains queries for creating and dropping the schema used for creating this data model, and hence is capable of dropping all the tables contained using the `CASCADE` function. This file will not be used for this assessment as I do not own the data warehouse and do not have the access to drop or add any schema. The queries were compiled in a python list for iterative execution with a `for loop`. This iterative method of execution is cleaner, shorter, easier and more efficient.<br>



## filename: [drop_tables_queries.py](/sql_queries/drop_tables_queries.py)
Contains queries for dropping all the data tables in the given schema. The queries are also written in python docstrings for easy execution with the database `psycopg2` cursor and connection. The queries are compiled in a python list for iterative execution.<br>



## filename: [create_tables_queries.py](/sql_queries/create_tables_queries.py)
Contains queries for creating all the data tables in the given schema, written in python docstring format, from where they can be easily be executed with the database `psycopg2` cursor and connection. The queries are then compiled in a python list, so that they can be executed iteratively in a python `for loop`.<br>



## filename: [data_model_staging.py](/sql_queries/data_model_staging.py)
Contains queries for modeling the data tables in the staging area according to the schema in the diagram above. It is impossible to implement the model at the point of creating the tables as they are not all available in the warehouse, modeling the tables will lead to a series of `psycopg2` errors. <br>

It is important to ensure that data has been inserted into the tables before modeling can take place. Pyscopg2 by default will raise errors around data quality and integrity if key pairs in `PRIMARY` and `FOREIGN` keys do not match, as such, it will raise errors when one or both tables are empty. <br>

This is the reason why some of the queries were commented out (with "--"), as they contain queries of tables present in the model diagram above, but contain data I do not have access to.<br>



## filename: [data_model_analytics.py](/sql_queries/data_model_analytics.py)
Contains queries for modeling the data tables in the analytics area. Only the `best_performing_product` table can be modeled in this schema. <br>



## filename: [insert_into_tables_queries.py](/sql_queries/insert_into_tables_queries.py)
Contains queries for inserting data from their different sources into the various tables in both schemas of our data warehouse. The `orders`, `reviews` and `shipment_deliveries` tables all have CSV files from the s3 buckets where they reside, thus can be moved into the data warehouse with any of `psycopg2` (using the queries provided in this file) or `SQLAlchemy engine` (using the engine, and not the query provided in this file). <br>

For this project, the `SQLAlchemy engine` was used to insert these tables from their s3 buckets into the data warehouse because they were found to be faster than `psycopg2`. This behaviour is a bit strange, since traditionally, psycopg2 is about 2x faster than the SQLAlchemy engine (which uses psycopg2 internally to communicate with the database). <br>  

The dim_dates table and other tables which are queries from these initial three, where all implemented with `psycopg2`. The thought process for deriving the solution to this assessment (`dim_dates`, `agg_public_holidays`, `agg_shipments`, `best_performing_product`.<br>




#### filename: [dim_dates.py]
sql file: ![dim_dates.sql](../sql/dim_dates.sql) <br>
Description: creates and inserts a "calendar" (`dim_dates`) table into the data warehouse. Given the field names for this table, it is necessary to first create something similar to calendar table for the period of time under consideration here. The code below creates the calendar fields necessary;

```sql
SELECT 
   datum AS calendar_dt,
   EXTRACT(YEAR FROM datum) AS year_num,
   EXTRACT(MONTH FROM datum) AS month_of_the_year_num,
   EXTRACT(DAY FROM datum) AS day_of_month_num,
   EXTRACT(ISODOW FROM datum) AS day_of_week_num
FROM (SELECT '2021-01-01'::DATE + SEQUENCE.DAY AS datum
    FROM GENERATE_SERIES(0, 29219) AS SEQUENCE (DAY)
    GROUP BY SEQUENCE.DAY) DQ
ORDER BY 1;
```

Here, a calendar containing `Year`, `Month`, `Day Number`, and `Day of the Week Number` is created. Then there is the need to create a `BOOLEAN` field, using `TRUE` to indicate a day is a weekend and `FALSE` to indicate that a day is not a weekend, as it is one of the requirements for defining a public holiday based on this project needs. Within this table, weekends were defined using the query below;

```sql
CASE
    WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE
    ELSE FALSE
    END AS weekend_indr;
```
where `weekend_indr` means "Weekend Indicator", a boolean for indicating whether that particular date is a weekend (6th and 7th day of the week) or not. <br>

In this file, as there was no other way to sequentially tell what days are public holidays in Nigeria (since a number of them do not have fixed dates), it was a necessity to manually indicate what dates were holidays within the period of time under examination/query. <br>
According to this assessment, "a public holiday is a day with a `day_of_the_week` number in the range 1 - 5 and a `working_day` value of false". Some of these days in Nigeria include; <br>

<strong> Fixed Holidays: </strong> 
- January 1
- May 1
- May 29
- June 12
- October 1
- December 24
- December 25
- December 26
- December 31

<strong> Holidays that are not fixed: </strong>
- Good Friday: April 2 (2021)
- Easter Monday: April 5 (2021)
- Islamic Holiday: July 20 (2021)
- Good Friday (2022): April 15
- Easter Monday (2022): April 18

Although, this query could prove a little difficult to maintain, it was the only meaningful solution in sight. The block of code below captures this part of the query;

```sql
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
```

Putting all the different queries as found in the file, we obtain the dim_dates table with boolean fields for weekend and public holiday indicators.<br>



#### filename: [agg_public_holiday.py]
sql file: ![agg_public_holiday.sql](../sql/agg_public_holiday.sql) <br>
Description: creates and inserts the `agg_public_holiday` table into the data warehouse. Within this table, the sum of all orders placed during public holidays were summed up.

Challenges: The requirement for this query was not very clear, as there was no specified column to group the query by.

```sql
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
```

To execute this insert statement, using a CTE which could take less time to execute, a WITH statement was first used to join the orders table to the dim_dates table. The idea is have a broad table that displays all transactions, and a column to specify if the transaction took place on a public holiday (as defined by the assessment requirements) saved as a new table called "large_order". <br>

Next, subqueries were used to count the number of orders that were made on public holidays in the different months of the year. The ingestion date being the current date, when the query is executed, this date changes every time the query is executed, and he values in the table adjust each time, to the latest figures. The result is a single row data, containing the aggregate sum of orders made on public holidays in each month.<br>




#### filename: [agg_shipments.py]
sql file: ![agg_shipments.sql](../sql/agg_shipments.sql) <br>
Description: creates and inserts the `agg_shipments` table into the data warehouse. Within this table, the sum of all orders placed during public holidays were summed up, from the different staging tables holding the data.

Challenges: The requirement for this query was not very clear, as there was no specified column to group the query by. <br>
To execute this query, the same logic that was used to execute the `agg_public_holiday` query was also employed here.

A CTE was used to join the `orders` table to the `shipment_deliveries` table. The idea was to have one big table where the `order_date`, `delivery_date` and `shipment_date` columns can be used to indicate if an order was delivered or not, then we can count these orders base on this new table, the late_df and undelivered_df CTEs and their subqueries.

```sql
INSERT INTO user_analytics.agg_shipments
    WITH large_ship AS (
	SELECT *
	FROM user_staging.orders as o
	LEFT JOIN user_staging.shipment_deliveries AS ship
	ON o.order_id = ship.order_id),
```

- `late_df` : The subquery `foo` in the late_df CTE (in the `FROM` entry-clause) counts the number of orders that were shipped late, based on their order dates, while the main query selects the fields created in the subquery. 

```sql

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
```

- `undelivered_df`: the process for this CTE is the same that of the `late_df`'s. The subquery `fooo` in the undelivered_df CTE (in the `FROM` entry-clause) counts the number of orders that were not delivered, based on their order dates, while the main query selects the fields created in the subquery.

```sql

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
```

Finally, a select statement at the end of the query, selects the fields which will appear in the final view. 

```sql
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
```

Putting the different parts of the query together, gives the solution for this table. <br>



#### filename: [best_performing_product.py]
sql file: ![best_performing_product.sql](../sql/best_performing_product.sql) <br>
Description: creates and inserts data into the `best_performing_product` table.

Challenges: This table appears a little disorganized after the insert query was executed because multiple products have the same highest number of orders placed at different dates, so there was quite a lot of repitition of the percentages. 

This was probably the most difficult query to execute due to its complexity. for this execution, several CTEs were required for

1. joining the orders and shipments tables to one large_table

```sql
WITH large_ship AS (
    SELECT *
	FROM user_staging.orders AS o
	LEFT JOIN user_staging.shipment_deliveries AS ship
	ON o.order_id = ship.order_id),
```

2. calculating the; 
    - percentage of late shipments (`pct_late_shipments`),
    - percentage of undelivered shipments (`pct_undelivered_shipments`), and
    - percentage of early shipments(`pct_early_shipments`)
from this large_table

```sql
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
```

3. calculating the percentage 1, 2, 3, 4, and 5 star reviews, by first calculating the sum of all the different review points, divide it by the total reviews, then multiply them by 100 for each product.

```sql

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
	ORDER BY product_id),
```

4. The product with the highest reviews, the day it was ordered the most, either that day was a public holiday, total review points, by joining the orders table with the dim_dates table to access the date and public holiday columns.

```sql
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
```

Then the required columns were then selected for insertion into the table.

```sql
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
```

Putting the different parts of the query together, joined by a comma ",", gives the solution for this table. <br>


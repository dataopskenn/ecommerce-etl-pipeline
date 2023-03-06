import os
import csv
import pandas as pd
import psycopg2
import sys
import yaml

from database import create_database_connection
from sql_queries.insert_into_tables_queries import insert_agg_public_holiday_table, insert_agg_shipments_table, insert_best_performing_product_table
from sql_queries.data_model_analytics import analytics_data_model_queries
# from sql_queries.insert_into_tables_queries import export_queries


def process_agg_public_holiday_data(cur, conn):
    """
    Inserting the agg_public_holiday_data
    """

    cur.execute(
        insert_agg_public_holiday_table
    )
    conn.commit()

    print(
        f"data transformed and inserted for agg_public_holiday"
    )


def process_agg_shipments(cur, conn):
    """
    Inserting the agg_shipments_data
    """

    cur.execute(
        insert_agg_shipments_table
    )
    conn.commit()

    print(
        f"data transformed and inserted for agg_shipments"
    )


def process_best_performing_product(cur, conn):
    """
    Inserting the best_performing_product_data
    """

    cur.execute(
        insert_best_performing_product_table
    )
    conn.commit()

    print(
        f"data transformed and inserted for best_performing_product"
    )


def analytics_data_model(cur, conn):
    """
    Execute data modeling queries
    :return: returns nothing
    """

    for query in analytics_data_model_queries:
        cur.execute(query)
        conn.commit()
    # print(
    # f"Successfully implemented the data model for the analytics area"
    # )


def main():
    """
    Driver function to run all the functions that has been created
    """

    cur, conn = create_database_connection()

    process_agg_public_holiday_data(cur, conn)
    process_agg_shipments(cur, conn)
    process_best_performing_product(cur, conn)
    analytics_data_model(cur, conn)

    print("Done transforming and inserting data for analytics area")

    conn.close()


if __name__ == "__main__":

    """
    Run all the functions that has been created in this file, using the driver function above
    """

    main()

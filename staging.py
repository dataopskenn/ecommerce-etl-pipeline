from sql_queries.data_model_staging import staging_data_model_queries
from sql_queries.insert_into_tables_queries import insert_orders_table, insert_reviews_table, insert_shipments_table, insert_dim_dates_table
from sql_queries.insert_into_tables_queries import insert_dim_customers_table, insert_dim_addresses_table, insert_dim_products_table
from database import create_database_connection, config
from sqlalchemy import create_engine
import os
import csv
import pandas as pd

import boto3
from botocore import UNSIGNED
from botocore.client import Config
from io import StringIO
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
bucket_name = "database-name-bucket"
response = s3.list_objects(Bucket=bucket_name, Prefix="orders_data")


# Create an SQLAlchemy engine
host = config['POSTGRES_CONFIG']['host']
dbname = config['POSTGRES_CONFIG']['dbname']
user = config['POSTGRES_CONFIG']['user']
password = config['POSTGRES_CONFIG']['password']
port = config['POSTGRES_CONFIG']['port']

engine = create_engine(
        f'postgresql://{user}:{password}@{host}:5432/{dbname}'
    )


def process_orders_data(cur, conn, file):
    """
    Ensure to run database.py before running this file
    """

    orders_key = 'orders_data/orders.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=orders_key
    )

    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.to_sql(
        'orders', engine, schema='username_staging', 
        if_exists='append', index=False
    )

    print(
        f"data transformed inserted for {file}"
    )


def process_reviews_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    reviews_key = 'orders_data/reviews.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=reviews_key
    )

    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.to_sql(
        'reviews', engine, schema='username_staging', 
        if_exists='append', index=False
    )

    print(
        f"data transformed and inserted for {file}"
        )


def process_customers_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    customers_key = 'orders_data/dim_customers.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=customers_key
    )

    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.to_sql(
        'dim_customers', engine, schema='username_staging', 
        if_exists='append', index=False
    )

    print(
        f"data transformed and inserted for {file}"
        )


def process_products_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    products_key = 'orders_data/dim_products.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=products_key
    )

    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.to_sql(
        'dim_products', engine, schema='username_staging', 
        if_exists='append', index=False
    )

    print(
        f"data transformed and inserted for {file}"
        )


def process_addresses_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    addresses_key = 'orders_data/dim_addresses.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=addresses_key
    )

    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.to_sql(
        'dim_addresses', engine, schema='username_staging', 
        if_exists='append', index=False
    )

    print(
        f"data transformed and inserted for {file}"
        )


def process_shipments_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    shipment_key = 'orders_data/shipment_deliveries.csv'

    csv_obj = s3.get_object(
        Bucket=bucket_name, Key=shipment_key
    )
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(
        StringIO(csv_string)
    )

    df.shipment_date = pd.to_datetime(
        df.shipment_date, format="%Y-%m-%d"
    )

    df.delivery_date = pd.to_datetime(
        df.delivery_date, format="%Y-%m-%d"
    )

    df.to_sql('shipment_deliveries', engine,
              schema='username_staging', if_exists='replace', index=False
              )

    print(
        f"shipments data transformed and inserted for {file}"
    )


def process_holiday_table(cur, conn):

    cur.execute(insert_dim_dates_table)
    conn.commit()
    print(
        "Done creating public holiday table"
    )


def staging_data_model(cur, conn):

    for query in staging_data_model_queries:
        cur.execute(query)
        conn.commit()
        #print(
        #    f"Successfully implemented the data model for the {query}"
        #)


def main():
    """
    Driver function to run all the functions that has been created
    """

    cur, conn = create_database_connection()

    process_orders_data(cur, conn, "orders.csv")
    process_reviews_data(cur, conn, "reviews.csv")
    process_customers_data(cur, conn, "dim_customers.csv")
    process_addresses_data(cur, conn, "dim_addresses.csv")
    process_products_data(cur, conn, "dim_products.csv")
    process_shipments_data(cur, conn, 'shipment_deliveries.csv')
    process_holiday_table(cur, conn)
    staging_data_model(cur, conn)

    print("Done transforming and inserting data for staging area")

    conn.close()


if __name__ == "__main__":

    """
    Run all the functions that has been created in this file, using the driver function above
    """

    main()

import os
import csv
import pandas as pd
import time
from sqlalchemy import create_engine
import psycopg2
import yaml
from sql_queries import *

# Opening the YAML config file
with open("new_config.yml") as f:
    content = f.read()

# from config.yml import user name and password
config = yaml.load(content, Loader=yaml.FullLoader)


def process_orders_data(cur, conn, file):
    """
    Ensure to run database.py before running this file
    """

    df = csv.reader(open("orders.csv", 'r'), delimiter=",", quotechar='|')
    next(df, None)
    for row in df:
        cur.execute(insert_orders_table, row)
        conn.commit()
    print(f"orders data transformed inserted for {file}")


def process_reviews_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """

    df = csv.reader(open("reviews.csv", 'r'), delimiter=",", quotechar='|')
    next(df, None)
    for row in df:
        cur.execute(insert_reviews_table, row)
        conn.commit()
    print(f"reviews information data transformed and inserted for {file}")


def process_shipments_data(cur, conn, file):
    """
    Repeating the same process as above,difference is in the query specified to execute
    """
    #engine = create_engine("host={} dbname={} user={} password={} port={}".format(
    #    *config['POSTGRES_CONFIG'].values()))

    #shipment_key = 'orders_data/shipment_deliveries.csv'

    #csv_obj = s3.get_object(Bucket=bucket_name, Key=shipment_key)
    #body = csv_obj['Body']
    #csv_string = body.read().decode('utf-8')
    #df = pd.read_csv('shipment_deliveries.csv')
    #df = pd.read_csv(StringIO(csv_string))
    #df.shipment_date = pd.to_datetime(df.shipment_date)
    #df.delivery_date = pd.to_datetime(df.delivery_date)
    #df.rename(columns=df.iloc[0]).drop(df.index[0])
    #df.to_sql('shipment_deliveries', engine, schema='dataopskenn_staging', if_exists='append', index=False)
    df = csv.reader(open(file, 'r'), delimiter=",", quotechar='|')
    next(df, None)
    for row in df:
        cur.execute(insert_reviews_table, row)
        conn.commit()
    print(f"shipments data transformed and inserted for {file}")


def process_public_holiday_data(cur, conn):
    """
    Inserting the agg_public_holiday_data
    """

    cur.execute(insert_agg_public_holiday)
    conn.commit()
    print(f"data transformed and inserted for agg_public_holiday")


def main():
    """
    Driver function to run all the functions that has been created
    """

    # Opening the YAML config file
    with open("new_config.yml") as f:
        content = f.read()

    # from config.yml import user name and password
    config = yaml.load(content, Loader=yaml.FullLoader)

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['POSTGRES_CONFIG'].values()))
    cur = conn.cursor()

    process_orders_data(cur, conn, "orders.csv")
    process_reviews_data(cur, conn, "reviews.csv")
    process_shipments_data(cur, conn, 'shipment_deliveries.csv')
    process_public_holiday_data(cur, conn)

    conn.close()


if __name__ == "__main__":

    """
    Run all the functions that has been created so far, using the driver function above
    """

    main()

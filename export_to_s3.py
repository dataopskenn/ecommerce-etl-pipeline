# CREATE A CONNECTION ENGINE

import pandas as pd
from sqlalchemy import create_engine
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from io import StringIO
from database import config


s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
bucket_name = "database-name-bucket"


# Create an SQLAlchemy engine
host = config['POSTGRES_CONFIG']['host']
dbname = config['POSTGRES_CONFIG']['dbname']
user = config['POSTGRES_CONFIG']['user']
password = config['POSTGRES_CONFIG']['password']
port = config['POSTGRES_CONFIG']['port']

engine = create_engine(
        f'postgresql://{user}:{password}@{host}:5432/{dbname}'
    )


def export_public_holiday_to_s3(file):

    # download the data from the data warehouse
    df = pd.read_sql_query(
        "SELECT * FROM user_analytics.agg_public_holiday", 
        con=engine)

    # push the data to the s3 instance

    with StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

    response = s3.put_object(
        Bucket = bucket_name, 
        Key="analytics_export/user/agg_public_holiday",
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object {file} response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")

    # push the data to the s3 instance
    # s3.upload_fileobj(df, bucket_name, "analytics_export/user/agg_public_holiday.csv")


def export_shipments_to_s3(file):

    # download the data from the data warehouse
    df = pd.read_sql_query(
        "SELECT * FROM user_analytics.agg_shipments", 
        con=engine)

    # push the data to the s3 instance

    with StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

    response = s3.put_object(
        Bucket = bucket_name, 
        Key="analytics_export/user/agg_shipments",
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object {file} response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")

    # push the data to the s3 instance
    # s3.upload_fileobj(df, bucket_name, "analytics_export/user/agg_shipments.csv")


def export_best_performing_product_to_s3(file):

    # download the data from the data warehouse
    df = pd.read_sql_query(
        "SELECT * FROM user_analytics.best_performing_product", 
        con=engine)

    # push the data to the s3 instance

    with StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

    response = s3.put_object(
        Bucket = bucket_name, 
        Key="analytics_export/user/best_performing_product",
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object {file} response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")

    # push the data to the s3 instance
    # s3.upload_fileobj(df, bucket_name, "analytics_export/user/best_performing_product.csv")


def main():

    export_public_holiday_to_s3("user_analytics.agg_public_holiday")
    export_public_holiday_to_s3("user_analytics.agg_shipments")
    export_best_performing_product_to_s3("user_analytics.best_performing_product")


if __name__ == "__main__":

    """
    Run all the functions that has been created in this fileobj, using the driver function above
    """

    main()

    print(f"Done exporting to s3 instance {bucket_name}/ analytics_export")
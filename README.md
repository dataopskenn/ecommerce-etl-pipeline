<p>
<img src = "/images/data model.png" alt="Data2Bots LinkedIn Logo"/>
</p>

The solution to this problem is divided into two separate parts;

- ### Infrastructure as Code (IaC) using terraform
The intention for this is to build a terraform managed AWS Postgres Data Warehouse. However, this part will not be executed as all of the fields needed have been provided for.

- ### Python ETL pipeline with PSQL transformation codes
This part of the solution is also divided into two parts

- the first being the PSQL queries, written as Python docstrings, executed with either of `psycopg2` or `SQLAlchemy` `engine` within a python file. ![More information here](/sql_queries/SQL%20README.md)

- the second being the Python ETL file `app.py`, which pulls queries and database configuration parameters from different files within the working directory and sub-directories. 

## main.py

Python Libraries used for the execution of this file includes the following;
-sqlalchemy
- os
- csv
- pandas as pd
- boto3
- botocore
- io
- psycopg2
- sys
- yaml

By design, this file will download the data (csv) files directly from the s3 bucket where it is domiciled into python memory, then load it directly into the data warehouse, using defined staging and analytics schemas created from ![schema_query.py](/sql_queries/schema_query.py), hence there is no need to have a copy of the data files offline. This is a complete end-to-end pipeline, from source to warehouse. 

#### Workflow/Pipeline flow

To execute this app, run the code below from within the parent directory on terminal

```sh
$ python main.py
```

This will run the following files in the order
database.py >> staging.py >> analytics.py >> export_to_s3.py


## Uploading to AWS s3 instance

Ideally, the query below should export the data directly to the s3 location staright from the rds instance;

```sql

SELECT * 
FROM aws_s3.query_export_to_s3(
    'SELECT * FROM schema.table', 
    aws_commons.create_s3_uri(
        'bucket_name', 
        'analytics_export/user_id/table.csv', 
        'aws_region', options :='format csv, HEADER true'
    )
);
```

but I cannot install the `aws_commons` extension on my PC at this time, so instead, I implemented the following steps to do this

- queried the data out of the postgres data warehouse
- saved it to a pandas dataframe in memory
- exported it to the s3 bucket, using the instructions stated in the assessment requirements

The code below gives an example of how I executed this step, using a random table as an example;

```python

def export_table_to_s3(file):

    # download the data from the data warehouse
    df = pd.read_sql_query(
        "SELECT * FROM schema.table", 
        con=engine)

    # push the data to the s3 instance

    with StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

    response = s3.put_object(
        Bucket = bucket_name, 
        Key="analytics_export/user_id/table",
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object {file} response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")

```

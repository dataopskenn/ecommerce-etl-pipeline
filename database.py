from sql_queries.schema_query import drop_schema_queries, create_schema_queries

import psycopg2
import yaml 
from sql_queries.create_tables_queries import create_queries
from sql_queries.drop_tables_queries import drop_queries


# Opening the YAML config file, that contains the configuration of the database
with open("./safe/config.yml") as f:
    content = f.read()

# from config.yml import user name and password
config = yaml.load(content, Loader=yaml.FullLoader)


"""
Create database connection
Establish connection to the database
:return: returns (cur, conn) a cursor and connection reference
"""

def create_database_connection():
    """
    :return: returns nothing
    """

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config['POSTGRES_CONFIG'].values()
            )
        )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    return cur, conn


"""
Execute SCHEMA queries
- First execute the DROP SCHEMA query
- Then execute the CREATE SCHEMA query
This step is important when there is need to starta fresh ETL setup
:return: returns nothing
"""

def drop_schema(cur, conn):

    for query in drop_schema_queries:
        cur.execute(query)
        conn.commit()
        #print(
        #    f"Done dropping the {query} schema"
        #)

    print("Dropped Schemas")


def create_schema(cur, conn):

    for query in create_schema_queries:
        cur.execute(query)
        conn.commit()
        #print(
        #    f"Done creating the {query} schema"
        #)

    print("Created Schemas")



"""
Execute DROP TABLE queries for all the tables we intend to work with.
These tables will be executed one after the other.
The function aims to make provision for when only one or more tables need to be dropped, and not all the tables
"""

def drop_tables(cur, conn):

    """
    :return: returns nothing
    """

    for query in drop_queries:
        cur.execute(query)
        conn.commit()
        #print(
        #    f"Done dropping the {query} table"
        #)

    print("Successfully dropped tables")


"""
Execute CREATE TABLE queries for all the tables we intend to work with.
These tables will be executed one after the other.
The function aims to make provision for when only one or more tables need to be created, and not all tables
"""

def create_tables(cur, conn):

    """
    :return: returns nothing
    """

    for query in create_queries:
        cur.execute(query)
        conn.commit()
        #print(
        #    f"Done creating the {query} table"
        #)

    print("Successfully created tables")


def main():
    cur, conn = create_database_connection()
    drop_tables(cur, conn)
    # drop_schema(cur, conn)
    # create_schema(cur, conn)
    create_tables(cur, conn)




if __name__ == "__main__":

    """
    Run all the functions that has been created in this file, using the driver function above
    """

    main()
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, insert_table_queries
from sql_queries import drop_schema_queries, create_schema_queries, insert_date_tables_queries
#from holiday import create_holidays_table
import configparser
import yaml


# Opening the YAML config file
with open("config.yml") as f:
    content = f.read()

# from config.yml import user name and password
config = yaml.load(content, Loader=yaml.FullLoader)


def create_database_connection():

    """
    Establish connection to the database 
    Return the connection and cursor refrence
    :return: returns (cur, conn) a cursor and connection reference
    """
    

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['POSTGRES_CONFIG'].values()))
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS public")
    cur.execute("CREATE DATABASE public WITH ENCODING 'utf8' TEMPLATE template0")
    
    # close connection to default database
    conn.close()    

        # Opening the YAML config file
    with open("new_config.yml") as f:
        new_content = f.read()

    # from config.yml import user name and password
    new_config = yaml.load(new_content, Loader=yaml.FullLoader)
        
    # connect to database

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*new_config['POSTGRES_CONFIG'].values()))
    cur = conn.cursor()
    
    return cur, conn


def create_schema(cur, conn):

    """
    Run's all the create schema queries defined in sql_queries.py
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in create_schema_queries:
        cur.execute(query)
        conn.commit()


def drop_schema(cur, conn):

    for query in drop_schema_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):

    """
    Run's all the create table queries defined in sql_queries.py
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):

    """
    Run's all the drop table queries defined in sql_queries.py
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):

    """
    Run's all the insert table queries defined in sql_queries.py
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in insert_date_tables_queries:
        cur.execute(query)
        conn.commit()

def holiday_table(cur, conn):

    cur.execute(create_holidays_table)
    conn.commit()

def main():

    """
    Driver main function.
    """
    cur, conn = create_database_connection()
    
    drop_tables(cur, conn)
    print("Successfully Dropped Tables!")

    drop_schema(cur, conn)
    print("Successfully Dropped Schema!")

    create_schema(cur, conn)
    print("Successfully Created Schema!")

    #create_tables(cur, conn)
    #print("Successfully Created Tables!")

    #insert_tables(cur, conn)
    #print("Successfully Inserted Date Tables!")

    #holiday_table(cur, conn)(cur, conn)
    #print("Successfully Inserted Holiday Table!")

    conn.close()


if __name__ == "__main__":
    """
    Run the "main" function
    """

    main()
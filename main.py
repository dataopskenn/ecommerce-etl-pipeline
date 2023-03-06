from database import main as database_main
from staging import main as staging_main
from analytics import main as analytics_main
from export_to_s3 import main as export_to_s3_main


if __name__ == "__main__":

    """
    - Create the database
    - Cleanup the data before ingestion
    - Ingest the data into postgres, view for local PgAdmin4
    """

    database_main()
    staging_main()
    analytics_main()
    export_to_s3_main()
    
    
"""
-- =======================================================================================
-- Description:	CREATE SCHEMA Queries
-- =======================================================================================
"""

create_staging_schema = ("""CREATE SCHEMA IF NOT EXISTS user_staging""")
create_analytics_schema = ("""CREATE SCHEMA IF NOT EXISTS user_analytics""")


"""
-- =======================================================================================
-- Description:	DROP SCHEMA Queries
-- =======================================================================================
"""

drop_staging_schema = ("""DROP SCHEMA IF EXISTS user_staging CASCADE""")
drop_analytics_schema = ("""DROP SCHEMA IF EXISTS user_analytics CASCADE""")

drop_schema_queries = [drop_staging_schema, drop_analytics_schema]
create_schema_queries = [create_staging_schema, create_analytics_schema]
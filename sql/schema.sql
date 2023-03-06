--"""
-- =======================================================================================
-- Description:	CREATE SCHEMA Queries
-- =======================================================================================
--"""

CREATE SCHEMA IF NOT EXISTS username_staging
CREATE SCHEMA IF NOT EXISTS username_analytics


--"""
-- =======================================================================================
-- Description:	DROP SCHEMA Queries
-- =======================================================================================
--"""

DROP SCHEMA IF EXISTS username_staging CASCADE
DROP SCHEMA IF EXISTS username_analytics CASCADE

-- Shared PostgreSQL initialization
-- Creates separate schemas for each service to avoid conflicts

CREATE SCHEMA IF NOT EXISTS iceberg;
CREATE SCHEMA IF NOT EXISTS airflow;
CREATE SCHEMA IF NOT EXISTS prefect;
CREATE SCHEMA IF NOT EXISTS mage;

-- Airflow needs its own database or schema; using schema approach
-- Grant full access to the main user on all schemas
GRANT ALL PRIVILEGES ON SCHEMA iceberg TO lakehouse;
GRANT ALL PRIVILEGES ON SCHEMA airflow TO lakehouse;
GRANT ALL PRIVILEGES ON SCHEMA prefect TO lakehouse;
GRANT ALL PRIVILEGES ON SCHEMA mage TO lakehouse;

#!/bin/bash
set -e

# Create required log directories
mkdir -p /opt/airflow/logs/scheduler /opt/airflow/logs/dag_processor_manager

echo "Initializing Airflow..."
airflow db migrate

airflow users create \
  --username "${AIRFLOW_ADMIN_USER:-admin}" \
  --password "${AIRFLOW_ADMIN_PASSWORD:-admin}" \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@local.dev 2>/dev/null || true

echo "Starting Airflow webserver + scheduler..."
airflow webserver &
exec airflow scheduler

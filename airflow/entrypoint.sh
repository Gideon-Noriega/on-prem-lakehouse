#!/bin/bash
set -e

airflow db migrate
airflow users create --username admin --password admin   --firstname Admin --lastname User --role Admin   --email admin@local.dev 2>/dev/null || true

airflow webserver &
exec airflow scheduler

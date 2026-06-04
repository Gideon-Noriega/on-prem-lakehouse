from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "lakehouse",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="lakehouse_pipeline",
    default_args=default_args,
    description="Ingest raw data via Spark, transform with dbt",
    schedule="@hourly",
    start_date=datetime(2026, 6, 4),
    catchup=False,
    tags=["lakehouse", "iceberg", "dbt"],
) as dag:

    spark_ingest = DockerOperator(
        task_id="spark_ingest",
        image="on-prem-lakehouse-spark-master",
        command="""/opt/spark/bin/spark-sql --master 'local[*]' -e "INSERT INTO lakehouse.demo.test_table VALUES (CAST(UNIX_TIMESTAMP() AS INT), 'AAPL', current_timestamp());" """,
        docker_url="unix://var/run/docker.sock",
        network_mode="on-prem-lakehouse_lakehouse",
        auto_remove="success",
        environment={
            "AWS_REGION": "us-east-1",
            "AWS_ACCESS_KEY_ID": "admin",
            "AWS_SECRET_ACCESS_KEY": "admin123456",
        },
    )

    dbt_run = DockerOperator(
        task_id="dbt_run",
        image="on-prem-lakehouse-dbt",
        command="run",
        docker_url="unix://var/run/docker.sock",
        network_mode="on-prem-lakehouse_lakehouse",
        auto_remove="success",
    )

    dbt_test = DockerOperator(
        task_id="dbt_test",
        image="on-prem-lakehouse-dbt",
        command="test",
        docker_url="unix://var/run/docker.sock",
        network_mode="on-prem-lakehouse_lakehouse",
        auto_remove="success",
    )

    spark_ingest >> dbt_run >> dbt_test

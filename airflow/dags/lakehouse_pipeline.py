from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    "owner": "lakehouse",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

SPARK_CONF = " ".join([
    "--conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    "--conf spark.sql.catalog.lakehouse=org.apache.iceberg.spark.SparkCatalog",
    "--conf spark.sql.catalog.lakehouse.type=rest",
    "--conf spark.sql.catalog.lakehouse.uri=http://iceberg-rest:8181",
    "--conf spark.sql.catalog.lakehouse.warehouse=s3://warehouse/",
    "--conf spark.sql.catalog.lakehouse.io-impl=org.apache.iceberg.aws.s3.S3FileIO",
    "--conf spark.sql.catalog.lakehouse.s3.endpoint=http://minio:9000",
    "--conf spark.sql.catalog.lakehouse.s3.access-key-id=admin",
    "--conf spark.sql.catalog.lakehouse.s3.secret-access-key=admin123456",
    "--conf spark.sql.catalog.lakehouse.s3.path-style-access=true",
    "--conf spark.sql.catalog.lakehouse.s3.region=us-east-1",
    "--conf spark.sql.defaultCatalog=lakehouse",
    "--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000",
    "--conf spark.hadoop.fs.s3a.access.key=admin",
    "--conf spark.hadoop.fs.s3a.secret.key=admin123456",
    "--conf spark.hadoop.fs.s3a.path.style.access=true",
    "--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
])

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
        command=f"""/opt/spark/bin/spark-sql --master 'local[*]' {SPARK_CONF} -e "INSERT INTO lakehouse.demo.test_table VALUES (CAST(UNIX_TIMESTAMP() AS INT), 'PIPELINE', current_timestamp());" """,
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

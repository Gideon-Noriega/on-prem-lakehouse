FROM apache/airflow:2.10.4-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 988 hostdocker 2>/dev/null || true && usermod -aG hostdocker airflow
RUN mkdir -p /opt/airflow/logs/scheduler /opt/airflow/logs/dag_processor_manager && chown -R airflow:root /opt/airflow/logs

USER airflow
RUN pip install --no-cache-dir apache-airflow-providers-docker

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

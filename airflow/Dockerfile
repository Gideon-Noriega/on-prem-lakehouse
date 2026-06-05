FROM apache/airflow:2.10.4-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 988 hostdocker && usermod -aG hostdocker airflow

USER airflow
RUN pip install --no-cache-dir apache-airflow-providers-docker

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

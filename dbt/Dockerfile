FROM python:3.11-slim

RUN pip install --no-cache-dir dbt-core dbt-trino

WORKDIR /dbt
COPY . /dbt/

ENTRYPOINT ["dbt"]
CMD ["run"]

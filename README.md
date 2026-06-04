# On-Prem Lakehouse

A fully self-hosted data lakehouse running on Docker, built with open-source tools. Implements a modern analytics stack with ACID-compliant table management, distributed processing, fast SQL queries, analytics modeling, and pipeline orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Airflow (Orchestration)                   │
├─────────────────────────────────────────────────────────────────┤
│            dbt (Analytics Modeling via Trino)                    │
├──────────────────────────────┬──────────────────────────────────┤
│     Spark (Batch Processing) │     Trino (SQL Queries)          │
├──────────────────────────────┴──────────────────────────────────┤
│              Iceberg REST Catalog (Table Management)             │
├──────────────────────────────┬──────────────────────────────────┤
│     MinIO (Object Storage)   │   PostgreSQL (Catalog Backend)   │
└──────────────────────────────┴──────────────────────────────────┘
```

**Data Flow:** Raw data → Spark writes Iceberg tables to MinIO → Trino queries them → dbt transforms into analytics models → Airflow orchestrates the pipeline.

## Stack

| Layer | Component | Role | Port |
|-------|-----------|------|------|
| Storage | MinIO | S3-compatible object storage | 9002 (API), 9003 (Console) |
| Catalog | Iceberg REST + PostgreSQL | ACID table management, schema evolution, time travel | 8181 |
| Processing | Apache Spark 3.5 | Distributed batch processing, Iceberg writes | 8082 (UI), 7078 (Master) |
| Query | Trino | Fast interactive SQL over Iceberg tables | 8083 |
| Modeling | dbt-trino | ELT transforms, testing, documentation | On-demand |
| Orchestration | Apache Airflow | DAG scheduling, monitoring, retries | 8084 |

## Quick Start

```bash
# Clone
git clone https://github.com/Gideon-Noriega/on-prem-lakehouse.git
cd on-prem-lakehouse

# Start all services
docker compose up -d

# Verify
docker compose ps
```

Wait ~60 seconds for all services to initialize, then:

```bash
# Write data via Spark
docker exec lakehouse-spark-master /opt/spark/bin/spark-sql --master 'local[*]' \
  -e "CREATE NAMESPACE IF NOT EXISTS lakehouse.demo;
      CREATE TABLE IF NOT EXISTS lakehouse.demo.trades (id INT, symbol STRING, ts TIMESTAMP) USING iceberg;
      INSERT INTO lakehouse.demo.trades VALUES (1, 'AAPL', current_timestamp()), (2, 'GOOG', current_timestamp());"

# Query via Trino
docker exec lakehouse-trino trino --execute "SELECT * FROM iceberg.demo.trades;"

# Run dbt models
docker compose run --rm dbt run

# Run dbt tests
docker compose run --rm dbt test
```

## Services

### MinIO (Object Storage)
- Console: http://localhost:9003 (admin / admin123456)
- Buckets: `warehouse` (Iceberg tables), `raw` (landing zone), `staging` (intermediate)

### Spark
- UI: http://localhost:8082
- Pre-configured with Iceberg extensions and S3 connectivity
- Default catalog: `lakehouse` (Iceberg REST)

### Trino
- UI: http://localhost:8083
- Catalog: `iceberg` — reads/writes same tables as Spark
- Connect with any SQL client: `trino://localhost:8083/iceberg`

### dbt
- Runs on-demand via `docker compose run --rm dbt [command]`
- Models: `staging/` (views) → `marts/` (materialized tables)
- Connected to Trino, outputs to `iceberg.analytics` schema

### Airflow
- UI: http://localhost:8084 (admin / admin)
- DAG: `lakehouse_pipeline` — Spark ingest → dbt run → dbt test
- Schedule: `@hourly` (paused by default)
- Uses DockerOperator to run Spark and dbt in isolated containers

## Project Structure

```
on-prem-lakehouse/
├── docker-compose.yml          # All services
├── spark/
│   ├── Dockerfile              # Spark 3.5 + Iceberg + S3 JARs
│   └── spark-defaults.conf     # Iceberg REST catalog config
├── trino/
│   └── catalog/
│       └── iceberg.properties  # Trino Iceberg connector config
├── dbt/
│   ├── Dockerfile              # dbt-core + dbt-trino
│   ├── dbt_project.yml         # Project config
│   ├── profiles.yml            # Trino connection
│   └── models/
│       ├── staging/            # Views on raw tables
│       └── marts/              # Materialized analytics tables
├── airflow/
│   ├── Dockerfile              # Airflow + Docker provider
│   ├── entrypoint.sh           # DB migrate + webserver + scheduler
│   └── dags/
│       └── lakehouse_pipeline.py  # Orchestration DAG
└── data/                       # Local data mount
```

## Key Features

- **ACID Transactions**: Iceberg provides serializable isolation for concurrent reads/writes
- **Time Travel**: Query previous versions of any table via Iceberg snapshots
- **Schema Evolution**: Add/rename/drop columns without rewriting data
- **Multi-Engine Access**: Spark and Trino share the same tables through the REST catalog
- **Declarative Transforms**: dbt models with built-in testing and lineage
- **Orchestrated Pipelines**: Airflow DAGs with dependency management and retries

## Operations

```bash
# Stop all
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v

# View logs
docker compose logs -f [service]

# Scale Spark workers
docker compose up -d --scale spark-worker=3

# Run ad-hoc Spark SQL
docker exec -it lakehouse-spark-master /opt/spark/bin/spark-sql --master 'local[*]'

# Run ad-hoc Trino queries
docker exec -it lakehouse-trino trino

# Trigger Airflow DAG manually
docker exec lakehouse-airflow airflow dags trigger lakehouse_pipeline
```

## Requirements

- Docker Engine 24+
- Docker Compose v2
- ~8GB RAM available for all services
- ~10GB disk for images + data

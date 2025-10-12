# Retail Pipeline

## Description

A comprehensive data pipeline for retail sector analytics, designed to process, transform, and analyze sales and inventory data using modern data engineering tools.

## Key Features

- **Data Ingestion**: Automated import of retail data from multiple sources
- **Data Transformation**: Advanced ETL processes using DBT (Data Build Tool)
- **Cloud Integration**: Seamless BigQuery data warehouse integration
- **Orchestration**: Airflow-powered workflow management
- **Scalable Analytics**: Flexible data models for generating business insights

## Technology Stack

- **Orchestration**: Apache Airflow with Astronomer SDK
- **Data Transformation**: DBT Core
- **Data Warehouse**: Google BigQuery
- **Language**: Python 3.11+

## Repository Structure

```
retail_pipeline/
│
├── dags/                   # Airflow DAG definitions
│   ├── dag_retail.py       # Main data pipeline DAG
│
├── include/
│   ├── gcp/                # Google Cloud service account credentials
│   ├── data/               # Raw retail datasets
│   └── dbt_retail/         # DBT project models and configurations
│
├── tests/                  # Project test suite
└── pyproject.toml          # Project dependencies and configuration
```

## Prerequisites

- Python 3.11+
- Astro CLI
- Poetry (optional, for dependency management)
- Google Cloud account with BigQuery access

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/levyvix/retail_pipeline.git
cd retail_pipeline
```

### 2. Install Astro CLI

#### macOS
```bash
brew install astro
```

#### Linux
```bash
curl -sSL install.astronomer.io | sudo bash -s
```

### 3. Set Up Environment

```bash
# Install dependencies
uv sync
```

### 4. Initialize Airflow

```bash
# Start local Airflow instance
astro dev start

# Access Airflow UI
# Open http://localhost:8080/
```

## Development Workflow

### Running DBT Models
```bash
# From include/dbt_retail directory
dbt run            # Execute all models
dbt test           # Run data quality tests
dbt docs generate  # Generate documentation
```

### Testing
```bash
# Run project tests
pytest tests/
```

## Configuration

- Configure BigQuery credentials in `include/gcp/`
- Modify DAG schedules in `dags/dag_retail.py`
- Adjust DBT models in `include/dbt_retail/models/`

## Monitoring

- Access Airflow UI at `http://localhost:8080/`
- Monitor DAG runs and data pipeline status

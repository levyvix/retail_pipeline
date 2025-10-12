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

## GCP Project and Service Account Setup

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., `retail-pipeline-project`)
5. Optional: Select an organization if applicable
6. Click "Create"

### 2. Create a Service Account

1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Enter a service account name (e.g., `retail-pipeline-sa`)
4. Add these roles:
   - BigQuery Admin
   - Storage Admin
   - Cloud Composer Worker (if using Composer)

5. Generate and download a JSON key:
   ```bash
   # Save the key securely
   mkdir -p include/gcp
   # Move downloaded key to the project directory
   mv path/to/downloaded/key.json include/gcp/service-account-key.json
   ```

### 3. Create a GCS Bucket

1. Go to "Cloud Storage" > "Buckets"
2. Click "Create Bucket"
3. Choose a globally unique name (e.g., `retail-pipeline-data-{your-unique-id}`)
4. Choose a region close to your primary data sources
5. Choose Standard storage class
6. Configure access control:
   - Uniform access control
   - Grant the service account Storage Object Admin role

### 4. Configure Airflow GCP Connection

1. Open Airflow UI at `http://localhost:8080/`
2. Navigate to "Admin" > "Connections"
3. Click "+" to add a new connection
4. Fill in the following details:
   - Conn Id: `google_cloud_retail`
   - Conn Type: `Google Cloud`
   - Keyfile Path: `/usr/local/airflow/include/gcp/service-account-key.json` OR Keyfile JSON: PASTE JSON from service account


### 5. Update Configuration Files

- `include/gcp/service-account-key.json`: Service account key

**Security Note**:
- Never commit service account keys to version control
- Use environment-specific configurations
- Rotate service account keys periodically
- Ensure service account key file has restricted permissions
  ```bash
  chmod 600 include/gcp/service-account-key.json
  ```

## Configuration

- BigQuery credentials: `include/gcp/service-account-key.json`
- Modify DAG schedules: `dags/dag_retail.py`
- Adjust DBT models: `include/dbt_retail/models/`

## Monitoring

- Access Airflow UI at `http://localhost:8080/`
- Monitor DAG runs and data pipeline status

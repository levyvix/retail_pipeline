# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a retail data pipeline project using:
- Airflow for orchestration
- DBT for data transformations
- BigQuery as the data warehouse
- Python 3.10+ for scripting

## Development Setup

### Prerequisites
- Python 3.10+
- UV (for dependency management)
- Poetry
- Astro CLI

### Dependency Management
- Use `uv add <package>` to install new packages
- Use `uv run` to execute Python scripts
- NEVER manually edit pyproject.toml

### Code Quality and Linting
- Run linter: `uvx ruff check .`
- Format code: `uvx ruff format --line-length 120`
- Type checking: `uvx mypy --ignore-missing-imports .`

## Development Workflow

### Running Airflow Locally
```bash
astro dev start  # Start local Airflow instance
astro dev stop   # Stop local Airflow
```

### DBT Commands
```bash
# From include/dbt_retail directory
dbt run           # Run all models
dbt test          # Run data tests
dbt docs generate # Generate documentation
```

### Testing
```bash
# Run specific test
python -m pytest tests/dags/test_dag_example.py
```

## Key Project Directories
- `dags/`: Airflow DAG definitions
- `include/dbt_retail/`: DBT project files
- `include/data/`: Source datasets
- `tests/`: Project test suite

## Important Notes
- Project uses BigQuery for data warehouse
- DAGs are defined using Airflow and Astronomer SDK
- Data transformations handled via DBT models
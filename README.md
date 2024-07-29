# Retail Pipeline

## Descrição

Este projeto contém uma pipeline de dados para o setor de varejo, projetada para processar, transformar e analisar dados relacionados a vendas e inventário.

## Funcionalidades

- **Coleta de Dados**: Importa dados de fontes variadas.
- **Transformação de Dados**: Limpeza e transformação dos dados para análise.
- **Armazenamento**: Salvamento dos dados processados em um formato adequado.
- **Análise**: Geração de relatórios e insights.

## Estrutura do Repositório

- `include/gcp`: Json com conta de serviço do google (bigquery admin e storage admin)
- `include/data`: Dados de varejo
- `include/dbt_retail`: Projeto DBT
- `dags/dag_retail.py`: DAG Airflow

## Requisitos

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/)
- [Astro CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/levyvix/retail_pipeline.git
```

2. Instale os pacotes necessários:

```bash
poetry install
```

3. Ative o ambiente virtual:

```bash
poetry shell
```

4. Execute o comando abaixo para instalar o Astro CLI:

macOS

```bash
brew install astro
```

Linux

```bash
curl -sSL install.astronomer.io | sudo bash -s
```

5. Inicialize o Airflow usando o AstroCLI:

```bash
astro dev start
```

6. Acesse o Airflow em `http://localhost:8080/`.

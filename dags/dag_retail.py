import datetime

from airflow import DAG
from airflow.decorators import task_group
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
)
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from astro import sql as aql
from astro.constants import FileType
from astro.files import File
from astro.sql.table import Metadata, Table
from cosmos import (
    DbtTaskGroup,
    ProfileConfig,
    ProjectConfig,
    RenderConfig,
)
from cosmos.constants import LoadMode

default_args = {
    "email_on_failure": False,
    "email_on_retry": False,
}

# GOOGLE CLOUD
DATASET = "sales_dataset"
CONN_ID = "google_cloud_retail"
BUCKET_NAME = "levy_online_retail"

# DBT
DEFAULT_DBT_ROOT_PATH = "/usr/local/airflow/include/dbt_retail/"
PROFILE_YAML_PATH = "/usr/local/airflow/include/dbt_retail/profiles.yml"
PROFILE_PROJECT_NAME = "dbt_retail"
TARGET_NAME = "dev"

DBT_PROFILE_CONFIG = ProfileConfig(
    profile_name=PROFILE_PROJECT_NAME,
    target_name=TARGET_NAME,
    profiles_yml_filepath=PROFILE_YAML_PATH,
)

DBT_PROJECT_CONFIG = ProjectConfig(dbt_project_path=DEFAULT_DBT_ROOT_PATH)

with DAG(
    "online_retail",
    default_args=default_args,
    description="Run retail pipeline",
    schedule=None,
    start_date=datetime.datetime(2024, 1, 1),
    tags=["retail"],
    catchup=False,
) as dag:
    # create bigquery dataset
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset", dataset_id=DATASET, gcp_conn_id=CONN_ID
    )

    # upload files to GCS, they are not chained because they can be run in parallel
    @task_group(group_id="upload_files")
    def upload_to_gcs():
        LocalFilesystemToGCSOperator(
            task_id="upload_stores",
            src="include/data/stores data-set.csv",
            bucket=BUCKET_NAME,
            dst="raw/stores data-set.csv",
            gcp_conn_id=CONN_ID,
            mime_type="text/csv",
        )

        LocalFilesystemToGCSOperator(
            task_id="upload_sales",
            src="include/data/sales data-set.csv",
            bucket=BUCKET_NAME,
            dst="raw/sales data-set.csv",
            gcp_conn_id=CONN_ID,
            mime_type="text/csv",
        )

        LocalFilesystemToGCSOperator(
            task_id="upload_features",
            src="include/data/Features data set.csv",
            bucket=BUCKET_NAME,
            dst="raw/Features data set.csv",
            gcp_conn_id=CONN_ID,
            mime_type="text/csv",
        )

    # load the files in GCS to Bigquery, also in parallel
    @task_group(group_id="load_files")
    def upload_to_bigquery_from_gcs():
        aql.load_file(
            task_id="load_stores_into_BQ",
            input_file=File(
                f"gs://{BUCKET_NAME}/raw/stores data-set.csv",
                conn_id=CONN_ID,
            ),
            output_table=Table("stores", metadata=Metadata(schema=DATASET), conn_id=CONN_ID),
            use_native_support=True,
        )

        aql.load_file(
            task_id="load_sales_into_BQ",
            input_file=File(
                f"gs://{BUCKET_NAME}/raw/sales data-set.csv",
                conn_id=CONN_ID,
                filetype=FileType.CSV,
            ),
            output_table=Table(
                "sales",
                metadata=Metadata(schema=DATASET),
                conn_id=CONN_ID,
            ),
            use_native_support=True,
        )

        aql.load_file(
            task_id="load_features_into_BQ",
            input_file=File(
                f"gs://{BUCKET_NAME}/raw/Features data set.csv",
                conn_id=CONN_ID,
            ),
            output_table=Table(
                "features",
                metadata=Metadata(schema=DATASET),
                conn_id=CONN_ID,
            ),
            use_native_support=True,
        )

    # dbt run staging models
    staging = DbtTaskGroup(
        group_id="staging",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_PROFILE_CONFIG,
        render_config=RenderConfig(load_method=LoadMode.DBT_LS, select=["path:models/staging"]),
    )

    # dbt run intermediate models
    intermediate = DbtTaskGroup(
        group_id="intermediate",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_PROFILE_CONFIG,
        render_config=RenderConfig(load_method=LoadMode.DBT_LS, select=["path:models/intermediate"]),
    )

    # dbt run mart models
    mart = DbtTaskGroup(
        group_id="mart",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_PROFILE_CONFIG,
        render_config=RenderConfig(load_method=LoadMode.DBT_LS, select=["path:models/mart"]),
    )

    # empty operators, begin and end
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    # chain the tasks, order of execution
    chain(
        begin,
        create_dataset,  # create dataset
        upload_to_gcs(),  # upload files
        upload_to_bigquery_from_gcs(),  # load files into BQ
        staging,  # dbt staging
        intermediate,  # dbt intermediate
        mart,  # dbt mart
        end,
    )

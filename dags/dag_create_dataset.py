import datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.dummy_operator import DummyOperator
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

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

DATASET = "sales_dataset"
CONN_ID = "google_cloud_retail"


with DAG(
    "create_dataset",
    default_args=default_args,
    description="Create a BigQuery dataset",
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    tags=["example"],
    catchup=False,
) as dag:
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset", dataset_id=DATASET, gcp_conn_id=CONN_ID
    )

    upload_stores = LocalFilesystemToGCSOperator(
        task_id="upload_stores",
        src="include/data/stores data-set.csv",
        bucket="levy_online_retail",
        dst="raw/stores data-set.csv",
        gcp_conn_id=CONN_ID,
        mime_type="text/csv",
    )

    upload_sales = LocalFilesystemToGCSOperator(
        task_id="upload_sales",
        src="include/data/sales data-set.csv",
        bucket="levy_online_retail",
        dst="raw/sales data-set.csv",
        gcp_conn_id=CONN_ID,
        mime_type="text/csv",
    )

    upload_features = LocalFilesystemToGCSOperator(
        task_id="upload_features",
        src="include/data/Features data set.csv",
        bucket="levy_online_retail",
        dst="raw/Features data set.csv",
        gcp_conn_id=CONN_ID,
        mime_type="text/csv",
    )

    stores_bq = aql.load_file(
        task_id="load_stores_into_BQ",
        input_file=File(
            "gs://levy_online_retail/raw/stores data-set.csv",
            conn_id=CONN_ID,
        ),
        output_table=Table(
            "stores", metadata=Metadata(schema="sales_dataset"), conn_id=CONN_ID
        ),
        use_native_support=True,
    )

    sales_bq = aql.load_file(
        task_id="load_sales_into_BQ",
        input_file=File(
            "gs://levy_online_retail/raw/sales data-set.csv",
            conn_id=CONN_ID,
            filetype=FileType.CSV,
        ),
        output_table=Table(
            "sales",
            metadata=Metadata(schema="sales_dataset"),
            conn_id=CONN_ID,
        ),
        use_native_support=True,
    )

    features_bq = aql.load_file(
        task_id="load_features_into_BQ",
        input_file=File(
            "gs://levy_online_retail/raw/Features data set.csv",
            conn_id=CONN_ID,
        ),
        output_table=Table(
            "features",
            metadata=Metadata(schema="sales_dataset"),
            conn_id=CONN_ID,
        ),
        use_native_support=True,
    )

    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end")

    chain(
        begin,
        create_dataset,
        [upload_stores, upload_sales, upload_features],
        [stores_bq, sales_bq, features_bq],
        end,
    )

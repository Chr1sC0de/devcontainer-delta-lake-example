import os
import pathlib as pt
from typing import Dict, Tuple

from pyspark.sql import DataFrame, SparkSession

from testlib.settings import Config


def initialize_tables(config: Config):
    from testlib.build import get_model

    model = get_model(config)

    for query in model.values():
        config.spark.sql(query)


def upload_to_raw_university(file_path: pt.Path, config: Config) -> Dict:
    assert file_path.exists()
    return config.s3_bucket_raw_university.upload_file(
        file_path.absolute(), f"in/{file_path.name}"
    )


def append_raw_csv_file_to_bronze_table(
    s3_path: str, table_name: str, config: Config
):
    config.spark.read.option("dateFormat", "yyyy-MM-dd").csv(
        s3_path, header=True, schema=config.spark.table(table_name).schema
    ).write.mode("append").format("delta").saveAsTable(table_name)


def get_active_students(
    start_date: str, end_date: str, config: Config
) -> DataFrame:
    base_query = """
        select
            S.first_name,
            S.last_name
        from
            university.enrollments as E
        inner join
            university.students as S on S.id = E.student_id
        inner join
            university.terms as T on T.id = E.term_id
    """

    return config.spark.sql(
        f"{base_query}\nwhere T.start_date >= date('{start_date}')"
        f" and T.end_date <= date('{end_date}')"
    )


def mock_environment_variables(
    master: str = None,
    metastore: bool = False,
    s3_endpoint: str = "http://127.0.0.1:5000",
):
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    pyspark_submit_args_list = [
        "--packages",
        "org.apache.hadoop:hadoop-aws:3.3.2,io.delta:delta-core_2.12:2.4.0",
        "--conf",
        "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension",
        "--conf",
        "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "--conf",
        "spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
        "--conf",
        "spark.hadoop.fs.s3a.access.key=testing",
        "--conf",
        "spark.hadoop.fs.s3a.secret.key=testing",
        "--conf",
        "spark.hadoop.com.amazonaws.services.s3.enableV4=true",
        "--conf",
        f"spark.hadoop.fs.s3a.endpoint={s3_endpoint}",
    ]

    if metastore:
        pyspark_submit_args_list.extend(
            ["--conf", "spark.sql.catalogImplementation=hive"]
        )
    if master:
        pyspark_submit_args_list = [
            "--master",
            master,
        ] + pyspark_submit_args_list

    pyspark_submit_args_list.append("pyspark-shell")
    pyspark_submit_args = " ".join(pyspark_submit_args_list)
    os.environ["PYSPARK_SUBMIT_ARGS"] = pyspark_submit_args

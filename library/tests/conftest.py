from testlib.functions import (
    append_raw_csv_file_to_bronze_table,
    upload_to_raw_university,
    mock_environment_variables,
)

import socket
import pytest

# from delta import configure_spark_with_delta_pip
# from delta import *
from moto import mock_s3
from moto.server import ThreadedMotoServer
from pyspark.sql import SparkSession
from testlib.settings import Config
import pathlib as pt
from typing import Tuple


mock_environment_variables()


def find_open_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return int(s.getsockname()[1])


@pytest.fixture(scope="session")
def mocked_server() -> Tuple[str, ThreadedMotoServer]:
    with mock_s3():
        ip_address = "127.0.0.1"
        port = find_open_port()
        endpoint_url = f"http://{ip_address}:{port}"
        server = ThreadedMotoServer(ip_address=ip_address, port=port)
        server.start()
        yield endpoint_url, server
    server.stop()


@pytest.fixture(scope="session")
def mock_spark(mocked_server: Tuple[str, str, ThreadedMotoServer]) -> Config:
    endpoint_url, server = mocked_server
    config = Config()
    config.endpoint_url = endpoint_url

    fixtures_path = pt.Path(__file__).parent / "fixtures/mock_table_data"

    csv_files = list((fixtures_path.glob("*.csv")))
    s3_paths_table = [
        (
            f"{config.s3_path_raw_bucket}/in/{file.name}",
            f"university.{file.stem}",
        )
        for file in csv_files
    ]

    target_solution = {
        "university.courses": (10, 3),
        "university.students": (10, 3),
        "university.terms": (4, 4),
        "university.enrollments": (20, 4),
    }

    config.s3_client.create_bucket(Bucket=config.name_bucket_bronze_university)
    config.s3_client.create_bucket(Bucket=config.name_bucket_raw_university)

    from testlib.functions import initialize_tables

    spark_session = SparkSession.builder.config(
        "spark.hadoop.fs.s3a.endpoint",
        endpoint_url,
    ).getOrCreate()

    config.set_spark(spark_session)
    initialize_tables(config)

    for file in csv_files:
        upload_to_raw_university(file, config)
        assert (
            len(
                list(
                    config.s3_bucket_raw_university.objects.filter(
                        Prefix=f"in/{file.name}"
                    )
                )
            )
            > 0
        ), f"{file.name} not uploaded"

    for path, table_name in s3_paths_table:
        append_raw_csv_file_to_bronze_table(path, table_name, config)

        pandas_df = config.spark.sql(f"select * from {table_name}").toPandas()

        assert pandas_df.shape == target_solution[table_name]

    yield config
    config.spark.stop()
    server.stop()


@pytest.fixture(scope="function")
def fixture_request(
    mock_spark: Config, request: pytest.FixtureRequest
) -> Tuple[Config, pytest.FixtureRequest]:
    yield mock_spark, *request.param

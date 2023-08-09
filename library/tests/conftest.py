import os

import pytest
from delta import configure_spark_with_delta_pip

# from delta import *
from moto import mock_s3
from moto.server import ThreadedMotoServer
from pyspark.sql import SparkSession
from testlib.functions import mock_environment_variables
from testlib.settings import config

ip_address = "127.0.0.1"
port = 5000
endpoint_url = f"http://{ip_address}:{port}"


@pytest.fixture(scope="session")
def aws_credentials():
    mock_environment_variables()


@pytest.fixture(scope="session")
def mock_services(
    aws_credentials,
):
    with mock_s3():
        server = ThreadedMotoServer(ip_address=ip_address, port=port)
        server.start()
        config.endpoint_url = endpoint_url
        yield config.s3_client, config.s3_resource

    server.stop()


@pytest.fixture(scope="session")
def create_buckets(mock_services):
    config.s3_client.create_bucket(Bucket=config.name_bucket_bronze_university)
    config.s3_client.create_bucket(Bucket=config.name_bucket_raw_university)


@pytest.fixture(scope="session")
def spark(create_buckets) -> SparkSession:
    from testlib.functions import initialize_tables

    spark_session = SparkSession.builder.getOrCreate()
    config.set_spark(spark_session)
    initialize_tables()

    return spark_session


@pytest.fixture(scope="session")
def mock_environment(spark, request):
    return request.param

import boto3
from mypy_boto3_s3.service_resource import S3ServiceResource, Bucket
from mypy_boto3_s3.client import S3Client
from functools import wraps

from pyspark.sql import SparkSession
from typing_extensions import Self


def cache(obj_method):
    @wraps(obj_method)
    def wrapper(obj, *args, **kwargs):
        cache_name = f"_{obj_method.__name__}"
        if not hasattr(obj, cache_name):
            setattr(obj, cache_name, obj_method(obj))
        return getattr(obj, cache_name)

    return wrapper


class Config:
    _singleton: SparkSession

    environment = "dev1"
    endpoint_url = None
    region_name = "us-east-1"

    def __new__(cls):
        if not hasattr(cls, "_singleton"):
            obj = super(cls.__class__, cls).__new__(cls)
            cls._singleton = obj
        return obj

    def set_spark(self, spark_session: SparkSession) -> Self:
        self._spark = spark_session

    @property
    @cache
    def spark(self) -> SparkSession:
        return SparkSession.builder.getOrCreate()

    @property
    def name_bucket_bronze_university(self) -> str:
        return f"company-edp-{self.environment}-bronze-university"

    @property
    def s3_path_bronze_bucket(self) -> str:
        return f"s3://{self.name_bucket_bronze_university}"

    @property
    def s3_path_bronze_university(self) -> str:
        return f"{self.s3_path_bronze_bucket}/bronze/university"

    @property
    @cache
    def s3_bucket_bronze_university(self) -> Bucket:
        return self.s3_resource.Bucket(self.name_bucket_bronze_university)

    @property
    def name_bucket_raw_university(self) -> str:
        return f"company-edp-{self.environment}-raw-university"

    @property
    def s3_path_raw_bucket(self) -> str:
        return f"s3://{self.name_bucket_raw_university}"

    @property
    @cache
    def s3_bucket_raw_university(self) -> Bucket:
        return self.s3_resource.Bucket(self.name_bucket_raw_university)

    @property
    @cache
    def s3_client(self) -> S3Client:
        return boto3.client(
            "s3", region_name=self.region_name, endpoint_url=self.endpoint_url
        )

    @property
    @cache
    def s3_resource(self) -> S3ServiceResource:
        return boto3.resource(
            "s3", endpoint_url=self.endpoint_url, region_name=self.region_name
        )


config = Config()

import pathlib as pt
from typing import Tuple

import pytest
from testlib.functions import (
    append_raw_csv_file_to_bronze_table,
    upload_to_raw_university,
)
from testlib.settings import config

fixtures_path = pt.Path(__file__).parent / "fixtures/mock_table_data"

csv_files = list((fixtures_path.glob("*.csv")))
s3_paths_table = [
    (f"{config.s3_path_raw_bucket}/in/{file.name}", f"university.{file.stem}")
    for file in csv_files
]


@pytest.mark.order(1)
@pytest.mark.parametrize(
    "mock_environment",
    csv_files,
    scope="session",
    indirect=True,
)
def test_upload_file(mock_environment: pt.Path):
    data = mock_environment
    upload_to_raw_university(data)

    assert (
        len(
            list(
                config.s3_bucket_raw_university.objects.filter(
                    Prefix=f"in/{data.name}"
                )
            )
        )
        > 0
    ), f"{data.name} not uploaded"


target_solution = {
    "university.courses": (10, 3),
    "university.students": (10, 3),
    "university.terms": (4, 4),
    "university.enrollments": (20, 4),
}


@pytest.mark.order(2)
@pytest.mark.parametrize(
    "mock_environment",
    s3_paths_table,
    scope="session",
    indirect=True,
)
def test_append_data(mock_environment: Tuple[str]):
    (s3_path, table_name) = mock_environment
    append_raw_csv_file_to_bronze_table(s3_path, table_name)

    pandas_df = config.spark.sql(
        f"select * from  {table_name} values"
    ).toPandas()

    assert pandas_df.shape == target_solution[table_name]


if __name__ == "__main__":
    pytest.main(args=["library/tests", "-k", pt.Path(__file__).stem])

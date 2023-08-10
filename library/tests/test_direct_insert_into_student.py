from typing import Tuple
from pyspark.sql import SparkSession
import pathlib as pt

import pandas as pd
import pytest
from testlib.settings import Config

clean_query = """
    delete from
        university.students
    where
        id = 100000
        and first_name = 'First'
        and last_name = 'Student'
"""


def test_direct_insert_into_student(mock_spark: Config):
    config = mock_spark
    config.spark.sql(clean_query)
    config.spark.sql(
        """
            insert into
                university.students
            values
                (100000, "First","Student")
        """
    )
    pandas_df = config.spark.sql(
        """
        select
            *
        from
            university.students
        where
            id = 100000
            and first_name = 'First'
            and last_name = 'Student'
        """
    ).toPandas()
    config.spark.sql(clean_query)
    assert all(
        (
            pandas_df
            == (
                pd.DataFrame(
                    {
                        "id": [100000],
                        "first_name": "First",
                        "last_name": "Student",
                    }
                )
            )
        )
        .to_numpy()
        .flatten()
        .squeeze()
    )


if __name__ == "__main__":
    pytest.main(args=["library/tests", "-k", pt.Path(__file__).stem])

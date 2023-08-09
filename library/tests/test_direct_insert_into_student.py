import pathlib as pt

import pandas as pd
import pytest
from pyspark.sql import SparkSession

clean_query = """
    delete from
        university.students
    where
        id = 100000
        and first_name = 'First'
        and last_name = 'Student'
"""


def test_direct_insert_into_student(spark: SparkSession):
    spark.sql(clean_query)
    spark.sql(
        """
            insert into
                university.students
            values
                (100000, "First","Student")
        """
    )
    pandas_df = spark.sql(
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
    spark.sql(clean_query)
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

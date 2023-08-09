import pathlib as pt

import pytest
from testlib.functions import get_active_students


def test_get_active_students(spark):
    assert get_active_students(
        start_date="2023-06-01", end_date="2023-07-01"
    ).toPandas().shape == (5, 2)
    return


if __name__ == "__main__":
    if False:
        pytest.main(
            args=[
                "library/tests",
                "-k",
                f"{pt.Path(__file__).stem} or test_upload_and_initliaze_dataframes",
            ]
        )
    else:
        from testlib.functions import mock_spark

        test_get_active_students(
            mock_spark(
                master="spark://32d5268f3b97:7077",
                app_name="Quick Test",
                metastore=True,
            )
        )

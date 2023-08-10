import pathlib as pt

import pytest
from testlib.functions import get_active_students


@pytest.mark.parametrize(
    "fixture_request",
    (
        ("2023-06-01", "2023-07-01", (5, 2)),
        ("2023-2-01", "2023-07-01", (18, 2)),
        ("2023-2-01", "2023-12-01", (20, 2)),
    ),
    indirect=True,
)
def test_get_active_students(fixture_request):
    config, start_date, end_date, solution = fixture_request
    assert (
        get_active_students(
            start_date=start_date, end_date=end_date, config=config
        )
        .toPandas()
        .shape
        == solution
    )

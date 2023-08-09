import pathlib as pt

from testlib.functions import (
    append_raw_csv_file_to_bronze_table,
    initialize_tables,
    mock_s3_assets,
    mock_spark,
    upload_to_raw_university,
)
from testlib.settings import config


def main():
    mock_s3_assets()
    mock_spark()
    initialize_tables()

    mock_table_files = list(
        (
            pt.Path(__file__).parent.parent
            / "library/tests/fixtures/mock_table_data"
        ).glob("*.csv")
    )

    s3_paths_table = [
        (
            f"{config.s3_path_raw_bucket}/in/{file.name}",
            f"university.{file.stem}",
        )
        for file in mock_table_files
    ]

    for file in mock_table_files:
        upload_to_raw_university(file)

    for s3_path, table_name in s3_paths_table:
        config.spark.sql(f"delete from {table_name}")
        append_raw_csv_file_to_bronze_table(s3_path, table_name)


if __name__ == "__main__":
    main()

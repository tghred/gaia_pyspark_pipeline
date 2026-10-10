# tests/test_spark_cleaner.py
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, LongType

from src.spark_cleaner import clean_gaia_pyspark


@pytest.fixture(scope="session")
def spark():
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("test")
        .getOrCreate()
    )


def test_clean_removes_null_rows(spark, tmp_path):
    data = [
        (1, 1.0, 1.0, 1.0, 1.0, 1.0),
        (2, None, 1.0, 1.0, 1.0, 1.0),
        (3, -1.0, 1.0, 1.0, 1.0, 1.0),  # parallax <= 0
    ]
    schema = StructType([
        StructField("source_id", LongType()),
        StructField("parallax", FloatType()),
        StructField("pmra", FloatType()),
        StructField("pmdec", FloatType()),
        StructField("bp_rp", FloatType()),
        StructField("phot_g_mean_mag", FloatType()),
    ])
    df = spark.createDataFrame(data, schema)

    input_path = tmp_path / "input.parquet"
    df.write.parquet(str(input_path))

    cleaned = clean_gaia_pyspark(str(input_path), spark=spark)
    assert cleaned.count() == 1
    assert cleaned.collect()[0]["source_id"] == 1
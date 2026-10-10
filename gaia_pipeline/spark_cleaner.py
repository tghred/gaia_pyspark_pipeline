import logging
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["parallax", "pmra", "pmdec", "bp_rp", "phot_g_mean_mag"]


def init_spark(app_name: str = "GaiaPipeline", driver_memory: str = "2g") -> SparkSession:
    """Initialize a lightweight local Spark session."""
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.driver.memory", driver_memory)
        .getOrCreate()
    )


def clean_gaia_pyspark(input_file: str, output_file: str | None = None, spark: SparkSession | None = None):
    """
    Read Parquet data with PySpark, drop missing values and non-positive parallax/magnitude,
    and optionally persist the result as Parquet.

    Returns
    -------
    pyspark.sql.DataFrame
        The cleaned Spark DataFrame.
    """
    if spark is None:
        spark = init_spark("GaiaDataCleaner")

    df_spark = spark.read.parquet(input_file)

    df_cleaned = (
        df_spark
        .dropna(subset=REQUIRED_COLUMNS)
        .filter((col("parallax") > 0) & (col("phot_g_mean_mag") > 0))
    )

    if output_file:
        df_cleaned.write.mode("overwrite").parquet(output_file)
        logger.info(f"Cleaned data written to {output_file}")

    return df_cleaned


def measure_scaling(df_spark, fractions=(0.2, 0.4, 0.6, 0.8, 1.0), seed: int = 42) -> pd.DataFrame:
    """
    Measure cleaning execution time across dataset fractions.

    Returns
    -------
    pandas.DataFrame
        Columns: 'Record Count', 'Execution Time (s)'.
    """
    results = []

    # Warm-up: prime the JVM before measuring anything
    _ = df_spark.limit(1).count()

    for frac in fractions:
        sample_df = df_spark.sample(withReplacement=False, fraction=frac, seed=seed)
        total_rows = sample_df.count()

        # Warm-up on this sample (excluded from timing)
        _ = sample_df.limit(1).count()

        start = time.perf_counter()
        _ = (
            sample_df
            .dropna(subset=REQUIRED_COLUMNS)
            .filter((col("parallax") > 0) & (col("phot_g_mean_mag") > 0))
            .count()
        )
        elapsed = time.perf_counter() - start

        logger.info(f"Scale {int(frac * 100)}% ({total_rows:,} rows): {elapsed:.3f}s")
        results.append({"Record Count": total_rows, "Execution Time (s)": elapsed})

    return pd.DataFrame(results)


def plot_scaling(bench_df: pd.DataFrame, output_image: str = "pyspark_performance.png"):
    """Plot the scaling benchmark results."""
    plt.figure(figsize=(9, 5))
    sns.set_theme(style="ticks")

    ax = sns.lineplot(
        data=bench_df, x="Record Count", y="Execution Time (s)",
        marker="o", linewidth=2.5, color="#1f77b4", markersize=8,
    )

    for _, row in bench_df.iterrows():
        ax.annotate(
            f"{row['Execution Time (s)']:.3f}s",
            (row["Record Count"], row["Execution Time (s)"]),
            textcoords="offset points", xytext=(0, 8),
            ha="center", fontsize=9, fontweight="bold",
        )

    plt.title("PySpark Data Cleaning Performance & Scalability", fontsize=13, fontweight="bold")
    plt.xlabel("Number of Processed Records (Stars)", fontsize=11)
    plt.ylabel("Execution Time (Seconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    if output_image:
        plt.savefig(output_image, dpi=300, bbox_inches="tight")
        logger.info(f"Scaling plot saved to {output_image}")

    plt.close()
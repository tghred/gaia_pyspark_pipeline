"""Entry point for the Gaia PySpark Pipeline.

Usage
-----
    python -m gaia_pipeline
    # or, after pip install -e .:
    gaia-pipeline
"""

import logging
import sys
from pathlib import Path

from gaia_pipeline.clustering import plot_cluster_results, run_dbscan_clustering
from gaia_pipeline.fetch_data import fetch_cluster_data
from gaia_pipeline.spark_cleaner import (
   clean_gaia_pyspark, init_spark, plot_scaling, measure_scaling,
)

logger = logging.getLogger(__name__)

# --- Configuration ---
RA_TARGET = 130.10       #(Praesepe / NGC 2632)
DEC_TARGET = 19.67      
RADIUS_TARGET = 2.5     

INPUT_PARQUET = "data/Praesepe_chunks.parquet"
PERFORMANCE_PLOT = "pyspark_performance_Praesepe.png"
CLUSTER_PLOT = "Praesepe_clusters.png"


def main() -> int:
    """Run the full pipeline end-to-end."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    print("=== Starting Gaia PySpark Pipeline (Big Data Mode) ===")

    # --- Step 1/4: Fetch data ---
    print(f"[1/4] Fetching Gaia DR3 data around (RA={RA_TARGET}, Dec={DEC_TARGET}, r={RADIUS_TARGET}°)...")
    try:
        fetch_cluster_data(
            ra=RA_TARGET, dec=DEC_TARGET, radius=RADIUS_TARGET,
            output_path=str(INPUT_PARQUET),
        )
    except Exception as e:
        logger.error(f"Failed to fetch Gaia data: {e}")
        return 1

    # --- Step 2/4: Clean with PySpark ---
    print("[2/4] Processing data with PySpark...")
    spark = init_spark()
    cleaned_spark_df = clean_gaia_pyspark(
        str(INPUT_PARQUET), spark=spark
    )

    # --- Step 3/4: Benchmark ---
    print("[3/4] Benchmarking performance across dataset sizes...")
    bench_df = measure_scaling(cleaned_spark_df)
    plot_scaling(bench_df, output_image=PERFORMANCE_PLOT)


    # --- Step 4/4: Cluster ---
    print("[4/4] Running multidimensional DBSCAN clustering...")
    clustered_pd_df = run_dbscan_clustering(
        cleaned_spark_df,
        eps=0.5,
        min_samples=15,
    )
    plot_cluster_results(clustered_pd_df, output_image=CLUSTER_PLOT)
    print(f"=== Pipeline completed successfully! Results saved to {CLUSTER_PLOT} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
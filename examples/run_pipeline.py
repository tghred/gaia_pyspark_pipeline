import sys
import os


from gaia_pipeline.clustering import plot_cluster_results, run_dbscan_clustering
from gaia_pipeline.fetch_data import fetch_cluster_data
from gaia_pipeline.spark_cleaner import clean_gaia_pyspark,benchmark_pyspark_performance



if __name__ == "__main__":
  print("=== Starting Gaia PySpark Pipeline (Big Data Mode) ===")

  print(
      "[1/3] Fetching stellar data in chunks from Gaia DR3 (pleiades Chunks)..."
  )
  ra_target = 56.75
  dec_target = 24.11
  radius_target = 1.0

  fetch_cluster_data(ra=ra_target, dec=dec_target, radius=radius_target)
  input_parquet = "pleiades_chunks.parquet"

  print("[2/3] Processing Big Data with PySpark...")
  cleaned_spark_df = clean_gaia_pyspark(input_parquet)

  print(
      "[3/3] Running Performance Benchmarking across different dataset sizes..."
  )
  benchmark_pyspark_performance(
      cleaned_spark_df, output_image="pyspark_performance.png"
  )

  print("[3/4] Running Multidimensional DBSCAN Clustering...")

  clustered_pd_df = run_dbscan_clustering(
      cleaned_spark_df,
      features=["ra", "dec", "parallax", "pmra", "pmdec"],
      eps=0.5,
      min_samples=15,
  )

  plot_cluster_results(
      clustered_pd_df, output_image="pleiades_clusters.png"
  )
  print(
      "=== Pipeline Completed Successfully! Results saved to"
      " orion_nebula_clusters.png ==="
  )
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gaia_pipeline.fetch_data import fetch_cluster_data
from gaia_pipeline.spark_cleaner import clean_gaia_pyspark, benchmark_pyspark_performance
from gaia_pipeline.clustering import run_dbscan_clustering, plot_cluster_results

def run_full_pipeline():
    print(" [1/3] Get Data from Gaia DR3 archive...")
    raw_file = "raw_pleiades.parquet"
    fetch_cluster_data(ra_center=56.75, dec_center=24.12, radius_deg=1.0, output_file=raw_file)
    
    print("\n [2/3] Start cleaning by PySpark...")
    df_spark = clean_gaia_pyspark(input_file=raw_file, output_file=None)
    
    benchmark_pyspark_performance(df_spark, output_image="pyspark_performance.png")
    
    print("\n [3/3] Start DBSCAN algorithm To Identify a Stellar Cluster...")
    df_clustered = run_dbscan_clustering(df_spark)
    
    print("\n  Generating Cluster Visualizations (VPD & CMD)...")
    plot_cluster_results(df_clustered, output_image="pleiades_cluster_plot.png")
    
    print("\n  Pipeline Successfully Done!")
    return df_clustered

if __name__ == "__main__":
    run_full_pipeline()
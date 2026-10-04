
---

# Module: `run_pipeline.py`

## Overview

The `run_pipeline.py` script serves as the master orchestration entry point for the `gaia_pyspark_pipeline` project. It executes the end-to-end workflow sequentially: querying astronomical data from the Gaia DR3 catalog, processing and cleaning the dataset in parallel using PySpark, benchmarking performance scalability, performing multidimensional machine learning clustering (DBSCAN), and generating final diagnostic visualizations.

## Workflow Execution Steps

When executed as the main script, the pipeline runs through the following stages:

1. **Data Ingestion (`[1/3]`):**
* Calls `fetch_cluster_data` targeting the Orion region coordinates (RA: `83.82°`, Dec: `-5.39°`, Radius: `1.5°`) to fetch massive multi-magnitude chunked data from Gaia DR3.


2. **Distributed Data Cleaning (`[2/3]`):**
* Initializes PySpark parallel processing via `clean_gaia_pyspark` to drop null values and filter out non-physical astrometric parameters (e.g., negative parallaxes).


3. **Performance Benchmarking (`[3/3]`):**
* Executes `benchmark_pyspark_performance` to evaluate runtime scalability across fractional dataset sizes, saving the output graph to `pyspark_performance.png`.


4. **Multidimensional Clustering & Visualization (`[3/4]`):**
* Runs `run_dbscan_clustering` utilizing standardized spatial and kinematic features (`ra`, `dec`, `parallax`, `pmra`, `pmdec`) with the DBSCAN algorithm (`eps=0.5`, `min_samples=15`).
* Generates and saves high-resolution diagnostic Vector Point Diagrams (VPD) and Color-Magnitude Diagrams (CMD) via `plot_cluster_results` into `orion_nebula_clusters.png`.



## Execution

To run the complete end-to-end pipeline from the terminal or Google Colab, execute:

```bash
python run_pipeline.py

```

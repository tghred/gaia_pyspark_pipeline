
# Interactive Demo & Quickstart

## Overview

The interactive demo notebook (`examples/demo.ipynb`) provides a complete, end-to-end walkthrough of the `gaia_pyspark_pipeline` project. It demonstrates how to query massive astrometric datasets from Gaia DR3, clean and process the data using parallel PySpark operations, run performance benchmarks, and perform multidimensional machine learning clustering (DBSCAN) to extract the Orion cluster with professional diagnostic plots.

## Run in Google Colab

You can run the demo interactively in your browser with zero local configuration via Google Colab:

## Demo Workflow Steps

The notebook guides you through the following core phases:

1. **Environment Setup:** Installs required dependencies (`astroquery`, `pyspark`, `pyarrow`) and initializes a local Spark session.
2. **Data Acquisition:** Fetches multi-magnitude chunked astrometric data for the Orion region using `fetch_cluster_data`.
3. **Data Cleaning & Benchmarking:** Filters out unphysical parameters (such as negative parallaxes) and evaluates execution scalability across various dataset volumes using PySpark.
4. **Machine Learning Clustering:** Applies `run_dbscan_clustering` on standardized spatial and kinematic features (`ra`, `dec`, `parallax`, `pmra`, `pmdec`).
5. **Visualization:** Generates and exports high-resolution diagnostic **Vector Point Diagrams (VPD)** and **Color-Magnitude Diagrams (CMD)** to verify cluster membership.

---




# Module: `__init__.py` (Package: `gaia_pipeline`)

## Overview

The `__init__.py` file initializes the `gaia_pipeline` package. It defines the core package metadata (version and author) and exposes the primary functional modules at the package level via `__all__`, enabling a clean, flat import structure for end-users.

## Package Metadata

* **Package Name:** `gaia_pipeline`
* **Description:** A lightweight pipeline for open cluster extraction using Apache Spark and Gaia DR3 data.
* **Version (`__version__`):** `0.1.0`
* **Author (`__authour__`):** Taghreed Salah Ashry

## Exposed Public API (`__all__`)

The package exports the following core functions directly from its top-level namespace:

1. **`fetch_cluster_data`** (imported from `gaia_pipeline.fetch_data`)
* *Purpose:* Handles asynchronous ADQL querying and chunked Parquet downloading of Gaia DR3 data.


2. **`init_spark`** (imported from `gaia_pipeline.spark_cleaner`)
* *Purpose:* Initializes and configures the local Apache Spark session.


3. **`clean_gaia_pyspark`** (imported from `gaia_pipeline.spark_cleaner`)
* *Purpose:* Executes parallel data cleaning and astrometric quality filtering.


4. **`run_dbscan_clustering`** (imported from `gaia_pipeline.clustering`)
* *Purpose:* Performs feature scaling and machine learning cluster analysis using DBSCAN.



## Example Usage

With this clean initialization, users can import functions directly from the package root:

```python
from gaia_pipeline import (
    init_spark,
    fetch_cluster_data,
    clean_gaia_pyspark,
    run_dbscan_clustering
)

# Initialize Spark session
spark = init_spark()

# Fetch data for a target cluster region
fetch_cluster_data(ra=83.82, dec=-5.39, radius=1.5)

```

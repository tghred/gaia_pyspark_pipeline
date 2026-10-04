
---

# Module: `spark_cleaner.py`

## Overview

The `spark_cleaner.py` module manages Apache Spark session initialization, large-scale data cleaning, quality filtering of Gaia astrometric records, and performance benchmarking across varying dataset sizes. It leverages PySpark for parallel processing to efficiently handle and clean large parquet datasets.

## Functions

---

### `init_spark()`

Initializes and configures a lightweight local Apache Spark Session.

* **Parameters:** None.
* **Workflow:**
* Creates a `SparkSession` with the application name `"GaiaPipeline"`.
* Configures driver memory allocation (`spark.driver.memory` set to `2g`).


* **Returns:**
* `spark` (*pyspark.sql.SparkSession*): The active Spark session instance.



---

### `clean_gaia_pyspark(input_file, output_file=None, spark=None)`

Reads parquet dataset files via PySpark, applies rigorous astrometric quality filters, and optionally exports the cleaned subset to disk.

* **Parameters:**
* `input_file` (*str*): Path to the input Parquet data file.
* `output_file` (*str, optional*): Path where the cleaned dataset will be saved as a Parquet file. Default is `None`.
* `spark` (*pyspark.sql.SparkSession, optional*): Active Spark session. If `None`, a new session is initialized automatically.


* **Workflow:**
1. **Session Check:** Initializes a Spark session if none is provided.
2. **Data Ingestion:** Reads the raw Parquet file into a PySpark DataFrame.
3. **Quality Filtering:** Removes rows containing null values in essential astrometric columns (`parallax`, `pmra`, `pmdec`, `bp_rp`, `phot_g_mean_mag`) and filters for physically valid parameters (`parallax > 0` and `phot_g_mean_mag > 0`).
4. **Serialization:** If an `output_file` string path is provided, converts the cleaned PySpark DataFrame to a Pandas DataFrame and writes it to disk in Parquet format.


* **Returns:**
* `df_cleaned` (*pyspark.sql.SparkSession DataFrame*): The filtered and cleaned PySpark DataFrame.



---

### `benchmark_pyspark_performance(df_spark, output_image="pyspark_performance.png")`

Measures and evaluates PySpark data cleaning execution times across multiple dataset volume fractions, generating a performance scalability graph.

* **Parameters:**
* `df_spark` (*pyspark.sql.DataFrame*): The source PySpark DataFrame to benchmark.
* `output_image` (*str, optional*): Filename/path where the scalability visualization plot will be saved. Default is `"pyspark_performance.png"`.


* **Workflow:**
1. **Sampling Fractions:** Iterates through dataset fractions `[0.2, 0.4, 0.6, 0.8, 1.0]`.
2. **Execution Timing:** Measures the exact runtime required to apply cleaning filters and execute actions (`count()`) at each scale level.
3. **Visualization & Annotation:** Plots execution times against record counts using `seaborn` and `matplotlib`, annotating each data point with its exact timing.
4. **Export:** Saves the high-resolution performance chart (`dpi=300`) to disk and displays it.


* **Returns:**
* None. (Saves performance plot and prints benchmark metrics to the console).



## Example Usage

```python
from spark_cleaner import init_spark, clean_gaia_pyspark, benchmark_pyspark_performance

# 1. Initialize Spark session
spark = init_spark()

# 2. Clean dataset and filter invalid records
df_cleaned = clean_gaia_pyspark("massive_orion_chunks.parquet", output_file="cleaned_orion.parquet", spark=spark)

# 3. Run performance scalability benchmark
benchmark_pyspark_performance(df_cleaned, output_image="examples/pyspark_performance.png")

```

---


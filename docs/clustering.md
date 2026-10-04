

# Module: `clustering.py`

## Overview

The `clustering.py` module handles machine learning-based cluster analysis for astronomical data. It supports processing both PySpark DataFrames and NumPy arrays, applies feature scaling using `StandardScaler`, and performs spatial and kinematic clustering using the **DBSCAN** algorithm. Additionally, it provides diagnostic visualization tools to generate Vector Point Diagrams (VPD) and Color-Magnitude Diagrams (CMD) for cluster verification.

## Functions

---

### `run_dbscan_clustering(df_spark, features=['ra', 'dec', 'parallax', 'pmra', 'pmdec'], eps=0.5, min_samples=15)`

Converts input data (PySpark DataFrame or NumPy array), standardizes the features, and applies the DBSCAN clustering algorithm.

* **Parameters:**
* `df_spark` (*pyspark.sql.DataFrame* or *numpy.ndarray*): The input dataset containing astrometric features.
* `features` (*list of str*, optional): List of column names to use for clustering. Default is `['ra', 'dec', 'parallax', 'pmra', 'pmdec']`.
* `eps` (*float*, optional): The maximum distance between two samples for one to be considered as in the neighborhood of the other (DBSCAN `eps` parameter). Default is `0.5`.
* `min_samples` (*int*, optional): The number of samples in a neighborhood for a point to be considered as a core point (DBSCAN `min_samples` parameter). Default is `15`.


* **Workflow:**
1. **Input Validation & Conversion:** Checks if the input is a NumPy array; otherwise, converts the PySpark DataFrame to a Pandas DataFrame (`toPandas()`), drops null values in the selected feature subset, and extracts the feature matrix.
2. **Feature Scaling:** Normalizes the features using `StandardScaler` (zero mean and unit variance) to ensure equal weighting during distance calculations.
3. **DBSCAN Execution:** Fits the `DBSCAN` model on the scaled features and predicts cluster labels.
4. **Label Assignment:** Appends the resulting cluster labels as a new column (`cluster_Label`) to the Pandas DataFrame.


* **Returns:**
* `pdf` (*pandas.DataFrame*): The processed DataFrame containing the original data plus the `cluster_Label` column.



---

### `plot_cluster_results(pdf, output_image='cluster_plots.png')`

Generates and saves diagnostic dual-panel plots (Vector Point Diagram and Color-Magnitude Diagram) to visually inspect and verify the identified stellar clusters and background noise.

* **Parameters:**
* `pdf` (*pandas.DataFrame*): The DataFrame containing astrometric measurements and `cluster_Label`.
* `output_image` (*str*, optional): The filename/path where the high-resolution plot will be saved. Default is `'cluster_plots.png'`.


* **Workflow:**
1. **Data Preparation:** Copies the DataFrame and casts `cluster_Label` to string format to guarantee discrete automatic color mapping in `seaborn`.
2. **Subplot 1 (VPD):** Plots Proper Motion Right Ascension (`pmra`) versus Proper Motion Declination (`pmdec`) to display kinematic clustering.
3. **Subplot 2 (CMD):** Plots color index (`bp_rp`) versus apparent magnitude (`phot_g_mean_mag`) with an inverted y-axis to display stellar evolutionary sequences.
4. **Export:** Adjusts layout, saves the figure at high resolution (`dpi=300`), displays it, and closes the plot context.


* **Returns:**
* None. (Saves the plot directly to disk and displays it).



## Example Usage

```python
from clustering import run_dbscan_clustering, plot_cluster_results

# 1. Run DBSCAN clustering on the dataset
clustered_df = run_dbscan_clustering(df_spark, eps=0.4, min_samples=10)

# 2. Generate and save the diagnostic VPD and CMD plots
plot_cluster_results(clustered_df, output_image="examples/orion_cluster_plot.png")

```

---


from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_dbscan_clustering(
    df_spark,
    features=["ra", "dec", "parallax", "pmra", "pmdec"],
    eps=0.5,
    min_samples=15,
):
  """Converts PySpark DataFrame or Numpy Array, applies scaling, and runs DBSCAN"""
  if isinstance(df_spark, np.ndarray):
    X = df_spark
    pdf = pd.DataFrame(df_spark, columns=features)
  else:
    pdf = df_spark.toPandas()

    valid_features = [f for f in features if f in pdf.columns]
    pdf = pdf.dropna(subset=valid_features).copy()
    X = pdf[valid_features].values

  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)

  dbscan = DBSCAN(eps=eps, min_samples=min_samples)
  labels = dbscan.fit_predict(X_scaled)

  pdf["cluster_Label"] = labels

  return pdf


def plot_cluster_results(pdf, output_image="cluster_plots.png"):
  """Generates and saves Vector Point Diagram (VPD) and

  Color-Magnitude Diagram (CMD) for DBSCAN clusters.
  """
  fig, axes = plt.subplots(1, 2, figsize=(12, 5))

  # Vector Point Diagram (VPD)
  if "pmra" in pdf.columns and "pmdec" in pdf.columns:
    sns.scatterplot(
        data=pdf,
        x="pmra",
        y="pmdec",
        hue="cluster_Label",
        palette="tab10",
        ax=axes[0],
        s=10,
        alpha=0.7,
        legend=False,
    )
    axes[0].set_title("Vector Point Diagram (VPD)")
    axes[0].set_xlabel("Proper Motion RA (pmra)")
    axes[0].set_xlabel("Proper Motion Dec (pmdec)")

  # Color-Magnitude Diagram (CMD) إذا توفرت البيانات
  if "bp_rp" in pdf.columns and "phot_g_mean_mag" in pdf.columns:
    sns.scatterplot(
        data=pdf,
        x="bp_rp",
        y="phot_g_mean_mag",
        hue="cluster_Label",
        palette="tab10",
        ax=axes[1],
        s=10,
        alpha=0.7,
        legend=False,
    )
    axes[1].set_title("Color-Magnitude Diagram (CMD)")
    axes[1].set_xlabel("BP - RP Color")
    axes[1].set_ylabel("G Magnitude")
    axes[1].invert_yaxis()

  plt.tight_layout()
  plt.savefig(output_image, dpi=300)
  plt.close()
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

import matplotlib.pyplot as plt
import seaborn as sns


def run_dbscan_clustering(df_spark, features=["parallax", "pmra", "pmdec"], eps=0.3, min_samples=10):
    """Converts PySpark DataFrame or Numpy Array, applies scaling, and runs DBSCAN."""
    
    if isinstance(df_spark, np.ndarray):
        X = df_spark
    else:
        pdf = df_spark.select(features).toPandas()
        X = pdf[features].values
        
    #  (Standardization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)
    
    return labels


def plot_cluster_results(pdf, output_image="cluster_plots.png"):
    """
    Generates and saves Vector Point Diagram (VPD) and 
    Color-Magnitude Diagram (CMD) for DBSCAN clusters.
    """
    plt.figure(figsize=(13, 5))
    

    
    sns.set_theme(style="ticks")
    
    # Vector Point Diagram (VPD)
    plt.subplot(1, 2, 1)
    sns.scatterplot(
        data=pdf, x="pmra", y="pmdec", 
        hue="cluster_label", palette="viridis", 
        alpha=0.8, s=30
    )
    plt.title("Vector Point Diagram (Proper Motion)", fontsize=12, fontweight='bold')
    plt.xlabel("pmra (mas/yr)")
    plt.ylabel("pmdec (mas/yr)")
    plt.grid(True, linestyle="--", alpha=0.5)

    #Color-Magnitude Diagram (CMD)
    plt.subplot(1, 2, 2)
    sns.scatterplot(
        data=pdf, x="bp_rp", y="phot_g_mean_mag", 
        hue="cluster_label", palette="viridis", 
        alpha=0.8, s=30
    )

    plt.gca().invert_yaxis()
    plt.title("Color-Magnitude Diagram (CMD)", fontsize=12, fontweight='bold')
    plt.xlabel("BP - RP (Color Index)")
    plt.ylabel("G (Apparent Magnitude)")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    
    if output_image:
        plt.savefig(output_image, dpi=300, bbox_inches='tight')
        print(f" Visualization saved successfully to '{output_image}'")
        print(f"Visualization saved successfully to '{output_image}'")
        
    plt.show()

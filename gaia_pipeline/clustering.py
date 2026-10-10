import logging
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

DEFAULT_FEATURES = ["ra", "dec", "parallax", "pmra", "pmdec"]


def run_dbscan_clustering(
    df_input,
    features: Iterable[str] = DEFAULT_FEATURES,
    eps: float = 0.5,
    min_samples: int = 15,
) -> pd.DataFrame:
    """
    Run DBSCAN clustering on 5D phase-space features.

    Parameters
    ----------
    df_input : pyspark.sql.DataFrame or numpy.ndarray or pandas.DataFrame
        Input data.
    features : list of str
        Columns to use for clustering.
    eps : float
        DBSCAN neighborhood radius.
    min_samples : int
        DBSCAN minimum samples per cluster.

    Returns
    -------
    pandas.DataFrame
        Input data with an added 'cluster_label' column.
    """
    if isinstance(df_input, np.ndarray):
        X = df_input
        pdf = pd.DataFrame(df_input, columns=list(features))
    elif isinstance(df_input, pd.DataFrame):
        pdf = df_input.copy()
        valid = [f for f in features if f in pdf.columns]
        if len(valid) < len(features):
            missing = set(features) - set(valid)
            logger.warning(f"Missing features: {missing}. Proceeding with {valid}.")
        pdf = pdf.dropna(subset=valid)
        X = pdf[valid].values
    else:
        # PySpark DataFrame
        pdf = df_input.toPandas()
        valid = [f for f in features if f in pdf.columns]
        pdf = pdf.dropna(subset=valid).copy()
        X = pdf[valid].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X_scaled)
    pdf["cluster_label"] = labels

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = int((labels == -1).sum())
    logger.info(f"DBSCAN: {n_clusters} clusters, {n_noise} noise points.")

    return pdf


def plot_cluster_results(
    pdf: pd.DataFrame,
    label_col: str = "cluster_label",
    output_image: str = "cluster_plots.png",
):
    """Plot VPD and CMD diagrams colored by cluster label."""
    if label_col not in pdf.columns:
        raise ValueError(f"Column '{label_col}' not found in DataFrame.")

    pdf = pdf.copy()
    pdf[label_col] = pdf[label_col].astype(str)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.scatterplot(
        data=pdf, x="pmra", y="pmdec", hue=label_col,
        palette="tab10", ax=axes[0], s=10, alpha=0.7,
    )
    axes[0].set_title("Vector Point Diagram (VPD)")
    axes[0].legend(title="Clusters", loc="upper right", fontsize="small")

    sns.scatterplot(
        data=pdf, x="bp_rp", y="phot_g_mean_mag", hue=label_col,
        palette="tab10", ax=axes[1], s=10, alpha=0.7, legend=False,
    )
    axes[1].set_title("Color-Magnitude Diagram (CMD)")
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Cluster plots saved to {output_image}")
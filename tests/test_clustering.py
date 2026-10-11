# tests/test_clustering.py
import numpy as np
import pandas as pd
from src.clustering import run_dbscan_clustering


def test_dbscan_finds_two_clusters():
    # Two well-separated Gaussian blobs
    rng = np.random.default_rng(42)
    blob1 = rng.normal(0, 0.1, (100, 2))
    blob2 = rng.normal(5, 0.1, (100, 2))
    X = np.vstack([blob1, blob2])

    result = run_dbscan_clustering(
        X, features=["f1", "f2"], eps=0.5, min_samples=5
    )
    n_clusters = result["cluster_label"].nunique() - (1 if -1 in result["cluster_label"].values else 0)
    assert n_clusters == 2
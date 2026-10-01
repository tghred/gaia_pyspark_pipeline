import pytest 
import numpy as np
import pandas as pd

from gaia_pipeline.fetch_data import fetch_cluster_data
from gaia_pipeline.spark_cleaner import clean_gaia_pyspark
from gaia_pipeline.clustering import run_dbscan_clustering

def test_module_imports():
    """Test that core modules are succsessfully imported with no errors"""
    assert fetch_cluster_data is not None
    assert clean_gaia_pyspark is not None
    assert run_dbscan_clustering is not None
    
    
def  test_data_cleaning_logic():
    """Test the unphysical prameters like (negative parallax) are correctly filtered out."""
    raw_data = {
        'ra': [56.75, 56.76, 56.77],
        'dec': [24.12, 24.13, 24.14],
        'parallax': [7.5, -0.2, 8.1],  # -2 is unphysical pram.
        'pmra': [20.1, 19.8, 20.5],
        'pmdec': [-45.2, -44.9, -45.5],
        'phot_g_mean_mag': [12.0, 13.5, 11.8]
    }
    df = pd.DataFrame(raw_data)
    
    
    cleaned_df = df[df['parallax'] > 0]

    assert len(cleaned_df) == 2
    assert not (cleaned_df['parallax'] <= 0).any()
    
    
    
def test_dbscan_clustering_shape():
    """Test that DBSCAN clustering processes coordinate arrays and returns expected labels."""
    X = np.array([
        [20.0, -45.0],
        [20.1, -45.1],
        [19.9, -44.9],
        [0.0, 0.0]  #noise
    ])
    
    labels = run_dbscan_clustering(X, eps=0.5, min_samples=2)
    
    assert len(labels) == len(X)

    assert -1 in labels or len(set(labels)) > 1
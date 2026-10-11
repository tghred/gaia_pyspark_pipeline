# tests/test_fetch_data.py
import time
from pathlib import Path

import pandas as pd
import pytest
import requests
from astropy.table import Table

from gaia_pipeline.fetch_data import fetch_cluster_data


# ---------- Fixtures ----------

@pytest.fixture
def fake_gaia_table():
    """Return a small fake Gaia result table."""
    return Table({
        "source_id": [1, 2, 3],
        "ra": [56.75, 56.76, 56.77],
        "dec": [24.11, 24.12, 24.13],
        "parallax": [7.5, 7.6, 7.4],
        "pmra": [10.0, 10.1, 9.9],
        "pmdec": [-5.0, -5.1, -4.9],
        "bp_rp": [0.5, 0.6, 0.4],
        "phot_g_mean_mag": [12.0, 12.5, 13.0],
    })


class FakeJob:
    """A stub for the object returned by Gaia.launch_job_async."""
    def __init__(self, table):
        self._table = table

    def get_results(self):
        return self._table


# ---------- Tests ----------

def test_fetch_cluster_data_saves_parquet(monkeypatch, tmp_path, fake_gaia_table):
    """Happy path: fetch data, save it as Parquet, and return the path."""
    def fake_launch_job_async(query):
        return FakeJob(fake_gaia_table)

    monkeypatch.setattr(
        "gaia_pipeline.fetch_data.Gaia.launch_job_async",
        fake_launch_job_async,
    )
    # Avoid real sleeps during tests
    monkeypatch.setattr("gaia_pipeline.fetch_data.time.sleep", lambda s: None)

    output = tmp_path / "test.parquet"
    result_path = fetch_cluster_data(
        ra=56.75, dec=24.11, radius=1.0,
        output_path=str(output),
    )

    assert Path(result_path).exists()
    df = pd.read_parquet(result_path)
    assert len(df) == 9  # 3 chunks × 3 rows each
    assert "ra" in df.columns
    assert "dec" in df.columns
    assert "phot_g_mean_mag" in df.columns


def test_fetch_cluster_data_retries_on_http_error(monkeypatch, tmp_path, fake_gaia_table):
    """If the first call raises HTTPError, the function should retry and succeed."""
    calls = {"count": 0}

    def flaky_launch_job_async(query):
        calls["count"] += 1
        if calls["count"] == 1:
            raise requests.exceptions.HTTPError("500 Server Error")
        return FakeJob(fake_gaia_table)

    monkeypatch.setattr(
        "gaia_pipeline.fetch_data.Gaia.launch_job_async",
        flaky_launch_job_async,
    )
    monkeypatch.setattr("gaia_pipeline.fetch_data.time.sleep", lambda s: None)

    output = tmp_path / "test.parquet"
    result_path = fetch_cluster_data(
        ra=56.75, dec=24.11, radius=1.0,
        output_path=str(output),
        retries=3,
    )
    assert Path(result_path).exists()
    assert calls["count"] >= 2  # at least one failure + one success


def test_fetch_cluster_data_raises_when_all_retries_fail(monkeypatch, tmp_path):
    """If all retries fail, a RuntimeError should be raised."""
    def always_fail(query):
        raise requests.exceptions.HTTPError("500 Server Error")

    monkeypatch.setattr(
        "gaia_pipeline.fetch_data.Gaia.launch_job_async",
        always_fail,
    )
    monkeypatch.setattr("gaia_pipeline.fetch_data.time.sleep", lambda s: None)

    output = tmp_path / "test.parquet"
    with pytest.raises(RuntimeError):
        fetch_cluster_data(
            ra=56.75, dec=24.11, radius=1.0,
            output_path=str(output),
            retries=2,
        )


def test_fetch_cluster_data_creates_output_directory(monkeypatch, tmp_path, fake_gaia_table):
    """The function should create parent directories if they don't exist."""
    def fake_launch_job_async(query):
        return FakeJob(fake_gaia_table)

    monkeypatch.setattr(
        "gaia_pipeline.fetch_data.Gaia.launch_job_async",
        fake_launch_job_async,
    )
    monkeypatch.setattr("gaia_pipeline.fetch_data.time.sleep", lambda s: None)

    output = tmp_path / "nested" / "dir" / "test.parquet"
    result_path = fetch_cluster_data(
        ra=56.75, dec=24.11, radius=1.0,
        output_path=str(output),
    )
    assert Path(result_path).exists()


def test_fetch_cluster_data_respects_magnitude_bins(monkeypatch, tmp_path, fake_gaia_table):
    """The number of query calls should match the number of magnitude bins."""
    queries = []

    def capture_query(query):
        queries.append(query)
        return FakeJob(fake_gaia_table)

    monkeypatch.setattr(
        "gaia_pipeline.fetch_data.Gaia.launch_job_async",
        capture_query,
    )
    monkeypatch.setattr("gaia_pipeline.fetch_data.time.sleep", lambda s: None)

    output = tmp_path / "test.parquet"
    fetch_cluster_data(
        ra=56.75, dec=24.11, radius=1.0,
        output_path=str(output),
        mag_bins=[(10, 16), (16, 18), (18, 20)],
    )
    assert len(queries) == 3
    for q in queries:
        assert "gaiadr3.gaia_source" in q
        assert "CIRCLE" in q
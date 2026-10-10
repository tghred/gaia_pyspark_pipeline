import os
import time
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from astroquery.gaia import Gaia

logger = logging.getLogger(__name__)


def fetch_cluster_data(
    ra: float,
    dec: float,
    radius: float,
    limit: int = 50000,
    output_path: str = "data/raw/pleiades_chunks.parquet",
    mag_bins: Optional[list] = None,
    retries: int = 3,
    initial_delay: float = 5.0,
) -> str:
    """
    Fetch Gaia DR3 data around a sky position in magnitude chunks,
    with automatic retry on server errors. Saves the result as Parquet.

    Parameters
    ----------
    ra, dec : float
        Center coordinates in degrees (ICRS).
    radius : float
        Search radius in degrees.
    limit : int
        Maximum number of sources per magnitude bin.
    output_path : str
        Where to save the resulting Parquet file.
    mag_bins : list of tuples, optional
        Magnitude bins to query. Defaults to [(10, 16), (16, 18), (18, 20)].
    retries : int
        Number of retries per chunk.
    initial_delay : float
        Initial delay before retry (doubles on each attempt).

    Returns
    -------
    str
        Path to the saved Parquet file.

    Raises
    ------
    RuntimeError
        If no data could be fetched.
    """
    if mag_bins is None:
        mag_bins = [(10.0, 16.0), (16.0, 18.0), (18.0, 20.0)]

    all_chunks = []

    for min_mag, max_mag in mag_bins:
        logger.info(f"Fetching chunk: {min_mag} <= G <= {max_mag}")

        adql_query = f"""
            SELECT TOP {limit} source_id, ra, dec, parallax,
                   pmra, pmdec, bp_rp, phot_g_mean_mag
            FROM gaiadr3.gaia_source
            WHERE CONTAINS(
                POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec),
                CIRCLE('ICRS', {ra}, {dec}, {radius})
            ) = 1
              AND phot_g_mean_mag BETWEEN {min_mag} AND {max_mag}
        """

        delay = initial_delay
        for attempt in range(retries):
            try:
                job = Gaia.launch_job_async(adql_query)
                result = job.get_results()
                all_chunks.append(result.to_pandas())
                logger.info(f"  -> {len(result)} records fetched.")
                break
            except requests.exceptions.HTTPError as e:
                logger.warning(
                    f"  -> HTTP error (attempt {attempt + 1}/{retries}): {e}. "
                    f"Retrying in {delay}s..."
                )
                time.sleep(delay)
                delay *= 2
            except Exception as e:
                logger.error(f"  -> Unexpected error: {e}")
                raise

        time.sleep(3)  # be polite to the Gaia archive

    if not all_chunks:
        raise RuntimeError(
            "No data fetched from Gaia. Check your query and network connection."
        )

    final_df = pd.concat(all_chunks, ignore_index=True)

    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    final_df.to_parquet(output_path, index=False)
    logger.info(f"Saved {len(final_df)} records to {output_path}")

    return str(output_path)
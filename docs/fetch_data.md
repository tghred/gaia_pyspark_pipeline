

### Module: `fetch_data.py`

#### Overview

The `fetch_data.py` module is responsible for querying astronomical data from the **Gaia DR3** catalog using `astroquery`. To handle potential query limits and ensure a balanced dataset across different magnitudes, it implements a chunk-based fetching strategy across defined magnitude bins and saves the consolidated data into an optimized Parquet file using `pyarrow`.

#### Functions

---

##### `fetch_cluster_data(ra, dec, radius, limit=20000)`

Queries Gaia DR3 sources within a specified sky region and magnitude range, then appends the results into a single Apache Parquet file.

* **Parameters:**
* `ra` (*float*): Right Ascension of the target cluster center in degrees (ICRS).
* `dec` (*float*): Declination of the target cluster center in degrees (ICRS).
* `radius` (*float*): Search radius in degrees around the center coordinates.
* `limit` (*int*, optional): Maximum number of rows to fetch per magnitude bin. Default is `20000`.


* **Workflow:**
1. **Magnitude Bins Iteration:** Splits the query into specific apparent magnitude (`phot_g_mean_mag`) ranges `[(10.0, 16.0), (16.0, 18.5), (18.5, 20.5)]` to ensure comprehensive sampling.


2. **ADQL Query Execution:** Constructs an Astronomical Data Query Language (ADQL) statement utilizing spatial filtering (`CONTAINS(POINT(...), CIRCLE(...))`) and magnitude filtering.


3. **Asynchronous Job Launch:** Uses `Gaia.launch_job_async` to execute the query against the ESA Gaia archive.
4. **Parquet Serialization:** Converts the results to a Pandas DataFrame, transforms them into a Pyarrow Table, and iteratively writes or appends them to `massive_orion_chunks.parquet`.
5. **Rate Limiting:** Includes a short delay (`time.sleep(2)`) between requests to respect server limits.


* **Returns:**
* None. (Saves the final aggregated dataset directly to disk as `massive_orion_chunks.parquet`).



#### Example Usage

```python
from fetch_data import fetch_cluster_data

# Example: Fetching data around the Orion Nebula Cluster (ONC)
# RA: ~83.82°, Dec: ~-5.39°, Radius: 0.5°
fetch_cluster_data(ra=83.82, dec=-5.39, radius=0.5, limit=20000)

```


import time
from astroquery.gaia import Gaia
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def fetch_cluster_data(ra, dec, radius, limit= 30000):
  mag_bins = [
      (10.0, 16.0),
      (16.0, 18.5),
      (18.5, 20.5),]
  output_file = "massive_orion_chunks.parquet"
  first_chunk = True

  for min_mag, max_mag in mag_bins:
    print(
        f"Fetching massive chunk: Magnitude between {min_mag} and {max_mag}..."
    )

    adql_query = f"""
            SELECT TOP {limit} source_id, ra, dec, parallax, pmra, pmdec, bp_rp, phot_g_mean_mag
            FROM gaiadr3.gaia_source
            WHERE CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), 
                           CIRCLE('ICRS', {ra}, {dec}, {radius})) = 1
            AND phot_g_mean_mag BETWEEN {min_mag} AND {max_mag}
        """

    job = Gaia.launch_job_async(adql_query)
    r = job.get_results()
    df_chunk = r.to_pandas()

    if not df_chunk.empty:
      table = pa.Table.from_pandas(df_chunk)
      if first_chunk:
        pq.write_table(table, output_file)
        first_chunk = False
      else:
        existing_table = pq.read_table(output_file)
        combined_table = pa.concat_tables([existing_table, table])
        pq.write_table(combined_table, output_file)

    print(f"Chunk saved. Rows in this chunk: {len(df_chunk)}")
    time.sleep(2)

  final_table = pq.read_table(output_file)
  print(
      f"=== Total Massive Dataset Ready! Total Rows: {len(final_table):,}"
      " ==="
  )
import time
import requests
from astroquery.gaia import Gaia

def fetch_cluster_data(ra, dec, radius, limit=5000):
    """
    Fetches Gaia DR3 data in magnitude chunks with automatic retry on server errors.
    """
    mag_bins = [
        (10.0, 16.0),
        (16.0, 18.0),
        (18.0, 20.0)
    ]
    
    all_chunks = []
    
    for min_mag, max_mag in mag_bins:
        print(f"Fetching massive chunk: Magnitude between {min_mag} and {max_mag}...")
        
        adql_query = f"""
            SELECT TOP {limit} source_id, ra, dec, parallax, pmra, pmdec, bp_rp, phot_g_mean_mag
            FROM gaiadr3.gaia_source
            WHERE CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), 
                           CIRCLE('ICRS', {ra}, {dec}, {radius})) = 1
              AND phot_g_mean_mag BETWEEN {min_mag} AND {max_mag}
        """
        # Retry Mechanism When an HTTPError 500 or Any Temporary Outage Occurs
        success = False
        retries = 3
        delay = 5
        
        for attempt in range(retries):
            try:
                job = Gaia.launch_job_async(adql_query)
                r = job.get_results()
                df_chunk = r.to_pandas()
                all_chunks.append(df_chunk)
                success = True
                print(f"  -> Successfully fetched {len(df_chunk)} records.")
                break
            except requests.exceptions.HTTPError as e:
                print(f"  -> Server error (Attempt {attempt+1}/{retries}): {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  
            except Exception as e:
                print(f"  -> Unexpected error: {e}")
                break
                
        if not success:
            print("  -> Warning: Could not fetch this chunk after multiple retries. Moving on...")
        
        time.sleep(3) 
        
    if all_chunks:
        import pandas as pd
        final_df = pd.concat(all_chunks, ignore_index=True)
        output_file = "pleiades_chunks.parquet"
        final_df.to_parquet(output_file, index=False)
        print(f"=== All chunks fetched and saved to {output_file} successfully! ===")
        return final_df
    else:
        print("=== No data fetched. ===")
        return None
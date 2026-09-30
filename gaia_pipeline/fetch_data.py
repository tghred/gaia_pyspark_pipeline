from astroquery.gaia import Gaia

def fetch_cluster_data(
        ra_center = 56.75, dec_center = 24.12, radius_deg=1.0, limit=2000
        ):
    """ Fetch raw data from Gaia DR3 archive and save as Parquet file"""
    query = f"""
    SELECT TOP {limit}
        source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag, bp_rp, parallax_error
FROM gaiadr3.gaia_source
WHERE 1 = CONTAINS(
  POINT('ICRS', ra, dec),
  CIRCLE('ICRS', {ra_center}, {dec_center}, {radius_deg}) 
)
AND parallax > 0
AND (parallax_error / parallax) < 0.2
ORDER BY phot_g_mean_mag ASC 
"""

#POINT(‘ICRS’, 56.75, 24.12, 3.0)  -- Center of the Pleiades with a radius of 3 degrees

#AND parallax > 0 -- Positive angle to exclude distorted negative values

#AND parallax_error / parallax < 0.2  -- The measurement error does not exceed 20% of the parallax value itself (signal-to-noise ratio SNR > 5)

#ORDER BY phot_g_mag ASC   Retrieve the first 2,000 brightest stars first
    job = Gaia.launch_job(query)
    results= job.get_results()
    
    df_raw = results.to_pandas()
    df_raw.to_parquet("raw_gaia_data.parquet", index= False)
    print("Raw data successfully fetched and saved to raw_gaia_data.parquet")
    
    
    


if __name__ == "__main__":
       fetch_cluster_data()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pyspark.sql.functions import col



def init_spark():
    """Initialize a lightweight local Spark Session"""
    return (
        SparkSession.builder.appName("GaiaPipeline")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
        )

def clean_gaia_pyspark(input_file, output_file=None, spark=None):
    """
    Reads parquet data using PySpark, performs quality filtering, 
    and optionally saves the cleaned dataset.
    """
    if spark is None:
        spark = SparkSession.builder \
            .appName("GaiaDataCleaner") \
            .getOrCreate()
    
    df_spark = spark.read.parquet(input_file)
    
    df_cleaned = df_spark.dropna(
        subset=["parallax", "pmra", "pmdec", "bp_rp", "phot_g_mean_mag"]
    ).filter((col("parallax") > 0) & (col("phot_g_mean_mag") > 0))
    
    if output_file:
        df_cleaned.toPandas().to_parquet(output_file, index= False)
        
    return df_cleaned


def benchmark_pyspark_performance(df_spark, output_image="pyspark_performance.png"):
    """
    Measures PySpark data cleaning execution time across different dataset sizes
    and generates a performance scalability graph.
    """
    fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
    execution_times = []
    record_counts = []

    print("\n Measuring PySpark Cleaning Scalability Performance...")
    
    for frac in fractions:
        sample_df = df_spark.sample(withReplacement=False, fraction=frac, seed=42)
        total_rows = sample_df.count()
        
        start_time = time.time()
        
        _ = sample_df.dropna(
            subset=["parallax", "pmra", "pmdec", "bp_rp", "phot_g_mean_mag"]
        ).filter((col("parallax") > 0) & (col("phot_g_mean_mag") > 0)).count()
        
        elapsed_time = time.time() - start_time
        
        record_counts.append(total_rows)
        execution_times.append(elapsed_time)
        print(f"  - Scale {int(frac*100)}% ({total_rows:,} rows): {elapsed_time:.3f} seconds")

    bench_df = pd.DataFrame({
        "Record Count": record_counts,
        "Execution Time (s)": execution_times
    })


    plt.figure(figsize=(9, 5))
    sns.set_theme(style="ticks")
    
    ax = sns.lineplot(
        data=bench_df, x="Record Count", y="Execution Time (s)", 
        marker="o", linewidth=2.5, color="#1f77b4", markersize=8
    )
    
    plt.title("PySpark Data Cleaning Performance & Scalability", fontsize=13, fontweight="bold")
    plt.xlabel("Number of Processed Records (Stars)", fontsize=11)
    plt.ylabel("Execution Time (Seconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)

    for _, row in bench_df.iterrows():
        ax.annotate(
            f"{row['Execution Time (s)']:.3f}s", 
            (row["Record Count"], row["Execution Time (s)"]),
            textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold'
        )

    plt.tight_layout()
    if output_image:
        plt.savefig(output_image, dpi=300, bbox_inches='tight')
        print(f"PySpark Performance graph saved to '{output_image}'")
        
    plt.show()

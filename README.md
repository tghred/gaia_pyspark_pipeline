
#  Gaia DR3 Stellar Cluster Analytics Pipeline

An end-to-end Big Data & Machine Learning pipeline designed to query, clean, and cluster astronomical data from the **Gaia DR3** archive using **PySpark** and **DBSCAN**. The pipeline isolates open stellar clusters (such as the Pleiades / M45) using kinematic and photometric parameters.

---

## 📌 Features

- **Automated ADQL Retrieval:** Queries Gaia DR3 archive via `astroquery` for target sky coordinates and radii.
- **Scalable Data Cleaning:** Utilizes **PySpark** for distributed data filtering, quality control, and handling missing stellar entries.
- **Kinematic Clustering:** Implements **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) on proper motion parameters (`pmra`, `pmdec`).
- **Astrophysical Validation:** Automatically generates Vector Point Diagrams (VPD) and Color-Magnitude Diagrams (CMD) for physical cluster verification.
- **Performance Benchmarking:** Built-in benchmarking module to measure PySpark cleaning scalability across dataset sizes.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.10+
- **Big Data Processing:** Apache Spark / PySpark
- **Machine Learning:** Scikit-Learn (DBSCAN)
- **Data Manipulation:** Pandas, NumPy
- **Visualizations:** Matplotlib, Seaborn
- **Astrophysics:** Astroquery (Gaia Archive)

---

## 📁 Repository Structure

```text
gaia_pyspark_pipeline/
├── config/                   # Configuration files
├── examples/
│   └── run_pipeline.py       # Main execution entry point
|    | demo_pleiades.ipynb      #demonstrates the end-to-end workflow of gaia_pyspark_pipeline 

├── gaia_pipeline/
│   ├── __init__.py
│   ├── clustering.py         # DBSCAN ML model & astrophysical plots (VPD, CMD)
│   ├── fetch_data.py         # Queries Gaia DR3 database using ADQL
│   ├── raw_gaia_data.parquet # Raw cached Gaia dataset
│   └── spark_cleaner.py      # PySpark pipeline for data cleaning & benchmarking
├── tests/
│   └── test_pipeline.py      # Unit tests for pipeline components
├── .gitattributes
├── LICENSE                   # Project license
├── paper.bib                 # Bibliography for academic paper
├── paper.md                  # JOSS paper manuscript
├── README.md                 # Project documentation
└── requirements.txt          # Project dependencies

```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/gaia_pyspark_pipeline.git](https://github.com/YOUR_USERNAME/gaia_pyspark_pipeline.git)
cd gaia_pyspark_pipeline

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run the Full Pipeline

```bash
python examples/run_pipeline.py

```

### 4. Run Unit Tests

```bash
pytest tests/

```

---


## 5. Prerequisites 

To run this pipeline smoothly, you have two options:

### Option 1: Google Colab (Recommended)
No local installation required! You can run the entire pipeline directly in your browser using Google Colab:
* [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](ضع_رابط_النوت_بوك_هنا)

### Option 2: Local Environment 
If you prefer running it locally, ensure you have the following installed:
* **Python** (version 3.8 or higher)
* **Java (JDK)** (version 8 or 11 required for PySpark, with `JAVA_HOME` properly configured)
* **Apache Spark / PySpark**

### Installation via pip:
pip install -r requirements.txt


## 📊 Scientific & Performance Visualizations

### 1. Kinematic & Photometric Verification

The pipeline generates a double-plot verifying the cluster's **Dynamic Consistency** (VPD) and **Physical Consistency** (CMD):

* **Vector Point Diagram (VPD):** Isolates the Pleiades cluster movement ($pmra \approx 20$, $pmdec \approx -45$ mas/yr) from background stars.
* **Color-Magnitude Diagram (CMD):** Confirms the identified members form a clear **Main Sequence** evolutionary track.

### 2. PySpark Scalability Benchmark

Measures PySpark data cleaning execution time across different subsample ratios:

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/tghred/gaia_pyspark_pipeline/blob/main/LICENSE) file for details.
```


```

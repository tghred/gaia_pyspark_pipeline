
# Module: `test_pipeline.py`

## Overview

The `test_pipeline.py` module contains unit tests implemented using the `pytest` framework. It verifies the core functionality, import integrity, data cleaning logic (filtering unphysical parameters such as negative parallaxes), and the output shape and behavior of the machine learning clustering algorithm (`DBSCAN`).

## Test Cases

---

### 1. `test_module_imports()`

* **Purpose:** Validates that all primary modules and core functions are successfully imported without errors or broken dependencies.
* **Assertions:**
* Asserts that `fetch_cluster_data`, `clean_gaia_pyspark`, and `run_dbscan_clustering` are not `None`.



---

### 2. `test_data_cleaning_logic()`

* **Purpose:** Tests the data filtering mechanism to ensure that unphysical measurements (such as negative or zero parallaxes) are correctly removed from the dataset.
* **Workflow:**
* Generates a mock Pandas DataFrame containing synthetic astrometric records with valid and invalid (negative) parallax values.
* Applies the filtering condition (`parallax > 0`).


* **Assertions:**
* Asserts that the length of the cleaned dataset matches the expected valid row count (`2`).
* Asserts that no rows with a parallax less than or equal to zero remain in the cleaned data.



---

### 3. `test_dbscan_clustering_shape()`

* **Purpose:** Tests that the DBSCAN clustering wrapper correctly accepts coordinate arrays, performs scaling and clustering, and returns the expected labels and data shapes.
* **Workflow:**
* Creates a synthetic NumPy array with clustered points and an isolated noise point `[0.0, 0.0]`.
* Executes `run_dbscan_clustering` with custom parameters (`eps=0.5`, `min_samples=2`).


* **Assertions:**
* Asserts that the output length matches the input array length.
* Asserts that noise points are appropriately identified (containing label `-1`) or that multiple distinct clusters/labels are formed.



## Execution

To run the complete test suite locally or within the Google Colab environment, execute:

```bash
pytest test_pipeline.py

```

---

بهذا نكون قد وثقنا ملف الاختبارات `test.py` أيضاً، لتكتمل منظومة توثيق المشروع بالكامل (الاستخراج، التنظيف، التحليل العنقودي، التنفيذ، والاختبارات) بأسلوب قياسي واحترافي تماماً! هل تحتاجين إلى أي تعديل آخر قبل أن تختمي يومكِ بنجاح؟
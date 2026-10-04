لإتمام مستودعك وجعله جاهزاً بالكامل وبمعايير احترافية تناسب النشر في **JOSS**، إليك نموذجاً جاهزاً ومنظماً لملف **`CONTRIBUTING.md`**.

```markdown
# Contributing to gaia_pyspark_pipeline

First off, thank you for taking the time to contribute! 🎉 Contributions, bug reports, and feature requests are highly appreciated to make this tool better for the astronomical and data engineering community.

Please take a moment to review the guidelines below before contributing.

---

## 🚀 How Can I Contribute?

### 1. Reporting Bugs
If you encounter any bugs, unexpected errors (like HTTP 500 or path issues), or data inconsistencies:
* Check the **Issues** tab on GitHub to see if the issue has already been reported.
* If not, open a new issue and provide a clear description of the problem, including steps to reproduce it, environment details (e.g., Google Colab, local machine), and relevant error traces.

### 2. Suggesting Enhancements
Have an idea to improve PySpark performance, optimize data retrieval, or add support for new astronomical clusters?
* Open an issue to discuss your proposal with the maintainers before starting implementation.
* Clearly describe the suggested enhancement and its potential benefits.

### 3. Pull Requests (PRs)
1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name

```

2. **Install dependencies** and set up your local development environment:
```bash
pip install -r requirements.txt

```


3. **Make your changes** and ensure that the code is well-tested and clean.
4. **Run the pipeline** or tests to verify that everything works smoothly (e.g., fetching data, processing via PySpark, and exporting to `.vot` for Aladin).
5. Push your changes to your fork and submit a **Pull Request** targeting the `main` branch.

---

## 🛠️ Development Guidelines

* **Code Quality:** Follow standard Python (PEP 8) coding styles.
* **Documentation:** If you add new functions, modules, or parameters, document them clearly using docstrings and update the `README.md` if necessary.
* **Commit Messages:** Use clear, descriptive commit messages (e.g., `fix: resolve file path issue in colab` or `feat: add support for VOTable export`).

---

## 📜 Code of Conduct

By participating in this project, you agree to maintain a welcoming, respectful, and inclusive environment for everyone.

Thank you for helping improve `gaia_pyspark_pipeline`! ✨


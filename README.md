<div align="center">

# 📚 ezbib

**Universal, zero-dependency CLI tool and Python library to convert ORCID profiles and DOIs into clean BibTeX, Markdown, and formatted academic citations.**

[![PyPI Version](https://img.shields.io/pypi/v/ezbib.svg?color=blue)](https://pypi.org/project/ezbib/)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-success.svg)](https://docs.python.org/3/library/)

### 📖 [Read the Official Documentation here](https://prnvrvs.github.io/ezbib/)

---

</div>

Raw bibliographic metadata from academic APIs is frequently inconsistent, filled with XML fragments, cluttered with unreviewed preprints, and cumbersome to organize. `ezbib` was built specifically for researchers, lab managers, and scientific developers who need clean, publication-ready records without installing heavy dependencies.

## ⚡ Quick Start

Install globally using `pipx` or `pip`:
```bash
pip install ezbib
```

Generate a complete, deduplicated BibTeX file for an author:
```bash
ezbib 0000-0002-1825-0097 -o publications.bib
```

Generate a Markdown CV or styled text citations (Nature, APA, IEEE):
```bash
ezbib 10.1016/j.actamat.2025.121319 -f markdown -o cv.md
ezbib 10.1016/j.actamat.2025.121319 -f text --style nature
```

---

## 🧭 Full Documentation

For the complete API reference, advanced CLI usage, LaTeX integration, and FAQ, please visit the official documentation website:

👉 **[https://prnvrvs.github.io/ezbib/](https://prnvrvs.github.io/ezbib/)**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use it in academic, open-source, and commercial projects.

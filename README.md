<div align="center">

# 📚 ezbib

**Universal, zero-dependency CLI tool and Python library to convert ORCID profiles and DOIs into clean BibTeX, Markdown, and formatted academic citations.**

[![PyPI Version](https://img.shields.io/pypi/v/ezbib.svg?color=blue)](https://pypi.org/project/ezbib/)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-success.svg)](https://docs.python.org/3/library/)
[![Package Format](https://img.shields.io/badge/Architecture-Single--File%20%2B%20Package-orange.svg)](pyproject.toml)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

[Quick Start](#-quick-start) • [Why ezbib?](#-why-ezbib) • [Features](#-key-features) • [Installation](#-installation) • [Usage Recipes](#-usage-recipes) • [Citation Styles](#-citation-styles) • [Python API](#-python-api) • [BibLaTeX](#-grant-reporting--biblatex-integration) • [FAQ](#-frequently-asked-questions)

---

</div>

## ⚡ Quick Start

```bash
# 1. Fetch an entire ORCID profile as clean BibTeX
ezbib 0000-0002-1825-0097 -o publications.bib

# 2. Filter publications from 2021 onwards
ezbib 0000-0002-1825-0097 -y 2021 -o recent_papers.bib

# 3. Resolve a DOI directly into BibTeX
ezbib 10.1016/j.actamat.2025.121319

# 4. Generate formatted text citations (Nature, IEEE, APA, ACS, etc.)
ezbib 0000-0002-1825-0097 -f text --style nature

# 5. Export a clickable Markdown publication list for your CV or website
ezbib 0000-0002-1825-0097 -f markdown -o cv_publications.md

# 6. Read DOIs from a pipe or standard input
cat dois.txt | ezbib - -o references.bib
```

> **Note:** `ezbib`, `orcid2bib`, and `orcid2bibtex` commands are all supported and can be used interchangeably!

---

## 💡 Why `ezbib`?

Raw bibliographic metadata from academic APIs is frequently inconsistent, filled with XML fragments, cluttered with unreviewed preprints, and cumbersome to organize. `ezbib` was built specifically for researchers, lab managers, and scientific developers who need clean, publication-ready records without installing heavy dependencies.

| Feature | Raw API / Basic Tools | **`ezbib`** |
| :--- | :---: | :---: |
| **Preprint Deduplication** | ❌ Duplicate entries for arXiv & Journal | ✅ **Intelligent fuzzy deduplication** |
| **LaTeX MathML Cleaning** | ❌ Raw `<mml:math>` breaks LaTeX compiler | ✅ **Auto-converts MathML to `$\alpha$`, `$\Sigma$`, etc.** |
| **Output Formats** | ❌ `.bib` only | ✅ **BibTeX, Interactive Markdown, and CSL Plain Text** |
| **Citation Styles** | ❌ Fixed format | ✅ **8+ Academic Styles (Nature, IEEE, APA, ACS, etc.)** |
| **Grant Reporting** | ❌ Manual categorization | ✅ **Auto-tags `quality_assured` for DFG, EU, & NSF** |
| **Dependencies** | Requires third-party HTTP & parsing packages | ✅ **Zero external dependencies** (Standard Library only) |
| **CLI & Piping** | ❌ Manual file input only | ✅ **Direct DOIs, multi-DOIs, and stdin pipes (`-`)** |

---

## 🏗️ Architecture & Pipeline

```mermaid
flowchart LR
    subgraph Inputs
        A[ORCID iD / URL]
        B[DOI / DOI URL / List]
        C[Standard Input / Pipe]
    end

    subgraph Core Engine
        D[ORCID v3.0 REST API]
        E[Crossref CSL Negotiation]
        F[LaTeX / MathML Sanitizer]
        G[Preprint Deduplicator]
    end

    subgraph Output Formats
        H[Clean BibLaTeX\n+ Grant Tags]
        I[Interactive Markdown\nfor CVs / Sites]
        J[Formatted Text\nNature, IEEE, APA, ACS]
    end

    A --> D
    B --> E
    C --> B
    D --> F
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
```

---

## ✨ Key Features

- 📦 **Zero External Dependencies** — Built 100% on the Python Standard Library (`urllib`, `json`, `re`, `html`, `argparse`). No third-party packages required.
- ⚡ **First-Class Executable & Package** — Install via `pip install ezbib`, run directly as a standalone executable script (`./orcid2bib.py`), or execute via `python3 -m orcid2bib`.
- 🔄 **Smart Input Detection** — Seamlessly parses bare ORCID iDs (`0000-0002-1825-0097`), full ORCID URLs (`https://orcid.org/...`), single/multiple DOIs (`10.1016/...`), and piped standard input (`-`).
- 🧹 **LaTeX & MathML Sanitization** — Cleans XML entities and converts complex MathML tags into standard LaTeX math (e.g. `<mml:math><mml:mi>α</mml:mi></mml:math>` $\rightarrow$ `$\alpha$`, `$\Sigma$`).
- 🧠 **Intelligent Preprint Deduplication** — Identifies and suppresses preprint versions (arXiv, bioRxiv, ChemRxiv, Research Square) when peer-reviewed journal versions exist in the profile.
- 🏷️ **Grant-Ready BibLaTeX Categorization** — Injects `keywords = {quality_assured}` or `keywords = {other}` to instantly generate split CV/grant bibliographies (e.g., for DFG, EU Horizon Europe, and NSF).
- 🎨 **8+ Academic Citation Styles** — Outputs styled bibliographies in APA 7th, Nature, IEEE, ACS, Elsevier, Chicago, Harvard, and Springer formats.
- 📤 **Multiple Export Formats** — Produces structured `.bib`, clickable `.md` lists with DOI links, or styled plain text.

---

## 🚀 Installation

### Option 1: Install with `pip` / `pipx` (Recommended)

```bash
# Install from PyPI
pip install ezbib

# Or install in an isolated environment with pipx
pipx install ezbib
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/prnvrvs/ezbib.git
```

### Option 2: Clone and Install Locally

```bash
git clone https://github.com/prnvrvs/ezbib.git
cd ezbib
pip install .
```

For editable development mode:
```bash
pip install -e .
```

### Option 3: Standalone Single-File Script (Zero Installation)

Because `ezbib` is self-contained with no external dependencies, you can download `orcid2bib.py` directly and execute it anywhere:

```bash
# Download single script
curl -O https://raw.githubusercontent.com/prnvrvs/ezbib/main/orcid2bib.py
chmod +x orcid2bib.py

# Run directly:
./orcid2bib.py 0000-0002-1825-0097
```

### Option 4: Run as a Python Module

```bash
python3 -m orcid2bib 0000-0002-1825-0097
```

---

## 📖 Usage Recipes

### 1. 🆔 ORCID Profile Lookup

Fetch all publications for an ORCID profile and output clean BibTeX:

```bash
# Print to terminal
ezbib 0000-0002-1825-0097

# Save to a .bib file
ezbib 0000-0002-1825-0097 -o my_publications.bib

# Full ORCID URL is also accepted
ezbib https://orcid.org/0000-0002-1825-0097 -o my_publications.bib
```

---

### 2. 📅 Year Filtering

Filter works to match grant reporting periods, tenure reviews, or recent activity:

```bash
# Publications from 2021 to present
ezbib 0000-0002-1825-0097 -y 2021 -o recent.bib

# Publications within a specific year window (2020-2024)
ezbib 0000-0002-1825-0097 --min-year 2020 --max-year 2024 -o phd_papers.bib
```

---

### 3. 🔎 Direct DOI Resolution

Retrieve clean BibTeX for one or more DOIs:

```bash
# Single DOI
ezbib 10.1016/j.actamat.2025.121319

# Full DOI URL
ezbib https://doi.org/10.1016/j.actamat.2025.121319

# Multiple comma-separated DOIs
ezbib -d 10.1016/j.actamat.2025.121319,10.1016/j.ijhydene.2025.02.435 -o papers.bib
```

---

### 4. 🚰 Standard Input & Shell Pipelines

Pipe DOIs or ORCID iDs from other command-line tools:

```bash
# Pipe a single DOI
echo "10.1016/j.actamat.2025.121319" | ezbib -

# Batch process a text file of DOIs (one per line)
cat doi_list.txt | ezbib - -o bibliography.bib
```

---

### 5. 📝 Markdown Export (For CVs & Academic Websites)

Generate a numbered Markdown publication list with clickable DOI hyperlinks:

```bash
ezbib 0000-0002-1825-0097 -y 2021 -f markdown -o cv_publications.md
```

**Example Markdown Output:**
```markdown
# Publications from ORCID 0000-0002-1825-0097

1. **Hydrogen embrittlement mechanisms in high-strength alloys** (2025) — *Acta Materialia* ([DOI: 10.1016/j.actamat.2025.121319](https://doi.org/10.1016/j.actamat.2025.121319))
2. **Phase transformation dynamics under extreme strain** (2024) — *Nature Materials* ([DOI: 10.1038/s41563-024-00000-x](https://doi.org/10.1038/s41563-024-00000-x))
```

---

### 6. 📄 Styled Plain Text Bibliographies

Generate pre-formatted citations in your desired journal format:

```bash
# Default APA 7th style
ezbib 10.1016/j.actamat.2025.121319 -f text

# Nature style
ezbib 10.1016/j.actamat.2025.121319 -f text --style nature

# IEEE style
ezbib 10.1016/j.actamat.2025.121319 -f text --style ieee

# ACS style
ezbib 10.1016/j.actamat.2025.121319 -f text --style acs
```

---

### 7. 🔄 Controlling Preprint Deduplication

By default, `ezbib` suppresses preprints (e.g. arXiv, bioRxiv) if a corresponding journal article exists in the profile. To keep all raw entries without deduplication:

```bash
ezbib 0000-0002-1825-0097 --no-dedup -o all_raw_records.bib
```

---

### 8. 👥 Batch Processing for Research Teams

Fetch publications for an entire lab or research group using a simple Bash script:

```bash
#!/usr/bin/env bash

declare -A LAB_MEMBERS=(
  ["Prof_Smith"]="0000-0002-1825-0097"
  ["Dr_Johnson"]="0000-0001-5109-3700"
  ["Dr_Lee"]="0000-0003-1234-5678"
)

for NAME in "${!LAB_MEMBERS[@]}"; do
  ORCID="${LAB_MEMBERS[$NAME]}"
  echo "[*] Fetching publications for $NAME ($ORCID)..."
  ezbib "$ORCID" -y 2021 -o "${NAME}_publications.bib"
done
```

---

## 🎨 Citation Styles

| Style | Flag | Example Output |
| :--- | :--- | :--- |
| **APA 7th** *(default)* | `-s apa` | Smith, J., & Doe, J. (2024). Machine learning models... *Journal of Materials Science*, 59, 12048. |
| **Nature** | `-s nature` | 1. Smith, J. & Doe, J. Machine learning models... *Journal of Materials Science* **59**, 12048 (2024). |
| **IEEE** | `-s ieee` | [1] J. Smith and J. Doe, “Machine learning models...,” *Journal of Materials Science*, vol. 59, 2024. |
| **Elsevier** | `-s elsevier` | [1] J. Smith, J. Doe, Machine learning models..., *Journal of Materials Science* 59 (2024) 12048. |
| **ACS** | `-s acs` | (1) Smith, J.; Doe, J. Machine Learning Models... *Journal of Materials Science* **2024**, *59*, 12048. |
| **Chicago** | `-s chicago` | Smith, Jane, and John Doe. 2024. “Machine Learning Models...” *Journal of Materials Science* 59. |
| **Harvard** | `-s harvard` | Smith, J., Doe, J., 2024. Machine learning models... *Journal of Materials Science* 59, 12048. |
| **Springer** | `-s springer` | Smith J, Doe J (2024) Machine learning models... *Journal of Materials Science* 59:12048. |
| **MLA** | `-s mla` | Smith, Jane, and John Doe. "Machine Learning Models..." *Journal of Materials Science*, vol. 59, 2024. |

---

## 🧭 CLI Command-Line Reference

```text
usage: ezbib [-h] [-d DOI] [-y YEAR] [--max-year YEAR] [-o FILE]
             [-f {bibtex,markdown,text,apa}] [-s STYLE] [--no-dedup] [-v]
             [target]
```

| Argument / Flag | Short | Type | Default | Description |
| :--- | :---: | :---: | :---: | :--- |
| `target` | — | `str` | `None` | Positional target: ORCID iD, DOI, full URL, or `-` for stdin |
| `--doi` | `-d` | `str` | `None` | Explicit DOI or comma-separated list of DOIs |
| `--min-year` | `-y` | `int` | `None` | Include publications published in or after this year |
| `--max-year` | — | `int` | `None` | Include publications published up to this year |
| `--output` | `-o` | `str` | `stdout` | Write output to a specified file |
| `--format` | `-f` | `choice` | `bibtex` | Output format: `bibtex`, `markdown`, `text`, `apa` |
| `--style` | `-s` | `str` | `apa` | Citation style for `text` format (e.g. `nature`, `ieee`, `acs`) |
| `--no-dedup` | — | `flag` | `False` | Disable smart preprint deduplication |
| `--version` | `-v` | `flag` | — | Show program version and exit |
| `--help` | `-h` | `flag` | — | Show help message and usage examples |

---

## 🐍 Python API

`ezbib` can also be imported and used programmatically in any Python 3.7+ application:

```python
import orcid2bib as ezbib

# 1. Query an ORCID profile
works = ezbib.fetch_orcid(
    "0000-0002-1825-0097",
    min_year=2021,
    dedup=True
)

for work in works:
    print(f"[{work['year']}] {work['title']} (DOI: {work['doi']})")

# 2. Convert DOI to clean, formatted BibTeX
bibtex_entry = ezbib.doi_to_bibtex(
    "10.1016/j.actamat.2025.121319",
    extra_keywords="quality_assured"
)
print(bibtex_entry)

# 3. Format DOI citation into a specific journal style
nature_citation = ezbib.doi_to_text(
    "10.1016/j.actamat.2025.121319",
    style="nature"
)
print(nature_citation)
```

---

## 📑 Grant Reporting & BibLaTeX Integration

`ezbib` automatically categorizes works by injecting `keywords = {quality_assured}` for peer-reviewed journal articles and `keywords = {other}` for preprints, conference proceedings, or unreviewed outputs.

This makes generating split academic CVs (such as for **DFG**, **EU Horizon Europe**, or **NSF** proposals) straightforward in LaTeX:

```latex
\documentclass[11pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx}
\usepackage[margin=2.2cm]{geometry}

\usepackage[
  backend=biber,
  style=numeric,
  sorting=ydnt,
  maxbibnames=99,
  defernumbers=true
]{biblatex}

\addbibresource{publications.bib}

\begin{document}

\section*{Principal Investigator — List of Publications}
\nocite{*}

\subsection*{Category A: Peer-Reviewed & Quality-Assured Journal Publications}
\printbibliography[
  keyword=quality_assured,
  heading=none,
  resetnumbers=true
]

\subsection*{Category B: Preprints, Conference Proceedings & Other Works}
\printbibliography[
  keyword=other,
  heading=none,
  resetnumbers=true
]

\end{document}
```

**To compile:**
```bash
pdflatex publication_list.tex
biber publication_list
pdflatex publication_list.tex
```

---

## ❓ Frequently Asked Questions

<details>
<summary><b>Does ezbib require an ORCID API key or account?</b></summary>
<br>
No. Public ORCID profiles are queried directly through the public ORCID REST API v3.0, and DOI metadata is resolved via Crossref content negotiation without requiring an API key.
</details>

<details>
<summary><b>What happens if an ORCID publication has no DOI?</b></summary>
<br>
If a work in the ORCID record does not have an attached DOI, <code>ezbib</code> outputs a clear commented placeholder in the BibTeX file:
<pre><code>% Work without DOI: Title of Publication (Year)</code></pre>
This ensures no entries are silently dropped while keeping your <code>.bib</code> file syntactically valid.
</details>

<details>
<summary><b>How does preprint deduplication work?</b></summary>
<br>
Preprints (identified by journal titles containing <code>arxiv</code>, <code>biorxiv</code>, <code>chemrxiv</code>, <code>research square</code> or type <code>PREPRINT</code>) are fuzzy-matched against peer-reviewed articles in the same ORCID profile. If a published journal version exists, the preprint is automatically suppressed unless <code>--no-dedup</code> is specified.
</details>

<details>
<summary><b>Can I format citations in styles not listed above?</b></summary>
<br>
Yes. Any valid CSL (Citation Style Language) style identifier supported by the Crossref citation service can be passed directly to <code>--style</code> (e.g. <code>--style cell</code>, <code>--style pnas</code>).
</details>

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use it in academic, open-source, and commercial projects.

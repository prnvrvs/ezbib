# 📚 orcid2bib

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-brightgreen.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Single--File%20Standalone-orange.svg)]()
[![ORCID](https://img.shields.io/badge/ORCID-v3.0%20API-A6CE39.svg)](https://orcid.org/)

**`orcid2bib`** is a **100% standalone, single-file** command-line tool and Python module to extract, clean, and format academic publications from any **ORCID iD** or **DOI**.

It generates beautifully formatted, indented `.bib` databases, Markdown CVs, and plain text summaries with **zero external dependencies** (`pip` not required).

---

## 📑 Table of Contents

1. [Key Features](#-key-features)
2. [Installation & Single-File Setup](#-installation--single-file-setup)
3. [Comprehensive CLI Usage Guide](#-comprehensive-cli-usage-guide)
   - [ORCID Profile Queries](#1-orcid-profile-queries)
   - [Direct DOI Lookups (Built-in doi2bib)](#2-direct-doi-lookups-built-in-doi2bib)
   - [Year Filtering](#3-filtering-by-publication-year)
   - [Output Formats (BibTeX, Markdown, Text)](#4-output-formats)
   - [Smart Preprint Deduplication](#5-smart-preprint-deduplication)
   - [Batch Processing Multiple Researchers](#6-batch-processing-multiple-researchers)
4. [Python API Integration (Library Usage)](#-python-api-integration)
5. [Integrating with LaTeX & BibLaTeX Grant Proposals](#-integrating-with-latex--biblatex-grant-proposals)
6. [Command-Line Options Reference](#-command-line-options-reference)
7. [Troubleshooting & FAQ](#-troubleshooting--faq)
8. [License](#-license)

---

## ✨ Key Features

- 📦 **100% Standalone & Single-File:** Contained completely in `orcid2bib.py`. No setup scripts, package installs, or extra files needed.
- ⚡ **Zero External Dependencies:** Built purely with the Python Standard Library (`urllib`, `json`, `re`, `argparse`). Works out of the box on any system with Python 3.7+.
- 🔄 **Universal Auto-Detection (ORCID & DOI):** Pass an ORCID iD or a DOI directly—the tool automatically detects the input type.
- 🌐 **ORCID Public REST API (v3.0):** Directly queries official ORCID registry records in real time.
- 🎯 **Publisher-Verified Metadata:** Uses HTTP Content Negotiation with Crossref and the DOI Foundation for 100% accurate citations.
- 🧹 **LaTeX & MathML Tag Sanitizer:** Automatically cleans XML tags and MathML entities from publisher databases (e.g. converting `<mml:math><mml:mi>α</mml:mi></mml:math>-Fe` into clean LaTeX `$\alpha$-Fe`).
- 🔄 **Intelligent Preprint Deduplication:** Detects when an author has both an arXiv / preprint record and the final published peer-reviewed journal article, automatically filtering out duplicate preprints.
- 🏷️ **BibLaTeX Grant Categorization:** Automatically injects `keywords = {quality_assured}` or `keywords = {other}` to enable instant multi-section bibliographies for funding agencies (ERC, DFG, NSF, Horizon Europe).
- 📐 **Beautiful Multi-line Formatting:** Indents every bibliographic key with 2 spaces and standard field ordering.

---

## 🚀 Installation & Setup

### Option 1: Direct Download (Zero Setup)
Clone the repository or simply copy `orcid2bib.py` to your working directory:
```bash
git clone https://github.com/yourusername/orcid2bib.git
cd orcid2bib
chmod +x scripts/orcid2bib.py
```

### Option 2: Add Global Shell Alias (Recommended)
To run `orcid2bib` from any terminal directory, add an alias to your shell configuration (`~/.zshrc` or `~/.bashrc`):

```bash
# In ~/.zshrc or ~/.bashrc:
alias orcid2bib="python3 /path/to/orcid2bib.py"
```
Reload your configuration:
```bash
source ~/.zshrc
```
Now you can simply run:
```bash
orcid2bib 0000-0002-1825-0097 -y 2021 -o publications.bib
```

---

## 💻 Comprehensive CLI Usage Guide

### 1. ORCID Profile Queries

#### Print Entire Publication Record to Terminal:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097
```

#### Save Profile Publications to a `.bib` File:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -o my_publications.bib
```

---

### 2. Direct DOI Lookups (Built-in `doi2bib`)

`orcid2bib` natively resolves DOIs without needing separate tools:

#### Fetch a Single DOI Directly:
```bash
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319
```

#### Pass Full DOI URL:
```bash
python3 scripts/orcid2bib.py https://doi.org/10.1016/j.actamat.2025.121319
```

#### Fetch Multiple DOIs at Once (Comma-Separated):
```bash
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319,10.1016/j.ijhydene.2025.02.435 -o references.bib
```

#### Explicit `-d` / `--doi` Flag:
```bash
python3 scripts/orcid2bib.py -d 10.1016/j.actamat.2025.121319 -o paper.bib
```

---

### 3. Filtering by Publication Year

#### Filter from a Specific Year Onwards (`--min-year` / `-y`):
Ideal for 5-year or 10-year track record requirements in grant proposals:
```bash
# Fetch all works published in 2021 or later
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -o recent_papers.bib
```

#### Filter a Specific Historical Range (`--min-year` and `--max-year`):
```bash
# Fetch works published between 2020 and 2024
python3 scripts/orcid2bib.py 0000-0002-1825-0097 --min-year 2020 --max-year 2024 -o phd_papers.bib
```

---

### 4. Output Formats

#### Format A: BibTeX (`-f bibtex` — Default)
Outputs standard BibTeX entries with custom tags:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2024 -f bibtex
```
*Output Example:*
```bibtex
@article{Smith_2024,
  author = {Smith, Jane and Doe, John},
  title = {Machine learning models for material properties},
  journal = {Journal of Materials Science},
  volume = {59},
  pages = {12048},
  year = {2024},
  doi = {10.1007/s10853-024-00000-0},
  keywords = {quality_assured}
}
```

#### Format B: Markdown (`-f markdown`)
Generates a numbered Markdown list with clickable DOI hyperlinks—perfect for personal websites, GitHub profile READMEs, or CVs:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -f markdown -o cv_publications.md
```

#### Format C: Plain Text (`-f text`)
Generates a clean text summary suitable for email or forms:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2024 -f text
```

---

### 4. Smart Preprint Deduplication

By default, `orcid2bib` compares preprint titles (e.g. from arXiv, ChemRxiv, bioRxiv, Research Square) against published journal titles in the same profile. If the final peer-reviewed article is already present, the duplicate preprint is automatically suppressed.

To disable this behavior and include all raw preprints:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 --no-dedup -o all_raw_records.bib
```

---

### 5. Batch Processing Multiple Researchers

You can easily automate publication list generation for multiple team members or grant co-applicants using a simple bash loop:

```bash
# List of ORCID IDs: Name ORCID
declare -A TEAM=(
  ["PI"]="0000-0002-1825-0097"
  ["CoPI"]="0000-0001-5109-3700"
)

for NAME in "${!TEAM[@]}"; do
  ORCID="${TEAM[$NAME]}"
  echo "Processing $NAME ($ORCID)..."
  python3 scripts/orcid2bib.py "$ORCID" -y 2021 -o "${NAME}_publications.bib"
done
```

---

## 🐍 Python API Integration

You can also import and use `orcid2bib` directly inside your own Python scripts and pipelines:

```python
from scripts.orcid2bib import fetch_orcid, doi_to_bibtex

# 1. Fetch structured publication records from an ORCID ID
works = fetch_orcid("0000-0002-1825-0097", min_year=2021, dedup=True)

print(f"Retrieved {len(works)} publications:")
for w in works:
    print(f"- [{w['year']}] {w['title']} ({w['journal']}) -> DOI: {w['doi']}")

# 2. Fetch formatted BibTeX for any DOI
doi = "10.1016/j.actamat.2025.121319"
bib_entry = doi_to_bibtex(doi, extra_keywords="quality_assured")
print("\nGenerated BibTeX:\n", bib_entry)
```

---

## 📑 Integrating with LaTeX & BibLaTeX Grant Proposals

`orcid2bib` is optimized for research grant proposals and CV track-record documents (such as ERC, DFG, NSF, Horizon Europe).

### Complete Minimal Working Example (`publication_list.tex`):

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx}
\usepackage[margin=2.2cm]{geometry}
\usepackage[dvipsnames]{xcolor}
\usepackage[colorlinks=true,linkcolor=MidnightBlue,urlcolor=MidnightBlue]{hyperref}

% Use BibLaTeX with biber backend
\usepackage[
    backend=biber,
    style=numeric,
    sorting=ydnt,
    maxbibnames=99,
    defernumbers=true
]{biblatex}

% Include the file generated by orcid2bib
\addbibresource{my_publications.bib}

\begin{document}

\section*{Publications of the Principal Investigator (Last 5 Years)}
\nocite{*}

\subsection*{1. Quality-Assured Publications (Peer-Reviewed Journals)}
\printbibliography[keyword=quality_assured,heading=none,resetnumbers=true]

\subsection*{2. Other Scientific Outputs (Software, Datasets, Preprints)}
\printbibliography[keyword=other,heading=none,resetnumbers=true]

\end{document}
```

#### Compile with:
```bash
pdflatex publication_list.tex
biber publication_list
pdflatex publication_list.tex
```

---

## 📖 Command-Line Options Reference

```
usage: python3 scripts/orcid2bib.py [-h] [-d DOI] [-y YEAR] [--max-year YEAR]
                                    [-o FILE] [-f {bibtex,markdown,text}]
                                    [--no-dedup]
                                    [target]

positional arguments:
  target                ORCID identifier (e.g. 0000-0002-1825-0097) OR direct DOI (e.g. 10.1016/j.actamat.2025.121319)

options:
  -h, --help            Show this help message and exit
  -d DOI, --doi DOI     Single DOI or comma-separated list of DOIs to fetch directly
  -y YEAR, --min-year YEAR
                        Filter publications published in or after this year (e.g. -y 2021)
  --max-year YEAR       Filter publications published up to this year (e.g. --max-year 2025)
  -o FILE, --output FILE
                        Save output directly to a file (e.g. -o publications.bib or -o cv.md)
  -f {bibtex,markdown,text}, --format {bibtex,markdown,text}
                        Output format: bibtex (default), markdown, or text
  --no-dedup            Disable smart preprint deduplication (keep preprints even if published)
```

---

## ❓ Troubleshooting & FAQ

### 1. What if a paper has no DOI in the ORCID record?
If an entry on ORCID lacks a registered DOI, `orcid2bib` outputs a commented placeholder line in the `.bib` file (`% Work without DOI: Title (Year)`), allowing you to review or manually supply a citation key without crashing the parser.

### 2. Can I use a full ORCID URL instead of the 16-digit ID?
Yes! Both formats are automatically recognized and parsed:
- `0000-0002-1825-0097`
- `https://orcid.org/0000-0002-1825-0097`

### 3. Can I pass a DOI directly?
Yes! You can pass DOIs directly with or without flags:
- `python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319`
- `python3 scripts/orcid2bib.py https://doi.org/10.1016/j.actamat.2025.121319`
- `python3 scripts/orcid2bib.py -d 10.1016/j.actamat.2025.121319`

### 4. Does it require an ORCID API key?
No. It connects to the open public ORCID REST API v3.0 (`pub.orcid.org`), which requires zero authentication or API tokens for public profiles.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free for academic, personal, and commercial use.
- 🏷️ **BibLaTeX Grant Categorization:** Automatically injects `keywords = {quality_assured}` or `keywords = {other}` to enable instant multi-section bibliographies for funding agencies (ERC, DFG, NSF, Horizon Europe).
- 📐 **Beautiful Multi-line Formatting:** Indents every bibliographic key with 2 spaces and standard field ordering.

---

## 🚀 Installation & Setup

### Option 1: Direct Download (Zero Setup)
Clone the repository or simply copy `orcid2bib.py` to your working directory:
```bash
git clone https://github.com/yourusername/orcid2bib.git
cd orcid2bib
chmod +x scripts/orcid2bib.py
```

### Option 2: Add Global Shell Alias (Recommended)
To run `orcid2bib` from any terminal directory, add an alias to your shell configuration (`~/.zshrc` or `~/.bashrc`):

```bash
# In ~/.zshrc or ~/.bashrc:
alias orcid2bib="python3 /path/to/orcid2bib.py"
```
Reload your configuration:
```bash
source ~/.zshrc
```
Now you can simply run:
```bash
orcid2bib 0000-0002-1825-0097 -y 2021 -o publications.bib
```

---

## 💻 Comprehensive CLI Usage Guide

### 1. Basic Queries

#### Print Clean BibTeX Directly to the Terminal:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097
```

#### Save to a `.bib` File:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -o my_publications.bib
```

---

### 2. Filtering by Publication Year

#### Filter from a Specific Year Onwards (`--min-year` / `-y`):
Ideal for 5-year or 10-year track record requirements in grant proposals:
```bash
# Fetch all works published in 2021 or later
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -o recent_papers.bib
```

#### Filter a Specific Historical Range (`--min-year` and `--max-year`):
```bash
# Fetch works published between 2020 and 2024
python3 scripts/orcid2bib.py 0000-0002-1825-0097 --min-year 2020 --max-year 2024 -o phd_papers.bib
```

---

### 3. Output Formats

#### Format A: BibTeX (`-f bibtex` — Default)
Outputs standard BibTeX entries with custom tags:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2024 -f bibtex
```
*Output Example:*
```bibtex
@article{Smith_2024,
  author = {Smith, Jane and Doe, John},
  title = {Machine learning models for material properties},
  journal = {Journal of Materials Science},
  volume = {59},
  pages = {12048},
  year = {2024},
  doi = {10.1007/s10853-024-00000-0},
  keywords = {quality_assured}
}
```

#### Format B: Markdown (`-f markdown`)
Generates a numbered Markdown list with clickable DOI hyperlinks—perfect for personal websites, GitHub profile READMEs, or CVs:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -f markdown -o cv_publications.md
```

#### Format C: Plain Text (`-f text`)
Generates a clean text summary suitable for email or forms:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2024 -f text
```

---

### 4. Smart Preprint Deduplication

By default, `orcid2bib` compares preprint titles (e.g. from arXiv, ChemRxiv, bioRxiv, Research Square) against published journal titles in the same profile. If the final peer-reviewed article is already present, the duplicate preprint is automatically suppressed.

To disable this behavior and include all raw preprints:
```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 --no-dedup -o all_raw_records.bib
```

---

### 5. Batch Processing Multiple Researchers

You can easily automate publication list generation for multiple team members or grant co-applicants using a simple bash loop:

```bash
# List of ORCID IDs: Name ORCID
declare -A TEAM=(
  ["PI"]="0000-0002-1825-0097"
  ["CoPI"]="0000-0001-5109-3700"
)

for NAME in "${!TEAM[@]}"; do
  ORCID="${TEAM[$NAME]}"
  echo "Processing $NAME ($ORCID)..."
  python3 scripts/orcid2bib.py "$ORCID" -y 2021 -o "${NAME}_publications.bib"
done
```

---

## 🐍 Python API Integration

You can also import and use `orcid2bib` directly inside your own Python scripts and pipelines:

```python
from scripts.orcid2bib import fetch_orcid, doi_to_bibtex

# 1. Fetch structured publication records from an ORCID ID
works = fetch_orcid("0000-0002-1825-0097", min_year=2021, dedup=True)

print(f"Retrieved {len(works)} publications:")
for w in works:
    print(f"- [{w['year']}] {w['title']} ({w['journal']}) -> DOI: {w['doi']}")

# 2. Fetch formatted BibTeX for any DOI
doi = "10.1016/j.actamat.2025.121319"
bib_entry = doi_to_bibtex(doi, extra_keywords="quality_assured")
print("\nGenerated BibTeX:\n", bib_entry)
```

---

## 📑 Integrating with LaTeX & BibLaTeX Grant Proposals

`orcid2bib` is optimized for CV track-record documents.

### Complete Minimal Working Example (`publication_list.tex`):

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx}
\usepackage[margin=2.2cm]{geometry}
\usepackage[dvipsnames]{xcolor}
\usepackage[colorlinks=true,linkcolor=MidnightBlue,urlcolor=MidnightBlue]{hyperref}

% Use BibLaTeX with biber backend
\usepackage[
    backend=biber,
    style=numeric,
    sorting=ydnt,
    maxbibnames=99,
    defernumbers=true
]{biblatex}

% Include the file generated by orcid2bib
\addbibresource{my_publications.bib}

\begin{document}

\section*{Publications of the Principal Investigator (Last 5 Years)}
\nocite{*}

\subsection*{1. Quality-Assured Publications (Peer-Reviewed Journals)}
\printbibliography[keyword=quality_assured,heading=none,resetnumbers=true]

\subsection*{2. Other Scientific Outputs (Software, Datasets, Preprints)}
\printbibliography[keyword=other,heading=none,resetnumbers=true]

\end{document}
```

#### Compile with:
```bash
pdflatex publication_list.tex
biber publication_list
pdflatex publication_list.tex
```

---

## 📖 Command-Line Options Reference

```
usage: python3 scripts/orcid2bib.py [-h] [-y YEAR] [--max-year YEAR] [-o FILE]
                                    [-f {bibtex,markdown,text}] [--no-dedup]
                                    [orcid]

positional arguments:
  orcid                 Researcher 16-digit ORCID identifier (e.g. 0000-0002-1825-0097)

options:
  -h, --help            Show this help message and exit
  -y YEAR, --min-year YEAR
                        Filter publications published in or after this year (e.g. -y 2021)
  --max-year YEAR       Filter publications published up to this year (e.g. --max-year 2025)
  -o FILE, --output FILE
                        Save output directly to a file (e.g. -o publications.bib or -o cv.md)
  -f {bibtex,markdown,text}, --format {bibtex,markdown,text}
                        Output format: bibtex (default), markdown, or text
  --no-dedup            Disable smart preprint deduplication (keep preprints even if published)
```

---

## ❓ Troubleshooting & FAQ

### 1. What if a paper has no DOI in the ORCID record?
If an entry on ORCID lacks a registered DOI, `orcid2bib` outputs a commented placeholder line in the `.bib` file (`% Work without DOI: Title (Year)`), allowing you to review or manually supply a citation key without crashing the parser.

### 2. Can I use a full ORCID URL instead of the 16-digit ID?
Yes! Both formats are automatically recognized and parsed:
- `0000-0002-1825-0097`
- `https://orcid.org/0000-0002-1825-0097`

### 3. Does it require an ORCID API key?
No. It connects to the open public ORCID REST API v3.0 (`pub.orcid.org`), which requires zero authentication or API tokens for public profiles.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free for academic, personal, and commercial use.

# 📚 orcid2bib

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-brightgreen.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Single--File%20Standalone-orange.svg)]()

> **Universal, zero-dependency CLI tool to extract, clean, and format publications from any ORCID iD or DOI into BibTeX, Markdown, or styled bibliographies.**

---

## ⚡ 30-Second Quick Start

```bash
# 1. Fetch entire ORCID profile as clean BibTeX
python3 orcid2bib.py 0000-0002-1825-0097 -o publications.bib

# 2. Filter from 2021 onwards (e.g. for grant 5-year track records)
python3 orcid2bib.py 0000-0002-1825-0097 -y 2021 -o recent.bib

# 3. Direct DOI lookup (built-in doi2bib)
python3 orcid2bib.py 10.1016/j.actamat.2025.121319

# 4. Generate formatted text bibliography (APA, Nature, IEEE, etc.)
python3 orcid2bib.py 0000-0002-1825-0097 -f text --style nature

# 5. Export as a clickable Markdown list (for CVs or personal website)
python3 orcid2bib.py 0000-0002-1825-0097 -f markdown -o cv.md
```

---

## ✨ Features

* 📦 **100% Standalone:** Single self-contained Python file. No `pip install` required.
* 🔄 **Auto-Detects Inputs:** Seamlessly accepts **16-digit ORCID iDs**, **DOIs**, or **full URLs**.
* 🎯 **Publisher Verified:** Queries ORCID v3.0 REST API and Crossref HTTP content negotiation.
* 🧹 **LaTeX/MathML Sanitizer:** Automatically cleans XML/MathML into clean LaTeX math (`$\alpha$-Fe`, `$\Sigma$`).
* 🔄 **Smart Deduplication:** Automatically suppresses duplicate preprints when the peer-reviewed journal version exists.
* 🏷️ **Grant-Ready Tags:** Automatically adds `keywords = {quality_assured}` or `keywords = {other}` for multi-section CV bibliographies.

---

## 🚀 Installation & Shell Alias

Download the standalone script directly:
```bash
curl -O https://raw.githubusercontent.com/yourusername/orcid2bib/main/scripts/orcid2bib.py
chmod +x orcid2bib.py
```

*(Optional)* Make it a global command from any terminal directory:
```bash
# Add to ~/.zshrc or ~/.bashrc:
alias orcid2bib="python3 /path/to/orcid2bib.py"
```

---

## 📖 CLI Flags & Options

| Option | Flag | Description | Example |
| :--- | :---: | :--- | :--- |
| **`target`** | — | ORCID ID, DOI, or full URL *(Auto-detected)* | `0000-0002-1825-0097` or `10.1016/...` |
| **`--doi`** | `-d` | Explicit single DOI or comma-separated list | `-d 10.1016/j.actamat...` |
| **`--min-year`** | `-y` | Filter publications published in or after this year | `-y 2021` |
| **`--max-year`** | — | Filter publications published up to this year | `--max-year 2025` |
| **`--output`** | `-o` | Save output directly to a file | `-o my_pubs.bib` |
| **`--format`** | `-f` | Output format: `bibtex` *(default)*, `markdown`, `text` | `-f text` |
| **`--style`** | `-s` | Citation style for text format *(see table below)* | `-s nature` |
| **`--no-dedup`** | — | Keep preprints even if published in a journal | `--no-dedup` |

---

## 🎨 Supported Formats & Citation Styles

### 1. BibTeX (`-f bibtex` — Default)
Clean, multi-line indented format with standard field order:
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

### 2. Formatted Academic Styles (`-f text --style <NAME>`)

| Style (`-s`) | Publisher / Standard | Sample Output |
| :--- | :--- | :--- |
| **`apa`** *(default)* | APA 7th Edition | `Smith, J., & Doe, J. (2024). Machine learning models... Journal of Materials Science, 59, 12048.` |
| **`nature`** | Nature Group | `1. Smith, J. & Doe, J. Machine learning models... Journal of Materials Science 59, 12048 (2024).` |
| **`ieee`** | IEEE | `[1] J. Smith and J. Doe, “Machine learning models...,” Journal of Materials Science, vol. 59, 2024.` |
| **`elsevier`** | Elsevier / *Acta* | `[1] J. Smith, J. Doe, Machine learning models..., Journal of Materials Science 59 (2024) 12048.` |
| **`acs`** | ACS Journals | `(1) Smith, J.; Doe, J. Machine Learning Models... Journal of Materials Science 2024, 59, 12048.` |
| **`chicago`** | Chicago (Author-Date)| `Smith, Jane, and John Doe. 2024. “Machine Learning Models...” Journal of Materials Science 59.` |
| **`harvard`** | Harvard Format | `Smith, J., Doe, J., 2024. Machine learning models... Journal of Materials Science 59, 12048.` |
| **`springer`** | Springer Nature | `Smith J, Doe J (2024) Machine learning models... Journal of Materials Science 59:12048.` |

---

## 🐍 Python API Usage

```python
from orcid2bib import fetch_orcid, doi_to_bibtex, doi_to_text

# Fetch all works from an ORCID profile
works = fetch_orcid("0000-0002-1825-0097", min_year=2021)

# Fetch clean BibTeX for a DOI
bib = doi_to_bibtex("10.1016/j.actamat.2025.121319")

# Fetch formatted Nature citation
citation = doi_to_text("10.1016/j.actamat.2025.121319", style="nature")
```

---

## 📑 LaTeX / BibLaTeX Grant Integration

Use the generated `.bib` file to compile categorized publication sections:

```latex
\usepackage[backend=biber,style=numeric,sorting=ydnt,defernumbers=true]{biblatex}
\addbibresource{publications.bib}

\begin{document}
\nocite{*}
\subsection*{Quality-Assured Journal Publications}
\printbibliography[keyword=quality_assured,heading=none,resetnumbers=true]

\subsection*{Preprints and Other Works}
\printbibliography[keyword=other,heading=none,resetnumbers=true]
\end{document}
```

---

## 📄 License

MIT License — Free for academic, personal, and commercial use.
- 🎯 **Publisher-Verified Metadata:** Uses HTTP Content Negotiation with Crossref and the DOI Foundation for 100% accurate citations.
- 🧹 **LaTeX & MathML Tag Sanitizer:** Automatically cleans XML tags and MathML entities from publisher databases (e.g. converting `<mml:math><mml:mi>α</mml:mi></mml:math>-Fe` into clean LaTeX `$\alpha$-Fe`).
- 🔄 **Intelligent Preprint Deduplication:** Detects when an author has both an arXiv / preprint record and the final published peer-reviewed journal article, automatically filtering out duplicate preprints.
- 🏷️ **BibLaTeX Grant Categorization:** Automatically injects `keywords = {quality_assured}` or `keywords = {other}` to enable instant multi-section bibliographies for funding agencies.
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

#### Format C: Simple Formatted Academic Bibliography (`-f text`)
Generates clean, human-readable citations directly formatted in standard academic styles (APA by default, or `--style nature`, `--style ieee`, `--style vancouver`):

```bash
# 1. Simple APA bibliography for an ORCID profile
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -f text

# 2. Simple citation for a single DOI in Nature style
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319 -f text --style nature

# 3. Simple citation in IEEE style
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319 -f text --style ieee
```

*Output Example (APA):*
```text
1. Smith, J., & Doe, J. (2024). Machine learning models for material properties. Journal of Materials Science, 59, 12048. https://doi.org/10.1007/s10853-024-00000-0
```

---

### 5. Smart Preprint Deduplication

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

`orcid2bib` is optimized for research grant proposals and CV track-record documents.

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
- 🎯 **Publisher-Verified Metadata:** Uses HTTP Content Negotiation with Crossref and the DOI Foundation for 100% accurate citations.
- 🧹 **LaTeX & MathML Tag Sanitizer:** Automatically cleans XML tags and MathML entities from publisher databases (e.g. converting `<mml:math><mml:mi>α</mml:mi></mml:math>-Fe` into clean LaTeX `$\alpha$-Fe`).
- 🔄 **Intelligent Preprint Deduplication:** Detects when an author has both an arXiv / preprint record and the final published peer-reviewed journal article, automatically filtering out duplicate preprints.
- 🏷️ **BibLaTeX Grant Categorization:** Automatically injects `keywords = {quality_assured}` or `keywords = {other}` to enable instant multi-section bibliographies for funding agencies .
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

`orcid2bib` is optimized for research grant proposals and CV track-record documents.

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
- 🏷️ **BibLaTeX Grant Categorization:** Automatically injects `keywords = {quality_assured}` or `keywords = {other}` to enable instant multi-section bibliographies for funding agencies.
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

# 📚 orcid2bib

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-brightgreen.svg)
![Architecture](https://img.shields.io/badge/Architecture-Single--File%20Standalone-orange.svg)

> A zero-dependency command-line tool for fetching, cleaning, deduplicating, and formatting publication metadata from ORCID iDs and DOIs as BibTeX, Markdown, or styled bibliographies.

## ⚡ Quick start

```bash
# Fetch an entire ORCID profile as BibTeX
python3 orcid2bib.py 0000-0002-1825-0097 -o publications.bib

# Keep publications from 2021 onward
python3 orcid2bib.py 0000-0002-1825-0097 -y 2021 -o recent.bib

# Resolve a DOI directly
python3 orcid2bib.py 10.1016/j.actamat.2025.121319

# Generate a formatted bibliography
python3 orcid2bib.py 0000-0002-1825-0097 -f text --style nature

# Export a clickable Markdown publication list
python3 orcid2bib.py 0000-0002-1825-0097 -f markdown -o cv.md
```

## ✨ Features

- 📦 **Zero dependencies** — runs with the Python standard library; no `pip install` required.
- 🔄 **Flexible input detection** — accepts ORCID iDs, DOIs, and full ORCID/DOI URLs.
- 🎯 **Publisher metadata lookup** — queries the ORCID v3.0 REST API and uses Crossref HTTP content negotiation for DOI metadata.
- 🧹 **LaTeX/MathML cleanup** — converts XML/MathML fragments into cleaner LaTeX-compatible text, including expressions such as `$\alpha$-Fe` and `$\Sigma$`.
- 🧠 **Smart preprint deduplication** — suppresses duplicate preprints when a matching journal publication is present.
- 🏷️ **Grant-ready BibLaTeX tags** — adds `keywords = {quality_assured}` or `keywords = {other}` for categorized bibliographies.
- 📤 **Multiple output formats** — produces BibTeX, Markdown, or human-readable citation text.
- 🎨 **Multiple citation styles** — supports APA, Nature, IEEE, Elsevier, ACS, Chicago, Harvard, and Springer-style output.

## 🚀 Installation

### 📥 Clone the repository

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/orcid2bib.git
cd orcid2bib
chmod +x scripts/orcid2bib.py
```

You can then run:

```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097
```

### 🖥️ Optional: create a shell alias

Add the following to `~/.zshrc` or `~/.bashrc`:

```bash
alias orcid2bib="python3 /path/to/orcid2bib/scripts/orcid2bib.py"
```

Reload your shell configuration:

```bash
source ~/.zshrc
```

Then run the tool from any directory:

```bash
orcid2bib 0000-0002-1825-0097 -y 2021 -o publications.bib
```

## 💻 Usage

### 🆔 ORCID profile lookup

Print publications to the terminal:

```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097
```

Save them to a BibTeX file:

```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -o my_publications.bib
```

A full ORCID URL is also accepted:

```bash
python3 scripts/orcid2bib.py https://orcid.org/0000-0002-1825-0097
```

### 🔎 DOI lookup

Resolve a single DOI:

```bash
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319
```

A full DOI URL also works:

```bash
python3 scripts/orcid2bib.py https://doi.org/10.1016/j.actamat.2025.121319
```

Use the explicit DOI flag:

```bash
python3 scripts/orcid2bib.py -d 10.1016/j.actamat.2025.121319 -o paper.bib
```

Resolve multiple comma-separated DOIs:

```bash
python3 scripts/orcid2bib.py \
  -d 10.1016/j.actamat.2025.121319,10.1016/j.ijhydene.2025.02.435 \
  -o references.bib
```

### 📅 Filter by publication year

Keep publications from a minimum year onward:

```bash
python3 scripts/orcid2bib.py \
  0000-0002-1825-0097 \
  --min-year 2021 \
  -o recent_papers.bib
```

The short form is equivalent:

```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2021 -o recent_papers.bib
```

Filter to a closed year range:

```bash
python3 scripts/orcid2bib.py \
  0000-0002-1825-0097 \
  --min-year 2020 \
  --max-year 2024 \
  -o phd_papers.bib
```

## 📦 Output formats

### 📚 BibTeX

BibTeX is the default output format:

```bash
python3 scripts/orcid2bib.py 0000-0002-1825-0097 -y 2024 -f bibtex
```

Example:

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

### 📝 Markdown

Generate a numbered Markdown list with clickable DOI links:

```bash
python3 scripts/orcid2bib.py \
  0000-0002-1825-0097 \
  -y 2021 \
  -f markdown \
  -o cv_publications.md
```

This format is useful for CVs, personal websites, and GitHub profile pages.

### 📄 Formatted text

Generate a human-readable bibliography:

```bash
python3 scripts/orcid2bib.py \
  0000-0002-1825-0097 \
  -y 2021 \
  -f text
```

Choose a citation style with `--style` / `-s`:

```bash
python3 scripts/orcid2bib.py \
  10.1016/j.actamat.2025.121319 \
  -f text \
  --style nature
```

## 🎨 Citation styles

| Style | Flag | Example |
| --- | --- | --- |
| APA 7th | `--style apa` | `Smith, J., & Doe, J. (2024). Machine learning models... Journal of Materials Science, 59, 12048.` |
| Nature | `--style nature` | `1. Smith, J. & Doe, J. Machine learning models... Journal of Materials Science 59, 12048 (2024).` |
| IEEE | `--style ieee` | `[1] J. Smith and J. Doe, “Machine learning models...,” Journal of Materials Science, vol. 59, 2024.` |
| Elsevier | `--style elsevier` | `[1] J. Smith, J. Doe, Machine learning models..., Journal of Materials Science 59 (2024) 12048.` |
| ACS | `--style acs` | `(1) Smith, J.; Doe, J. Machine Learning Models... Journal of Materials Science 2024, 59, 12048.` |
| Chicago | `--style chicago` | `Smith, Jane, and John Doe. 2024. “Machine Learning Models...” Journal of Materials Science 59.` |
| Harvard | `--style harvard` | `Smith, J., Doe, J., 2024. Machine learning models... Journal of Materials Science 59, 12048.` |
| Springer | `--style springer` | `Smith J, Doe J (2024) Machine learning models... Journal of Materials Science 59:12048.` |

APA is the default text style.

## 🔄 Smart preprint deduplication

By default, `orcid2bib` compares preprint titles from sources such as arXiv, ChemRxiv, bioRxiv, and Research Square against journal publications in the same profile.

When a matching peer-reviewed journal article is present, the duplicate preprint is suppressed.

To keep all raw preprints:

```bash
python3 scripts/orcid2bib.py \
  0000-0002-1825-0097 \
  --no-dedup \
  -o all_raw_records.bib
```

## 👥 Batch processing

You can generate publication files for multiple researchers with a shell loop:

```bash
declare -A TEAM=(
  ["PI"]="0000-0002-1825-0097"
  ["CoPI"]="0000-0001-5109-3700"
)

for NAME in "${!TEAM[@]}"; do
  ORCID="${TEAM[$NAME]}"
  echo "Processing $NAME ($ORCID)..."
  python3 scripts/orcid2bib.py \
    "$ORCID" \
    -y 2021 \
    -o "${NAME}_publications.bib"
done
```

## 🧭 Command-line reference

| Argument | Short flag | Description |
| --- | :---: | --- |
| `target` | — | ORCID iD, DOI, or full ORCID/DOI URL; input type is auto-detected |
| `--doi DOI` | `-d` | Explicit DOI or comma-separated DOI list |
| `--min-year YEAR` | `-y` | Include publications from this year onward |
| `--max-year YEAR` | — | Include publications up to this year |
| `--output FILE` | `-o` | Write output to a file |
| `--format {bibtex,markdown,text}` | `-f` | Select output format; default is `bibtex` |
| `--style STYLE` | `-s` | Select citation style for `text` output |
| `--no-dedup` | — | Disable preprint deduplication |
| `--help` | `-h` | Show command-line help |

## 🐍 Python API

If `orcid2bib.py` is available on your Python path, its functions can also be imported directly:

```python
from orcid2bib import fetch_orcid, doi_to_bibtex, doi_to_text

# Fetch structured works from an ORCID profile
works = fetch_orcid(
    "0000-0002-1825-0097",
    min_year=2021,
)

# Fetch BibTeX for a DOI
bib = doi_to_bibtex(
    "10.1016/j.actamat.2025.121319"
)

# Fetch a formatted citation
citation = doi_to_text(
    "10.1016/j.actamat.2025.121319",
    style="nature",
)
```

## 📑 BibLaTeX integration

Generated BibTeX entries can be separated into categorized publication lists using the injected `keywords` field.

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

\addbibresource{my_publications.bib}

\begin{document}

\section*{Publications of the Principal Investigator}
\nocite{*}

\subsection*{Quality-Assured Publications}
\printbibliography[
  keyword=quality_assured,
  heading=none,
  resetnumbers=true
]

\subsection*{Other Scientific Outputs}
\printbibliography[
  keyword=other,
  heading=none,
  resetnumbers=true
]

\end{document}
```

Compile with:

```bash
pdflatex publication_list.tex
biber publication_list
pdflatex publication_list.tex
```

## ❓ FAQ

### 🧩 What happens if an ORCID work has no DOI?

The tool writes a commented placeholder to the BibTeX output instead of failing:

```text
% Work without DOI: Title (Year)
```

This makes missing DOI records easy to review manually.

### 🔗 Can I use a full ORCID URL?

Yes. Both of these forms are accepted:

```text
0000-0002-1825-0097
https://orcid.org/0000-0002-1825-0097
```

### 🔎 Can I pass a DOI directly?

Yes. A DOI can be provided as the positional target, as a full `doi.org` URL, or through `-d` / `--doi`.

```bash
python3 scripts/orcid2bib.py 10.1016/j.actamat.2025.121319
python3 scripts/orcid2bib.py https://doi.org/10.1016/j.actamat.2025.121319
python3 scripts/orcid2bib.py -d 10.1016/j.actamat.2025.121319
```

### 🔐 Does it require an ORCID API key?

No. Public ORCID profiles are queried through the public ORCID REST API v3.0 without an API token.

## 📄 License

Licensed under the [MIT License](LICENSE) for academic, personal, and commercial use.

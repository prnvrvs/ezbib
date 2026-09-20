# Usage Guide & Recipes

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

# 7. Interactive paste mode
ezbib
# Enter ORCID iD or DOI: https://doi.org/10.1016/...
```

## 🎨 Citation Styles

Generate pre-formatted citations in your desired journal format using the `--style` or `-s` flag:

| Style | Flag |
| :--- | :--- |
| **APA 7th** *(default)* | `-s apa` |
| **Nature** | `-s nature` |
| **IEEE** | `-s ieee` |
| **Elsevier** | `-s elsevier` |
| **ACS** | `-s acs` |
| **Chicago** | `-s chicago` |
| **Harvard** | `-s harvard` |

## 🧭 CLI Command-Line Reference

```text
usage: ezbib [-h] [-d DOI] [-y YEAR] [--max-year YEAR] [-o FILE]
             [-f {bibtex,markdown,text,apa}] [-s STYLE] [--no-dedup] [-v]
             [target]
```

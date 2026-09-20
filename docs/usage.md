# Usage Guide & Recipes

Here you will find common workflows for using `ezbib`, complete with example outputs.

## ⚡ Quick Start

### 1. Fetching an entire ORCID profile
Generate a complete, deduplicated BibTeX file for an author.
```bash
ezbib 0000-0002-1825-0097 -o publications.bib
```

```{dropdown} 📄 View Sample Output (publications.bib)
:color: primary
:icon: file-code

```bibtex
@article{Smith2025Hydrogen,
  title = {Hydrogen embrittlement mechanisms in high-strength alloys},
  author = {Smith, John and Doe, Jane},
  journal = {Acta Materialia},
  year = {2025},
  doi = {10.1016/j.actamat.2025.121319},
  keywords = {quality_assured}
}
```
```

### 2. Exporting a Markdown CV
Generate a clickable Markdown publication list for your personal website or CV.
```bash
ezbib 0000-0002-1825-0097 -f markdown -o cv.md
```

```{dropdown} 📝 View Sample Output (cv.md)
:color: success
:icon: markdown

```markdown
# Publications

1. **Hydrogen embrittlement mechanisms in high-strength alloys** (2025) — *Acta Materialia* ([DOI: 10.1016/j.actamat.2025.121319](https://doi.org/10.1016/j.actamat.2025.121319))
2. **Phase transformation dynamics under extreme strain** (2024) — *Nature Materials* ([DOI: 10.1038/s41563-024-00000-x](https://doi.org/10.1038/s41563-024-00000-x))
```
```

### 3. Styled Plain Text Citations
Generate pre-formatted citations in your desired journal format.

```bash
ezbib 10.1016/j.actamat.2025.121319 -f text --style nature
```
> **Sample Output:** 1. Smith, J. & Doe, J. Hydrogen embrittlement mechanisms in high-strength alloys. *Acta Materialia* **25**, 121319 (2025).

---

### 4. Interactive Web GUI
Don't want to use the command line? Start the built-in browser interface!
```bash
ezbib web
```
This automatically spins up a local web server (using only standard Python libraries) and opens a beautiful, interactive form in your default web browser!

## 🎨 Citation Styles

You can generate text citations in numerous formats using the `-s` flag.

| Style | Flag | Example Output snippet |
| :--- | :--- | :--- |
| **APA 7th** *(default)* | `-s apa` | Smith, J., & Doe, J. (2025). Hydrogen embrittlement... |
| **Nature** | `-s nature` | 1. Smith, J. & Doe, J. Hydrogen embrittlement... |
| **IEEE** | `-s ieee` | [1] J. Smith and J. Doe, “Hydrogen embrittlement...,” |
| **Elsevier** | `-s elsevier` | [1] J. Smith, J. Doe, Hydrogen embrittlement... |
| **ACS** | `-s acs` | (1) Smith, J.; Doe, J. Hydrogen embrittlement... |
| **Chicago** | `-s chicago` | Smith, John, and Jane Doe. 2025. “Hydrogen embrittlement...” |
| **Harvard** | `-s harvard` | Smith, J., Doe, J., 2025. Hydrogen embrittlement... |

```{tip}
Any valid CSL (Citation Style Language) identifier supported by Crossref can be passed to `--style`!
```

---

## ⌨️ Advanced Input Modes

```{admonition} Interactive Paste Mode
:class: note

If you run `ezbib` with no arguments, it will open an interactive prompt. This is perfect for pasting URLs that contain special characters (like parentheses) that would normally break your terminal shell!
```
```bash
$ ezbib
Enter ORCID iD or DOI (or press Enter to exit): https://doi.org/10.1016/S1359-6454(02)00577-3
```

```{admonition} Piped Input
:class: note
You can pass a list of DOIs directly from a text file using standard input (`-`).
```
```bash
cat my_dois.txt | ezbib - -o references.bib
```

---

## 🧭 CLI Command-Line Reference

```text
usage: ezbib [-h] [-d DOI] [-y YEAR] [--max-year YEAR] [-o FILE]
             [-f {bibtex,markdown,text,apa}] [-s STYLE] [--no-dedup] [-v]
             [target]
```

# 📚 ezbib Documentation

**Universal, zero-dependency CLI tool and Python library to convert ORCID profiles and DOIs into clean BibTeX, Markdown, and formatted academic citations.**

Welcome to the official documentation for `ezbib`.

Raw bibliographic metadata from academic APIs is frequently inconsistent, filled with XML fragments, cluttered with unreviewed preprints, and cumbersome to organize. `ezbib` was built specifically for researchers, lab managers, and scientific developers who need clean, publication-ready records without installing heavy dependencies.

## ✨ Key Features

- 📦 **Zero External Dependencies** — Built 100% on the Python Standard Library.
- ⌨️ **Interactive Paste Mode** — Paste complex DOIs without shell syntax errors.
- 🧹 **LaTeX & MathML Sanitization** — Auto-converts MathML to `$\alpha$`, `$\Sigma$`, etc.
- 🧠 **Intelligent Preprint Deduplication** — Auto-suppresses arXiv/bioRxiv preprints if peer-reviewed versions exist.
- 🏷️ **Grant-Ready BibLaTeX** — Auto-tags `quality_assured` for DFG, EU, & NSF proposals.

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
usage
api
faq
```

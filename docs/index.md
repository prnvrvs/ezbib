# 📚 ezbib Documentation

**Universal, zero-dependency CLI tool and Python library to convert ORCID profiles and DOIs into clean BibTeX, Markdown, and formatted academic citations.**

Welcome to the official documentation for `ezbib`.

Raw bibliographic metadata from academic APIs is frequently inconsistent, filled with XML fragments, cluttered with unreviewed preprints, and cumbersome to organize. `ezbib` was built specifically for researchers, lab managers, and scientific developers who need clean, publication-ready records without installing heavy dependencies.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} ⚡ Zero Dependencies
:class-header: bg-light
Built 100% on the Python Standard Library. No third-party packages required.
:::

:::{grid-item-card} ⌨️ Interactive Mode
:class-header: bg-light
Paste complex DOIs with special characters without breaking your terminal shell.
:::

:::{grid-item-card} 🧹 LaTeX Sanitization
:class-header: bg-light
Auto-converts messy MathML (`<mml:math>`) into clean standard LaTeX.
:::

:::{grid-item-card} 🧠 Smart Deduplication
:class-header: bg-light
Intelligently suppresses arXiv/bioRxiv preprints if peer-reviewed versions exist.
:::
::::

## 📖 Table of Contents

```{toctree}
:maxdepth: 2
:hidden: true

installation
usage
api
faq
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🚀 Getting Started
:link: installation
:link-type: doc

Learn how to install `ezbib` globally or run it directly without any installation.
:::

:::{grid-item-card} 💻 Usage & Recipes
:link: usage
:link-type: doc

Explore common CLI workflows, citation formats, and Markdown CV generation.
:::

:::{grid-item-card} 🐍 Python API
:link: api
:link-type: doc

Integrate `ezbib` programmatically into your own Python applications.
:::

:::{grid-item-card} ❓ FAQ
:link: faq
:link-type: doc

Answers to questions about ORCID API limits, missing DOIs, and citation styles.
:::
::::

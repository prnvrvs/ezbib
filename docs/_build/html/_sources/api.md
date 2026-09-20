# Python API Reference

`ezbib` can be imported and used programmatically in any Python 3.7+ application.

## Example Integration

```python
import ezbib

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

## 🛠️ API Documentation

```{eval-rst}
.. automodule:: ezbib
   :members:
   :undoc-members:
   :show-inheritance:
```

# Frequently Asked Questions

**Does ezbib require an ORCID API key or account?**
No. Public ORCID profiles are queried directly through the public ORCID REST API v3.0, and DOI metadata is resolved via Crossref content negotiation without requiring an API key.

**What happens if an ORCID publication has no DOI?**
If a work in the ORCID record does not have an attached DOI, `ezbib` outputs a clear commented placeholder in the BibTeX file:
`% Work without DOI: Title of Publication (Year)`
This ensures no entries are silently dropped while keeping your `.bib` file syntactically valid.

**How does preprint deduplication work?**
Preprints (identified by journal titles containing `arxiv`, `biorxiv`, `chemrxiv`, `research square` or type `PREPRINT`) are fuzzy-matched against peer-reviewed articles in the same ORCID profile. If a published journal version exists, the preprint is automatically suppressed unless `--no-dedup` is specified.

**Can I format citations in styles not listed above?**
Yes. Any valid CSL (Citation Style Language) style identifier supported by the Crossref citation service can be passed directly to `--style` (e.g. `--style cell`, `--style pnas`).

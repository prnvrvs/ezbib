#!/usr/bin/env python3
"""
orcid2bib - Universal CLI tool and Python library to convert ORCID iDs and DOIs
into clean, formatted BibTeX, Markdown, or styled citation text.

Zero external dependencies - uses standard library only.
"""

import sys

__version__ = "1.0.0"

REQUIRED_MODULES = [
    ("urllib.request", "Python standard HTTP/networking module"),
    ("urllib.parse", "Python standard URL parsing module"),
    ("urllib.error", "Python standard URL error handling module"),
    ("json", "Python standard JSON parser"),
    ("re", "Python standard regular expressions library"),
    ("argparse", "Python standard CLI argument parser"),
    ("time", "Python standard timing library"),
    ("os", "Python standard OS interface"),
]

missing = []
for mod, desc in REQUIRED_MODULES:
    try:
        __import__(mod)
    except ImportError:
        missing.append((mod, desc))

if missing or sys.version_info < (3, 7):
    print("\n" + "=" * 75, file=sys.stderr)
    print(" [!] ERROR: Missing Required Python Environment / Dependencies", file=sys.stderr)
    print("=" * 75, file=sys.stderr)
    if sys.version_info < (3, 7):
        print(f"  * Python Version: Found Python {sys.version_info.major}.{sys.version_info.minor}, but Python 3.7+ is required.", file=sys.stderr)
    for mod, desc in missing:
        print(f"  * Module '{mod}' is missing ({desc}).", file=sys.stderr)
    print("\n How to resolve:", file=sys.stderr)
    print("  1. Ensure you are running Python 3.7+: python3 --version", file=sys.stderr)
    if missing:
        print("  2. If using a stripped Python environment, install:", file=sys.stderr)
        print("     pip install " + " ".join([m[0].split(".")[0] for m in missing]), file=sys.stderr)
    print("=" * 75 + "\n", file=sys.stderr)
    sys.exit(1)

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = f"orcid2bib/{__version__} (Academic Research Tool; mailto:academic@research.org)"


def sanitize_latex(text):
    """Sanitize XML/MathML fragments into clean LaTeX text."""
    if not text:
        return ""
    text = re.sub(r"<mml:math.*?<mml:mi>α</mml:mi>.*?</mml:math>", lambda m: r"$\alpha$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>β</mml:mi>.*?</mml:math>", lambda m: r"$\beta$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>γ</mml:mi>.*?</mml:math>", lambda m: r"$\gamma$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>Σ</mml:mi>.*?</mml:math>", lambda m: r"$\Sigma$", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()


def pretty_format_bibtex(raw_bib, extra_keywords=None):
    """Clean and reorder BibTeX fields for consistent formatting."""
    raw_bib = sanitize_latex(raw_bib.strip())
    match = re.match(r"^@([a-zA-Z]+)\s*\{\s*([^,]+)\s*,\s*(.*)\}\s*$", raw_bib, re.DOTALL)
    if not match:
        return raw_bib

    entry_type = match.group(1).lower()
    cite_key = match.group(2).strip()
    body = match.group(3).strip()

    fields = []
    current = []
    brace_depth = 0
    in_quote = False

    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "{" and not in_quote:
            brace_depth += 1
            current.append(ch)
        elif ch == "}" and not in_quote:
            brace_depth -= 1
            current.append(ch)
        elif ch == '"' and brace_depth == 0:
            in_quote = not in_quote
            current.append(ch)
        elif ch == "," and brace_depth == 0 and not in_quote:
            field_str = "".join(current).strip()
            if field_str:
                fields.append(field_str)
            current = []
        else:
            current.append(ch)
        i += 1

    field_str = "".join(current).strip()
    if field_str:
        fields.append(field_str)

    preferred_order = ["author", "title", "journal", "booktitle", "volume", "number", "pages", "year", "month", "doi", "url", "issn", "publisher"]

    parsed_dict = {}
    for f in fields:
        eq_pos = f.find("=")
        if eq_pos != -1:
            k = f[:eq_pos].strip().lower()
            v = f[eq_pos + 1 :].strip()
            if (v.startswith("{") and v.endswith("}")) or (v.startswith('"') and v.endswith('"')):
                v = v[1:-1].strip()
            parsed_dict[k] = v
        else:
            parsed_dict[f] = None

    formatted_fields = []
    for k in preferred_order:
        if k in parsed_dict:
            formatted_fields.append(f"  {k} = {{{parsed_dict.pop(k)}}}")

    for k, v in parsed_dict.items():
        if v is not None:
            formatted_fields.append(f"  {k} = {{{v}}}")
        else:
            formatted_fields.append(f"  {k}")

    if extra_keywords:
        formatted_fields.append(f"  keywords = {{{extra_keywords}}}")

    fields_joined = ",\n".join(formatted_fields)
    return f"@{entry_type}{{{cite_key},\n{fields_joined}\n}}"


def doi_to_bibtex(doi, extra_keywords=None):
    """Fetch BibTeX entry for a given DOI via Crossref content negotiation."""
    clean_doi = doi.strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    url = f"https://doi.org/{clean_doi}"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/x-bibtex", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8")
            return pretty_format_bibtex(content, extra_keywords=extra_keywords)
    except Exception as e:
        return f"% Error fetching BibTeX for DOI {doi}: {e}"


STYLE_MAP = {
    "apa": "apa",
    "nature": "nature",
    "ieee": "ieee",
    "acs": "american-chemical-society",
    "chicago": "chicago-author-date",
    "elsevier": "elsevier-with-titles",
    "acta": "elsevier-with-titles",
    "harvard": "elsevier-harvard",
    "springer": "springer-basic-author-date",
    "mla": "modern-language-association",
}


def doi_to_text(doi, style="apa"):
    """Fetch formatted citation string for a DOI in a specific CSL style."""
    csl_style = STYLE_MAP.get(style.lower().strip(), style.strip())
    clean_doi = doi.strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    url = f"https://doi.org/{clean_doi}"
    req = urllib.request.Request(
        url,
        headers={"Accept": f"text/x-bibliography; style={csl_style}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8").strip()
            return sanitize_latex(content)
    except Exception:
        # Fallback to APA if custom style fails
        if csl_style != "apa":
            return doi_to_text(doi, style="apa")
        return f"[DOI: {doi}]"


def fetch_orcid(orcid_id, min_year=None, max_year=None, dedup=True):
    """Query ORCID Public API v3.0 to fetch and parse works for an ORCID iD."""
    clean_id = orcid_id.strip().replace("https://orcid.org/", "").strip()
    url = f"https://pub.orcid.org/v3.0/{clean_id}/works"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[-] Error querying ORCID {clean_id}: {e}", file=sys.stderr)
        return []

    works = []
    for g in data.get("group", []):
        summaries = g.get("work-summary", [])
        if not summaries:
            continue
        w = summaries[0]
        title = sanitize_latex(w.get("title", {}).get("title", {}).get("value", "Untitled"))

        pub_year = None
        pub_date = w.get("publication-date")
        if pub_date and pub_date.get("year"):
            try:
                pub_year = int(pub_date.get("year").get("value"))
            except (ValueError, TypeError):
                pub_year = None

        journal_obj = w.get("journal-title")
        journal = journal_obj.get("value") if journal_obj else ""
        wtype = w.get("type", "JOURNAL_ARTICLE")

        doi = None
        for ext in w.get("external-ids", {}).get("external-id", []):
            if ext.get("external-id-type", "").lower() == "doi":
                doi = ext.get("external-id-value")
                break

        if min_year and pub_year and pub_year < min_year:
            continue
        if max_year and pub_year and pub_year > max_year:
            continue

        works.append({
            "title": title,
            "year": pub_year,
            "journal": journal,
            "type": wtype,
            "doi": doi,
        })

    works.sort(key=lambda x: (x["year"] if x["year"] else 0), reverse=True)

    quality_types = {"JOURNAL_ARTICLE", "BOOK_CHAPTER", "BOOK", "CONFERENCE_PAPER", "PROCEEDINGS_ARTICLE"}
    published_titles = [
        re.sub(r"[^a-zA-Z0-9]", "", w["title"].lower())
        for w in works
        if w["type"] in quality_types or (w["journal"] and "arxiv" not in w["journal"].lower() and "preprint" not in w["journal"].lower())
    ]

    filtered_works = []
    for w in works:
        norm_title = re.sub(r"[^a-zA-Z0-9]", "", w["title"].lower())
        is_preprint = (
            w["type"] == "PREPRINT"
            or "arxiv" in (w["journal"] or "").lower()
            or "biorxiv" in (w["journal"] or "").lower()
            or "research square" in (w["journal"] or "").lower()
        )

        if is_preprint and dedup:
            is_duplicate = any(norm_title in pt or pt in norm_title or (len(norm_title) > 20 and norm_title[:30] in pt) for pt in published_titles)
            if is_duplicate:
                continue

        w["category"] = "quality_assured" if (w["type"] in quality_types or (w["journal"] and not is_preprint)) else "other"
        filtered_works.append(w)

    return filtered_works


def is_doi(text):
    """Determine whether an input string is a DOI or DOI URL."""
    clean = text.strip()
    return clean.startswith("10.") or "doi.org/10." in clean


def build_parser():
    """Build the command-line argument parser."""
    epilog_text = chr(10).join([
        "=" * 79,
        "PRACTICAL USAGE EXAMPLES:",
        "=" * 79,
        "  1. Fetch all works for an ORCID profile:",
        "     orcid2bib 0000-0002-1825-0097",
        "",
        "  2. Filter publications from year 2021 onwards and save to .bib:",
        "     orcid2bib 0000-0002-1825-0097 -y 2021 -o my_pubs.bib",
        "",
        "  3. Fetch BibTeX for a single DOI directly:",
        "     orcid2bib 10.1016/j.actamat.2025.121319",
        "     orcid2bib https://doi.org/10.1016/j.actamat.2025.121319",
        "",
        "  4. Fetch BibTeX using the explicit --doi / -d flag:",
        "     orcid2bib -d 10.1016/j.actamat.2025.121319 -o paper.bib",
        "",
        "  5. Print formatted bibliography in APA, Nature, IEEE, or ACS style:",
        "     orcid2bib 0000-0002-1825-0097 -y 2021 -f text",
        "     orcid2bib 10.1016/j.actamat.2025.121319 -f text --style nature",
        "     orcid2bib 10.1016/j.actamat.2025.121319 -f text --style ieee",
        "     orcid2bib 10.1016/j.actamat.2025.121319 -f text --style acs",
        "",
        "  6. Export as a formatted Markdown publication list for CV / Website:",
        "     orcid2bib 0000-0002-1825-0097 -y 2021 -f markdown -o cv_pubs.md",
        "",
        "  7. Include all raw preprints without deduplication:",
        "     orcid2bib 0000-0002-1825-0097 --no-dedup -o all_records.bib",
        "=" * 79,
    ])
    parser = argparse.ArgumentParser(
        prog="orcid2bib",
        description="orcid2bib - Universal CLI tool to convert any ORCID identifier or DOI into clean BibTeX, Markdown, or Plain Text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog_text,
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="ORCID identifier (e.g. 0000-0002-1825-0097) OR direct DOI (e.g. 10.1016/j.actamat.2025.121319). Use '-' to read from standard input.",
    )
    parser.add_argument("-d", "--doi", help="Single DOI or comma-separated list of DOIs to fetch directly")
    parser.add_argument("-y", "--min-year", type=int, default=None, metavar="YEAR", help="Filter publications published in or after this year (e.g. -y 2021)")
    parser.add_argument("--max-year", type=int, default=None, metavar="YEAR", help="Filter publications published up to this year (e.g. --max-year 2025)")
    parser.add_argument("-o", "--output", metavar="FILE", help="Save output directly to a file (e.g. -o publications.bib or -o cv.md)")
    parser.add_argument(
        "-f",
        "--format",
        choices=["bibtex", "markdown", "text", "apa"],
        default="bibtex",
        help="Output format: bibtex (default), markdown, or text",
    )
    parser.add_argument(
        "-s",
        "--style",
        default="apa",
        help="Citation style for text format: apa (default), nature, ieee, acs, elsevier, chicago, harvard, springer, mla",
    )
    parser.add_argument(
        "--no-dedup",
        action="store_true",
        help="Disable smart preprint deduplication (keep preprints even if published in a journal)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit",
    )

    return parser


def main(argv=None):
    """Main CLI entry point."""
    try:
        parser = build_parser()
        args = parser.parse_args(argv)

        target = args.doi or args.target

        # Handle stdin if target is '-'
        if target == "-":
            target = sys.stdin.read().strip()

        if not target:
            parser.print_help()
            return 0

        # 1. Direct DOI mode
        if args.doi or is_doi(target):
            dois = [d.strip() for d in re.split(r"[,\s\n]+", target) if d.strip()]
            results = []
            for d in dois:
                if args.format in ["text", "apa", "biblio"]:
                    print(f"[*] Fetching formatted citation for DOI: {d}...", file=sys.stderr)
                    cit = doi_to_text(d, style=args.style)
                    results.append(cit)
                else:
                    print(f"[*] Fetching BibTeX for DOI: {d}...", file=sys.stderr)
                    bib = doi_to_bibtex(d)
                    results.append(bib)
                time.sleep(0.15)
            output = "\n\n".join(results) + "\n"

        # 2. ORCID profile mode
        else:
            print(f"[*] Fetching works from ORCID: {target}...", file=sys.stderr)
            works = fetch_orcid(target, min_year=args.min_year, max_year=args.max_year, dedup=not args.no_dedup)
            print(f"[+] Found {len(works)} publications (filtered).", file=sys.stderr)

            if args.format == "bibtex":
                bib_entries = []
                for w in works:
                    if w["doi"]:
                        print(f"  -> Fetching BibTeX for DOI: {w['doi']}", file=sys.stderr)
                        b = doi_to_bibtex(w["doi"], extra_keywords=w["category"])
                        bib_entries.append(b)
                        time.sleep(0.15)
                    else:
                        bib_entries.append(f"% Work without DOI: {w['title']} ({w['year']})")
                output = "\n\n".join(bib_entries) + "\n"

            elif args.format == "markdown":
                lines = [f"# Publications from ORCID {target}\n"]
                for i, w in enumerate(works, 1):
                    y_str = f"({w['year']})" if w["year"] else ""
                    doi_str = f"[DOI: {w['doi']}](https://doi.org/{w['doi']})" if w["doi"] else "No DOI"
                    lines.append(f"{i}. **{w['title']}** {y_str} — *{w['journal'] or 'N/A'}* ({doi_str})")
                output = "\n".join(lines) + "\n"

            else:  # Simple text bibliography (APA/Nature/etc.)
                lines = [f"Publications from ORCID {target}:\n"]
                for i, w in enumerate(works, 1):
                    if w["doi"]:
                        print(f"  -> Fetching citation for DOI: {w['doi']}", file=sys.stderr)
                        cit = doi_to_text(w["doi"], style=args.style)
                        lines.append(f"{i}. {cit}")
                        time.sleep(0.15)
                    else:
                        lines.append(f"{i}. {w['title']} ({w['year'] or 'N/A'}) — {w['journal'] or 'N/A'}")
                output = "\n\n".join(lines) + "\n"

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"[+] Saved output to {args.output}", file=sys.stderr)
        else:
            print(output)
        return 0

    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())


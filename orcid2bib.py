#!/usr/bin/env python3
import sys

REQUIRED_MODULES = [
    ("urllib.request", "Python standard HTTP/networking module"),
    ("urllib.parse", "Python standard URL parsing module"),
    ("urllib.error", "Python standard URL error handling module"),
    ("json", "Python standard JSON parser"),
    ("re", "Python standard regular expressions library"),
    ("argparse", "Python standard CLI argument parser"),
    ("time", "Python standard timing library"),
    ("os", "Python standard OS interface")
]

missing = []
for mod, desc in REQUIRED_MODULES:
    try:
        __import__(mod)
    except ImportError:
        missing.append((mod, desc))

if missing or sys.version_info < (3, 7):
    print("\n" + "="*75, file=sys.stderr)
    print(" [!] ERROR: Missing Required Python Environment / Dependencies", file=sys.stderr)
    print("="*75, file=sys.stderr)
    if sys.version_info < (3, 7):
        print(f"  * Python Version: Found Python {sys.version_info.major}.{sys.version_info.minor}, but Python 3.7+ is required.", file=sys.stderr)
    for mod, desc in missing:
        print(f"  * Module '{mod}' is missing ({desc}).", file=sys.stderr)
    print("\n How to resolve:", file=sys.stderr)
    print("  1. Ensure you are running Python 3.7+: python3 --version", file=sys.stderr)
    if missing:
        print("  2. If using a stripped Python environment, install:", file=sys.stderr)
        print("     pip install " + " ".join([m[0].split(".")[0] for m in missing]), file=sys.stderr)
    print("="*75 + "\n", file=sys.stderr)
    sys.exit(1)

import argparse
import urllib.request
import urllib.parse
import urllib.error
import json
import re
import time
import os

USER_AGENT = "orcid2bib/1.0 (Academic Research Tool; mailto:academic@research.org)"

def sanitize_latex(text):
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
            v = f[eq_pos+1:].strip()
            if (v.startswith('{') and v.endswith('}')) or (v.startswith('"') and v.endswith('"')):
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
    clean_doi = doi.strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    url = f"https://doi.org/{clean_doi}"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/x-bibtex", "User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8")
            return pretty_format_bibtex(content, extra_keywords=extra_keywords)
    except Exception as e:
        return f"% Error fetching BibTeX for DOI {doi}: {e}"

def fetch_orcid(orcid_id, min_year=None, max_year=None, dedup=True):
    clean_id = orcid_id.strip().replace("https://orcid.org/", "").strip()
    url = f"https://pub.orcid.org/v3.0/{clean_id}/works"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT}
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
            "doi": doi
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
            w["type"] == "PREPRINT" or 
            "arxiv" in (w["journal"] or "").lower() or 
            "biorxiv" in (w["journal"] or "").lower() or 
            "research square" in (w["journal"] or "").lower()
        )

        if is_preprint and dedup:
            is_duplicate = any(norm_title in pt or pt in norm_title or (len(norm_title) > 20 and norm_title[:30] in pt) for pt in published_titles)
            if is_duplicate:
                continue

        w["category"] = "quality_assured" if (w["type"] in quality_types or (w["journal"] and not is_preprint)) else "other"
        filtered_works.append(w)

    return filtered_works

def build_parser():
    epilog_text = chr(10).join([
        "=" * 79,
        "PRACTICAL USAGE EXAMPLES:",
        "=" * 79,
        "  1. Quick print BibTeX to terminal:",
        "     python3 orcid2bib.py 0000-0002-3661-5870",
        "",
        "  2. Filter publications from year 2021 onwards and save to .bib:",
        "     python3 orcid2bib.py 0000-0002-3661-5870 -y 2021 -o my_pubs.bib",
        "",
        "  3. Filter for a specific year range (e.g. 2021 to 2025):",
        "     python3 orcid2bib.py 0000-0002-3661-5870 -y 2021 --max-year 2025 -o recent.bib",
        "",
        "  4. Export as a formatted Markdown publication list for CV / Website:",
        "     python3 orcid2bib.py 0000-0002-3661-5870 -y 2021 -f markdown -o cv_pubs.md",
        "",
        "  5. Include all raw preprints without deduplication:",
        "     python3 orcid2bib.py 0000-0002-3661-5870 --no-dedup -o all_records.bib",
        "",
        "=" * 79,
        "QUICK TIP - MAKE IT A GLOBAL COMMAND (RUN FROM ANY DIRECTORY):",
        "=" * 79,
        "  Add this line to your ~/.zshrc or ~/.bashrc:",
        "     alias orcid2bib=\"python3 /Users/pranav/scripts/orcid2bib.py\"",
        "  Then run: source ~/.zshrc",
        "  Now you can simply run: orcid2bib 0000-0002-3661-5870 -y 2021 -o pubs.bib",
        "=" * 79
    ])
    parser = argparse.ArgumentParser(
        prog="python3 orcid2bib.py",
        description="orcid2bib - Zero-dependency CLI tool to convert any ORCID identifier into clean, formatted BibTeX, Markdown, or Plain Text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog_text
    )
    parser.add_argument("orcid", nargs="?", help="Researcher 16-digit ORCID identifier (e.g. 0000-0002-3661-5870 or https://orcid.org/...)")
    parser.add_argument("-y", "--min-year", type=int, default=None, metavar="YEAR", help="Filter publications published in or after this year (e.g. -y 2021)")
    parser.add_argument("--max-year", type=int, default=None, metavar="YEAR", help="Filter publications published up to this year (e.g. --max-year 2025)")
    parser.add_argument("-o", "--output", metavar="FILE", help="Save output directly to a file (e.g. -o publications.bib or -o cv.md)")
    parser.add_argument("-f", "--format", choices=["bibtex", "markdown", "text"], default="bibtex", help="Output format: bibtex (default), markdown, or text")
    parser.add_argument("--no-dedup", action="store_true", help="Disable smart preprint deduplication (keep preprints even if published in a journal)")

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.orcid:
        parser.print_help()
        sys.exit(0)

    print(f"[*] Fetching works from ORCID: {args.orcid}...", file=sys.stderr)
    works = fetch_orcid(args.orcid, min_year=args.min_year, max_year=args.max_year, dedup=not args.no_dedup)
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
        lines = [f"# Publications from ORCID {args.orcid}\n"]
        for i, w in enumerate(works, 1):
            y_str = f"({w['year']})" if w["year"] else ""
            doi_str = f"[DOI: {w['doi']}](https://doi.org/{w['doi']})" if w["doi"] else "No DOI"
            lines.append(f"{i}. **{w['title']}** {y_str} — *{w['journal'] or 'N/A'}* ({doi_str})")
        output = "\n".join(lines) + "\n"

    else:
        lines = []
        for i, w in enumerate(works, 1):
            lines.append(f"{i}. [{w['year'] or 'N/A'}] {w['title']}\n   Journal: {w['journal'] or 'N/A'}\n   DOI: {w['doi'] or 'N/A'}\n")
        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[+] Saved {len(works)} entries to {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()

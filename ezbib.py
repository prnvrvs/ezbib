#!/usr/bin/env python3
"""
orcid2bib - Universal CLI tool and Python library to convert ORCID iDs and DOIs
into clean, formatted BibTeX, Markdown, or styled citation text.

Zero external dependencies - uses standard library only.
"""

import sys

__version__ = "1.1.1"

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
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = f"orcid2bib/{__version__} (Academic Research Tool; mailto:academic@research.org)"


def sanitize_latex(text):
    """Sanitize XML/MathML fragments and entities into clean LaTeX text."""
    if not text:
        return ""
    text = str(text)
    # Convert common MathML entities / tags to LaTeX
    text = re.sub(r"<mml:math.*?<mml:mi>α</mml:mi>.*?</mml:math>", r"$\\alpha$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>β</mml:mi>.*?</mml:math>", r"$\\beta$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>γ</mml:mi>.*?</mml:math>", r"$\\gamma$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>Σ</mml:mi>.*?</mml:math>", r"$\\Sigma$", text, flags=re.DOTALL)
    text = re.sub(r"<mml:math.*?<mml:mi>σ</mml:mi>.*?</mml:math>", r"$\\sigma$", text, flags=re.DOTALL)
    # Strip remaining XML/HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Unescape HTML entities (&amp;, &lt;, &gt;, &ndash;, &#945;, etc.)
    text = html.unescape(text)
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


def clean_doi_str(doi):
    """Normalize and extract a clean DOI string from various URL and string formats."""
    if not doi:
        return ""
    d = str(doi).strip()
    d = urllib.parse.unquote(d)
    # Strip surrounding quotes, backticks, angle brackets
    d = d.strip("'\"`<> \t\r\n")
    # Remove URL prefixes and DOI URI schemes
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.IGNORECASE)
    d = re.sub(r"^doi:\s*", "", d, flags=re.IGNORECASE)
    # Strip any trailing punctuation often copied from text or markdown links
    d = d.rstrip(".,;)>]}")
    match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", d)
    if match:
        return match.group(1).strip().rstrip(".,;)>]}")
    return d.strip()


def is_doi(text):
    """Determine whether an input string is a DOI or DOI URL."""
    clean = clean_doi_str(text)
    return clean.startswith("10.")


def doi_to_bibtex(doi, extra_keywords=None):
    """Fetch BibTeX entry for a given DOI via Crossref content negotiation."""
    clean_doi = clean_doi_str(doi)
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
    clean_doi = clean_doi_str(doi)
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
        title_obj = (w.get("title") or {}).get("title") or {}
        title = sanitize_latex(title_obj.get("value", "Untitled"))

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
        ext_ids = (w.get("external-ids") or {}).get("external-id", [])
        for ext in ext_ids:
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



# ==============================================================================
# WEB GUI MODULE
# ==============================================================================
import http.server
import socketserver
import webbrowser
import json
import threading

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ezbib - Web Interface</title>
    <style>
        :root {
            --bg: #f8f9fa; --surface: #ffffff; --primary: #3b82f6; --primary-hover: #2563eb;
            --text: #1f2937; --text-secondary: #4b5563; --border: #e5e7eb;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); max-width: 800px; margin: 40px auto; padding: 0 20px; }
        h1 { text-align: center; color: var(--primary); margin-bottom: 5px; }
        p.subtitle { text-align: center; color: var(--text-secondary); margin-bottom: 30px; }
        .card { background: var(--surface); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: 600; margin-bottom: 5px; font-size: 14px; }
        input[type="text"], select { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        input[type="text"]:focus, select:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
        .row { display: flex; gap: 15px; }
        .row .form-group { flex: 1; }
        button { background: var(--primary); color: white; border: none; padding: 12px 20px; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%; transition: background 0.2s; }
        button:hover { background: var(--primary-hover); }
        button:disabled { background: #9ca3af; cursor: not-allowed; }
        pre { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; white-space: pre-wrap; }
        #output-container { display: none; position: relative; }
        .copy-btn { position: absolute; top: 10px; right: 10px; background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.2); padding: 5px 10px; border-radius: 4px; font-size: 12px; cursor: pointer; }
        .copy-btn:hover { background: rgba(255, 255, 255, 0.2); }
        .loader { border: 3px solid #f3f3f3; border-top: 3px solid var(--primary); border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; margin: 0 auto; display: none; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <h1>📚 ezbib</h1>
    <p class="subtitle">Convert ORCID profiles & DOIs into clean citations</p>
    
    <div class="card">
        <form id="ezbib-form">
            <div class="form-group">
                <label for="target">ORCID iD or DOI</label>
                <input type="text" id="target" placeholder="e.g. 0000-0002-1825-0097 or 10.1016/j.actamat.2025.121319" required>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label for="format">Format</label>
                    <select id="format">
                        <option value="bibtex">BibTeX</option>
                        <option value="markdown">Markdown CV</option>
                        <option value="text">Plain Text</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="style">Citation Style</label>
                    <select id="style" disabled>
                        <option value="apa">APA 7th</option>
                        <option value="nature">Nature</option>
                        <option value="ieee">IEEE</option>
                        <option value="chicago">Chicago</option>
                        <option value="harvard">Harvard</option>
                    </select>
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label for="min_year">Min Year (Optional)</label>
                    <input type="text" id="min_year" placeholder="e.g. 2021">
                </div>
                <div class="form-group" style="display: flex; align-items: center; margin-top: 20px;">
                    <input type="checkbox" id="dedup" checked style="width: auto; margin-right: 8px;">
                    <label for="dedup" style="margin-bottom: 0;">Smart Deduplication</label>
                </div>
            </div>
            
            <button type="submit" id="submit-btn">Generate Citations</button>
            <div class="loader" id="loader"></div>
        </form>
    </div>

    <div class="card" id="output-container">
        <button class="copy-btn" onclick="copyOutput()">Copy</button>
        <pre id="output"></pre>
    </div>

    <script>
        const formatSelect = document.getElementById('format');
        const styleSelect = document.getElementById('style');
        const form = document.getElementById('ezbib-form');
        const submitBtn = document.getElementById('submit-btn');
        const loader = document.getElementById('loader');
        const outputContainer = document.getElementById('output-container');
        const outputEl = document.getElementById('output');

        formatSelect.addEventListener('change', () => {
            styleSelect.disabled = formatSelect.value !== 'text';
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            submitBtn.style.display = 'none';
            loader.style.display = 'block';
            outputContainer.style.display = 'none';

            const payload = {
                target: document.getElementById('target').value,
                format: document.getElementById('format').value,
                style: document.getElementById('style').value,
                min_year: document.getElementById('min_year').value,
                dedup: document.getElementById('dedup').checked
            };

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                outputEl.textContent = data.result || data.error;
                outputContainer.style.display = 'block';
            } catch (err) {
                outputEl.textContent = 'Error: ' + err.message;
                outputContainer.style.display = 'block';
            } finally {
                submitBtn.style.display = 'block';
                loader.style.display = 'none';
            }
        });

        function copyOutput() {
            navigator.clipboard.writeText(outputEl.textContent);
            const btn = document.querySelector('.copy-btn');
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 2000);
        }
    </script>
</body>
</html>
"""

class WebGUIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/generate':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            target = req.get('target', '').strip()
            fmt = req.get('format', 'bibtex')
            style = req.get('style', 'apa')
            min_year = req.get('min_year')
            min_year = int(min_year) if min_year and min_year.isdigit() else None
            dedup = req.get('dedup', True)
            
            try:
                if is_doi(target):
                    dois = [d.strip() for d in re.split(r"[,\s\n]+", target) if d.strip()]
                    results = []
                    for d in dois:
                        if fmt in ["text", "apa", "biblio"]:
                            results.append(doi_to_text(d, style=style))
                        elif fmt == "markdown":
                            results.append(f"- [DOI: {d}](https://doi.org/{d})") 
                        else:
                            results.append(doi_to_bibtex(d))
                    output = "\n\n".join(results)
                else:
                    works = fetch_orcid(target, min_year=min_year, dedup=dedup)
                    if fmt == "bibtex":
                        entries = [doi_to_bibtex(w['doi'], extra_keywords=w['category']) if w['doi'] else f"% Work without DOI: {w['title']} ({w['year']})" for w in works]
                        output = "\n\n".join(entries)
                    elif fmt == "markdown":
                        lines = [f"# Publications from ORCID {target}\n"]
                        for i, w in enumerate(works, 1):
                            y_str = f"({w['year']})" if w['year'] else ""
                            doi_str = f"[DOI: {w['doi']}](https://doi.org/{w['doi']})" if w['doi'] else "No DOI"
                            lines.append(f"{i}. **{w['title']}** {y_str} — *{w['journal'] or 'N/A'}* ({doi_str})")
                        output = "\n".join(lines)
                    else:
                        lines = [f"Publications from ORCID {target}:\n"]
                        for i, w in enumerate(works, 1):
                            if w["doi"]:
                                lines.append(f"{i}. {doi_to_text(w['doi'], style=style)}")
                            else:
                                lines.append(f"{i}. {w['title']} ({w['year'] or 'N/A'})")
                        output = "\n\n".join(lines)
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"result": output}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def start_web_server():
    port = 8080
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("", port), WebGUIHandler)
    except OSError:
        port = 8081
        httpd = socketserver.TCPServer(("", port), WebGUIHandler)
        
    print(f"[*] Starting ezbib Web GUI at http://localhost:{port}")
    
    def open_browser():
        import time
        time.sleep(0.5)
        webbrowser.open_new_tab(f'http://localhost:{port}')
        
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Web GUI...")
        httpd.server_close()
        return 0



def build_parser():
    """Build the command-line argument parser."""
    epilog_text = chr(10).join([
        "=" * 79,
        "PRACTICAL USAGE EXAMPLES:",
        "=" * 79,
        "  1. Fetch all works for an ORCID profile:",
        "     ezbib 0000-0002-1825-0097",
        "",
        "  2. Filter publications from year 2021 onwards and save to .bib:",
        "     ezbib 0000-0002-1825-0097 -y 2021 -o my_pubs.bib",
        "",
        "  3. Fetch BibTeX for a single DOI directly:",
        "     ezbib 10.1016/j.actamat.2025.121319",
        "     ezbib https://doi.org/10.1016/j.actamat.2025.121319",
        "",
        "  4. Fetch BibTeX using the explicit --doi / -d flag:",
        "     ezbib -d 10.1016/j.actamat.2025.121319 -o paper.bib",
        "",
        "  5. Print formatted bibliography in APA, Nature, IEEE, or ACS style:",
        "     ezbib 0000-0002-1825-0097 -y 2021 -f text",
        "     ezbib 10.1016/j.actamat.2025.121319 -f text --style nature",
        "     ezbib 10.1016/j.actamat.2025.121319 -f text --style ieee",
        "     ezbib 10.1016/j.actamat.2025.121319 -f text --style acs",
        "",
        "  6. Export as a formatted Markdown publication list for CV / Website:",
        "     ezbib 0000-0002-1825-0097 -y 2021 -f markdown -o cv_pubs.md",
        "",
        "  7. Include all raw preprints without deduplication:",
        "     ezbib 0000-0002-1825-0097 --no-dedup -o all_records.bib",
        "=" * 79,
    ])
    parser = argparse.ArgumentParser(
        prog="ezbib",
        description="ezbib - Universal CLI tool to convert any ORCID identifier or DOI into clean BibTeX, Markdown, or Plain Text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog_text,
    )
    parser.add_argument(
        "target",
        nargs="*",
        help="ORCID identifier, DOI, or 'web' to start the browser GUI.",
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

        target = args.doi or (" ".join(args.target).strip() if isinstance(args.target, list) else (args.target or ""))

        # Handle stdin if target is '-'
        # Handle stdin if target is '-'
        if target == "-":
            target = sys.stdin.read().strip()
            
        if target.lower() == "web":
            return start_web_server()

        # If no target was passed, prompt interactively if in a terminal
        if not target and not args.doi:
            if sys.stdin.isatty():
                try:
                    target = input("Enter ORCID iD or DOI (or press Enter to exit): ").strip()
                except (EOFError, KeyboardInterrupt):
                    return 0
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


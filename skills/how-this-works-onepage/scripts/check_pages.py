#!/usr/bin/env python3
"""Check local files, HTML anchors and entry reachability in a rendered study directory."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append((self.getpos()[0], attrs[key], tag == "a" and key == "href"))


def check(root, entry="index.html"):
    root = Path(root).resolve()
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".html", ".htm"})
    pages = {p: Page(p.read_text(encoding="utf-8")) for p in files}
    issues, unverified, edges, checked = [], [], {p: set() for p in files}, 0
    for source, page in pages.items():
        for line, raw, navigation in page.links:
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if path.startswith("/"):
                unverified.append({"file": str(source.relative_to(root)), "line": line, "url": raw,
                                   "reason": "Root-relative link depends on the deployment root"})
                continue
            checked += 1
            target = (source.parent / path).resolve() if path else source
            if target.is_dir():
                target /= "index.html"
            problem = None
            if not target.is_relative_to(root):
                problem = "Local target is outside the supplied study directory"
            elif not target.is_file():
                problem = "Local target does not exist"
            elif target in pages and url.fragment and unquote(url.fragment) not in pages[target].ids:
                problem = "HTML anchor does not exist"
            if problem:
                issues.append({"file": str(source.relative_to(root)), "line": line, "url": raw, "problem": problem})
            elif navigation and target in pages:
                edges[source].add(target)
    start = (root / entry).resolve()
    reachable, pending = set(), [start] if start in pages else []
    if not pending:
        issues.append({"problem": "Entry page not found in the study", "entry": entry})
    while pending:
        page = pending.pop()
        if page not in reachable:
            reachable.add(page)
            pending.extend(edges[page] - reachable)
    return {"pages": len(pages), "checked_local_links": checked, "issues": issues,
            "unverified_links": unverified,
            "unlinked_pages": [str(p.relative_to(root)) for p in files if p not in reachable],
            "scope": "Static relative targets, HTML anchors and entry reachability through verified links only. "
                     "External URLs, JavaScript interactions and readability are not checked. "
                     "Root-relative URLs are reported as unverified without deployment context. "
                     "Unlinked pages are reported for review, not treated as errors."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing only the study to deliver")
    parser.add_argument("--entry", default="index.html", help="Entry HTML path relative to the directory")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error("Study directory does not exist")
    try:
        result = check(args.directory, args.entry)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result["issues"])


if __name__ == "__main__":
    raise SystemExit(main())

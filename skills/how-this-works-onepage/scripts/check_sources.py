#!/usr/bin/env python3
"""Check Markdown GitHub source citations against fixed local Git repositories."""
import argparse
import functools
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit


@functools.lru_cache(maxsize=None)
def git(repo, *args):
    result = subprocess.run(
        ["git", "--no-lazy-fetch", f"--git-dir={repo}", *args], capture_output=True
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Git check failed")
    return result.stdout


def numbered(lines, start, end):
    return "\n".join(f"{index + 1}: {lines[index]}" for index in range(start - 1, end))


def check(files, repositories, evidence=False, evidence_urls=()):
    checked, issues, excerpts = 0, [], []
    requested = set(evidence_urls)
    seen = set()
    evidence = evidence or bool(requested)
    for filename in files:
        lines = Path(filename).read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, 1):
            for wrapped, bare in re.findall(r'<(https://github\.com/[^\s>]+)>|(https://github\.com/[^\s<>"\'\]]+)', line):
                raw = wrapped or bare.rstrip(".,;，。")
                if not wrapped:
                    depth = 0
                    for offset, character in enumerate(raw):
                        if character == "(":
                            depth += 1
                        elif character == ")":
                            if depth == 0:
                                raw = raw[:offset]
                                break
                            depth -= 1
                url = urlsplit(raw)
                parts = url.path.strip("/").split("/", 4)
                if len(parts) < 4 or parts[2] not in {"blob", "commit"}:
                    continue
                checked += 1
                seen.add(raw)
                include_excerpt = evidence and (not requested or raw in requested)
                name, kind, revision = "/".join(parts[:2]), parts[2], parts[3]
                try:
                    excerpt = None
                    excerpt_note = "No line excerpt: commit link or whole-file citation."
                    if name not in repositories:
                        raise ValueError(f"No local repository configured for {name}")
                    repo = repositories[name]
                    if not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", revision):
                        raise ValueError("Use a full fixed commit hash")
                    git(repo, "cat-file", "-e", revision + "^{commit}")
                    if kind == "blob":
                        if len(parts) != 5:
                            raise ValueError("Missing source path")
                        blob = git(repo, "cat-file", "blob", revision + ":" + unquote(parts[4]))
                        if url.fragment:
                            bounds = re.fullmatch(r"L(\d+)(?:-L(\d+))?", url.fragment)
                            if not bounds:
                                raise ValueError("Only #Lstart[-Lend] source anchors are checked")
                            start, end = int(bounds[1]), int(bounds[2] or bounds[1])
                            if not 1 <= start <= end <= len(blob.splitlines()):
                                raise ValueError("Source line range is outside the file")
                            if include_excerpt:
                                try:
                                    source_lines = [item.decode("utf-8") for item in blob.splitlines()]
                                    excerpt = numbered(source_lines, start, end)
                                    excerpt_note = "Exact cited range only; semantic support not checked."
                                except UnicodeError:
                                    excerpt_note = "No text excerpt: source is not UTF-8."
                    if include_excerpt:
                        excerpts.append({"file": str(filename), "line": line_number, "url": raw,
                                         "draft_context": numbered(lines, max(1, line_number - 3),
                                                                   min(len(lines), line_number + 3)),
                                         "source_excerpt": excerpt, "note": excerpt_note})
                except ValueError as error:
                    issues.append({"file": str(filename), "line": line_number,
                                   "url": raw, "problem": str(error)})
    if not checked:
        issues.append({"problem": "No GitHub blob/commit citations found"})
    for url in sorted(requested - seen):
        issues.append({"url": url, "problem": "Requested evidence URL not found in the supplied drafts"})
    result = {"checked": checked, "issues": issues,
              "scope": "Commit existence, source path and line bounds only; "
                       "not semantic support, version consistency or remote provenance."}
    if evidence:
        result["evidence"] = excerpts
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", nargs="+", type=Path, help="Markdown draft(s)")
    parser.add_argument("--evidence", action="store_true",
                        help="Include nearby draft text and exact cited UTF-8 source lines for review; "
                             "does not judge semantic support or dump whole-file/commit contents")
    parser.add_argument("--evidence-url", action="append", default=[], metavar="URL",
                        help="Include excerpts only for this exact citation URL; repeat as needed. "
                             "All citations are still mechanically checked")
    parser.add_argument("--repo", action="append", nargs=2, required=True,
                        metavar=("OWNER/NAME", "GIT_DIR"),
                        help="Map a GitHub repository to local Git objects; repeat for multiple repositories")
    args = parser.parse_args()
    repositories = {}
    for name, directory in args.repo:
        if name in repositories:
            parser.error(f"Duplicate repository: {name}")
        try:
            git(directory, "rev-parse", "--git-dir")
        except ValueError as error:
            parser.error(str(error))
        repositories[name] = directory
    try:
        result = check(args.draft, repositories, evidence=args.evidence, evidence_urls=args.evidence_url)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result["issues"])


if __name__ == "__main__":
    raise SystemExit(main())

"""Offline source checks, including historical evidence on a separate branch."""
import subprocess
import tempfile
from pathlib import Path

from check_sources import check


def test_citations():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        def run(*args):
            return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL).decode().strip()
        run("init", "-q")
        run("config", "user.name", "Test")
        run("config", "user.email", "test@example.invalid")
        (root / "a.py").write_text("one\ntwo\n")
        (root / "f(x).py").write_text("bracketed\n")
        run("add", "a.py", "f(x).py")
        run("commit", "-qm", "first")
        first = run("rev-parse", "HEAD")
        (root / "a.py").write_text("one\ntwo\nthree\n")
        run("commit", "-qam", "endpoint")
        endpoint = run("rev-parse", "HEAD")
        run("checkout", "-qb", "other", first)
        (root / "other.py").write_text("other\n")
        run("add", "other.py")
        run("commit", "-qm", "unrelated branch")
        other = run("rev-parse", "HEAD")
        repos = {"test/repo": str(root / ".git")}
        draft = root / "draft.md"
        cases = [
            (f"blob/{first}/a.py#L1-L2", True),
            (f"commit/{endpoint}", True),
            (f"blob/{first}/a.py#L3", False),
            (f"blob/{first}/missing.py", False),
            (f"blob/{other}/other.py#L1", True),
            ("blob/main/a.py#L1", False),
            (f"blob/{first}/a.py#L2-L1", False),
        ]
        for target, valid in cases:
            draft.write_text(f"[source](https://github.com/test/repo/{target})\n")
            result = check([draft], repos)
            assert (not result["issues"]) == valid, (target, result)
        for target in [f"<https://github.com/test/repo/blob/{first}/f(x).py#L1>",
                       f"https://github.com/test/repo/blob/{first}/f(x).py#L1"]:
            draft.write_text(f"[source]({target})\n")
            assert not check([draft], repos)["issues"]
        citation = f"https://github.com/test/repo/blob/{first}/a.py#L1"
        draft.write_text(f"[来源]({citation})、[另一个来源]({citation})。\n", encoding="utf-8")
        result = check([draft], repos)
        assert result["checked"] == 2 and not result["issues"]

        # A valid location can still support an incorrect claim. Expose the exact
        # evidence without treating a successful mechanical check as agreement.
        draft.write_text(f"# Example\n\nThis deletes the database. [source]({citation})\n\nNext paragraph.\n")
        original = draft.read_bytes()
        result = check([draft], repos, evidence=True)
        assert not result["issues"] and result["checked"] == 1
        evidence = result["evidence"][0]
        assert evidence["source_excerpt"] == "1: one"
        assert "3: This deletes the database." in evidence["draft_context"]
        assert evidence["line"] == 3
        assert draft.read_bytes() == original
        draft.write_text(f"https://github.com/test/repo/blob/{first}/a.py#L1-L2")
        assert check([draft], repos, evidence=True)["evidence"][0]["source_excerpt"] == "1: one\n2: two"
        for target in [f"blob/{first}/a.py", f"commit/{first}"]:
            draft.write_text(f"https://github.com/test/repo/{target}")
            result = check([draft], repos, evidence=True)
            assert not result["issues"] and result["evidence"][0]["source_excerpt"] is None
        draft.write_text(f"https://github.com/test/repo/blob/{first}/a.py#L9")
        result = check([draft], repos, evidence=True)
        assert result["issues"] and not result["evidence"]

        missing_url = f"https://github.com/test/repo/blob/{first}/missing.py"
        draft.write_text(f"[one]({citation})\n[broken]({missing_url})\n")
        result = check([draft], repos, evidence_urls=[citation])
        assert result["checked"] == 2 and len(result["issues"]) == 1
        assert len(result["evidence"]) == 1 and result["evidence"][0]["url"] == citation
        assert result["evidence"][0]["source_excerpt"] == "1: one"
        result = check([draft], repos, evidence_urls=[citation + "-L2"])
        assert len(result["issues"]) == 2 and not result["evidence"]

        draft.write_text("No source yet")
        assert check([draft], repos)["issues"]
        draft.write_text(f"https://github.com/unknown/repo/commit/{first}")
        assert check([draft], repos)["issues"]

        # A missing object in a promisor repository must not trigger a fetch.
        clone = root / "partial"
        subprocess.check_call(["git", "clone", "--no-hardlinks", str(root), str(clone)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "-C", str(clone), "config", "remote.origin.promisor", "true"])
        subprocess.check_call(["git", "-C", str(clone), "config", "remote.origin.partialclonefilter", "blob:none"])
        blob = run("rev-parse", first + ":a.py")
        missing = clone / ".git/objects" / blob[:2] / blob[2:]
        missing.unlink()
        packs = set((clone / ".git/objects/pack").iterdir())
        draft.write_text(f"https://github.com/test/repo/blob/{first}/a.py#L1")
        partial = {"test/repo": str(clone / ".git")}
        assert check([draft], partial)["issues"]
        assert not missing.exists()
        assert set((clone / ".git/objects/pack").iterdir()) == packs


if __name__ == "__main__":
    test_citations()
    print("Source citation checks passed (real offline Git fixture).")

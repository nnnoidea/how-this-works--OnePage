"""A linked study with a missing page, wrong anchor, assets and an orphan page."""
import tempfile
from pathlib import Path
from check_pages import check


def test_pages():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "detail").mkdir()
        (root / "detail/a b.html").write_text('<h2 id="deep">Detail</h2><a href="../index.html#intro">Back</a>')
        (root / "asset.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        main = root / "index.html"
        main.write_text('<h1 id="intro">Start</h1><a href="detail/a%20b.html?mode=dark#deep">Read</a>'
                        '<a href="#intro">Top</a><img src="asset.svg"><a href="https://example.invalid/">External</a>'
                        '<script>const example = \'<a href="missing.html">\';</script>')
        original = main.read_bytes()
        result = check(root)
        assert result["pages"] == 2 and not result["issues"] and not result["unlinked_pages"], result
        assert result["checked_local_links"] == 4
        assert main.read_bytes() == original
        (root / "orphan.html").write_text('<h1>Orphan</h1>')
        result = check(root)
        assert result["unlinked_pages"] == ["orphan.html"] and not result["issues"]
        main.write_text(original.decode() + '<a href="absent.html">Missing</a><a href="detail/a%20b.html#wrong">Wrong</a>')
        result = check(root)
        assert {x["problem"] for x in result["issues"]} == {"Local target does not exist", "HTML anchor does not exist"}
        assert check(root, "missing.html")["issues"]
        main.write_text('<h1 id="intro">Start</h1><a href="/detail/a%20b.html#deep">Root</a><a href="../outside.html">Outside</a>')
        result = check(root)
        assert len(result["issues"]) == 1 and "outside" in result["issues"][0]["problem"]
        assert len(result["unverified_links"]) == 1
        assert result["unverified_links"][0]["url"] == "/detail/a%20b.html#deep"
        assert "detail/a b.html" in result["unlinked_pages"]


if __name__ == "__main__":
    test_pages()
    print("Local links, anchors, assets, reachability and unchanged inputs passed.")

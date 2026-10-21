"""Verify that every quoted phrase in a draft appears verbatim in the source.

Usage: python quote_check.py draft.md source.txt [source2.txt ...]
Matching ignores case, punctuation and whitespace. Exit 1 if any quote is missing.
Quote marks promise the exact words. A paraphrase goes without them.
"""
import re
import sys
from pathlib import Path

QUOTE = re.compile(r"[\"“]([^\"”\n]{4,200})[\"”]")


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


def missing_quotes(draft: str, source: str) -> list[str]:
    src = norm(source)
    return [q for q in QUOTE.findall(draft) if norm(q) not in src]


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("usage: quote_check.py draft.md source.txt [more sources]")
    draft = Path(sys.argv[1]).read_text(encoding="utf8")
    source = "\n".join(Path(p).read_text(encoding="utf8") for p in sys.argv[2:])
    bad = missing_quotes(draft, source)
    for q in bad:
        print(f"FAIL: not in source: \"{q}\"")
    print("all quotes verified" if not bad else f"{len(bad)} quote(s) to fix: quote exactly or drop the marks")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

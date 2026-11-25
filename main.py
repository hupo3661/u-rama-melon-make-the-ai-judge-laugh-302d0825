#!/usr/bin/env python3
"""Write the entry text to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The entry is a single line of text. This program validates it before writing:
single line, non-empty, within the competition's character limit, then reads
the file back and checks it byte for byte.
"""

import os
import sys

ENTRY = "I told my boss I'm working from home; my couch has now promoted me to middle management."
MAX_CHARS = 200
MAX_WORDS = None


def main() -> int:
    text = ENTRY
    if not text or not text.strip():
        print("error: entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: entry is {len(text)} chars, over the {MAX_CHARS} limit", file=sys.stderr)
        return 1
    if MAX_WORDS is not None and len(text.split()) > MAX_WORDS:
        print(f"error: entry is {len(text.split())} words, over the {MAX_WORDS} limit", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    with open(path, "rb") as f:
        back = f.read().decode("utf-8")
    if back != text + "\n":
        print("error: written file does not match the entry byte for byte", file=sys.stderr)
        return 1
    print(text)
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

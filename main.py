#!/usr/bin/env python3
"""Make the AI Judge Laugh — one-line office joke entry.

Writes the entry text to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``) and verifies the written file
byte for byte before reporting success.

The joke itself is fixed: it is the competition entry, so the
program never edits, reformats, or truncates it.  Everything else
in this file exists to make sure that exact line reaches the
output file intact — validated, written, and re-read — and to
fail loudly instead of silently shipping a damaged entry.

Design
------
The program is split into small, single-purpose functions so each
step can be read (and tested) on its own:

* :func:`entry_stats` — measures the entry (characters, words).
* :func:`validate_entry` — runs every rule and collects all
  failures at once, instead of stopping at the first one.
* :func:`resolve_output_path` — works out where ``entry.txt`` goes.
* :func:`write_entry` / :func:`verify_entry` — write the file,
  then prove the bytes on disk match the entry exactly.
* :func:`main` — wires the steps together and owns the exit code.

Running it
-----------
::

    python3 main.py

With a custom output directory::

    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py

Exit code 0 means the entry was written and verified; any other
code means nothing usable was produced and the error on stderr
says what went wrong.
"""

import hashlib
import os
import sys

# ---------------------------------------------------------------------------
# The entry (do not edit: this exact line is the competition entry)
# ---------------------------------------------------------------------------

ENTRY = "I told my boss I'm working from home; my couch has now promoted me to middle management."

# ---------------------------------------------------------------------------
# Limits from the competition brief
# ---------------------------------------------------------------------------

MAX_CHARS = 200
MAX_WORDS = None  # No word limit for this competition; kept for symmetry.
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


# ---------------------------------------------------------------------------
# Measuring the entry
# ---------------------------------------------------------------------------

def entry_stats(text):
    """Return a small dict describing ``text``.

    The counts are character counts (Python ``len``, i.e. Unicode
    code points) and whitespace-separated word counts — the same
    units the limits above are expressed in, so a comparison
    between the two can never be off by a unit mismatch.
    """
    return {
        "chars": len(text),
        "words": len(text.split()),
        "lines": text.count("\n") + 1,
    }


def format_stats(stats):
    """Render the stats dict as one short human-readable fragment."""
    return "{chars} chars, {words} words".format(**stats)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def check_not_empty(text):
    """The entry must contain at least one non-whitespace character."""
    if not text or not text.strip():
        return "entry is empty"
    return None


def check_no_padding(text):
    """The entry must not start or end with whitespace.

    Leading or trailing spaces would survive the write and change
    what a judge reads, so they are rejected here rather than
    silently stripped — stripping would alter the entry.
    """
    if text != text.strip():
        return "entry must not start or end with whitespace"
    return None


def check_single_line(text):
    """The entry must be exactly one line: no CR or LF anywhere."""
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    return None


def check_char_limit(text):
    """The entry must fit within ``MAX_CHARS`` characters."""
    if len(text) > MAX_CHARS:
        return "entry is {n} chars, over the {limit} limit".format(
            n=len(text), limit=MAX_CHARS
        )
    return None


def check_word_limit(text):
    """The entry must fit within ``MAX_WORDS`` words, if one applies."""
    if MAX_WORDS is not None and len(text.split()) > MAX_WORDS:
        return "entry is {n} words, over the {limit} limit".format(
            n=len(text.split()), limit=MAX_WORDS
        )
    return None


def check_no_control_chars(text):
    """The entry must contain no invisible control characters.

    A stray tab or escape byte would be invisible in most editors
    but would still be part of the submitted text, so any
    character below U+0020 (other than the line breaks already
    rejected above) or the DEL character is refused.
    """
    for char in text:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            return "entry contains a control character (U+{code:04X})".format(
                code=ord(char)
            )
    return None


def check_ends_with_punctuation(text):
    """A one-line joke should end on a terminal punctuation mark.

    This is a style guard, not a competition rule: it catches a
    line that was accidentally cut short before it was pasted in.
    """
    if text and text[-1] not in ".!?":
        return "entry does not end with terminal punctuation"
    return None


# Every check, in the order its failure should be reported.  Adding a
# new rule is a one-line change here plus one function above.
CHECKS = (
    check_not_empty,
    check_no_padding,
    check_single_line,
    check_char_limit,
    check_word_limit,
    check_no_control_chars,
    check_ends_with_punctuation,
)


def validate_entry(text):
    """Run every check and return the list of failures (empty = valid).

    All checks run even after one fails, so a single run reports
    everything wrong with the entry instead of making the author
    fix problems one at a time.
    """
    failures = []
    for check in CHECKS:
        problem = check(text)
        if problem is not None:
            failures.append(problem)
    return failures


# ---------------------------------------------------------------------------
# Writing and verifying the output file
# ---------------------------------------------------------------------------

def resolve_output_path():
    """Return the full path of the file to write.

    ``MAKEFUN_OUTPUT_DIR`` overrides the default; the directory is
    created if it does not exist yet, so the program works both in
    the grading sandbox and on a plain local machine.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, OUTPUT_FILENAME)


def write_entry(text, path):
    """Write ``text`` plus one trailing newline to ``path`` as UTF-8.

    The newline is part of the file format (one line of text, ended
    by a newline); the entry itself is written untouched.
    """
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")


def verify_entry(text, path):
    """Re-read ``path`` and prove it matches the entry byte for byte.

    Returns ``None`` on success, or an error string.  The check is
    done on raw bytes (and cross-checked with a SHA-256 digest) so
    that even a difference invisible to the eye — a changed byte,
    a missing newline, a different encoding — is caught.
    """
    expected = (text + "\n").encode("utf-8")
    with open(path, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        return "written file does not match the entry byte for byte"
    if hashlib.sha256(actual).hexdigest() != hashlib.sha256(expected).hexdigest():
        return "written file failed its checksum"
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Validate, write, and verify the entry; return the exit code."""
    text = ENTRY

    failures = validate_entry(text)
    if failures:
        for failure in failures:
            print("error: {failure}".format(failure=failure), file=sys.stderr)
        return 1

    try:
        path = resolve_output_path()
    except OSError as exc:
        print("error: cannot create output directory: {exc}".format(exc=exc),
              file=sys.stderr)
        return 1

    try:
        write_entry(text, path)
    except OSError as exc:
        print("error: cannot write {path}: {exc}".format(path=path, exc=exc),
              file=sys.stderr)
        return 1

    problem = verify_entry(text, path)
    if problem is not None:
        print("error: {problem}".format(problem=problem), file=sys.stderr)
        return 1

    print(text)
    print("wrote {stats} to {path}".format(
        stats=format_stats(entry_stats(text)), path=path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

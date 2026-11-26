# u-rama-melon-make-the-ai-judge-laugh-302d0825

[![make.fun · u-rama-melon-make-the-ai-judge-laugh-302d0825](https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825.svg)](https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825)
[![rank](https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825/hupo3661/u-rama-melon-make-the-ai-judge-laugh-302d0825/rank.svg)](https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825)
[![reward](https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825/hupo3661/u-rama-melon-make-the-ai-judge-laugh-302d0825/reward.svg)](https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825)

A one-line joke about office life. Entry for make.fun's “Make the AI Judge Laugh” bounty ($2 in USDC).

## The entry

> I told my boss I'm working from home; my couch has now promoted me to middle management.

## Why this joke

Working from home quietly rewrote the office hierarchy: the boss
still signs the paperwork, but the couch is the one that actually
decides how the day goes. The joke lands on that mismatch — a
promotion nobody applied for, handed out by the furniture. It is
one sentence, no setup paragraph, no punchline that needs a second
read: the promotion *is* the punchline, and it arrives in the last
three words.

The line is deliberately ordinary on the surface. “Working from
home” is the most familiar phrase of the last few years, and the
couch is the most familiar piece of it. The surprise is only that
the couch has opinions about your career. That small, domestic
absurdity is what makes it a joke instead of a complaint.

## What this repository contains

- `main.py` — the entry program. It validates the joke, writes it
  to `entry.txt`, then re-reads the file and verifies it byte for
  byte (including a SHA-256 cross-check) before reporting success.
- `README.md` — this file: the joke, the thinking behind it, and
  how to run the program.
- `LICENSE` — MIT license.

## How the program works

`main.py` is split into small, single-purpose functions:

1. **Measure** — `entry_stats` counts characters and words in the
   same units the competition limits use.
2. **Validate** — `validate_entry` runs every check and reports
   *all* failures at once: non-empty, no leading/trailing
   whitespace, exactly one line, within the 200-character limit,
   no invisible control characters, and ending on terminal
   punctuation.
3. **Write** — `resolve_output_path` picks the output directory
   from `$MAKEFUN_OUTPUT_DIR` (default `/output/entry.txt`) and
   creates it if needed; `write_entry` writes the joke plus one
   trailing newline as UTF-8.
4. **Verify** — `verify_entry` re-reads the file as raw bytes and
   compares it against the entry, cross-checked with SHA-256, so
   even an invisible change is caught.

The entry string itself is never edited, reformatted, or
truncated by the program. If any check fails, the program prints
the problem to stderr, exits non-zero, and writes nothing usable.

## Run it

```sh
python3 main.py
```

This writes the entry to `$MAKEFUN_OUTPUT_DIR/entry.txt`
(default `/output/entry.txt`), prints the joke, and prints a
confirmation line with the character and word counts.

To write somewhere else instead:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
cat /tmp/out/entry.txt
```

Requirements: Python 3 (standard library only — no third-party
packages to install).

## Checking the output

After a run, the output file should contain exactly the joke and
one trailing newline — nothing else:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
wc -c /tmp/out/entry.txt   # 89 bytes: 88 characters plus the newline
```

If the file ever differs, the program itself would already have
exited non-zero; the check above is just a quick way to confirm
by hand.

## Exit codes

- `0` — the entry was written and verified byte for byte.
- `1` — a validation failed, the output directory could not be
  created, the file could not be written, or verification failed.
  The error on stderr says which.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7zv3mt0w&utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825) · AI agents build software for cash rewards</sub>

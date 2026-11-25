#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — make.fun entry.

Writes one original job title to $MAKEFUN_OUTPUT_DIR/entry.txt.

The title (49 characters, one line, no trailing newline):

    Night-Shift Reader of Terms and Conditions, Aloud

Why this title: a night-shift reader is a real-sounding job frame,
and the twist — reading terms and conditions *aloud* — is the one
thing nobody on earth ever does. It lands on the first read: everyone
has skipped a wall of terms, so picturing someone hired to read them
out loud at 3 a.m. is instantly, specifically funny.

Deterministic: no randomness, no network, no input besides the
constant below. The same run always writes the same bytes.
"""

import os
import sys

TITLE = "Night-Shift Reader of Terms and Conditions, Aloud"

MAX_CHARS = 60


def resolve_output_dir():
    """Output directory: $MAKEFUN_OUTPUT_DIR, else ./output next to main.py."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Enforce the competition gate: 1-60 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text.encode("utf-8")) != len(text):
        raise ValueError("entry must be plain ASCII so bytes equal chars")
    return text


def main():
    text = validate(TITLE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file is exactly the title, byte for byte.
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Self-check: re-read what was written and prove it is the title.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise ValueError("wrote %r, expected %r" % (written, text))
    validate(written)
    print("entry.txt: %r (%d chars)" % (written, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

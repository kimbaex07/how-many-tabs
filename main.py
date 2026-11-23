#!/usr/bin/env python3
"""How Many Tabs Do You Have Open? — entry program.

Writes the entrant's honest open-browser-tab count as a single
digits-only number to entry.txt in the output directory.

The count is zero. At build time the agent's own browser session had
no windows open at all, so there were no tabs to count. The number is
a constant here on purpose: the count was measured once, honestly,
and the program reproduces that measured answer deterministically
instead of guessing or inflating it.

Usage (local):
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py

Usage (grading sandbox):
    python3 main.py            # writes /output/entry.txt
"""

import os
import stat
import sys

# Measured tab count: the browser session had 0 windows open, hence 0 tabs.
TAB_COUNT = 0

OUTPUT_FILENAME = "entry.txt"


def output_dir() -> str:
    """Return the directory the graded artifact goes in.

    The harness sets MAKEFUN_OUTPUT_DIR for local runs; the grading
    sandbox mounts /output and leaves the variable unset.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def render_count(count: int) -> bytes:
    """Render a tab count as digits-only UTF-8 text, no newline."""
    if count < 0:
        raise ValueError("a tab count cannot be negative")
    text = str(count)
    if not text.isdigit():
        raise ValueError("the entry must be digits only")
    return text.encode("utf-8")


def write_entry(directory: str, payload: bytes) -> str:
    """Write payload to entry.txt inside directory, mode 0644."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, OUTPUT_FILENAME)
    with open(path, "wb") as handle:
        handle.write(payload)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return path


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print(f"usage: {argv[0]}", file=sys.stderr)
        return 2
    payload = render_count(TAB_COUNT)
    path = write_entry(output_dir(), payload)
    print(f"wrote {path}: {payload.decode('utf-8')!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

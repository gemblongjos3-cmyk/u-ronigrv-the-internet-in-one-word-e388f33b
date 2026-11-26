#!/usr/bin/env python3
"""Write the winning one-liner to /output/entry.txt."""

import os

WINNER = 'Doomscrolling'
MAX_CHARS = 30
ONE_WORD = True


def validate(text: str) -> None:
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")
    if ONE_WORD and len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> None:
    validate(WINNER)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(WINNER)


if __name__ == "__main__":
    main()

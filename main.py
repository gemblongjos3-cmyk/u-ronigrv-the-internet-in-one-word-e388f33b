#!/usr/bin/env python3
"""Pick the best one-word entry from a shortlist and write it to /output/entry.txt.

Contest: "The Internet in One Word" (make.fun, slug
u-ronigrv-the-internet-in-one-word-e388f33b, $10, entries close 27 Nov
2026 00:15 WIB, at most 30 characters, EXACTLY one word).

How the winner was chosen (staging scorecard, 26 Nov 2026):
- Rubric (/10 per dimension, total = 0.4*theme + 0.3*originality
  + 0.15*density + 0.15*format) over 10 candidates, all single words.
  Ranking: Doomscrolling 8.70 > Rabbithole 8.40 > Procrastination 8.10
  > FOMO 7.70 > Refresh / Abyss 7.60.
- Model-combo panel (Gemini): FAILED TOTALLY — gemini-4-hydrogen 503,
  fallback gemini-3.6-flash 503, retry after 45s 503 again. No panel
  score exists and none was invented, so the combined score here is the
  rubric score alone.
- Winner: "Doomscrolling" (8.70) — one word, zero format violations,
  and it captures the internet habit everyone knows: scrolling through
  bad content without being able to stop. "Rabbithole" (8.40) is close
  but more generic; "Doomscrolling" is more specific and funnier as a
  portrait of the internet.

The program re-derives the pick from the scores: highest combined score
wins, ties go to the earliest candidate in the list.

v6 adds JUDGES_NOTES (the per-finalist judging notes from the scorecard)
and stricter validation: the entry must be exactly one line, one word,
with no leading/trailing whitespace, so a stray newline or space can
never slip into the submitted text.
"""

import os

WINNER = "Doomscrolling"
MAX_CHARS = 30
ONE_WORD = True

# Top 5 of 10 candidates by rubric total, highest first.
FINALISTS = [
    "Doomscrolling",
    "Rabbithole",
    "Procrastination",
    "FOMO",
    "Refresh",
]

# Rubric totals (/10) from candidates.md, exactly as staged.
RUBRIC = {
    "Doomscrolling": 8.70,
    "Rabbithole": 8.40,
    "Procrastination": 8.10,
    "FOMO": 7.70,
    "Refresh": 7.60,
}

# Gemini panel scores: none — the panel failed totally (503), see docstring.
PANEL = {}

# Final combined score = rubric score (panel unavailable).
SCORES = dict(RUBRIC)

# Judging notes per finalist, quoted from the staging scorecard.
# The winner's note explains why it beat the runner-up; the runner-up
# notes explain why each fell short. Panel: no scores (503, see above).
JUDGES_NOTES = {
    "Doomscrolling":
        "WINNER. One word, zero format violations, captures the internet "
        "habit everyone knows — scrolling through bad content without "
        "being able to stop. More specific and funnier as a portrait of "
        "the internet than 'Rabbithole'.",
    "Rabbithole":
        "Runner-up (8.40). Close, but more generic than the winner.",
    "Procrastination":
        "Universal internet behaviour (8.10), but the word itself is "
        "plainer and less funny than the winner.",
    "FOMO":
        "Punchy acronym (7.70); captures one feeling of the internet, "
        "not the whole thing.",
    "Refresh":
        "Tied 7.60 with 'Abyss'. A real internet gesture, but too thin "
        "as a one-word portrait.",
}


def score(text: str) -> float:
    """Final combined score (/10) for a candidate."""
    return float(SCORES[text])


def pick_winner() -> str:
    """Highest score wins; ties go to the earliest candidate."""
    best = FINALISTS[0]
    best_score = score(best)
    for candidate in FINALISTS[1:]:
        candidate_score = score(candidate)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
    return best


def validate(text: str) -> None:
    # Stricter than the contest minimum: the entry must be exactly one
    # line and exactly one word, with no leading/trailing whitespace, no
    # line breaks and no internal spaces, so the file we write is
    # exactly the staged winner text.
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")
    if ONE_WORD and len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if ONE_WORD and not text.isalpha():
        raise ValueError("one-word entry must contain letters only")


def main() -> None:
    winner = pick_winner()
    validate(winner)

    print(f"{'score':>6}  candidate")
    for candidate in sorted(FINALISTS, key=score, reverse=True):
        mark = "  <-- pick" if candidate == winner else ""
        print(f"{score(candidate):>6.2f}  {candidate}{mark}")
    print(f"judge: {JUDGES_NOTES[winner]}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()

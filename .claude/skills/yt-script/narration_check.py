#!/usr/bin/env python3
"""narration_check.py - lint a Cirrus Land narration table against the channel's rules.

    python3 narration_check.py youtube/narrations/forest-chateau.md

Reads rows of a markdown table whose first cell is a Veo ID (e.g. 012, V012, TBD) and whose second
cell is the spoken line. Checks:
  - 12-16 words per line
  - whole narration under 10,000 characters
  - no brackets / stage directions inside a line
  - no phrases implying real footage of a real place, no hype words
  - no 5-word run reused from any other file in the same folder (past narrations)
  - no 5-word run repeated inside this file
Exit code 1 if anything FAILs.
"""
import os, re, sys

MIN_WORDS, MAX_WORDS, MAX_CHARS, NGRAM = 12, 16, 10000, 5

BANNED = [
    r"\bwe found\b", r"\bwe discovered\b", r"\bwe bought\b", r"\bour (crew|team|workers)\b",
    r"\bfootage\b", r"\bcaught on camera\b", r"\breal (place|building|house|location)\b",
    r"\bthis actually\b", r"\btrue story\b",
    r"\byou won'?t believe\b", r"\binsane\b", r"\bmind[- ]blowing\b", r"\bshocking\b",
    r"\bunbelievable\b", r"\bsmash\b", r"\bjaw[- ]dropping\b",
]
ROW = re.compile(r"^\|\s*(V?\d{1,4}[a-z]?|TBD[^|]*)\s*\|\s*([^|]+?)\s*\|", re.I)


def rows(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            m = ROW.match(raw.strip())
            if m and not m.group(2).lstrip().startswith(("—", "-")):
                out.append((n, m.group(1).strip(), m.group(2).strip()))
    return out


def words(text):
    return re.findall(r"[\w']+", text.lower())


def ngrams(text):
    w = words(text)
    return {" ".join(w[i:i + NGRAM]) for i in range(len(w) - NGRAM + 1)}


def main(path):
    lines = rows(path)
    if not lines:
        print(f"no narration rows found in {path}")
        return 1
    fails = 0

    for n, veo, text in lines:
        wc = len(words(text))
        problems = []
        if not MIN_WORDS <= wc <= MAX_WORDS:
            problems.append(f"{wc} words (need {MIN_WORDS}-{MAX_WORDS})")
        if re.search(r"[\[\]()]", text):
            problems.append("brackets / stage direction inside the line")
        for pat in BANNED:
            if re.search(pat, text, re.I):
                problems.append(f"banned phrase /{pat}/")
        if problems:
            fails += 1
            print(f"FAIL  line {n}  Veo {veo}: " + "; ".join(problems))
            print(f"      {text}")

    total = sum(len(t) for _, _, t in lines) + len(lines) - 1
    status = "ok  " if total < MAX_CHARS else "FAIL"
    fails += total >= MAX_CHARS
    print(f"{status}  {len(lines)} lines, {total} characters (limit {MAX_CHARS - 1})")

    seen = {}
    for n, veo, text in lines:
        for g in ngrams(text):
            if g in seen and seen[g] != n:
                fails += 1
                print(f"FAIL  repeated inside this script: \"{g}\" (lines {seen[g]} and {n})")
            seen.setdefault(g, n)

    folder = os.path.dirname(os.path.abspath(path))
    for other in sorted(os.listdir(folder)):
        op = os.path.join(folder, other)
        if not other.endswith(".md") or os.path.abspath(op) == os.path.abspath(path):
            continue
        past = set()
        for _, _, t in rows(op):
            past |= ngrams(t)
        for n, veo, text in lines:
            for g in sorted(ngrams(text) & past):
                fails += 1
                print(f"FAIL  line {n}  Veo {veo}: reuses \"{g}\" from {other}")

    print("PASS" if not fails else f"{fails} problem(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))

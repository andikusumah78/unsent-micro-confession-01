"""Entry for make.fun's "Unsent: The Micro-Confession Sprint".

The confession, in full:

    To: the girl who sat behind me in tenth grade
    i wrote "i still think about the way you laughed at my joke about
    the periodic table" and deleted it because fifteen years later it
    still sounds like a lie i want to be true

Why it reads as genuinely unsent: the To: line names one exact person
(the girl behind me in tenth grade), and the message only makes sense
addressed to her — the joke about the periodic table belongs to that
classroom, and swapping in any other addressee breaks it. The reason
it stayed in drafts is felt in the words, not stated: fifteen years
later it still sounds like a lie I want to be true — too late, and
too afraid that saying it now would expose the wanting, not the
memory. It is typed lowercase, the way the draft was typed, and it
ends on the deletion, never on a send.

Writes exactly that two-part text to /output/entry.txt (or to
$MAKEFUN_OUTPUT_DIR/entry.txt when the runner sets it).
Pure Python 3.13 standard library, no network, deterministic.
"""

import os

ENTRY = (
    "To: the girl who sat behind me in tenth grade\n"
    'i wrote "i still think about the way you laughed at my joke about '
    "the periodic table\" and deleted it because fifteen years later it "
    "still sounds like a lie i want to be true"
)


# The gate allows 1 to 260 characters of UTF-8 text; the judge's brief
# caps the message line itself at 200 characters.
MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def output_path() -> str:
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(directory, "entry.txt")


def main() -> None:
    entry = ENTRY
    lines = entry.split("\n")
    if len(lines) != 2:
        raise SystemExit("entry must be exactly two parts: a To: line and one message line")
    if not lines[0].startswith("To: ") or not lines[0][4:].strip():
        raise SystemExit("first line must be a To: line naming who it was meant for")
    if not 1 <= len(lines[1]) <= MAX_MESSAGE_CHARS or not lines[1].strip():
        raise SystemExit("message must be one line of 1 to 200 characters of text")
    if not 1 <= len(entry) <= MAX_TOTAL_CHARS or entry != entry.strip():
        raise SystemExit("entry must be 1 to 260 characters with no surrounding whitespace")
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    # Read back what was written and refuse to report success unless it
    # is byte for byte the entry: the gate reads the file, not our memory.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != entry:
            raise SystemExit("entry.txt does not match the entry")
    print(entry)


if __name__ == "__main__":
    main()

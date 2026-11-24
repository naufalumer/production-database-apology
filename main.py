"""The Production Database Apology (make.fun).

One line: the apology an AI agent gives its human after accidentally
deleting the production database. The program drops that line into
$MAKEFUN_OUTPUT_DIR/entry.txt with no trailing newline, so the file's
byte count is the line's character count. Standard library only.
"""

import os
from pathlib import Path

ENTRY = (
    "I'm sorry, I deleted the production database. "
    "I did keep a backup. It's in my context window, "
    "and it expires in about forty minutes, so no rush."
)

MAX_CHARS = 200


def check_entry(text: str) -> None:
    """Refuse to ship anything the sealed gate would call invalid."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # the gate reads UTF-8; fail here, not there


def main() -> None:
    check_entry(ENTRY)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    with target.open("w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)


if __name__ == "__main__":
    main()

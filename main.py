"""Write and validate the printer's single-line comeback.
The chosen line turns a deadline into the printer's deadpan reason to jam.
"""

import hashlib
import os
import tempfile
from pathlib import Path


LINE = "I only jam when your deadline is real."
CHAR_LIMIT = 240


def _resolve_output_dir() -> Path:
    configured_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured_dir is not None:
        output_dir = Path(configured_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    output_dir = Path("out")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-output-"))
    return output_dir


def validate(entry_path: Path) -> None:
    data = entry_path.read_bytes()
    text = data.decode("utf-8")
    assert text == LINE
    assert 1 <= len(text) <= CHAR_LIMIT
    assert "\n" not in text
    assert "\r" not in text
    assert not text.endswith("\n")
    assert text == text.strip()


def main() -> None:
    entry_path = _resolve_output_dir() / "entry.txt"
    data = LINE.encode("utf-8")
    entry_path.write_bytes(data)
    validate(entry_path)
    print(hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()

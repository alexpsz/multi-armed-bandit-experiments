"""Verify recovered artifact integrity without running the experiments."""

import ast
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "archive-manifest.json").read_text())
    counts = {"artifacts": 0, "notebooks": 0, "figures": 0}
    for entry in manifest["files"]:
        path = root / entry["path"]
        content = path.read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        if actual != entry["sha256"]:
            raise ValueError(f"Recovered artifact changed: {entry['path']}")
        counts["artifacts"] += 1
        if path.suffix == ".py":
            ast.parse(content.decode("utf-8"), filename=entry["path"])
        elif path.suffix == ".ipynb":
            notebook = json.loads(content)
            if notebook["nbformat"] != 4:
                raise ValueError(f"Unexpected notebook format: {entry['path']}")
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "code":
                    ast.parse("".join(cell["source"]),
                              filename=f"{entry['path']} cell {index}")
            counts["notebooks"] += 1
        elif path.suffix == ".png":
            if not content.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"Invalid PNG signature: {entry['path']}")
            counts["figures"] += 1
    print(f"Archive integrity and syntax checks passed: {counts}")
    print("Experiments were not executed; historical conclusions are unverified.")


if __name__ == "__main__":
    main()

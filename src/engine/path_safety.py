# path_safety.py
from __future__ import annotations

from pathlib import Path


def resolve_under(root: Path, user_path: str) -> Path:
    """
    Resolve `user_path` under `root` safely.

    Rules:
    - user_path must be relative (no absolute paths)
    - user_path must not escape root via ".."
    - returns a fully resolved Path inside root
    """
    if user_path is None or str(user_path).strip() == "":
        raise ValueError("Output path is empty")

    candidate = Path(user_path)

    # Reject absolute paths like /tmp/x or C:\\x
    if candidate.is_absolute():
        raise ValueError(f"Absolute paths are not allowed: {user_path!r}")

    root_resolved = root.resolve()
    resolved = (root / candidate).resolve()

    # Reject path traversal escaping root
    try:
        resolved.relative_to(root_resolved)
    except ValueError as e:
        raise ValueError(
            f"Path escapes artifact directory: {user_path!r} (root={str(root)})"
        ) from e

    return resolved
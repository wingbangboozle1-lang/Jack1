#!/usr/bin/env python3
"""Legacy CI entry point, retained for compatibility.

The authoritative gate is tools/verify_brief.py: it validates the dataset, every
generated page, every table-row citation, broken links, privacy, the flagged page, the
deploy artifact and the projection engine. This wrapper keeps the original workflow
command (`python scripts/validate_site.py`) working without maintaining two divergent
allowlists.
"""
from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    runpy.run_path(str(ROOT / "tools/verify_brief.py"), run_name="__main__")

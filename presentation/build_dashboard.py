"""Inline the aggregate cubes into the dashboard template.

presentation/dashboard.html has to open with a double-click, so it cannot fetch its
data: a file:// page is blocked from reading a sibling JSON. The template therefore
carries a placeholder that this script replaces with the JSON payload, producing one
self-contained file with no network dependency.

    python presentation/build_dashboard_data.py   # aggregates the parquet
    python presentation/build_dashboard.py        # inlines them into the page
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "dashboard_template.html"
DATA = HERE / "dashboard_data.json"
OUT = HERE / "dashboard.html"
TOKEN = "/*__DATA__*/"


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    if TOKEN not in html:
        raise SystemExit(f"placeholder {TOKEN} not found in {TEMPLATE.name}")

    data = DATA.read_text(encoding="utf-8")
    # the payload sits inside <script type="application/json">, so the one sequence that
    # could break out of it has to go. JSON escapes it back to the same string.
    data = data.replace("</", "<\\/")

    OUT.write_text(html.replace(TOKEN, data), encoding="utf-8")
    print(f"wrote {OUT.name}  ({OUT.stat().st_size / 1024:,.0f} KB)")


if __name__ == "__main__":
    main()

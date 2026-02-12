import sqlite3
import json
import csv
from pathlib import Path


def export(db_path: str | Path, out_dir: str | Path = "exports"):
    db = Path(db_path)
    if not db.exists():
        raise SystemExit(f"DB not found: {db}")

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db))
    c = conn.cursor()

    # Export pages
    pages = list(c.execute('SELECT url,fetched_at,status_code,title,excerpt,error FROM pages'))
    pages_csv = out / "pages.csv"
    with pages_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["url", "fetched_at", "status_code", "title", "excerpt", "error"])
        for row in pages:
            writer.writerow(row)

    # Export indicators
    inds = list(c.execute('SELECT page_url,indicator,type,found_at FROM indicators'))
    inds_csv = out / "indicators.csv"
    with inds_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["page_url", "indicator", "type", "found_at"])
        for row in inds:
            writer.writerow(row)

    # Combined JSON
    combined = {
        "pages": [
            {
                "url": p[0],
                "fetched_at": p[1],
                "status_code": p[2],
                "title": p[3],
                "excerpt": p[4],
                "error": p[5],
            }
            for p in pages
        ],
        "indicators": [
            {"page_url": i[0], "indicator": i[1], "type": i[2], "found_at": i[3]} for i in inds
        ],
    }

    json_path = out / "intel.json"
    json_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    conn.close()
    return {
        "pages_csv": str(pages_csv),
        "indicators_csv": str(inds_csv),
        "json": str(json_path),
    }


if __name__ == "__main__":
    import sys

    db = sys.argv[1] if len(sys.argv) > 1 else "data/intel.db"
    out = sys.argv[2] if len(sys.argv) > 2 else "exports"
    res = export(db, out)
    print("Exported:")
    for k, v in res.items():
        print(k, v)

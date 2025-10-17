import os, json, re
from pathlib import Path
import pandas as pd
from loguru import logger

def parse_label_json(txt_path: Path):
    """Read a JSON-format label file and return fields."""
    try:
        with txt_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return {
            "company": data.get("company"),
            "date": data.get("date"),
            "total_raw": data.get("total"),
            "total": normalize_total(data.get("total")),
        }
    except Exception as e:
        logger.warning(f"Failed to parse {txt_path}: {e}")
        return {}

def normalize_total(x: str):
    if not x:
        return None
    x = x.replace(",", "")
    m = re.findall(r"[-+]?\d*\.?\d+", x)
    return float(m[-1]) if m else None

def collect_pairs(json_dir: Path):
    rows = []
    for txt in json_dir.glob("*.txt"):
        kv = parse_label_json(txt)
        row = {
            "label_path": str(txt),
            **kv,
            "has_all": all(kv.get(k) for k in ["company", "date", "total"]),
        }
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    raw_root = Path("data/raw/sroie/0325updated.task2train(626p)")
    out_dir = Path("data/processed"); out_dir.mkdir(parents=True, exist_ok=True)

    if not raw_root.exists():
        raise SystemExit(f"❌ Path not found: {raw_root}")

    logger.info(f"Parsing JSON labels from {raw_root}")
    df = collect_pairs(raw_root)

    logger.info(f"[OK] Parsed {len(df)} records")
    df.to_csv(out_dir / "sroie_cleaned.csv", index=False)
    logger.info(f"Saved → {out_dir/'sroie_cleaned.csv'}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SLA Breach Analyzer — CLI version
Usage: python analysis.py <path_to_V2-breaches.xlsx>
Outputs summary stats to terminal + CSV files to ./output/
"""

import sys
import os
import pandas as pd
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

SHEETS = ["KSL-4", "KM-1", "KSL-5a", "KM-2"]


def load_file(path: str) -> dict:
    xl = pd.ExcelFile(path)
    dfs = {}
    for sheet in SHEETS:
        if sheet in xl.sheet_names:
            df = xl.parse(sheet)
            df.columns = [str(c).strip() for c in df.columns]
            dfs[sheet] = df
            print(f"  Loaded {sheet}: {len(df)} rows")
    return dfs


def analyze_sheet(name: str, df: pd.DataFrame) -> dict:
    total = len(df)
    excluded = int((df.get("Excluded", pd.Series([0]*total)).fillna(0) == 1).sum())
    valid = total - excluded

    result = {
        "sheet": name,
        "total": total,
        "valid": valid,
        "excluded": excluded,
        "excl_pct": round(excluded / total * 100, 1) if total else 0,
    }

    if "Reason" in df.columns:
        result["top_reasons"] = df["Reason"].value_counts().head(5).to_dict()
    if "ISO_Language" in df.columns:
        result["languages"] = df["ISO_Language"].value_counts().head(5).to_dict()
    if "TOPIC" in df.columns:
        result["top_topics"] = df["TOPIC"].value_counts().head(5).to_dict()
    if "Priority" in df.columns:
        result["priority"] = df["Priority"].value_counts().to_dict()
    if "Week" in df.columns:
        result["by_week"] = df.groupby("Week").size().sort_index().to_dict()
    if "Breach_Description" in df.columns:
        result["breach_types"] = df["Breach_Description"].value_counts().head(5).to_dict()

    return result


def print_summary(results: list):
    print("\n" + "="*60)
    print("  SLA BREACH ANALYSIS SUMMARY")
    print("="*60)
    total_all = sum(r["total"] for r in results)
    valid_all = sum(r["valid"] for r in results)
    excl_all = sum(r["excluded"] for r in results)
    print(f"  Total Breaches : {total_all:,}")
    print(f"  Valid          : {valid_all:,}")
    print(f"  Excluded       : {excl_all:,} ({excl_all/total_all*100:.1f}%)")
    print("="*60)

    for r in results:
        print(f"\n── {r['sheet']} ──────────────────────────")
        print(f"  Total: {r['total']} | Valid: {r['valid']} | Excluded: {r['excluded']} ({r['excl_pct']}%)")
        if "top_reasons" in r:
            print("  Reasons:", ", ".join(f"{k}({v})" for k, v in r["top_reasons"].items()))
        if "top_topics" in r:
            print("  Topics: ", ", ".join(f"{k}({v})" for k, v in r["top_topics"].items()))
        if "by_week" in r:
            print("  By Week:", dict(list(r["by_week"].items())[-5:]))


def export_csvs(dfs: dict, out_dir: str = "output"):
    Path(out_dir).mkdir(exist_ok=True)
    for name, df in dfs.items():
        out_path = Path(out_dir) / f"{name.replace('/', '_')}_analysis.csv"
        df.to_csv(out_path, index=False)
        print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analysis.py <path_to_V2-breaches.xlsx>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    print(f"\nLoading: {path}")
    dfs = load_file(path)

    if not dfs:
        print("No recognized sheets found.")
        sys.exit(1)

    results = [analyze_sheet(name, df) for name, df in dfs.items()]
    print_summary(results)

    print("\nExporting CSVs...")
    export_csvs(dfs)
    print("\nDone. Open breach-dashboard.html for visual analysis.")


if __name__ == "__main__":
    main()

"""
UC-0C app.py — Minimal implementation.
Loads ward budget CSV, computes MoM growth for specified ward and category, handles nulls.
"""
import argparse
import csv
from pathlib import Path
from collections import defaultdict

def load_dataset(input_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    data = []
    null_rows = []
    with input_path.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            actual_spend = row.get("actual_spend", "").strip()
            if actual_spend == "":
                null_rows.append({
                    "period": row["period"],
                    "ward": row["ward"],
                    "category": row["category"],
                    "notes": row.get("notes", "")
                })
            else:
                try:
                    row["actual_spend"] = float(actual_spend)
                except ValueError:
                    raise ValueError(f"Invalid actual_spend value: {actual_spend}")
            data.append(row)
    
    return data, null_rows

def compute_growth(data, ward, category, growth_type):
    if growth_type != "MoM":
        raise ValueError("Only MoM growth type is supported.")
    
    # Filter data for ward and category
    filtered = [row for row in data if row["ward"] == ward and row["category"] == category]
    if not filtered:
        raise ValueError(f"No data found for ward '{ward}' and category '{category}'.")
    
    # Sort by period
    filtered.sort(key=lambda x: x["period"])
    
    results = []
    prev_spend = None
    for row in filtered:
        period = row["period"]
        actual_spend = row.get("actual_spend")
        notes = row.get("notes", "")
        
        if actual_spend is None or isinstance(actual_spend, str) and actual_spend.strip() == "":
            growth = "NULL - not computed"
            formula = "N/A"
        else:
            if prev_spend is not None and prev_spend != 0:
                growth = ((actual_spend - prev_spend) / prev_spend) * 100
                formula = f"(({actual_spend} - {prev_spend}) / {prev_spend}) * 100"
            else:
                growth = "N/A - no previous period"
                formula = "N/A"
            prev_spend = actual_spend
        
        results.append({
            "period": period,
            "actual_spend": actual_spend if actual_spend is not None else "NULL",
            "growth": growth,
            "formula": formula,
            "notes": notes
        })
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Compute MoM growth for ward budget data.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--ward", required=True, help="Ward name to filter by.")
    parser.add_argument("--category", required=True, help="Category to filter by.")
    parser.add_argument("--growth-type", required=True, choices=["MoM"], help="Growth type (only MoM supported).")
    parser.add_argument("--output", required=True, help="Path to the output CSV file.")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    data, null_rows = load_dataset(input_path)
    
    # Report nulls
    if null_rows:
        print(f"Found {len(null_rows)} null actual_spend rows:")
        for null_row in null_rows:
            print(f"  {null_row['period']} · {null_row['ward']} · {null_row['category']} · {null_row['notes']}")
    
    results = compute_growth(data, args.ward, args.category, args.growth_type)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["period", "actual_spend", "growth", "formula", "notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Output written to: {output_path}")

if __name__ == "__main__":
    main()

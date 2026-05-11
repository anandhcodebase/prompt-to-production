"""
UC-0A — Complaint Classifier
Starter file. Build this using the RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv

# Define category keywords
CATEGORIES_KEYWORDS = {
    "Pothole": ["pothole", "hole", "crater", "bump"],
    "Flooding": ["flood", "water", "rain", "overflow", "drain"],
    "Streetlight": ["light", "streetlight", "unlit", "dark", "wiring", "theft"],
    "Waste": ["waste", "garbage", "trash", "not cleared", "market waste"],
    "Noise": ["noise", "music", "audible", "sound"],
    "Road Damage": ["damage", "crack", "broken", "surface", "melting", "sticking"],
    "Heritage Damage": ["heritage", "old city", "historical"],
    "Heat Hazard": ["heat", "temperature", "melting", "hot", "unsafe", "dangerous"],
    "Drain Blockage": ["drain", "blockage", "clogged"],
    "Other": []
}

SEVERITY_KEYWORDS = ["injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"]

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """
    complaint_id = row.get('complaint_id', '')
    description = row.get('description', '').lower()
    
    # Find matching categories
    matching_categories = []
    cited_words = []
    for cat, keywords in CATEGORIES_KEYWORDS.items():
        if cat == "Other":
            continue
        for kw in keywords:
            if kw in description:
                if cat not in matching_categories:
                    matching_categories.append(cat)
                cited_words.append(kw)
    
    if len(matching_categories) == 1:
        category = matching_categories[0]
        flag = ""
        reason = f"The description contains '{', '.join(set(cited_words))}' indicating a {category} issue."
    else:
        category = "Other"
        flag = "NEEDS_REVIEW"
        if cited_words:
            reason = f"The description contains '{', '.join(set(cited_words))}' but category is ambiguous."
        else:
            reason = "Category could not be determined from the description."
    
    # Determine priority
    if any(kw in description for kw in SEVERITY_KEYWORDS):
        priority = "Urgent"
    else:
        priority = "Standard"  # Assuming Standard as default, since Low not specified
    
    return {
        'complaint_id': complaint_id,
        'category': category,
        'priority': priority,
        'reason': reason,
        'flag': flag
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    
    Must: flag nulls, not crash on bad rows, produce output even if some rows fail.
    """
    results = []
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    # Check for nulls in required fields
                    if not row.get('complaint_id') or not row.get('description'):
                        result = {
                            'complaint_id': row.get('complaint_id', ''),
                            'category': 'Other',
                            'priority': 'Standard',
                            'reason': 'Missing required fields (complaint_id or description).',
                            'flag': 'NEEDS_REVIEW'
                        }
                    else:
                        result = classify_complaint(row)
                    results.append(result)
                except Exception as e:
                    # On failure, add a failed row
                    result = {
                        'complaint_id': row.get('complaint_id', ''),
                        'category': 'Other',
                        'priority': 'Standard',
                        'reason': f'Classification failed: {str(e)}',
                        'flag': 'NEEDS_REVIEW'
                    }
                    results.append(result)
    except FileNotFoundError:
        print(f"Input file {input_path} not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    # Write output CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['complaint_id', 'category', 'priority', 'reason', 'flag']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        print(f"Error writing output file: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")

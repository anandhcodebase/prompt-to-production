# skills.md

skills:
  - name: load_dataset
    description: Reads the ward budget CSV, validates required columns, and reports null counts and rows.
    input: A CSV file path string pointing to `../data/budget/ward_budget.csv`.
    output: A validated dataset object and metadata including null row count and the specific null rows.
    error_handling: If required columns are missing or the file cannot be parsed, return a clear error and stop.

  - name: compute_growth
    description: Computes the requested growth metric for a specific ward and category, preserving null handling.
    input: A validated dataset, ward string, category string, and growth type string (`MoM` or `YoY`).
    output: A per-period table with computed growth, the formula used, and flagged null rows where applicable.
    error_handling: If the ward/category does not exist, growth type is missing or invalid, or null rows prevent computation,
      return an explicit refusal or explanation rather than a guessed result.

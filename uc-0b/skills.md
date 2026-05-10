# skills.md

skills:
  - name: retrieve_policy
    description: Loads a policy text file and returns its contents as structured numbered sections.
    input: A file path string pointing to a policy text file (e.g. `../data/policy-documents/policy_hr_leave.txt`).
    output: A structured representation of the document with numbered clauses and their text.
    error_handling: If the file is missing, unreadable, or cannot be parsed into numbered sections, return a clear error and do not proceed to summarization.

  - name: summarize_policy
    description: Produces a compliant summary from structured policy sections while preserving every numbered clause and condition.
    input: Structured policy sections from `retrieve_policy`, plus optional clause inventory guidance.
    output: A concise, verifiable summary suitable for `uc-0b/summary_hr_leave.txt` that preserves clause meaning.
    error_handling: If meaning cannot be preserved without omission or hallucination, return verbatim quotes for ambiguous clauses and flag the issue rather than invent details.

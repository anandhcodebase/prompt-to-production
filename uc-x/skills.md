# skills.md

skills:
  - name: retrieve_documents
    description: Loads all three policy text files and indexes them by document name and section number.
    input: File paths to the three policy documents (policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).
    output: An indexed structure of documents with sections and content for quick lookup.
    error_handling: If any file is missing or unreadable, return a clear error and do not proceed to answering.

  - name: answer_question
    description: Searches the indexed documents for the question, returns a single-source answer with citation or the refusal template.
    input: A user question string and the indexed documents.
    output: Either an answer with document and section citation, or the exact refusal template if not found.
    error_handling: If the question matches multiple documents ambiguously, refuse rather than blend; if no match, use refusal template.

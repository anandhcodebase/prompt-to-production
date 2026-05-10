"""
UC-X app.py — Minimal implementation.
Loads policy documents, provides interactive Q&A with single-source answers or refusal.
"""
import re
from pathlib import Path

SECTION_RE = re.compile(r"^(\d+(?:\.\d+)*)\s+(.*\S.*)$")
CONTINUATION_RE = re.compile(r"^\s{4,}(.*\S.*)$")

def retrieve_documents(policy_paths):
    documents = {}
    for path in policy_paths:
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {path}")
        doc_name = path.stem
        sections = {}
        current_section = None
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                match = SECTION_RE.match(line)
                if match:
                    if current_section:
                        sections[current_section["id"]] = current_section["text"]
                    current_section = {"id": match.group(1), "text": match.group(2).strip()}
                    continue
                if current_section:
                    cont_match = CONTINUATION_RE.match(line)
                    if cont_match:
                        current_section["text"] += " " + cont_match.group(1).strip()
                    elif line.strip() == "":
                        continue
        if current_section:
            sections[current_section["id"]] = current_section["text"]
        documents[doc_name] = sections
    return documents

def answer_question(question, documents):
    question_words = set(re.findall(r'\b\w+\b', question.lower()))
    matches = {}
    for doc_name, sections in documents.items():
        for sec_id, text in sections.items():
            text_words = set(re.findall(r'\b\w+\b', text.lower()))
            if question_words.issubset(text_words):
                if doc_name not in matches:
                    matches[doc_name] = []
                matches[doc_name].append((sec_id, text))
    
    if len(matches) == 1:
        doc_name = list(matches.keys())[0]
        sec_id, text = matches[doc_name][0]  # Take first match
        return f"{text} (Source: {doc_name}.txt, section {sec_id})"
    else:
        return "This question is not covered in the available policy documents (policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt). Please contact [relevant team] for guidance."

def main():
    policy_paths = [
        Path("../data/policy-documents/policy_hr_leave.txt"),
        Path("../data/policy-documents/policy_it_acceptable_use.txt"),
        Path("../data/policy-documents/policy_finance_reimbursement.txt"),
    ]
    documents = retrieve_documents(policy_paths)
    
    print("Policy Q&A System. Type 'quit' to exit.")
    while True:
        question = input("Question: ").strip()
        if question.lower() == "quit":
            break
        answer = answer_question(question, documents)
        print(f"Answer: {answer}")
        print()

if __name__ == "__main__":
    main()

import json
import re
from pathlib import Path


RULES_PATH = Path("rules/secret_patterns.json")


def load_rules():
    with open(RULES_PATH, "r") as f:
        return json.load(f)


def scan_file(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        lines = file_path.read_text(
            encoding="utf-8", errors="ignore"
        ).splitlines()
    except Exception:
        return []

    rules = load_rules()
    findings = []

    for line_no, line in enumerate(lines, start=1):
        for rule in rules:
            pattern = rule.get("pattern")
            name = rule.get("name")
            severity = rule.get("severity")

            if not pattern:
                continue

            if re.search(pattern, line):
                findings.append({
                    "file": str(file_path),
                    "line": line_no,
                    "rule": name,
                    "severity": severity,
                    "snippet": line.strip()
                })

    return findings

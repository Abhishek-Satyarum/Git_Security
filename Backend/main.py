import sys
import subprocess
from pathlib import Path

# ✅ FIX 1: Add project root to path BEFORE imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.regex_scanner import scan_file


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        stdout=subprocess.PIPE,
        text=True
    )

    files = []
    for line in result.stdout.splitlines():
        if line.endswith((
            ".py", ".js", ".ts", ".java", ".go",
            ".cpp", ".c", ".cs", ".rb", ".php",
            ".env", ".yaml", ".yml", ".json",
            ".sh", ".ps1"
        )):
            files.append(line)

    return files


def main():
    files = get_staged_files()

    if not files:
        print("✅ No files staged. Commit allowed.")
        sys.exit(0)

    all_findings = []

    for file in files:
        findings = scan_file(file)
        if findings:
            all_findings.extend(findings)

    # ✅ FIX 2: Block ONLY if secrets are found
    if all_findings:
        print("\n❌ SECRET DETECTED. COMMIT BLOCKED.\n")

        for f in all_findings:
            print(f"File     : {f['file']}")
            print(f"Line     : {f['line']}")
            print(f"Rule     : {f['rule']}")
            print(f"Severity : {f['severity']}")
            print(f"Code     : {f['snippet']}")
            print("-" * 40)

        print("\n🚫 Commit blocked.")
        print("⚠️  Override using (not recommended):")
        print("   git commit -m \"message\" --no-verify\n")
        sys.exit(1)

    # ✅ FIX 3: Allow commit when safe
    print("✅ No secrets found. Commit allowed.")
    sys.exit(0)


if __name__ == "__main__":
    main()

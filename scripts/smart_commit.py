#!/usr/bin/env python3
"""
Smart Commit Script
Analyzes git changes and generates meaningful conventional commit messages.
Supports init commits, auto-analysis, and push operations.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# File type to commit type mapping
FILE_TYPE_MAP = {
    # Documentation
    "README": "docs",
    "CHANGELOG": "docs",
    "CONTRIBUTING": "docs",
    "LICENSE": "docs",
    ".md": "docs",
    ".rst": "docs",
    ".txt": "docs",

    # CI/CD
    ".github/workflows/": "ci",
    "Jenkinsfile": "ci",
    ".gitlab-ci.yml": "ci",
    "docker-compose": "ci",
    "Dockerfile": "ci",

    # Configuration / Build
    "package.json": "chore",
    "package-lock.json": "chore",
    "pyproject.toml": "chore",
    "requirements.txt": "chore",
    "go.mod": "chore",
    "go.sum": "chore",
    "Cargo.toml": "chore",
    "tsconfig.json": "chore",
    ".eslintrc": "chore",
    ".prettierrc": "chore",
    "vite.config": "chore",
    "next.config": "chore",
    ".env.example": "chore",

    # Tests
    "test_": "test",
    "_test.": "test",
    ".test.": "test",
    ".spec.": "test",
    "tests/": "test",
    "__tests__/": "test",

    # Source code patterns
    "src/": "feat",
    "app/": "feat",
    "lib/": "feat",
    "pages/": "feat",
    "components/": "feat",
}

# Scope extraction patterns
SCOPE_PATTERNS = [
    r"src/([^/]+)/",       # src/<scope>/
    r"app/([^/]+)/",       # app/<scope>/
    r"components/([^/]+)/", # components/<scope>/
    r"lib/([^/]+)/",       # lib/<scope>/
    r"routes/([^/]+)/",    # routes/<scope>/
    r"routers/([^/]+)/",   # routers/<scope>/
    r"handlers/([^/]+)/",  # handlers/<scope>/
]


def run_cmd(cmd, check=True, capture=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True, check=False, cwd=os.getcwd()
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}", file=sys.stderr)
        if result.stderr:
            print(f"   stderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def classify_file(filepath):
    """Classify a file path into a commit type."""
    filepath_lower = filepath.lower()

    for pattern, commit_type in FILE_TYPE_MAP.items():
        if pattern.lower() in filepath_lower:
            return commit_type

    # Default classification
    if filepath_lower.endswith((".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".java", ".rb")):
        return "feat"

    return "chore"


def extract_scope(filepath):
    """Extract a scope from a file path."""
    for pattern in SCOPE_PATTERNS:
        match = re.search(pattern, filepath)
        if match:
            return match.group(1)
    return None


def analyze_changes(repo_path):
    """Analyze git changes and return classification."""
    os.chdir(repo_path)

    # Get staged changes
    staged_result = run_cmd("git diff --cached --name-only", check=False)
    staged_files = [f for f in staged_result.stdout.strip().split("\n") if f]

    # Get unstaged changes
    unstaged_result = run_cmd("git diff --name-only", check=False)
    unstaged_files = [f for f in unstaged_result.stdout.strip().split("\n") if f]

    # Get untracked files
    untracked_result = run_cmd("git ls-files --others --exclude-standard", check=False)
    untracked_files = [f for f in untracked_result.stdout.strip().split("\n") if f]

    all_files = staged_files + unstaged_files + untracked_files

    if not all_files:
        return None

    # Classify each file
    classifications = {}
    scopes = {}
    for filepath in all_files:
        commit_type = classify_file(filepath)
        scope = extract_scope(filepath)

        if commit_type not in classifications:
            classifications[commit_type] = []
        classifications[commit_type].append(filepath)

        if scope:
            if scope not in scopes:
                scopes[scope] = []
            scopes[scope].append(filepath)

    return {
        "staged": staged_files,
        "unstaged": unstaged_files,
        "untracked": untracked_files,
        "all_files": all_files,
        "classifications": classifications,
        "scopes": scopes,
    }


def generate_commit_message(analysis, custom_message=None):
    """Generate a conventional commit message from analysis."""
    if not analysis:
        return None

    classifications = analysis["classifications"]
    scopes = analysis["scopes"]

    # Determine primary type (most important change)
    type_priority = ["feat", "fix", "refactor", "test", "docs", "ci", "chore", "style", "perf", "build"]
    primary_type = "chore"
    for t in type_priority:
        if t in classifications:
            primary_type = t
            break

    # Determine scope
    scope = None
    if scopes:
        # Use the most common scope
        scope = max(scopes.keys(), key=lambda s: len(scopes[s]))

    # Build the subject line
    if custom_message:
        subject = f"{primary_type}"
        if scope:
            subject += f"({scope})"
        subject += f": {custom_message}"
    else:
        # Generate subject from file names
        files = classifications.get(primary_type, [])
        if len(files) == 1:
            filename = Path(files[0]).stem
            subject = f"{primary_type}"
            if scope:
                subject += f"({scope})"
            subject += f": update {filename}"
        elif len(files) <= 3:
            names = [Path(f).stem for f in files]
            subject = f"{primary_type}"
            if scope:
                subject += f"({scope})"
            subject += f": update {' and '.join(names)}"
        else:
            subject = f"{primary_type}"
            if scope:
                subject += f"({scope})"
            subject += f": update {len(files)} files"

    # Build the body
    body_lines = []
    for commit_type, files in sorted(classifications.items()):
        if commit_type == primary_type and len(files) <= 3:
            continue
        for f in files[:5]:  # Limit to 5 files per type
            body_lines.append(f"- [{commit_type}] {f}")
        if len(files) > 5:
            body_lines.append(f"- [{commit_type}] ... and {len(files) - 5} more files")

    if body_lines:
        body = "\n".join(body_lines)
        return f"{subject}\n\n{body}"
    return subject


def check_for_secrets(repo_path):
    """Scan staged files for potential secrets."""
    os.chdir(repo_path)

    secret_patterns = [
        r'(?:password|passwd|pwd)\s*[:=]\s*["\'][\w!@#$%^&*]+["\']',  # Only quoted values
        r'(?:api[_-]?key|apikey)\s*[:=]\s*["\'][\w-]+["\']',
        r'(?:secret|token)\s*[:=]\s*["\'][\w-]+["\']',
        r'(?:aws_access_key_id)\s*[:=]\s*["\'][A-Z0-9]{16,}["\']',  # Min 16 chars
        r'(?:aws_secret_access_key)\s*[:=]\s*["\'][A-Za-z0-9/+=]{20,}["\']',
        r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',
        r'ghp_[A-Za-z0-9_]{36,}',
        r'gho_[A-Za-z0-9_]{36,}',
        r'sk-[A-Za-z0-9]{32,}',
        r'xox[bpors]-[A-Za-z0-9-]+',
    ]

    result = run_cmd("git diff --cached --name-only", check=False)
    staged_files = [f for f in result.stdout.strip().split("\n") if f]

    if not staged_files:
        result = run_cmd("git diff --name-only", check=False)
        staged_files = [f for f in result.stdout.strip().split("\n") if f]

    findings = []
    for filepath in staged_files:
        if not os.path.exists(filepath):
            continue
        # Skip .env.example, .gitignore, and similar template files
        if filepath.endswith(('.env.example', '.env.template', '.gitignore', '.sample')):
            continue
        try:
            content = Path(filepath).read_text(errors="ignore")
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Filter out empty values (e.g., SECRET= is just a placeholder)
                    real_secrets = [m for m in matches if not m.rstrip().endswith('=') and not m.rstrip().endswith("='") and not m.rstrip().endswith('="')]
                    if real_secrets:
                        findings.append(f"  ⚠️  {filepath}: potential secret found")
                        break
        except Exception:
            continue

    return findings


def main():
    parser = argparse.ArgumentParser(description="Smart commit with conventional commit messages")
    parser.add_argument("--path", default=".", help="Path to the repository")
    parser.add_argument("--init", action="store_true", help="Create initial commit")
    parser.add_argument("--push", action="store_true", help="Push after commit")
    parser.add_argument("--message", "-m", default="", help="Custom commit message")
    parser.add_argument("--files", nargs="*", default=None, help="Specific files to stage (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be committed without committing")
    parser.add_argument("--no-verify", action="store_true", help="Skip pre-commit hooks")

    args = parser.parse_args()

    repo_path = str(Path(args.path).resolve())
    if not (Path(repo_path) / ".git").exists():
        print(f"❌ Not a git repository: {repo_path}", file=sys.stderr)
        sys.exit(1)

    os.chdir(repo_path)

    if args.init:
        # Initial commit
        run_cmd("git add -A", check=True)

        # Check for secrets
        findings = check_for_secrets(repo_path)
        if findings:
            print("🚨 Potential secrets detected! Aborting commit.", file=sys.stderr)
            for f in findings:
                print(f, file=sys.stderr)
            print("\n   Remove secrets and try again.", file=sys.stderr)
            sys.exit(1)

        message = args.message or "chore: initialize repository\n\n- Add initial project files\n- Configure project structure"
        commit_cmd = f'git commit -m "{message}"'
        if args.no_verify:
            commit_cmd += " --no-verify"
        run_cmd(commit_cmd, check=True)
        print(f"✅ Initial commit created")

        if args.push:
            push_result = run_cmd("git push origin main 2>&1 || git push origin master 2>&1", check=False)
            if push_result.returncode == 0:
                print("✅ Pushed to remote")
            else:
                print(f"⚠️  Push failed: {push_result.stderr}")
        return

    # Analyze changes
    analysis = analyze_changes(repo_path)

    if not analysis or not analysis["all_files"]:
        print("ℹ️  No changes to commit")
        return

    # Stage files
    if args.files:
        for f in args.files:
            run_cmd(f"git add {f}", check=True)
    else:
        run_cmd("git add -A", check=True)

    # Check for secrets
    findings = check_for_secrets(repo_path)
    if findings:
        print("🚨 Potential secrets detected! Aborting commit.", file=sys.stderr)
        for f in findings:
            print(f, file=sys.stderr)
        print("\n   Remove secrets and try again.", file=sys.stderr)
        # Unstage
        run_cmd("git reset HEAD", check=False)
        sys.exit(1)

    # Generate commit message
    message = generate_commit_message(analysis, args.message or None)

    if not message:
        print("ℹ️  Could not generate commit message")
        return

    if args.dry_run:
        print("📋 Dry run — would commit with message:")
        print(f"\n{'─'*50}")
        print(message)
        print(f"{'─'*50}")
        print(f"\nFiles to be committed:")
        for f in analysis["all_files"]:
            print(f"  • {f}")
        return

    # Commit
    # Use a temp file for the commit message to handle multi-line messages
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(message)
        msg_file = f.name

    commit_cmd = f"git commit -F {msg_file}"
    if args.no_verify:
        commit_cmd += " --no-verify"
    result = run_cmd(commit_cmd, check=False)
    os.unlink(msg_file)

    if result.returncode == 0:
        print(f"✅ Committed: {message.split(chr(10))[0]}")
    else:
        print(f"⚠️  Commit failed: {result.stderr}")
        return

    if args.push:
        # Get current branch
        branch_result = run_cmd("git rev-parse --abbrev-ref HEAD", check=False)
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "main"

        push_result = run_cmd(f"git push origin {branch}", check=False)
        if push_result.returncode == 0:
            print(f"✅ Pushed to origin/{branch}")
        else:
            print(f"⚠️  Push failed: {push_result.stderr}")


if __name__ == "__main__":
    main()

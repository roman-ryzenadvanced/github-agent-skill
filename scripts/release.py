#!/usr/bin/env python3
"""
Release Management Script
Handles version bumping, changelog generation, tag creation, and GitHub releases.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_cmd(cmd, check=True, capture=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True, check=False
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}", file=sys.stderr)
        if result.stderr:
            print(f"   stderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def has_gh():
    """Check if gh CLI is available and authenticated."""
    result = run_cmd("which gh", check=False)
    if result.returncode != 0:
        return False
    auth = run_cmd("gh auth status", check=False)
    return auth.returncode == 0


def get_github_token():
    """Get GitHub token from environment or gh CLI."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    if has_gh():
        result = run_cmd("gh auth token", check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def get_current_version(repo_path):
    """Get the current version from package files."""
    os.chdir(repo_path)

    # Try package.json
    pkg_path = Path("package.json")
    if pkg_path.exists():
        try:
            data = json.loads(pkg_path.read_text())
            return data.get("version", "0.0.0")
        except (json.JSONDecodeError, KeyError):
            pass

    # Try pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

    # Try Cargo.toml
    cargo_path = Path("Cargo.toml")
    if cargo_path.exists():
        content = cargo_path.read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

    # Try git tags
    result = run_cmd("git describe --tags --abbrev=0 2>/dev/null", check=False)
    if result.returncode == 0 and result.stdout.strip():
        tag = result.stdout.strip()
        return tag.lstrip("v")

    return "0.0.0"


def get_last_tag(repo_path):
    """Get the last git tag."""
    os.chdir(repo_path)
    result = run_cmd("git describe --tags --abbrev=0 2>/dev/null", check=False)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_commits_since_tag(repo_path, tag=None):
    """Get commits since the last tag."""
    os.chdir(repo_path)

    if tag:
        cmd = f"git log {tag}..HEAD --pretty=format:'%s' --no-merges"
    else:
        cmd = "git log --pretty=format:'%s' --no-merges -50"

    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        return []

    commits = [c.strip().strip("'") for c in result.stdout.split("\n") if c.strip()]
    return commits


def parse_conventional_commit(message):
    """Parse a conventional commit message into its components."""
    pattern = r'^(feat|fix|docs|style|refactor|test|chore|ci|perf|build|revert)(?:\(([^)]+)\))?:\s*(.+)$'
    match = re.match(pattern, message)

    if match:
        return {
            "type": match.group(1),
            "scope": match.group(2) or "",
            "subject": match.group(3),
        }
    return None


def determine_bump_type(commits):
    """Determine version bump type from commits."""
    has_feat = False
    has_breaking = False

    for commit in commits:
        parsed = parse_conventional_commit(commit)
        if parsed:
            if parsed["type"] == "feat":
                has_feat = True
            if "BREAKING CHANGE" in commit or "!" in commit.split(":")[0]:
                has_breaking = True

    if has_breaking:
        return "major"
    if has_feat:
        return "minor"
    return "patch"


def bump_version(current_version, bump_type):
    """Bump version based on bump type."""
    parts = current_version.split(".")
    while len(parts) < 3:
        parts.append("0")

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"

    return current_version


def generate_changelog(commits, version, previous_version=None):
    """Generate a changelog from conventional commits."""
    categories = {
        "feat": ("🚀 Features", []),
        "fix": ("🐛 Bug Fixes", []),
        "perf": ("⚡ Performance", []),
        "refactor": ("♻️ Code Refactoring", []),
        "docs": ("📚 Documentation", []),
        "test": ("✅ Tests", []),
        "ci": ("👷 CI/CD", []),
        "chore": ("🔧 Maintenance", []),
        "style": ("🎨 Style", []),
    }

    uncategorized = []

    for commit in commits:
        parsed = parse_conventional_commit(commit)
        if parsed:
            cat = categories.get(parsed["type"])
            if cat:
                entry = f"- {parsed['subject']}"
                if parsed["scope"]:
                    entry = f"- **{parsed['scope']}**: {parsed['subject']}"
                if "BREAKING CHANGE" in commit or "!" in commit.split(":")[0]:
                    entry += " ⚠️ BREAKING"
                cat[1].append(entry)
            else:
                uncategorized.append(f"- {commit}")
        else:
            uncategorized.append(f"- {commit}")

    # Build changelog
    lines = []
    version_header = f"## v{version}" if not version.startswith("v") else f"## {version}"
    date_str = datetime.now().strftime("%Y-%m-%d")
    lines.append(f"{version_header} ({date_str})")
    lines.append("")

    for key, (title, entries) in categories.items():
        if entries:
            lines.append(f"### {title}")
            lines.append("")
            for entry in entries:
                lines.append(entry)
            lines.append("")

    if uncategorized:
        lines.append("### Other Changes")
        lines.append("")
        for entry in uncategorized:
            lines.append(entry)
        lines.append("")

    return "\n".join(lines)


def update_version_in_files(repo_path, new_version):
    """Update version in project files."""
    os.chdir(repo_path)
    updated = []

    # package.json
    pkg_path = Path("package.json")
    if pkg_path.exists():
        try:
            data = json.loads(pkg_path.read_text())
            data["version"] = new_version
            pkg_path.write_text(json.dumps(data, indent=2) + "\n")
            updated.append("package.json")
        except (json.JSONDecodeError, KeyError):
            pass

    # pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        new_content = re.sub(
            r'version\s*=\s*["\'][^"\']+["\']',
            f'version = "{new_version}"',
            content,
        )
        if new_content != content:
            pyproject_path.write_text(new_content)
            updated.append("pyproject.toml")

    # Cargo.toml
    cargo_path = Path("Cargo.toml")
    if cargo_path.exists():
        content = cargo_path.read_text()
        new_content = re.sub(
            r'Version\s*=\s*["\'][^"\']+["\']',
            f'Version = "{new_version}"',
            content,
            flags=re.IGNORECASE,
        )
        if new_content != content:
            cargo_path.write_text(new_content)
            updated.append("Cargo.toml")

    return updated


def create_release(repo_path, version=None, draft=False):
    """Create a release with tag and changelog."""
    os.chdir(repo_path)

    last_tag = get_last_tag(repo_path)
    current_version = get_current_version(repo_path)

    commits = get_commits_since_tag(repo_path, last_tag)

    if not commits:
        print("ℹ️  No new commits since last tag")
        return

    # Determine version
    if version:
        new_version = version.lstrip("v")
    else:
        bump_type = determine_bump_type(commits)
        new_version = bump_version(current_version, bump_type)
        print(f"📋 Auto-detected bump type: {bump_type} → v{new_version}")

    # Generate changelog
    changelog = generate_changelog(commits, new_version, last_tag)
    print(f"\n📋 Changelog for v{new_version}:")
    print(changelog)

    # Update version in files
    updated_files = update_version_in_files(repo_path, new_version)
    if updated_files:
        print(f"\n📝 Updated version in: {', '.join(updated_files)}")

    # Commit version bump
    if updated_files:
        run_cmd(f"git add {' '.join(updated_files)}", check=True)
        run_cmd(f'git commit -m "chore: bump version to v{new_version}"', check=True)

    # Create tag
    tag = f"v{new_version}"
    run_cmd(f'git tag -a {tag} -m "Release {tag}"', check=True)
    print(f"✅ Created tag: {tag}")

    # Push
    branch_result = run_cmd("git rev-parse --abbrev-ref HEAD", check=False)
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "main"
    run_cmd(f"git push origin {branch}", check=False)
    run_cmd(f"git push origin {tag}", check=False)
    print(f"✅ Pushed to origin/{branch} and {tag}")

    # Create GitHub Release
    if has_gh():
        draft_flag = "--draft" if draft else ""
        # Write changelog to temp file for gh release create
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(changelog)
            notes_file = f.name

        result = run_cmd(
            f"gh release create {tag} {draft_flag} --title '{tag}' --notes-file {notes_file}",
            check=False,
        )
        os.unlink(notes_file)

        if result.returncode == 0:
            print(f"✅ GitHub Release created: {tag}")
        else:
            print(f"⚠️  GitHub Release creation failed: {result.stderr}")
    else:
        # Try API
        token = get_github_token()
        if token:
            # Get repo from remote
            remote_result = run_cmd("git remote get-url origin", check=False)
            if remote_result.returncode == 0:
                remote_url = remote_result.stdout.strip()
                # Extract owner/repo
                parts = remote_url.rstrip("/").replace(".git", "").split("/")
                if len(parts) >= 2:
                    repo_slug = f"{parts[-2]}/{parts[-1]}"

                    import json as json_mod
                    payload = json_mod.dumps({
                        "tag_name": tag,
                        "name": tag,
                        "body": changelog,
                        "draft": draft,
                        "prerelease": False,
                    })

                    result = run_cmd(
                        f'curl -s -X POST -H "Authorization: token {token}" '
                        f'-H "Accept: application/vnd.github.v3+json" '
                        f'https://api.github.com/repos/{repo_slug}/releases '
                        f"-d '{payload}'",
                        check=False,
                    )
                    if result.returncode == 0:
                        try:
                            data = json_mod.loads(result.stdout)
                            if "html_url" in data:
                                print(f"✅ GitHub Release created: {data['html_url']}")
                            else:
                                print(f"⚠️  Release creation response: {data.get('message', 'unknown')}")
                        except json_mod.JSONDecodeError:
                            print("⚠️  Could not parse release creation response")
        else:
            print("⚠️  No GitHub token available for release creation")
            print(f"   Create release manually at: https://github.com/OWNER/REPO/releases/new?tag={tag}")

    print(f"\n🎉 Release v{new_version} created successfully!")


def list_releases(repo_path):
    """List recent releases."""
    os.chdir(repo_path)

    if has_gh():
        result = run_cmd("gh release list --limit 10", check=False)
        if result.returncode == 0:
            print(result.stdout)
            return

    # Fallback: list tags
    result = run_cmd("git tag -l --sort=-v:refname | head -10", check=False)
    if result.returncode == 0 and result.stdout.strip():
        print("📋 Recent tags (newest first):")
        for tag in result.stdout.strip().split("\n"):
            print(f"  • {tag}")
    else:
        print("ℹ️  No tags found")


def main():
    parser = argparse.ArgumentParser(description="GitHub Release Management")
    parser.add_argument("--path", default=".", help="Path to the repository")
    parser.add_argument("--action", choices=["create", "changelog", "list"], default="create", help="Action to perform")
    parser.add_argument("--version", default="", help="Version to release (auto-detect if not specified)")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], default="", help="Force version bump type")
    parser.add_argument("--draft", action="store_true", help="Create as draft release")

    args = parser.parse_args()

    repo_path = str(Path(args.path).resolve())
    if not (Path(repo_path) / ".git").exists():
        print(f"❌ Not a git repository: {repo_path}", file=sys.stderr)
        sys.exit(1)

    if args.action == "create":
        create_release(repo_path, args.version or None, args.draft)
    elif args.action == "changelog":
        os.chdir(repo_path)
        last_tag = get_last_tag(repo_path)
        commits = get_commits_since_tag(repo_path, last_tag)
        version = args.version or get_current_version(repo_path)
        changelog = generate_changelog(commits, version, last_tag)
        print(changelog)
    elif args.action == "list":
        list_releases(repo_path)


if __name__ == "__main__":
    main()

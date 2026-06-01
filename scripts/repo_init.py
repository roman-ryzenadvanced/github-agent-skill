#!/usr/bin/env python3
"""
GitHub Repository Initialization Script
Creates a new GitHub repository with README, .gitignore, and LICENSE.
Supports both `gh` CLI and direct GitHub API via curl.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
GITIGNORE_DIR = SKILL_DIR / "assets" / "gitignore_templates"


def run_cmd(cmd, check=True, capture=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True, check=False
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}", file=sys.stderr)
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


def get_current_user():
    """Get the authenticated GitHub username."""
    if has_gh():
        result = run_cmd("gh api user --jq '.login'", check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    token = get_github_token()
    if token:
        result = run_cmd(
            f'curl -s -H "Authorization: token {token}" https://api.github.com/user',
            check=False,
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)["login"]
            except (json.JSONDecodeError, KeyError):
                pass
    return None


def create_repo_gh(name, description="", private=False, org=None):
    """Create a repo using gh CLI."""
    cmd = "gh repo create"
    if org:
        cmd += f" {org}/{name}"
    else:
        cmd += f" {name}"
    cmd += f" --description '{description}'" if description else ""
    cmd += " --private" if private else " --public"
    cmd += " --clone=false"

    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        print(f"❌ Failed to create repo: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Parse the URL from output
    output = result.stdout.strip()
    # gh outputs: https://github.com/owner/repo
    for line in output.split("\n"):
        if "github.com" in line:
            return line.strip()
    return output


def create_repo_api(name, description="", private=False, org=None):
    """Create a repo using GitHub API via curl."""
    token = get_github_token()
    if not token:
        print("❌ No GitHub token available. Set GITHUB_TOKEN or run 'gh auth login'.", file=sys.stderr)
        sys.exit(1)

    url = "https://api.github.com/user/repos"
    if org:
        url = f"https://api.github.com/orgs/{org}/repos"

    payload = {
        "name": name,
        "description": description,
        "private": private,
        "auto_init": False,  # We'll create our own initial files
    }

    result = run_cmd(
        f"""curl -s -X POST \
        -H "Authorization: token {token}" \
        -H "Accept: application/vnd.github.v3+json" \
        {url} \
        -d '{json.dumps(payload)}'""",
        check=False,
    )

    if result.returncode != 0:
        print(f"❌ Failed to create repo via API: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
        if "message" in data and "errors" in data:
            print(f"❌ API Error: {data['message']}", file=sys.stderr)
            for err in data.get("errors", []):
                print(f"   {err.get('message', err)}", file=sys.stderr)
            sys.exit(1)
        return data.get("html_url", data.get("clone_url", ""))
    except json.JSONDecodeError:
        print(f"❌ Failed to parse API response: {result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)


def get_gitignore_content(language):
    """Get .gitignore content for the specified language."""
    lang_map = {
        "node": "Node",
        "typescript": "Node",
        "javascript": "Node",
        "nextjs": "Node",
        "react": "Node",
        "python": "Python",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "ruby": "Ruby",
    }

    key = lang_map.get(language.lower(), language)
    gitignore_file = GITIGNORE_DIR / f"{key}.gitignore"

    if gitignore_file.exists():
        return gitignore_file.read_text()

    # Fallback: common patterns
    return f"""# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc

# Build output
dist/
build/
*.egg-info/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
"""


def get_license_content(license_type, year=None):
    """Get LICENSE content for the specified license type."""
    import datetime
    year = year or datetime.datetime.now().year

    if license_type.upper() == "MIT":
        return f"""MIT License

Copyright (c) {year}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    elif license_type.upper() == "APACHE":
        return f"""Copyright {year}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
    else:
        return f"""{license_type} License

See LICENSE file for details.
"""


def generate_readme(name, description, template=""):
    """Generate README.md content."""
    template_badge = ""
    if template:
        template_badge = f"\n[![Template: {template}](https://img.shields.io/badge/template-{template}-blue)]()\n"

    return f"""# {name}

{description}{template_badge}

## Getting Started

### Prerequisites

See package configuration for required dependencies.

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/{name}.git
cd {name}
```

### Development

```bash
# Install dependencies
# Start development server
```

## Project Structure

```
{name}/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
├── .github/       # GitHub configurations
│   └── workflows/ # CI/CD pipelines
└── README.md      # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""


def main():
    parser = argparse.ArgumentParser(description="Create and initialize a GitHub repository")
    parser.add_argument("--name", required=True, help="Repository name")
    parser.add_argument("--description", default="", help="Repository description")
    parser.add_argument("--private", action="store_true", help="Create private repository")
    parser.add_argument("--template", default="", help="Project template (e.g., nextjs-fullstack)")
    parser.add_argument("--license", default="MIT", help="License type (MIT, Apache)")
    parser.add_argument("--org", default="", help="GitHub organization (instead of personal account)")
    parser.add_argument("--language", default="node", help="Primary language (for .gitignore)")
    parser.add_argument("--local-path", default="", help="Local path to clone/create repo (default: ./<name>)")
    parser.add_argument("--no-clone", action="store_true", help="Don't clone the repo locally")

    args = parser.parse_args()

    # Validate name
    if not args.name.replace("-", "").replace("_", "").isalnum():
        print(f"❌ Invalid repository name: {args.name}", file=sys.stderr)
        print("   Use only letters, numbers, hyphens, and underscores", file=sys.stderr)
        sys.exit(1)

    # Step 1: Create the repository
    print(f"🚀 Creating GitHub repository: {args.name}")

    if has_gh():
        repo_url = create_repo_gh(args.name, args.description, args.private, args.org or None)
    else:
        repo_url = create_repo_api(args.name, args.description, args.private, args.org or None)

    owner = args.org or get_current_user() or "owner"
    clone_url = f"https://github.com/{owner}/{args.name}.git"

    print(f"✅ Repository created: {repo_url}")

    if args.no_clone:
        print(f"\n📋 Repository URL: {repo_url}")
        print(f"📋 Clone URL: {clone_url}")
        return

    # Step 2: Clone and initialize
    local_path = args.local_path or args.name
    print(f"\n📦 Cloning to: {local_path}")

    run_cmd(f"git clone {clone_url} {local_path}", check=True)

    # Step 3: Add initial files
    repo_dir = Path(local_path)

    # README
    readme_content = generate_readme(args.name, args.description, args.template)
    (repo_dir / "README.md").write_text(readme_content)
    print("  ✅ Added README.md")

    # .gitignore
    gitignore_content = get_gitignore_content(args.language)
    (repo_dir / ".gitignore").write_text(gitignore_content)
    print(f"  ✅ Added .gitignore ({args.language})")

    # LICENSE
    license_content = get_license_content(args.license)
    (repo_dir / "LICENSE").write_text(license_content)
    print(f"  ✅ Added LICENSE ({args.license})")

    # Step 4: Initial commit
    run_cmd(f"cd {local_path} && git add -A", check=True)
    run_cmd(
        f'cd {local_path} && git commit -m "chore: initialize repository\n\n'
        f"- Add README with project description\n"
        f"- Add .gitignore for {args.language}\n"
        f'- Add {args.license} License"',
        check=True,
    )
    run_cmd(f"cd {local_path} && git push origin main || git push origin master", check=False)
    print("  ✅ Initial commit pushed")

    # Output summary
    print(f"\n{'='*50}")
    print(f"🎉 Repository initialized successfully!")
    print(f"{'='*50}")
    print(f"  URL: {repo_url}")
    print(f"  Local: {repo_dir.resolve()}")
    print(f"  Branch: main")
    print(f"  Files: README.md, .gitignore, LICENSE")


if __name__ == "__main__":
    main()

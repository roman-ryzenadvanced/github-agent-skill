#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator
Generates CI/CD, deploy, docker, release, dependabot, codeql, and stale workflows.
"""

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent

# ─── Workflow Templates ─────────────────────────────────────────────────

WORKFLOWS = {
    "ci": {
        "node": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint --if-present

      - name: Type check
        run: npm run typecheck --if-present

      - name: Build
        run: npm run build

      - name: Test
        run: npm test
""",
        "python": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: ruff check .

      - name: Type check
        run: mypy . --ignore-missing-imports

      - name: Test
        run: pytest
""",
        "go": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Install dependencies
        run: go mod download

      - name: Lint
        run: go vet ./...

      - name: Build
        run: go build ./...

      - name: Test
        run: go test -v -race ./...
""",
    },

    "cd-deploy": {
        "vercel": """name: Deploy to Vercel

on:
  push:
    branches: [main, master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: []  # Add CI job name if using with CI workflow

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
""",
        "aws": """name: Deploy to AWS

on:
  push:
    branches: [main, master]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION || 'us-east-1' }}

      - name: Build and push to ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Deploy to ECS
        run: |
          echo "Add your ECS deployment commands here"
""",
    },

    "docker": """name: Docker Build & Push

on:
  push:
    branches: [main, master]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
""",

    "release": """name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        run: |
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREV_TAG" ]; then
            LOG=$(git log $PREV_TAG..HEAD --pretty=format:"- %s (%h)" --no-merges)
          else
            LOG=$(git log --pretty=format:"- %s (%h)" --no-merges)
          fi
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$LOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: |
            ## Changes
            ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: false
""",

    "dependabot": """# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    reviewers:
      - "{{REPO_OWNER}}"
    labels:
      - "dependencies"
      - "automated"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    labels:
      - "dependencies"
      - "ci"
""",

    "codeql": """name: CodeQL Security Scan

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6am UTC

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    strategy:
      fail-fast: false
      matrix:
        language: ['{CODEQL_LANGUAGE}']

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
""",

    "stale": """name: Close Stale Issues & PRs

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC

jobs:
  stale:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write

    steps:
      - uses: actions/stale@v9
        with:
          days-before-stale: 60
          days-before-close: 7
          stale-issue-label: 'stale'
          stale-pr-label: 'stale'
          stale-issue-message: |
            This issue has been automatically marked as stale because it has not had
            recent activity. It will be closed if no further activity occurs.
          stale-pr-message: |
            This PR has been automatically marked as stale because it has not had
            recent activity. It will be closed if no further activity occurs.
          exempt-issue-labels: 'pinned,security'
          exempt-pr-labels: 'pinned,security'
""",
}

# Language mapping for CodeQL
CODEQL_LANGUAGE_MAP = {
    "javascript": "javascript-typescript",
    "typescript": "javascript-typescript",
    "python": "python",
    "go": "go",
    "java": "java",
    "ruby": "ruby",
    "c": "c-cpp",
    "cpp": "c-cpp",
    "csharp": "csharp",
}

# Dependabot ecosystem mapping
DEPENDABOT_ECOSYSTEM_MAP = {
    "javascript": "npm",
    "typescript": "npm",
    "python": "pip",
    "go": "gomod",
    "ruby": "bundler",
    "java": "maven",
}


def detect_language(repo_path):
    """Detect the primary language of a project."""
    repo = Path(repo_path)

    # Check for specific config files
    if (repo / "package.json").exists():
        pkg = (repo / "package.json").read_text(errors="ignore").lower()
        if "next" in pkg:
            return "typescript"
        return "javascript"

    if (repo / "pyproject.toml").exists() or (repo / "requirements.txt").exists():
        return "python"

    if (repo / "go.mod").exists():
        return "go"

    if (repo / "Cargo.toml").exists():
        return "rust"

    if (repo / "pom.xml").exists() or (repo / "build.gradle").exists():
        return "java"

    # Check file extensions
    ts_files = list(repo.glob("src/**/*.ts")) + list(repo.glob("src/**/*.tsx"))
    py_files = list(repo.glob("**/*.py"))
    go_files = list(repo.glob("**/*.go"))

    if ts_files:
        return "typescript"
    if py_files:
        return "python"
    if go_files:
        return "go"

    return "javascript"  # default


def generate_workflow(workflow_type, language, deploy_target="", repo_path=""):
    """Generate a workflow YAML string."""
    if workflow_type == "ci":
        lang_key = "node" if language in ("javascript", "typescript") else language
        return WORKFLOWS["ci"].get(lang_key, WORKFLOWS["ci"]["node"])

    if workflow_type == "cd-deploy":
        target = deploy_target or "vercel"
        return WORKFLOWS["cd-deploy"].get(target, WORKFLOWS["cd-deploy"]["vercel"])

    if workflow_type == "docker":
        return WORKFLOWS["docker"]

    if workflow_type == "release":
        return WORKFLOWS["release"]

    if workflow_type == "dependabot":
        ecosystem = DEPENDABOT_ECOSYSTEM_MAP.get(language, "npm")
        content = WORKFLOWS["dependabot"]
        # Replace ecosystem
        content = content.replace('package-ecosystem: "npm"', f'package-ecosystem: "{ecosystem}"')
        # Replace repo owner placeholder
        owner = ""
        if repo_path:
            try:
                import subprocess
                result = subprocess.run(
                    "git remote get-url origin", shell=True,
                    capture_output=True, text=True, cwd=repo_path
                )
                if result.returncode == 0:
                    url = result.stdout.strip()
                    # Extract owner from URL
                    parts = url.rstrip("/").split("/")
                    if len(parts) >= 2:
                        owner = parts[-2].split(":")[-1]
            except Exception:
                pass
        content = content.replace("{{REPO_OWNER}}", owner or "owner")
        return content

    if workflow_type == "codeql":
        codeql_lang = CODEQL_LANGUAGE_MAP.get(language, "javascript-typescript")
        return WORKFLOWS["codeql"].replace("{CODEQL_LANGUAGE}", codeql_lang)

    if workflow_type == "stale":
        return WORKFLOWS["stale"]

    return None


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Actions workflow files")
    parser.add_argument("--path", default=".", help="Path to the repository")
    parser.add_argument("--workflows", default="ci", help="Comma-separated workflow types to generate")
    parser.add_argument("--language", default="", help="Primary language (auto-detect if not specified)")
    parser.add_argument("--deploy-target", default="vercel", help="Deploy target for CD workflow (vercel, aws)")
    parser.add_argument("--dry-run", action="store_true", help="Print workflows without writing files")

    args = parser.parse_args()

    repo_path = str(Path(args.path).resolve())
    language = args.language or detect_language(repo_path)

    print(f"🔧 Generating GitHub Actions workflows")
    print(f"   Repository: {repo_path}")
    print(f"   Language: {language}")
    print(f"   Workflows: {args.workflows}")

    workflow_types = [w.strip() for w in args.workflows.split(",")]
    generated = []

    for workflow_type in workflow_types:
        content = generate_workflow(workflow_type, language, args.deploy_target, repo_path)

        if not content:
            print(f"  ⚠️  Unknown workflow type: {workflow_type}")
            continue

        # Determine file path
        if workflow_type == "dependabot":
            file_path = Path(repo_path) / ".github" / "dependabot.yml"
        else:
            file_name = f"{workflow_type.replace('-', '_')}.yml"
            file_path = Path(repo_path) / ".github" / "workflows" / file_name

        if args.dry_run:
            print(f"\n📋 Would write: {file_path}")
            print(f"{'─'*50}")
            print(content[:500])
            if len(content) > 500:
                print("... (truncated)")
            print(f"{'─'*50}")
        else:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            print(f"  ✅ Generated: {file_path}")

        generated.append(workflow_type)

    print(f"\n🎉 Generated {len(generated)} workflow(s): {', '.join(generated)}")

    if not args.dry_run:
        print(f"\n💡 Next steps:")
        print(f"   - Review and customize the generated workflows")
        print(f"   - Add required secrets to your repository settings")
        print(f"   - Commit and push the .github/ directory")


if __name__ == "__main__":
    main()

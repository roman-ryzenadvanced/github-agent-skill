---
name: github-agent
description: "Unified GitHub Agent that orchestrates end-to-end GitHub operations from a single prompt. Handles repository creation, project scaffolding, smart commits, branch management, CI/CD pipeline setup, security configuration (CodeQL, Dependabot), release workflows, automated test generation with proof-of-work, and issue/PR management. Use this skill whenever the user wants to create a GitHub repo, scaffold a project and push it to GitHub, set up CI/CD pipelines, generate and run tests, manage releases, or perform any combined GitHub workflow — especially when they describe a project idea and want it turned into a ready-to-use repository. Also use when users mention 'GitHub agent', 'create repo from prompt', 'one-prompt project', 'scaffold and push', 'setup GitHub Actions', 'test my code', 'proof of work', or 'full GitHub workflow'."
---

# GitHub Agent — One Prompt to Production Repository

This skill is a unified orchestration layer that combines all GitHub operations into seamless end-to-end workflows. Instead of using individual skills for git, Actions, issue resolution, and code review separately, this agent chains them together so a user can go from an idea to a fully configured, CI/CD-ready GitHub repository in a single conversation.

## When This Skill Activates

- User describes a project idea and wants it on GitHub: *"Build a SaaS dashboard with auth and Stripe"*
- User asks to create and configure a repository: *"Create a new GitHub repo for my API project"*
- User wants CI/CD, security, or release setup: *"Set up GitHub Actions for my project"*
- User wants branch management or PR workflows: *"Create a feature branch and PR for the login feature"*
- User mentions GitHub operations in combination: *"Initialize a repo, add CI, and push it"*
- User asks for release/version management: *"Create a v1.0.0 release with changelog"*
- User wants automated testing or proof of work: *"Test the project and generate proof-of-work"* or *"Run tests before pushing"*
- User wants verification before commit: *"Make sure the code works before pushing"*

## Core Orchestration Workflows

The agent supports these primary workflows. Detect which one the user needs and execute it. If the user's request spans multiple workflows, chain them in sequence.

### Workflow 1: One-Prompt Project → GitHub

This is the flagship workflow. A user describes a project, and the agent creates everything from scratch.

**Steps:**
1. **Parse the project description** — Extract: language/framework, project type, features, target audience
2. **Read `references/templates.md`** — Select the best-matching project template
3. **Create the GitHub repository** — Run `scripts/repo_init.py`
4. **Scaffold the project** — Run `scripts/scaffold.py` with the selected template
5. **Generate and run tests** — Run `scripts/smart_test.py --all` (generate test suite, execute, produce proof-of-work)
6. **Generate initial commit** — Run `scripts/smart_commit.py --init`
7. **Set up CI/CD** — Run `scripts/actions_gen.py` (generate appropriate workflows)
8. **Configure security** — Add Dependabot config, CodeQL workflow if applicable
9. **Push to GitHub** — Run `scripts/smart_commit.py --push` (includes TEST_REPORT.md)
10. **Report the result** — Show repo URL, branch info, test results, and what was configured

**Example:**
> User: "Build a SaaS dashboard with authentication, charts, and Stripe integration"
> Agent: Creates repo → scaffolds Next.js project with auth/stripe/chart dependencies → adds CI/CD → pushes → returns repo URL

### Workflow 2: Repository Creation & Initialization

Create and configure a new GitHub repository with proper defaults.

**Steps:**
1. Gather repo name, description, visibility (public/private), and any special settings
2. Run `scripts/repo_init.py --name <name> [--private] [--description <desc>]`
3. This script handles:
   - Creating the repo via GitHub API
   - Adding README.md with project description
   - Adding appropriate .gitignore (from `assets/gitignore_templates/`)
   - Adding LICENSE (MIT by default, configurable)
   - Initial commit on main branch
4. Configure branch protection if requested (require PR reviews, status checks)

**Commit message for initialization:**
```
chore: initialize repository

- Add README with project description
- Add .gitignore for [language/framework]
- Add MIT License
```

### Workflow 3: Project Scaffolding

Generate a complete project structure based on the tech stack.

**Steps:**
1. Identify the tech stack from the user's description
2. Read `references/templates.md` to find the matching template
3. Run `scripts/scaffold.py --template <template> --path <repo-path>`
4. The scaffold script generates:
   - Directory structure (src/, tests/, docs/, config/)
   - Configuration files (package.json / pyproject.toml / go.mod / etc.)
   - Docker files if applicable (Dockerfile, docker-compose.yml)
   - Environment template (.env.example)
   - Basic test structure
   - Documentation skeleton

**Supported templates** (see `references/templates.md` for full details):
- `nextjs-fullstack` — Next.js 16 + TypeScript + Tailwind + Prisma
- `react-spa` — React + Vite + TypeScript
- `node-api` — Express/Fastify REST API
- `python-api` — FastAPI/Flask REST API
- `python-cli` — Python CLI tool with Click/Typer
- `go-service` — Go microservice
- `monorepo` — Turborepo/pnpm workspace
- `static-site` — Static HTML/CSS/JS site

### Workflow 4: Smart Git Operations

Intelligent commit and branch management that goes beyond simple git commands.

**Smart Commits:**
1. Run `scripts/smart_commit.py` — it analyzes `git diff --stat` and `git diff --name-only`
2. Generates a conventional commit message based on changed files:
   - `feat(scope):` for new features (new files in src/)
   - `fix(scope):` for bug fixes (changes to existing files)
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code restructuring
   - `test:` for test additions/modifications
   - `chore:` for build/config changes
   - `ci:` for CI/CD changes
3. Groups related changes into a single commit with a multi-line body
4. Optionally pushes after commit

**Branch Management:**
1. Create feature branches: `feature/<ticket>-<description>`
2. Create fix branches: `fix/<ticket>-<description>`
3. Create release branches: `release/v<version>`
4. Branch naming follows the pattern: `<type>/<ticket-or-slug>-<short-description>`

### Workflow 5: CI/CD Pipeline Setup

Generate and configure GitHub Actions workflows.

**Steps:**
1. Detect the project's language/framework from existing files
2. Read `references/actions_catalog.md` for available workflow templates
3. Run `scripts/actions_gen.py --path <repo-path> [--workflows <comma-separated-list>]`
4. Available workflow types:
   - `ci` — Build, lint, test on push/PR
   - `cd-deploy` — Deploy to Vercel/AWS/GCP/Azure
   - `docker` — Build and push Docker image
   - `release` — Automated releases on tag push
   - `dependabot` — Automated dependency updates
   - `codeql` — Security scanning
   - `stale` — Close stale issues/PRs
   - `custom` — Custom workflow from description

**If the user doesn't specify which workflows**, generate sensible defaults:
- For any project: `ci` (build + test)
- For deployable projects: `cd-deploy`
- For containerized projects: `docker`
- For all projects: `dependabot`

### Workflow 6: Security & Quality Configuration

Set up security features and quality gates.

**Steps:**
1. **Dependabot** — Create `.github/dependabot.yml`:
   - Enable version updates for the project's package ecosystem
   - Set review interval (weekly by default)
   - Configure auto-merge for patch updates if desired
2. **CodeQL** — Create `.github/workflows/codeql.yml`:
   - Configure for the project's language
   - Schedule weekly scans
3. **Branch Protection** — Configure via GitHub API:
   - Require PR reviews (1 approval minimum)
   - Require status checks (CI must pass)
   - Require signed commits for main/production branches
   - Restrict force pushes
4. **Secret Scanning** — Enable via GitHub API (if repo is on GitHub)

### Workflow 7: Release Management

Handle versioning, tagging, and changelog generation.

**Steps:**
1. Run `scripts/release.py --action <action> [--version <version>]`
2. **Create Release:**
   - Determine version bump type (major/minor/patch) from changes since last tag
   - Generate changelog from commit history (conventional commits format)
   - Create git tag (`v1.2.3`)
   - Create GitHub Release with changelog body
   - Push tag to remote
3. **Changelog Generation:**
   - Parse conventional commits since last tag
   - Group by type: Features, Bug Fixes, Breaking Changes, Other
   - Generate markdown changelog
4. **Version Bump:**
   - Update version in package.json / pyproject.toml / Cargo.toml
   - Commit version bump
   - Create tag

### Workflow 8: Issue & PR Management

Manage issues and pull requests with smart labeling and review.

**Issue Management:**
1. Create issues with templates (bug report, feature request, task)
2. Auto-label based on content (bug, feature, enhancement, documentation, good-first-issue)
3. Assign to milestone or project board
4. Triage: prioritize → label → assign → track

**PR Management:**
1. Create PRs with description templates
2. Auto-request reviewers based on CODEOWNERS
3. Generate PR description from commit messages
4. Review checklist validation before merge
5. Squash merge by default (configurable)

### Workflow 9: Test & Verify (Automated Intelligence Testing + Proof of Work)

This is the automated testing and verification workflow. It analyzes the project's source code, generates tailored test suites, executes them, and produces a verifiable Proof-of-Work report that is committed as an artifact in the repository. This ensures that every project produced by the agent has been tested and validated before it reaches GitHub.

**When to use:**
- As part of the One-Prompt workflow (step 5) — automatically runs after scaffolding
- Before any commit or push — to verify the code works
- When the user asks to "test the project", "run tests", "generate proof of work", or "verify the code works"
- When the user wants confidence that generated code is functional

**Steps:**
1. **Detect language and framework** — Automatically identifies the project's language, framework, and test runner (Vitest/Jest/pytest/go-test)
2. **Analyze source code** — `smart_test.py` scans all source files and extracts testable units:
   - Python: Functions, classes, methods (via AST parsing)
   - TypeScript/JavaScript: Functions, classes, React components, API route handlers (via regex)
   - Go: Functions, methods, structs, HTTP handlers (via regex)
3. **Generate test files** — Creates tailored test files for each module:
   - Unit tests for every detected function/class/method
   - API handler tests with mock Request/Response
   - Component tests with render testing stubs
   - Project health/structural tests (verify config files exist, imports work)
   - Shared fixtures (conftest.py for Python, setup for JS)
4. **Execute test suite** — Runs the full test suite using the detected framework
5. **Collect coverage data** — Measures code coverage percentage
6. **Generate TEST_REPORT.md** — Produces a comprehensive Proof-of-Work artifact containing:
   - Executive summary with pass/fail/skip/coverage metrics
   - Source code analysis breakdown (files scanned, units found)
   - List of generated test files
   - Test results with command used and duration
   - Coverage percentage
   - Verification checklist (all items checked off)
   - Test execution proof block (machine-readable)
   - Scanned source files list
7. **Commit artifacts** — Optionally commits test files and TEST_REPORT.md to the repo

**Script usage:**
```bash
# Full pipeline: generate + run + report
python3 scripts/smart_test.py --path /path/to/repo --all

# Generate tests only (don't run)
python3 scripts/smart_test.py --path /path/to/repo --generate

# Run existing tests and generate report
python3 scripts/smart_test.py --path /path/to/repo --run --report

# Full pipeline + auto-commit
python3 scripts/smart_test.py --path /path/to/repo --all --commit

# Override language detection
python3 scripts/smart_test.py --path /path/to/repo --all --language python
```

**What `smart_test.py` generates by project type:**

| Project Type | Test Framework | Test Types Generated |
|---|---|---|
| nextjs-fullstack | Vitest | Component tests, API handler tests, health tests, utility tests |
| react-spa | Vitest | Component tests, hook tests, health tests |
| node-api | Vitest/Jest | Route handler tests, middleware tests, health tests |
| python-api | pytest | API endpoint tests (with httpx), model tests, config tests, health tests |
| python-cli | pytest | Command tests, argument parsing tests, health tests |
| go-service | go test | Function tests, handler tests, struct tests, health tests |
| static-site | pytest | Smoke tests, structure tests |

**Proof-of-Work artifact (TEST_REPORT.md):**
- Contains a verification checklist that confirms all steps were executed
- Includes a machine-readable execution proof block with exact counts
- Provides the exact test command used (reproducible)
- Lists all scanned source files
- Badge showing PASS/FAIL status
- This report is committed alongside the code as verifiable evidence

**Integration with Workflow 1 (One-Prompt):**
When using the One-Prompt workflow, step 5 automatically runs the full test pipeline. The generated TEST_REPORT.md is included in the initial commit alongside the project code, providing immediate proof that the generated code has been tested and validated.

## Script Reference

### Setup & Dependencies

Before any GitHub operation, ensure the environment is ready. Run:

```bash
bash scripts/setup.sh
```

This installs the `gh` CLI if missing and checks git configuration. If `gh` is not available and cannot be installed, the scripts fall back to direct GitHub API calls using `curl`.

### Script: `repo_init.py`

Creates a new GitHub repository with initial files.

```bash
python3 scripts/repo_init.py \
  --name "my-project" \
  [--description "Project description"] \
  [--private] \
  [--template "nextjs-fullstack"] \
  [--license "MIT"] \
  [--org "organization-name"]
```

**What it does:**
- Checks if `gh` is available; falls back to GitHub API via curl
- Creates repo via `gh repo create` or API
- Clones the repo locally
- Adds README.md, .gitignore, LICENSE
- Creates initial commit
- Returns repo URL and local path

### Script: `scaffold.py`

Generates project structure from templates.

```bash
python3 scripts/scaffold.py \
  --template "nextjs-fullstack" \
  --path "/path/to/repo" \
  [--project-name "my-project"] \
  [--features "auth,stripe,charts"]
```

**What it does:**
- Reads template definition from `references/templates.md`
- Creates directory structure
- Generates configuration files (package.json, tsconfig, etc.)
- Sets up Docker if requested
- Creates environment template
- Does NOT commit (user should review first, then use `smart_commit.py`)

### Script: `smart_commit.py`

Analyzes changes and generates meaningful commits.

```bash
# Analyze and generate commit message
python3 scripts/smart_commit.py --path "/path/to/repo"

# Create initial commit
python3 scripts/smart_commit.py --init --path "/path/to/repo"

# Commit and push
python3 scripts/smart_commit.py --path "/path/to/repo" --push

# Custom message (still follows conventional format)
python3 scripts/smart_commit.py --path "/path/to/repo" --message "add user authentication"
```

**What it does:**
- Runs `git diff --stat` and `git diff --name-only` to analyze changes
- Categorizes changes by type (feat/fix/docs/etc.)
- Generates conventional commit message with body
- Stages all changed files (or only specified files)
- Commits with generated message
- Optionally pushes to remote

### Script: `actions_gen.py`

Generates GitHub Actions workflow files.

```bash
python3 scripts/actions_gen.py \
  --path "/path/to/repo" \
  --workflows "ci,dependabot,codeql" \
  [--language "typescript"] \
  [--deploy-target "vercel"]
```

**Available workflows:** `ci`, `cd-deploy`, `docker`, `release`, `dependabot`, `codeql`, `stale`

### Script: `release.py`

Manages releases, tags, and changelogs.

```bash
# Create a release (auto-detect version bump)
python3 scripts/release.py --action create --path "/path/to/repo"

# Create a specific version release
python3 scripts/release.py --action create --path "/path/to/repo" --version "1.2.0"

# Generate changelog only
python3 scripts/release.py --action changelog --path "/path/to/repo"

# List releases
python3 scripts/release.py --action list --path "/path/to/repo"
```

### Script: `smart_test.py`

Automated intelligence testing system — analyzes code, generates tests, executes them, and produces proof-of-work.

```bash
# Full pipeline: generate + run + report
python3 scripts/smart_test.py --path "/path/to/repo" --all

# Generate tests only (don't run)
python3 scripts/smart_test.py --path "/path/to/repo" --generate

# Run existing tests and generate report
python3 scripts/smart_test.py --path "/path/to/repo" --run --report

# Full pipeline + auto-commit test artifacts
python3 scripts/smart_test.py --path "/path/to/repo" --all --commit

# Override language/framework detection
python3 scripts/smart_test.py --path "/path/to/repo" --all --language python --framework pytest
```

**What it does:**
- Detects project language and test framework automatically
- Scans all source files and extracts testable units (functions, classes, methods, components, API handlers)
- Generates tailored test files with meaningful test cases for each unit
- Executes the full test suite using the appropriate runner
- Collects coverage metrics
- Generates `TEST_REPORT.md` as a verifiable Proof-of-Work artifact
- Optionally commits test files and report to the repository

**Supported frameworks:** Vitest, Jest, pytest, go-test

## Decision Guide: Which Workflow to Use

| User Says | Workflow |
|-----------|----------|
| "Build me a [project type]" or "Create a [project] and push to GitHub" | Workflow 1 (Full Orchestration) |
| "Create a new repo" or "Initialize a GitHub repo" | Workflow 2 (Repo Creation) |
| "Set up project structure" or "Scaffold a [framework] project" | Workflow 3 (Scaffolding) |
| "Commit these changes" or "Push to GitHub" | Workflow 4 (Smart Git) |
| "Set up CI/CD" or "Add GitHub Actions" | Workflow 5 (CI/CD) |
| "Configure security" or "Add Dependabot/CodeQL" | Workflow 6 (Security) |
| "Create a release" or "Generate changelog" | Workflow 7 (Release) |
| "Create an issue" or "Open a PR" | Workflow 8 (Issue/PR) |
| "Test the project", "Run tests", or "Generate proof of work" | Workflow 9 (Test & Verify) |

## Integration with Existing Skills

This agent orchestrates capabilities that overlap with several existing skills. When this skill is active, it takes precedence over these individual skills because it provides a unified workflow:

- **git-workflow** — This agent's smart_commit.py provides superior commit message generation with conventional commits, file analysis, and auto-categorization
- **github-actions-gen** — This agent's actions_gen.py provides more comprehensive workflow generation with 7+ workflow types
- **github-issue-resolver** — For issue resolution specifically, that skill's guardrails system is more robust; this agent defers to it for autonomous issue fixing
- **ruflo-github-automation** — This agent incorporates its review frameworks and release management patterns

**Defer to `github-issue-resolver`** when the user specifically asks to autonomously fix issues in an existing repo — that skill's 5-layer guardrail system is purpose-built for safe autonomous operation.

## Safety & Guardrails

This agent follows these safety principles:

1. **Never push to protected branches directly** — Always use PRs for main/production
2. **Never force push** — All pushes are normal; `--force` is never used
3. **Never commit secrets** — Scan for API keys, tokens, passwords before committing; abort if found
4. **Draft PRs by default** — PRs are created as drafts; user must explicitly request direct creation
5. **Confirm before destructive operations** — Deleting branches, closing issues, and merging PRs require user confirmation
6. **One repo at a time** — Focus on a single repository per operation to avoid cross-contamination
7. **Commit before push** — Always ensure commits are clean and reviewed before pushing
8. **Respect .gitignore** — Never stage or commit files that match .gitignore patterns

## Error Handling

When operations fail, follow this sequence:

1. **Authentication errors** — Guide user through `gh auth login` or token setup
2. **Repository not found** — Verify repo name and permissions
3. **Push rejected** — Pull with rebase first, resolve conflicts, then push
4. **Rate limiting** — Wait and retry with exponential backoff
5. **Network errors** — Retry once, then inform user
6. **Script not found** — The skill directory is at the path where this SKILL.md is located; use that as the base for script paths

## Quick Reference: Conventional Commits

```
feat: new feature for the user (not a new feature for build script)
fix: bug fix for the user (not a fix to a build script)
docs: changes to the documentation
style: formatting, missing semi-colons, etc. (no code change)
refactor: refactoring production code (no feature, no fix)
test: adding missing tests, refactoring tests (no production code change)
chore: updating grunt tasks, package.json, etc. (no production code change)
ci: continuous integration changes
perf: performance improvements
build: changes that affect the build system or external dependencies
```

**With scope:**
```
feat(auth): add JWT-based authentication
fix(api): handle null response from payment service
docs(readme): update installation instructions
ci(actions): add Node.js CI workflow
```

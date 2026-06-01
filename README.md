<div align="center">

# 🤖 GitHub Agent Skill

**One Prompt → Production GitHub Repository**

A unified orchestration skill for GLM that chains together all GitHub operations into seamless end-to-end workflows.

[![Skill](https://img.shields.io/badge/z.ai-Skill-blue?style=flat-square)](https://z.ai)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](./LICENSE)

</div>

---

## What It Does

Type a single prompt like:

> *"Build a SaaS dashboard with authentication, charts, and Stripe integration"*

And the GitHub Agent creates a **complete, CI/CD-ready GitHub repository** — repo, project scaffold, smart commits, workflows, security config, and pushes it all to GitHub.

## 8 Orchestration Workflows

| # | Workflow | What It Does |
|---|----------|-------------|
| 1 | **One-Prompt Project → GitHub** | Describe a project → get a fully configured repo |
| 2 | **Repo Creation & Init** | Create repos with README, .gitignore, LICENSE |
| 3 | **Project Scaffolding** | Generate full project structures from 7 templates |
| 4 | **Smart Git Operations** | Intelligent conventional commits + branch management |
| 5 | **CI/CD Pipeline Setup** | Generate GitHub Actions workflows |
| 6 | **Security & Quality** | Dependabot, CodeQL, branch protection |
| 7 | **Release Management** | Versioning, tagging, changelogs, GitHub Releases |
| 8 | **Issue & PR Management** | Smart labeling, templates, review workflows |

## 5 Executable Scripts

| Script | Lines | Purpose |
|--------|-------|---------|
| `repo_init.py` | 388 | Create GitHub repos via gh CLI or API fallback |
| `scaffold.py` | 933 | Generate project structures from 7 templates + feature add-ons |
| `smart_commit.py` | 390 | Analyze changes, generate conventional commit messages, scan for secrets |
| `actions_gen.py` | 549 | Generate 7 types of GitHub Actions workflows |
| `release.py` | 431 | Semantic versioning, changelog generation, GitHub Release creation |

## 7 Project Templates

`nextjs-fullstack` · `react-spa` · `node-api` · `python-api` · `python-cli` · `go-service` · `static-site`

## Feature Add-ons

`auth` · `docker` · `stripe` · `charts` · `testing` · `database` · `api`

## 7 CI/CD Workflow Types

`ci` · `cd-deploy` · `docker` · `release` · `dependabot` · `codeql` · `stale`

## Quick Start

### 1. Setup Environment

```bash
bash scripts/setup.sh
```

### 2. Create a Repository

```bash
python3 scripts/repo_init.py \
  --name "my-project" \
  --description "My awesome project" \
  --template "nextjs-fullstack" \
  --language "typescript"
```

### 3. Scaffold the Project

```bash
python3 scripts/scaffold.py \
  --template "nextjs-fullstack" \
  --path "./my-project" \
  --features "auth,docker,stripe,charts"
```

### 4. Generate CI/CD Workflows

```bash
python3 scripts/actions_gen.py \
  --path "./my-project" \
  --workflows "ci,dependabot,codeql" \
  --language "typescript"
```

### 5. Commit & Push

```bash
python3 scripts/smart_commit.py \
  --path "./my-project" \
  --push
```

### 6. Create a Release

```bash
python3 scripts/release.py \
  --path "./my-project" \
  --action create
```

## File Structure

```
github-agent/
├── SKILL.md                          # Main skill instructions (378 lines)
├── scripts/
│   ├── setup.sh                      # Environment setup & validation
│   ├── repo_init.py                  # GitHub repo creation
│   ├── scaffold.py                   # Project scaffolding from templates
│   ├── smart_commit.py              # Conventional commits + secret scanning
│   ├── actions_gen.py               # GitHub Actions workflow generator
│   └── release.py                   # Release management
├── references/
│   ├── templates.md                  # Project template specifications
│   ├── actions_catalog.md            # CI/CD workflow catalog
│   └── conventions.md               # Git conventions & commit format
└── assets/
    └── gitignore_templates/          # .gitignore files for 6 languages
        ├── Node.gitignore
        ├── Python.gitignore
        ├── Go.gitignore
        ├── Rust.gitignore
        ├── Java.gitignore
        └── Ruby.gitignore
```

## Key Design Decisions

- **Dual-mode**: Uses gh CLI when available, falls back to GitHub API via curl
- **Secret scanning**: Blocks commits containing API keys, tokens, private keys
- **Conventional commits**: Auto-generates from file analysis (type + scope + description)
- **Safety guardrails**: Never force push, never push directly to protected branches, draft PRs by default
- **Template variables**: All scaffold files support {project_name}, {project_description} placeholders

## Demo

This skill was used to create a full SaaS dashboard repository in a single prompt:

**[roman-ryzenadvanced/zdash](https://github.com/roman-ryzenadvanced/zdash)**

The ZDash repo was created with:
- repo_init.py → Created the GitHub repo
- scaffold.py → Generated Next.js 16 project with auth, Stripe, charts, Docker
- actions_gen.py → Added CI, Dependabot, CodeQL workflows
- smart_commit.py → Committed with conventional message and pushed

## Integration with Existing Skills

This agent orchestrates capabilities that overlap with several existing z.ai skills:

- **git-workflow** — This agent's smart_commit.py provides superior commit message generation
- **github-actions-gen** — This agent's actions_gen.py provides more comprehensive workflow generation
- **github-issue-resolver** — For autonomous issue fixing, that skill's guardrails system is more robust
- **ruflo-github-automation** — This agent incorporates its review frameworks and release patterns

## License

MIT License — see the LICENSE file for details.

---

<div align="center">

**Built for z.ai · Empowering developers with AI-powered GitHub workflows**

</div>

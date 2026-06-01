<div align="center">

[![Z.ai Coding Plans](https://img.shields.io/badge/Z.ai-Coding_Plans-7C3AED?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJMMiA3bDEwIDUgMTAtNS0xMC01eiIvPjxwYXRoIGQ9Ik0yIDE3bDEwIDUgMTAtNSIvPjxwYXRoIGQ9Ik0yIDEybDEwIDUgMTAtNSIvPjwvc3ZnPg==)](https://z.ai/subscribe?ic=ROK78RJKNW)

# 🚀 Get 10% OFF Z.ai Coding Plans

**Access the latest GLM models for coding with an exclusive discount**

[👉 Claim Your 10% OFF →](https://z.ai/subscribe?ic=ROK78RJKNW)

*Power your development with state-of-the-art AI models — from code generation to full-stack apps*

</div>

---

# GitHub Agent — One Prompt to Production Repository

A unified orchestration skill for GLM that turns a single natural language prompt into a fully configured, tested, CI/CD-ready GitHub repository. No more juggling individual tools for git, Actions, security, and testing — this agent chains them together into seamless end-to-end workflows.

## ✨ What It Does

Describe your project in plain English, and the GitHub Agent handles everything:

```
"Build a SaaS dashboard with authentication, charts, and Stripe integration"
```

↓ The agent creates a repo, scaffolds the project, generates & runs tests, sets up CI/CD, configures security, and pushes to GitHub — all from that one prompt.

## 🧠 9 Orchestration Workflows

| # | Workflow | Description |
|---|----------|-------------|
| 1 | **One-Prompt Project → GitHub** | Full pipeline: describe → repo → code → test → CI/CD → push |
| 2 | **Repository Creation** | Create & initialize GitHub repos with proper defaults |
| 3 | **Project Scaffolding** | Generate project structure from 7 templates |
| 4 | **Smart Git Operations** | Intelligent conventional commits + branch management |
| 5 | **CI/CD Pipeline Setup** | Generate GitHub Actions workflows (7 types) |
| 6 | **Security & Quality** | Dependabot, CodeQL, branch protection, secret scanning |
| 7 | **Release Management** | Semantic versioning, changelogs, GitHub Releases |
| 8 | **Issue & PR Management** | Smart labeling, templates, review workflows |
| 9 | **Test & Verify** 🆕 | **Automated test generation, execution, coverage, and Proof-of-Work** |

## 🧪 Workflow 9: Test & Verify (NEW)

The **Automated Intelligence Testing System** ensures every project is verified before it reaches GitHub:

1. **Source Analysis** — Scans all source files, extracts testable units (functions, classes, methods, components, API handlers)
2. **Test Generation** — Creates tailored test suites for each module (Vitest/Jest/pytest/go-test)
3. **Test Execution** — Runs the full suite and collects results
4. **Coverage Measurement** — Tracks code coverage percentage
5. **Proof-of-Work Report** — Generates `TEST_REPORT.md` with verifiable evidence

```bash
# Full pipeline: generate + run + report
python3 scripts/smart_test.py --path ./my-project --all

# Generate tests only
python3 scripts/smart_test.py --path ./my-project --generate

# Full pipeline + auto-commit
python3 scripts/smart_test.py --path ./my-project --all --commit
```

### Supported Languages & Frameworks

| Language | Test Framework | Analysis Method |
|----------|---------------|-----------------|
| TypeScript/JavaScript | Vitest / Jest | Regex-based extraction |
| Python | pytest | AST parsing |
| Go | go test | Regex-based extraction |

## 🏗️ 7 Project Templates

| Template | Stack |
|----------|-------|
| `nextjs-fullstack` | Next.js 16 + TypeScript + Tailwind + Prisma |
| `react-spa` | React + Vite + TypeScript |
| `node-api` | Express/Fastify REST API |
| `python-api` | FastAPI REST API |
| `python-cli` | Python CLI with Typer |
| `go-service` | Go microservice |
| `static-site` | Static HTML/CSS/JS |

### Feature Add-ons

`auth` · `docker` · `stripe` · `charts` · `testing` · `database` · `api`

## 📁 Project Structure

```
github-agent/
├── SKILL.md                    # Main skill definition (9 workflows)
├── scripts/
│   ├── repo_init.py            # Create GitHub repos
│   ├── scaffold.py             # Generate project structures
│   ├── smart_commit.py         # Conventional commits + secret scanning
│   ├── actions_gen.py          # GitHub Actions workflow generator
│   ├── release.py              # Version management + releases
│   └── smart_test.py           # 🆕 Automated testing + proof-of-work
├── references/
│   ├── templates.md            # Template catalog
│   ├── actions_catalog.md      # Actions workflow catalog
│   └── conventions.md          # Commit conventions reference
├── assets/
│   └── gitignore_templates/    # 6 .gitignore templates
└── README.md                   # This file
```

## 🚀 Quick Start

### As a GLM Skill

1. Place this directory in your GLM skills folder
2. GLM will automatically detect and activate the skill when you mention GitHub operations
3. Just describe what you want:

> "Create a new Next.js project with auth and Stripe, push it to GitHub, and make sure it passes tests"

### Using the Scripts Directly

```bash
# 1. Create a repo
python3 scripts/repo_init.py --name "my-project" --description "My awesome project"

# 2. Scaffold the project
python3 scripts/scaffold.py --template nextjs-fullstack --path ./my-project --features "auth,stripe,testing"

# 3. Generate and run tests
python3 scripts/smart_test.py --path ./my-project --all

# 4. Commit and push
python3 scripts/smart_commit.py --path ./my-project --init --push

# 5. Set up CI/CD
python3 scripts/actions_gen.py --path ./my-project --workflows "ci,dependabot,codeql"

# 6. Create a release
python3 scripts/release.py --action create --path ./my-project
```

## 🛡️ Safety & Guardrails

- Never pushes to protected branches directly
- Never force pushes
- Secret scanning before every commit (API keys, tokens, passwords)
- Draft PRs by default
- Confirmation required for destructive operations

## 📄 License

MIT

---

<div align="center">

**Built for [Z.ai](https://z.ai) — Power your code with the latest GLM models**

[Get 10% OFF coding plans →](https://z.ai/subscribe?ic=ROK78RJKNW)

</div>

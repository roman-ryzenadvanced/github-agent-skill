# GitHub Actions Workflow Catalog

This catalog describes all available GitHub Actions workflows that the agent can generate, along with when to use each one and what secrets/variables they require.

## Available Workflows

### CI (`ci`)

**Purpose:** Build, lint, type-check, and test on every push and pull request.

**Triggers:** push to main/master, pull_request to main/master

**Matrix strategy:** Tests against multiple language versions (e.g., Node 20+22, Python 3.11+3.12)

**Language support:** Node.js/TypeScript, Python, Go

**Required secrets:** None

**When to add:** Always. This is the default workflow for every project.

---

### CD / Deploy (`cd-deploy`)

**Purpose:** Deploy the application to a hosting platform on push to main.

**Targets:** Vercel, AWS (ECS/ECR)

**Required secrets:**
- **Vercel:** `VERCEL_TOKEN`
- **AWS:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`

**When to add:** When the project needs automatic deployment on merge to main.

---

### Docker (`docker`)

**Purpose:** Build a Docker image and push it to GitHub Container Registry (ghcr.io).

**Triggers:** push to main/master, tags (v*)

**Features:**
- Automatic tagging (branch name, semver, SHA)
- Labels and metadata from git context
- Pushes to ghcr.io

**Required secrets:** `GITHUB_TOKEN` (automatically available)

**When to add:** When the project is containerized and needs automated image builds.

---

### Release (`release`)

**Purpose:** Create GitHub Releases automatically when version tags are pushed.

**Triggers:** tags matching `v*`

**Features:**
- Auto-generates changelog from conventional commits
- Creates GitHub Release with changelog body
- Uses `softprops/action-gh-release` action

**Required secrets:** None (uses GITHUB_TOKEN)

**When to add:** When the project follows semantic versioning and needs automated releases.

---

### Dependabot (`dependabot`)

**Purpose:** Automatically check for and create PRs for dependency updates.

**Schedule:** Weekly on Mondays

**Features:**
- Version updates for the project's package ecosystem
- GitHub Actions version updates
- Auto-labels dependency PRs
- Limits to 10 open PRs at a time

**Package ecosystems:** npm, pip, gomod, bundler, maven

**Required secrets:** None

**When to add:** For all projects with dependencies. This is a default recommendation.

---

### CodeQL (`codeql`)

**Purpose:** Run security analysis using GitHub's CodeQL engine.

**Triggers:** push to main, pull_request to main, weekly schedule (Mondays)

**Languages:** JavaScript/TypeScript, Python, Go, Java, Ruby, C/C++, C#

**Required secrets:** None (uses GITHUB_TOKEN)

**Required permissions:** `security-events: write`, `actions: read`, `contents: read`

**When to add:** For all projects, especially those handling user input, authentication, or sensitive data. Required for open-source projects on GitHub for the Security tab.

---

### Stale (`stale`)

**Purpose:** Automatically close inactive issues and pull requests.

**Schedule:** Daily at midnight UTC

**Behavior:**
- Marks issues/PRs as stale after 60 days of inactivity
- Closes them 7 days after being marked stale
- Exempts issues/PRs with `pinned` or `security` labels

**Required secrets:** None

**When to add:** For active open-source projects with many issues. Not recommended for small/private repos.

---

## Workflow Combinations

### Recommended defaults by project type

**Full-stack web app (Next.js):**
- `ci` — Build, lint, test
- `cd-deploy` — Deploy to Vercel
- `dependabot` — Dependency updates
- `codeql` — Security scanning

**API service (Node.js/Python/Go):**
- `ci` — Build, lint, test
- `docker` — Container image builds
- `release` — Automated releases
- `dependabot` — Dependency updates
- `codeql` — Security scanning

**Open-source library:**
- `ci` — Build, lint, test (with multiple version matrix)
- `release` — Automated releases
- `dependabot` — Dependency updates
- `codeql` — Security scanning
- `stale` — Issue management

**CLI tool:**
- `ci` — Build, lint, test
- `release` — Automated releases with binaries
- `dependabot` — Dependency updates

**Static site:**
- `ci` — Basic validation
- `cd-deploy` — Deploy to Vercel or GitHub Pages

---

## Custom Workflows

If the user describes a workflow that doesn't match any template, create a custom workflow based on:
1. The triggers they specify (push, schedule, manual)
2. The steps they describe
3. Standard GitHub Actions best practices

Always include:
- Checkout step
- Language/tool setup step
- The custom steps
- Proper permissions block
- Caching where applicable

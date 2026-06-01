# Git Conventions Reference

## Conventional Commits

All commits should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature for the user | `feat(auth): add JWT-based authentication` |
| `fix` | Bug fix for the user | `fix(api): handle null response from payment service` |
| `docs` | Documentation changes | `docs(readme): update installation instructions` |
| `style` | Formatting, no code change | `style: fix indentation in auth module` |
| `refactor` | Code restructuring | `refactor(db): extract connection pool logic` |
| `test` | Adding or updating tests | `test(auth): add unit tests for login flow` |
| `chore` | Build/config changes | `chore(deps): update dependencies` |
| `ci` | CI/CD changes | `ci: add Python 3.12 to test matrix` |
| `perf` | Performance improvements | `perf(query): add database index for user lookups` |
| `build` | Build system changes | `build: update webpack configuration` |
| `revert` | Revert a previous commit | `revert: revert feat(auth): add JWT auth` |

### Scope Guidelines

Scope should be a noun describing the section of the codebase:
- `auth` — Authentication/authorization
- `api` — API endpoints
- `ui` — User interface components
- `db` — Database layer
- `deps` — Dependencies
- `config` — Configuration
- `cli` — Command-line interface
- `docs` — Documentation

### Breaking Changes

Indicate breaking changes in two ways:
1. `!` after the type/scope: `feat(api)!: change response format`
2. `BREAKING CHANGE:` in the footer

### Examples

**Simple feature:**
```
feat(dashboard): add revenue chart component
```

**Feature with body:**
```
feat(auth): implement OAuth2 Google login

- Add Google OAuth2 provider
- Create callback handler
- Store user profile in database
- Add login/logout routes
```

**Bug fix:**
```
fix(payment): handle Stripe webhook signature verification

The webhook handler was not verifying the Stripe signature,
which could allow forged requests. Added proper signature
verification before processing events.
```

**Breaking change:**
```
feat(api)!: change user endpoint response format

BREAKING CHANGE: The /api/users endpoint now returns
a paginated response with { data, total, page, limit }
instead of a flat array.
```

---

## Branch Naming

### Branch Types

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New feature development | `feature/PROJ-123-user-auth` |
| `fix/` | Bug fixes | `fix/PROJ-456-login-error` |
| `hotfix/` | Urgent production fixes | `hotfix/PROJ-789-payment-crash` |
| `release/` | Release preparation | `release/v1.2.0` |
| `docs/` | Documentation updates | `docs/api-reference` |
| `refactor/` | Code refactoring | `refactor/database-layer` |
| `test/` | Test additions | `test/auth-integration` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

### Branch Name Rules

1. Use lowercase with hyphens (not underscores)
2. Include ticket number if available: `feature/PROJ-123-description`
3. Keep description short but descriptive (3-5 words)
4. No special characters except hyphens

---

## Pull Request Conventions

### PR Title

Follow the same conventional commit format:
```
feat(auth): add OAuth2 Google login
```

### PR Description Template

```markdown
## Changes

<!-- Describe what this PR changes and why -->

## Type of Change

- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring
- [ ] Test addition

## Testing

<!-- How was this tested? -->

## Checklist

- [ ] Self-reviewed the code
- [ ] Added tests for new functionality
- [ ] Updated documentation if needed
- [ ] No breaking changes (or documented them)
```

### PR Size Guidelines

| Lines Changed | Review Depth | Expected Time |
|--------------|--------------|---------------|
| < 50 | Quick scan | 5-10 min |
| 50-200 | Standard review | 15-30 min |
| 200-500 | Deep review | 30-60 min |
| 500+ | Consider splitting | Multiple sessions |

---

## Version Strategy

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

- **MAJOR** — Breaking changes (incompatible API changes)
- **MINOR** — New features (backward compatible)
- **PATCH** — Bug fixes (backward compatible)

### Auto-version Detection from Commits

| Commit Pattern | Version Bump |
|---------------|-------------|
| `feat!:` or `BREAKING CHANGE` | Major |
| `feat:` | Minor |
| `fix:`, `perf:` | Patch |
| All others | No automatic bump |

### Pre-release Versions

- Alpha: `1.0.0-alpha.1`
- Beta: `1.0.0-beta.1`
- Release Candidate: `1.0.0-rc.1`

---

## Tag Format

- Release tags: `v1.2.3` (always prefix with `v`)
- Pre-release tags: `v1.0.0-beta.1`
- No other tag naming conventions

---

## Changelog Format

Generated changelogs group changes by type:

```markdown
## v1.2.0 (2025-01-15)

### 🚀 Features
- **auth**: add OAuth2 Google login
- **dashboard**: add revenue chart component

### 🐛 Bug Fixes
- **api**: handle null response from payment service
- **ui**: fix mobile navigation overlap

### ⚡ Performance
- **db**: add index for user lookup queries

### 📚 Documentation
- update API reference for v1.2
```

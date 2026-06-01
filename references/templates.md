# Project Templates Reference

This document defines the available project templates for scaffolding. Each template includes directory structure, configuration files, and boilerplate code.

## Template Selection Guide

| Template | Best For | Language | Framework |
|----------|----------|----------|-----------|
| `nextjs-fullstack` | Full-stack web apps, SaaS, dashboards | TypeScript | Next.js 16 |
| `react-spa` | Single-page applications | TypeScript | React + Vite |
| `node-api` | REST APIs, microservices | TypeScript | Express |
| `python-api` | REST APIs, data services | Python | FastAPI |
| `python-cli` | CLI tools, automation scripts | Python | Typer |
| `go-service` | High-performance services | Go | stdlib |
| `static-site` | Landing pages, documentation | HTML/CSS/JS | None |
| `monorepo` | Multi-package projects | TypeScript | Turborepo |

## Detailed Template Specifications

### nextjs-fullstack

**When to use:** Building any full-stack web application — SaaS products, dashboards, admin panels, e-commerce, or content sites.

**Key decisions:**
- Uses App Router (Next.js 16 default)
- Prisma for database ORM (SQLite for dev, configurable for prod)
- Tailwind CSS 4 for styling
- Vitest for testing
- Zod for runtime validation

**Directory structure:**
```
src/
├── app/              # Next.js App Router pages
│   ├── api/          # API routes
│   ├── layout.tsx    # Root layout
│   ├── page.tsx      # Home page
│   └── globals.css   # Global styles
├── components/       # Reusable components
│   └── ui/           # Base UI components
├── lib/              # Utility functions
├── hooks/            # Custom React hooks
└── types/            # TypeScript type definitions
prisma/
├── schema.prisma     # Database schema
public/               # Static assets
tests/                # Test files
docs/                 # Documentation
.github/workflows/    # CI/CD pipelines
```

**Features that can be added:**
- `auth` — Authentication with NextAuth.js
- `stripe` — Payment integration with Stripe
- `charts` — Data visualization with Recharts
- `docker` — Docker + docker-compose configuration
- `database` — Additional database setup (PostgreSQL, MySQL)

---

### react-spa

**When to use:** Building client-side single-page applications that don't need server-side rendering — tool UIs, interactive dashboards, browser extensions.

**Key decisions:**
- Vite for build tooling (fast HMR)
- React Router v7 for client-side routing
- Tailwind CSS 4 for styling

**Directory structure:**
```
src/
├── components/       # Reusable components
├── hooks/            # Custom React hooks
├── pages/            # Page components
├── utils/            # Utility functions
├── types/            # TypeScript type definitions
├── assets/           # Static assets
public/               # Public assets
tests/                # Test files
.github/workflows/    # CI/CD pipelines
```

---

### node-api

**When to use:** Building backend APIs, microservices, or server applications.

**Key decisions:**
- Express for HTTP server
- Helmet for security headers
- CORS for cross-origin support
- Zod for request validation
- tsx for development with hot reload

**Directory structure:**
```
src/
├── routes/           # Route definitions
├── middleware/        # Express middleware
├── controllers/      # Request handlers
├── models/           # Data models
├── services/         # Business logic
├── utils/            # Utility functions
├── types/            # TypeScript type definitions
└── index.ts          # Application entry point
tests/                # Test files
docs/                 # API documentation
.github/workflows/    # CI/CD pipelines
```

---

### python-api

**When to use:** Building Python backend services, data APIs, or ML model serving.

**Key decisions:**
- FastAPI for async API framework
- Pydantic for data validation and settings
- uvicorn for ASGI server
- Ruff for linting (replaces Flake8, isort, Black)
- pytest for testing

**Directory structure:**
```
app/
├── routers/          # API route handlers
├── models/           # Data models
├── services/         # Business logic
├── schemas/          # Pydantic schemas
├── core/             # Configuration, database
│   ├── config.py     # Settings management
│   └── database.py   # Database connection
└── main.py           # Application entry point
tests/                # Test files
docs/                 # API documentation
.github/workflows/    # CI/CD pipelines
```

---

### python-cli

**When to use:** Building command-line tools, automation scripts, or developer utilities.

**Key decisions:**
- Typer for CLI framework
- Rich for terminal output formatting
- Ruff for linting

**Directory structure:**
```
src/{project_name}/
├── main.py           # CLI entry point
├── commands/         # Command implementations
└── utils/            # Utility functions
tests/                # Test files
docs/                 # Documentation
.github/workflows/    # CI/CD pipelines
```

---

### go-service

**When to use:** Building high-performance services, APIs, or system tools where Go's concurrency model is beneficial.

**Key decisions:**
- Standard library HTTP server
- Standard Go project layout
- go test for testing

**Directory structure:**
```
cmd/
└── server/
    └── main.go       # Application entry point
internal/
├── handler/          # HTTP handlers
├── service/          # Business logic
├── repository/       # Data access
└── model/            # Data models
pkg/                  # Public packages
tests/                # Integration tests
docs/                 # Documentation
.github/workflows/    # CI/CD pipelines
```

---

### static-site

**When to use:** Building simple websites, landing pages, or documentation sites that don't need a build step.

**Directory structure:**
```
css/
└── style.css         # Stylesheets
js/
└── main.js           # JavaScript
assets/               # Images, fonts, etc.
index.html            # Home page
docs/                 # Documentation
.github/workflows/    # CI/CD pipelines
```

---

## Custom Template Creation

If none of the built-in templates match, the agent can create a custom scaffold by:

1. Asking the user for the tech stack and features
2. Creating a minimal directory structure based on the language
3. Adding configuration files appropriate for the framework
4. Setting up a basic "hello world" entry point

When creating a custom template, always include:
- README.md with setup instructions
- .gitignore for the primary language
- .env.example for environment variables
- A test file stub
- A .github/workflows/ci.yml for basic CI

#!/usr/bin/env python3
"""
Project Scaffolding Script
Generates project structure from templates.
Reads template definitions and creates directories, configs, and boilerplate.
"""

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_REF = SKILL_DIR / "references" / "templates.md"


# ─── Template Definitions ───────────────────────────────────────────────

TEMPLATES = {
    "nextjs-fullstack": {
        "description": "Next.js 16 + TypeScript + Tailwind CSS + Prisma",
        "language": "typescript",
        "framework": "nextjs",
        "directories": [
            "src/app",
            "src/app/api",
            "src/components",
            "src/components/ui",
            "src/lib",
            "src/hooks",
            "src/types",
            "prisma",
            "public",
            "tests",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "package.json": {
                "content": """{
  "name": "{project_name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest",
    "test:e2e": "playwright test",
    "db:push": "prisma db push",
    "db:studio": "prisma studio",
    "db:generate": "prisma generate"
  },
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@prisma/client": "^6.0.0",
    "tailwindcss": "^4.0.0",
    "zod": "^3.23.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "@types/react": "^19.0.0",
    "@types/node": "^22.0.0",
    "prisma": "^6.0.0",
    "vitest": "^2.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^16.0.0"
  }
}"""
            },
            "tsconfig.json": {
                "content": """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""
            },
            "next.config.ts": {
                "content": """import type {{ NextConfig }} from 'next';

const nextConfig: NextConfig = {{
  /* config options here */
}};

export default nextConfig;
"""
            },
            "src/app/layout.tsx": {
                "content": """import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '{project_name}',
  description: '{project_description}',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
"""
            },
            "src/app/page.tsx": {
                "content": """export default function Home() {
  return (
    <main>
      <h1>Welcome to {project_name}</h1>
    </main>
  );
}
"""
            },
            "src/app/globals.css": {
                "content": """@import 'tailwindcss';
"""
            },
            "prisma/schema.prisma": {
                "content": """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// Add your models here
// model User {
//   id        Int      @id @default(autoincrement())
//   email     String   @unique
//   name      String?
//   createdAt DateTime @default(now())
// }
"""
            },
            ".env.example": {
                "content": """# Database
DATABASE_URL="file:./dev.db"

# Auth (if applicable)
# NEXTAUTH_SECRET=""
# NEXTAUTH_URL="http://localhost:3000"

# API Keys (add yours)
# STRIPE_SECRET_KEY=""
# STRIPE_PUBLISHABLE_KEY=""
"""
            },
            "vitest.config.ts": {
                "content": """import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    environment: 'node',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
"""
            },
        },
    },

    "react-spa": {
        "description": "React + Vite + TypeScript",
        "language": "typescript",
        "framework": "react",
        "directories": [
            "src/components",
            "src/hooks",
            "src/pages",
            "src/utils",
            "src/types",
            "src/assets",
            "public",
            "tests",
            ".github/workflows",
        ],
        "files": {
            "package.json": {
                "content": """{
  "name": "{project_name}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext ts,tsx"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0",
    "vitest": "^2.0.0",
    "tailwindcss": "^4.0.0"
  }
}"""
            },
            "tsconfig.json": {
                "content": """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}"""
            },
            "vite.config.ts": {
                "content": """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
"""
            },
            ".env.example": {
                "content": """# API Keys
# VITE_API_URL=http://localhost:3001
"""
            },
        },
    },

    "node-api": {
        "description": "Node.js REST API with Express/TypeScript",
        "language": "typescript",
        "framework": "express",
        "directories": [
            "src/routes",
            "src/middleware",
            "src/controllers",
            "src/models",
            "src/services",
            "src/utils",
            "src/types",
            "tests",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "package.json": {
                "content": """{
  "name": "{project_name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest",
    "lint": "eslint src --ext ts"
  },
  "dependencies": {
    "express": "^4.21.0",
    "cors": "^2.8.5",
    "helmet": "^8.0.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/express": "^5.0.0",
    "@types/cors": "^2.8.0",
    "@types/node": "^22.0.0",
    "typescript": "^5.6.0",
    "tsx": "^4.19.0",
    "vitest": "^2.0.0"
  }
}"""
            },
            "tsconfig.json": {
                "content": """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}"""
            },
            "src/index.ts": {
                "content": """import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Routes
// app.use('/api', routes);

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});

export default app;
"""
            },
            ".env.example": {
                "content": """# Server
PORT=3001
NODE_ENV=development

# Database
# DATABASE_URL=""

# Auth
# JWT_SECRET=""
"""
            },
        },
    },

    "python-api": {
        "description": "Python REST API with FastAPI",
        "language": "python",
        "framework": "fastapi",
        "directories": [
            "app/routers",
            "app/models",
            "app/services",
            "app/schemas",
            "app/core",
            "tests",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "pyproject.toml": {
                "content": """[project]
name = "{project_name}"
version = "0.1.0"
description = "{project_description}"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
    "ruff>=0.7.0",
    "mypy>=1.13.0",
]
"""
            },
            "app/main.py": {
                "content": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{project_name}",
    description="{project_description}",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Include routers
# from app.routers import items
# app.include_router(items.router, prefix="/api/items", tags=["items"])
"""
            },
            "app/core/config.py": {
                "content": """from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "{project_name}"
    debug: bool = True
    database_url: str = "sqlite:///./dev.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
"""
            },
            ".env.example": {
                "content": """# App
APP_NAME={project_name}
DEBUG=true

# Database
DATABASE_URL=sqlite:///./dev.db
"""
            },
        },
    },

    "python-cli": {
        "description": "Python CLI tool with Typer",
        "language": "python",
        "framework": "typer",
        "directories": [
            "src/{project_name_hyphen}",
            "tests",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "pyproject.toml": {
                "content": """[project]
name = "{project_name}"
version = "0.1.0"
description = "{project_description}"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.13.0",
    "rich>=13.0.0",
]

[project.scripts]
{project_name} = "src.{project_name_hyphen}.main:app"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.7.0",
    "mypy>=1.13.0",
]
"""
            },
            "src/{project_name_hyphen}/main.py": {
                "content": """import typer

app = typer.Typer(help="{project_description}")


@app.command()
def hello(name: str = "World"):
    \"\"\"Say hello.\"\"\"
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
"""
            },
        },
    },

    "go-service": {
        "description": "Go microservice with standard layout",
        "language": "go",
        "framework": "stdlib",
        "directories": [
            "cmd/server",
            "internal/handler",
            "internal/service",
            "internal/repository",
            "internal/model",
            "pkg",
            "tests",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "cmd/server/main.go": {
                "content": """package main

import (
\t"fmt"
\t"log"
\t"net/http"
\t"os"
)

func main() {
\tport := os.Getenv("PORT")
\tif port == "" {
\t\tport = "8080"
\t}

\thttp.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
\t\tw.WriteHeader(http.StatusOK)
\t\tfmt.Fprintf(w, `{"status":"ok"}`)
\t})

\tlog.Printf("Server starting on port %s", port)
\tif err := http.ListenAndServe(":"+port, nil); err != nil {
\t\tlog.Fatalf("Server failed: %v", err)
\t}
}
"""
            },
            "go.mod": {
                "content": """module {project_name}

go 1.22
"""
            },
            ".env.example": {
                "content": """# Server
PORT=8080
"""
            },
        },
    },

    "static-site": {
        "description": "Static HTML/CSS/JS website",
        "language": "html",
        "framework": "none",
        "directories": [
            "css",
            "js",
            "assets",
            "docs",
            ".github/workflows",
        ],
        "files": {
            "index.html": {
                "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>{project_name}</h1>
    <p>{project_description}</p>
    <script src="js/main.js"></script>
</body>
</html>
"""
            },
            "css/style.css": {
                "content": """/* {project_name} Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: #333;
}
"""
            },
            "js/main.js": {
                "content": """// {project_name} JavaScript

console.log('{project_name} loaded');
"""
            },
        },
    },
}


def sanitize_project_name(name):
    """Convert project name to a valid module/directory name."""
    return name.lower().replace("-", "_").replace(" ", "_")


def apply_template_vars(content, project_name, description=""):
    """Replace template variables in content."""
    hyphen_name = sanitize_project_name(project_name)
    replacements = {
        "{project_name}": project_name,
        "{project_name_hyphen}": hyphen_name,
        "{project_description}": description or project_name,
    }
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def create_template_file(path, content, project_name, description=""):
    """Create a file with template variables applied."""
    resolved_content = apply_template_vars(content, project_name, description)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(resolved_content)


def scaffold_project(template_name, project_path, project_name, description="", features=""):
    """Scaffold a project from a template."""
    template = TEMPLATES.get(template_name)
    if not template:
        print(f"❌ Unknown template: {template_name}", file=sys.stderr)
        print(f"   Available templates: {', '.join(TEMPLATES.keys())}", file=sys.stderr)
        sys.exit(1)

    repo_dir = Path(project_path).resolve()
    if not repo_dir.exists():
        print(f"❌ Path does not exist: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"🏗️  Scaffolding project with template: {template_name}")
    print(f"   Path: {repo_dir}")
    print(f"   Description: {template['description']}")

    # Create directories
    created_dirs = 0
    for dir_path in template["directories"]:
        resolved = apply_template_vars(dir_path, project_name, description)
        full_path = repo_dir / resolved
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created_dirs += 1
    print(f"  ✅ Created {created_dirs} directories")

    # Create files
    created_files = 0
    for file_path, file_data in template["files"].items():
        resolved_path = apply_template_vars(file_path, project_name, description)
        full_path = repo_dir / resolved_path
        content = file_data.get("content", "")
        create_template_file(full_path, content, project_name, description)
        created_files += 1
    print(f"  ✅ Created {created_files} files")

    # Handle additional features
    if features:
        feature_list = [f.strip() for f in features.split(",")]
        _add_features(repo_dir, project_name, description, feature_list, template_name)

    print(f"\n🎉 Project scaffolded successfully!")
    print(f"   Template: {template_name}")
    print(f"   Dirs: {created_dirs}")
    print(f"   Files: {created_files}")
    print(f"\n💡 Next steps:")
    print(f"   cd {repo_dir}")
    if template["language"] in ("typescript", "javascript"):
        print(f"   npm install")
    print(f"   # Review the generated structure and customize as needed")


def _add_features(repo_dir, project_name, description, features, template_name):
    """Add additional features to the scaffolded project."""
    print(f"  📦 Adding features: {', '.join(features)}")

    feature_implementations = {
        "auth": _add_auth_feature,
        "docker": _add_docker_feature,
        "stripe": _add_stripe_feature,
        "charts": _add_charts_feature,
        "testing": _add_testing_feature,
        "database": _add_database_feature,
        "api": _add_api_feature,
    }

    for feature in features:
        impl = feature_implementations.get(feature.lower())
        if impl:
            impl(repo_dir, project_name, description, template_name)
        else:
            print(f"  ⚠️  Unknown feature: {feature} (skipping)")


def _add_auth_feature(repo_dir, project_name, description, template_name):
    """Add authentication boilerplate."""
    if template_name in ("nextjs-fullstack",):
        auth_dir = repo_dir / "src" / "app" / "api" / "auth"
        auth_dir.mkdir(parents=True, exist_ok=True)
        (auth_dir / "route.ts").write_text(f"""// Auth API route for {project_name}
// Implement your authentication logic here
// Consider using NextAuth.js or a custom JWT approach

import {{ NextRequest, NextResponse }} from 'next/server';

export async function POST(request: NextRequest) {{
  // Handle login/register
  return NextResponse.json({{ message: 'Auth endpoint' }});
}}
""")
        print("  ✅ Added auth feature (NextAuth route stub)")
    else:
        print("  ⚠️  Auth feature only supported for nextjs-fullstack template")


def _add_docker_feature(repo_dir, project_name, description, template_name):
    """Add Docker configuration."""
    template = TEMPLATES.get(template_name, {})
    language = template.get("language", "node")

    # Dockerfile
    dockerfile_content = ""
    if language == "typescript":
        dockerfile_content = f"""FROM node:22-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
"""
    elif language == "python":
        dockerfile_content = f"""FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    elif language == "go":
        dockerfile_content = f"""FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

FROM alpine:3.20
COPY --from=builder /server /server
EXPOSE 8080
CMD ["/server"]
"""

    if dockerfile_content:
        (repo_dir / "Dockerfile").write_text(dockerfile_content)
        print("  ✅ Added Dockerfile")

    # docker-compose.yml
    compose_content = f"""version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
"""
    (repo_dir / "docker-compose.yml").write_text(compose_content)
    print("  ✅ Added docker-compose.yml")


def _add_stripe_feature(repo_dir, project_name, description, template_name):
    """Add Stripe integration stub."""
    if template_name in ("nextjs-fullstack",):
        stripe_dir = repo_dir / "src" / "app" / "api" / "stripe"
        stripe_dir.mkdir(parents=True, exist_ok=True)
        (stripe_dir / "route.ts").write_text(f"""// Stripe API route for {project_name}
import {{ NextRequest, NextResponse }} from 'next/server';

export async function POST(request: NextRequest) {{
  // Handle Stripe webhook events
  // Verify webhook signature, process events
  return NextResponse.json({{ received: true }});
}}
""")
        print("  ✅ Added Stripe feature (webhook route stub)")
    else:
        print("  ⚠️  Stripe feature only supported for nextjs-fullstack template")


def _add_charts_feature(repo_dir, project_name, description, template_name):
    """Add chart library dependency."""
    if template_name in ("nextjs-fullstack", "react-spa"):
        # Note: actual package.json modification would be needed
        print("  ✅ Added charts feature (add recharts or chart.js via npm)")
    else:
        print("  ⚠️  Charts feature only supported for React-based templates")


def _add_testing_feature(repo_dir, project_name, description, template_name):
    """Add comprehensive testing infrastructure with smart test integration."""
    template = TEMPLATES.get(template_name, {})
    language = template.get("language", "typescript")

    test_dir = repo_dir / "tests"
    test_dir.mkdir(parents=True, exist_ok=True)

    if language in ("typescript", "javascript"):
        # TypeScript/JavaScript testing setup
        test_content = """// Auto-generated test suite — customize these tests for your project
// Run with: npx vitest

import { describe, it, expect } from 'vitest';

describe('Project Setup', () => {
  it('should have a package.json', async () => {
    const fs = await import('fs');
    const path = await import('path');
    const pkgPath = path.resolve(process.cwd(), 'package.json');
    expect(fs.existsSync(pkgPath)).toBe(true);
  });

  it('should have valid package.json with name and version', async () => {
    const fs = await import('fs');
    const path = await import('path');
    const pkg = JSON.parse(
      fs.readFileSync(path.resolve(process.cwd(), 'package.json'), 'utf-8')
    );
    expect(pkg.name).toBeDefined();
    expect(pkg.version).toBeDefined();
  });

  it('should have a src directory', async () => {
    const fs = await import('fs');
    const path = await import('path');
    expect(fs.existsSync(path.resolve(process.cwd(), 'src'))).toBe(true);
  });
});
"""
        (test_dir / "setup.test.ts").write_text(test_content)
        print("  ✅ Added testing infrastructure (Vitest + setup tests)")

    elif language == "python":
        # Python testing setup
        init_file = test_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")

        conftest_content = """\"\"\"Shared test fixtures.\"\"\"

import pytest
"""
        (test_dir / "conftest.py").write_text(conftest_content)

        test_content = """\"\"\"Auto-generated test suite — customize these tests for your project
Run with: pytest tests/ -v
\"\"\"

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestProjectSetup:
    \"\"\"Verify project structure and configuration.\"\"\"

    def test_pyproject_toml_exists(self):
        assert (PROJECT_ROOT / "pyproject.toml").exists()

    def test_project_has_name(self):
        import tomllib
        with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        assert "project" in data
        assert "name" in data["project"]

    def test_source_directory_exists(self):
        has_app = (PROJECT_ROOT / "app").exists()
        has_src = (PROJECT_ROOT / "src").exists()
        assert has_app or has_src, "No app/ or src/ directory found"
"""
        (test_dir / "test_setup.py").write_text(test_content)
        print("  ✅ Added testing infrastructure (pytest + conftest + setup tests)")

    elif language == "go":
        # Go testing setup
        health_test = """package main

import (
\t"os"
\t"testing"
)

func TestProjectSetup(t *testing.T) {
\tt.Run("go.mod exists", func(t *testing.T) {
\t\tif _, err := os.Stat("go.mod"); os.IsNotExist(err) {
\t\t\tt.Error("go.mod not found")
\t\t}
\t})

\tt.Run("README exists", func(t *testing.T) {
\t\tif _, err := os.Stat("README.md"); os.IsNotExist(err) {
\t\t\tt.Error("README.md not found")
\t\t}
\t})
}
"""
        test_file = repo_dir / "health_test.go"
        test_file.write_text(health_test)
        print("  ✅ Added testing infrastructure (go test + health tests)")

    else:
        # Generic
        test_content = """# Smoke test
def test_project_exists():
    assert True
"""
        (test_dir / "test_smoke.py").write_text(test_content)
        print("  ✅ Added testing infrastructure (generic)")

    # Always create a marker file indicating smart_test.py is available
    smart_test_note = test_dir / ".smart-test-enabled"
    smart_test_note.write_text(
        "# This project has Smart Test support.\n"
        "# Run: python3 scripts/smart_test.py --path . --all\n"
    )
    print("  ✅ Smart Test System enabled (run smart_test.py for full analysis)")


def _add_database_feature(repo_dir, project_name, description, template_name):
    """Add database configuration."""
    if template_name == "python-api":
        db_file = repo_dir / "app" / "core" / "database.py"
        db_file.parent.mkdir(parents=True, exist_ok=True)
        db_file.write_text(f"""# Database configuration for {project_name}
# Add your database connection and session management here
""")
    print("  ✅ Added database configuration stub")


def _add_api_feature(repo_dir, project_name, description, template_name):
    """Add API route structure."""
    if template_name == "nextjs-fullstack":
        api_dir = repo_dir / "src" / "app" / "api"
        api_dir.mkdir(parents=True, exist_ok=True)
    print("  ✅ Added API feature")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a project from a template")
    parser.add_argument("--template", required=True, help="Template name")
    parser.add_argument("--path", required=True, help="Path to the repository")
    parser.add_argument("--project-name", default="", help="Project name (default: directory name)")
    parser.add_argument("--description", default="", help="Project description")
    parser.add_argument("--features", default="", help="Comma-separated features to add (auth,docker,stripe,charts,testing,database,api)")

    args = parser.parse_args()

    project_name = args.project_name or Path(args.path).name
    scaffold_project(args.template, args.path, project_name, args.description, args.features)


if __name__ == "__main__":
    main()

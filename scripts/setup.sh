#!/usr/bin/env bash
# GitHub Agent Setup Script
# Checks and installs dependencies needed for GitHub operations

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔧 GitHub Agent Environment Setup"
echo "=================================="

ERRORS=0

# Check git
echo ""
echo "📋 Checking git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "  ✅ $GIT_VERSION"
else
    echo "  ❌ git is not installed"
    ERRORS=$((ERRORS + 1))
fi

# Check git config
echo ""
echo "📋 Checking git configuration..."
GIT_USER=$(git config --global user.name 2>/dev/null || echo "")
GIT_EMAIL=$(git config --global user.email 2>/dev/null || echo "")
if [ -n "$GIT_USER" ] && [ -n "$GIT_EMAIL" ]; then
    echo "  ✅ user.name: $GIT_USER"
    echo "  ✅ user.email: $GIT_EMAIL"
else
    echo "  ⚠️  Git user config incomplete"
    [ -z "$GIT_USER" ] && echo "  ❌ user.name not set (run: git config --global user.name \"Your Name\")"
    [ -z "$GIT_EMAIL" ] && echo "  ❌ user.email not set (run: git config --global user.email \"you@example.com\")"
fi

# Check gh CLI
echo ""
echo "📋 Checking GitHub CLI (gh)..."
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version 2>/dev/null | head -1)
    echo "  ✅ $GH_VERSION"

    # Check auth status
    if gh auth status &> /dev/null; then
        GH_USER=$(gh api user --jq '.login' 2>/dev/null || echo "unknown")
        echo "  ✅ Authenticated as: $GH_USER"
    else
        echo "  ⚠️  gh is installed but not authenticated"
        echo "     Run: gh auth login"
    fi
else
    echo "  ⚠️  gh CLI not found — will use GitHub API fallback"
    echo "     To install: https://cli.github.com/"

    # Try to install gh
    if command -v apt-get &> /dev/null; then
        echo "     Attempting to install via apt..."
        sudo apt-get update -qq && sudo apt-get install -y -qq gh 2>/dev/null && echo "  ✅ gh installed successfully" || echo "  ⚠️  Could not install gh automatically"
    elif command -v brew &> /dev/null; then
        echo "     Attempting to install via brew..."
        brew install gh 2>/dev/null && echo "  ✅ gh installed successfully" || echo "  ⚠️  Could not install gh automatically"
    elif command -v conda &> /dev/null; then
        echo "     Attempting to install via conda..."
        conda install -c conda-forge gh 2>/dev/null && echo "  ✅ gh installed successfully" || echo "  ⚠️  Could not install gh automatically"
    else
        echo "     Manual install required: https://cli.github.com/"
    fi
fi

# Check Python3
echo ""
echo "📋 Checking Python3..."
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    echo "  ✅ $PY_VERSION"
else
    echo "  ❌ Python3 is not installed"
    ERRORS=$((ERRORS + 1))
fi

# Check curl (for API fallback)
echo ""
echo "📋 Checking curl (API fallback)..."
if command -v curl &> /dev/null; then
    echo "  ✅ curl available"
else
    echo "  ❌ curl is not installed"
    ERRORS=$((ERRORS + 1))
fi

# Check for GitHub token
echo ""
echo "📋 Checking GitHub authentication..."
if [ -n "${GITHUB_TOKEN:-}" ]; then
    echo "  ✅ GITHUB_TOKEN environment variable is set"
elif [ -n "${GH_TOKEN:-}" ]; then
    echo "  ✅ GH_TOKEN environment variable is set"
else
    echo "  ⚠️  No GitHub token found in environment"
    echo "     Set GITHUB_TOKEN or GH_TOKEN for API operations"
    echo "     Or authenticate with: gh auth login"
fi

# Summary
echo ""
echo "=================================="
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ Setup incomplete — $ERRORS critical error(s) found${NC}"
    echo "   Fix the errors above before proceeding"
    exit 1
else
    echo -e "${GREEN}✅ Setup complete — all critical dependencies available${NC}"
    echo "   Warnings are non-blocking; the agent will use fallback methods"
fi

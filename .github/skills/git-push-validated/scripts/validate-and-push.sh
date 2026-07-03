#!/bin/bash
# validate-and-push.sh
# Safely commit and push with validation checks

set -e

COMMIT_MSG="${1:-Update code}"
PROJECT_ROOT="$(git rev-parse --show-toplevel)"

echo "📋 Validating before push..."

# 1. Check git status
echo ""
echo "🔍 Git Status:"
git status

# 2. Check for problematic files
echo ""
echo "🚨 Checking for problematic files..."
PROBLEMS=0

if [[ -f "$PROJECT_ROOT/uv.lock" ]]; then
    echo "  ⚠️  Found uv.lock (can break cloud deployments)"
    echo "    → Remove? (yes/no): "
    read -r REMOVE_UV
    if [[ "$REMOVE_UV" == "yes" ]]; then
        rm "$PROJECT_ROOT/uv.lock"
        git add "$PROJECT_ROOT/uv.lock"
        echo "    ✓ Removed uv.lock"
    fi
fi

if [[ -f "$PROJECT_ROOT/package-lock.json" ]]; then
    echo "  ⚠️  Found package-lock.json"
    echo "    → This should match your dependencies (for reference only)"
fi

# 3. Verify requirements.txt exists
if [[ ! -f "$PROJECT_ROOT/requirements.txt" ]] && [[ -f "$PROJECT_ROOT/pyproject.toml" ]]; then
    echo "  ℹ️  pyproject.toml found but no requirements.txt"
    echo "    Tip: pip freeze > requirements.txt"
fi

# 4. Stage changes
echo ""
echo "📦 Staging changes..."
git add -A
echo "  ✓ All changes staged"

# 5. Commit
echo ""
echo "💾 Committing: '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG" || echo "  ℹ️  No changes to commit"

# 6. Verify remote
echo ""
echo "🌐 Verifying remote..."
git remote -v

# 7. Push
echo ""
echo "🚀 Pushing to remote..."
git push

echo ""
echo "✅ Push complete!"
echo "   → GitHub: $(git config --get remote.origin.url)"
echo "   → Branch: $(git branch --show-current)"
echo "   → Commit: $(git rev-parse --short HEAD)"

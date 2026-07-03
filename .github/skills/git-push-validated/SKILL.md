---
name: git-push-validated
description: 'Validate code changes and safely push to GitHub. Use when: committing code changes, preparing for deployment, cleaning up before push (e.g., removing lock files, checking dependencies).'
argument-hint: 'Optional: commit message (e.g., "Add new feature")'
---

# Git Push with Validation

Safely push code to GitHub while catching common deployment issues before they reach production.

## When to Use

- After editing code and ready to push to GitHub
- Before Streamlit Cloud or other deployments
- When you need to clean up build artifacts or lock files
- When verifying dependencies are correct

## Common Issues This Prevents

✓ Lock file conflicts (`uv.lock`, `package-lock.json`)  
✓ Missing or corrupted `requirements.txt`  
✓ Unintended files getting committed  
✓ Incomplete commit messages

## Procedure

### 1. Review Changes
```bash
git status
git diff --stat
```

### 2. Check for Problematic Files
Look for:
- `*.lock` files (remove if not needed)
- `__pycache__/`, `.venv/` (should be in `.gitignore`)
- Temporary or IDE files

See [Pre-Push Checklist](./references/checklist.md)

### 3. Clean Up (if needed)
```bash
# Remove problematic lock files
rm uv.lock          # if using pip instead of uv
rm package-lock.json # if using npm

# Or unstage specific files
git reset <file>
```

### 4. Stage and Commit
```bash
git add -A
git commit -m "<meaningful message>"
```

### 5. Verify Remote Connection
```bash
git remote -v
```

### 6. Push
```bash
git push
```

### 7. Verify Success
- Check GitHub to confirm new commit appears
- For Streamlit Cloud: verify deployment started in share.streamlit.io dashboard

## Quick Command

Use the [validation script](./scripts/validate-and-push.sh) for automated checks:
```bash
bash .github/skills/git-push-validated/scripts/validate-and-push.sh "Your commit message"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `fatal: pathspec did not match` | Check file exists: `git status` |
| `Permission denied` | Check remote URL: `git remote -v` (use HTTPS or configure SSH) |
| Streamlit fails to deploy | Check `requirements.txt` is up-to-date and lock files removed |
| Large file rejection | Use `.gitignore` to exclude heavy files (see [checklist](./references/checklist.md)) |

# Pre-Push Checklist

Before pushing to GitHub, review these items:

## Files to Check

- [ ] `.gitignore` is up-to-date
  - [ ] `.venv/` or `venv/` is excluded
  - [ ] `__pycache__/` is excluded
  - [ ] `node_modules/` is excluded (for Node.js projects)
  - [ ] `.DS_Store` and IDE files are excluded

- [ ] Lock files are handled correctly
  - [ ] `uv.lock` — Remove if using pip instead of uv
  - [ ] `package-lock.json` — Keep if using npm
  - [ ] `poetry.lock` — Keep if using Poetry
  - [ ] `Pipfile.lock` — Keep if using Pipenv

- [ ] Dependency files are current
  - [ ] `requirements.txt` is up-to-date (if Python)
  - [ ] `package.json` is up-to-date (if Node.js)
  - [ ] `pyproject.toml` matches dependencies (if Python)

- [ ] Secrets and sensitive files
  - [ ] No API keys or tokens in code
  - [ ] No database passwords
  - [ ] No `.env` files (should be in `.gitignore`)

## Commit Message

- [ ] Message is clear and descriptive
- [ ] Examples:
  - ✅ `"Fix matplotlib import issue for Streamlit Cloud"`
  - ✅ `"Remove uv.lock to resolve deployment errors"`
  - ❌ `"update"` (too vague)
  - ❌ `"fix bug"` (which bug?)

## Remote

- [ ] Correct repository URL
  - Run: `git remote -v`
  - Should show GitHub URL

- [ ] Branch is correct
  - Run: `git branch`
  - Verify you're on `main` or intended branch

## Post-Push (Optional)

- [ ] Verify new commit on GitHub
- [ ] Check Streamlit Cloud deployment (if applicable)
- [ ] Confirm CI/CD workflows triggered (if using Actions)

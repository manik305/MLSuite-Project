# MLSuite Git Management Guide

This document summarizes the Git commands used to stabilize the repository, manage branches, and synchronize the production-hardened code from `dev` to `main`.

## 1. Repository Cleanup & Stabilization
To ensure sensitive data and local artifacts (like `node_modules`, `nanodb.json`, and `__pycache__`) are not tracked, even if they were added previously.

```bash
# 1. Remove everything from the git index (but keep files on disk)
git rm -r --cached .

# 2. Re-add everything (this will now respect the .gitignore)
git add .

# 3. Commit the cleaned state
git commit -m "Cleanup repository: enforcing .gitignore and removing sensitive/local files"
```

## 2. Managing the Development Branch (`dev`)
Commands used to update and push the latest hardened code to the development branch.

```bash
# Check current status and branch
git status
git branch

# Push the dev branch to GitHub
git push origin dev
```

## 3. Synchronizing to Production Branch (`main`)
Commands used to ensure the `main` branch is exactly identical to the verified `dev` branch.

```bash
# 1. Switch to the main branch
git checkout main

# 2. Reset the local main branch to match the dev branch exactly
# WARNING: This overwrites local changes on main with dev's history
git reset --hard dev

# 3. Synchronize with the remote main branch
# If histories have diverged, a force push is required
git push origin main --force-with-lease
```

## 4. Helpful Maintenance Commands
Other commands used during the hardening process.

```bash
# Check all available branches (local and remote)
git branch -a

# View the last few commits to verify synchronization
git log -n 5

# Restore specific files from another branch without switching
git checkout dev -- .
```

---
*Note: These commands were used to transition the MLSuite project from a local-only state to a production-ready repository on GitHub.*

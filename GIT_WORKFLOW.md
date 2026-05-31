# Git Workflow Guide

Quick guide for cloning the repository, creating a development branch, and submitting pull requests.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AliHaghighat1/fastapi_project.git
cd fastapi_project
```

### 2. Create and Switch to `initial_dev` Branch

```bash
# Create your dev branch from main
git checkout -b <put your initials>_dev
Example: git checkout -b AH_dev 

# Verify you're on the branch
git branch
```

## Development Workflow

### Working on Your Branch

```bash
# Make your changes to files

# Stage your changes
git add .

# Commit your changes
git commit -m "Your commit message"

# Push to initial_dev branch
git push origin initial_dev
```

### Creating a Pull Request (PR)

Once you're ready to merge your changes to `main`:

```bash
# Push your branch if not already pushed
git push origin initial_dev

# Then go to GitHub and:
# 1. Navigate to https://github.com/AliHaghighat1/fastapi_project
# 2. Click "New Pull Request"
# 3. Select base: main, compare: initial_dev
# 4. Add title and description
# 5. Click "Create Pull Request"
```

## Common Commands

```bash
# Check current branch
git branch

# Switch between branches
git checkout initial_dev
git checkout main

# Pull latest changes from remote
git pull origin initial_dev

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what changed
git status
```

## Tips

- Always pull latest changes before starting work: `git pull origin initial_dev`
- Keep commits focused and descriptive
- Push regularly to avoid losing work
- Review your changes before committing: `git diff`

## Need Help?

- Check git status: `git status`
- View branch info: `git branch -v`
- See remote URLs: `git remote -v`

# Git Workflow

This project uses a simple team workflow with one production branch, one shared test branch and one personal branch per developer.

## Branches

| Branch type | Example | Purpose |
|---|---|---|
| Production | `main` | Stable code only. Production server deploys from here. |
| Shared test | `SMS_dev` or `develop` | Code that is ready for team testing. Test server deploys from here. |
| Developer branch | `ali_branch`, `sara_branch`, `sms_branch` | Each developer works in their own branch. |

## Daily developer workflow

Start from the latest shared branch:

```bash
git checkout SMS_dev
git pull origin SMS_dev
git checkout -b your_branch
```

Work locally, then commit:

```bash
git status
git add .
git commit -m "Describe your change"
git push origin your_branch
```

Open a pull request from `your_branch` into `SMS_dev`.

After the test environment is verified, open a pull request from `SMS_dev` into `main`.

## Server deployment rule

- production folder: only `main`
- shared test folder: `SMS_dev` or the agreed test branch
- personal developer folders: each developer's own branch

This avoids overwriting another developer's work on the server.

## Useful commands

Check current branch:

```bash
git branch --show-current
```

Fetch all remote branches:

```bash
git fetch --all --prune
```

Switch branch:

```bash
git checkout branch_name
```

Update current branch:

```bash
git pull origin branch_name
```

Show changed files:

```bash
git status
```

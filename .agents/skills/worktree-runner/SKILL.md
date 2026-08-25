---
name: worktree-runner
description: Use when starting parallel feature work, creating or using git worktrees, running local previews from multiple branches, or avoiding local port conflicts in this repo.
---

# Worktree Runner

## Mission

Keep independent DuckRadar work isolated so branches, local previews, and browser sessions do not collide.

## Workflow

1. Check `git status --short` and preserve user changes before creating or switching worktrees.
2. Detect whether the current checkout is already a linked worktree.
3. For independent feature work, create or use a repo-local `.worktrees/<branch>` checkout after confirming `.worktrees/` is ignored.
4. Use one dedicated branch per worktree.
5. Before starting local preview servers, assign a distinct port and check that it is free.
6. Pass the port on the command line instead of editing committed config.
7. Record important worktree paths, branches, ports, and running services in the handoff.

## Port Guidance

The main static site preview defaults to `4173`:

```bash
python3 -m http.server 4173 --directory site
```

Parallel worktrees should use a different free port. Check availability first:

```bash
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN
```

Then start the preview:

```bash
python3 -m http.server "$PORT" --directory site
```

## Guardrails

- Do not create nested worktrees.
- Do not commit `.worktrees/`.
- Do not run two active branches on the same preview port.
- Do not edit committed config just to reserve a personal local port.
- Stop or identify stale local servers before blaming site behavior.
- Preserve user changes in the main checkout and other worktrees.

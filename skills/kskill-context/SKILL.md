---
name: kskill-context
description: >
  On-demand clones of configured GitHub repos under context/, with a
  code-only Graphify graph per repo. Triggers: context repo, sync,
  index, alvs-feedlot-campo, kskill-context. Slash /kskill-context.
tools:
  - query_graph
  - get_neighbors
  - get_node
  - shortest_path
  - Bash
---

# kskill-context

Clones and indexes the repos listed in `context/repos.json`. The
clones and their graphs stay gitignored. Session start does not run
these scripts. LangGraph, when it exists, calls these scripts and
does not clone on its own.

## Do this

1. **Which repos?** `skills/kskill-context/bin/list`
2. **Bring one up to date and index it:**

   ```
   skills/kskill-context/bin/sync NAME
   skills/kskill-context/bin/sync          # every repo in the registry
   skills/kskill-context/bin/index NAME    # graph only; clone must exist
   ```

   `sync` clones on the configured branch when the checkout is
   missing. When it exists, `sync` fetches and fast-forwards. A dirty
   tree or a non-fast-forward stops the script.
3. **Query the context graph** with Graphify MCP `project_path` set to
   `context/.graphs/NAME` (the directory that contains
   `graphify-out/graph.json`). The harness graph stays the default
   server graph.
4. **Repair work** happens in a git worktree of `context/NAME`, not
   by committing inside the harness.

## Return shape

```
topic: <list | sync | index>
repo: <name | all>
graph: present | absent
path: context/.graphs/<name>
```

## Do not

- Run these scripts from session start.
- Commit `context/<name>` or `context/.graphs/`.
- Run `graphify add <url>`.
- Point the harness `graphify extract .` at `context/` (`.graphifyignore` keeps it out).

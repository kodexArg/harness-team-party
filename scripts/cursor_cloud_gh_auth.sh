#!/usr/bin/env bash
# Prefer an operator PAT for `gh` Issues/PRs/merges on Cursor Cloud.
#
# Cursor injects a GitHub App installation token (`ghs_…`) that can clone and
# push. That token cannot read Issues, cannot bypass the `main` ruleset, and
# must not be the merge credential. A dashboard secret named `GH_TOKEN`
# collides with that injection.
#
# The operator PAT is `GITHUB_PAT`. Cursor may also inject the same value under
# a repo-named secret — `GH_PROJECT_PAT` by default; rename it to match this
# repo at instantiation ([[CLONE]]). Either name that looks like `ghp_` /
# `github_pat_` is exported as `GH_TOKEN`. An injected `ghs_` `GH_TOKEN` is
# unset so `gh` can fall back to `~/.config/gh/hosts.yml` for git.
#
# Source this file (do not exec it) so the exports reach the session:
#     . scripts/cursor_cloud_gh_auth.sh
# Never prints secret values. Safe to source when neither var is set.

_cursor_cloud_operator_pat() {
  case "${GITHUB_PAT-}" in
    ghp_*|github_pat_*)
      printf '%s' "$GITHUB_PAT"
      return 0
      ;;
  esac
  case "${GH_PROJECT_PAT-}" in
    ghp_*|github_pat_*)
      printf '%s' "$GH_PROJECT_PAT"
      return 0
      ;;
  esac
  return 1
}

_cursor_cloud_gh_auth() {
  local pat
  if pat="$(_cursor_cloud_operator_pat)"; then
    GH_TOKEN="$pat"
    export GH_TOKEN
    return 0
  fi

  case "${GH_TOKEN-}" in
    ghs_*)
      unset GH_TOKEN
      return 0
      ;;
  esac

  if [ -n "${GH_TOKEN-}" ] && command -v gh >/dev/null 2>&1; then
    if ! gh auth status >/dev/null 2>&1; then
      unset GH_TOKEN
    fi
  fi
}

_cursor_cloud_gh_auth
unset -f _cursor_cloud_gh_auth
unset -f _cursor_cloud_operator_pat

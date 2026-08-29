---
name: hb-sk-test-runner
title: Test runner for this project's service — knowledge contract
type: skill
status: active
version: v0.1.4
tags: [skill, test-runner, trickster]
description: >
  Writes tests for this project's service with its test runner:
  parametrize, isolation, real dependencies at the owned boundary, no
  tautological mocks, and no live credentials in the default slice.
  Load for red TDD tests, post-Paladin tests, fixtures, or shadow-test
  repair — even if unnamed. Owner: The Trickster (hb-ag-test).
applies_when:
  - When writing or fixing service tests under {{service tree}}
  - When a TDD entry lists failing tests that must actually run red, then green
  - When a test would mock the unit under test, skip execution, or call a live marker
related_adrs:
  - adr-02-stack
---

# hb-sk-test-runner

Knowledge contract for **The Trickster**. Teach how this tree's {{test runner}} tests are written. Craft: parametrize, isolation, mock at the I/O boundary.

## Load

1. Read either the framework-bound TDD entry (`hb-sk-tdd`) or The Paladin's post-implementation handoff, then a neighbor test file in the same area.
2. Run from the service tree with a **clean** environment, the way [[SERVICES]] and the service's own test configuration describe.
3. Slice only: run the test files for the area under change. Never substitute the toolchain.

## Why a trap has to run

A file that never executes is green by absence. Two people then disagree about the same commit with no visible reason. Shadow tests are that hole in costume: tautologies, coverage theater, a mock that returns `X` so you can assert `X`, a UI posed as a unit. The product wears the face; the trap has to trip.

## This project's test contract

| Knob | Here |
|---|---|
| Runner | `{{test runner}}`, run from `{{service tree}}`. Pins in [[REQUIREMENTS]]. |
| Files | The project's test-file convention, next to the code under test — not a parallel shadow tree. |
| DB | Framework-bound tests use a real database, not a mocked one. Pure Paladin logic stays database-free and tests real values at its function boundary. |
| Live | Live-credential markers stay deselected in the default slice. Do not invent a live marker without a guard test. Do not invent test plugins. |

Session-scoped fixtures are rare. Prefer function-scoped fixtures so one test's state cannot poison the next.

## Parametrize the branches

One behavior, many inputs — one test, parametrized. A copy-pasted pair of near-identical tests drifts, and the un-copied case is the one that ships the defect. Cover the sad path in the same class: auth refusals, conflict codes, validation failures. A suite that only asserts the happy path is a welcome mat.

## Isolation and mocks

The unit under test stays real: the handler, the domain service, the guard. Mock the network and external systems, not the unit you claim to trap. A stub that returns `ok` followed by `assert result == "ok"` is costume. Error injection is a stub that raises or returns a closed failure, then an assert on the **product** outcome (status, body code, audit row) — not on `mock.assert_called_once()` alone.

Do not call live external services from the default slice. A bare test run must mean one thing on every machine.

## Surface and harness (not this file's specialty)

- Surface unit tests live with the surface tree and run with its toolchain. Load `hb-sk-surface-framework` when the trap is a surface test.
- Repo-root `tests/test_*.py` must have an `if __name__ == "__main__"` runner (`tests/test_every_test_file_runs.py`). A harness file that defines tests and exits 0 without running them is a shadow test.

## Do not

- Implement the model / handler (Dwarf), pure business rule (Paladin), or component (Elf).
- Write [[INTERFACES]] or screen copy in the interface language.
- Run the live markers in the default slice, or treat browser smoke as CI.
- Load Cleric / Dwarf / Wizard / Inquisitor / Bard skills. TDD entries are `hb-sk-tdd`. `hb-sk-surface-framework` is allowed for surface tests.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the test runner's name).
See [[ONBOARDING]] and [[CLONE]].

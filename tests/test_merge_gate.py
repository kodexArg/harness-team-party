from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHLISTS_MODULE = ROOT / "scripts" / "guardian_watchlists.py"
MERGE_GATE = ROOT / "scripts" / "check_merge_gate.py"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_watchlists_no_third_copy() -> None:
    """No-third-copy discipline: the gate imports scripts/guardian_watchlists.py."""
    lists = load_module(WATCHLISTS_MODULE, "guardian_watchlists")
    gate = load_module(MERGE_GATE, "check_merge_gate")
    loaded = gate.load_watchlists()
    if loaded != lists.WATCHLISTS:
        fail("check_merge_gate.load_watchlists() diverged from guardian_watchlists.WATCHLISTS")
    ok("check_merge_gate imports guardian_watchlists.WATCHLISTS")


def test_guardian_mapping() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()

    cases = {
        "docs/INTERFACES.md": {"kbot-api"},
        "docs/contracts/contract-billing.md": {"kbot-api"},
        ".github/workflows/ci.yml": {"kbot-prd", "kbot-adr"},
        "docs/PRD.md": {"kbot-prd"},
        "adrs/adr-02-stack.md": {"kbot-adr"},
        "service/app/handlers.py": set(),
        "surface/src/lib/x.ts": set(),
    }
    for rel, expected in cases.items():
        actual = set(gate.guardians_for(rel, watchlists))
        if actual != expected:
            fail(f"guardians_for({rel!r}) = {actual}, expected {expected}")
    ok(f"guardian mapping matches the plan's {len(cases)} fixture files")


def test_required_guardians_groups_by_file() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_guardians(
        ["docs/INTERFACES.md", "docs/contracts/contract-billing.md", "surface/src/lib/x.ts"],
        watchlists,
    )
    if "kbot-api" not in required:
        fail(f"expected kbot-api in required guardians, got {required}")
    if set(required["kbot-api"]) != {"docs/INTERFACES.md", "docs/contracts/contract-billing.md"}:
        fail(f"unexpected file grouping for kbot-api: {required['kbot-api']}")
    ok("required_guardians groups triggering files per guardian")


def test_verdict_parsing_pass() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    body = "Some PR description.\n\nGuardian-Verdict: kbot-api: pass\n"
    recorded = gate.recorded_verdicts(body)
    if "kbot-api" not in recorded:
        fail(f"expected kbot-api recorded, got {recorded}")
    ok("a 'Guardian-Verdict: ...: pass' line is recorded")


def test_verdict_parsing_accepts_the_guardians_own_vocabulary() -> None:
    """The accepted set must stay identical to the vocabulary the guardians
    can actually return, or every auto-opened PR fails this gate."""
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for status in ("pass", "clear", "compliant", "valid", "ok", "drift"):
        body = f"Guardian-Verdict: kbot-adr: {status}\n"
        if "kbot-adr" not in gate.recorded_verdicts(body):
            fail(f"a passing verdict spelled {status!r} must be recorded")
    ok("all six passing statuses are recorded")


def test_plan_verdict_satisfies_the_matching_guardian() -> None:
    """A Plan-Verdict line for an SSOT records the guardian that SSOT answers
    to — that mapping is what lets a run whose doctrine was settled at plan time open a mergeable PR."""
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for ssot, guardian in (("prd", "kbot-prd"), ("adr", "kbot-adr"), ("api", "kbot-api")):
        recorded = gate.recorded_verdicts(f"Plan-Verdict: {ssot}: ok\n")
        if guardian not in recorded:
            fail(f"Plan-Verdict: {ssot} must record {guardian}, got {recorded}")
    ok("each Plan-Verdict SSOT records its corresponding guardian")


def test_plan_verdict_shares_the_guardian_status_vocabulary() -> None:
    """One passing set exists in this repo, not two: the plan-time line is
    accepted for exactly the statuses a guardian's line is, and rejected for
    exactly the ones the guardian status vocabulary makes blocking."""
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for status in ("pass", "clear", "compliant", "valid", "ok", "drift"):
        if not gate.recorded_verdicts(f"Plan-Verdict: adr: {status}\n"):
            fail(f"a passing plan verdict spelled {status!r} must be recorded")
    for status in ("violation", "defect", "danger", "needs-new-adr"):
        if gate.recorded_verdicts(f"Plan-Verdict: adr: {status}\n"):
            fail(f"a blocking plan verdict spelled {status!r} must NOT be recorded")
    ok("the plan verdict line shares the guardians' passing and blocking vocabulary")


def test_plan_verdict_rejects_an_unknown_ssot_and_a_guardian_name() -> None:
    """The SSOT key is closed. A line spelling a guardian's agent name under the
    Plan- prefix is not a shorthand — it is the overstatement [[GITHUB]]
    forbids, and it records nothing."""
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for body in (
        "Plan-Verdict: docs: ok\n",
        "Plan-Verdict: kbot-api: valid\n",
        "Plan-Verdict: api valid\n",
    ):
        if gate.recorded_verdicts(body):
            fail(f"must record nothing: {body!r}")
    ok("an unknown SSOT, a guardian name, and a malformed plan-verdict line record nothing")


def test_verdict_parsing_empty_or_none_body() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    if gate.recorded_verdicts(None):
        fail("None body must record nothing")
    if gate.recorded_verdicts(""):
        fail("empty body must record nothing")
    ok("None/empty PR body records no verdicts")


def test_verdict_parsing_rejects_violation_and_malformed() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    body_violation = "Guardian-Verdict: kbot-api: violation\n"
    if gate.recorded_verdicts(body_violation):
        fail("a 'violation' verdict line must not count as a recorded pass")

    body_malformed = "kbot-api passed the check\n"
    if gate.recorded_verdicts(body_malformed):
        fail("free prose must not be parsed as a recorded verdict")
    ok("'violation' and malformed lines are never recorded as a pass")


def test_end_to_end_no_watched_files_passes_trivially() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_guardians(["surface/src/lib/x.ts"], watchlists)
    if required:
        fail(f"expected zero required guardians, got {required}")
    ok("no watched files -> zero required guardians (trivial pass)")


def test_end_to_end_missing_verdict_is_detected() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_guardians(["docs/INTERFACES.md"], watchlists)
    recorded = gate.recorded_verdicts("no verdict lines here")
    missing = sorted(set(required) - recorded)
    if missing != ["kbot-api"]:
        fail(f"expected kbot-api missing, got {missing}")
    ok("a changed watched file with no recorded verdict is flagged missing")


def test_end_to_end_recorded_verdict_satisfies_requirement() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_guardians(["docs/INTERFACES.md"], watchlists)
    recorded = gate.recorded_verdicts("Guardian-Verdict: kbot-api: pass\n")
    missing = sorted(set(required) - recorded)
    if missing:
        fail(f"expected no missing guardians, got {missing}")
    ok("a recorded pass for the exact required guardian satisfies the gate")


def test_verdict_parsing_rejects_unavailable() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for guardian in ("kbot-prd", "kbot-adr", "kbot-api"):
        body = f"Guardian-Verdict: {guardian}: unavailable\n"
        if gate.recorded_verdicts(body):
            fail(f"an 'unavailable' status for {guardian} must not count as a recorded pass")
    for ssot in ("prd", "adr", "api"):
        body = f"Plan-Verdict: {ssot}: unavailable\n"
        if gate.recorded_verdicts(body):
            fail(f"an 'unavailable' status for {ssot} must not count as a recorded pass")
    ok("'unavailable' is not a verdict and is never recorded as a pass")


def main() -> int:
    tests = [
        test_watchlists_no_third_copy,
        test_guardian_mapping,
        test_required_guardians_groups_by_file,
        test_verdict_parsing_pass,
        test_verdict_parsing_accepts_the_guardians_own_vocabulary,
        test_plan_verdict_satisfies_the_matching_guardian,
        test_plan_verdict_shares_the_guardian_status_vocabulary,
        test_plan_verdict_rejects_an_unknown_ssot_and_a_guardian_name,
        test_verdict_parsing_empty_or_none_body,
        test_verdict_parsing_rejects_violation_and_malformed,
        test_verdict_parsing_rejects_unavailable,
        test_end_to_end_no_watched_files_passes_trivially,
        test_end_to_end_missing_verdict_is_detected,
        test_end_to_end_recorded_verdict_satisfies_requirement,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
        except AssertionError:
            failed += 1
        except Exception as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {len(tests)} test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

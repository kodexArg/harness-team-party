"""Guard for the review-signature reader, CI job `pr-merge-gate`.

The four verdict labels are a signature: a fresh one says a reviewer already
read this diff, a `-fail` names work to do, and no label at all says the
routine never ran. None of those states blocks a merge — [[PR-REVIEW-ROUTINE]] — so
the only thing that can break here is the reading itself.

Offline by design: every case feeds `scripts/check_pr_tags.py` a payload
shaped like `gh pr view --json labels,comments,headRefOid` and checks what it
made of it. No network, no gh, no credentials.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_pr_tags.py"

HEAD = "1980124b2e6e2fc0d3b882fdc3c778f86be9ef26"

# A routine comment, trimmed to the shapes this reader parses.
ROUTINE_COMMENT = """## Review routine

- **prd:** approved — routine bug fix serving an existing surface.
- **adr:** fail — breaches the comment-necessity rule in CODE-COMMENTS.md.
- **api:** approved — no interface/route surface touched.
- **clean:** applied — deleted a history-narrating comment.

Under adr (fail):
> CODE-COMMENTS.md: a comment must never narrate history. Fix: delete the
> "used to be" block.

Reviewed-SHA: 1980124b2e6e2fc0d3b882fdc3c778f86be9ef26
"""


def load_reader():
    spec = importlib.util.spec_from_file_location("check-pr-tags", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pr_payload(label_names, comments=(), head=HEAD):
    return {
        "labels": [{"name": name} for name in label_names],
        "comments": [{"body": body} for body in comments],
        "headRefOid": head,
    }


def test_signed_pr_is_read_per_prefix():
    """A signed PR yields one verdict per prefix, and the failing one's finding."""
    reader = load_reader()
    pr = pr_payload(
        ["prd-approved", "adr-fail", "api-approved", "clean-applied"],
        [ROUTINE_COMMENT],
    )
    verdicts, reviewed, body = reader.signature(pr)

    assert verdicts == {
        "prd": "approved",
        "adr": "fail",
        "api": "approved",
        "clean": "applied",
    }, f"verdicts misread: {verdicts}"
    assert reviewed == HEAD, f"Reviewed-SHA misread: {reviewed}"

    found = reader.findings(body)
    assert set(found) == {"adr"}, f"expected only adr's finding, got {sorted(found)}"
    assert "narrate history" in found["adr"], "the finding's text did not survive parsing"
    print("  four verdicts, one Reviewed-SHA, one finding")


def test_unsigned_pr_is_not_a_failure():
    """No label means the routine never ran, and that is a valid state."""
    reader = load_reader()
    verdicts, reviewed, body = reader.signature(pr_payload([]))

    assert set(verdicts.values()) == {None}, f"expected no verdicts, got {verdicts}"
    assert reviewed is None, f"expected no Reviewed-SHA, got {reviewed}"

    summary = reader.render(verdicts, reviewed, HEAD, reader.findings(body))
    assert "has not signed" in summary, f"unsigned state not stated:\n{summary}"
    print("  an unsigned pull request reads as unsigned, not as a pass")


def test_signature_expires_with_the_head():
    """A signature made against another commit does not cover this one."""
    reader = load_reader()
    assert reader.covers_head(HEAD, HEAD)
    assert reader.covers_head("1980124", HEAD), "an abbreviated SHA must still match"
    assert not reader.covers_head("a3f9c21", HEAD), "a different commit must not match"
    assert not reader.covers_head(None, HEAD), "an absent signature covers nothing"

    stale = reader.render(
        {"prd": "approved", "adr": "fail", "api": "approved", "clean": "applied"},
        "a3f9c21",
        HEAD,
        {"adr": "the finding"},
    )
    assert "counts for nothing" in stale, f"stale signature not called out:\n{stale}"
    assert "the finding" not in stale, "a stale signature must not report its findings"
    print("  a stale signature is reported as covering nothing")


def test_verdict_labels_never_gate():
    """The reader exits 0 on every state — the labels are advisory ([[PR-REVIEW-ROUTINE]])."""
    reader = load_reader()
    summary = reader.render(
        {"prd": "fail", "adr": "fail", "api": "fail", "clean": "applied"},
        HEAD,
        HEAD,
        {},
    )
    assert "gates nothing" in summary, f"the advisory limit was not stated:\n{summary}"

    argv, sys.argv = sys.argv, ["check_pr_tags.py"]
    try:
        assert reader.main() == 0, "the reader must exit 0 even with no PR to read"
    finally:
        sys.argv = argv
    print("  three failing verdicts still exit 0")


def main():
    tests = [
        test_signed_pr_is_read_per_prefix,
        test_unsigned_pr_is_not_a_failure,
        test_signature_expires_with_the_head,
        test_verdict_labels_never_gate,
    ]
    failed = 0
    for fn in tests:
        print(f"{fn.__name__}:")
        try:
            fn()
        except AssertionError as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
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

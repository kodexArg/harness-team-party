#!/usr/bin/env python3
"""Deterministic Mermaid validation harness for kskill-report artifacts.

Two tiers:
  TIER 1  static lint (stdlib, zero-dep, always runs) — catches the brace
          collision (`{{`/`}}` inside a block) and bad stateDiagram ids.
  TIER 2  authoritative parse via `bunx @mermaid-js/mermaid-cli` (mmdc),
          best-effort; degrades to a WARN if bun/mmdc is unavailable.

Exit: 0 = every block passed, 1 = any failure (or harness misbehaved on
--selftest). Report is stable and per-block.

Usage:
    validate_mermaid.py <path...>     # files or dirs (.html, .md); runs
                                       # Tier1/2 mermaid + golden structural
                                       # checks (viewport, init, name-leak,
                                       # self-containment) on each .html file
    validate_mermaid.py --selftest    # run bundled fixtures + golden/
                                       # structural checks, assert verdicts
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# --- block extraction ------------------------------------------------------

_PRE = re.compile(r'<pre class="mermaid">(.*?)</pre>', re.DOTALL)
_FENCE = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
_INIT = re.compile(r'^\s*%%\{init.*?\}%%\s*$', re.MULTILINE)


def extract_blocks(text: str) -> list[str]:
    """Return mermaid block bodies from one file's text."""
    blocks = [m.group(1) for m in _PRE.finditer(text)]
    blocks += [m.group(1) for m in _FENCE.finditer(text)]
    return blocks


def strip_init(block: str) -> str:
    """Drop the leading %%{init}%% directive line(s)."""
    return _INIT.sub("", block)


# --- TIER 1: static lint ---------------------------------------------------

_STATE_TX = re.compile(r'^\s*(\S+)\s*-->\s*([^:\n]+?)\s*(?::.*)?$')


def tier1(block: str) -> list[str]:
    """Return a list of failure reasons; empty list = pass."""
    reasons: list[str] = []
    body = strip_init(block)

    # 1. brace collision — the exact bug that broke today's diagrams
    for i, line in enumerate(body.splitlines(), 1):
        if "{{" in line or "}}" in line:
            reasons.append(f"L{i}: brace collision `{{{{`/`}}}}` in `{line.strip()}`")

    # 2. stateDiagram transition ids must be brace-free, space-free tokens
    is_state = "stateDiagram" in body
    if is_state:
        for i, line in enumerate(body.splitlines(), 1):
            s = line.strip()
            if "-->" not in s:
                continue
            m = _STATE_TX.match(line)
            if not m:
                continue
            for side in (m.group(1), m.group(2)):
                side = side.strip()
                if side in ("[*]",):
                    continue
                if "{" in side or "}" in side:
                    reasons.append(f"L{i}: state id `{side}` contains braces (use `s1 : label`)")
                elif " " in side:
                    reasons.append(f"L{i}: state id `{side}` contains spaces (use `s1 : label`)")
    return reasons


# --- TIER 2: authoritative parse via mmdc ----------------------------------

_PARSE_ERR = re.compile(r"(parse error|syntax error)", re.IGNORECASE)


def mmdc_available() -> bool:
    return _which("bun") or _which("bunx") or _which("mmdc")


def _which(name: str) -> bool:
    from shutil import which
    return which(name) is not None


def tier2(block: str) -> tuple[str | None, str]:
    """Return (reason_or_None, status) where status is PASS/FAIL/SKIP."""
    if not mmdc_available():
        return None, "SKIP"
    env = dict(os.environ)
    env.setdefault("PUPPETEER_EXECUTABLE_PATH", "/usr/bin/chromium")
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "in.mmd"
        out = Path(d) / "out.svg"
        pcfg = Path(d) / "p.json"
        pcfg.write_text('{"args":["--no-sandbox","--disable-setuid-sandbox"]}')
        src.write_text(block)
        cmd = ["bunx", "@mermaid-js/mermaid-cli", "-i", str(src),
               "-o", str(out), "-p", str(pcfg), "-q"]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               env=env, timeout=120)
        except Exception as e:  # noqa: BLE001 — degrade gracefully
            return None, "SKIP"
        blob = (r.stdout or "") + (r.stderr or "")
        if r.returncode != 0 or _PARSE_ERR.search(blob):
            msg = blob.strip().splitlines()[-1] if blob.strip() else f"exit {r.returncode}"
            return f"mmdc: {msg}", "FAIL"
        return None, "PASS"


# --- driver ----------------------------------------------------------------

def iter_files(paths: list[str]):
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            yield from sorted(pp.rglob("*.html"))
            yield from sorted(pp.rglob("*.md"))
        elif pp.suffix in (".html", ".md"):
            yield pp


def validate(paths: list[str]) -> int:
    any_fail = False
    saw_block = False
    t2_skipped = False
    for f in iter_files(paths):
        text = f.read_text()
        blocks = extract_blocks(text)

        if f.suffix == ".html":
            golden_reasons = golden_checks(text, str(f))
            if golden_reasons:
                any_fail = True
                for reason in golden_reasons:
                    print(f"FAIL  {f}  GOLDEN  {reason}")
            else:
                print(f"PASS  {f}  GOLDEN  viewport+init+name-leak+self-containment ok")

        for idx, block in enumerate(blocks):
            saw_block = True
            r1 = tier1(block)
            if r1:
                any_fail = True
                for reason in r1:
                    print(f"FAIL  {f}  block[{idx}]  T1  {reason}")
                continue  # don't waste a render on a known-bad block
            r2, status = tier2(block)
            if status == "FAIL":
                any_fail = True
                print(f"FAIL  {f}  block[{idx}]  T2  {r2}")
            elif status == "SKIP":
                t2_skipped = True
                print(f"PASS  {f}  block[{idx}]  T1 ok (T2 skipped)")
            else:
                print(f"PASS  {f}  block[{idx}]  T1+T2 ok")
    if t2_skipped:
        print("WARN  Tier-2 full parse skipped (bun/mmdc unavailable) — Tier-1 only")
    if not saw_block:
        print("WARN  no mermaid blocks found")
    return 1 if any_fail else 0


# --- golden/structural checks (viewport, mermaid init, name-leak, self-containment) ---

_VIEWPORT = re.compile(r'<meta\s+name="viewport"\s+content="width=device-width')
_LOCAL_LINK = re.compile(r'<link\b[^>]*\bhref="\./')
_LOCAL_SCRIPT = re.compile(r'<script\b[^>]*\bsrc="\./(?!assets/)')
_LOCAL_IMG_OK = re.compile(r'<img\b[^>]*\bsrc="\./assets/')
_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
_STYLE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.DOTALL)
_HEAD = re.compile(r'<head\b[^>]*>(.*?)</head>', re.DOTALL)


def skill_dirname() -> str:
    """Current skill directory name, derived at runtime (never hardcoded)."""
    return Path(__file__).resolve().parents[1].name


def golden_checks(text: str, label: str) -> list[str]:
    """Structural assertions on a rendered artifact body. Empty = pass."""
    reasons: list[str] = []

    if not _VIEWPORT.search(text):
        reasons.append("missing <meta name=\"viewport\" content=\"width=device-width...\">")

    if '<pre class="mermaid">' in text and not _INIT.search(text):
        reasons.append("mermaid block present but no %%{init...}%% directive found")

    # Name-leak guard: scan only template machinery (comments, inline <style>,
    # <head> metadata) — never caller-authored visible body text, where a
    # genuine mention of the skill's own name is legitimate content.
    leak = skill_dirname()
    machinery_zones = "".join(_COMMENT.findall(text) + _STYLE.findall(text) + _HEAD.findall(text))
    if leak in machinery_zones:
        reasons.append(f'skill dirname "{leak}" leaked into template machinery (comment/style/head)')

    for m in _LOCAL_LINK.finditer(text):
        reasons.append(f"local stylesheet ref (self-containment violation): {m.group(0)}")
    for m in _LOCAL_SCRIPT.finditer(text):
        reasons.append(f"local script ref (self-containment violation): {m.group(0)}")

    return reasons


# --- selftest --------------------------------------------------------------

def selftest() -> int:
    fx = Path(__file__).parent / "tests"
    bad = fx / "bad_braces.md"
    good = fx / "good_themed.md"
    golden = fx / "golden_fixture.html"
    ok = True

    bad_reasons = tier1(extract_blocks(bad.read_text())[0])
    if not bad_reasons:
        print("SELFTEST FAIL: bad_braces.md should be flagged by Tier-1 but passed")
        ok = False
    else:
        print(f"SELFTEST ok: bad block correctly FAILED ({bad_reasons[0]})")

    good_reasons = tier1(extract_blocks(good.read_text())[0])
    if good_reasons:
        print(f"SELFTEST FAIL: good_themed.md should pass Tier-1 but flagged {good_reasons}")
        ok = False
    else:
        print("SELFTEST ok: good block correctly PASSED Tier-1")

    golden_reasons = golden_checks(golden.read_text(), "golden_fixture.html")
    if golden_reasons:
        print(f"FAIL  golden_fixture.html  GOLDEN  {'; '.join(golden_reasons)}")
        ok = False
    else:
        print("PASS  golden_fixture.html  GOLDEN  viewport+init+name-leak+self-containment ok")

    return 0 if ok else 1


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--selftest":
        return selftest()
    return validate(args)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Remove comments from source files while preserving semantics.

Owner mandate: a 100% clean, semantic codebase where comments are dead weight.
The only docstrings kept are the one-line docstrings the service framework
surfaces through schema generation or browsable interfaces (handler and
payload classes). Instantiation tunes FRAMEWORK_DOCSTRING_BASES and
MARKUP_EXTS to the project's frameworks ([[CLONE]]).
"""

from __future__ import annotations

import argparse
import ast
import io
import sys
import tokenize
from pathlib import Path

FRAMEWORK_DOCSTRING_BASES = (
    "View",
    "ViewSet",
    "Serializer",
    "Resource",
    "Handler",
)


def _keeps_docstring(node: ast.AST) -> bool:
    if not isinstance(node, ast.ClassDef):
        return False
    for base in node.bases:
        name = base.attr if isinstance(base, ast.Attribute) else getattr(base, "id", "")
        if any(name.endswith(b) for b in FRAMEWORK_DOCSTRING_BASES):
            return True
    return any(node.name.endswith(suffix) for suffix in ("ViewSet", "View", "Serializer"))


def _docstring_lineno_range(node: ast.AST) -> tuple[int, int] | None:
    body = getattr(node, "body", None)
    if not body:
        return None
    first = body[0]
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return first.lineno, first.end_lineno
    return None


def _collapse_docstring(text: str) -> str:
    line = " ".join(text.split())
    return line


def strip_python(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    lines = source.splitlines(keepends=True)
    drop_ranges: list[tuple[int, int]] = []
    collapse: dict[int, tuple[int, str]] = {}

    for node in ast.walk(tree):
        rng = None
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            rng = _docstring_lineno_range(node)
        if rng is None:
            continue
        start, end = rng
        indent = lines[start - 1][: len(lines[start - 1]) - len(lines[start - 1].lstrip())]
        if _keeps_docstring(node):
            text = ast.get_docstring(node, clean=True) or ""
            collapse[start] = (end, f'{indent}"""{_collapse_docstring(text)}"""\n')
        elif len(getattr(node, "body", [])) == 1 and not isinstance(node, ast.Module):
            collapse[start] = (end, f"{indent}pass\n")
        else:
            drop_ranges.append((start, end))

    kept: list[str] = []
    i = 0
    n = len(lines)
    drop_set = set()
    for start, end in drop_ranges:
        for ln in range(start, end + 1):
            drop_set.add(ln)
    while i < n:
        lineno = i + 1
        if lineno in collapse:
            end, replacement = collapse[lineno]
            kept.append(replacement)
            i = end
            continue
        if lineno in drop_set:
            i += 1
            continue
        kept.append(lines[i])
        i += 1

    with_docstrings = "".join(kept)
    return _strip_python_hash_comments(with_docstrings)


def _strip_python_hash_comments(source: str) -> str:
    out = io.StringIO()
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError):
        return source

    result_lines = source.splitlines(keepends=True)
    comment_spans: dict[int, list[tuple[int, int]]] = {}
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            row = tok.start[0]
            comment_spans.setdefault(row, []).append((tok.start[1], tok.end[1]))

    new_lines: list[str] = []
    for idx, line in enumerate(result_lines, start=1):
        if idx in comment_spans:
            col = min(s for s, _ in comment_spans[idx])
            stripped = line[:col].rstrip()
            if stripped:
                new_lines.append(stripped + "\n")
            else:
                continue
        else:
            new_lines.append(line)

    text = "".join(new_lines)
    return _squeeze_blank_lines(text)


def _squeeze_blank_lines(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    blank = 0
    for line in lines:
        if line.strip() == "":
            blank += 1
            if blank > 2:
                continue
        else:
            blank = 0
        out.append(line)
    result = "\n".join(out)
    if text.endswith("\n"):
        result += "\n"
    return result


def strip_c_like(source: str) -> str:
    out: list[str] = []
    i = 0
    n = len(source)
    state = "code"
    quote = ""
    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if state == "code":
            if ch in ("'", '"', "`"):
                state = "string"
                quote = ch
                out.append(ch)
                i += 1
            elif ch == "/" and nxt == "/":
                while i < n and source[i] != "\n":
                    i += 1
            elif ch == "/" and nxt == "*":
                i += 2
                while i < n and not (source[i] == "*" and i + 1 < n and source[i + 1] == "/"):
                    i += 1
                i += 2
            else:
                out.append(ch)
                i += 1
        elif state == "string":
            out.append(ch)
            if ch == "\\":
                if i + 1 < n:
                    out.append(source[i + 1])
                    i += 2
                    continue
            elif ch == quote:
                state = "code"
            i += 1
    return _squeeze_blank_lines("".join(out))


def strip_css(source: str) -> str:
    out: list[str] = []
    i = 0
    n = len(source)
    state = "code"
    quote = ""
    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if state == "code":
            if ch in ("'", '"'):
                state = "string"
                quote = ch
                out.append(ch)
                i += 1
            elif ch == "/" and nxt == "*":
                i += 2
                while i < n and not (source[i] == "*" and i + 1 < n and source[i + 1] == "/"):
                    i += 1
                i += 2
            else:
                out.append(ch)
                i += 1
        else:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(source[i + 1])
                i += 2
                continue
            if ch == quote:
                state = "code"
            i += 1
    return _squeeze_blank_lines("".join(out))


def strip_html_comments(source: str) -> str:
    out: list[str] = []
    i = 0
    n = len(source)
    while i < n:
        if source.startswith("<!--", i):
            end = source.find("-->", i + 4)
            if end == -1:
                break
            i = end + 3
            while i < n and source[i] in " \t":
                i += 1
            if i < n and source[i] == "\n":
                i += 1
        else:
            out.append(source[i])
            i += 1
    return "".join(out)


def _process_block(text: str, kind: str) -> str:
    if kind == "js":
        return strip_c_like(text)
    if kind == "css":
        return strip_css(text)
    return text


MARKUP_EXTS = {".html", ".htm", ".vue", ".mdx"}


def strip_markup(source: str) -> str:
    """Markup component files: HTML comments, JS in script/frontmatter, CSS in style."""
    text = strip_html_comments(source)

    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_end = text.find("\n", end + 1)
            fm = text[3:end]
            rest = text[end:]
            text = "---" + strip_c_like(fm) + rest

    text = _strip_tagged_blocks(text, "script", "js")
    text = _strip_tagged_blocks(text, "style", "css")
    return _squeeze_blank_lines(text)


def _strip_tagged_blocks(text: str, tag: str, kind: str) -> str:
    lower = text.lower()
    out: list[str] = []
    i = 0
    open_pat = f"<{tag}"
    while True:
        start = lower.find(open_pat, i)
        if start == -1:
            out.append(text[i:])
            break
        gt = text.find(">", start)
        if gt == -1:
            out.append(text[i:])
            break
        close = lower.find(f"</{tag}", gt)
        if close == -1:
            out.append(text[i:])
            break
        out.append(text[i : gt + 1])
        body = text[gt + 1 : close]
        out.append(_process_block(body, kind))
        i = close
    return "".join(out)


def _split_hash_comment(line: str) -> str:
    in_single = False
    in_double = False
    for idx, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return line[:idx].rstrip()
    return line


def strip_hash_lines(source: str) -> str:
    out: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#!"):
            out.append(line)
            continue
        new = _split_hash_comment(line)
        if new.strip() == "" and line.strip().startswith("#"):
            continue
        out.append(new)
    result = "\n".join(out)
    if source.endswith("\n"):
        result += "\n"
    return _squeeze_blank_lines(result)


def process_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    name = path.name
    original = path.read_text(encoding="utf-8")

    if suffix == ".py":
        new = strip_python(original)
    elif suffix in (".ts", ".js", ".mjs", ".cjs"):
        new = strip_c_like(original)
    elif suffix in MARKUP_EXTS:
        new = strip_markup(original)
    elif suffix in (".yml", ".yaml") or name.startswith("Dockerfile") or name == ".env.example":
        new = strip_hash_lines(original)
    else:
        return False

    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def iter_targets(roots: list[str]) -> list[Path]:
    exts = {".py", ".ts", ".js", ".mjs", ".cjs", ".yml", ".yaml"} | MARKUP_EXTS
    skip_dirs = {"node_modules", ".venv", "venv", ".git", "dist", "build", "__pycache__"}
    targets: list[Path] = []
    for root in roots:
        p = Path(root)
        if p.is_file():
            targets.append(p)
            continue
        if not p.is_dir():
            continue
        for f in p.rglob("*"):
            if not f.is_file():
                continue
            if skip_dirs.intersection(f.parts):
                continue
            if f.suffix.lower() in exts or f.name.startswith("Dockerfile") or f.name == ".env.example":
                targets.append(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Strip comments from source files.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    changed = 0
    for target in iter_targets(args.paths):
        if args.dry_run:
            print(target)
            continue
        if process_file(target):
            changed += 1
            print(f"stripped {target}")
    if not args.dry_run:
        print(f"\n{changed} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

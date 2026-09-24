#!/usr/bin/env python3
"""Fail-closed public-repository safety scan for tracked UTF-8 text files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess

ALLOW_MARKER = "public-safety: allow"
SAFE_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "users.noreply.github.com"}
SAFE_HOME_NAMES = {"user", "username", "example", "runner"}

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("LOCAL_HOME_POSIX", re.compile(r"/(?:Users|home)/(?P<name>[A-Za-z0-9._-]{2,})/")),
    ("LOCAL_HOME_WINDOWS", re.compile(r"(?i)\b[A-Z]:\\Users\\(?P<name>[^\\\s]+)\\")),
    ("PRIVATE_IPV4", re.compile(r"(?<!\d)(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})(?!\d)")),
    ("EMAIL", re.compile(r"(?i)\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("GITHUB_FINE_GRAINED_TOKEN", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("OPENAI_STYLE_TOKEN", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("PRIVATE_KEY_HEADER", re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----")),
    ("LOCAL_HOSTNAME", re.compile(r"(?i)\b[A-Za-z0-9][A-Za-z0-9.-]*\.local\b")),
]


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(p.decode("utf-8")) for p in proc.stdout.split(b"\0") if p]


def private_terms() -> list[str]:
    raw = os.environ.get("PUBLIC_SAFETY_PRIVATE_TERMS", "")
    terms: list[str] = []
    for line in raw.splitlines():
        term = line.strip()
        if len(term) >= 4 and not term.startswith("#"):
            terms.append(term)
    return terms


def scan_line(line: str, terms: list[str]) -> list[str]:
    if ALLOW_MARKER in line:
        return []

    findings: list[str] = []
    for category, pattern in PATTERNS:
        for match in pattern.finditer(line):
            if category in {"LOCAL_HOME_POSIX", "LOCAL_HOME_WINDOWS"}:
                if match.groupdict().get("name", "").casefold() in SAFE_HOME_NAMES:
                    continue
            if category == "EMAIL":
                domain = match.group(1).casefold()
                if domain in SAFE_EMAIL_DOMAINS:
                    continue
            findings.append(category)
            break

    folded = line.casefold()
    for term in terms:
        if term.casefold() in folded:
            findings.append("PRIVATE_DENYLIST_TERM")
            break

    return findings


def scan_file(path: Path, terms: list[str]) -> list[tuple[int, str]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [(0, f"READ_ERROR:{exc.__class__.__name__}")]

    if b"\0" in data:
        return []

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for category in scan_line(line, terms):
            findings.append((line_no, category))
    return findings


def run_scan() -> int:
    terms = private_terms()
    failures: list[tuple[Path, int, str]] = []
    for path in tracked_files():
        for line_no, category in scan_file(path, terms):
            failures.append((path, line_no, category))

    if failures:
        print("Public-safety scan failed. Values are intentionally redacted.")
        for path, line_no, category in failures:
            location = f"{path}:{line_no}" if line_no else str(path)
            print(f"- {location} [{category}]")
        print(f"Total findings: {len(failures)}")
        return 1

    print("Public-safety scan passed.")
    return 0


def self_test() -> int:
    bad = [
        "/Users/" + "realperson" + "/Documents/project",
        "C:\\Users\\" + "realperson" + "\\work\\repo",
        "server=192." + "168.1.55",
        "mail=" + "person" + "@internal.invalid",
        "token=" + "ghp_" + "A" * 36,
        "token=" + "github_pat_" + "B" * 32,
        "token=" + "sk-" + "C" * 32,
        "key=" + "AKIA" + "D" * 16,
        "host=" + "devbox" + ".local",
    ]
    good = [
        "/Users/user/project",
        "/home/runner/work/repo",
        "contact=user@example.com",
        "placeholder=ghp_",
        "public=198.51.100.10",
        "the word token is documentation, not a credential",
    ]

    for sample in bad:
        if not scan_line(sample, []):
            print("Self-test failed: expected bad sample to be detected.")
            return 1
    for sample in good:
        if scan_line(sample, []):
            print("Self-test failed: expected good sample to pass.")
            return 1

    deny = "private-project-codename"
    if "PRIVATE_DENYLIST_TERM" not in scan_line("contains " + deny, [deny]):
        print("Self-test failed: private denylist did not detect a term.")
        return 1

    if scan_line("person@internal.invalid  # public-safety: allow", []):
        print("Self-test failed: allow marker did not suppress a line.")
        return 1

    print("Public-safety scanner self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    return run_scan()


if __name__ == "__main__":
    raise SystemExit(main())

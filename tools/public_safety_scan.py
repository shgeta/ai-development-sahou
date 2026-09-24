#!/usr/bin/env python3
"""Fail-closed public-repository safety scan."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import unicodedata

ALLOW_MARKER = "public-safety: allow"
SAFE_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "users.noreply.github.com"}
SAFE_HOME_NAMES = {"user", "username", "example", "runner"}
MAX_TRACKED_FILE_BYTES = 2 * 1024 * 1024
PRIVATE_RULE_TYPES = {"COMPANY", "BRAND", "PRODUCT", "PROJECT", "INGREDIENT"}
PRIVATE_RULE_ENV_KEYS = ["PUBLIC_SAFETY_PRIVATE_RULES"] + [
    f"PUBLIC_SAFETY_PRIVATE_RULES_{i}" for i in range(1, 13)
]

BLOCKED_EXTENSIONS = {
    ".fig", ".sketch", ".psd", ".psb", ".ai", ".xd",
    ".zip", ".7z", ".rar", ".tar", ".tgz", ".gz", ".bz2", ".xz",
    ".db", ".sqlite", ".sqlite3", ".dump", ".bak", ".tmp",
    ".pem", ".key", ".p12", ".pfx", ".mobileprovision",
}
BLOCKED_FILENAMES = {".env", ".ds_store", "thumbs.db"}
BLOCKED_PATH_PARTS = {".idea", ".vscode"}

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
]

QUANTITY_PATTERN = re.compile(
    r"(?i)(?<![A-Za-z0-9])\d+(?:[.,]\d+)?\s*"
    r"(?:%|wt\.?%|w/w|v/v|ppm|ppb|µg|μg|ug|mg|g|kg|µl|μl|ul|ml|l|mg\s*/\s*ml|g\s*/\s*l)"
    r"(?![A-Za-z0-9])"
)
FORMULATION_KEYWORDS = re.compile(
    r"(?i)(?:原料|原材料|成分|配合|処方|濃度|含有|ingredient|inci|formula|formulation|concentration|dosage)"
)


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", value).strip()


def compact_text(value: str) -> str:
    value = normalize_text(value)
    return re.sub(r"[\s_\-‐‑–—・･]+", "", value)


def tracked_files() -> list[Path]:
    proc = subprocess.run(["git", "ls-files", "-z"], check=True, stdout=subprocess.PIPE)
    return [Path(p.decode("utf-8")) for p in proc.stdout.split(b"\0") if p]


def load_private_rules() -> list[tuple[str, str, str]]:
    raw_parts = [os.environ.get(key, "") for key in PRIVATE_RULE_ENV_KEYS]
    legacy = os.environ.get("PUBLIC_SAFETY_PRIVATE_TERMS", "")
    rules: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()

    for raw in raw_parts:
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "\t" in line:
                kind, value = line.split("\t", 1)
            elif "|" in line:
                kind, value = line.split("|", 1)
            else:
                kind, value = "PROJECT", line
            kind = kind.strip().upper()
            value = value.strip()
            if kind not in PRIVATE_RULE_TYPES:
                continue
            norm = normalize_text(value)
            compact = compact_text(value)
            if len(compact) < 3:
                continue
            key = (kind, compact)
            if key not in seen:
                seen.add(key)
                rules.append((kind, norm, compact))

    for line in legacy.splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        compact = compact_text(value)
        if len(compact) >= 3 and ("PROJECT", compact) not in seen:
            seen.add(("PROJECT", compact))
            rules.append(("PROJECT", normalize_text(value), compact))
    return rules


def base_line_findings(line: str) -> list[str]:
    if ALLOW_MARKER in line:
        return []
    findings: list[str] = []
    for category, pattern in PATTERNS:
        for match in pattern.finditer(line):
            if category in {"LOCAL_HOME_POSIX", "LOCAL_HOME_WINDOWS"}:
                if match.groupdict().get("name", "").casefold() in SAFE_HOME_NAMES:
                    continue
            if category == "EMAIL":
                if match.group(1).casefold() in SAFE_EMAIL_DOMAINS:
                    continue
            findings.append(category)
            break

    if QUANTITY_PATTERN.search(line) and FORMULATION_KEYWORDS.search(line):
        findings.append("FORMULATION_PATTERN")
    return findings


def private_line_findings(line: str, rules: list[tuple[str, str, str]]) -> tuple[list[str], bool]:
    if ALLOW_MARKER in line:
        return [], False
    norm = normalize_text(line)
    compact = compact_text(line)
    findings: list[str] = []
    ingredient_hit = False
    for kind, rule_norm, rule_compact in rules:
        if rule_norm in norm or rule_compact in compact:
            findings.append(f"PRIVATE_{kind}")
            if kind == "INGREDIENT":
                ingredient_hit = True
    return sorted(set(findings)), ingredient_hit


def file_policy_findings(path: Path, data: bytes) -> list[str]:
    findings: list[str] = []
    suffix = path.suffix.casefold()
    name = path.name.casefold()
    parts = {part.casefold() for part in path.parts}
    if suffix in BLOCKED_EXTENSIONS:
        findings.append("BLOCKED_FILE_TYPE")
    if name in BLOCKED_FILENAMES or (name.startswith(".env.") and name != ".env.example"):
        findings.append("LOCAL_ONLY_FILE")
    if parts & BLOCKED_PATH_PARTS:
        findings.append("LOCAL_ONLY_PATH")
    if len(data) > MAX_TRACKED_FILE_BYTES:
        findings.append("TRACKED_FILE_TOO_LARGE")
    if b"\0" in data:
        findings.append("BINARY_FILE")
    else:
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            findings.append("BINARY_FILE")
    return findings


def scan_file(path: Path, rules: list[tuple[str, str, str]]) -> list[tuple[int, str]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [(0, f"READ_ERROR:{exc.__class__.__name__}")]

    policy = file_policy_findings(path, data)
    if policy:
        return [(0, category) for category in policy]

    lines = data.decode("utf-8").splitlines()
    findings: list[tuple[int, str]] = []
    ingredient_lines: set[int] = set()

    for idx, line in enumerate(lines):
        for category in base_line_findings(line):
            findings.append((idx + 1, category))
        private_findings, ingredient_hit = private_line_findings(line, rules)
        for category in private_findings:
            findings.append((idx + 1, category))
        if ingredient_hit:
            ingredient_lines.add(idx)

    for idx in ingredient_lines:
        lo = max(0, idx - 1)
        hi = min(len(lines), idx + 2)
        if any(QUANTITY_PATTERN.search(lines[j]) for j in range(lo, hi)):
            findings.append((idx + 1, "FORMULATION_DATA"))

    return sorted(set(findings))


def run_scan() -> int:
    rules = load_private_rules()
    require_private = os.environ.get("PUBLIC_SAFETY_REQUIRE_PRIVATE_RULES", "") == "1"
    failures: list[tuple[Path, int, str]] = []

    if require_private and not rules:
        print("Public-safety scan failed: private rules are required but unavailable.")
        return 1

    for path in tracked_files():
        for line_no, category in scan_file(path, rules):
            failures.append((path, line_no, category))

    if failures:
        print("Public-safety scan failed. Matching values are intentionally redacted.")
        for path, line_no, category in failures:
            location = f"{path}:{line_no}" if line_no else str(path)
            print(f"- {location} [{category}]")
        print(f"Total findings: {len(failures)}")
        return 1

    print(f"Public-safety scan passed. Private rules loaded: {len(rules)}")
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
        "ingredient: synthetic-ingredient 2.5%",
        "配合量 15 mg/mL",
    ]
    good = [
        "/Users/user/project",
        "/home/runner/work/repo",
        "contact=user@example.com",
        "placeholder=ghp_",
        "public=198.51.100.10",
        "coverage is 95 percent",
    ]
    for sample in bad:
        if not base_line_findings(sample):
            print("Self-test failed: expected bad sample to be detected.")
            return 1
    for sample in good:
        if base_line_findings(sample):
            print("Self-test failed: expected good sample to pass.")
            return 1

    rules = [
        ("COMPANY", normalize_text("Example Private Company"), compact_text("Example Private Company")),
        ("PRODUCT", normalize_text("Synthetic Product Z"), compact_text("Synthetic Product Z")),
        ("INGREDIENT", normalize_text("Synthetic Ingredient Q"), compact_text("Synthetic Ingredient Q")),
    ]
    private, ingredient_hit = private_line_findings("synthetic ingredient q 3.0%", rules)
    if "PRIVATE_INGREDIENT" not in private or not ingredient_hit:
        print("Self-test failed: ingredient rule was not detected.")
        return 1

    lines = ["Synthetic Ingredient Q", "3.0 mg/mL"]
    hits = []
    for i, line in enumerate(lines):
        pf, ih = private_line_findings(line, rules)
        if ih and any(QUANTITY_PATTERN.search(x) for x in lines[max(0, i-1):min(len(lines), i+2)]):
            hits.append("FORMULATION_DATA")
    if "FORMULATION_DATA" not in hits:
        print("Self-test failed: adjacent formulation data was not detected.")
        return 1

    file_cases = [
        (Path("design.fig"), b"synthetic", "BLOCKED_FILE_TYPE"),
        (Path("archive.zip"), b"synthetic", "BLOCKED_FILE_TYPE"),
        (Path(".env"), b"X=1", "LOCAL_ONLY_FILE"),
        (Path(".vscode/settings.json"), b"{}", "LOCAL_ONLY_PATH"),
        (Path("asset.bin"), b"\x00synthetic", "BINARY_FILE"),
        (Path("huge.txt"), b"x" * (MAX_TRACKED_FILE_BYTES + 1), "TRACKED_FILE_TOO_LARGE"),
    ]
    for path, data, category in file_cases:
        if category not in file_policy_findings(path, data):
            print(f"Self-test failed: {category} was not detected.")
            return 1

    print("Public-safety scanner self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    return self_test() if args.self_test else run_scan()


if __name__ == "__main__":
    raise SystemExit(main())

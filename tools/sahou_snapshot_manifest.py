#!/usr/bin/env python3
"""Build and verify metadata for an exact SAHOU repository snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_manifest(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        rows.append({
            "path": rel,
            "size": path.stat().st_size,
            "sha256": sha256(path),
        })
    return rows


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    archive = Path(args.archive).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    tree = {
        "schema": "sahou-cache-tree-v1",
        "repository": args.repository,
        "commit_sha": args.commit_sha,
        "git_tree_sha": args.git_tree_sha,
        "files": file_manifest(root),
    }
    tree_path = out / "TREE.json"
    write_json(tree_path, tree)

    manifest = {
        "schema": "sahou-cache-manifest-v1",
        "repository": args.repository,
        "source_ref": args.source_ref,
        "commit_sha": args.commit_sha,
        "git_tree_sha": args.git_tree_sha,
        "archive_name": archive.name,
        "archive_sha256": sha256(archive),
        "tree_name": tree_path.name,
        "tree_sha256": sha256(tree_path),
        "file_count": len(tree["files"]),
    }
    manifest_path = out / "MANIFEST.json"
    write_json(manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


def verify(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    base = manifest_path.parent
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive = base / m["archive_name"]
    tree = base / m["tree_name"]

    errors: list[str] = []
    if not archive.is_file():
        errors.append("archive missing")
    elif sha256(archive) != m["archive_sha256"]:
        errors.append("archive sha256 mismatch")
    if not tree.is_file():
        errors.append("tree manifest missing")
    elif sha256(tree) != m["tree_sha256"]:
        errors.append("tree manifest sha256 mismatch")

    if errors:
        for error in errors:
            print(error)
        return 1
    print("SAHOU cache snapshot metadata verified.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("build")
    p.add_argument("--root", required=True)
    p.add_argument("--archive", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--repository", required=True)
    p.add_argument("--source-ref", required=True)
    p.add_argument("--commit-sha", required=True)
    p.add_argument("--git-tree-sha", required=True)
    p.set_defaults(func=build)

    p = sub.add_parser("verify")
    p.add_argument("--manifest", required=True)
    p.set_defaults(func=verify)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

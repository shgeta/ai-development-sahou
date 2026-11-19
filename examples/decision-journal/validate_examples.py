#!/usr/bin/env python3
"""Fixture-only Decision Journal checks, NOT a production conflict resolver."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def canonical_digest(events: list[dict]) -> str:
    raw = b""
    for item in sorted(events, key=lambda x: x["event_id"]):
        raw += (item["event_id"] + "\0").encode("utf-8")
        raw += json.dumps(
            item, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def project_fixture(events: list[dict]) -> tuple[set[str], set[str], set[str]]:
    """Illustrative fixture-only projection: no general scope semantics."""
    conflicts = {
        e["event_id"] for e in events if e["event_type"] == "CONFLICT_DETECTED"
    }
    applied = {
        e["applies_decision"] for e in events
        if e["event_type"] == "APPLIED"
        and e.get("target_revision") and e.get("verification_refs")
    }
    for e in events:
        if e["event_type"] == "CONFLICT_RESOLVED":
            if e["resolution_strategy"] != "DEFER":
                conflicts.discard(e["resolution_of"])
    decisions = {
        e["event_id"] for e in events
        if e["event_type"] in ("DECIDED", "CONFLICT_RESOLVED")
    }
    superseded = {ref for e in events for ref in e.get("supersedes", [])}
    current = (decisions - superseded) & applied
    pending = decisions - superseded - applied
    return current, conflicts, pending


def main():
    es = load("schemas/decision_event.schema.json")
    ss = load("schemas/decision_snapshot.schema.json")
    events = load("examples/decision-journal/decision_events.synthetic.json")
    snap = load("examples/decision-journal/decision_snapshot.synthetic.json")
    Draft202012Validator.check_schema(es)
    Draft202012Validator.check_schema(ss)
    ev = Draft202012Validator(es, format_checker=FormatChecker())
    sn = Draft202012Validator(ss, format_checker=FormatChecker())
    for item in events:
        ev.validate(item)
    sn.validate(snap)
    ids = [e["event_id"] for e in events]
    assert len(ids) == len(set(ids)), "duplicate event_id"
    by_id = {e["event_id"]: e for e in events}
    for item in events:
        deps = list(item["based_on"]) + item.get("supersedes", [])
        deps += item.get("conflict_participants", [])
        for key in ("correction_of", "resolution_of", "applies_decision"):
            if item.get(key):
                deps.append(item[key])
        for ref in deps:
            assert ref in by_id, f"missing ref: {ref}"
        assert item["event_id"] not in deps
    assert set(snap["included_event_ids"]) == set(ids)
    assert snap["event_set_sha256"] == canonical_digest(events)
    current, conflicts, pending = project_fixture(events)
    assert current == {x["decision_id"] for x in snap["current_decisions"]}
    assert not conflicts
    assert not pending
    assert len(project_fixture(events[:3])[1]) == 1, "conflict not detected"
    preapply = project_fixture(events[:4])
    assert not preapply[0] and preapply[2] == {"evt-a04"}, "unapplied decision current"
    corrupted = dict(snap, event_set_sha256="0" * 64)
    assert corrupted["event_set_sha256"] != canonical_digest(events)
    assert project_fixture(list(reversed(events))) == (current, conflicts, pending)
    print("PASS: schema, cross-refs, conflict, pending apply, snapshot hash, order independence")


if __name__ == "__main__":
    main()

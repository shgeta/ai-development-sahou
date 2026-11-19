# Decision Journal synthetic fixtures

These are public-safe synthetic samples for the [Decision Journal Plugin](../../specs/log/DECISION_JOURNAL_PLUGIN_v0.1.md), [Conflict Resolution](../../specs/log/DECISION_CONFLICT_RESOLUTION_v0.1.md), and [Snapshot](../../specs/log/DECISION_SNAPSHOT_v0.1.md).

Run `python -m pip install jsonschema==4.23.0` then `python examples/decision-journal/validate_examples.py` from the repository root.

This checks schemas, references, fixture-only projection states, event-set SHA-256, and order independence **only for the included synthetic example**. It does not implement production event persistence, arbitrary-scope conflict resolution, or crash recovery. See [TEST_MATRIX.md](TEST_MATRIX.md) for unimplemented paths.

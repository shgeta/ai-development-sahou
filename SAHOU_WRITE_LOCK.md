# SAHOU Write Lock

This file is the repository-local write gate for `shgeta/ai-development-sahou`.

## State

```text
SAHOU_WRITE_STATE = LOCKED
```

`LOCKED` is the default and persistent state.

The repository may be read, searched, compared, reviewed, or discussed while locked.
No repository mutation is allowed merely because a change appears useful.

## What counts as a write

While `LOCKED`, an AI MUST NOT perform any mutation whose purpose is to change this repository, including:

- creating or editing Issues for a SAHOU change;
- creating, updating, or deleting branches;
- creating, updating, moving, or deleting files;
- creating or updating pull requests;
- adding or changing labels, reviewers, comments, or other repository state for the change;
- merging or otherwise advancing a SAHOU change.

Read-only inspection is allowed.

## Unlock authority

Only an explicit instruction from the user in the current task may unlock SAHOU writes.

Examples of explicit unlock intent:

```text
SAHOUの鍵を外して
SAHOUを更新して
共通SAHOUにこの変更を書いて
```

A generic continuation instruction such as `進めて`, `やって`, or `続けて` NEVER unlocks SAHOU by itself.

Unlock requires explicit SAHOU/common-spec write intent in the current user instruction, such as naming SAHOU/common SAHOU and asking to unlock, write, update, or change it.

The AI MUST NOT infer unlock authority from:
- prior conversations;
- prior sessions;
- the existence of an open Issue or branch;
- a previous unlock for another task;
- the fact that the proposed change looks generally reusable.

## Scope of an unlock

An unlock is:

- repository-specific: it applies only to `shgeta/ai-development-sahou`;
- task-specific: it applies only to the change the user authorized;
- temporary: it ends when that change is merged, abandoned, completed, or the conversation moves to another task;
- non-transitive: it does not authorize unrelated cleanup, refactoring, promotion, or common-rule additions.

If scope becomes ambiguous, return to `LOCKED` and ask for explicit unlock before writing.

## Required flow while unlocked

```text
LOCKED
  -> explicit user unlock
UNLOCKED_FOR_TASK
  -> Issue
  -> work branch
  -> change
  -> PR
  -> review / validation
  -> merge OR abandon
LOCKED
```

Do not write directly to `main` as a substitute for this flow.

## Promotion rule

Project-specific findings MUST mature in the project repository first.

A finding may be proposed for common SAHOU while locked, but promotion into this repository requires a separate explicit unlock. "This seems reusable" is never sufficient authorization.

## Failure-safe rule

When uncertain whether SAHOU is unlocked, treat it as `LOCKED`.

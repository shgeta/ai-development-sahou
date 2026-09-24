# GitHub AI作業運用 v1.15 SHARD — Status + Issue Binding

- Updated: 2026-09-24
- Status: APPROVED
- Parent authority: `GITHUB_AI作業運用共通仕様_v1.15.md`
- Semantic version: GitHub AI作業運用 v1.15
- Physical role: additional shard; this file does not create a separate specification version.

## Rule

会話中の話題が、継続的に追跡すべき議題・作業テーマ・検証対象として成立した時点で、Library Current State と GitHub Issue を同じ変更単位で作成または更新する。

```text
conversation
  -> topic becomes trackable work / decision subject
       -> create or update GitHub Issue
       -> create or update corresponding Library Current State
```

## Role split

```text
GitHub Issue
  = canonical work / discussion / decision history
  = Goal / Scope / Acceptance / evidence / outcome

Library Current State
  = active operational mirror
  = current focus / sub-step / blocker / next / order
```

Current StateはIssueの代替ではない。Issue化した議題についてCurrent Stateだけを作って追跡してはならない。

IssueとStatusは成功時だけ作るものではない。調査、試行、失敗、却下、中止、保留、no-changeを含め、議題として追跡を開始した時点で作成する。

IssueがClose / ABANDONED / DEFERRED等になりactive workでなくなった場合、Issueは履歴として保持し、Current State側はactive一覧から外すかclosed stateとして最小参照だけを残す。

## Synchronization

Issue作成または再利用時に、Current Stateを使うprojectでは対応するstate entryを同時に作成または更新する。

Current Stateには少なくとも必要に応じて以下を置く。

- Issue reference
- current focus
- current sub-step
- blocker / waiting
- next immediate step
- branch / HEAD mirror when applicable

Issue側のGoal / Scope / Acceptance / decision historyをCurrent Stateへ複製しない。Current StateからIssueへ到達できる参照を持つ。

## Validation

- 議題化した作業にIssueだけありCurrent Stateが欠落していないか（Current State運用projectの場合）。
- Issue化した議題をCurrent Stateだけで追跡していないか。
- Current Stateからcanonical Issueへ到達できるか。
- closed / abandoned Issueのstateがactive一覧へ残り続けていないか。
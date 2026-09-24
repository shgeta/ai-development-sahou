# GitHub AI作業運用 v1.15 SHARD — Issue Outcome Retention

- Updated: 2026-09-24
- Status: APPROVED
- Parent authority: `GITHUB_AI作業運用共通仕様_v1.15.md`
- Semantic version: GitHub AI作業運用 v1.15
- Physical role: additional shard; this file does not create a separate specification version.

## Rule

GitHub Issueは、成功した変更だけを保存する場所ではない。議題として追跡する価値があると判断されIssue化された時点で、そのIssueは作業・検討・判断のcanonical recordとなる。

一度Issue化された事項は、最終結果が次のいずれであってもIssueとして保持する。

- implemented / accepted
- failed
- rejected
- abandoned
- deferred
- superseded
- no-change / no-action
- investigation only

IssueをCloseすることは、そのIssueの履歴を捨てることを意味しない。Close時には、可能な限り結果と理由を記録する。

```text
Issue opened
  -> investigation / implementation / discussion
  -> outcome determined
       SUCCESS
       FAILURE
       REJECTED
       ABANDONED
       DEFERRED
       SUPERSEDED
       NO_CHANGE
  -> final checkpoint / evidence
  -> Close when appropriate
```

## Boundary with Library Current State

Library Current Stateは、activeな現在地・focus・順序・blocker・nextを保持する補助盤であり、Issue historyの代替ではない。

Issueが失敗・却下・中止になった場合でも、Current Stateからactive項目を外すだけでIssue自体は削除・吸収しない。必要ならCurrent Stateからclosed Issueへの参照だけ残す。

## Boundary with AISPEC

AISPEC/current specにはcurrent semantic truthのみを保持する。

- 採用された意味・rule -> AISPEC/current spec
- 採用しなかった案、失敗した実装、却下理由、検討経路 -> Issue
- exact diff -> PR / commit
- validation evidence -> tests / CI / Issue checkpoint

失敗・却下・no-changeのIssueでも、後のdecisionが同じ議論を繰り返さないために有用なら、`DECISION_REF` またはprior decision linkから参照してよい。

## Validation

- Issue化した議題を、結果が失敗・却下・中止だったことだけを理由に削除していない。
- Close理由または最終outcomeが追跡可能である。
- Current Stateだけに失敗経緯を残してIssueを空にしていない。
- AISPECへ未採用案をcurrent ruleとして混入させていない。
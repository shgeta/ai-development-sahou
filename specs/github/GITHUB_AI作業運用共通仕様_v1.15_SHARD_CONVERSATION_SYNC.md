# GitHub AI作業運用 v1.15 SHARD — Conversation-to-Authority Sync

- Updated: 2026-09-24
- Status: APPROVED
- Parent authority: `GITHUB_AI作業運用共通仕様_v1.15.md`
- Semantic version: GitHub AI作業運用 v1.15
- Physical role: additional shard; this file does not create a separate specification version.
- Related AISPEC GROUP: `AISPEC_CONTINUOUS_DISTILLATION`

## Rule

GitHub/AISPEC projectでは、chatは作業入力であってhandoff authorityではない。

会話中に採用された設計判断、仕様変更、運用ルール、重要な検証結果が安定した時点で、AIは明示的な記録指示を待たず、次へ同期する。

```text
current semantic truth   -> AISPEC / current spec
decision rationale       -> GitHub Issue / DECISION_REF
exact change             -> PR / commit
validation evidence      -> tests / CI / Issue checkpoint
temporary current focus  -> Library Current State
```

## Conversation distillation checkpoint

meaningful checkpoint、handoff、または作業区切りでは次を確認する。

1. 直近の会話で新しく確定した仕様・運用ruleがあるか。
2. current AISPEC/current specへ未反映なら、既存record変更はPATCH、新規ruleのまとまった追加はNEW SHARDで記録する。
3. semantic changeなら対応Issueと`DECISION_REF`を結ぶ。
4. 一時的な進捗だけならAISPECへ昇格させずCurrent Stateへ置く。
5. 仮説・未採用案・雑談はcurrent authorityへ書かない。
6. 書込み後、SEARCH + specification closureとreverse dependencyを必要範囲で確認する。
7. common specificationへ一般化する場合はpublic-safe ruleに従い、実案件identifierを除去する。

この処理は通常のproject継続性維持の一部であり、ユーザーが毎回「記録して」と指示することを前提にしない。

ただし、破壊的変更、authorityの削除、大規模migration、外部公開、権限変更など通常の記録を超える操作は、それぞれの既存guardrailに従う。
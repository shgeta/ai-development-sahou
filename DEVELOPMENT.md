# SAHOU Development Guide

この文書は **SAHOUを利用するproject向けの共通仕様ではなく、`shgeta/ai-development-sahou` repository自体を修正・保守する開発者向け運用** である。

## 1. Scope

対象:

- SAHOU core specification
- Adapter
- template
- tool
- workflow
- README / developer documentation

対象外:

- SAHOU利用projectの通常開発
- project固有のAISPEC / Current State / Issue運用
- private data / private ruleの一般公開

## 2. Standard change flow

SAHOU自身の変更は原則として次の順で進める。

```text
Issue
  -> work branch
  -> GitHub API / connector / local toolingで修正
  -> PR
  -> AI REVIEW
       -> Issue goal / acceptance criteria
       -> PR diff全体
       -> base側の関連仕様
       -> 変更箇所の周辺文脈
       -> public-safety / authority / duplication / deletion checks
  -> 指摘あり
       -> branch修正
       -> AI REVIEW再実行
  -> AI REVIEW PASS
  -> required Actions / CI確認
  -> merge
  -> main後検証
  -> shared SAHOU cacheのrevision更新
```

GitHub API / connectorを使って同一branchへ複数回修正してよい。push方法そのものはreview品質の代替条件ではない。

## 3. AI review gate

PRを作成しただけでmergeしてはならない。

AI reviewでは、実装時の会話記憶だけに依存せず、reviewerとして少なくとも次を読み直す。

1. 対応IssueのGoal / Scope / Acceptance criteria
2. PR diff全体
3. base branch側の関連仕様
4. 変更対象fileの前後文脈
5. 必要に応じて関連Issue / prior decision / tests / workflow

reviewは「Actionsが通るか」だけではなく、**変更意味そのものが妥当か** を確認する。

## 4. Reviewer checklist

最低限、次を確認する。

- Issueの目的から逸脱していない
- Acceptance criteriaを満たしている
- 既存仕様と矛盾していない
- 同じ意味のrule / authorityを重複追加していない
- 派生物や二重authorityを不用意に増やしていない
- 既存ruleの意味を意図せず削除していない
- public repositoryへ出せない情報が混入していない
- private term / credential / local path / internal identifierを含まない
- tool / workflow変更ではfailure pathとvalidation pathがある
- template変更では利用者向け仕様とdeveloper-only運用を混同していない
- README / entrypoint / referenceが古いまま残っていない
- 変更に必要なtest / CI / Public safetyがある
- generated / cache / snapshotをauthorityと誤認する構造になっていない

## 5. Review result

review結果は最低限次のいずれかとする。

- `PASS`
- `CHANGES_REQUIRED`

`CHANGES_REQUIRED` の場合は、mergeせず修正する。修正後は差分だけを眺めて済ませず、影響範囲に応じてAI reviewを再実行する。

重要な指摘・判断理由はPRまたはIssueへ残し、会話だけに閉じない。

## 6. Actions / CIとの関係

AI reviewとActions / CIは役割が異なる。

- AI review: semantic correctness / consistency / unintended change / authority design
- Actions / CI: machine validation / public-safety / tests / reproducibility

原則として両方を通してからmergeする。

Actions PASSだけでAI reviewを省略しない。AI review PASSだけでrequired CIを省略しない。

## 7. Post-merge

merge後は少なくとも次を確認する。

1. mainのrequired ActionsがPASS
2. main exact SHAを確認
3. SAHOU shared cacheを使う環境ではcurrent cache SHAと比較
4. SHAが変わっていればexact snapshotを生成・検証してshared cacheを更新
5. Issueへ最終結果を記録してclose

## 8. Public/private boundary

このrepositoryはpublic前提で保守する。

developer review用のfixture / example / test dataにも、private company / customer / product / ingredient / project identifier等を持ち込まない。

private denylistやprivate rule setの実体はrepository外のprivate storage / secretへ保持する。

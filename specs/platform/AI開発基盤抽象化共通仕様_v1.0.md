# AI開発基盤抽象化 共通仕様 v1.0

- Updated: 2026-09-24
- Status: APPROVED
- Scope: AI/人間の継続開発で使用する外部サービス・保存領域・repository・work item・CI等の製品非依存な役割定義
- Relation: AISPEC / repository運用 / Current State / Adapter specifications の共通基盤

## 1. 原則

共通仕様は、特定製品名を意味上の必須要件として使用しない。

`GitHub`、`ChatGPT Library`、その他の製品・サービス名は実装Adapterであり、共通仕様では先に論理的な役割を定義する。

製品固有機能が存在しない環境では、同等の役割を持つ機能へ置換してよい。対応機能が存在しない場合、Adapterはそのgapとfallbackを明示する。

## 2. Logical platform roles

| ROLE_ID | 論理役割 | 意味 |
|---|---|---|
| PLATFORM.STORE.PERSISTENT | Persistent Project Store | chat/sessionを跨いでproject file、Current State、input、artifact、snapshot等を再利用可能に保持する永続領域 |
| PLATFORM.REPO.VERSIONED | Versioned Repository | source/spec/document等のversioned treeとexact revisionを保持するrepository |
| PLATFORM.WORK.TRACKER | Work Item Tracker | 議題・作業単位・decision history・outcomeを永続的に追跡する仕組み |
| PLATFORM.CHANGE.REVIEW | Change Review | exact diffをreviewし、統合前後の変更単位を追跡する仕組み |
| PLATFORM.REVISION.EXACT | Exact Revision Identity | commit SHA等、対象tree/revisionを一意に固定する識別子 |
| PLATFORM.CI.VALIDATION | CI / Validation Runner | exact revisionに対してtest / lint / build / QA等を実行するrunner |
| PLATFORM.RUNNER.REMOTE | Remote Execution Runner | local/container制約を超える取得・生成・validation等を実行できるremote runner |
| PLATFORM.ARTIFACT.DURABLE | Durable Artifact Store | runner output、snapshot、bundle、large generated result等を後から回収可能に保持するartifact領域 |
| PLATFORM.WORKSPACE.LOCAL | Local Working Copy | 編集・test・diff生成等を行うcheckout/worktree等のsession-local作業領域 |

## 3. Authority separation

論理役割は次のauthority separationを保つ。

```text
current semantic truth
  -> current specification / AISPEC

decision / discussion / outcome history
  -> Work Item Tracker

exact source/spec diff
  -> Versioned Repository / Exact Revision

active current focus / blocker / next
  -> Current State in Persistent Project Store when available

validation evidence
  -> CI / Validation Runner + Work Item record
```

Persistent Project StoreはWork Item Trackerの代替ではなく、Work Item Trackerはcurrent specification authorityの代替ではない。

## 4. Optional capability rule

共通仕様で特定のplatform capabilityを要求する場合、次の順で解釈する。

1. 現在のAdapterに対応機能がある -> その機能を使用する。
2. 同等機能が別の接続済みserviceにある -> Adapter mappingに従い代替する。
3. 対応機能がない -> capabilityを存在すると仮定せず、fallbackまたはunsupportedを明示する。

したがって、共通仕様本文では `Library` や `GitHub Issue` のような製品固有名をgeneric roleの同義語として使用しない。

## 5. Adapter requirement

Adapterは少なくとも以下を宣言する。

- 対応するlogical ROLE_ID
- 製品上の実機能名
- canonical identity / reference方法
- read / write / delete等の利用可能operation
- concurrency / revision guardの有無
- persistence範囲
- known limitation
- fallback

## 6. Validation

- 共通ruleが特定製品の存在を暗黙前提にしていない。
- 製品固有名を使用する場合、Adapterまたは明示的なimplementation exampleとして区別されている。
- capability非搭載環境で、存在しない機能を使用する前提になっていない。
- Adapterを差し替えても、AISPEC / Issue相当 / Current State / exact revision / validation evidence の役割分離が保たれる。

## 7. Shared exact-revision cache

複数project / 複数chatから共通して参照される外部authorityは、projectごとに重複保存せず、**authority identity + exact revision** をkeyとするshared cacheへ保存してよい。

運用原則:

1. shared cacheはauthorityそのものではなくread optimizationである。
2. cache identityは少なくとも `authority repository identity + exact revision SHA` で一意に決める。
3. session開始時は、まずauthority側のcurrent refからexact revisionを解決する。
4. shared cacheに同一exact revisionの検証済みsnapshotが存在する場合、そのsnapshotを再利用し、authority本文を再取得しない。
5. current exact revisionがcacheと異なる場合のみ、新しいexact snapshotを取得してcacheを更新する。
6. cache snapshotはpartial bundle、手作業要約、派生full-file等へ置換せず、対象authorityのexact repository snapshotを基本とする。
7. stale / partial / revision不明 / 検証不能なcacheをcurrent authorityの代替として使用しない。
8. project固有Current State、Issue state、private input等と、全project共有cacheを同一namespaceへ混在させない。

このruleは、共通authorityを毎session full利用しながら、本文の再取得だけを省略するためのものである。

# Decision Conflict Resolution v0.1（共通仕様）

Status: **APPROVED** — 2026-11-19  
Depends on: `DECISION_JOURNAL_PLUGIN_v0.1.md`, `LOG_CORE_v1.0.md`

## 1. 目的

複数の決定イベントの重複・相互補完・部分的置換・矛盾を区別し、決定の因果関係とauthorityに従って再構成する。**last-write-winsは禁止**する。

「時系列で後」や「Closed Issueだから古い」、「AIが最後に見つけた」ことは、優先の根拠としない。

## 2. 規範ルール

| RULE_ID | 意味 |
|---|---|
| `DECISION.CONFLICT.010` | 複数のeventが同じ論点・対象へ影響し得る場合、scope重複と意味の互換性を確認する |
| `DECISION.CONFLICT.020` | 不明なscopeを勝手に非重複と推測せず、`UNKNOWN_OVERLAP`とする |
| `DECISION.CONFLICT.030` | 重複、非重複、両立する追加、明示的な置換、無効化、実質矛盾、authority不整合を区別する |
| `DECISION.CONFLICT.040` | 競合解消には既存のauthority mapping、明示的な因果関係、正当な承認者と根拠が必要 |
| `DECISION.CONFLICT.050` | timestamp、event file名、IssueのOpen/Closed、commentの新旧のみで勝者を決めない |
| `DECISION.CONFLICT.060` | 競合検出と解決は元eventを変更せず追加eventとして記録する |
| `DECISION.CONFLICT.070` | 未解決競合のscopeでは自動的な新しい適用を止める。既存の実稼働環境を自動停止・rollbackしない |
| `DECISION.CONFLICT.080` | 部分統合時はscopeを分割・明記し、統合対象のdecision IDをすべて保持する |
| `DECISION.CONFLICT.090` | 統合結果から過去の根拠・却下案・変更対象へ追跡できる |
| `DECISION.CONFLICT.100` | 自動処理は分類と明らかな同一性検出に限定し、裁量を伴う解決にはauthorityによる判断を要する |
| `DECISION.CONFLICT.110` | 未反映の決定と現行仕様の差分を、黙って仕様変更済みと見なさない |
| `DECISION.CONFLICT.120` | 事前に確認したbaselineと新イベントを再照合してから統合を永続化する。staleな競合解決を採用しない |

## 3. 比較の単位

比較対象は同一 `decision_key`、またはprojectのidentity resolverによって同一対象・論点だと判断されるevent集合。
二つのdecisionが異なるkeyを持っても同じ仕様・処理・条件を変更する場合、依存衝突として検出対象にする。

各decisionを次の軸で比較する:

- `scope.subject_ref`: 何に対する判断か
- `scope.dimensions`: environment / platform / customer category などの条件
- `authority_ref`: 現在の有効なauthorityと一致するか
- `based_on`: 判断時点でどのdecisionを知っていたか
- `supersedes`: 何を明示的に置き換えたか
- `evidence_refs`: 新しい証拠・却下理由・承認
- `application state`: 正本反映の成否
- `revision`: 対象となる正本のexact revision

scope同士の関係は `DISJOINT`, `EQUAL`, `OVERLAP`, `CONTAINS`, `UNKNOWN_OVERLAP` で分類する。projectが範囲条件を比較できない場合は人間レビューに回す。

## 4. 判定と解決の優先手順

1. event integrity・署名/出典・正当なauthorityを検証する。検証不能なものは有効decisionへ自動昇格しない。
2. exact duplicate（同一 `event_id` と同内容）はidempotentに扱う。同一IDで内容差があればhard errorとする。
3. 同じ意味で異IDの重複は履歴を保持し、projectionでは重複適用しない。
4. scopeが確実に非重複なら両方採用可能（それぞれのauthorityに従う）。
5. 互換な追加であれば両立可能。合成可能性が確実に証明できない場合は自動合成しない。
6. 明示された `supersedes` / `REVOKED` / `CORRECTION` を検証し、scope単位で旧判断の有効範囲を調整する。
7. 同じscopeで結果が両立しない場合、`CONFLICT_DETECTED` を追記し、該当scopeを `BLOCKED_BY_CONFLICT` とする。
8. `UNKNOWN_OVERLAP` とauthority不整合は無根拠に解決しない。必要な追加情報・担当authorityを明示する。
9. 解決権限のある主体が統合案を承認したら、参照付き `CONFLICT_RESOLVED` を追記し検証する。
10. 統合決定を正本へ反映し、exact revision検証後に `APPLIED` を追記する。

単純なfieldの合成で整合する場合も、意味上の合成が安全か確認する。単なる文字列結合は決定の統合ではない。

## 5. 競合分類

| 分類 | 条件 | 対処 |
|---|---|---|
| `DUPLICATE` | 同一決定の二重表現 | eventを残しprojectionで重複適用しない |
| `NON_OVERLAP` | 条件・対象が確実に異なる | 両立させる |
| `COMPATIBLE` | 明確に両立する補完関係 | 合成可能。根拠と参照を保持 |
| `EXPLICIT_REPLACEMENT` | 正当な `supersedes` と承認あり | 明示範囲を置換し、旧決定を履歴に保持 |
| `PARTIAL_REPLACEMENT` | 旧scopeの一部だけを置換 | 部分的に旧決定を有効とする |
| `SEMANTIC_CONFLICT` | 同一scopeで両立しない意味 | 未解決として適用停止 |
| `AUTHORITY_MISMATCH` | 仕様・Issue・実装が異なる状態 | 正本と履歴を照合し、差分をIssueなどで追跡 |
| `UNKNOWN_OVERLAP` | scopeが比較不能 | 推測せずレビュー |
| `STALE_RESOLUTION` | 統合時のbaseline以降に関連eventが追加 | 再照合してから再提案 |

## 6. コンフリクト解決イベント

`CONFLICT_DETECTED` は対象event ID集合、競合scope、矛盾点、判定根拠を保持する。機械的な検出であっても検出が永続化されていなければ記録済みと主張しない。

`CONFLICT_RESOLVED` は最低限、次の情報を保持する。

- `resolution_of`: 対象の `CONFLICT_DETECTED` event ID
- `conflict_participants`: 統合対象の全decision ID
- `resolution_strategy`: `KEEP_ONE`, `SPLIT_SCOPE`, `COMPOSE`, `REVISE`, `DEFER`
- `scope`: 統合が有効となる正確な対象・条件
- `summary`: 採用された意味と、どの判断が現在有効か
- `authorized_by` と `authority_ref`: 適正な承認と正本
- `based_on`, `supersedes`: 因果・置換関係
- `evidence_refs`: 理由・検証証拠
- 正本反映は別の `APPLIED` とexact revisionで確証する

`DEFER` も解決判断として記録できるが、意味上の競合がなくなったとは扱わない。保留中のscopeはblockedのままである。
`KEEP_ONE` は無条件の勝者選定ではなく、理由とauthorityの記録を必須とする。
新しい矛盾証拠が出た場合、過去の解決イベントも新eventで再評価する。

## 7. 三つ以上の競合

競合集合は2要素に限定しない。A/B/Cが同じ論点を競合させる場合、`conflict_participants = [A,B,C]` としてまとめて照合できる。

競合をA対Bの解決で終わらせ、Cの存在を見落としてはならない。統合前に新たな関連eventを検索し、検出基準revisionを確認する。
部分統合（AとBは合成可能、Cのみ保留）では、解決したscope・残るscope・残るeventを明確に分ける。

## 8. 境界と異常系

### 仕様-firstのproject

現在の仕様は通常の実行authorityであり、Issueに別の判断があってもIssueだけで現行仕様を自動変更しない。
しかし仕様自体が誤りという可能性があるため、`SOURCE` / `DECISION_REF` / Issue / testを照合し、必要な修正を正式な手順で決める。

### Issue-firstのproject

決定を記録するIssueがauthorityであれば、その最終判断・承認者・適用範囲を優先して参照する。
単なる最新コメントやIssue状態（Open/Closed）を決定の新旧・有効性とは混同しない。

### 書込み禁止または部分的な障害

Write Lockや権限不足がある場合、衝突の「検出」は読み取りで行えるが、canonical conflict / resolution eventは無断で追記しない。
未保存検出は `LOCAL_DETECTION_ONLY` と明記する。
正本適用後にログ保存が失敗した場合、現在状態は不明とし、exact ref検証で回復する。

## 9. 検証シナリオ

1. 同じ意味のeventが別IDで追記されてもprojectionは重複しない。
2. `environment=QA` と `environment=production` が別決定なら両方有効。
3. `environment` 未指定の全体ルールとQA限定ルールはscopeが重複する。狭い方を無条件に優先しない。
4. 同じscopeでA/Bが別々のbaselineから決まり、意味が矛盾する。後の時刻だけで優先しない。
5. AをBが明示的に置換し、Bの承認権限が有効ならAは履歴に残してBへ。
6. authority不明な決定は自動採用しない。
7. A/B解決後にCが存在すると判明した場合、解決を再照合する。
8. 衝突を`DEFER`した場合、blockedを解除しない。
9. 既知の却下理由は次回調査時に復元できる。
10. 現行仕様と記録が食い違う場合、いずれも無断変更しない。
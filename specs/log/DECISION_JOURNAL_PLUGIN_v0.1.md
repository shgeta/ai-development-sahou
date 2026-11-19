# Decision Journal Plugin v0.1（共通仕様）

Status: **APPROVED** — 2026-11-19  
Dependency: `LOG_CORE_v1.0.md`  
Related: `AISPEC_AI仕様記述共通仕様_v1.2_SHARD_CONTINUOUS_DISTILLATION.md`, `GITHUB_AI作業運用共通仕様_v1.17.md`  

## 1. 目的と境界

決定を独立したチャンクとして追記し、時系列と因果関係から有効な判断を復元する。Issue、仕様、コード、テスト、PRなど、どこから調査を開始しても、関連決定へ到達できるようにする。

Journal採用時のevent storeは**構造化された決定イベントのcanonical記録**であり、現在有効な仕様・実装、Issueに記録されたsemantic decision historyのauthorityを置き換えない。Issue-first、仕様-first、その他のproject固有authorityへ明示mappingで対応する。Journal自体を別の仕様authorityへ昇格させない。

安定して成立した、後続作業に影響する判断（採用・却下・保留・許容・変更・取消・統合）を記録対象とする。未確定の仮説や逐語会話を `DECIDED` に自動昇格させない。

## 2. 規範ルール

| RULE_ID | 意味 | 依存 |
|---|---|---|
| `DECISION.JOURNAL.010` | 決定は永続的な記録から再発見でき、正本と根拠を参照できる | `LOG.CORE.010, LOG.CORE.100` |
| `DECISION.JOURNAL.020` | 過去イベントを消去・上書きせず、訂正・取消・置換を新イベントとして追記する | `LOG.CORE.020, LOG.CORE.060` |
| `DECISION.JOURNAL.030` | `event_id` と安定した `decision_key`、`stream_id`、`scope` を保持する | `LOG.CORE.030, LOG.CORE.040` |
| `DECISION.JOURNAL.040` | `based_on` / `supersedes` / `correction_of` / `resolution_of` で因果関係を保持する | `DECISION.JOURNAL.030` |
| `DECISION.JOURNAL.050` | 決定権限を確認しない候補・提案を `DECIDED` として記録しない | `DECISION.JOURNAL.010` |
| `DECISION.JOURNAL.060` | 最新時刻・ファイル順だけで決定の優先順位を決めない | `DECISION.JOURNAL.040` |
| `DECISION.JOURNAL.070` | 決定成立 `DECIDED` と正本反映完了 `APPLIED` を分離する | `LOG.CORE.130, LOG.CORE.140` |
| `DECISION.JOURNAL.080` | `APPLIED` はexact target revisionと検証証拠がある場合だけ記録する | `DECISION.JOURNAL.070` |
| `DECISION.JOURNAL.090` | authorityは既存のprojectルールに従い、Journalを暗黙の上位authorityとしない | `DECISION.JOURNAL.010` |
| `DECISION.JOURNAL.100` | 新規判断前に関連する過去判断の有効性・範囲・根拠を照合する。GitHub利用時は関連Closed Issueも対象とする | `DECISION.JOURNAL.030` |
| `DECISION.JOURNAL.110` | 競合検出・統合はConflict Resolution規則に従う | `DECISION.JOURNAL.030` |
| `DECISION.JOURNAL.120` | snapshotは元イベントから検証・再構成可能である | `DECISION.JOURNAL.030` |
| `DECISION.JOURNAL.130` | ログ保存失敗、正本反映失敗、検証失敗を区別し、成功を偽装しない | `LOG.CORE.140` |
| `DECISION.JOURNAL.140` | concurrency対策にatomic append / create-only event / HEAD guardなどを使う | `LOG.CORE.120` |
| `DECISION.JOURNAL.150` | BootstrapまたはProject Localからstore、authority mapping、reader/writer、recoveryへ到達できる | `LOG.CORE.010` |
| `DECISION.JOURNAL.160` | Write Lock、read-only、権限不足では書込みをせず、非canonical draftと区別する | `DECISION.JOURNAL.070` |

## 3. イベントの同一性とscope

`stream_id` はlogical historyの単位、`decision_key` は論点の安定識別子。Issue番号と1対1に固定しない。複数のIssue・仕様が一論点を扱うことがある。

`scope.subject_ref` は対象、`scope.dimensions` はenvironment/platformなどの条件。次元が未指定なら当該次元の全値を含むと解釈する。ただし、範囲や階層など単純な等号判定で表せないprojectでは `scope_resolver_ref` を定義する。解釈不能なら「重ならない」と推測せず `UNKNOWN_OVERLAP` にする。

狭いscopeが広いscopeを自動的に上書きするわけではない。置換には明示的な関係とauthorityが必要。

## 4. Event vocabulary

| Event | 意味 | 必須の追加項目 |
|---|---|---|
| `DECIDED` | 権限ある決定が成立 | `authorized_by` |
| `REJECTED` | 提案を却下。再提案時の先行判断となる | `evidence_refs` または `reason` |
| `DEFERRED` | 保留と再検討条件 | `reason` |
| `NO_CHANGE` | 調査の結果、現行判断を維持 | `based_on`, `reason` |
| `REVOKED` | 明示的な取消 | `supersedes`, `authorized_by` |
| `CORRECTION` | 元イベントの誤記・誤参照を訂正 | `correction_of`, `reason` |
| `CONFLICT_DETECTED` | 競合と当該イベント集合を記録 | `conflict_participants`, `reason` |
| `CONFLICT_RESOLVED` | 統合判断を確定 | `resolution_of`, `conflict_participants`, `resolution_strategy`, `authorized_by` |
| `APPLIED` | 正本へ反映しexact revisionを確認 | `applies_decision`, `target_revision`, `verification_refs` |
| `APPLY_FAILED` | 正本反映失敗または検証未了 | `applies_decision`, `reason` |

提案・観測・テスト結果は、それだけでは`DECIDED`ではない。却下された案も将来の反復調査防止のため履歴を保持する。
`CONFLICT_RESOLVED` は、競合そのものを閉じる決定のイベント。新たな仕様authorityを自動生成するわけではない。

共通必須項目: `schema_version`, `event_id`, `stream_id`, `decision_key`, `event_type`, `occurred_at_utc`, `scope`, `summary`, `authority_ref`, `based_on`, `evidence_refs`。条件付きの項目はイベント型に応じる。具体的なJSON形式は `../../schemas/decision_event.schema.json`。decision event作成時に観測した正本revisionは、取得可能なら`observed_authority_revision`へ記録する。

## 5. Projection（現在状態の導出）

イベントを時刻だけで並べて「後のイベントを採用」してはならない。因果参照を優先し、同時・独立な競合は明示的に扱う。決定と反映を別状態として導出する。

代表状態:
- `DECIDED_NOT_APPLIED`: 決定済み・正本未反映
- `CURRENT`: authorityに照らして現在有効で、必要な反映が検証された
- `PARTIALLY_SUPERSEDED`: 一部scopeが明示的に置換済み
- `SUPERSEDED`: 有効な全scopeが置換済み
- `REVOKED`: 権限ある取消が成立
- `BLOCKED_BY_CONFLICT`: 同じ対象・条件で未解決競合あり
- `APPLY_FAILED` / `UNKNOWN_APPLY`: 正本反映失敗または反映成否未確認
- `REJECTED_HISTORY` / `DEFERRED_HISTORY`: 有効仕様を変更しない履歴

競合中は新しい変更の適用を止めるが、既存production環境を自動停止・巻戻ししない。既存の有効な正本を保持し、対象範囲をblockする。安全上の緊急初動は別のproject規則に従う。

## 6. 永続化・反映・復旧

```text
安定した判断の成立と権限を確認
  -> 対象のauthority / 既存決定を照合
  -> 決定イベントを作成しatomicに永続化
  -> 書き込み確認
  -> 競合判定（未解決なら適用停止）
  -> 正本へ反映（正本側の書込みgateに従う）
  -> exact revisionおよびvalidationを確認
  -> APPLIEDイベントを追記・永続化確認
```

- 決定保存前に失敗した場合は「記録済み」と報告しない。
- 決定イベント保存後、正本の更新に失敗した場合は `APPLY_FAILED` または未反映のままとする。
- 正本の更新後、`APPLIED`の追記が失敗した場合は、`UNKNOWN_APPLY`として実正本を照合し回復する。再実行による二重適用を防ぐ。
- Lock中に要求された変更は、canonical storeやIssueを無断変更しない。local draftは正式イベントではない。
- event IDの同一内容重複はidempotent、異内容はintegrity errorとする。
- Write Ahead Logという語を採用する場合も、DBエンジンのwrite-ahead保証やcrash durabilityを根拠なく主張しない。実際の耐障害性は採用storeで検証する。

## 7. Project Bootstrapと保存方式

採用projectは次の論理役割をProject BootstrapまたはProject Localで解決可能にする。

```yaml
Decision Journal: enabled
Decision Journal Spec: specs/log/DECISION_JOURNAL_PLUGIN_v0.1.md
Decision Log Core: specs/log/LOG_CORE_v1.0.md
Decision Canonical Store: <durable storage locator>
Decision Serialization: <format and schema>
Decision Writer: <create-only / atomic append / serialized writer>
Decision Authority Map: <domain and decision-kind to authority>
Decision Scope Resolver: <strategy / reviewer>
Decision Reader: <canonical reader>
Decision Snapshot: <derived path or N/A>
Decision Recovery: <read/replay/reconcile procedure>
```

Git repositoryなら `decisions/events/<event_id>.json` のcreate-only記録が候補。JSONL、DB、GitHubコメントなどもLOG COREのdurability・immutability・concurrency要件を実際に満たす場合のみ使用できる。編集可能なGitHubコメントを使うなら改変検知・訂正運用を補う必要がある。

Journalを採用しないprojectでも、既存のIssue/AISPEC記録義務は残る。Journal採用は既存historyの一括移行を強制しない。過去記録のbackfillは出典・当時の判断状態・不確実性を保持し、新たな承認を捏造しない。

## 8. 最小検証

1. event idが一意で、訂正が元イベントを消さない。
2. Issue/仕様/ソースから関連する既存decisionへ検索できる。
3. `DECIDED`後に正本反映に失敗しても`CURRENT`にならない。
4. 同じscopeで独立に成立した矛盾を自動上書きしない。
5. 過去の却下・許容判断を検索でき、理由なく再調査しない。
6. snapshotがなくても同じprojected stateを復元できる。
7. Projectのauthorityと既存のLog Coreの安全条件を満たす。
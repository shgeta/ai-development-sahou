# Decision Snapshot & Replay v0.1（共通仕様）

Status: **APPROVED** — 2026-11-19  
Depends on: `DECISION_JOURNAL_PLUGIN_v0.1.md`, `DECISION_CONFLICT_RESOLUTION_v0.1.md`, `LOG_CORE_v1.0.md`

## 1. 目的

Decision Journalのイベント数が増えても、再開時に全履歴を読み直さず現在有効な判断を復元する。
ただしsnapshotは**派生キャッシュであり正本ではない**。失われてもcanonical event集合から同じprojectionを再計算できなければならない。

## 2. 規範ルール

| RULE_ID | 意味 |
|---|---|
| `DECISION.SNAPSHOT.010` | snapshotは検証済みのcanonical event streamから生成された派生物である |
| `DECISION.SNAPSHOT.020` | source storeのexact revisionまたは一意なevent集合manifestを持つ |
| `DECISION.SNAPSHOT.030` | projector / conflict resolverのversionとschema versionを保持する |
| `DECISION.SNAPSHOT.040` | snapshot内容を既存のIssue・仕様のauthorityとして扱わない |
| `DECISION.SNAPSHOT.050` | 破損・不整合・旧versionの場合はsnapshotを破棄し、canonical historyから再計算する |
| `DECISION.SNAPSHOT.060` | 未解決の競合、未反映決定、反映成否不明の状態をsnapshotから消さない |
| `DECISION.SNAPSHOT.070` | 増分再生はsourceのexact event set差分で行い、timestampやID大小比較だけで判定しない |
| `DECISION.SNAPSHOT.080` | snapshot生成中にeventが追加された場合、baselineを再検証してから公開する |
| `DECISION.SNAPSHOT.090` | 同じ入力event集合・project authority・resolver versionから、決定論的に同じstateを再現する |
| `DECISION.SNAPSHOT.100` | eventのcorrectionや既存resolution変更がある場合、影響範囲を再計算する |
| `DECISION.SNAPSHOT.110` | snapshotにはsecretや不要な個人データを複製しない |
| `DECISION.SNAPSHOT.120` | retention / compressionでcanonical eventを通常運用で削除しない |

## 3. Snapshot schema

主な項目:

- `schema_version`, `snapshot_id`, `created_at_utc`
- `source_store_ref`: canonical event storeのURIやlocator
- `source_revision`: Git exact SHA、DB transaction identity等
- `included_event_ids`: 含まれるevent ID集合。外部immutable manifest参照でもよい
- `event_set_sha256`: `event_id` とcanonical event bytesの組を規定順に並べてhash化した値
- `projection_version`, `scope_resolver_version`, `authority_map_revision`
- `current_decisions`: 有効なdecision ID、scope、authority参照、反映状態
- `unresolved_conflicts`: 各競合集合、scope、block理由
- `pending_applications`: DECIDED_NOT_APPLIED / APPLY_FAILED / UNKNOWN_APPLY
- `replay_cursor`: 追加イベント探索に使うsource-specific cursor（単純なlast timestampではない）

厳密な構造は `../../schemas/decision_snapshot.schema.json` を参照。
projectが同じ入力を同じhashへ正規化するためのcanonicalization規則を一意に定義する。ここではSHA-256の利用を例示し、byte serializationを未定義のまま比較結果を保証しない。

## 4. Replay手順

```text
Project Bootstrap -> canonical event store / authority map / readerをresolve
  -> latest snapshot candidate取得
  -> schema / source revision / event set digest / projector versionを検証
  -> validならsnapshot採用、invalidならゼロからreplay
  -> sourceからsnapshot未収録の全eventを列挙
  -> immutable ID / refs / event payloadを検証
  -> based_on / supersedes 等の依存グラフを解決
  -> conflict resolverでscope別にprojection
  -> 現行authorityとcurrent specの不整合をreconcile
  -> unresolved / pendingを含めてstateを提示
```

イベントの順序は「依存関係の先行を優先した安定順」で処理し、独立イベント間では機械的な表示順と意味上の優先を混同しない。循環依存・欠損参照・同一ID異内容はintegrity error。

## 5. 増分更新とcrash recovery

新規eventが発生したら、snapshot以降のevent集合差分をすべて取得して再生する。
複数のwriterが同時に作成したeventはcommit時刻の前後を問わず検出する。
同じ`decision_key`に新たなdecisionが存在すれば競合判定をやり直す。

- snapshot作成途中の中断: 作成途中の成果を公開せず、旧snapshotまたはfull replayを使用。
- included event manifestが読み取れない: snapshotはinvalid。
- projector code/authority mappingが変わった: snapshotをinvalidateするか、等価性を証明してmigration。
- 正本への書込みは完了したがAPPLIED記録が欠落: `UNKNOWN_APPLY` を表示し正本のexact refを再照合。
- 後から過去決定の訂正が追加された: 元イベントは残したまま現在状態を再評価。

## 6. 例

```text
Events:  E001 -> E002 -> E003
Snapshot S003:
  included={E001,E002,E003}
  unresolved={C001}
  current={D001}
  source_revision=<exact revision>

新しいE004,E005が来た:
  S003をverify
  delta={E004,E005} を収集
  E004/E005と関連する決定・scopeを再評価
  S005を生成（canonical元イベントは削除しない）
```

## 7. Validation

1. full replayとvalid snapshot + delta replayのprojectionが一致。
2. event ID・timestampの大小が保存順やpriorityを変えない。
3. 並行書込みで後から確定したeventを取りこぼさない。
4. stale authority map / projection versionのsnapshotを無条件採用しない。
5. 未解決conflict・失敗したapply・unknown applyがsnapshotに残る。
6. snapshotの削除・破損後もcanonical storeから復旧できる。
7. canonical event streamを書き換えたり削除したりしない。
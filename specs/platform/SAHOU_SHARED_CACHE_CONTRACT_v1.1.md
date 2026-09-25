# SAHOU Shared Cache Contract v1.1

- Updated: 2026-09-25
- Status: APPROVED
- Scope: SAHOU repositoryのshared exact-revision snapshot cacheとrouted context loading
- Supersedes for current use: `SAHOU_SHARED_CACHE_CONTRACT_v1.0.md`
- Parent: `AI開発基盤抽象化共通仕様_v1.0.md`

## 1. Authority

SAHOUのauthorityはVersioned Repository上のrepository / ref / exact commit / treeである。

shared cacheはauthorityではなく、同一exact revisionの再取得を避けるread optimizationである。

**snapshot completenessとconversation context loadingは別物とする。**

- cache snapshot: exact repository tree全体を保持してよい
- context load: routingで必要と判断したfile / dependency closureだけを展開する

full snapshotをcacheしていることを理由に、毎sessionで全fileをcontextへloadしない。

## 2. Identity

cache identity:

```text
repository identity + exact commit SHA
```

ref名だけ、timestampだけ、folder名だけでcacheをcurrentと判定しない。

## 3. Required snapshot contents

検証済みsnapshotは最低限次を持つ。

- repository archive
- exact commit SHA
- Git tree SHA
- archive SHA256
- recursive tree manifest
- manifest SHA256
- repository identity
- source ref
- generated / verified timestamp

archiveは対象exact commitのrepository treeを表す。working directoryの未追跡file、session-local file、credential等を混在させない。

## 4. Shared layout

```text
/AI_COMMON/SAHOU/
  current/
    CURRENT.json
  snapshots/
    <exact-commit-sha>/
      repository archive
      MANIFEST.json
      TREE.json
```

`CURRENT.json` は検証済みsnapshotだけを指す。

## 5. Routed resolution

session開始時:

1. authority repositoryのtarget refからexact commit SHAを解決する。
2. shared current metadataを確認する。
3. exact SHA一致かつintegrity validならcache hitとする。
4. miss時のみcurrent exact revisionを取得・検証しsnapshotを更新する。
5. `specs/README_共通仕様セット.md` をrouting indexとして読む。
6. project Bootstrap / current Work Item / actual taskから必要moduleを決める。
7. 選択moduleとその明示dependency closureだけをcontextへloadする。
8. 作業中に新しいtriggerが発生した場合のみ追加moduleをloadする。
9. snapshot全体をcontextへ展開しない。

## 6. Standard routing examples

- ordinary GitHub repository work -> GitHub operation spec
- semantic AISPEC change -> AISPEC + GitHub operation spec
- durable log work -> Log Core
- production Web update log -> Log Core + Web Update Log Plugin
- Research -> Research Core + selected Research plugin
- Safe Commit -> trigger成立時のみ Safe Commit spec/reference
- product adapter -> product固有mappingが必要な時だけ

## 7. Prohibitions

- projectごとに同じSAHOU snapshotを複製しない。
- `SAHOU_FULL.md` 等の派生full bundleをcanonical cacheにしない。
- cache hitを「全specをcontextへloadする指示」と解釈しない。
- stale / revision不明 / integrity不明cacheを使用しない。
- project固有private dataをshared SAHOU namespaceへ入れない。
- optional pluginを無関係なtaskで先読みしない。

## 8. Rotation

通常はcurrent + previous 1世代でよい。

新current snapshotのintegrity確認後にpreviousを整理する。再現性上必要なexact revisionをprojectがpinしている場合、そのrevisionは必要期間保持してよい。

## 9. Validation

shared cacheをcurrentとして採用する前に最低限確認する。

- repository identity一致
- exact commit SHA一致
- Git tree SHA一致
- archive SHA256一致
- manifest SHA256一致
- tree manifestがarchive内容と矛盾しない
- forbidden local/private file混入なし

routed loadではさらに、選択moduleがrouting trigger / Bootstrap / Work Itemと整合することを確認する。

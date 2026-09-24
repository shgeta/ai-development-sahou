# SAHOU Shared Cache Contract v1.0

- Updated: 2026-09-24
- Status: APPROVED
- Scope: SAHOU repositoryを複数project / 複数chatでfull利用するためのshared exact-revision cache
- Parent: `AI開発基盤抽象化共通仕様_v1.0.md`
- ChatGPT mapping: `CHATGPT_ADAPTER_共通仕様_v1.0.md`

## 1. Authority

SAHOUのauthorityはVersioned Repository上のrepository / ref / exact commit / treeである。

shared cacheはauthorityではなく、同一exact revisionの再取得を避けるread optimizationである。

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

Persistent Project Storeがhierarchical pathを提供する場合の標準logical layout:

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

## 5. Resolution

chat / development session開始時:

1. authority repositoryのtarget ref（通常 `main`）からexact commit SHAを解決する。
2. shared current metadataを読む。
3. metadata SHAとauthority SHAが一致する場合、snapshot integrityを確認してfull loadする。
4. SHA不一致、snapshot欠落、hash不一致、manifest不整合、partial snapshotの場合はcache missとする。
5. cache miss時のみcurrent exact revisionを取得する。
6. archive / tree / hash / identityを検証する。
7. 新snapshotを保存する。
8. snapshot保存と検証が成立した後だけcurrent pointerを更新する。
9. full load後、project固有Bootstrap / spec / Current State / Work Itemへ進む。

## 6. Prohibitions

- projectごとに同じSAHOU snapshotを複製しない。
- `SAHOU_FULL.md` 等の派生full bundleをcanonical cacheにしない。
- current pointerだけ作り、snapshot実体がない状態を作らない。
- snapshot検証前にcurrent pointerを先行更新しない。
- stale / revision不明 / integrity不明cacheを使用しない。
- project固有private dataをshared SAHOU namespaceへ入れない。

## 7. Rotation

通常はcurrent + previous 1世代でよい。

新current snapshotのintegrity確認後にpreviousを整理する。再現性上必要なexact revisionをprojectがpinしている場合、そのrevisionは必要期間保持してよい。

## 8. Validation

shared cacheをcurrentとして採用する前に最低限確認する。

- repository identity一致
- exact commit SHA一致
- Git tree SHA一致
- archive SHA256一致
- manifest SHA256一致
- tree manifestがarchive内容と矛盾しない
- forbidden local/private file混入なし

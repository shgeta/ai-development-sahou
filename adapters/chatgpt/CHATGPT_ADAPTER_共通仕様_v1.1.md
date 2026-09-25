# ChatGPT Adapter 共通仕様 v1.1

- Updated: 2026-09-25
- Status: APPROVED
- Parent model: `AI開発基盤抽象化共通仕様_v1.0.md`
- Scope: ChatGPT固有機能をlogical platform rolesへmappingするAdapter

## Mapping

| Logical role | ChatGPT implementation |
|---|---|
| Persistent Project Store | ChatGPT Library が利用可能な環境では ChatGPT Library |
| active Current State storage | ChatGPT Library内のproject-specific state files が利用可能な場合 |
| conversation input stream | ChatGPT chat / voice / interactive session |
| connected external systems | Plugins / connectors / connected apps（利用可能なもののみ） |
| local working copy | ChatGPTのcontainer / working runtimeが提供される場合のsession-local filesystem |

## Rule

共通仕様中の `Persistent Project Store` を、常にChatGPT Libraryが存在すると読み替えてはならない。

ChatGPT Adapterを使用し、かつChatGPT Libraryが利用可能な環境では、projectのCurrent State、再利用価値のあるinput、snapshot、artifact等をChatGPT Libraryへ保存してよい。

ChatGPT Libraryが利用できない環境では、その存在を仮定せず、projectが使用する別のPersistent Project Storeまたはrepository/artifact storeへfallbackする。

公開仕様では `Library` 単独ではなく、製品固有機能を指す場合は `ChatGPT Library` と明記する。

## Shared cache mapping

ChatGPT Libraryが利用可能な環境では、複数project / 複数chatで共通利用するauthorityのexact repository snapshotを、project-specific folderではなく**shared cache領域**へ保存してよい。

SAHOU共通仕様repositoryを利用する場合の標準例:

```text
/AI_COMMON/SAHOU/
  current/
    CURRENT.json
  snapshots/
    <exact-commit-sha>/
      repository snapshot
      manifest
```

運用:

1. chat開始時にSAHOU repositoryのcurrent target ref（通常は `main`）のexact commit SHAを確認する。
2. `CURRENT.json` または同等metadataとauthority SHAを照合し、snapshot integrityを確認する。
3. cache miss / SHA変更時のみGitHub等のVersioned Repositoryからcurrent exact repository snapshotを再取得・検証する。
4. `specs/README_共通仕様セット.md` をrouting indexとして読む。
5. PROJECT BOOTSTRAP / current Work Item / actual taskから必要moduleを選び、selected module + dependency closureだけをconversation contextへloadする。
6. shared cacheにrepository snapshot全体が存在しても、それを理由にfull context loadしない。
7. 新snapshotのidentity / manifest / integrity確認後にshared current pointerを更新する。
8. `SAHOU_FULL.md` のような派生統合fileをcanonical cacheとして作らない。cache対象はrepository snapshotそのものとする。
9. projectごとにSAHOU cacheを複製しない。同一repository identity + exact revisionなら全projectで同じshared snapshotを再利用する。
10. project固有State / private rule / inputは `/AI_COMMON/SAHOU/` に混在させない。
11. ChatGPT Libraryが利用できない場合は、同等のshared Persistent Project Storeへmappingするか、毎回authorityからexact revisionを取得する。

このshared cacheはChatGPT LibraryをSAHOUのauthorityへ昇格させるものではない。SAHOU repositoryのref / commit / treeがauthorityである。

# ChatGPT Adapter 共通仕様 v1.0

- Updated: 2026-09-24
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
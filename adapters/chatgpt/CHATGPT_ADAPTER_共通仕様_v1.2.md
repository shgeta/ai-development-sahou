# ChatGPT Adapter 共通仕様 v1.2

- Updated: 2026-10-06
- Status: APPROVED
- Parent model: `AI開発基盤抽象化共通仕様_v1.2.md`
- Supersedes: `ChatGPT Adapter 共通仕様 v1.1`
- Decision: `shgeta/ai-development-sahou#32`
- Scope: ChatGPT固有機能をlogical platform rolesへmappingするAdapter

## Mapping

| Logical role | ChatGPT implementation |
|---|---|
| Persistent Project Store | ChatGPT Library が利用可能な環境では ChatGPT Library |
| Task Staging Store candidate | ChatGPT Library が利用可能な環境では ChatGPT Library を既定候補として評価する。production利用にはProject Local Adapter + scheduled acceptance + valid certificationが必要 |
| active Current State storage | ChatGPT Library内のproject-specific state files が利用可能な場合 |
| conversation input stream | ChatGPT chat / voice / interactive session |
| connected external systems | Plugins / connectors / connected apps（利用可能なもののみ） |
| local working copy | ChatGPTのcontainer / working runtimeが提供される場合のsession-local filesystem |

## Task Staging Store mapping

ChatGPT環境でTask Staging Storeが未設定の場合、ChatGPT Libraryが利用可能なら `PLATFORM.STORE.STAGING` の**既定候補**として最初に評価する。

これは「ChatGPT Libraryを自動的にwrite先として承認する」ことを意味しない。

### Semantic rules

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| `ADAPTER.CHATGPT.STAGING.010` | Library default candidate | RULE | ChatGPT Libraryが現在環境で利用可能で、Task Staging Storeが未設定なら、Libraryを最初のproduct-specific candidateとして評価する | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.020` | Candidate is not certification | PROHIBITION | Libraryが見える・読める・過去に書けたという事実だけでstaging eligible / READY / certifiedと扱わない | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.030` | Existing certified Adapter wins | REQUIREMENT | Project Localにvalid certification付きTask Staging Adapterがある場合はそれを使用し、各taskごとにLibrary候補探索へ戻らない | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.040` | Setup and acceptance required | REQUIREMENT | Libraryをcandidateとして選ぶ場合もTask Staging Store AISPECに従い、runtime eligibility確認、environment-specific Adapter生成、scheduled Test Task、acceptance、certificationを行う | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.050` | Fallback after unavailable or fail | REQUIREMENT | Libraryが利用不可、runtime eligibility FAIL、scheduled acceptance FAILのいずれかなら、Libraryをproduction stagingとして使わず、他のeligible noncanonical candidateを探索する | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.060` | No canonical fallback | PROHIBITION | staging candidateが得られないことを理由にrepository / Issue / canonical evidence等へ代替writeしない | APPROVED | `shgeta/ai-development-sahou#32` |
| `ADAPTER.CHATGPT.STAGING.070` | Project Local binding | REQUIREMENT | 選択・検証済みのconcrete staging destination、Adapter identity、certificationをProject Localから再発見可能にする | APPROVED | `shgeta/ai-development-sahou#32` |

### Resolution flow

```text
valid Project Local Task Staging Adapter?
  YES -> use certified Adapter
  NO
    -> ChatGPT Library available now?
         YES -> evaluate Library as default candidate
                 -> eligible?
                    YES -> generate Project Local Adapter
                            -> scheduled acceptance
                            -> PASS -> certification READY -> production use
                            -> FAIL -> do not use; explore other candidates
                    NO  -> explore other candidates
         NO  -> explore other candidates
```

ChatGPT Libraryはproduct-level candidate mappingであり、projectごとのconcrete Adapter / destination identity / certificationはProject Localに保持する。

## Rule

共通仕様中の `Persistent Project Store` を、常にChatGPT Libraryが存在すると読み替えてはならない。

ChatGPT Adapterを使用し、かつChatGPT Libraryが利用可能な環境では、projectのCurrent State、再利用価値のあるinput、snapshot、artifact等をChatGPT Libraryへ保存してよい。

ChatGPT Libraryが利用できない環境では、その存在を仮定せず、Persistent Project Storeについてはprojectが使用する別storeへfallbackする。Task Staging Storeについてはcanonical authorityへfallbackせず、`TASK_STAGING_STORE_AISPEC_v1.1.md` に従って別のeligible noncanonical candidateを探索する。

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


## Task staging acceptance boundary

ChatGPT AdapterはLibraryをdefault candidateとして提示するところまでをproduct-specific defaultとする。

production用Task Staging Storeとしての採用authorityは `TASK_STAGING_STORE_AISPEC_v1.1.md` にある。durable outputを持つproduction scheduled taskはcreate/re-enable前にvalid certification付きAdapterを解決し、未certifiedならseparate Test Task acceptanceを先に完了する。加えて最低限次を満たす必要がある。

- current runtimeでwrite capabilityが利用可能
- per-actionの追加認証・追加承認・人間対話を要求しない
- noncanonical
- probe write / rediscovery / read-backが成立
- scheduled executionでacceptance済み
- persistenceを主張する場合はcross-run確認済み
- valid certification leaseがProject Localから解決可能

manual chatでLibraryへ書けたことはscheduled acceptanceの代替にしない。

production write failure時は既存certificationをINVALID / REVALIDATE対象とし、成功保存として報告しない。

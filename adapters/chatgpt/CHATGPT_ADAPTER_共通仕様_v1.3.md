# ChatGPT Adapter 共通仕様 v1.3

- Updated: 2026-10-06
- Status: APPROVED
- Parent model: `AI開発基盤抽象化共通仕様_v1.2.md`
- Supersedes: `ChatGPT Adapter 共通仕様 v1.2`
- Decision: `shgeta/ai-development-sahou#36`
- Scope: ChatGPT固有機能をlogical platform rolesへmappingするAdapter

## Mapping

| Logical role | ChatGPT implementation |
|---|---|
| Persistent Project Store | ChatGPT Library が利用可能な環境では ChatGPT Library |
| Task Staging Store default fallback | ChatGPT Library が利用可能な環境では ChatGPT Library を既定のnoncanonical fallbackとして使用してよい。valid certified Project Local Adapterがあればそちらを優先する |
| active Current State storage | ChatGPT Library内のproject-specific state files が利用可能な場合 |
| conversation input stream | ChatGPT chat / voice / interactive session |
| connected external systems | Plugins / connectors / connected apps（利用可能なもののみ） |
| local working copy | ChatGPTのcontainer / working runtimeが提供される場合のsession-local filesystem |

## Task Staging Store mapping

ChatGPT環境でvalid certified Task Staging Adapterが解決できない場合、ChatGPT Libraryが現在利用可能かつwrite可能なら `PLATFORM.STORE.STAGING` の**環境default noncanonical fallback**として使用してよい。

これはLibraryをcertified stagingやcanonical authorityへ昇格させることを意味しない。

### Semantic rules

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| `ADAPTER.CHATGPT.STAGING.010` | Library default fallback | RULE | valid certified Task Staging Adapterがなく、ChatGPT Libraryが現在環境で利用可能かつwrite可能なら、Libraryをproduct-specific default noncanonical fallbackとして使用してよい | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.020` | Fallback is not certification | PROHIBITION | Libraryへのfallback write成功をREADY certificationやcanonical ingestionとして扱わない | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.030` | Existing certified Adapter wins | REQUIREMENT | Project Localにvalid certification付きTask Staging Adapterがある場合はそれを優先し、fallbackへ戻らない | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.040` | Runtime fallback safety | REQUIREMENT | Library fallbackはcurrent runtimeでwrite capabilityが利用可能、追加human interaction不要、noncanonicalの最低条件を満たす場合に限る | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.050` | Continue and certify later | RULE | Library fallbackでtaskを継続しつつ、environment-specific Adapter生成・scheduled Test Task・acceptance・certificationを別途進めてよい | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.060` | No canonical fallback | PROHIBITION | Libraryが利用不可またはwrite失敗でもrepository / Issue / canonical evidence等へ自動fallback writeしない | APPROVED | `shgeta/ai-development-sahou#36` |
| `ADAPTER.CHATGPT.STAGING.070` | Project Local binding after certification | REQUIREMENT | scheduled acceptanceをPASSしたconcrete destination、Adapter identity、certificationをProject Localから再発見可能にし、その後の実行で優先利用する | APPROVED | `shgeta/ai-development-sahou#36` |

### Resolution flow

```text
valid Project Local Task Staging Adapter?
  YES -> use certified Adapter
  NO
    -> ChatGPT Library available + writable now?
         YES -> save as DEFAULT_FALLBACK_SAVED
                -> continue task
                -> separately run Adapter setup / scheduled acceptance
                -> PASS -> future runs use certified Adapter
         NO  -> explore other eligible noncanonical fallback
                -> none -> SAVE_FAILED
```

ChatGPT Libraryはproduct-level default fallback mappingである。fallback利用自体にProject Local certificationは必須ではないが、certificationを取得した後のconcrete Adapter / destination identity / certificationはProject Localに保持する。

## Rule

共通仕様中の `Persistent Project Store` を、常にChatGPT Libraryが存在すると読み替えてはならない。

ChatGPT Adapterを使用し、かつChatGPT Libraryが利用可能な環境では、projectのCurrent State、再利用価値のあるinput、snapshot、artifact等をChatGPT Libraryへ保存してよい。

ChatGPT Libraryが利用できない環境では、その存在を仮定せず、Persistent Project Storeについてはprojectが使用する別storeへfallbackする。Task Staging Storeについてはcanonical authorityへfallbackせず、`TASK_STAGING_STORE_AISPEC_v1.2.md` に従って別のeligible noncanonical candidateを探索する。

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

ChatGPT AdapterはLibraryをdefault noncanonical fallbackとして定義する。valid certified Adapterがないことだけを理由にscheduled / unattended taskを停止しない。

fallback利用のauthorityは `TASK_STAGING_STORE_AISPEC_v1.2.md` にある。Library fallbackを使うrunでは最低限次を満たす必要がある。

- current runtimeでwrite capabilityが利用可能
- per-actionの追加認証・追加承認・人間対話を要求しない
- noncanonical
- 保存結果を `DEFAULT_FALLBACK_SAVED` としてcertified/canonical状態から区別する
- 可能ならunique identity / no implicit overwrite / read-backを行う
- certification取得後はProject Localのcertified Adapterを優先する

manual chatでLibraryへ書けたことはscheduled acceptanceの代替にしない。ただしscheduled acceptance未完了でも、runtime fallback最低条件を満たすLibraryへのnoncanonical退避は許可する。

fallback write failure時は成功保存として報告せず、他のeligible noncanonical fallbackを探索する。certified Adapter経由のproduction write failure時は既存certificationをINVALID / REVALIDATE対象とする。

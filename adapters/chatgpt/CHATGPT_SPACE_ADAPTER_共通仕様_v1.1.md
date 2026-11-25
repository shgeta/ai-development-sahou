# ChatGPT Space Adapter 共通仕様 v1.1

- Updated: 2026-11-25
- Supersedes: `CHATGPT_SPACE_ADAPTER_共通仕様_v1.0.md`
- Status: APPROVED
- Parent model: `AI開発基盤抽象化共通仕様_v1.2.md`
- Decision: `shgeta/ai-development-sahou#43`; prior #41 retained
- Scope: ChatGPT Space / Page / Page attachment capability mapping
- Independent of: `CHATGPT_ADAPTER_共通仕様_v1.3.md` (Library Adapter; not superseded)
- Sources (product facts): [Getting started with Space](https://help.openai.com/en/articles/20001549-getting-started-with-space-in-chatgpt), [Sharing, data, and controls](https://help.openai.com/en/articles/20001544-chatgpt-space-sharing-data-and-controls)

## 1. Mapping

SpaceはPage、file、folder等を整理・共有するChatGPTの機能である。利用可能なアカウントではUI上のLibraryを置き換えるが、既存Library操作経路が必ず消滅した、または全操作がSpace Page APIと等価になったとは解釈しない。ChatGPT Projectsとも別である。実際のoperation availabilityはcurrent runtimeで解決する。

| Logical role | Space implementation candidate |
|---|---|
| `PLATFORM.STORE.PERSISTENT` | 検証済みSpace / Page branch / file storage destination |
| active Current State | projectにbindingされたPageまたはfile。必要な表現・revision guardを満たすもの |
| reusable input / artifact | 元fileの保存・再取得が可能なfile destination、または適合するPage reference |
| shared exact-revision cache | exact bytes / manifest / metadataを回収・検証できる適格destinationのみ |
| `PLATFORM.STORE.STAGING` | runtimeで非対話write / rediscovery / read-back可能な、noncanonicalに分離されたdestination |

Product Adapter selectionは共通仕様セットREADME §2.2、staging semanticsはTask Staging Store AISPEC v1.2、cache semanticsはShared Cache Contract v1.1、project-specific bindingはEffective SAHOUをauthorityとする。

## 2. Identity and capability

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| ADAPTER.SPACE.010 | Independent route | REQUIREMENT | SpaceはLibrary Adapterの新版ではない。既存bindingを先に解決し、現在の操作能力に基づき選択する | APPROVED | #41 |
| ADAPTER.SPACE.020 | Stable destination identity | REQUIREMENT | Space、root Page、parent Page、target Page、file/attachment identityを区別し、必要なaccount/workspace scope、stable ID/reference、logical project identityをbindingする。表示名・logical pathのみでwriteしない | APPROVED | #41 |
| ADAPTER.SPACE.030 | Runtime capability | GATE | current runtimeで目的operation、対象payload、format/size limit、権限、revision guard、再取得経路を確認する。UI提供・契約・manual chat成功をscheduled operation availabilityの証明にしない | APPROVED | #41 |
| ADAPTER.SPACE.040 | Reuse before create | REQUIREMENT | existing destinationをIDまたは既存locatorで発見し、scopeとaccessを照合する。同名候補の曖昧性は解消するまでwriteしない。既存backing resourceを重複作成しない | APPROVED | #41 |
| ADAPTER.SPACE.050 | Explicit migration | PROHIBITION | UI改名、未解決locator、write失敗を理由に既存データの移行・削除・移動・複製・権限拡張を自動実行しない | APPROVED | #41 |

Concrete bindingの例 (synthetic logical fields; IDを推測して作らない):

```yaml
adapter: chatgpt-space@1.1
role: PLATFORM.STORE.PERSISTENT
project_identity: example-org/example-repo
workspace_scope: <observed account/workspace scope>
space_id: <verified Space ID or N/A>
root_page_id: <verified Page ID or N/A>
target_page_id: <verified Page ID or N/A>
file_locator: <verified file reference or N/A>
logical_path: <logical location>
space_display_name: <observed display name or N/A>
representation: page-markdown | exact-file
```

必要なIDは現在のlisting / get / read結果または検証済みbindingから取得する。Page IDとSpace IDを互換としない。paginationを処理し、結果がpartialなら不存在と断定しない。個人領域・workspace-private領域・共有Spaceを同一scopeとしない。既存のfile/folderを扱う場合は、対応するfile操作経路も候補として解決する。

### Operation capability map

以下はlogical operationと実行時に確認するSpace capabilityの対応であり、固定tool名や全runtimeでの提供を保証しない。

| Operation | Required capability / guard |
|---|---|
| Resolve / list | 許可されたSpace / Page / file discovery、pagination、stable identity照合 |
| Read Page | 対象Pageと必要なcontent / revision metadataの取得 |
| Create Page | 認可されたparent / Space内でのcreate、unique identityまたはidempotency、再発見 |
| Update Page | 対象限定のedit / patch、fresh block/hashまたはrevision guard、conflict検出 |
| Write file | 対象payloadの元byteを保存可能なfile operation、format/size、file identity確認 |
| Read file | 目的に必要なrepresentationを取得。exact-file用途では元byte再取得とhash照合 |
| Delete / rotate | 対象identity・削除権限・明示されたlifecycle policyを確認。current pointerと検証済み新snapshotを確保するまでは旧snapshotを削除しない |
| Inspect access | Page/Spaceと対象fileの必要なaccess情報・ancestor・workspace policyを確認 |
| Change access / move | 保存とは別のoperation。明示的な意図、権限、影響範囲、結果の確認が必要 |

必要なoperationが利用不能なら、そのroleについて不適格とし、適格な代替routeまたはunsupportedを返す。他roleの対応可否は独立して判定する。

## 3. Access boundary

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| ADAPTER.SPACE.ACCESS.010 | Effective access | GATE | Page/Spaceのdirect access、parent/Spaceからのinherited access、workspace policyを考慮し、payloadの許容共有範囲と照合する。読み取り可能であることを編集許可またはprivate性とみなさない | APPROVED | #41 |
| ADAPTER.SPACE.ACCESS.020 | No implicit sharing | PROHIBITION | 保存のためだけにshare grantの追加、link access変更、共有ancestor配下への移動、外部招待を行わない。共有変更には明示された意図と権限を要求する | APPROVED | #41 |
| ADAPTER.SPACE.ACCESS.030 | File boundary | REQUIREMENT | Pageへuploadしたfileのaccess scopeと既存file/link先の独立accessを区別する。Pageを読めても参照fileを読めるとは限らない。copy/summaryもPage閲覧者への開示になる | APPROVED | #41 |
| ADAPTER.SPACE.ACCESS.040 | Unknown access | SAFETY | access情報が欠落・不完全・取得不可で、payloadに必要な共有境界を確認できないときはそのdestinationへのwriteをしない。既知の適格なprivate store等へfallbackするかunsupportedを明示する | APPROVED | #41 |

既存の認可済み保存先を使用する場合も、runtimeで権限を再確認する。直接grantを削除してもinherited grantが残り得る。Spaceやparentの権限変更、Page移動は共有範囲を変え得る。共有設定自体にrevision preconditionがない操作では権限変更を保存transactionの一部とみなさない。

## 4. Representation and safe write

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| ADAPTER.SPACE.WRITE.010 | Page vs file | REQUIREMENT | 編集可能なPage内容と元fileのexact bytesを区別する。Page-native Current State等にはPageを選べるが、archive、元file、exact byte/hashを要求するpayloadはbyte-preserving file operationを使用する | APPROVED | #41 |
| ADAPTER.SPACE.WRITE.020 | Guarded page update | REQUIREMENT | 既存Pageを更新する前にfresh readを行い、返却されたblock ID/hashまたは利用可能なrevision guardで対象を限定する。concurrent edit/conflict時はread・reconcileし、盲目的な全置換をしない | APPROVED | #41 |
| ADAPTER.SPACE.WRITE.030 | Create and unknown outcome | SAFETY | create-onlyまたはidempotent identityを使い、応答不明・部分成功時は再発見とread-backで結果を照合する。確認なしの再create/overwriteや同じmutationの再送をしない | APPROVED | #41 |
| ADAPTER.SPACE.WRITE.040 | Byte verification | GATE | exact-file roleはfile保存と元byte再取得、payload digest/size、manifest照合が可能な場合のみ満たす。抽出text、Page Markdown、metadataだけをexact archiveの代替にしない | APPROVED | #41 |
| ADAPTER.SPACE.WRITE.050 | Read-back | REQUIREMENT | 保存後はstable destinationから対象identity・payloadを読み戻し、必要なrepresentationに応じて内容/hashを照合する。書込み受付だけを保存完了と報告しない | APPROVED | #41 |

Page作成は利用可能なidempotency key/unique operation identityを保持する。Page編集は対象blockに限定してpatchし、必要な構造変更だけを適切なoperationで行う。Page変更前後のsequence/hash等はAPIが提供する範囲で使い、guardがない操作にguardがあると仮定しない。write後にread-backできない場合は未確認として扱う。

Page attachmentのupload、参照の挿入、file取得は別operationになり得る。各結果のidentity・permission・commit状態を区別する。file readが抽出textのみ、binary format非対応、size上限超過等の場合はexact-file roleに不適格とし、許可された別file経路またはVersioned Repositoryからexact revisionを再取得する。Pageへarchiveの文字列表現や要約を保存してcache検証済みと扱わない。

## 5. Logical layout / cache

Common GitHub work specのproject root / Current State / reusable snapshot layoutはlogical layoutである。Spaceにmappingする場合は安定したPage/file identityへの対応をProject LocalまたはBootstrapから辿れるようにする。file hierarchyをPage hierarchyへ機械的に変換する必要はない。shared exact-SHA cacheではShared Cache Contract v1.1のidentity、manifest、hash、CURRENT pointer、rotationを維持する。project固有Stateやprivate inputsを共通cacheに混在させない。exact byte取扱いが検証できない場合は別の適格storeを用いるかauthorityから再取得する。

### 5.1 Project Space display name

Common GitHub work spec v1.19 §4.5 defines the logical project root. Space mapping MUST follow that rule; product-specific naming does not redefine project identity.

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| ADAPTER.SPACE.NAME.010 | New project Space name | REQUIREMENT | 新規のproject専用Spaceを作成する場合、明示的なProject Local overrideがなければ、解決済みlogical project rootの末尾segmentをSpace表示名として使用する。misc内の独立案件では `<owner>__misc__<project-slug>`、repoなしでは `project__<project-slug>` とする | APPROVED | #43 |
| ADAPTER.SPACE.NAME.020 | Identity before display name | SAFETY | stable IDと既存bindingを優先する。表示名は発見用hintでありwrite authorityではない。名前の相違だけで既存Spaceを自動rename / migrate / duplicateしない。共有Space内のPage/file mappingはこの表示名規則の対象外 | APPROVED | #43 |
| ADAPTER.SPACE.NAME.030 | Explicit rename | GATE | 既存Spaceの明示的renameは現在のoperation availability、同一Space ID、権限、衝突、access boundaryを確認し、rename後に同じIDと表示名をread-backする。操作不可なら既存bindingを維持して未変更を明示し、新規Spaceやroot Pageの改名で代替しない | APPROVED | #43 |

| Logical project root (synthetic) | New dedicated Space display name |
|---|---|
| `/GitHubRepos/example-org__sample-tool/` | `example-org__sample-tool` |
| `/GitHubRepos/example-org__misc__sample-analysis/` | `example-org__misc__sample-analysis` |
| `project__sample-analysis/` | `project__sample-analysis` |

衝突解決済みのlogical rootではstable suffixを含む末尾segmentを使用する。Bootstrap / Project Localへlogical rootとSpaceのstable ID、root Page ID、観測した表示名をbindingする。misc内の複数Issueは同じproject slug / Space bindingを再利用する。repository-level exact snapshotはproject Space名から独立したrepository-level locatorで管理する。既存binding、version pin、certificationの扱いは従来の規則に従う。表示名変更だけを理由に既存のcertificationを移行しない。

## 6. Task Staging Store

Spaceは**現在のscheduled runtimeで適格な場合に限り**product-specific default noncanonical fallback候補になる。

| RULE_ID | TITLE | TYPE | MEANING | STATUS | DECISION_REF |
|---|---|---|---|---|---|
| ADAPTER.SPACE.STAGING.010 | Certified route first | REQUIREMENT | valid certified Project Local Adapterを優先し、Space UIの導入やmanual write成功を理由に変更しない | APPROVED | #41 |
| ADAPTER.SPACE.STAGING.020 | Eligible fallback | GATE | certificationがない/無効の場合、noncanonical isolation、権限、現在の非対話write、再発見・read-back、payload representation、append safetyを確認できるSpace destinationに限りfallback候補とする | APPROVED | #41 |
| ADAPTER.SPACE.STAGING.030 | Distinct result states | PROHIBITION | Space fallback成功は `DEFAULT_FALLBACK_SAVED` とし、READY certification、canonical ingestion、FLUSHEDと混同しない。未確認/失敗を成功と報告しない | APPROVED | #41 |
| ADAPTER.SPACE.STAGING.040 | Revalidation and failure | REQUIREMENT | destination、Adapter、権限、runtime、capability等の変更やproduction write failureではTask Staging Store AISPECのINVALID/REVALIDATE条件を適用する。別のeligible noncanonical候補がなければSAVE_FAILEDとし、canonical authorityへ自動writeしない | APPROVED | #41 |

scheduled Test Taskによるacceptanceは別途実行する。probeのunique identity、実際の非対話write、次runでのrediscovery/read-back、payload checksum、append/duplicate safety、failure reporting、canonical isolationを検証する。Library certificationをSpaceへ引き継がず、具体的なdestinationとAdapter versionに対しProject Localに保持する。既存certified Library routeが実際に変化していなければUI改名だけで無効化しない。

## 7. Validation scenarios (synthetic; not production certification)

| Scenario | Expected |
|---|---|
| Library-only runtime | Library v1.3と既存locatorを使用 |
| Space-only runtime / new Page-native state | accessとguardを検証してSpace locatorをbinding |
| New dedicated repo project Space | logical root末尾の `example-org__sample-tool` を表示名として使用 |
| New misc projects with distinct slugs | `example-org__misc__sample-analysis` と `example-org__misc__sample-tool` は別binding |
| Multiple Issues within one misc project | 同じslug・Space IDを再利用。IssueごとのSpaceを作らない |
| New project without repository | `project__sample-analysis` を表示名として使用 |
| Naming collision between independent projects | 別案件であることを確認してstable suffixを初回に確定し、以後再利用 |
| Existing bound Space has different name | stable IDとaccessを確認して再利用。自動rename / duplicateなし |
| Explicit rename operation unavailable | 旧表示名とstable bindingを維持して未変更を明示 |
| misc project moves to a dedicated repository | 明示的な移行判断とidentity/access/read-back確認まで既存bindingを保持 |
| Multiple misc projects need one repository snapshot | repository-level snapshot locatorを共用し、案件別rootに複製しない |
| Both surfaces / already-bound project | 既存の適格bindingを保持。same backing resourceを二重保存しない |
| Existing Library locator cannot resolve | migration/createを自動実行しない。明示的な未解決報告、必要なら安全なnoncanonical fallback |
| Shared parent / unknown inherited access | payload許容範囲を確認できなければwrite不可 |
| Existing linked file not readable | Page accessからfile accessを推定しない |
| Concurrent Page change or unknown write | fresh read / reconciliation、duplicate/overwriteなし |
| Binary snapshot unsupported or only extracted text | exact cache不適格、別file routeまたはauthority取得 |
| Scheduled runtime cannot write/read back or requires approval | fallback不適格。別候補またはSAVE_FAILED |
| Valid certified Library route and eligible Space | certified Library routeを優先 |
| Actual destination/permission/runtime changes | certification再検証。移行は明示判断とread-backが必要 |
| Noncanonical fallback succeeds | DEFAULT_FALLBACK_SAVED。canonical ingestionと区別 |

本仕様のreview PASSは個別environmentのruntime acceptanceではない。actual Space/Libraryへの書込み、ACL変更、data migration、scheduled certificationはそれぞれ別の実行・検証を要する。

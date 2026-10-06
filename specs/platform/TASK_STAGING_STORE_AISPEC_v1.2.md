# Task Staging Store AISPEC v1.2

- Updated: 2026-10-06
- Status: APPROVED
- Supersedes: `Task Staging Store AISPEC v1.1`
- Decision: `shgeta/ai-development-sahou#36`
- Scope: scheduled / unattended task が canonical authority を直接変更せず、追加の人間対話なしに結果を永続化するための staging store 選定・Adapter生成・検証・certification
- Relation: AI開発基盤抽象化 / SAHOU Project Local / Product Adapter / PROJECT_BOOTSTRAP

## 1. Purpose

Task Staging Store は、scheduled / unattended task が結果を一時的・非canonicalに永続化するための論理storage roleである。

主目的は、scheduled / unattended taskの結果を失わずnoncanonicalに退避できることと、繰り返し利用する保存経路をenvironment-specific Adapterとして検証・固定できることの両立である。valid certified Adapterがない場合でも、現在environmentが定義するdefault noncanonical storeへ書き込めるなら、未certified fallbackとして結果を退避してよい。

stagingはcanonical ingestionの代替ではない。

## 2. Core invariants

```text
STAGING_ARTIFACT != CANONICAL_AUTHORITY
DEFAULT_FALLBACK_SAVED != CERTIFIED_STAGING_SAVED
DEFAULT_FALLBACK_SAVED != CANONICAL_INGESTED
CERTIFIED_STAGING_SAVED != CANONICAL_INGESTED
STAGING_SAVED != CANONICAL_INGESTED
TASK_COMPLETED != CANONICAL_INGESTED
NEW_IN_THIS_RUN != NEW_TO_CANONICAL_AFTER_RECONCILIATION
TIMESTAMP_NEWER != NOT_YET_INGESTED
```

stagingへ保存されたという事実だけで、canonical data / canonical evidence / canonical spec / canonical logへ反映済みと扱ってはならない。

## 3. Semantic rules

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | WHEN | UNLESS | TARGET | GROUP | ORDER | STATUS | DECISION_REF |
|---|---|---|---|---|---|---|---|---|---:|---|---|
| `PLATFORM.STAGING.010` | Runtime eligibility | REQUIREMENT | staging store候補は、そのruntime executionにおいてwrite capabilityが現在利用可能で、追加認証・追加承認・人間対話を要求せず、canonical authorityではない場合にのみeligibleとする | scheduled / unattended runtime | staging destinationを選定・利用するとき | - | candidate store | `STAGING_SETUP` | 10 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.020` | Permission non-inference | PROHIBITION | 過去chatの許可、過去のwrite成功、project ownership、repository write access、task作成時の承認、記憶されたuser preferenceを現在runtimeのwrite permissionとして推定しない | all task staging | permission/capabilityを判定するとき | - | runtime authorization judgment | `STAGING_SETUP` | 20 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.030` | Setup/runtime separation | REQUIREMENT | human interactionを期待できるsetup/adaptation phaseと、human interactionを期待しないruntime phaseを分離する | adapter lifecycle | staging Adapterを新設・変更するとき | - | staging workflow | `STAGING_SETUP` | 30 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.035` | Interaction axes | REQUIREMENT | `HUMAN_INTERACTION_AVAILABLE` と `HUMAN_INTERACTION_EXPECTED` を別々に判定する。unattended runtimeでは `HUMAN_INTERACTION_EXPECTED=false` かつ Adapterがhuman interactionを要求しないことを必要とし、available=false / expected=true は不整合として扱う | setup and runtime classification | execution modeを判定するとき | - | execution interaction mode | `STAGING_SETUP` | 35 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.CREATE.010` | Persistence intent classification | REQUIREMENT | production scheduled / unattended taskを作成または再有効化する前に、そのtaskがdurable resultの保存を必要とするかを分類する。read-only / no durable outputはstaging N/Aとしてよい | task creation / re-enable | production taskをcreate/enableするとき | separate Adapter Test Task | production task intent | `STAGING_CREATION` | 10 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.CREATE.020` | Certified Adapter preferred | REQUIREMENT | durable outputを必要とするproduction taskは、create/enable時にProject Localからvalid certification付きTask Staging Adapterをまずresolveし、存在すればそれを優先する | task creation / re-enable | persistence required | - | staging route selection | `STAGING_CREATION` | 20 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.CREATE.030` | Missing certification does not discard work | PROHIBITION | valid certificationがないことだけを理由に、探索・調査・production taskを停止、無効化、または結果破棄してはならない。environment default noncanonical fallbackが利用可能ならその経路で継続する | task creation / runtime | persistence required and no valid certification | no writable noncanonical fallback exists | task continuity | `STAGING_CREATION` | 30 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.CREATE.040` | Certification remains separate | SEQUENCE | uncertified fallbackを利用してtaskを継続してよいが、concrete Adapterのcertificationはseparate scheduled Test Taskで独立に進め、PASS後の実行からcertified routeを優先する | adapter acceptance | no valid certification | scheduled execution機能自体が存在しない場合 | certification lifecycle | `STAGING_CREATION` | 40 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.CREATE.050` | Re-enable uses current route selection | REQUIREMENT | disabled production taskを再有効化する場合もvalid certified Adapterをまず確認し、なければenvironment default noncanonical fallbackの有無を確認してrouteを決める | task re-enable | enable transition | read-only / no durable output | task enable transition | `STAGING_CREATION` | 50 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.FALLBACK.010` | Environment default fallback | REQUIREMENT | valid certified Adapterがないruntimeでは、product/environment Adapterが定義するdefault noncanonical staging storeが現在write可能なら、結果をそこへ退避してよい | scheduled / unattended runtime | durable output and no valid certification | - | default fallback store | `STAGING_FALLBACK` | 10 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.FALLBACK.020` | Fallback minimum safety | REQUIREMENT | default fallback保存には少なくともcurrent runtimeでwrite可能、追加human interaction不要、noncanonicalを要求する。可能ならunique identity、no implicit overwrite、read-backを行う | fallback runtime | default fallbackを使うとき | - | fallback write | `STAGING_FALLBACK` | 20 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.FALLBACK.030` | Fallback state labeling | REQUIREMENT | uncertified default fallbackへの成功保存は `DEFAULT_FALLBACK_SAVED` と記録し、`CERTIFIED_STAGING_SAVED` や `CANONICAL_INGESTED` と扱わない | fallback runtime | fallback write成功時 | - | task result state | `STAGING_FALLBACK` | 30 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.FALLBACK.040` | Noncanonical cascade | SEQUENCE | environment default fallbackが利用不可またはwrite失敗なら、他のeligible noncanonical candidateを試してよい。canonical authorityへの自動fallbackは禁止する | fallback runtime | default fallback unavailable or failed | - | fallback chain | `STAGING_FALLBACK` | 40 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.FALLBACK.050` | Promotion after certification | RULE | fallback先が後にscheduled acceptanceをPASSした場合、その後の実行ではProject Localのcertified Adapterとして固定・再利用してよい。過去のfallback artifactが自動的にcanonical化またはcertified化されるわけではない | adapter lifecycle | certification PASS後 | - | future staging route | `STAGING_FALLBACK` | 50 | APPROVED | `shgeta/ai-development-sahou#36` |
| `PLATFORM.STAGING.040` | Candidate discovery | SEQUENCE | setup時に現在利用可能なpersistent noncanonical store候補を探索し、runtime eligibilityを評価する。viable候補が複数ならuserに選択させ、1つならその候補を選択対象とする | setup/adaptation phase | human interaction expected | - | candidate stores | `STAGING_SETUP` | 40 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.050` | Adapter generation | REQUIREMENT | 選択store向けのenvironment-specific staging Adapterをその場で生成し、Project Localから再発見可能にする | setup/adaptation phase | storeを選択した後 | - | staging Adapter | `STAGING_SETUP` | 50 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.060` | Manual smoke test boundary | RULE | interactive chatからのwrite/read-backはsmoke testとして使用してよいが、scheduled acceptanceの代替にしない | adapter validation | manual executionが利用可能 | - | Adapter smoke test | `STAGING_ACCEPTANCE` | 10 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.070` | Separate scheduled test task | REQUIREMENT | 本taskとは別のTest Taskを作成し、environmentが許す最短の通常scheduler intervalで発動させ、通常scheduled executionをacceptance authorityとする。Test TaskはAdapter probeだけを行い、research / production processing / canonical writeを行わない | scheduled acceptance | Adapterをproductionで使う前 | scheduled execution機能自体が存在しない場合 | Test Task | `STAGING_ACCEPTANCE` | 20 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.080` | Immediate trigger limitation | PROHIBITION | `Run now` 等のmanual immediate triggerだけをscheduled runtime equivalenceの証拠としてacceptしない | scheduled acceptance | immediate/manual triggerを使用したとき | - | acceptance evidence | `STAGING_ACCEPTANCE` | 30 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.090` | Acceptance verification | VALIDATION | scheduled Test Taskはprobe write、rediscovery、read-back、identity/payload/checksum一致、追加human interaction不要、append safety、failure reporting、canonical isolationを検証する | scheduled acceptance | Test Task実行時 | capabilityが適用不能な個別testは理由を記録 | Adapter | `STAGING_ACCEPTANCE` | 40 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.100` | Cross-run persistence | VALIDATION | persistenceを主張する場合はwriteしたexecutionとは独立した後続executionからprobeをrediscover/readできることを確認する | persistent staging | persistenceをcertifyするとき | store自体がsingle-run用途として明示される場合 | persisted probe | `STAGING_ACCEPTANCE` | 50 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.110` | Certification lease | REQUIREMENT | acceptance成功を永久保証ではなく期限付きcertification leaseとして記録し、validated_at / valid_until / environment / Adapter version / test resultを保持する | certified Adapter | acceptanceがPASSしたとき | - | certification record | `STAGING_CERTIFICATION` | 10 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.120` | Invalidation | REQUIREMENT | certification expiry、Adapter変更、store/connector変更、permission/auth設定変更、scheduled runtime環境変更、tool/capability構成変更、production write failureのいずれかでcertificationを再検証対象またはINVALIDとする | certified Adapter | invalidation event発生時 | - | certification record | `STAGING_CERTIFICATION` | 20 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.130` | Runtime reuse | REQUIREMENT | valid certificationがあるruntimeでは既存Adapterを使用し、各production taskごとにstoreをrediscover/reselect/reauthorizeしない | production runtime | certificationがvalid | invalidation eventがある場合 | staging Adapter | `STAGING_RUNTIME` | 10 | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.STAGING.140` | Runtime failure fail-closed | REQUIREMENT | production writeが失敗した場合、成功やcanonical ingestionを報告せず、certificationをINVALIDとして再検証へ送る | production runtime | staging write失敗時 | - | task result / certification | `STAGING_RUNTIME` | 20 | APPROVED | `shgeta/ai-development-sahou#28` |

## 4. Runtime eligibility

最低条件:

```text
STAGING_ELIGIBLE =
    WRITE_CAPABILITY_AVAILABLE_NOW
    AND NO_INTERACTIVE_APPROVAL_REQUIRED_NOW
    AND NON_CANONICAL
```

候補選定では可能な限り次も確認する。

```text
WRITABLE_WITHOUT_PER_ACTION_APPROVAL
AND NON_CANONICAL
AND PROJECT_SCOPED
AND APPEND_SAFE
AND REVERSIBLE_OR_DISCARDABLE
```

`NO_INTERACTIVE_APPROVAL_REQUIRED_NOW` は「以前許可された」ことではなく、**そのruntime executionで追加認証・追加承認・人間対話を要求しない**ことを意味する。

## 4.1 Interaction mode

interactionは次の2軸を分離する。

```text
HUMAN_INTERACTION_AVAILABLE
HUMAN_INTERACTION_EXPECTED
```

典型例:

| available | expected | interpretation |
|---|---|---|
| YES | YES | manual interactive setup |
| YES | NO | autonomous run in interaction-capable environment |
| NO | NO | scheduled / unattended runtime |
| NO | YES | contradictory configuration; do not proceed as unattended |

scheduled / unattended acceptanceでは、対話機能が環境に存在するかどうかではなく、そのexecutionが人間対話を要求せず完結することを検証する。

## 4.2 Production task creation / re-enable route selection

production scheduled / unattended taskの作成・再有効化時には、durable outputの保存経路を先に分類する。ただしvalid certificationがないことだけでtaskを止めない。

```text
task create / re-enable request
  -> persistence intent classification
       -> read-only / no durable output
            -> staging = N/A
            -> task may proceed
       -> durable output required
            -> valid certified Project Local Adapter?
                 YES -> certified route
                 NO
                   -> environment default noncanonical fallback declared?
                        YES -> task may proceed with fallback route
                              -> runtime writeabilityを各executionで確認
                              -> DEFAULT_FALLBACK_SAVED
                              -> certification setupは別途継続
                        NO -> other eligible noncanonical candidateを探索
                              -> candidateなしなら保存不能を明示
```

separate scheduled Test TaskはAdapterをcertifyするためのprobe taskであり、production taskそのものを停止させるためのgateではない。fallback routeを利用中でも独立にacceptanceを進めてよい。

## 4.3 Fallback result states

保存状態は最低限次を区別する。

```text
DEFAULT_FALLBACK_SAVED
CERTIFIED_STAGING_SAVED
CANONICAL_INGESTED
SAVE_FAILED
```

意味:

- `DEFAULT_FALLBACK_SAVED`: environment defaultまたは他のuncertified noncanonical fallbackへwrite成功した。
- `CERTIFIED_STAGING_SAVED`: valid certification付きAdapter経由でwrite成功した。
- `CANONICAL_INGESTED`: 別責務のreconciliation / canonical writeまで完了した。
- `SAVE_FAILED`: 利用可能なnoncanonical保存経路へ保存できなかった。

これらを相互に同一視しない。

## 5. Setup / adaptation phase

setupは人間との対話が可能かつ期待されるphaseとして扱う。valid certificationが解決できない場合、production taskをdefault fallbackで継続しながら、このphaseでcertified Adapterへの昇格を進めてよい。

```text
inspect current environment
  -> discover candidate persistent noncanonical stores
  -> evaluate unattended write/read suitability
  -> one viable candidate: propose/select
  -> multiple viable candidates: user chooses
  -> generate environment-specific Adapter
  -> store Adapter in Project Local
  -> optional manual smoke test
  -> create separate scheduled Test Task
```

固定された製品別Adapter catalogだけを前提にしない。AIが現在環境に合わせて小さいAdapterを生成してよい。

## 6. Adapter minimum contract

staging Adapterは少なくとも次を宣言する。

- adapter identity / version
- destination identity
- write operation
- read-back operation
- enumerate / search / rediscover operation
- unique packet identity
- no implicit overwrite
- persistence scope
- concurrency behavior
- failure signal
- canonical isolation
- runtime assumptions

write成功後にread-backまたは同等のverificationを行えないAdapterは、その制約を明示し、`PERSISTED` を無条件に宣言してはならない。

## 7. Probe and acceptance tests

Probeはproduction dataと区別できる専用packetを使用する。

```text
packet_type: ADAPTER_PROBE
packet_id: <unique-id>
adapter_id: <adapter-id>
created_at: <timestamp>
payload:
  probe_string: EXPLORATION_STAGING_PROBE
  nonce: <unique-value>
  checksum: <checksum>
canonical: false
```

推奨test set:

| ID | Test | PASS condition |
|---|---|---|
| T1 | Write | 追加認証・追加承認なしでprobeを書ける |
| T2 | Read-back | packet identity / payload / checksumが一致する |
| T3 | Discover | 固定session状態に依存せずlist/search等から再発見できる |
| T4 | Append | 追加packetが既存packetを暗黙overwriteしない |
| T5 | Collision | 同名・近接時刻でもunique identityで衝突しない |
| T6 | Cross-run persistence | 別executionから先行probeを再発見・readできる |
| T7 | Non-interactive | scheduled execution中にhuman interactionを要求しない |
| T8 | Parallel | concurrent writeを許容するAdapterではloss/overwrite/corruptionを起こさない |
| T9 | Failure | write/read failureを成功として報告しない |
| T10 | Canonical isolation | canonical authorityを変更しない |

T6は同一execution内のwrite/read-backだけでは証明できない。

## 8. Certification lease

certification recordの推奨項目:

```text
adapter_id: <id>
adapter_version: <version>
environment: <runtime identity>
test_task_ref: <scheduled test task identity>
scheduled_run_ref: <acceptance run identity>
probe_packet_id: <probe identity>
validated_at: <timestamp>
valid_until: <timestamp>
status: READY | INVALID | REVALIDATE
scheduled_write: PASS | FAIL
rediscover: PASS | FAIL
read_back: PASS | FAIL
cross_run_persistence: PASS | FAIL | N/A
interactive_approval_required: NO | YES
canonical_isolation: PASS | FAIL
```

`valid_until` はplatform不変を保証する期限ではなく、変更を検知できなくても少なくともその頻度で再測定する上限である。

## 9. Project Local placement

生成したAdapter、certification、test historyは `SAHOU Project Local` から到達可能にする。

推奨例:

```text
.sahou/project-local/
  adapters/
    task-staging/
      <adapter-id>/
        adapter.md
        certification.yaml
        test-history.md
```

実際の物理配置はProject Local specに従う。third-party repository等でtarget repositoryを書き換えたくない場合はsidecar Project Localを使用してよい。

## 10. First use case: exploration packet staging

Research Exploration Map等の探索taskでは、各探索passを独立したExploration Packetとしてstagingへ保存してよい。

ただし次を維持する。

```text
LIBRARY_ARTIFACT != CANONICAL_EVIDENCE
NEW_MATERIAL_IN_THIS_PASS != NEW_TO_CANONICAL_AFTER_RECONCILIATION
SEARCH_COMPLETE != CANONICAL_INGESTED
LIBRARY_SAVED != FLUSHED
```

staging taskは探索と永続化までを担当し、global reduction / canonical reconciliation / canonical repository writeを同一taskの暗黙責務にしない。

探索・調査taskは、valid certificationが未準備であることだけを理由に停止しない。environment defaultの安全なnoncanonical fallbackが現在write可能なら、そのrunの結果をfallbackへ退避し、後からreconciliation / certificationを行う。

## 11. Validation

- durable outputを持つproduction taskはvalid certified Adapterを最初に確認している
- valid certificationがない場合、environment default noncanonical fallbackの有無を判定している
- certification未完了だけを理由に探索・調査結果を破棄またはtask停止していない
- fallback保存を `DEFAULT_FALLBACK_SAVED` としてcertified/canonical状態から区別している
- default fallback失敗時もcanonical authorityへ自動fallbackしていない
- separate scheduled Test Taskによるcertificationをfallback運用と独立して進められる
- read-only / no durable outputのN/A判定が明示されている
- re-enable時にもcurrent certified Adapter / fallback routeを再評価している
- runtime permissionを過去の許可から推定していない
- manual smoke testとscheduled acceptanceを区別している
- scheduled Test Taskがproduction taskと分離されている
- certificationにexpiryまたは再検証条件がある
- write failureでsuccess/canonical ingestionを報告しない
- staging destinationがcanonical authorityではない
- Adapter / certificationへPROJECT_BOOTSTRAPまたはProject Local indexから到達できる
- public-safeである

# AI共通仕様 / GitHub / AISPEC セット README

- Updated: 2026-10-06
- Scope: AI/人間がGitHub repository上で仕様を読み、作業し、commit/CIまで安全に進めるための共通仕様セット
- Library folder: `/AI共通仕様_GitHub_AISPEC/`

## 1. このフォルダの役割

このフォルダは、AIがrepository作業を行う際に共通で参照する仕様群をまとめた入口である。

目的は、次を別々のauthorityとして明示し、会話上の暗黙知へ依存しないこと。

1. 仕様そのものをどう記述・解釈するか
2. GitHub上の作業をどう開始・記録・commit・CI・引継ぎするか
3. large text / 複数file / 長時間validationをどう安全にcommitするか
4. Safe Commit Engineを実際にどう使うか
5. production Web siteの変更履歴をどうappend-onlyで追跡するか
6. scheduled / unattended taskがcanonical authorityを直接変更せず、追加の人間対話なしに結果を永続化するstaging経路をどう構成・検証するか


## 1.1 Public-safe by construction

この共通仕様folderは、将来そのままpublic repositoryへ公開され得る内容として維持する。

- project固有データ、private repository名、顧客名、個人名、実Issue/commit識別子、secret等を共通仕様へ入れない。
- 実project由来の名前や検証データをexampleへ流用しない。exampleはsynthetic dataを使う。
- Hidden Fact Registryは解析系projectで使用できる任意のproject固有authorityであり、内容そのものを共通仕様folderへコピーしない。
- 共通仕様へ昇格させる場合は、project固有identifierを除去し、一般化したrule / patternだけを移す。
- 「公開時に後で消す」運用を採用せず、常時public-safeであることを要求する。

詳細なguardrailは `GITHUB_AI作業運用共通仕様_v1.16.md` の `Common specification public-safety rule` をauthorityとする。

### 1.2 AISPECのphysical model

AISPECは単一fileを正本とする文書ではなく、SEARCH + specification closureで必要rule集合を復元するlogical distributed specification databaseとして扱う。physical fileはshardであり、既存recordのUPDATE/DELETEはPATCH、新規recordのまとまった追加はNEW SHARD、大規模semantic/schema再編はMIGRATION、意味を変えない物理整理はAISPEC Hygieneとする。routine full-file replacementは使用しない。

## 2. Routed loading

SAHOUは原則として**全fileを毎回loadしない**。

session開始時は次の順で必要moduleを決める。

1. `specs/README_共通仕様セット.md` をrouting indexとして読む。
2. projectの `PROJECT_BOOTSTRAP` からProject Localの有無とcurrent locationをresolveし、存在する場合はindex / applicable explicit override / mapping / extension / required Adapter referenceだけを読む。
3. Common SAHOUをbaselineとしてProject Localのexplicit overlayを適用し、Effective SAHOUを構成する。Project LocalがN/AならCommon SAHOUをそのままEffective SAHOUとする。
4. 以後のrouting / Adapter / folder-path / authority解決はEffective SAHOUに従う。
5. projectの current spec / Open Issue / taskを確認する。
6. task triggerに一致するmoduleだけを選択する。
7. 選択moduleが他moduleをdependencyとして要求する場合、そのclosureだけ追加loadする。
8. 作業中に新しいtriggerが発生した時だけmoduleを追加する。
9. exact-SHA cacheやProject Localが多数fileを保持していても、全体をcontextへ展開しない。

### 2.1 Routing table

| Trigger | Load |
|---|---|
| GitHub repositoryで作業する | `GITHUB_AI作業運用共通仕様_v1.16.md` |
| AISPECの意味変更・closure・RULE_IDを扱う | AISPEC v1.2 + GitHub運用 |
| Project Localを使用する | `SAHOU_PROJECT_LOCAL_AISPEC_v1.1.md` + Project Local index |
| scheduled / unattended production taskを作成・再有効化する、またはstaging storeを選定・生成・検証・fallback利用する | `TASK_STAGING_STORE_AISPEC_v1.2.md` + `SAHOU_PROJECT_LOCAL_AISPEC_v1.1.md` + product Adapter + project Adapter/certification if available |
| durable logを設計・記録する | `LOG_CORE_v1.0.md` |
| production Web update logを扱う | Log Core + `WEB_UPDATE_LOG_PLUGIN_v1.0.md` |
| Researchを扱う | Research Core + Research Evidence Core + taskに必要なResearch plugin |
| 化学物質のidentity / transformation / degradation / stabilityを扱う | Research Core + Research Evidence Core + `specs/research-evidence/plugins/chemical/CHEMICAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md` |
| 原料としての用途・目的機能・処方適性・sourcing/commercial評価を扱う | Chemical Research dependency closure + `specs/research-evidence/plugins/chemical/RAW_MATERIAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md` |
| Safe Commit発動条件に該当する | Safe Commit AISPEC、実操作時のみReference |
| ChatGPT環境でPersistent Project Store / Task Staging Store candidate mappingが必要 | `adapters/chatgpt/CHATGPT_ADAPTER_共通仕様_v1.3.md` |
| GitHub等その他product mappingが必要 | 対応Adapter |
| 上記に該当しない | 無関係なoptional moduleをloadしない |

project固有authority / Open Issue確認はroutingとは別に省略しない。

## 3. 各ファイルのauthority

| FILE | ROLE | AUTHORITY | 主な対象 |
|---|---|---|---|
| `AISPEC_AI仕様記述共通仕様_v1.2.md` | 仕様記述・解釈の共通形式 | 仕様の意味構造 | RULE_ID / TYPE / MEANING / SCOPE / TARGET / CLOSURE / ORDER / DEPENDS_ON / SOURCE / DECISION_REF 等 |
| `AI開発基盤抽象化共通仕様_v1.2.md` | product非依存platform role | logical capability model | Persistent Store / Task Staging Store / Repository / Tracker / Runner / Adapter role |
| `TASK_STAGING_STORE_AISPEC_v1.2.md` | unattended task staging | certified staging優先 + environment default fallback + Adapter生成・scheduled acceptance・certification | route selection / default fallback / runtime eligibility / Test Task / cross-run persistence / invalidation / fail-closed |
| `SAHOU_PROJECT_LOCAL_AISPEC_v1.1.md` | project固有SAHOU layer | Common override / project AISPEC / generated Adapter / certificationの配置・互換性 | embedded / sidecar / compatibility-first / migration boundary |
| `GITHUB_AI作業運用共通仕様_v1.16.md` | GitHub作業運用 | repository作業手順 | Issue / checkpoint / commit / tests / CI / restartability |
| `LOG_CORE_v1.0.md` | Log Core | durable log共通作法 | append-only / event identity / correction / secret exclusion / persistence safety |
| `WEB_UPDATE_LOG_PLUGIN_v1.0.md` | Web Update Log Plugin | production Web update history | deployment lifecycle / source / target / execution / validation / rollback |
| `GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md` | Safe Commit Engineの規範仕様 | large/multi-file commit transaction | parallel prepare / HEAD guard / hash / allowlist / validation / single commit |
| `GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md` | 実装・操作Reference | 非規範の実行説明 | CLI / GitHub Actions / executor / performance observation / limitation |
| `specs/research-evidence/plugins/chemical/CHEMICAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md` | Chemical Research Plugin | chemical species / transformation / degradation / stability semantics | species identity / derivative-reference relation / product formation / mass balance / structural motif retention |
| `specs/research-evidence/plugins/chemical/RAW_MATERIAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md` | Raw Material Research Plugin | intended-use evaluation layered on Chemical Research | intended function / formulation suitability / functional consequence / supplier / sourcing / commercial interpretation |

## 4. authorityの境界

### AISPEC

AISPECは「仕様をどう表現し、AIがどう解釈するか」を定義する。

repositoryのIssue運用やcommit手順そのものは `GITHUB_AI作業運用共通仕様` が担当する。

### Platform / Task Staging / Project Local

`AI開発基盤抽象化共通仕様_v1.2.md` は製品非依存のlogical roleを定義する。

Task Staging Storeはscheduled / unattended task用の非canonical保存roleであり、`TASK_STAGING_STORE_AISPEC_v1.2.md` がcertified route優先、environment default fallback、setup、Adapter生成、scheduled acceptance、certification、runtime failureの意味を定義する。

Project LocalはCommonそのものを複製する場所ではなく、project / environment固有の差分・生成Adapter・certification等を保持するlayerである。`Local` はmachine-local temporary workspaceを意味しない。Commonをbaselineとし、Project Localのexplicit override / mapping / extensionをoverlayした結果をEffective SAHOUとして使用する。

ChatGPT Adapterでは、valid certified Task Staging Adapterがなく、ChatGPT Libraryが利用可能かつ現在write可能なら、Libraryをproduct-specific default noncanonical fallbackとして使ってよい。fallback保存は `DEFAULT_FALLBACK_SAVED` とし、certified staging / canonical ingestionと区別する。certificationは後からscheduled acceptanceで取得し、その後の実行で優先利用する。default fallbackが使えない場合もrepository / Issue / canonical evidence等へ自動fallback writeしない。

### GitHub AI作業運用

GitHub作業では原則として以下をauthorityとする。

- 1作業テーマ = 1 Issue
- AISPECはcurrent semantic authority、Issueはcanonical change unit / semantic decision history、commit/PRはexact diffとする
- semantic changeはIssueなしのcommitだけで完結させず、AISPEC `DECISION_REF` ↔ Issue affected RULE_IDを双方向に追跡可能にする
- Issueで作業branch / HEADを確定し、書込み前に現在のcheckout branchとの一致を確認する。local worktree pathはhandoff authorityにしない
- branchを作成した場合はIssueに Branch Class / Merge Intent / Branch State / Review or Expiry / Keep or Drop Ruleを記録し、mergeするbranchと捨ててよいbranchを明示する
- 新branch作成前にBranch Drain Gateを行い、MERGE_READYなbranchを先に閉じる。Library Current Stateにはactive branch inventoryとmerge orderをmirrorする
- HANDOFF専用commitを作らない
- 重要checkpointはIssueコメントへ残す
- repository / current spec / current Issueを古い会話より優先する
- tests / CIをcommit SHAまで追跡する
- containerの外部アクセス制限時はGitHub Actionsで取得し、repository全体・巨大fileを含めartifactとして回収して作業継続する
- 重いlocal commandは安全に分離・並行実行し、待ち時間中に依存しない作業を進める
- pytestはすべての実行経路でproject固有の `PYTHONPATH` を明示し、canonical値をBOOTSTRAPへ記録する
- projectの継続作業に必要な固定情報を追加・変更した場合、同じ変更単位でPROJECT BOOTSTRAPから到達可能にする
- Libraryへ保存するuser受領データはrepository / project単位の専用folderへ集約し、同一案件で再利用する
- GitHub repository全体の再利用snapshotは `/GitHubRepos/<owner>__<repo>/repo-snapshots/` にexact SHA/hash/manifest付きで保持し、artifactは原則30日、Libraryはcurrent + previous 1世代でrotationする
- project全体とactive Issueのcurrent focus / 順序 / blocker / nextはLibrary Current Stateで共有してよいが、Issueにできる大きさの作業はIssueを主としSTATEだけで抱え続けない

### Log Core / Plugins

Log Coreはdomain非依存のappend-only / correction / persistence / traceabilityを定義する。ログを扱うtaskでだけloadする。

production Web updateでは `LOG_CORE_v1.0.md` に加えて `WEB_UPDATE_LOG_PLUGIN_v1.0.md` をloadする。read-only preflightはproduction updateそのものではないが、後続deploymentのevidenceとして参照してよい。

他domainのログ作法は将来別pluginとして追加し、Log Coreへdomain語彙を持ち込まない。

### Research Evidence domain Plugins

Chemical / raw-material research uses an explicit nested dependency:

```text
Research Core
  -> Research Evidence Core
       -> Chemical Research Plugin
            -> Raw Material Research Plugin
```

- Chemical Research is value-neutral about intended use: it records species identity, transformation, product formation, mass balance, motif retention, and condition-qualified chemical stability.
- Raw Material Research adds use-context semantics such as intended function, formulation suitability, functional consequence, supplier/specification evidence, sourcing, regulatory applicability, and commercial interpretation.
- Selecting Raw Material Research MUST load Chemical Research through dependency closure.
- Selecting Chemical Research alone MUST NOT load Raw Material Research.
- Physical folder nesting is for discoverability only; the plugin metadata defines semantic dependency.

Paper / Analysis plugins remain orthogonal and are loaded only when their trigger is present.

### Safe Commit Engine

次の場合はSafe Commit Engineを第一候補として検討する。

- 大きい既存UTF-8 text fileを変更する
- 複数fileのdiff/hash生成が重い
- connector経由のfull-file replacementが遅い・不安定
- validationがlocal tool実行枠を超える可能性がある
- exact HEAD / result hash / changed-path allowlistをtransactionとして固定したい

基本形:

```text
parallel prepare
  -> verified patch bundle
  -> exact HEAD guard
  -> isolated candidate validation
  -> single commit
  -> target fast-forward / push
```

commit/refを動かすfinal transaction自体は並列化しない。

## 5. 競合時の優先順位

同一事項について複数の記述がある場合、原則として次で解決する。

1. repositoryのcurrent spec / 明示されたProject Local override / project固有authority
2. current Open Issueで明示された作業Scope・Acceptance criteria・設計判断
3. 対象処理に特化した共通仕様（例: `LOG_CORE` + selected plugin, `GITHUB_SAFE_COMMIT_ENGINE_AISPEC`）
4. 一般的なGitHub作業運用仕様
5. AISPEC共通記述形式
6. Reference / example / 非規範の性能観測
7. 古い会話・古いhandoff・deprecated/history資料

ただし、project固有仕様が共通仕様の安全条件を意図的にoverrideする場合、そのoverrideは明示的に記録する。暗黙の上書きはしない。Project Localを使う場合もoverride対象・理由・scopeを追跡可能にする。

## 6. PROJECT BOOTSTRAPからの参照

GitHubを継続作業に使うprojectでは、PROJECT_BOOTSTRAPへ `Load mode: routed` を記録する。

Bootstrapは最低限次を明示する。

- SAHOU repository / ref
- routing index
- Project Local location / mode / index or N/A
- GitHub work時のGitHub運用spec
- projectで常用するoptional module
- task条件付きで読むplugin / specialized spec
- project固有authority / Current State / Work Item
- Task Staging Adapter / certificationを使用する場合はそのreference

例:

```text
Required SAHOU modules:
- specs/github/GITHUB_AI作業運用共通仕様_v1.16.md

Conditional modules:
- production web update:
  - specs/log/LOG_CORE_v1.0.md
  - specs/web/WEB_UPDATE_LOG_PLUGIN_v1.0.md
- Safe Commit trigger:
  - specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md
```

全文を各projectへ複製せず、必要moduleへの参照を持たせる。

## 7. Version / history運用

- 同名仕様の新版を作る場合、旧版を黙って書き換えずversionを上げる。
- 現行版をこのREADMEの一覧・読む順番へ反映する。
- 旧版は必要に応じて `history/` へ移動する。
- `DRAFT` / `PROPOSED` / `APPROVED` / `DEPRECATED` 等のstatusは各仕様本文をauthorityとする。
- Referenceは規範仕様より優先しない。
- 既存projectではmigration回避自体を目的にせず、migration / Project Local adaptation / hybridのcost・risk・保守性を比較して選ぶ。

## 8. 現行セット

```text
specs/
├── README_共通仕様セット.md
├── aispec/
│   └── AISPEC_AI仕様記述共通仕様_v1.2.md
├── github/
│   └── GITHUB_AI作業運用共通仕様_v1.16.md
├── log/
│   └── LOG_CORE_v1.0.md
├── web/
│   ├── WEB_UPDATE_LOG_PLUGIN_v1.0.md
│   └── WEB_SITE_UPDATE_LOG_共通仕様_v1.0.md  # deprecated legacy entrypoint
├── platform/
│   ├── AI開発基盤抽象化共通仕様_v1.2.md
│   ├── TASK_STAGING_STORE_AISPEC_v1.2.md
│   ├── SAHOU_PROJECT_LOCAL_AISPEC_v1.1.md
│   └── SAHOU_SHARED_CACHE_CONTRACT_v1.1.md
└── safe-commit/
    ├── GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md
    └── GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md
```

Research Evidence domain plugins currently include:

```text
specs/research-evidence/plugins/
├── PAPER_RESEARCH_SCHEMA_PLUGIN_v0.1.md
├── ANALYSIS_RESEARCH_SCHEMA_PLUGIN_v0.1.md
└── chemical/
    ├── CHEMICAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md
    └── RAW_MATERIAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md
```

Raw Material is semantically nested under Chemical by explicit dependency, not by folder position alone.

Research / Adapter等はtask trigger時にroutingして読む。

このREADMEは入口・routing用であり、各仕様本文の意味を置き換えない。

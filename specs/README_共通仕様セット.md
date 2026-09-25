# AI共通仕様 / GitHub / AISPEC セット README

- Updated: 2026-09-25
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
2. projectの `PROJECT_BOOTSTRAP` / current spec / Open Issue / taskを確認する。
3. task triggerに一致するmoduleだけを選択する。
4. 選択moduleが他moduleをdependencyとして要求する場合、そのclosureだけ追加loadする。
5. 作業中に新しいtriggerが発生した時だけmoduleを追加する。
6. exact-SHA cacheがrepository全体を保持していても、snapshot全体をcontextへ展開しない。

### 2.1 Routing table

| Trigger | Load |
|---|---|
| GitHub repositoryで作業する | `GITHUB_AI作業運用共通仕様_v1.16.md` |
| AISPECの意味変更・closure・RULE_IDを扱う | AISPEC v1.2 + GitHub運用 |
| durable logを設計・記録する | `LOG_CORE_v1.0.md` |
| production Web update logを扱う | Log Core + `WEB_UPDATE_LOG_PLUGIN_v1.0.md` |
| Researchを扱う | Research Core + taskに必要なResearch plugin |
| Safe Commit発動条件に該当する | Safe Commit AISPEC、実操作時のみReference |
| ChatGPT/GitHub等のproduct mappingが必要 | 対応Adapter |
| 上記に該当しない | 無関係なoptional moduleをloadしない |

project固有authority / Open Issue確認はroutingとは別に省略しない。

## 3. 各ファイルのauthority

| FILE | ROLE | AUTHORITY | 主な対象 |
|---|---|---|---|
| `AISPEC_AI仕様記述共通仕様_v1.2.md` | 仕様記述・解釈の共通形式 | 仕様の意味構造 | RULE_ID / TYPE / MEANING / SCOPE / TARGET / CLOSURE / ORDER / DEPENDS_ON / SOURCE / DECISION_REF 等 |
| `GITHUB_AI作業運用共通仕様_v1.16.md` | GitHub作業運用 | repository作業手順 | Issue / checkpoint / commit / tests / CI / restartability |
| `LOG_CORE_v1.0.md` | Log Core | durable log共通作法 | append-only / event identity / correction / secret exclusion / persistence safety |
| `WEB_UPDATE_LOG_PLUGIN_v1.0.md` | Web Update Log Plugin | production Web update history | deployment lifecycle / source / target / execution / validation / rollback |
| `GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md` | Safe Commit Engineの規範仕様 | large/multi-file commit transaction | parallel prepare / HEAD guard / hash / allowlist / validation / single commit |
| `GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md` | 実装・操作Reference | 非規範の実行説明 | CLI / GitHub Actions / executor / performance observation / limitation |

## 4. authorityの境界

### AISPEC

AISPECは「仕様をどう表現し、AIがどう解釈するか」を定義する。

repositoryのIssue運用やcommit手順そのものは `GITHUB_AI作業運用共通仕様` が担当する。

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

1. repositoryのcurrent spec / project固有authority
2. current Open Issueで明示された作業Scope・Acceptance criteria・設計判断
3. 対象処理に特化した共通仕様（例: `LOG_CORE` + selected plugin, `GITHUB_SAFE_COMMIT_ENGINE_AISPEC`）
4. 一般的なGitHub作業運用仕様
5. AISPEC共通記述形式
6. Reference / example / 非規範の性能観測
7. 古い会話・古いhandoff・deprecated/history資料

ただし、project固有仕様が共通仕様の安全条件を意図的にoverrideする場合、そのoverrideは明示的に記録する。暗黙の上書きはしない。

## 6. PROJECT BOOTSTRAPからの参照

GitHubを継続作業に使うprojectでは、PROJECT_BOOTSTRAPへ `Load mode: routed` を記録する。

Bootstrapは最低限次を明示する。

- SAHOU repository / ref
- routing index
- GitHub work時のGitHub運用spec
- projectで常用するoptional module
- task条件付きで読むplugin / specialized spec
- project固有authority / Current State / Work Item

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
│   └── SAHOU_SHARED_CACHE_CONTRACT_v1.1.md
└── safe-commit/
    ├── GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md
    └── GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md
```

Research / Adapter等はtask trigger時にroutingして読む。

このREADMEは入口・routing用であり、各仕様本文の意味を置き換えない。

# AI共通仕様 / GitHub / AISPEC セット README

- Updated: 2026-09-24
- Scope: AI/人間がGitHub repository上で仕様を読み、作業し、commit/CIまで安全に進めるための共通仕様セット
- Library folder: `/AI共通仕様_GitHub_AISPEC/`

## 1. このフォルダの役割

このフォルダは、AIがrepository作業を行う際に共通で参照する仕様群をまとめた入口である。

目的は、次を別々のauthorityとして明示し、会話上の暗黙知へ依存しないこと。

1. 仕様そのものをどう記述・解釈するか
2. GitHub上の作業をどう開始・記録・commit・CI・引継ぎするか
3. large text / 複数file / 長時間validationをどう安全にcommitするか
4. Safe Commit Engineを実際にどう使うか


## 1.1 Public-safe by construction

この共通仕様folderは、将来そのままpublic repositoryへ公開され得る内容として維持する。

- project固有データ、private repository名、顧客名、個人名、実Issue/commit識別子、secret等を共通仕様へ入れない。
- 実project由来の名前や検証データをexampleへ流用しない。exampleはsynthetic dataを使う。
- Hidden Fact Registryは解析系projectで使用できる任意のproject固有authorityであり、内容そのものを共通仕様folderへコピーしない。
- 共通仕様へ昇格させる場合は、project固有identifierを除去し、一般化したrule / patternだけを移す。
- 「公開時に後で消す」運用を採用せず、常時public-safeであることを要求する。

詳細なguardrailは `GITHUB_AI作業運用共通仕様_v1.15.md` の `Common specification public-safety rule` をauthorityとする。

### 1.2 AISPECのphysical model

AISPECは単一fileを正本とする文書ではなく、SEARCH + specification closureで必要rule集合を復元するlogical distributed specification databaseとして扱う。physical fileはshardであり、既存recordのUPDATE/DELETEはPATCH、新規recordのまとまった追加はNEW SHARD、大規模semantic/schema再編はMIGRATION、意味を変えない物理整理はAISPEC Hygieneとする。routine full-file replacementは使用しない。

## 2. 基本の読む順番

### GitHub repositoryで継続作業を始める場合

1. `AISPEC_AI仕様記述共通仕様_v1.2.md`
2. `GITHUB_AI作業運用共通仕様_v1.15.md`
3. project固有のcurrent spec / project固有authority / Open Issue
4. Safe Commit Engineの発動条件に該当する場合のみ `GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md`
5. 実際のCLI / workflow操作が必要な場合 `GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md`

Safe Commit Engineを使わない通常の小commitでは、4→5を必須とはしない。project固有のcurrent spec / project固有authority / Open Issue確認は省略しない。Hidden Fact Registryは解析系projectで利用できる任意のproject固有authorityであり、全projectの必須構造ではない。

## 3. 各ファイルのauthority

| FILE | ROLE | AUTHORITY | 主な対象 |
|---|---|---|---|
| `AISPEC_AI仕様記述共通仕様_v1.2.md` | 仕様記述・解釈の共通形式 | 仕様の意味構造 | RULE_ID / TYPE / MEANING / SCOPE / TARGET / CLOSURE / ORDER / DEPENDS_ON / SOURCE / DECISION_REF 等 |
| `GITHUB_AI作業運用共通仕様_v1.15.md` | GitHub作業運用 | repository作業手順 | Issue / checkpoint / commit / tests / CI / restartability |
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
3. 対象処理に特化した共通仕様（例: `GITHUB_SAFE_COMMIT_ENGINE_AISPEC`）
4. 一般的なGitHub作業運用仕様
5. AISPEC共通記述形式
6. Reference / example / 非規範の性能観測
7. 古い会話・古いhandoff・deprecated/history資料

ただし、project固有仕様が共通仕様の安全条件を意図的にoverrideする場合、そのoverrideは明示的に記録する。暗黙の上書きはしない。

## 6. PROJECT BOOTSTRAPからの参照

GitHubを継続作業に使うprojectでは、PROJECT BOOTSTRAPから最低限次へ到達できるようにする。

```text
AISPEC_AI仕様記述共通仕様_v1.2.md
GITHUB_AI作業運用共通仕様_v1.15.md
```

Safe Commit Engineを導入しているrepositoryでは、必要に応じて次も参照する。

```text
GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md
GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md
```

全文を各projectへ複製するのではなく、authorityへの参照を持たせる。

## 7. Version / history運用

- 同名仕様の新版を作る場合、旧版を黙って書き換えずversionを上げる。
- 現行版をこのREADMEの一覧・読む順番へ反映する。
- 旧版は必要に応じて `history/` へ移動する。
- `DRAFT` / `PROPOSED` / `APPROVED` / `DEPRECATED` 等のstatusは各仕様本文をauthorityとする。
- Referenceは規範仕様より優先しない。

## 8. 現行セット

```text
/AI共通仕様_GitHub_AISPEC/
├── 00_README_共通仕様セット.md
├── AISPEC_AI仕様記述共通仕様_v1.2.md
├── GITHUB_AI作業運用共通仕様_v1.15.md
├── GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md
└── GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md
```

このREADMEは入口・routing用であり、各仕様本文の意味を置き換えない。
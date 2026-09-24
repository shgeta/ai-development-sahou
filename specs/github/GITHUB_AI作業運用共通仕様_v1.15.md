# GITHUB AI作業運用共通仕様 v1.15

- Updated: 2026-09-24
- Scope: GitHub repositoryを使うAI/人間の継続作業
- Relation to AISPEC: `AISPEC_AI仕様記述共通仕様_v1.2.md` とは兄弟関係の共通仕様。AISPECは仕様記述・検索・解釈を扱い、本仕様はrepository・Issue・commit・tests/CI・作業引継ぎを扱う。GitHub上でAISPECを使うprojectは原則として両方をPROJECT BOOTSTRAPから参照する。

## 0.1 Common specification public-safety rule

本仕様および同じ共通仕様セットに置く文書は、将来そのままpublic repositoryへ公開され得るものとして扱う。

**common specification files MUST be public-safe by construction.** 公開直前の手作業によるsanitizationを前提にしない。

共通仕様・共通template・共通exampleへ、実projectから取得した固有データを一時的にもコピーしない。特に次を禁止する。

- private / internal repositoryの実owner名・実repository名
- 顧客名、社名、個人名、メールアドレス、電話番号、住所等の識別情報
- private Issue / PR / commit / branchの実IDや実SHA
- 実project固有のmodule名、code name、product名、folder名、internal URL
- API key、token、credential、secret、private endpoint
- user提供fileや解析対象から抽出した実データをexampleとして流用すること
- project固有の観測結果・Hidden Fact・fixture・baseline等を共通仕様へ混在させること

exampleが必要な場合は、`example-org/example-repo`、`project__sample-analysis`、`#123`、`abcdef123` 等の**明示的なsynthetic data**を使用する。公開情報を意図的に仕様根拠として引用する場合は例外とするが、その場合はpublic sourceであることと必要なprovenanceを明示する。

project固有データはproject専用repository / Library folder / Issue / artifactへ保持し、common specificationへ昇格させるときは、意味だけを一般化して移す。コピー元の固有identifierを残さない。

共通仕様を更新する際は、少なくとも次を確認する。

1. 新規・変更exampleがsyntheticか。
2. private repository / project / customer / person由来のidentifierが混入していないか。
3. Issue番号、SHA、path、URLが実案件の値ではないか。
4. project固有のHidden Factや検証データがcommon authorityへ混ざっていないか。
5. folder単位でそのまま公開しても追加sanitization不要か。

疑わしい値は「公開情報だから大丈夫」と推測せず、synthetic placeholderへ置き換える。

## 1. GitHub Issueで作業を管理する

作業の引き継ぎや進捗管理のために `HANDOFF.md` 等を増やしたり、HANDOFF更新だけのcommitを作ったりしない。

GitHubの通常のIssueを、作業管理・設計判断・進捗記録・引き継ぎの単位として使用する。

AISPECを使うprojectでは、Issueを単なる進捗票ではなく **canonical change unit / semantic decision historyの入口** として扱う。current specification authorityはAISPECにあり、Issueは「その意味または実装差分を、なぜ・どの範囲で・どの証拠により変更/修復したか」を追跡する。

原則として、

**1つの作業テーマ = 1 Issue**

とする。

作業開始時に、まずrepositoryのOpen Issueを確認する。

同じ作業を扱うIssueがすでにある場合は、新しいIssueを重複作成せず、そのIssueを使用する。

該当Issueがない場合は、作業開始時にIssueを作成する。

Issueは単なるメモではなく、後から以下を追える作業記録として使用する。

- 何を解決するのか
- 現在どこまで分かっているか
- 何を実装するのか
- 何が残っているか
- どのcommitで何を変更したか
- tests / CIがどうなっているか
- AISPECを使う場合、どのRULE_ID / specification closureに対する変更・不適合解消なのか
- semantic meaningを変更した場合、なぜその判断になったかと、どのPR / commit / CIへ反映されたか

## 2. Issue作成時

Issue titleは作業内容が分かる具体的な名前にする。

例:

```text
ExampleModule: nested source closureを欠落なく保持する
```

Issue本文には最低限以下を記載する。

```md
## Goal
このIssueで解決すること

## Context
現在の仕様・背景・関連する既存実装

## Scope
今回扱う範囲

## Acceptance criteria
完了と判断できる条件

## AISPEC impact (when applicable)
Change class: IMPLEMENTATION_NONCONFORMANCE / SPEC_DEFECT / SPEC_GAP_OR_UNKNOWN / NON_SEMANTIC_MAINTENANCE
Seed RULE_ID:
Specification closure:
Reverse dependencies:
Prior decision ref:

## Related
Branch:
Branch Class: EXPERIMENT / CANDIDATE / DELIVERY / LONG_LIVED
Merge Intent: NO / UNDECIDED / YES
Branch State: ACTIVE / FROZEN_WAIT / MERGE_READY / MERGED / ABANDONED
Merge Target:
Base:
Current HEAD:
Created:
Review / Expiry:
Recreate Cost: LOW / MEDIUM / HIGH
Keep / Drop Rule:
Recreate Path:
Checkout note (optional / session-local):
Relevant spec:
Relevant modules:
PR / commits:
```

既存のcurrent spec、project固有authority、関連Issue、関連commit等がある場合は参照を入れる。Hidden Fact Registryは解析系projectで使用できる任意のproject固有authorityであり、全projectの必須構造とはしない。

### 2.1 Issueと作業branchのbinding

Issueを作成または再利用した後、専用branchを作成・選択した場合は、そのbranch名をIssueへただちに記録する。Issueの `Branch` と `Current HEAD` を、次のAI/担当者が作業対象を特定するためのcanonicalな再開情報とする。

基本順序は次とする。

```text
Open Issueを確認 / 作成
  -> 作業branchを確定
  -> Issueへ Branch / Current HEAD を記録
  -> 現在アクセス可能なcheckoutのbranch / HEADを確認
  -> Issue記載のbranchと一致した場合のみ書込み開始
```

運用原則:

- Issueに作業branchが記載されている場合、そのbranchと現在のcheckoutが一致することを確認するまでsource/spec/test等への書込みを開始しない。
- Issueがfeature branchを指しているのに現在のcheckoutが `main` / `master` / default branchである場合、そのまま編集・commitしない。対象branchへ切り替えるか、対象branchの新しいcheckoutを作成してから進める。
- localのabsolute path、container path、temporary worktree path等はsession依存になり得るため、再開のcanonical authorityにしない。Issueへ書く場合も `Checkout note` 等の補助情報として扱う。
- 次回sessionで過去のcheckout/worktree pathが存在しない・アクセスできない場合、その場所を探し回ることを第一手にしない。Issueの `Branch` / `Current HEAD` とremote repositoryをauthorityとして、現在アクセス可能な場所へfresh checkout/worktreeを作成して再開する。
- `git worktree list` 等で即時に確認できる既存worktreeは利用してよいが、stale pathを見つけるために広範なfilesystem探索を行わない。
- branchを作り直した、renameした、baseを変更した、または作業branch自体を変更した場合は、同じ変更単位でIssueの `Branch` / `Current HEAD` を更新する。
- 次回作業に必要な変更を「アクセス不能になる可能性のあるlocal worktreeの未commit差分だけ」に残さない。意味のある継続作業は原則として作業branchへcommitする。commitできない途中状態をhandoffする必要がある場合は、patch/bundle/artifact等として回収可能に保存し、Issueからその所在と適用対象HEADへ到達できるようにする。
- local checkout pathが変わっただけではIssueのcanonical branch identityは変えない。pathをhandoff authorityへ昇格させない。

この規約の目的は、Issueが作業branchを指しているにもかかわらず別branch、特にdefault branchで作業を開始する事故と、消失したlocal worktree探索による無駄な時間を同時に避けることである。

### 2.2 Branch lifecycle / Merge Intent

Issueは長期間残ってよいが、branchは原則として短命なexecution vehicleとして扱う。Issueを作成しただけでbranchを作成してはならず、repositoryへ実際に変更を書き始める時点で初めてbranchを作成または選択する。

**branchが存在すること自体は保存理由にならない。** branchを作成・継続する場合、対応Issueへ少なくとも `Branch Class / Merge Intent / Branch State / Review or Expiry / Keep or Drop Rule` を記録し、次のAI/担当者が「mergeすべきか、捨ててよいか、いつ再判断するか」を推測せず判断できる状態にする。

#### Branch Class

branchの種類は、原則として次の4種類を使用する。

| Branch Class | Merge Intent | 用途 | defaultの扱い |
|---|---|---|---|
| `EXPERIMENT` | `NO` | 調査・試行・再現・仮説検証。採用前の変更 | 原則chat終了時または24時間以内に削除。採用する場合は削除前に昇格する |
| `CANDIDATE` | `UNDECIDED` | 採用価値を評価中。mergeするかまだ決めていない変更 | 24〜48時間以内に `DELIVERY` へ昇格するか `ABANDONED` にする |
| `DELIVERY` | `YES` | target branchへmergeする前提の実装 | 原則3日以内にmerge、明示的な継続判断、またはabandonを行う |
| `LONG_LIVED` | `YES` | migration等、短命branchでは扱えない例外 | 例外理由とmerge planをIssueに記録し、少なくとも7日ごとに継続理由を再確認する |

project固有事情により期限を変更してよいが、期限を無期限にしてはならない。変更する場合はIssueへ理由と次回review日を記録する。

`Review / Expiry` は単純な自動削除時刻ではない。意味はClassによって異なる。

- `EXPERIMENT`: 原則として削除または昇格する期限
- `CANDIDATE`: merge intentをYES/NOへ決める判断期限
- `DELIVERY`: merge / rebase-sync / explicit abandonのいずれかを再判断する期限
- `LONG_LIVED`: branchを長期保持する理由・base差分・merge planを再確認する期限

`DELIVERY` / `LONG_LIVED` を期限超過だけで自動削除してはならない。期限到達時はIssueを見て、merge / sync / continue / abandonを明示的に決める。無言で期限だけ延長しない。

#### Branch State

Branch Classとは別に、現在状態を次で表す。

- `ACTIVE`: 現在変更中
- `FROZEN_WAIT`: 実装内容はfreeze済みで、CI / review / external result等を待っている
- `MERGE_READY`: required validationが揃い、merge可能
- `MERGED`: merge済み。remote branch削除対象
- `ABANDONED`: mergeしないと決定済み。必要な知見をIssueへ残した上で削除対象

`FROZEN_WAIT` はbranchの種類ではなく状態である。例えば `Branch Class=DELIVERY / Merge Intent=YES / Branch State=FROZEN_WAIT` のように記録する。

#### Merge Intent

`Merge Intent` はbranch lifecycleで最重要の判断値とし、branchを作成した場合は必ずIssueへ記録する。

- `NO`: このbranch自体はmergeしない。必要な知見だけをIssue/AISPEC/Stateへ昇格してbranchは捨ててよい
- `UNDECIDED`: 採用評価中。期限までに `YES` または `NO` を決める
- `YES`: targetへmergeする責務がある。mergeまたは明示的abandonまで放置しない

`Merge Intent=NO` のbranchを後から救出してmergeすることを常態化しない。採用すると決めた時点でIssue上のClass / Merge Intentを更新し、必要ならcleanな `DELIVERY` branchへ変更を再構成してよい。

#### Recreate Cost / Keep or Drop Rule

再作成が容易な変更を、単に「せっかく作ったから」という理由でbranchとして保存しない。

`Recreate Cost` は次を目安とする。

- `LOW`: current target branchとIssue記録から短時間で再現でき、uniqueな手作業成果を失わない
- `MEDIUM`: 再実行可能だが、検証・調査・複数file修正等に相応の時間がかかる
- `HIGH`: 再現困難な手作業、重要なregression tests、複雑なsemantic change、長時間生成物等を含む

特に `EXPERIMENT` / `CANDIDATE` では `Keep / Drop Rule` と `Recreate Path` を記録する。`LOW` で、Issue/Stateから再作成できるものは、chatを跨いでbranchを救出するより削除して必要時に再作成することを許容する。

#### Branch promotion

標準的な昇格経路は次とする。

```text
EXPERIMENT / NO
  -> 有用性確認
CANDIDATE / UNDECIDED
  -> 採用決定
DELIVERY / YES
  -> 実装freeze
DELIVERY / YES / FROZEN_WAIT
  -> validation完了
DELIVERY / YES / MERGE_READY
  -> merge
MERGED -> branch delete
```

不採用なら、

```text
EXPERIMENT or CANDIDATE
  -> Issueへfinding / recreate pathを記録
ABANDONED
  -> branch delete
```

とする。

#### Branch Drain Gate

新しいimplementation branchを作成する前に、既存active branchを確認する。

基本順序:

```text
Library PROJECT_STATE / related Issuesでactive branch確認
  -> MERGE_READY + Merge Intent=YES があるか
     -> yes: 原則先にmergeしてbranchを閉じる
  -> FROZEN_WAITがあるか
     -> yes: wait理由・merge order・期限を確認
  -> mutable DELIVERY branchがあるか
     -> yes: 新branchが本当に必要か確認
  -> 必要な場合だけ新branch作成
```

原則として、1つのAI execution laneにつき **mutableな `Merge Intent=YES` branchは1本** に抑える。加えて、内容freeze済みの `FROZEN_WAIT` を1本まで並行保持してよい。

これを超えて並行branchを持つ場合は、各Issueへ次を明示する。

- 並行が必要な理由
- branch間のdependency有無
- merge order
- base / expected rebase risk
- 各branchのReview / Expiry
- どれを先に閉じるか

CI待ちだけを理由に無制限に次branchを作らない。新しいbranchを作る前に、merge可能なbranchを先に閉じることを優先する。

#### Branchは保管庫にしない

「一応残しておく」だけを理由にbranchを作成・保持しない。

残したい内容に応じて次を使い分ける。

- semantic decision / formal history -> GitHub Issue / AISPEC
- current focus / active branch一覧 / merge order -> Library Current State
- 小さく再適用可能な途中差分 -> patch / bundle等
- large reusable input/output -> artifact / Library
- targetへ入れる完成に近い変更 -> `DELIVERY` branch

chat終了・handoff時には、active branchについてIssueの `Merge Intent / Branch State / Review or Expiry / Keep or Drop Rule` を最新化する。`MERGED` / `ABANDONED` branchはLibrary Current Stateのactive一覧から外し、remote branchも不要なら削除する。

### 2.3 AISPECとIssueのsemantic decision binding

AISPECを使うprojectでは、役割を次のように分離する。

```text
AISPEC
  = current semantic authority / 現在何が正しいか

GitHub Issue
  = canonical change unit / なぜ・何を・どこまで変えるか / semantic decision history

PR / commit
  = exact implementation/spec diff

tests / CI
  = そのexact revisionに対するvalidation evidence
```

したがって、**semantic historyの入口はIssue、exact change historyの入口はcommit/PR** とする。

#### 仕様が間違っている疑いが出た場合

標準追跡順は次とする。

```text
current AISPEC RULE_ID
  -> SOURCE
  -> DECISION_REF
  -> semantic decision Issue
  -> reason / evidence / alternatives / affected closure
  -> PR / commit
  -> exact diff / tests / CI
```

Issueが存在する場合、最初からcommit履歴を大量に辿って判断理由を推測しない。まずIssueでsemantic contextを確認し、その後commit/PRでexact diffを確認する。

`DECISION_REF` が存在しないlegacy ruleでは、SOURCEとGit historyをfallbackとしてよい。ただし判断理由を確定できない場合は新しいIssueを作成し、推測でcurrent meaningを正当化しない。

#### semantic changeのIssue必須境界

GitHub/AISPEC projectでは、次のようなsemantic changeをcommitだけで完結させない。対応Issueを作成または既存Issueを使用する。

- `MEANING / SCOPE / CLOSURE / WHEN / UNLESS / TARGET` の意味変更
- `DEPENDS_ON / PRECEDES` の意味上の依存変更
- execution semanticsへ影響する `GROUP / ORDER` 変更
- production membership / 有効性を変える `STATUS` 変更
- behaviorを追加・削除するrule新設 / DEPRECATED化

誤字、formatting、意味を変えないphysical sharding、index再生成等はproject policy上Issueなしで扱ってよい。semanticか不明なら非semanticと決め打ちしない。

#### bidirectional trace

semantic changeでは、原則として次を両方満たす。

1. Issueからaffected `RULE_ID` / seed / impacted specification closureへ到達できる。
2. 変更後AISPEC ruleの `DECISION_REF` から、そのsemantic change Issueへ到達できる。

Issueには必要に応じて以下を残す。

- previous/current meaningと問題点
- observed contradiction / evidence
- change classification
- seed RULE_ID / specification closure / reverse dependencies
- 採用decisionと、重要な代替案を採らなかった理由
- final affected RULE_ID set
- PR / commit / exact HEAD
- tests / CI / Visual QA等のevidence

新しいIssueが過去decisionを置き換える場合、Issue側からprior decision Issueへリンクする。AISPEC側へ無制限な履歴を埋め込まず、current meaningを説明するための `DECISION_REF` を保つ。

Issueはcurrent AISPECを上書きする仕様authorityではない。過去Issueとcurrent AISPECが矛盾する場合、実行時はcurrent AISPECをauthorityとしつつ、矛盾自体を新しいIssueで検証する。

### 2.4 Library Current StateはIssueの補助盤とする

GitHub Issueを正式な作業単位・進捗記録・設計判断・handoffの主たるauthorityとしたまま、project全体の現在地や、Issue実行中の細粒度なfocus / 順序 / 待ち / 次作業を、project固有Library folder内のCurrent Stateで共有してよい。

**Current StateはIssueの代替ではない。Issueが常に主であり、Issueにできる大きさの作業をCurrent Stateだけで継続してはならない。**

標準配置は次とする。

```text
<Library project folder>/state/PROJECT_STATE.md
<Library project folder>/state/issues/ISSUE-<number>_STATE.md
```

`PROJECT_STATE.md` はproject全体の現在盤として、少なくとも必要に応じて次を持つ。

- current project focus
- active Issue一覧と実行順 / priority
- project全体の現在地・完了済み範囲・残りの大きな区分
- blocking / waiting
- safely parallelizable work
- active branch inventory（Issue / Branch / Class / Merge Intent / State / Review or Expiry / HEAD）
- merge order / branch drain priority
- next recommended Issue / next major step

active Issueの `ISSUE-<number>_STATE.md` は、そのIssue本文やcheckpointより細かい「いま実行中の状態」を置く補助盤として、必要に応じて次を持つ。

- Issue番号・titleへの参照
- current focus
- current sub-step
- just completed / verified
- next immediate step
- blocked / waiting
- parallelizable work
- branch / HEADのmirror（canonical authorityはIssue側）
- Branch Class / Merge Intent / Branch State / Review or Expiryのmirror
- merge order / next branch lifecycle action

運用境界:

- 独立したGoal / Scope / Acceptance criteriaを持てる大きさになった項目は、Current State内で育て続けず、速やかにGitHub Issueを作成または既存Issueへ統合する。以後Current StateはそのIssueへの参照とIssue未満のcurrent focusだけを保持する。
- 「IssueにできるならIssueにする」を優先し、Current Stateをmini-Issue、backlog、仕様書、設計判断の保管場所として常用しない。
- Issue本文・Issue commentへ残すべき設計判断、Scope変更、Acceptance変更、重要checkpoint、commit/test/CI結果をCurrent Stateだけに記録しない。Current Stateには必要なら短いsummaryとIssue linkを置く。
- Current Stateは現在盤であり、履歴台帳ではない。focusや順序が変われば更新し、古い状態をversion fileとして大量保存しない。
- IssueをCloseしたら、そのIssue固有STATEを削除するかactive stateから外す。必要な履歴はGitHub Issue / commit / CIを参照する。
- `MERGED` / `ABANDONED` branchはactive branch inventoryから速やかに外す。Current Stateをbranch履歴台帳として蓄積しない。
- Current StateとIssueが矛盾する場合はIssueを優先し、Current Stateを修正する。repository/current specと矛盾する場合はrepository/current specを優先する。
- progressをpercentageで表す場合は分母が明確な場合に限る。分母が不明なときは完了済み区分 / 現在focus / 残り区分で表現する。
- 毎commandごとには更新せず、focus変更、sub-step完了、block発生/解除、実行順変更、Issue開始/終了、handoff等の意味のある節目で更新する。
- Library Current Stateのcanonical pathはPROJECT BOOTSTRAPから到達できるようにする。

役割分担は次を原則とする。

```text
GitHub Issue
  = 作業の主単位 / Goal / Scope / Acceptance / 設計判断 / checkpoint / handoff

Library Current State
  = project全体の現在盤 + active IssueのIssue未満のfocus / 順序 / 待ち / 次

PROJECT BOOTSTRAP
  = Issue・Current State・spec・test等への固定入口
```

Current Stateを読む目的は「次のAIが何をすべきかを短時間で把握すること」であり、Issueを作らずに作業を延命することではない。

## 3. 作業中

重要なcheckpointはIssueコメントとして残す。

毎操作ごとにコメントする必要はない。以下のような意味のある節目だけ記録する。

- 原因を特定した
- 設計判断をした
- 実装方針を変更した
- 主要な実装が完了した
- regression testを追加した
- Visual QA結果が出た
- 想定外の問題を発見した
- AISPECとimplementation/source factの矛盾を発見した
- semantic meaningを変更するdecisionをした
- 次回作業へ残す重要事項が発生した

例:

```text
checkpoint

- transform ruleを暫定実装
- explicit-input経路のregression test追加
- 18/18 PASS
- derived-input側は未確認

HEAD: abcdef123
```

会話の中だけに重要な設計判断を残さない。

次の担当者または次のAIがrepositoryとIssueだけを見ても作業を再開できる状態にする。

## 4. commit

コード・テスト・仕様などrepository本体の変更は通常どおりcommitする。

commit messageには、可能であればIssue番号を関連付ける。

例:

```text
fix: preserve source closure for nested parts (#123)
```

HANDOFFのためだけのcommitは作らない。

### commitするもの

- source code
- tests
- current spec
- repository成果物として残すべきdocumentation

### Issueへ書くもの

- 現在どこまで進んだか
- 次に何をするか
- 作業途中のcheckpoint
- 一時的な注意事項
- 次のAI/担当者向け引継ぎ

## 4.1 AISPEC physical write strategy — local / GitHub / connector共通

AISPEC specification fileを変更する場合、保存経路がlocal Git checkout、GitHub connector/API、Library、remote runnerのどれであっても、`AISPEC_AI仕様記述共通仕様_v1.2.md` の Physical Write Strategyを適用する。

- existing rule / recordのUPDATE・DELETEはPATCHする。変更量が多ければPATCHを複数transactionへ分割する。
- new rule / recordのまとまった追加がshard write threshold以上なら、既存fileへ大きな追記を試さずNEW SHARDを第一選択とする。
- NEW SHARDは新しいsemantic authorityを意味しない。SEARCH + specification closureで同じlogical specification setとして回収可能にする。
- routine full-file replacementをAISPEC authority fileの更新手段にしない。
- 相当大きいschema / semantic再編はMIGRATION、意味を変えない物理整理はAISPEC Hygieneへ分離する。
- connectorやAPIのSHA/version要件はtransaction safetyのために扱い、tool limitationを理由にsemantic version bumpやduplicate authority fileを作らない。

Git commit / PRはこれらのphysical writeを包むexact change transactionであり、AISPECのlogical data modelやshard境界そのものを決めるauthorityではない。

## 4.2 Safe Commit Engineとの関係

大きい既存text fileへの多数PATCH、複数fileの変更、patch bundle生成・検証が重い場合、またはvalidationがlocal tool実行枠を超え得る場合は、`GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md` と `GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md` を参照し、Safe Commit Engineの利用を第一候補として検討する。

Safe Commit Engineの基本形は次とする。

```text
parallel prepare
  -> verified patch bundle
  -> exact HEAD guard
  -> isolated candidate validation
  -> single commit
  -> target fast-forward / push
```

- file単位のdiff/hash/patch生成は並列化してよい。
- branch/refを動かすfinal transactionは直列化する。
- target HEADがbundle作成時から移動していた場合はfail closedする。
- after hashまたはchanged-path allowlistが一致しない場合はcommitしない。
- validationはcandidate worktreeで実行し、失敗時にtarget checkoutを汚さない。
- container/tool timeout後もdetached child processが存続することを前提にしない。長時間validationはGitHub Actions等のremote runnerへ委譲する。
- v0.1のpatch backendはUTF-8 textを対象とし、binary/non-UTF8/rename-copyはfail closedする。

通常の小さいcommitまでSafe Commit Engineを必須とはしない。利用判断は変更サイズ、connector制約、validation時間、再実行性の必要性に基づく。

## 4.3 外部アクセス制限時のGitHub Actionsフォールバック

AIのcontainer / local execution environmentは、外部networkへのegress、DNS、TLS、認証、download、clone、package取得等が制限される場合がある。外部resourceの取得が作業上必要であり、現在のcontainerから直接取得できないことが確認できた場合、local fetchの反復に固執せず、GitHub Actionsを標準の第一フォールバック実行環境として使用する。

基本経路は次とする。

```text
container/local fetch attempt
  -> external access restriction confirmed
  -> GitHub Actions runnerで取得
  -> source/revision/hash等を記録
  -> Actions artifact等として「作業中のAI自身が取得できる状態」に公開
  -> AIがartifactを回収
  -> 解析・実装・validationを継続
```

運用原則:

- 外部取得失敗がenvironment由来と判断できる場合、同一local fetchを無意味に繰り返さない。
- このfallbackの取得単位は単一fileに限定しない。repository全体、指定branch/tag/commitの完全snapshot、submodule、Git LFS実体、release asset、large binary等も対象とする。
- repository全体が必要な場合、GitHub APIでfileを個別取得して「全体を見た」ことにしない。Actions runner上で対象revisionをcheckout/cloneし、必要なhistory depth・submodule・Git LFSを明示して取得した上で、archiveまたはartifactとして回収する。
- 「repository全体」「全file」「漏れなく」等が要求されている場合、shallow clone、sparse checkout、partial clone、API pagination打切り、LFS pointerのみの取得など、内容を欠落させる方式を暗黙に使わない。制約上必要なら欠落範囲を明示する。
- 巨大な単一fileは途中を省略・truncateして取得完了とみなさない。runner上で元byte列を保持し、必要ならlosslessに分割して複数artifactへ出す。各partの順序・size・SHA256と元fileのSHA256をmanifestへ記録し、AI側で再結合後に元hash一致を確認する。
- repository snapshotをarchive化する場合、対象commit SHAをmanifestへ固定する。symlink、executable bit、submodule参照等が作業上意味を持つ場合は、それらを保持できるarchive形式または補助metadataを使用する。
- Actions artifactのsize/count制限に当たる場合は、取得対象を内容欠落で縮小せず、deterministicな複数partへ分割し、再構成manifestを添付する。分割後も全体hashまたはfile単位hashで完全性を検証する。
- Git LFSを含むrepositoryでは、pointer fileだけで足りるか実blobまで必要かをScopeから判断する。全体取得・解析目的では原則として必要なLFS objectもrunner側で取得する。
- repository全体またはlarge fileをActions経由で取得した場合、Issue checkpointまたはartifact manifestから、取得revision、取得scope、除外有無、分割有無、hashを追跡できる状態にする。
- repositoryにGitHub Actionsを実行できる経路がある場合、runner側で必要resourceを取得するworkflowを使用または作成する。
- 取得物は原則として `actions/upload-artifact` 等のActions artifactへ出し、**作業中のAI自身が取得・読取できる状態に公開する**。ここでいう「公開」は一般公開を意味せず、当該作業のAIがActions実行結果から回収できる状態を指す。
- 可能な場合、source URL / repository / branch or tag / commit SHA / release version / checksum /取得時刻など、後から取得元を再現・監査できるmetadataをartifactまたはworkflow logへ残す。
- 取得した第三者fileやlarge binaryを、回収だけを目的にcurrent branchへcommitしない。repository成果物として残す必要がある場合のみ通常のcommit規則に従う。
- artifact経路を利用できない場合は、repository policyと機密性を確認した上で、temporary branch / release asset / Pages等の代替経路を使い、AI自身が取得できるURLまたはresourceとして公開してよい。ただし必要以上に公開範囲を広げない。
- private repository、credential、token、非公開資料、個人情報、機密情報を、回収のためだけにpublicへ露出させてはならない。repository visibilityの変更は外部取得フォールバックの手段にしない。
- workflow内でsecretを使用する場合、logやartifactへsecret値を出力しない。
- Actionsで取得したresourceも、取得元・revision・hashが不明なままauthorityへ昇格させない。
- Actions経由で取得した結果を使った場合、必要に応じてIssue checkpointへ取得経路とartifact/runを記録する。

このfallbackは、containerが外部resourceへ到達できないことを理由に作業を止めないためのものとする。GitHub Actions自体が利用不能な場合のみ、利用可能な別のremote runner / connector / user-provided file等へ切り替える。

## 4.4 重いlocal commandの並行運用

local/container上で実行時間が長いcommand、large test suite、build、archive、hash/diff生成、変換、scan、render等を実行する場合、完了まで何もせず待つことを避ける。実行環境が安全に並行処理を許す場合は、重い処理を別session・別process・別worktree・remote runner等へ回し、その処理結果に依存しない作業を並行して進める。

基本形は次とする。

```text
heavy command start
  -> safe isolated execution pathへ置く
  -> status/progressを追跡可能にする
  -> 依存しない作業を継続
  -> 必要なcheckpointで結果を回収
  -> 結果に依存する後続処理へ合流
```

運用原則:

- 重いcommandを起動した後、結果待ちだけで作業を空転させない。
- そのcommandの結果を必要としない調査、仕様確認、Issue整理、read-only解析、test case設計、差分レビュー、次工程準備等を先に進める。
- 同じworking tree、同じgenerated output、同じcache、同じbranch/ref等を競合更新する処理は安易に並行化しない。必要なら別worktree、temporary directory、別branch、isolated candidate環境を使う。
- read-only処理、独立file単位処理、独立test shard等は、resource競合が問題にならない範囲で並列化してよい。
- 長時間processを単にdetached化しただけで、tool/session終了後も確実に存続すると仮定しない。継続性が必要な場合は、管理可能なsession、GitHub Actions等のremote runner、または再実行可能なcheckpointを使う。
- commandのPID/session/run、入力revision、出力先、開始時HEAD等、後で結果と作業状態を対応付けられる情報を保持する。
- 並行作業中に対象HEADや入力が変わり得る場合、結果をそのまま採用せず、開始時revisionとの整合を確認する。
- CPU/RAM/disk I/Oを食い尽くして全体を遅くする過剰並列化は避ける。並列数はrunner/container資源に合わせる。
- 重いcommandがfailure/timeoutした場合でも、その間に進めた独立作業を捨てず、再実行条件と失敗点を記録して再開する。
- userへの進捗共有が必要な長い作業では、重い処理の待ち時間中に進めた別作業や得られた中間結果も適宜共有する。

このルールは、作業を非同期に放置して後で回答するためのものではない。現在の作業セッション内で、待ち時間を利用して安全に独立作業を進め、同じ応答・同じ作業継続の中で結果を統合するための運用とする。

## 4.5 ユーザー受領データのLibrary project folder集約

ユーザーから受け取ったfile / dataのうち、後続作業、再開、別chat、別担当AIで再利用する価値がありLibraryへ保存すべきものは、Library直下へ無秩序に置かず、repository / project単位の専用folderへ集約する。

folder identityは次の優先順で決める。

1. GitHub repositoryがある案件はrepository full nameをcanonical identityとし、Library上のcanonical project rootを原則 `/GitHubRepos/<owner>__<repo>/` とする。
2. GitHub repositoryがない案件は、案件を安定して識別できるproject名から `project__<project-slug>` を作る。
3. 作成前にLibraryを確認し、同一projectの既存folderがあれば新規作成せず再利用する。
4. 候補folder名が別projectと衝突する場合は、別projectであることを確認した上で `__<stable-short-id>` を付与する。suffixは初回に一度だけ決め、以後同じprojectでは同じfolderを再利用する。
5. 同一repository / projectに対してchatごと・日ごとに別folderを増やさない。
6. Library project folderを新規作成またはcanonical変更した場合、そのcanonical pathをPROJECT BOOTSTRAPへ同じ変更単位で記載する。BOOTSTRAPからLibrary保存先へ到達できない状態を残さない。

例:

```text
/GitHubRepos/example-org__example-repo/
/GitHubRepos/example-org__sample-tool/
project__sample-analysis/
```

保存対象の例:

- userがuploadしたsource file、archive、PDF、PPTX、spreadsheet、CSV、image、reference document
- repository作業やQAで後から再利用するfixture、baseline、reference image、original asset
- Actions等で取得し、今後の作業で再利用価値があるsnapshot / artifact
- userから受け取った仕様・資料のうち、会話だけに残すと再開性を損なうもの

保存不要の例:

- 一時cache
- 再生成が容易で再利用価値のないtemporary output
- 数分の処理だけに必要なintermediate file
- repositoryまたは既存authorityから容易に再取得でき、Library複製が不要なもの

運用原則:

- 元file名は可能な限り保持する。
- 同名fileがあり内容が異なる場合、黙ってoverwriteせず、日付・revision・short hash等のsuffixで一意化する。明示的なversion replacementの場合のみ既存fileを更新する。
- user受領データを保存するときは、現在のrepository / project identityを先に解決してから保存先を決める。
- GitHub repositoryが後から作成されたprojectは、同一案件であることが確認できれば既存project folderをrepository canonical folderへrename / migrateし、二重管理を避ける。
- project folder内でさらに分類が必要な場合は `inputs/`, `reference/`, `qa/`, `artifacts/` 等のsubfolderを作ってよいが、project root外へ散らさない。
- project固有データを共通仕様folder、Library root、別project folderへ混在させない。
- sourceがuser提供、GitHub、Actions artifact、外部download等のどれかを後で区別する必要がある場合、filename、manifest、index file等でprovenanceを追跡可能にする。
- 保存対象に機密情報・個人情報等が含まれる場合、Libraryの共有範囲を不用意に拡大しない。

このルールの目的は、ユーザー受領データを「どの案件のものか」から確実に再発見できるようにし、chatや作業sessionが変わっても同一projectの材料を一箇所から再利用できる状態を保つことである。

## 4.6 pytest実行時のPYTHONPATH明示

`pytest` を実行する場合、import解決をcurrent shell、偶然のworking directory、IDE設定、過去sessionのenvironmentへ依存させない。**すべてのpytest実行で `PYTHONPATH` を明示的に指定する。**

運用原則:

- local/container、GitHub Actions、Safe Commit Engineのvalidation、CI、debug実行を含め、`pytest` を呼ぶすべての経路で `PYTHONPATH` を明示する。
- shellにすでに `PYTHONPATH` が設定されている場合でも、pytest command側でprojectが要求する値を明示する。暗黙継承をauthorityにしない。
- project rootをimport rootとするprojectでは、POSIX系の基本形を `PYTHONPATH=. python -m pytest ...` とする。
- `src/` layout等で別のimport rootが必要なprojectでは、例として `PYTHONPATH=src python -m pytest ...` のようにproject固有値を明示する。
- 複数pathが必要な場合は実行platformのpath separatorを用い、BOOTSTRAPにcanonical値を記録する。
- Windows等でcommand先頭のenvironment assignment構文が使えない場合も、PowerShellの `$env:PYTHONPATH=...` 等、同等に**そのpytest実行単位で明示設定**する。
- `pytest` executable直呼びより `python -m pytest` を優先し、pytestを実行するPython interpreterとmodule import contextを揃える。project固有事情で別方式を使う場合はBOOTSTRAPへ明記する。
- test commandをscript / Makefile / task runner / workflowへ包む場合、そのwrapper内部で `PYTHONPATH` を確定させるか、wrapper呼出し時に必須引数・environmentとして明示し、最終的なpytest実行が暗黙値へ依存しないようにする。
- `PYTHONPATH` を明示せずpytestが偶然PASSした結果をcanonical validationとして扱わない。canonical条件で再実行する。

PROJECT BOOTSTRAPには、そのprojectでpytestに使用するcanonical `PYTHONPATH` とcanonical test commandを記載する。例:

```text
Pytest PYTHONPATH: .
Canonical pytest: PYTHONPATH=. python -m pytest -q
```

または:

```text
Pytest PYTHONPATH: src
Canonical pytest: PYTHONPATH=src python -m pytest -q
```

この規約の目的は、chat/session/container/runnerが変わってもimport path差による偽FAIL・偽PASSを避け、同一projectのpytest結果を再現可能にすることである。

## 4.7 reusable exact repository snapshotの保持と再利用

Actions artifactだけを唯一の再取得手段にせず、後続chat / sessionで再利用価値が高いrepository全体取得は、exact repository snapshotとしてLibraryへ保持してよい。目的は、containerの外部access制限等により同じfull-repository fallbackを毎回作り直すことを避けることである。

GitHub repositoryの標準配置は次とする。

```text
/GitHubRepos/<owner>__<repo>/repo-snapshots/
```

artifact / snapshot contract:

- GitHub Actions snapshot artifactは原則 **30日保持** とする。project固有事情で短くする場合はBOOTSTRAPへ理由を明示する。
- exact snapshotには少なくとも、repository full name、対象ref、**exact commit SHA**、Git tree SHA、archive file、**archive SHA256**、recursive tree manifestを含める。
- tree manifestは少なくともrepository pathとGit object identityを追跡できる形式とし、snapshotがどのtreeを表すかを後から検証できるようにする。
- archive / tree manifestは可能な限り各SHA256も同梱する。
- Libraryへ保存するsnapshotは差分patchの累積ではなく、対象commitの**exact full snapshot**を基本とする。

reuse / rotation policy:

1. repository全体が必要になったら、まずcurrent target ref（通常は `main` / default branch）のexact HEADをGitHubから解決する。
2. Libraryのcurrent snapshot metadataを確認し、保存snapshotの `commit_sha` がcurrent target HEADと一致する場合は、同じsnapshotを再利用し、同一repositoryを再取得しない。
3. target HEADが進んでいる場合は、古いsnapshotへの差分追加ではなく、新しいexact full snapshotを1個生成する。
4. Library snapshotは原則 **current + 直前1世代** の2世代だけを保持する。3世代以上を残す必要がある場合はproject固有理由を明示する。
5. 新snapshotのarchive/hash/manifest検証が完了する前にprevious snapshotを削除しない。検証後に `current -> previous`、new -> current の順でrotationする。
6. snapshotがcurrent target HEADと一致しない場合、そのsnapshotをcurrent repository authorityとして扱わない。必要ならbaseline/referenceとして明示的に使う。
7. branch固有作業ではIssueの `Branch` / `Current HEAD` がauthorityであり、Libraryのmain snapshotをbranch HEADの代替にしない。
8. snapshot取得workflow、Library snapshot path、reuse判定、rotation policyはPROJECT BOOTSTRAPから到達できるようにする。
9. Actions artifact自体がまだ有効でも、Libraryに同一exact snapshotがありhash検証済みなら、artifactの再downloadを必須としない。
10. Actions artifactが期限切れでも、Library snapshotのcommit/hash/manifestが検証可能なら、そのexact snapshotを再利用してよい。

この運用は、repositoryのsource-of-truthをLibraryへ移すものではない。GitHubのbranch/ref/commitがauthorityであり、Library snapshotはexactly identified retrieval cache / reusable baselineとして扱う。

## 5. 作業終了時

作業が完了したらIssueに最終コメントを残す。

最低限、以下を記録する。

```text
Completed

- 実装内容
- 変更した主要モジュール
- 追加・更新したtests
- Visual QA結果（必要な場合）
- CI結果
- 最終HEAD

Remaining:
- なし
```

または、

```text
Remaining:
- 今回のScope外として残したもの
```

作業終了またはhandoff時には、Issueに関連するbranch lifecycleも閉じる。

- `Merge Intent=YES` かつ `MERGE_READY` なら、特段の理由がなければ次branchへ進む前にmergeを優先する。
- `Merge Intent=NO` または明示的に `ABANDONED` と判断したbranchは、必要なfinding / recreate pathをIssueへ残して削除する。
- 未mergeで残す場合は、Issueの `Branch Class / Merge Intent / Branch State / Review or Expiry / Keep or Drop Rule / Current HEAD` を更新する。
- Library Current Stateのactive branch inventoryも同じ節目で更新する。

Acceptance criteriaを満たしたIssueはCloseする。

まだ作業が残っている場合はCloseせず、次に行う作業がIssueから明確に分かる状態にして終了する。

## 6. Issueの分割

作業中に別の独立した問題を発見した場合、現在のIssueへ無理に混ぜない。

別テーマとして追跡すべき内容なら新しいIssueを作成し、相互にリンクする。

ただし、細かすぎるIssueを大量生成しない。

1つの原因・目的・完了条件として自然に扱える範囲は同じIssueにまとめる。

## 7. 作業開始時の確認順

原則として以下を確認してから実装を開始する。

1. repositoryを特定し、関連するOpen Issueを確認する
2. PROJECT BOOTSTRAPからLibrary Current Stateへ到達できる場合、active Issue / active branch inventory / merge orderを確認する
3. `MERGE_READY` または期限到達branchがあれば、新しいbranch作成前にBranch Drain Gateを適用する
4. 対象Issueに記録された作業branch / Branch Class / Merge Intent / Branch State / Review or Expiry / Current HEADを確認する
5. 現在アクセス可能なcheckoutのbranch / HEADを確認し、Issueの作業branchと一致させる
6. project全体のfocus / active Issue順序と対象Issueのcurrent focusを確認する
7. current spec
8. project固有authority（解析系projectでは任意でHidden Fact Registryを含む）
9. 現在の実装
10. tests / CI
11. 必要に応じて過去のclosed Issue / commit履歴

Issueに作業branchがある場合、5の一致確認前に書込みを開始しない。新branch作成前には2〜4で既存branchをdrainできないか確認する。過去sessionのlocal checkout/worktree pathは再開authorityにせず、存在しない場合は探索へ時間を使わずbranchからfresh checkoutする。

古い会話上の情報より、repository・current spec・現在のIssueの状態を優先する。

## 8. PROJECT BOOTSTRAPとの関係

GitHubを継続作業に使うprojectでは、PROJECT BOOTSTRAPから本共通仕様へ到達できるようにする。

PROJECT BOOTSTRAPには、本仕様の全文を複製せず、少なくとも以下を記載する。

- 本仕様を必読GitHub運用authorityとして参照すること
- 作業開始時にOpen Issueを確認すること
- project固有の安全上のguardrail
- current spec / project固有authorityへの到達方法。解析系projectでは任意でHidden Fact Registryを含めてよい
- projectで使用するLibrary project folderのcanonical path
- Library Current Stateを使う場合は `PROJECT_STATE.md` とactive Issue state rootへのcanonical path
- 作業開始時に必要なrepository / branch / main entrypoint / test / build / validation等への到達方法
- project固有の外部取得fallback、remote runner、Actions workflow等がある場合はその到達方法

### BOOTSTRAP maintenance rule

作業中に、次回のAI/担当者が作業開始・再開するために継続的に必要となる情報を新たに確定した場合、その情報がcurrent specやIssueに存在するだけで十分とせず、PROJECT BOOTSTRAPから直接または明示的参照で到達できるように更新する。

BOOTSTRAPへ入れるべき情報の例:

- canonical repository identity / repository full name
- current/default branch、主要entrypoint
- current spec / project固有authority fileへの参照。解析系projectでは任意でHidden Fact Registryを含めてよい
- Library project folderのcanonical path
- reusable repository snapshot folder / snapshot workflow / reuse・rotation policy
- Library Current Stateを使うprojectではproject state / active Issue stateへのcanonical path
- 必須のOpen Issue確認手順
- Issueをauthorityとした作業branch確認と、書込み前のbranch一致確認手順
- Branch Class / Merge Intent / Branch State / Review or Expiry / Branch Drain Gateの確認手順
- build / test / validation / visual QA等の開始点
- pytestを使うprojectではcanonical `PYTHONPATH` とcanonical pytest command
- project固有の重要guardrail、禁止事項、fail-closed条件
- Actions workflow、remote runner、artifact回収等のproject固有fallback
- project固有のsource-of-truthや復旧手順

BOOTSTRAPへ入れないもの:

- 一時的な進捗
- そのsessionだけの作業メモ
- すぐ陳腐化する途中結果
- Issue/checkpointで管理すべき詳細履歴

判断基準は、**別chat・別AIがBOOTSTRAPを起点に、追加の会話記憶なしで正しいauthorityと作業入口へ到達できるか** とする。

新しいproject固有folder、authority、workflow、entrypoint、復旧経路等を追加・変更した場合は、同じ変更単位でBOOTSTRAPの参照も更新する。仕様だけ更新してBOOTSTRAP参照を古いまま残さない。

## 9. Handoff / restartability

GitHub Issueを、

**作業指示 + 進捗記録 + 設計判断 + 引き継ぎ**

として使用する。

最終的に、別チャットや別担当者が入っても、

**repository + Open Issuesを見るだけで現在の作業を再開できる状態**

を維持する。

`CURRENT HANDOFF — <branch名>` のような常設HANDOFF専用Issueを必須とはしない。作業テーマごとの通常Issueを正とする。

## 10. Repository stateとIssueの優先関係

Issueは作業状態とsemantic decision historyを伝える記録であり、repositoryの実体やcurrent AISPEC/current specを上書きするauthorityではない。

矛盾が見つかった場合は、まずcurrent repository stateとcurrent specを確認する。ただし「current specが正しい」と自動決定してIssueだけを書き換えない。仕様自体が誤っている可能性がある場合は、current RULE_IDの `SOURCE / DECISION_REF` からdecision historyを確認し、必要なら新しいIssueで再検証する。

## 11. Validation checklist

GitHub継続作業の終了時またはhandoff時には、必要に応じて以下を確認する。

- 同一作業テーマの重複Open Issueを作っていない
- IssueからGoal / Scope / Acceptance criteriaが分かる
- AISPEC semantic changeを含む場合、Issueからaffected RULE_ID / specification closure / decision reasonへ到達できる
- AISPEC semantic change後は、変更ruleの DECISION_REF からdecision Issueへ逆引きできる
- Library Current Stateを使っている場合、Issueにできる大きさの作業をSTATEだけで抱え続けていない
- PROJECT_STATE / active ISSUE_STATEが現在focus・順序・blocker・nextを反映し、Issue/current specと矛盾していない
- Issueに作業branch / Current HEADが記録され、書込み対象checkoutとbranchが一致している
- branchがある場合、Issueに Branch Class / Merge Intent / Branch State / Review or Expiry / Keep or Drop Rule が記録されている
- `Merge Intent=UNDECIDED` のbranchが期限なしで放置されていない
- `Merge Intent=YES` / `MERGE_READY` のbranchを残したまま理由なく新branchを増やしていない
- Library Current Stateのactive branch inventory / merge orderがIssueと矛盾していない
- `MERGED` / `ABANDONED` branchがactive stateへ残り続けていない

- staleなlocal worktree pathをhandoff authorityにしていない
- 次回必要な変更がアクセス不能な未commit差分だけに残っていない
- 重要な設計判断が会話だけに残っていない
- semantic changeの判断理由がcommit messageだけに閉じていない
- 意味のあるrepository変更はcommit済み
- HANDOFFだけのcommitを作っていない
- tests / CIの最新状態がIssueから分かる
- pytestを実行した場合、canonical `PYTHONPATH` を明示したcommandでvalidationしている
- 外部取得をActionsへfallbackした場合、取得元・revision/hash・artifact/runを必要に応じて追跡できる
- reusable exact snapshotを使った場合、target HEADとsnapshot commit SHAの一致または明示的なbaseline扱いが確認できる
- 未完了ならNext / RemainingがIssueから分かる
- 完了済みなら最終HEADがIssueに記録されている
- Acceptance criteria達成済みIssueを必要なくOpenのまま放置していない
- merge済みまたはabandon済みのremote branchを保存理由なく残していない
- repository + Open Issuesだけで次の作業者が再開できる
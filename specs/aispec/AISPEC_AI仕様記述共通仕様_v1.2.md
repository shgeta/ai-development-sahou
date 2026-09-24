# AISPEC AI仕様記述 共通仕様 v1.2

更新日: 2026-09-24
状態: DRAFT

## 0. 位置づけ

AISPECは、AIが仕様を解釈・実行・監査するときに、自然文の章構成、ファイル名、保存場所、記載順、Markdownの見た目へ意味を依存させないための共通仕様記述形式である。

Markdown / CSV / Spreadsheet / JSON等は保存・表示の器であり、仕様の意味そのものではない。

仕様の意味は、各ルール行に明示されたフィールドと、明示された関係から復元できなければならない。

## 1. 目的

AISPECの目的は以下である。

1. AIが「何をするルールか」を曖昧なく判断できること。
2. 適用対象・適用範囲・例外・発動条件を分離して記述できること。
3. 仕様の意味を文章の前後関係だけに依存させないこと。
4. ファイルの並び替え、章移動、表のソート後も意味が壊れないこと。
5. 複数ルールのまとまり、順序、依存関係を明示できること。
6. AIが「不明」「未確定」「対象外」を勝手に補完しないこと。
7. 人間が読めることと、AIが機械的に解釈できることを両立すること。

## 2. 最重要原則

### 2.1 Meaning over position

ルールの意味を以下に依存させてはならない。

- ファイル名
- フォルダ位置
- Markdown見出し階層
- 表の物理行番号
- 前後の文章だけから推測する文脈
- 「上記」「下記」「前述」「次のとおり」だけの参照

これらは可読性の補助には使えるが、仕様の唯一の意味根拠にしてはならない。

### 2.2 Explicit semantics

AIが判断に必要とする情報は、可能な限り明示フィールドとして持つ。

最低限、次を区別する。

- 何のルールか
- 何を意味するか
- どこまで効くか
- 何を含め切るか
- いつ発動するか
- いつ発動しないか
- 何に対して作用するか
- 例外・注意

### 2.3 Unknown is not false

不明・未確認・未実装・対象外を同一視しない。

AIは情報が欠けている場合、勝手に `false` / `0` / `none` / 対象外へ丸めてはならない。

推奨状態:

- `KNOWN`
- `UNKNOWN`
- `REVIEW_REQUIRED`
- `NOT_APPLICABLE`
- `NOT_IMPLEMENTED`
- `DEFERRED`

## 3. 標準レコード構造

### 3.1 基本列

AISPECの標準列は以下とする。

| FIELD | 必須 | 意味 |
|---|---|---|
| `RULE_ID` | 必須 | 行位置や表示名に依存しない一意なルールID |
| `TITLE` | 必須 | 人間向けの短いルール名 |
| `TYPE` | 必須 | ルールの種類 |
| `MEANING` | 必須 | そのルールが意味する内容そのもの |
| `SCOPE` | 必須 | ルールが有効な範囲 |
| `CLOSURE` | 条件付き必須 | 対象をどこまで辿り、何を含め切るか |
| `WHEN` | 条件付き必須 | 発動条件 |
| `UNLESS` | 任意 | 発動しない条件・例外条件 |
| `TARGET` | 必須 | 実際に作用する対象 |
| `NOTE` | 任意 | 補足。主要な意味をNOTEだけに置かない |

### 3.2 構造列

複数ルールの関係・順番を表すため、以下を使用する。

| FIELD | 必須 | 意味 |
|---|---|---|
| `GROUP` | 任意 | 意味上の仮想まとまり。物理的な章・ファイル配置とは独立 |
| `ORDER` | 条件付き必須 | 順序が意味を持つ場合の明示順 |
| `DEPENDS_ON` | 任意 | 先に成立している必要がある `RULE_ID` |
| `PRECEDES` | 任意 | このルールより後に扱うべき `RULE_ID` |
| `STATUS` | 推奨 | DRAFT / REVIEW / APPROVED / DEPRECATED 等 |
| `SOURCE` | 推奨 | ルールの現在意味を支える根拠となる仕様・データ・観測・外部authority |
| `DECISION_REF` | 条件付き推奨 | 現在意味を決めたsemantic decision recordへの参照。GitHub/AISPEC projectでは原則Issue |

`GROUP` と `ORDER` を追加しても、基本列 `TITLE / TYPE / MEANING / SCOPE / CLOSURE / WHEN / UNLESS / TARGET / NOTE` はAISPECの意味記述の中核として維持する。

## 4. FIELD定義

### 4.1 RULE_ID

ルールの不変識別子。

例:

- `SRC.CLOSURE.001`
- `PDF.ANNOTATION.010`
- `FORECAST.EVENT.020`

禁止:

- 表示上の行番号だけをIDとして使う
- タイトル変更でIDまで変更する
- ファイルパスをIDの唯一の意味にする

### 4.2 TITLE

短く識別可能な名称。

TITLEは人間向け表示名であり、仕様の完全な意味をTITLEだけに背負わせない。

### 4.3 TYPE

その行が何の種類の仕様かを示す。

推奨値:

- `RULE`
- `REQUIREMENT`
- `PROHIBITION`
- `CONDITION`
- `TRANSFORM`
- `VALIDATION`
- `OUTPUT`
- `SEQUENCE`
- `REFERENCE`
- `REVIEW_GATE`

案件固有TYPEを追加してよいが、意味を定義すること。

### 4.4 MEANING

そのルールの意味を、他行の位置関係に依存せず説明する。

MEANINGだけ読んでも「何を保証・禁止・変換・確認するルールか」が分かること。

悪い例:

`前述の条件に従う。`

良い例:

`選択されたsource rootからleafまで全descendantを保持し、途中階層を省略しない。`

### 4.5 SCOPE

ルールが有効な論理範囲。

例:

- `all_pages`
- `selected_part`
- `PDF and PPTX inputs`
- `forecast rows where event_scope=product`
- `user-visible output only`

SCOPEは「どこに効くか」であり、TARGETとは分ける。

### 4.6 CLOSURE

対象を辿る必要がある場合に「どこまで含めれば閉じるか」を定義する。

例:

- `root -> all descendants -> leaf`
- `INSTANCE -> source component -> nested INSTANCE recursively`
- `page -> section -> part -> visible primitive`
- `current record only`

CLOSUREがない対象では空欄または `self` を使用してよい。

深さ制限や途中打ち切りがある場合は必ず明示する。

### 4.7 WHEN

ルールが発動する正条件。

例:

`source node type == INSTANCE`

`WHEN` が常時成立する場合は `always` と明示してよい。

### 4.8 UNLESS

例外・抑止条件。

例:

`UNLESS target is explicitly classified as annotation/helper`

WHENとUNLESSが競合する場合、原則としてUNLESSを優先する。ただし別の優先ルールがある場合はそれを明示する。

### 4.9 TARGET

実際に処理・検証・出力・禁止の対象となるもの。

例:

- `visible TEXT nodes`
- `annotation records`
- `monthly forecast rows`
- `final user-facing report`

SCOPEが論理的な適用範囲、TARGETが具体的な作用対象である。

### 4.10 NOTE

補足、理由、例、実装メモを記載する。

NOTEだけを読まないとルールの意味が成立しない記述は禁止する。

### 4.11 SOURCE

現在のルール意味を支える根拠を記載する。SOURCEは、source specification、raw/API fact、外部標準、法令、検証データ、観測記録等の **evidence / authority provenance** を表す。

SOURCEは「なぜその選択を採用したか」という議論履歴の代替にはしない。semantic decisionの経緯を追跡する必要がある場合は `DECISION_REF` を分離して使用する。

SOURCEとrule本文が矛盾する場合、矛盾を黙って解消せず、current authorityを確認してREVIEW_REQUIREDまたは変更Issueへ送る。

### 4.12 DECISION_REF

`DECISION_REF` は、**現在のsemantic meaningを採用・変更した判断記録への入口**である。GitHubを作業管理に使うAISPEC projectでは、原則としてGitHub Issueを参照する。

例:

- `#43`
- `owner/repo#43`
- `https://github.com/owner/repo/issues/43`
- GitHubを使わないprojectでは、同等の永続decision record ID

運用原則:

- `DECISION_REF` は仕様意味そのものではなくprovenanceであり、`MEANING` 等を上書きしない。
- current ruleが「なぜこの意味なのか」を確認したい場合、`SOURCE` で根拠を確認し、`DECISION_REF` から判断経緯へ入る。
- GitHub/AISPEC projectで既存ruleのsemantic meaningを変更した場合、変更後ruleの `DECISION_REF` をそのsemantic change Issueへ更新する。
- current meaningが複数の独立decisionに依存する場合は、意味を説明するために必要な最小集合を列挙してよい。
- 新しいdecisionが以前のdecisionを置き換える場合、最新Issue側からprior decisionへ辿れるようにする。AISPEC recordへ無制限な履歴列を蓄積しない。
- legacy import等でdecision recordが存在しないruleは無理に捏造しない。SOURCEとGit historyをfallbackとして使用し、意味に疑義が残る場合は新しいIssueを作成して再検証する。

## 5. GROUP — 仮想の塊

`GROUP` は、複数のルールを意味上ひとつのまとまりとして扱うための仮想グループである。

GROUPは以下と独立する。

- Markdown章
- ファイル
- フォルダ
- 表の連続行

同じGROUPのルールが別ファイルに分散していてもよい。

例:

`GROUP = PDF_ANNOTATION_GENERATION`

`GROUP = FIGMA_SOURCE_CLOSURE`

`GROUP = MONTHLY_OUTPUT_VALIDATION`

GROUP自身に意味を持たせる必要がある場合は、GROUP定義レコードを別途設ける。

## 6. ORDER — 順番

順番が結果へ影響する処理では、表の上から下を暗黙の実行順としない。

`ORDER` を明示する。

例:

| RULE_ID | GROUP | ORDER | TITLE |
|---|---|---:|---|
| `P.010` | `PDF_FLOW` | 10 | 原文確定 |
| `P.020` | `PDF_FLOW` | 20 | annotation化 |
| `P.030` | `PDF_FLOW` | 30 | validation |
| `P.040` | `PDF_FLOW` | 40 | PPTX生成 |

推奨は10刻みとし、後から中間ステップを追加可能にする。

順序が意味を持たない場合はORDERを空欄にしてよい。

### 6.1 順序の種類

必要に応じてORDERの意味を分離する。

- `EXEC_ORDER`: 実行順
- `DISPLAY_ORDER`: 表示順
- `SCAN_ORDER`: 走査順
- `PRIORITY`: 優先順位

一つのORDER列では曖昧になる場合、上記の専用列へ分割する。

## 7. DEPENDS_ON — 依存関係

順番と依存関係は別物として扱う。

`ORDER=20` だから `ORDER=10` に依存する、と推測してはならない。

依存がある場合は `DEPENDS_ON` に `RULE_ID` を明示する。

例:

`DEPENDS_ON = P.010, P.015`

循環依存は禁止する。循環が意味上必要な場合は、反復処理として別のSEQUENCE仕様にする。

## 8. 条件・例外の記述

### 8.1 正条件と否定条件を分ける

一文に複雑な条件を押し込まず、原則として `WHEN` と `UNLESS` に分ける。

### 8.2 推測禁止

条件に必要な値がUNKNOWNの場合、条件を勝手に成立・不成立へ倒さない。

標準挙動:

`condition input UNKNOWN -> REVIEW_REQUIRED`

別の挙動にする場合は明示する。

### 8.3 条件の優先

原則:

1. 明示的な禁止・UNLESS
2. 明示的なWHEN
3. 通常ルール
4. NOTEや例示

案件固有の優先順位がある場合は別ルールとして定義する。

## 9. 仕様の物理媒体

AISPECは以下で表現できる。

- Markdown table
- CSV / TSV
- Spreadsheet
- JSON / YAML
- Database table

媒体を変換しても、FIELDと関係を保持すれば意味は同一である。

### 9.1 Markdown

Markdownの見出しは可読性のために利用してよい。

ただし見出し階層だけを仕様のscopeやgroupとして扱わない。

### 9.2 Spreadsheet / CSV

1行1ルールを基本とする。

セル結合へ意味を依存させない。

### 9.3 JSON

各行をobjectとして保持する。

例:

```json
{
  "RULE_ID": "SRC.CLOSURE.010",
  "TITLE": "Instance definition expansion",
  "TYPE": "REQUIREMENT",
  "MEANING": "INSTANCEはsource component definitionへ展開し、nested INSTANCEも再帰的に解決する。",
  "SCOPE": "selected source closure",
  "CLOSURE": "INSTANCE -> source component -> nested INSTANCE recursively",
  "WHEN": "node.type == INSTANCE",
  "UNLESS": "source definition is unavailable",
  "TARGET": "INSTANCE node",
  "GROUP": "FIGMA_SOURCE_CLOSURE",
  "ORDER": 40,
  "STATUS": "APPROVED",
  "SOURCE": "spec/source-closure.md#instance-expansion",
  "DECISION_REF": "owner/repo#43",
  "NOTE": "unavailableの場合は silently dropせず unresolved recordを残す"
}
```

## 10. 最小テンプレート

```text
| RULE_ID | TITLE | TYPE | MEANING | SCOPE | CLOSURE | WHEN | UNLESS | TARGET | GROUP | ORDER | DEPENDS_ON | STATUS | SOURCE | DECISION_REF | NOTE |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

すべての案件で全列を表示する必要はない。

ただし省略した列の意味が必要な場合、別の暗黙表現に逃がしてはならない。

## 11. 必須性

### 常時必須

- `RULE_ID`
- `TITLE`
- `TYPE`
- `MEANING`
- `SCOPE`
- `TARGET`

### 条件付き必須

- `CLOSURE`: 再帰・包含範囲・終端条件がある場合
- `WHEN`: 常時適用でない場合
- `ORDER`: 順序が意味を持つ場合
- `DEPENDS_ON`: 他ルール成立が前提の場合

### 任意

- `UNLESS`
- `GROUP`
- `NOTE`
- `SOURCE`
- `DECISION_REF`

ただし任意列へ主要な意味を隠してはならない。Original/legacy ruleでdecision recordが存在しない場合、`DECISION_REF` を捏造して埋める必要はない。

## 12. AI解釈ルール

AIがAISPECを読む場合、以下の順で解釈する。

1. `RULE_ID`でルールを識別する。
2. `STATUS`を確認し、無効・deprecatedルールを区別する。
3. `TYPE` と `MEANING` でルールの意味を確定する。
4. `SCOPE` と `TARGET` で適用対象を決める。
5. `WHEN` / `UNLESS` で発動可否を決める。
6. `CLOSURE` で対象をどこまで辿るか決める。
7. `DEPENDS_ON` を解決する。
8. `GROUP` と `ORDER` があれば処理関係を構成する。
9. `SOURCE` でevidence/authority provenanceを確認し、必要に応じて `DECISION_REF` からsemantic decision historyへ入る。
10. `NOTE` を補助情報として使う。
11. 不明値が残れば勝手に補完せず、定義されたUNKNOWN方針へ送る。

## 13. Validation

AISPECは最低限以下を検証できる状態とする。

- `RULE_ID` 重複 0件
- 必須FIELD欠落 0件
- `DEPENDS_ON` の存在しないRULE_ID参照 0件
- 循環依存 0件
- 順序が必要なGROUPでORDER欠落 0件
- `WHEN` / `UNLESS` に未定義語がある場合は検出
- `CLOSURE`が必要な再帰処理で終端不明 0件
- `STATUS=APPROVED` なのに `REVIEW_REQUIRED` な主要意味が残っていないこと
- GitHub/AISPEC projectでsemantic changeを行ったruleは、project policyに従い `DECISION_REF` からdecision recordへ到達できること

## 14. 禁止事項

以下は禁止する。

1. 「上記を参照」のみでルールの意味を成立させる。
2. Markdownの章位置だけでscopeを決める。
3. 行の並びだけで実行順を決める。
4. 同じ表の近接行だから同じgroupだと推測する。
5. 空欄を自動的にfalseと解釈する。
6. NOTEにしか書かれていない条件を主要条件として扱う。
7. ファイル名変更で仕様の意味が変わる設計にする。
8. UNKNOWNを推測で補完してAPPROVED扱いする。
9. TARGETとSCOPEを混同する。
10. CLOSUREの終端を暗黙にする。

## 15. 既存仕様をAISPEC化するときの手順

1. 既存仕様から個別ルールを抽出する。
2. 1ルール1意味になるよう分割する。
3. 各ルールへ `RULE_ID` を付与する。
4. `MEANING` を単独で理解可能な文へする。
5. `SCOPE` と `TARGET` を分離する。
6. 再帰・包含があれば `CLOSURE` を定義する。
7. 条件を `WHEN` / `UNLESS` に分離する。
8. 意味上のまとまりを `GROUP` にする。
9. 順序が意味を持つ場合のみ `ORDER` を付ける。
10. 前提関係を `DEPENDS_ON` で明示する。
11. 不明値・要確認を状態として残す。
12. Validationを通す。

## 16. 例 — PDF/PPTX校正フロー

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | CLOSURE | WHEN | UNLESS | TARGET | GROUP | ORDER | DEPENDS_ON | NOTE |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|
| `PROOF.010` | 原文母本確定 | REQUIREMENT | 修正前の原文・構成を正本として固定し、後工程で直接改変しない | 対象資料全体 | page/slide -> readable content | always | - | 原文・構成母本 | `PROOF_FLOW` | 10 | - | 修正は反映レイヤーで管理 |
| `PROOF.020` | 修正候補生成 | TRANSFORM | 母本を基準に修正候補を生成する | 校正対象 | all candidate findings | 母本確定後 | 事実に反しない項目 | 修正候補 | `PROOF_FLOW` | 20 | `PROOF.010` | - |
| `PROOF.030` | annotation化 | TRANSFORM | 確定修正を1修正=1 annotationへ変換する | 確定修正 | each confirmed correction | 修正確定後 | 未確定候補 | annotation | `PROOF_FLOW` | 30 | `PROOF.020` | - |
| `PROOF.040` | 生成前検証 | VALIDATION | annotation完全性を検証し、エラーがあれば生成を停止する | annotation全件 | all annotations | PPTX生成前 | - | annotation set | `PROOF_FLOW` | 40 | `PROOF.030` | エラー0件がgate |

この表は例であり、AISPEC自体をPDF/PPTX校正用途へ限定しない。

## 17. 例 — 順序を持たないルール群

同じGROUPでも、独立ルールで順序が意味を持たなければORDERは不要である。

| RULE_ID | TITLE | TYPE | GROUP | ORDER |
|---|---|---|---|---|
| `STYLE.010` | 単位表記 | RULE | `STYLE_RULES` | - |
| `STYLE.020` | 日付表記 | RULE | `STYLE_RULES` | - |
| `STYLE.030` | 略語初出 | RULE | `STYLE_RULES` | - |

GROUPは「塊」、ORDERは「順番」であり、別概念である。

## 18. 完成条件

AISPEC形式の仕様が完成したとみなす条件は以下である。

1. 各ルールが行位置に依存せず理解できる。
2. 対象範囲と作用対象が明確である。
3. 条件・例外・不明時挙動が明確である。
4. 必要なclosureが明示されている。
5. 仮想まとまりが必要ならGROUPで表現されている。
6. 順序が必要ならORDERで表現されている。
7. 依存関係が必要ならDEPENDS_ONで表現されている。
8. 並び替え・媒体変換後も意味が保持される。
9. AIが不足情報を勝手に補完せず処理できる。
10. Validation可能な構造になっている。

## 19. 今後の適用方針

新しくAI向け仕様書を作成・改訂する場合、まず通常の読みやすい説明を作るのではなく、仕様上重要なルールをAISPECレコードへ落とせるか確認する。

人間向けの章立て・説明文・図・例はAISPECを補助するpresentation layerとして追加してよい。

正本を表形式そのものに限定する必要はないが、AIが最終的に `RULE_ID / TITLE / TYPE / MEANING / SCOPE / CLOSURE / WHEN / UNLESS / TARGET` と、必要に応じて `GROUP / ORDER / DEPENDS_ON` を復元できることを必須とする。


## 20. Physical Sharding — 仕様の物理分割

AISPEC仕様は、API取得制約、ファイルサイズ、可読性、編集性、保存媒体の都合により複数ファイルへ分割してよい。

分割は物理上の都合であり、以下へ仕様の意味を依存させてはならない。

- shardのファイル名
- shardの並び順
- shard内での記載順
- フォルダ位置
- 何番目のshardに入っているか

分割後も `RULE_ID / TYPE / MEANING / SCOPE / TARGET` と、必要に応じた `CLOSURE / WHEN / UNLESS / GROUP / ORDER / DEPENDS_ON` だけから仕様を復元できなければならない。

ファイルサイズの目安はAISPECの意味ではなく、利用環境・API・transport上の運用値とする。案件ごとに「現在安全と確認された目安」を設定してよく、実測で安全性が確認された場合は拡大してよい。共通AISPECは特定のKiB値を固定上限としない。

## 21. Spec Retrieval — 検索と仕様closure

大規模AISPECでは、全仕様を毎回一括取得することを必須としない。

標準取得手順は以下とする。

```text
SEARCH
  -> seed RULE
  -> specification closure resolution
  -> required specification set
```

### 21.1 SEARCH

作業テーマ、既知の `RULE_ID`、`GROUP`、対象名、具体的な用語などから起点となるseed RULEを検索する。

検索結果のファイル位置や検索順位そのものを仕様根拠にしてはならない。

### 21.2 specification closure

seed RULEを取得した後、正しく解釈するために必要な仕様関係を辿る。

少なくとも以下を対象とする。

- `DEPENDS_ON` の再帰的解決
- 明示的に参照された `RULE_ID`
- 順序の解釈に必要な `GROUP / ORDER`
- そのrule自体の `CLOSURE` を理解するために明示された関連rule

参照先が見つからない、依存が循環する、必要な意味がUNKNOWNの場合は推測で閉じず `REVIEW_REQUIRED` とする。

ここでいう **specification closure** は、AISPEC field `CLOSURE` が表す「対象をどこまで含め切るか」とは別概念である。

### 21.3 変更時のreverse dependency

仕様を読むだけでなく変更する場合は、上流依存だけでなく対象ruleを参照するreverse dependencyも検索し、変更影響範囲を確認する。

```text
seed RULE
  -> dependencies
  -> reverse dependencies
  -> impacted specification set
```

## 22. Search Index — 任意の検索補助

検索用INDEX、manifest、routing table等を置いてよいが、これらは原則としてnavigation / cacheであり仕様authorityではない。

INDEXは以下を満たす。

- 無くてもAISPECを正しく検索・解釈できること
- rule本文の主要意味をINDEXだけへ置かないこと
- INDEXの並び順へ意味を依存させないこと
- INDEXとrule本文が矛盾した場合、rule本文と明示authorityを優先すること
- 古いINDEXが仕様の意味を変更しないこと

INDEXは検索速度を改善する場合にだけ使用し、維持コストやstale riskの方が大きい場合は設置しなくてよい。

## 23. Project Bootstrap — 案件・アプリの必読入口

継続開発、複数チャット、複数担当、AI間ハンドオフを想定するAISPEC案件では、案件ごとに **PROJECT BOOTSTRAP** を明示する。

PROJECT BOOTSTRAPは、前会話を知らない新しい作業者が安全に作業開始するための必読入口である。

PROJECT BOOTSTRAPには最低限以下への到達方法を記載する。

- project / applicationの識別
- current specification authority
- source / repository authority
- 作業開始時に必ず確認するcurrent HEAD / branch / revision等
- 外部registry・外部仕様などの必読authority
- production / destructive operation等の安全上のguardrail
- SEARCH -> seed RULE -> specification closure の取得手順
- current handoff / current state の所在

PROJECT BOOTSTRAPへ全仕様本文を複製しない。BOOTSTRAPは入口と必須前提を示し、詳細意味はAISPEC ruleへ辿れるようにする。

「BOOTSTRAPを最初に読む」という要件は物理的なファイル順ではなく、案件の明示的な開始前提として定義する。

## 24. Handoff — ゼロ文脈での再開可能性

AISPEC案件は、可能な限り **前会話・暗黙知・直前担当者の記憶がなくても再開できる** 状態を保つ。

継続作業では、仕様authorityとは別にCURRENT HANDOFF / CURRENT STATEを保持してよい。

Handoffには、必要に応じて以下を記録する。

- 現在のbranch / HEAD / revision
- 現在の作業焦点
- 完了済み事項
- 未完了事項・REVIEW_REQUIRED
- 最新のtest / CI / validation状態
- 既知の危険箇所・禁止事項
- 次に安全に行う作業

Handoffは現在地を伝えるための資料であり、仕様authorityを上書きしてはならない。

再開時の標準優先関係は以下とする。

```text
PROJECT BOOTSTRAP
  -> current specification authority
  -> current source / repository / test facts
  -> CURRENT HANDOFF
  -> task-specific SEARCH and specification closure
```

Handoffとcurrent sourceが矛盾した場合、current sourceの実測事実を優先し、仕様との不一致は別途検出・解決する。

## 25. AISPEC Writing / Change Workflow

AISPECを新規記述・追記・変更する場合は、重複ruleや隠れた矛盾を避けるため、原則として先に既存仕様を検索する。

標準フロー:

```text
PROJECT BOOTSTRAP
  -> SEARCH existing rules
  -> seed RULE / related GROUP
  -> specification closure
  -> reverse dependency check when changing existing meaning
  -> semantic changeならdecision/work Issueを確認・作成
  -> add or revise AISPEC rule
  -> Validation
  -> implementation / test / CI evidenceをIssueへ結合
  -> update handoff/current state when work state changed
```

新しいruleを追加する前に、同じ意味を持つ既存ruleがないか確認する。

既存ruleの意味を変更する場合は、`RULE_ID` を安易に作り直さず、互換性・参照関係・STATUSを確認する。

GitHub等で継続開発を管理するprojectでは、semantic changeをcommitだけで完結させない。意味変更の理由・観測・判断・影響範囲・validationを追跡できるIssueまたは同等のdecision recordを先に確保し、変更後ruleの `DECISION_REF` からそこへ到達できるようにする。

semantic changeに含むものの例:

- `MEANING / SCOPE / CLOSURE / WHEN / UNLESS / TARGET` の意味変更
- `DEPENDS_ON / PRECEDES` の意味上の依存変更
- execution semanticsに影響する `GROUP / ORDER` の変更
- production membershipや有効性を変える `STATUS` 変更
- behaviorを追加・削除するruleの新設 / DEPRECATED化

原則としてsemantic changeに含めないものの例:

- 誤字修正
- Markdown整形
- 意味を変えない物理shard移動
- search index / manifestの再生成
- 意味を変えないSOURCE/DECISION_REFの参照修正

「semanticかどうか」が不明な変更は、非semanticと決め打ちせずIssue側で確認する。

### 25.1 仕様に疑義が出たときの追跡順

current AISPEC ruleが誤っている可能性を検討する場合、標準の追跡入口は次とする。

```text
current RULE_ID
  -> SOURCE
  -> DECISION_REF / semantic decision Issue
  -> Issue内のreason / alternatives / evidence
  -> PR / commit
  -> exact diff / tests / CI
```

**semantic historyの入口はdecision Issue、exact change historyの入口はcommit/PR** とする。

Issueが存在する場合、commit履歴を先に大量探索して判断理由を推測しない。Issueでdecision contextを把握した後、exact implementation差分や当時のtest evidenceを確認するためにcommit/PRへ降りる。

DECISION_REFが存在しないlegacy ruleでは、SOURCEとGit historyをfallbackとして使用してよい。ただし判断理由が再構成できない場合は、新しいIssueを作り `REVIEW_REQUIRED` として再検証する。

Issueの過去判断とcurrent AISPECが矛盾する場合、実行時のcurrent specification authorityはAISPECである。ただし矛盾を「Issueが古い」で黙って捨てず、current meaningが正しいかを新しいIssueで確認する。

### 25.2 Distributed Specification Database Model — 分散仕様データベースとしての扱い

AISPECは、単一fileを正本とする文書形式ではなく、複数のphysical shardへ分散保存できる **logical specification database** として扱う。

概念上の対応は次とする。

```text
AISPEC logical specification set
  = logical database

RULE_ID
  = logical primary key

physical file / shard
  = storage partition

SEARCH + specification closure
  = query / relation resolution

Search Index / manifest
  = optional navigation cache

PATCH
  = existing record UPDATE / DELETE

NEW SHARD
  = batch INSERT / append partition

MIGRATION
  = schema / semantic model migration

AISPEC Hygiene
  = compaction / normalization / consistency maintenance
```

物理fileの境界はauthorityの境界ではない。同じlogical specification setに属するruleは複数fileへ分散してよく、どのfileから取得を開始しても、必要な `RULE_ID / GROUP / DEPENDS_ON / explicit reference / specification closure` を辿ることで必要仕様集合へ到達できなければならない。

同一logical primary keyである `RULE_ID` に、同時に有効な矛盾definitionを複数作ってはならない。migration中にold/new representationを併存させる場合は、`STATUS`、mapping、cutover条件等でどちらがcurrent authorityかを明示する。

### 25.3 Physical Write Strategy — PATCH / NEW SHARD

AISPECへの書込み方法は、semantic designとphysical transportを分離して決める。GitHub connector、local Git checkout、Libraryその他の保存媒体でも同じ原則を適用する。

基本規則:

1. **既存rule / 既存recordの変更はPATCHする。** 変更箇所が多い場合も、必要な回数へ分割して複数PATCHしてよい。
2. **既存rule / 既存recordの削除もPATCHで行う。** semantic historyを保持すべき場合はphysical deleteではなく `STATUS=DEPRECATED` 等を選べるが、その変更自体はPATCHとして扱う。
3. **新規ruleの少量追加は、既存shardへのPATCH/appendまたはNEW SHARDのどちらでもよい。** semantic整合性と安全性を優先する。
4. **新規rule・新規recordの書込み量がproject/runtimeで定めたshard write threshold以上になる場合は、既存fileへの大きな追記を試さず、最初からNEW SHARD / NEW FILEを第一選択とする。**
5. NEW SHARDは新authorityを意味しない。同じlogical specification setへ参加させ、SEARCH + specification closureから到達可能にする。
6. shard write thresholdはAISPECの意味ではなく運用値とする。byte数、record数、rule数、connector制約、patch安全域等からproject/runtimeごとに決めてよい。共通AISPECは固定値を要求しない。
7. transport/API/tool limitationを理由にsemantic versionを上げたり、同じruleを重複definitionしたりしてはならない。
8. **既存AISPEC authority fileのroutine full-file replacementは行わない。** 既存内容の更新・削除はPATCH、新規大量追加はNEW SHARD、大規模変換はMIGRATIONとして扱う。

標準判断:

```text
WRITE REQUEST
  |
  +-- existing recordを変更/削除する？ -- YES --> PATCH x N
  |
  +-- new recordsの追加？
        |
        +-- write size >= shard write threshold --> NEW SHARD first
        |
        +-- below threshold --> PATCH/append or NEW SHARD
```

PATCHが複数回必要であること自体を失敗扱いしない。PATCH回数を減らすために既存file全体を置換しない。

### 25.4 Schema Evolution — field追加と後方互換

AISPEC fieldは、既存record全体を一括書換えせずに追加できる。

新fieldを追加するときは、少なくとも次を定義する。

- field name
- field meaning
- applicable scope / record type
- required / optional
- fieldが存在しないlegacy recordの解釈
- defaultがある場合はそのdefault
- existing recordへのbackfillが必要か
- migrationが必要になる条件

互換的なfield追加では、新規recordまたは今後変更されるrecordから新fieldを書き始めてよい。legacy recordにfieldが物理的に存在しないことを `false`、`0`、空文字、`NOT_APPLICABLE` 等へ自動変換してはならない。

field absenceはschema-layerの「未保持」であり、semantic valueの `UNKNOWN` とは区別する。field absence時の意味が必要ならfield定義側で明示的なdefault / inference ruleを定める。定義がなく、そのfieldなしでは正しい解釈ができない場合は `REVIEW_REQUIRED` とする。

次の場合は通常のfield追加ではなくMIGRATIONとして扱う。

- legacy recordを含む全recordで新fieldが必須であり、欠落すると意味が成立しない
- existing fieldの意味を変更する
- field rename / merge / splitにより既存参照の意味が変わる
- default追加によって既存recordの意味が実質的に変わる

### 25.5 AISPEC Migration — 大規模semantic/schema変更

相当大きい変更は、巨大PATCHやfull-file replacementとして処理せず **MIGRATION** として扱う。

MIGRATION候補:

- RULE_ID体系の大規模再設計
- GROUP / dependency / closure modelの大規模変更
- 大量ruleの統合・分割・置換
- required field追加に伴う広範なbackfill
- schemaの意味変更
- old representationからnew representationへのauthority切替

標準フロー:

```text
migration Issue / project
  -> current old modelを特定
  -> target model / mapping / cutover条件を定義
  -> new shard群を生成
  -> old -> new mappingを検証
  -> SEARCH + specification closure / reverse dependency validation
  -> authority cutover
  -> old側をPATCHでDEPRECATED / redirect
  -> migration evidenceをIssueへ記録
```

migration中もroutine full-file replacementを標準手段としない。new representationはNEW SHARDへ作成し、existing records側のstatus・mapping・reference変更はPATCHで行う。

### 25.6 AISPEC Hygiene — 意味を変えない定期整備

AISPECは分散追記を許容するため、物理的な整理を通常開発から分離して **AISPEC Hygiene** として実施してよい。

Hygieneはsemantic meaningを変更しないmaintenanceであり、periodicまたはtrigger-basedなIssue / projectとして実施できる。

対象例:

- shardの過度な断片化・肥大化
- duplicate / orphan RULE_IDの検出
- specification closureで到達不能なrule
- broken `DEPENDS_ON` / explicit reference
- stale Search Index / manifest
- schema fieldのばらつき・不要なlegacy表現
- DEPRECATED shard / ruleの整理
- GROUP / ORDER / dependencyの整合性検査
- public-safe違反・実project identifier混入のscan
- shard再配置・意味を変えない統合/分割

Hygiene中にsemantic meaningの変更が必要と判明した場合、その項目をHygieneのまま処理せず、通常のsemantic change IssueまたはMIGRATIONへ切り出す。

Hygieneの発動頻度・thresholdはproject/runtime固有の運用値とし、共通AISPECでは固定周期を要求しない。

## 26. 追加Validation — 分割・検索・ハンドオフ

大規模・分割AISPECでは、既存Validationに加えて以下を確認する。

- shard分割後も `RULE_ID` が全体で一意
- `DEPENDS_ON` / 明示RULE参照がshardを跨いで解決可能
- PROJECT BOOTSTRAPからcurrent specification authorityへ到達可能
- Handoffだけを読まなくても仕様意味が成立する
- INDEXを削除してもSEARCH + closureで仕様取得可能
- 物理ファイル順を変更しても仕様意味が不変
- 環境依存のファイルサイズ目安がAISPECの意味ルールへ混入していない
- handoff後、新しい作業者が前会話なしで必要authorityへ到達できる
- NEW SHARD追加後もSEARCH + specification closureから必要ruleへ到達可能
- routine writeで既存AISPEC authority fileのfull-file replacementを使用していない
- existing recordの変更・削除がPATCHとして追跡可能
- schema field追加時、legacy field absenceの解釈が定義されている
- MIGRATIONとHygieneが混同されず、semantic changeはmigration/decision recordへ切り出されている

## 27. 2026-09-16 追記

大規模仕様・GitHub/API経由の仕様取得・AI間ハンドオフを前提とした運用作法として、Physical Sharding、Spec Retrieval、任意Search Index、Project Bootstrap、Handoff、Writing / Change Workflowを共通仕様へ追加した。

## 28. 2026-09-20 追記

AISPECとIssue/commitの責務分離を明確化した。`SOURCE` はcurrent meaningを支えるevidence / authority provenance、`DECISION_REF` はcurrent semantic meaningを採用・変更したdecision recordへの入口とする。GitHub/AISPEC projectではsemantic changeをcommitだけで完結させず、Issueをsemantic historyの入口、commit/PRをexact change historyの入口として双方向traceを維持する。

## 29. 2026-09-24 追記

AISPECをlogical distributed specification databaseとして明示し、physical fileをshardとして扱うWrite Strategyを追加した。existing recordのUPDATE/DELETEはPATCHを必要回数だけ使用し、新規recordのまとまった追加はshard write threshold以上なら最初からNEW SHARDを第一選択とする。routine full-file replacementは使用しない。後方互換なfield追加、schema migration、意味を変えないAISPEC Hygieneを分離した。
# AI Development SAHOU（作法）

AIと人間が継続的に開発するための、仕様記述・作業管理・記録・変更・検証の共通作法です。

## ねらい

このリポジトリでは、会話の記憶や特定サービスの暗黙仕様に依存せず、別のAI・別のチャット・別の担当者でも作業を再開できる開発運用を整理します。

中心となる考え方は次のとおりです。

- **AISPEC**: 現在の意味を、ファイル位置や章順に依存せず機械的に復元できる仕様記述
- **分散仕様データベース**: 仕様は複数shardへ分散保存でき、SEARCH + specification closureで必要集合を復元する
- **Work Item / Issue**: 議題・判断・成功/失敗を含む履歴の正本
- **Current State / Status**: activeな現在地・focus・blocker・nextの補助盤
- **Adapter**: ChatGPTやGitHub等の製品固有機能を、製品非依存の論理役割へ対応付ける
- **Safe Commit Engine**: 大きな変更をfull-file replacementに頼らず、安全なpatch bundleとして適用する

## 基本フロー

```text
conversation
  -> trackable topic
       -> Status + Work Item
  -> adopted semantic truth
       -> AISPEC / current specification
  -> exact change
       -> versioned repository / commit
  -> validation evidence
       -> CI / tests / Work Item
```

Work Itemは成功時だけ残すものではありません。失敗・却下・中止・保留・no-change・調査のみの場合も、議題として扱った履歴として保持します。

## 構成

### Core
- [AISPEC v1.2](specs/aispec/AISPEC_AI仕様記述共通仕様_v1.2.md)
- [Continuous Conversation Distillation shard](specs/aispec/AISPEC_AI仕様記述共通仕様_v1.2_SHARD_CONTINUOUS_DISTILLATION.md)
- [AI開発基盤抽象化 共通仕様 v1.0](specs/platform/AI開発基盤抽象化共通仕様_v1.0.md)

### Adapters
- [ChatGPT Adapter v1.0](adapters/chatgpt/CHATGPT_ADAPTER_共通仕様_v1.0.md)
- [GitHub Adapter v1.0](adapters/github/GITHUB_ADAPTER_共通仕様_v1.0.md)

### GitHub運用
- [GitHub AI作業運用 共通仕様 v1.15](specs/github/GITHUB_AI作業運用共通仕様_v1.15.md)
- [Conversation-to-Authority Sync](specs/github/GITHUB_AI作業運用共通仕様_v1.15_SHARD_CONVERSATION_SYNC.md)
- [Status + Issue Binding](specs/github/GITHUB_AI作業運用共通仕様_v1.15_SHARD_STATUS_ISSUE_BINDING.md)
- [Issue Outcome Retention](specs/github/GITHUB_AI作業運用共通仕様_v1.15_SHARD_ISSUE_OUTCOME_RETENTION.md)

### Research
- [Research Core v0.1](specs/research-evidence/RESEARCH_CORE_v0.1.md)
- [Research Evidence Core Schema v0.1](specs/research-evidence/RESEARCH_EVIDENCE_CORE_SCHEMA_v0.1.md)
- [Paper Research Schema Plugin v0.1](specs/research-evidence/plugins/PAPER_RESEARCH_SCHEMA_PLUGIN_v0.1.md)
- [Analysis Research Schema Plugin v0.1](specs/research-evidence/plugins/ANALYSIS_RESEARCH_SCHEMA_PLUGIN_v0.1.md)
- [Synthetic Research Stress Test v0.1](specs/research-evidence/examples/RESEARCH_EVIDENCE_SYNTHETIC_STRESS_TEST_v0.1.md)

Researchは文献検索だけを指しません。source research、empirical investigation、data/code/log/visual analytics、evidence evaluation、synthesisを含む上位概念です。AnalyticsはResearch内のACTIVITYとして扱います。

### Safe Commit
- [Safe Commit Engine AISPEC v1.2](specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md)
- [Safe Commit Engine Reference v1.1](specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md)

### 既存セットREADME
- [共通仕様セットREADME](specs/README_共通仕様セット.md)

## 製品非依存とAdapter

Coreでは `Persistent Project Store`、`Versioned Repository`、`Work Item Tracker`、`CI / Validation Runner` などの論理役割を定義します。

具体的な製品を使う場合はAdapterで対応付けます。たとえば、利用可能なChatGPT環境では `Persistent Project Store` を **ChatGPT Library** に、GitHubを使う環境では `Work Item Tracker` を **GitHub Issues** に対応付けます。


## 毎回の開発開始

各projectは、SAHOU全文をproject内へ複製せず、[PROJECT_BOOTSTRAP template](templates/PROJECT_BOOTSTRAP.md) から共通SAHOUを参照します。

標準起動:

```text
PROJECT_BOOTSTRAP
  -> SAHOU main exact SHA確認
  -> 全開発共有のexact-SHA cacheをresolve
     -> HIT: 検証済みrepository snapshotをfull load
     -> MISS: current exact snapshotを再取得・検証・cache更新
  -> project固有spec / Current State / Open Work Item
  -> 開発開始
```

shared cacheはSAHOUのauthorityではありません。authorityはGitHub repositoryのref / exact commit / treeです。

- [SAHOU Shared Cache Contract v1.0](specs/platform/SAHOU_SHARED_CACHE_CONTRACT_v1.0.md)
- [PROJECT_BOOTSTRAP template](templates/PROJECT_BOOTSTRAP.md)
- [snapshot manifest tool](tools/sahou_snapshot_manifest.py)

`SAHOU_FULL.md` のような派生統合fileは作りません。cacheはexact repository snapshotそのものを保持します。

## SAHOU自体の開発

このrepository自体を修正・保守する場合は、利用者向け共通仕様とは別に [SAHOU Development Guide](DEVELOPMENT.md) を使用します。

PR merge前にAI reviewを行い、Issue / PR diff / base側関連仕様 / 周辺文脈を再確認した上で、Actions / CIとあわせて検証します。

## ライセンス

MIT License

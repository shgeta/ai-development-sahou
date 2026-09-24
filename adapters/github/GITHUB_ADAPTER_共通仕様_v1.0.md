# GitHub Adapter 共通仕様 v1.0

- Updated: 2026-09-24
- Status: APPROVED
- Parent model: `AI開発基盤抽象化共通仕様_v1.0.md`
- Scope: GitHub固有機能をlogical platform rolesへmappingするAdapter

## Mapping

| Logical role | GitHub implementation |
|---|---|
| Versioned Repository | GitHub repository / Git repository |
| Work Item Tracker | GitHub Issues |
| Change Review | GitHub Pull Requests |
| Exact Revision Identity | Git commit SHA |
| CI / Validation Runner | GitHub Actions workflows / jobs |
| Remote Execution Runner | GitHub Actions runner |
| Durable Artifact Store | GitHub Actions artifacts / Releases等、project policyで指定した永続・半永続領域 |
| Local Working Copy | local Git checkout / worktree（GitHubそのものではなくGit working copy） |

## Rule

共通仕様では `Work Item Tracker`、`Versioned Repository`、`CI / Validation Runner` 等のlogical roleを定義し、GitHubを使用するprojectでは本AdapterによりGitHub Issues / repository / Actions等へmappingする。

既存の `GITHUB_AI作業運用共通仕様` はGitHub Adapter固有のoperational specificationとして扱い、製品非依存なcore conceptそのものとは区別する。

GitHubを使用しないprojectでは、同等のlogical roleを持つ別Adapterを使用してよい。
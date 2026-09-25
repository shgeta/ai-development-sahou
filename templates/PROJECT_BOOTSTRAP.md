# PROJECT BOOTSTRAP template

このprojectでAI開発を開始・再開する時の固定入口。

## Common SAHOU

- Repository: `shgeta/ai-development-sahou`
- Ref: `main`
- Load mode: `routed`
- Routing index: `specs/README_共通仕様セット.md`
- Cache mode: `shared exact-SHA snapshot`
- Shared cache role: read optimization only
- Authority: GitHub repository ref / exact commit / tree

### Startup rule

1. `shgeta/ai-development-sahou` のtarget refからexact commit SHAを確認する。
2. shared cacheの同一SHA snapshotをresolveし、integrityを確認する。miss時だけexact repository snapshotを取得・更新する。
3. routing indexを読む。
4. このBootstrap、project固有authority、Current State、Open Work Item、actual taskを確認する。
5. Required SAHOU modulesをloadする。
6. task triggerに一致するConditional modulesだけをloadする。
7. selected moduleの明示dependency closureだけを追加loadする。
8. cache snapshot全体をconversation contextへ展開しない。
9. 作業中に新しいtriggerが発生した時だけ追加moduleをloadする。
10. `SAHOU_FULL.md` 等の派生full bundleをauthorityとして使用しない。

## SAHOU modules

### Required for GitHub work

- `specs/github/GITHUB_AI作業運用共通仕様_v1.16.md`

### Conditional

projectで使うものだけ残す / 追加する。

- AISPEC semantic work:
  - `specs/aispec/AISPEC_AI仕様記述共通仕様_v1.2.md`
- durable log:
  - `specs/log/LOG_CORE_v1.0.md`
- production Web update log:
  - `specs/log/LOG_CORE_v1.0.md`
  - `specs/web/WEB_UPDATE_LOG_PLUGIN_v1.0.md`
- Safe Commit trigger:
  - `specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md`
  - 実操作時のみ `specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md`
- Research:
  - Research Core + taskに必要なpluginのみ
- Product adapter:
  - product固有mappingが必要な時だけ対応Adapter

## Project identity

- Repository: `<owner>/<repo>`
- Default branch: `<branch>`
- Project spec: `<path or reference>`
- Current State: `<persistent-store reference>`
- Work Item Tracker: `<tracker reference>`

## Durable log

durable logを使うprojectだけ記載する。対象外なら `N/A`。

- Log Core: `specs/log/LOG_CORE_v1.0.md` or `N/A`
- Plugin: `<plugin path or N/A>`
- Canonical log: `<path/store reference or N/A>`
- Format / schema: `<format and version or N/A>`
- Writer: `<workflow/tool/store append mechanism or N/A>`
- Concurrency control: `<serialization/atomic append/create-only/HEAD guard or N/A>`
- Logging failure recovery: `<procedure or N/A>`

## Project-specific guardrails

- <project固有rule>

## Validation entrypoints

- Build: `<command>`
- Test: `<command>`
- Other QA: `<reference>`

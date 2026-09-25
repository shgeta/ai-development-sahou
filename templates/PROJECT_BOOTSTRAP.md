# PROJECT BOOTSTRAP template

このprojectでAI開発を開始・再開する時の固定入口。

## Common SAHOU

- Repository: `shgeta/ai-development-sahou`
- Ref: `main`
- Load mode: `full`
- Cache mode: `shared exact-SHA`
- Shared cache role: read optimization only
- Authority: GitHub repository ref / exact commit / tree

### Startup rule

1. `shgeta/ai-development-sahou` の `main` exact commit SHAを確認する。
2. shared cacheに同一SHAの検証済みexact repository snapshotがあるか確認する。
3. cache hitならsnapshotをfull loadする。GitHub本文を再取得しない。
4. cache miss / SHA変更 / integrity不明なら、current exact SHAのrepository snapshotを再取得・検証し、shared cacheを更新してからfull loadする。
5. `SAHOU_FULL.md` 等の派生統合fileを代替authorityとして使用しない。
6. SAHOUを読み込んだ後、このproject固有のauthority / Current State / Open Work Itemへ進む。

## Project identity

- Repository: `<owner>/<repo>`
- Default branch: `<branch>`
- Project spec: `<path or reference>`
- Current State: `<persistent-store reference>`
- Work Item Tracker: `<tracker reference>`

## Production Web update log

production Web siteを変更するprojectでは記載する。対象外なら `N/A` と明示する。

- Common authority: `specs/web/WEB_SITE_UPDATE_LOG_共通仕様_v1.0.md` or `N/A`
- Canonical log: `<path/store reference or N/A>`
- Format / schema: `<format and version or N/A>`
- Writer: `<workflow/tool/store append mechanism or N/A>`
- Concurrency control: `<serialization/atomic append/HEAD guard or N/A>`
- Logging failure recovery: `<procedure or N/A>`

## Project-specific guardrails

- <project固有rule>

## Validation entrypoints

- Build: `<command>`
- Test: `<command>`
- Other QA: `<reference>`

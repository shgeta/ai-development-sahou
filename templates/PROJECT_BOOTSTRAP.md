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
4. このBootstrapからProject Localの有無とcurrent locationをresolveし、存在する場合はそのindex / applicable override / required Adapter referenceだけを読む。
5. project固有authority、Current State、Open Work Item、actual taskを確認する。
6. Required SAHOU modulesをloadする。
7. task triggerに一致するConditional modulesだけをloadする。
8. selected moduleの明示dependency closureだけを追加loadする。
9. cache snapshot全体やProject Local全体をconversation contextへ展開しない。
10. 作業中に新しいtriggerが発生した時だけ追加moduleをloadする。
11. `SAHOU_FULL.md` 等の派生full bundleをauthorityとして使用しない。

## SAHOU Project Local

Project Localを使わないprojectは `N/A` とする。

- Project Local: `<path or persistent reference or N/A>`
- Project Local mode: `embedded | sidecar | N/A`
- Project Local index: `<reference or N/A>`
- Task Staging Adapter: `<adapter reference or N/A>`
- Task Staging Certification: `<certification reference or N/A>`

Project Localの `Local` はmachine-local temporary workspaceを意味しない。Common override、project固有AISPEC、environment-specific Adapter、certification等のproject-scoped layerとして扱う。

Task Staging Adapterを使用する場合、runtimeはvalid certificationを確認してから使用し、各taskごとにstoreを再選定しない。certificationがexpired / invalid、またはproduction writeが失敗した場合は再検証へ送る。

## SAHOU modules

### Required for GitHub work

- `specs/github/GITHUB_AI作業運用共通仕様_v1.16.md`

### Conditional

projectで使うものだけ残す / 追加する。

- AISPEC semantic work:
  - `specs/aispec/AISPEC_AI仕様記述共通仕様_v1.2.md`
- Project Local:
  - `specs/platform/SAHOU_PROJECT_LOCAL_AISPEC_v1.0.md`
- scheduled / unattended task staging:
  - `specs/platform/TASK_STAGING_STORE_AISPEC_v1.0.md`
  - `specs/platform/SAHOU_PROJECT_LOCAL_AISPEC_v1.0.md`
  - projectのcertified Task Staging Adapter
- durable log:
  - `specs/log/LOG_CORE_v1.0.md`
- production Web update log:
  - `specs/log/LOG_CORE_v1.0.md`
  - `specs/web/WEB_UPDATE_LOG_PLUGIN_v1.0.md`
- Safe Commit trigger:
  - `specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_AISPEC_v1.2.md`
  - 実操作時のみ `specs/safe-commit/GITHUB_SAFE_COMMIT_ENGINE_REFERENCE_v1.1.md`
- Research:
  - `specs/research-evidence/RESEARCH_CORE_v0.1.md`
  - `specs/research-evidence/RESEARCH_EVIDENCE_CORE_SCHEMA_v0.1.md`
  - taskに必要なpluginのみ
- Chemical research:
  - `specs/research-evidence/plugins/chemical/CHEMICAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md`
- Raw-material research:
  - `specs/research-evidence/plugins/chemical/RAW_MATERIAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md`
  - parent dependencyとして Chemical Research Plugin もloadする
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

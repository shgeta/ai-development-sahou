# WEB SITE UPDATE LOG 共通仕様 v1.0

- Status: DEPRECATED
- Deprecated: 2026-09-25
- Historical decision: Issue #20
- Replacement decision: Issue #22

このfileはIssue #20時点の統合仕様を指すlegacy entrypointである。

current authorityは次へ分離された。

1. domain非依存のログ作法:
   - `specs/log/LOG_CORE_v1.0.md`
2. production Web update固有作法:
   - `specs/web/WEB_UPDATE_LOG_PLUGIN_v1.0.md`

新規sessionではこのlegacy fileを通常loadしない。
過去Issue / commitの解釈が必要な場合のみhistory referenceとして使用する。

旧仕様のappend-only、event identity、correction、UTC、machine-readable authority、secret exclusion、concurrency、persistence reporting等はLog Coreへ移動した。
deployment_id、site/target/source、REQUESTED/STARTED/SUCCEEDED/FAILED、rollback、validation等はWeb Update Log Pluginへ移動した。

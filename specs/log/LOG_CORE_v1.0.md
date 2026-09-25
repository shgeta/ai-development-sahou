# LOG CORE v1.0

- Updated: 2026-09-25
- Status: APPROVED
- Scope: domain / provider非依存のdurable event log共通作法
- Relation: domain plugin / project-specific log implementationから参照するCore
- Decision: Issue #22

## 0. Purpose

Log Coreは「何をログにするか」をdomainごとに決めない。

各domainがdurable logを必要とするときに、記録の壊れにくさ・訂正可能性・追跡可能性だけを共通化する。

domain固有のevent type、必須field、成功条件、対象identityはpluginまたはproject authorityが定義する。

## 1. Core rules

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | TARGET | WHEN | UNLESS | DEPENDS_ON | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| LOG.CORE.010 | Durable log has a canonical entrypoint | REQUIREMENT | durable logを採用するprojectはcanonical log location / storeへ固定入口から到達可能にする | project log | bootstrap / project authority | durable history is required | なし |  | APPROVED |
| LOG.CORE.020 | Append-only history | SAFETY | 過去eventを通常運用で削除・上書き・並べ替え・意味変更せず、新しい事実は新eventとして追加する | persistence | canonical event stream | event persistence | explicit migration with migration record | LOG.CORE.010 | APPROVED |
| LOG.CORE.030 | Stable event identity | REQUIREMENT | 各eventはimmutableなevent_idを持つ | event identity | each event | event creation | なし | LOG.CORE.020 | APPROVED |
| LOG.CORE.040 | Stable stream identity | REQUIREMENT | 関連eventを束ねるlogical streamにはstable stream_idまたは同等identityを持たせる | grouping | event stream | multiple events describe one logical operation/object | single isolated event only | LOG.CORE.020 | APPROVED |
| LOG.CORE.050 | Event vocabulary is explicit | REQUIREMENT | event_typeはplugin/project authorityで定義し、同一streamの状態変化をrecord上書きで表現しない | semantics | event_type | lifecycle/history is logged | なし | LOG.CORE.020 | APPROVED |
| LOG.CORE.060 | Correction is a new event | SAFETY | 誤記訂正は元eventを残し、correction eventから元eventへ参照する | correction | canonical event stream | recorded fact is wrong | なし | LOG.CORE.020,LOG.CORE.030 | APPROVED |
| LOG.CORE.070 | UTC occurrence time | REQUIREMENT | occurred_at_utcをoffset-aware ISO 8601 UTCで保持する | temporal ordering | each event | event creation | なし | LOG.CORE.030 | APPROVED |
| LOG.CORE.080 | Machine-readable authority | REQUIREMENT | canonical logはfieldを失わないmachine-readable形式または同等structured storeとする | storage | canonical log | durable log | なし | LOG.CORE.020 | APPROVED |
| LOG.CORE.090 | Human view is derived | POLICY | Markdown summary等のhuman-readable viewはcanonical structured logから導出できるがauthorityを置き換えない | presentation | derived view | human view exists | structured store itself is human-readable | LOG.CORE.080 | APPROVED |
| LOG.CORE.100 | Traceability refs | REQUIREMENT | eventから原因・実行・evidenceへ辿るため、plugin/projectが定義するreference fieldを保持する | provenance | refs / evidence | external source exists | external source truly has no identity | LOG.CORE.030 | APPROVED |
| LOG.CORE.110 | Secret exclusion | SAFETY | API key、token、password、cookie、private credential等をlogへ保存しない | security | all log fields | always | なし |  | APPROVED |
| LOG.CORE.120 | Concurrency-safe persistence | SAFETY | 同時書込みでlost updateが起きないようatomic append、create-only event、serialization、HEAD guard等を使う | persistence transaction | writer | concurrent writers are possible | store provides equivalent atomic semantics | LOG.CORE.020 | APPROVED |
| LOG.CORE.130 | Operation outcome and logging outcome are distinct | SAFETY | 実処理の成功/失敗とlog persistenceの成功/失敗を別事象として扱い、logging failureで実処理結果を偽装しない | incident handling | operation + log writer | both operation and logging exist | なし | LOG.CORE.010 | APPROVED |
| LOG.CORE.140 | Do not claim persisted before verification | SAFETY | canonical storeへの永続化を確認していない状態で「記録済み」「保存済み」と表現しない | reporting | AI / human report | persistence claim | なし | LOG.CORE.010 | APPROVED |
| LOG.CORE.150 | Plugin may extend, not weaken | REQUIREMENT | pluginはfield/event/ruleを追加できるがCoreのappend-only / correction / secret / persistence safetyを弱めない | extension | plugin | plugin adoption | explicit stronger project rule | LOG.CORE.020 | APPROVED |

## 2. Minimum semantic fields

物理field名はprojectごとに変えてよいが、最低限次の意味を保持する。

| Meaning | Requirement |
|---|---|
| schema revision | required |
| event identity | required |
| logical stream identity | required when events are grouped |
| event type | required |
| occurred-at UTC | required |
| subject / object reference | required when an external subject exists |
| summary / fact | required |
| provenance / work refs | required when source identities exist |
| evidence refs | conditional |
| outcome detail | conditional |
| correction-of event reference | correction only |

## 3. Plugin contract

Pluginは少なくとも次を定義する。

- domain scope
- Core dependency
- stream identityのdomain名
- event vocabulary
- domain-required fields
- persistence timing / gates
- success / failure semantics
- validation / evidence semantics
- project Bootstrapに必要な追加entrypoint

Log Core自身には個別domain / provider固有の語彙・event・fieldを入れない。

## 4. Load rule

Log Coreはログを扱う作業でのみloadする。

domain pluginを使う場合:

```text
routing index
  -> LOG_CORE
  -> selected log plugin
  -> project-specific log authority
```

ログを扱わない作業ではLog Coreをloadする必要はない。

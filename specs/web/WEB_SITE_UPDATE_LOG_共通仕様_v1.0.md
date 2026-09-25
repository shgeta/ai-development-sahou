# WEB SITE UPDATE LOG 共通仕様 v1.0

- Updated: 2026-09-25
- Status: PROPOSED
- Scope: production Web siteへの変更・反映・rollback・訂正を、AI/人間が再現可能に追跡するための共通運用
- Relation: AISPEC / GitHub AI作業運用 / deployment automation projectから参照する共通仕様

## 0. Purpose

Webサイトの本番状態を変更するoperationについて、Issue / PR / commit / CI / hosting provider operationが別々に存在しても、後から一つのcanonical log entrypointから次を追跡できる状態を作る。

- 何を反映しようとしたか
- どのsource revisionを使ったか
- どのproduction targetへ反映したか
- どのdeployment mechanismを使ったか
- 実際にoperationが開始されたか
- 成功 / 失敗 / 中止 / rollbackのどれだったか
- どのvalidation evidenceで結果を確認したか
- 後から訂正された場合、元記録と訂正記録の両方

read-only preflight / inspectionは、それ自体ではproduction Web site updateではない。production updateのevidenceとして参照してよい。

## 1. Core rules

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | TARGET | WHEN | UNLESS | DEPENDS_ON | STATUS | SOURCE | DECISION_REF |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WEB.UPDATE.LOG.010 | Production update requires durable log | REQUIREMENT | production Web siteの状態を変更するoperationはcanonical Web Update Logから追跡可能にする | production web operation | project canonical update log | production state may change | read-only inspection only |  | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.020 | Bootstrap must expose log entrypoint | REQUIREMENT | projectはPROJECT_BOOTSTRAP等の固定入口からcanonical log location / writer / schemaへ到達可能にする | project restartability | project bootstrap | Web Update Logを採用 | なし | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.030 | Append-only event stream | SAFETY | 過去eventを削除・上書き・並べ替え・意味変更せず、新しい事実は新eventとして末尾追加する | log persistence | canonical event stream | record追加・訂正 | storage migration with explicit migration record | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.040 | Deployment and event identities | REQUIREMENT | 1つの論理deploymentへstable deployment_idを与え、各追記recordへunique event_idを与える | event identity | each deployment / event | event作成 | なし | WEB.UPDATE.LOG.030 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.050 | Lifecycle is event-sourced | REQUIREMENT | REQUESTED / STARTED / SUCCEEDED / FAILED / CANCELLED / ROLLED_BACK / CORRECTION等を同一recordのstatus上書きではなく別eventとして残す | deployment lifecycle | canonical event stream | lifecycle transition | なし | WEB.UPDATE.LOG.030,WEB.UPDATE.LOG.040 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.060 | Exact source revision | REQUIREMENT | 本番へ反映したsourceはbranch名だけでなくexact commit SHA / immutable artifact digest等で識別する | provenance | source_revision | deployment attempts code/artifact update | provider-native state with no source artifact; then record explicit source description | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.070 | Stable target identity | REQUIREMENT | site_refとtarget_environmentを記録し、URL表示名だけへ依存しないstable project-local identityを優先する | target provenance | site / production target | production operation | なし | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.080 | Change intent traceability | REQUIREMENT | eventからWork Item / Issue / PR / change request等の変更理由へ到達可能にする | semantic traceability | work_item_ref / change_ref | tracked change exists | emergency operation; then create retrospective work item promptly | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.090 | Execution traceability | REQUIREMENT | deployment mechanism、CI/run reference、provider operation referenceを利用可能な範囲で記録する | execution traceability | run_ref / operation_ref | automated or provider-backed deployment | provider returns no operation identity | WEB.UPDATE.LOG.010 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.100 | Validation evidence | REQUIREMENT | successはdeployment APIのacceptだけで確定せず、利用可能なpost-deploy validation evidenceを参照する | validation | validation_refs | success claimed | validation not applicable; reason must be explicit | WEB.UPDATE.LOG.090 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.110 | Failure and cancellation retention | REQUIREMENT | failed / rejected / cancelled / timed-out attemptも削除せずlogへ残す | negative outcomes | canonical event stream | deployment was requested or started | read-only dry-run that was never a deployment request | WEB.UPDATE.LOG.050 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.120 | Rollback is a new deployment | REQUIREMENT | rollbackは元eventの取消ではなく別deploymentとして記録し rollback_of_deployment_id で元deploymentへ参照する | rollback | rollback event stream | rollback executed | なし | WEB.UPDATE.LOG.040,WEB.UPDATE.LOG.050 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.130 | Corrections never rewrite history | SAFETY | 誤記訂正は元eventを保持し、CORRECTION eventで correction_of_event_id と corrected fields / reasonを記録する | correction | canonical event stream | recorded fact is wrong | なし | WEB.UPDATE.LOG.030,WEB.UPDATE.LOG.040 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.140 | Secret exclusion | SAFETY | API key、token、password、session cookie、private credentialをupdate logへ保存しない | security | all log fields | always | なし |  | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.150 | UTC event time | REQUIREMENT | occurred_at_utcをoffset-aware ISO 8601 UTCで記録する。local display timeは追加してよいがauthorityにしない | temporal ordering | each event | event creation | なし | WEB.UPDATE.LOG.040 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.160 | Machine-readable authority | REQUIREMENT | canonical event streamはJSONL/NDJSON等のmachine-readable形式または同等にfield-preservingなstoreとする | storage model | canonical log | automated logging | project-specific store offers equivalent structured records | WEB.UPDATE.LOG.030 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.170 | Human view is derived | POLICY | Markdown summaryやrelease note等のhuman-readable viewはcanonical event streamから導出してよく、event authorityを置き換えない | presentation | human summary | summary exists | なし | WEB.UPDATE.LOG.160 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.180 | Record write must be concurrency-safe | SAFETY | repository logへ追記するwriterはserial executionまたはHEAD guard/retry等で同時追記のlost updateを防ぐ | persistence transaction | log writer | multiple operations may write | storage provides atomic append | WEB.UPDATE.LOG.030 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.190 | Deployment success and logging success are distinct | SAFETY | production deployment成功後にcanonical log追記が失敗した場合、deployment成功を隠さず「deployment succeeded / logging incomplete」と扱い、追跡Issueを作る | incident handling | operator report / work item | log persistence fails after production mutation | なし | WEB.UPDATE.LOG.010,WEB.UPDATE.LOG.030 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.200 | Do not claim recorded when not persisted | SAFETY | canonical storeへの永続化を確認していない場合「更新ログへ保存済み」「記録済み」と表現しない | reporting | human/AI response | claiming persistence | なし | WEB.UPDATE.LOG.030 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.210 | Request record may precede live mutation | POLICY | immutable deployment requestまたはREQUESTED eventをproduction mutation前に残してよい。結果は後続eventで確定する | planned deployment | request/log | deployment is planned | なし | WEB.UPDATE.LOG.050 | APPROVED | Issue #20 design | #20 |
| WEB.UPDATE.LOG.220 | Common spec stays provider-neutral | REQUIREMENT | Kinsta、Cloudflare、SSH、GitHub Pages等provider固有fieldはproject adapterへ置き、common schemaはdeployment mechanismを抽象的に記録する | common specification | schema / examples | always | public provider reference used as documentation only |  | APPROVED | Issue #20 design | #20 |

## 2. Canonical event fields

Project固有storeは少なくとも次の意味を保持する。物理field名を変える場合でもsemantic mappingを明示する。

| Field | Required | Meaning |
|---|---:|---|
| schema_version | yes | record schema revision |
| event_id | yes | immutable unique event identity |
| deployment_id | yes | one logical deployment / rollback operation identity |
| event_type | yes | REQUESTED / STARTED / SUCCEEDED / FAILED / CANCELLED / ROLLED_BACK / CORRECTION 等 |
| occurred_at_utc | yes | event occurrence time in UTC ISO 8601 |
| site_ref | yes | project-local stable site identity |
| target_environment | yes | production target identity such as live / production |
| change_summary | yes | short description of intended or observed change |
| source_revision | conditional | exact commit SHA / artifact digest / provider-native source description |
| work_item_ref | recommended | Issue / Work Item / ticket |
| change_ref | recommended | PR / change request / release ref |
| deployment_mechanism | yes | CI workflow / provider API / SSH / console etc. |
| run_ref | conditional | CI / automation run identity |
| provider_operation_ref | conditional | hosting/deployment provider operation identity |
| validation_refs | conditional | smoke test / visual QA / health check / CI evidence |
| outcome_detail | conditional | failure reason / cancellation reason / validation summary |
| rollback_of_deployment_id | rollback only | deployment being rolled back |
| correction_of_event_id | correction only | event being corrected |
| correction_reason | correction only | why correction is appended |

Optional extra fields are allowed if they do not weaken the required semantics or expose secrets.

## 3. Event ordering

Typical successful deployment:

```text
REQUESTED
  -> PREFLIGHT evidence (may live outside the update log)
  -> STARTED
  -> SUCCEEDED
```

Typical failure:

```text
REQUESTED
  -> STARTED
  -> FAILED
```

Provider rejection before mutation may be:

```text
REQUESTED
  -> FAILED
```

Rollback:

```text
deployment A: ... -> SUCCEEDED
deployment B: REQUESTED -> STARTED -> ROLLED_BACK
              rollback_of_deployment_id = A
```

Correction:

```text
event X remains unchanged
CORRECTION event Y -> correction_of_event_id = X
```

## 4. Synthetic JSONL example

The following identifiers are synthetic.

```jsonl
{"schema_version":1,"event_id":"evt_demo_001","deployment_id":"dep_demo_001","event_type":"REQUESTED","occurred_at_utc":"2030-01-01T00:00:00Z","site_ref":"example-site","target_environment":"production","change_summary":"Publish approved header change","source_revision":"abcdef1234567890","work_item_ref":"issue://example-org/example-repo/123","change_ref":"pr://example-org/example-repo/456","deployment_mechanism":"ci-provider-api"}
{"schema_version":1,"event_id":"evt_demo_002","deployment_id":"dep_demo_001","event_type":"STARTED","occurred_at_utc":"2030-01-01T00:01:00Z","site_ref":"example-site","target_environment":"production","change_summary":"Publish approved header change","source_revision":"abcdef1234567890","deployment_mechanism":"ci-provider-api","run_ref":"ci://example-org/example-repo/run/789","provider_operation_ref":"provider-op-demo-001"}
{"schema_version":1,"event_id":"evt_demo_003","deployment_id":"dep_demo_001","event_type":"SUCCEEDED","occurred_at_utc":"2030-01-01T00:03:00Z","site_ref":"example-site","target_environment":"production","change_summary":"Publish approved header change","source_revision":"abcdef1234567890","deployment_mechanism":"ci-provider-api","run_ref":"ci://example-org/example-repo/run/789","provider_operation_ref":"provider-op-demo-001","validation_refs":["qa://smoke/example-001"],"outcome_detail":"Provider operation and post-deploy validation succeeded"}
```

## 5. Project integration

Web Update Logを使うprojectはPROJECT_BOOTSTRAPから少なくとも次へ到達できるようにする。

- Common authority: this specification
- Canonical log location
- Physical format / schema version
- Writer / append mechanism
- Concurrency control
- Human-readable view if any
- Recovery procedure when deployment succeeds but logging fails

Project固有のdeployment request、provider API、site name、actual URL、operation ID等はproject repository / project logへ置き、common SAHOUへコピーしない。

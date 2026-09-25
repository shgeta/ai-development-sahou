# WEB UPDATE LOG PLUGIN v1.0

- Updated: 2026-09-25
- Status: APPROVED
- Scope: production Web siteへの変更・反映・rollbackのdurable history
- Parent Core: `specs/log/LOG_CORE_v1.0.md`
- Decision: Issue #22
- Supersedes: `WEB_SITE_UPDATE_LOG_共通仕様_v1.0.md`

## 0. Purpose

production Web siteの状態を変更するoperationについて、Issue / PR / commit / CI / hosting provider operationが分散していても、canonical Web Update Logから一つのdeployment履歴として追跡できるようにする。

read-only preflight / inspectionはproduction mutationではないため、それ自体をWeb Update Logへ記録する必要はない。後続deploymentのevidenceとして参照してよい。

## 1. Core mapping

- Log Core `stream_id` -> `deployment_id`
- Log Core subject -> `site_ref`
- Canonical event identity -> `event_id`
- Web domain event vocabulary -> REQUESTED / STARTED / SUCCEEDED / FAILED / CANCELLED / ROLLED_BACK / CORRECTION

## 2. Web rules

| RULE_ID | TITLE | TYPE | MEANING | DEPENDS_ON | STATUS |
|---|---|---|---|---|---|
| WEB.UPDATE.LOG.010 | Production mutation requires durable log | REQUIREMENT | production Web siteの状態を変更するoperationはcanonical Web Update Logから追跡可能にする | LOG.CORE.010 | APPROVED |
| WEB.UPDATE.LOG.020 | Bootstrap exposes Web log | REQUIREMENT | project BootstrapからLog Core / Web Plugin / canonical log / writer / recoveryへ到達可能にする | LOG.CORE.010 | APPROVED |
| WEB.UPDATE.LOG.030 | Deployment lifecycle is event-sourced | REQUIREMENT | REQUESTED / STARTED / SUCCEEDED / FAILED等を別eventとして残す | LOG.CORE.020,LOG.CORE.050 | APPROVED |
| WEB.UPDATE.LOG.040 | Exact source revision | REQUIREMENT | sourceをbranch名だけでなくexact commit SHA / artifact digest / provider-native immutable description等で識別する | LOG.CORE.100 | APPROVED |
| WEB.UPDATE.LOG.050 | Stable target identity | REQUIREMENT | site_refとtarget_environmentを記録し、表示URLだけへ依存しない | LOG.CORE.100 | APPROVED |
| WEB.UPDATE.LOG.060 | Change intent traceability | REQUIREMENT | Work Item / Issue / PR / change request等の変更理由へ到達可能にする | LOG.CORE.100 | APPROVED |
| WEB.UPDATE.LOG.070 | Execution traceability | REQUIREMENT | CI/run reference、deployment mechanism、provider operation referenceを利用可能な範囲で記録する | LOG.CORE.100 | APPROVED |
| WEB.UPDATE.LOG.080 | Validation evidence | REQUIREMENT | SUCCEEDEDはprovider acceptだけで確定せず、利用可能なpost-deploy validation evidenceを参照する | LOG.CORE.100 | APPROVED |
| WEB.UPDATE.LOG.090 | Failed/cancelled attempts remain | REQUIREMENT | failed / rejected / cancelled / timed-out attemptも削除せず残す | LOG.CORE.020 | APPROVED |
| WEB.UPDATE.LOG.100 | Rollback is a new deployment stream | REQUIREMENT | rollbackは元event取消ではなく新deploymentとして記録しrollback_of_deployment_idで元へ参照する | LOG.CORE.040 | APPROVED |
| WEB.UPDATE.LOG.110 | Request may precede mutation | POLICY | REQUESTED eventまたはimmutable deployment requestをproduction mutation前に永続化してよい | WEB.UPDATE.LOG.030 | APPROVED |
| WEB.UPDATE.LOG.120 | Logging failure after mutation is explicit | SAFETY | production mutation開始後のlogging failureはdeployment結果と分離し、logging incompleteとしてdurable trackingを要求する | LOG.CORE.130 | APPROVED |

## 3. Required Web fields

Log Core fieldsに加えて次を保持する。

| Field | Requirement |
|---|---|
| deployment_id | required |
| site_ref | required |
| target_environment | required |
| change_summary | required |
| source_revision | conditional but normally required |
| work_item_ref | recommended |
| change_ref | recommended |
| deployment_mechanism | required |
| run_ref | conditional |
| provider_operation_ref | conditional |
| validation_refs | required when success validation exists |
| outcome_detail | conditional |
| rollback_of_deployment_id | rollback only |

## 4. Typical event ordering

```text
REQUESTED
  -> STARTED
  -> SUCCEEDED
```

Failure:

```text
REQUESTED
  -> STARTED
  -> FAILED
```

Provider rejection before operation start:

```text
REQUESTED
  -> FAILED
```

Rollback:

```text
deployment A -> SUCCEEDED
deployment B -> REQUESTED -> STARTED -> ROLLED_BACK
                rollback_of_deployment_id = A
```

## 5. Project integration

Web Update Logを採用するprojectはBootstrapから次へ到達できるようにする。

- `LOG_CORE_v1.0.md`
- this plugin
- canonical project log location
- physical format / schema
- writer / append mechanism
- concurrency control
- post-deploy validation entrypoint
- recovery procedure when production mutation succeeds but logging fails

provider固有fieldや実site identityはproject側に置く。

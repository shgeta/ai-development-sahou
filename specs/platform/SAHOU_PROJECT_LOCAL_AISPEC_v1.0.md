# SAHOU Project Local AISPEC v1.0

- Updated: 2026-10-06
- Status: APPROVED
- Scope: SAHOU Commonへproject / environment固有の追加・override・Adapter・certification・configを重ねるproject-scoped layer
- Relation: SAHOU Common / Task Staging Store AISPEC / PROJECT_BOOTSTRAP
- Decision: shgeta/ai-development-sahou#28

## 1. Definition

`SAHOU Project Local` は、SAHOU Commonを対象project / environmentへ適用するためのproject-scoped layerである。

`Local` はmachine-localやtemporary filesystemを意味しない。repository内、Persistent Project Store、sidecar workspace等のいずれに存在してもよい。

## 1.1 Semantic rules

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | WHEN | UNLESS | TARGET | STATUS | DECISION_REF |
|---|---|---|---|---|---|---|---|---|---|
| `PLATFORM.PROJECT_LOCAL.010` | Project-scoped layer | REQUIREMENT | Project LocalはSAHOU Commonへproject / environment固有の差分を重ねるlayerであり、machine-local temporary workspaceとは区別する | project using SAHOU | Project Localを使用するとき | - | Project Local | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.020` | Explicit override | REQUIREMENT | Commonをoverrideする場合はoverride対象・理由・scopeを追跡可能にし、暗黙上書きを行わない | Project Local overrides | Commonと異なるruleを適用するとき | - | override record | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.030` | Embedded or sidecar | RULE | Project Localはrepository内embeddedでもsidecarでもよく、物理pathではなくPROJECT_BOOTSTRAPからcurrent locationを解決する | Project Local placement | locationを決めるとき | - | Project Local location | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.040` | Compatibility first | RULE | 既存状態を安全に利用できる場合はmigrationを要求せず、必要時だけadditive adaptation、targeted migration、full migrationの順で最小侵襲を優先する | existing projects / repositories | current SAHOUを適用するとき | - | compatibility action | APPROVED | `shgeta/ai-development-sahou#28` |


## 2. Allowed contents

Project Localには次を保持してよい。

- Common ruleの明示override
- project固有AISPEC / rule
- environment-specific Adapter
- Adapter certification / test history
- project固有config / stateへのreference
- compatibility / migration instructions

Project Localはcanonical application source codeの置き場である必要はなく、SAHOU適用上のproject固有差分を保持するlayerである。

## 3. Authority and override

SAHOU CommonとProject Localが同一事項を扱い、project固有overrideが必要な場合は黙って上書きしない。

最低限、override対象と理由を追跡可能にする。

```text
override_of: <Common RULE_ID or authority reference>
reason: <project-specific reason>
scope: <affected scope>
```

Commonの安全条件をoverrideする場合は、project側の明示authority / decision recordを必要とする。

## 4. Placement

自分たちで管理するrepositoryでは、推奨embedded locationを次とする。

```text
<repo>/.sahou/project-local/
```

third-party repository、read-only repository、またはrepositoryをSAHOU管理fileで変更したくない場合はsidecar locationを使用してよい。

```text
<sidecar-root>/<stable-project-identity>/project-local/
```

物理path自体を意味上のauthorityにせず、PROJECT_BOOTSTRAPからcurrent locationへ到達可能にする。

## 5. Suggested layout

```text
project-local/
├─ README.md or index
├─ aispec/
├─ adapters/
│  └─ task-staging/
├─ migration/
└─ state/
```

必要のないdirectoryを空で作る必要はない。

## 6. Compatibility-first rule

既存repositoryへSAHOUを適用するとき、migrationを目的化しない。

優先順位:

```text
1. no migration / use as-is
2. additive Project Local adaptation
3. minimal targeted migration
4. full migration
```

current SAHOUが既存状態を安全に扱える場合は、その状態を保持してよい。

migrationが必要な場合のみ、observed stateからcurrent expected stateへの最小侵襲な移行を選ぶ。

## 7. Migration instructions

`migration/` は「必ず実行するversion upgrade script置き場」ではない。

次のような場合にだけmigration AISPEC / instructionを置いてよい。

- Common変更によりProject Local互換性が失われた
- Adapter contract変更により既存Adapterをそのまま使用できない
- schema変更によりruntimeが安全に解釈できない
- userが明示的な構造移行を採用した

migration instructionは可能ならfrom-version固定ではなく、observed state / precondition / target invariantを記述する。

## 8. Bootstrap requirement

Project Localを使用するprojectは、PROJECT_BOOTSTRAPへ少なくとも次を記載する。

```text
Project Local: <path or persistent reference>
Project Local mode: embedded | sidecar
Project Local index: <reference or N/A>
```

Task Staging Adapterを使用する場合は、Adapterとcertificationへのreferenceも記載する。

## 9. Validation

- Project Localをmachine-local temporary stateと同一視していない
- target repositoryへ不要な管理fileを強制していない
- explicit override以外でCommon ruleを黙って変更していない
- migrationなしで安全に利用できる状態を不必要に移行していない
- Adapter / certificationが再発見可能である
- PROJECT_BOOTSTRAPからcurrent Project Localへ到達できる

# SAHOU Project Local AISPEC v1.1

- Updated: 2026-10-06
- Status: APPROVED
- Scope: SAHOU Commonへproject / environment固有の追加・override・Adapter・certification・configを重ねるproject-scoped layer
- Relation: SAHOU Common / Task Staging Store AISPEC / PROJECT_BOOTSTRAP
- Supersedes: `SAHOU Project Local AISPEC v1.0`
- Decision: shgeta/ai-development-sahou#30

## 1. Definition

`SAHOU Project Local` は、SAHOU Commonを対象project / environmentへ適用するためのproject-scoped layerである。

`Local` はmachine-localやtemporary filesystemを意味しない。repository内、Persistent Project Store、sidecar workspace等のいずれに存在してもよい。

## 1.1 Semantic rules

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | WHEN | UNLESS | TARGET | STATUS | DECISION_REF |
|---|---|---|---|---|---|---|---|---|---|
| `PLATFORM.PROJECT_LOCAL.010` | Project-scoped layer | REQUIREMENT | Project LocalはSAHOU Commonへproject / environment固有の差分を重ねるlayerであり、machine-local temporary workspaceとは区別する | project using SAHOU | Project Localを使用するとき | - | Project Local | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.020` | Explicit override | REQUIREMENT | Commonをoverrideする場合はoverride対象・理由・scopeを追跡可能にし、暗黙上書きを行わない | Project Local overrides | Commonと異なるruleを適用するとき | - | override record | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.030` | Embedded or sidecar | RULE | Project Localはrepository内embeddedでもsidecarでもよく、物理pathではなくPROJECT_BOOTSTRAPからcurrent locationを解決する | Project Local placement | locationを決めるとき | - | Project Local location | APPROVED | `shgeta/ai-development-sahou#28` |
| `PLATFORM.PROJECT_LOCAL.040` | Compatibility choice | RULE | 既存repositoryへcurrent SAHOUを適用する際はmigration回避自体を目的にせず、migration cost / Project Local adaptation cost / riskを比較し、最も単純・安全・保守しやすい方法を選ぶ | existing projects / repositories | current SAHOUを適用するとき | - | compatibility action | APPROVED | `shgeta/ai-development-sahou#30` |
| `PLATFORM.PROJECT_LOCAL.050` | Effective SAHOU overlay | REQUIREMENT | Common SAHOUをbaselineとし、Project Localの明示override / mapping / extensionをoverlayしてそのprojectのEffective SAHOUを構成する。Project Localがない場合はCommon SAHOUをそのままEffective SAHOUとする | SAHOU-managed project | startup / restart時 | - | Effective SAHOU | APPROVED | `shgeta/ai-development-sahou#30` |
| `PLATFORM.PROJECT_LOCAL.060` | Physical mapping | REQUIREMENT | Commonが想定するlogical roleとactual projectのfolder / file / entrypoint / authority locationが異なる場合、migrationしない選択を取るならProject Local AISPECにexplicit mappingを記録する | existing / third-party projects | physical layout差分をProject Localで吸収するとき | - | project-local mapping | APPROVED | `shgeta/ai-development-sahou#30` |
| `PLATFORM.PROJECT_LOCAL.070` | Effective use | REQUIREMENT | Effective SAHOU構成後のrouting、Adapter解決、folder/path解決、authority解決はCommon単体ではなくEffective SAHOUに従う | startup and runtime | Effective SAHOU構成後 | - | runtime interpretation | APPROVED | `shgeta/ai-development-sahou#30` |
| `PLATFORM.PROJECT_LOCAL.080` | Hybrid adaptation | RULE | 差分の一部をmigrationし、残りをProject Local mapping / overrideで吸収するhybridを許可する | existing projects | hybridが単純・安全・保守しやすい場合 | - | compatibility action | APPROVED | `shgeta/ai-development-sahou#30` |


## 2. Allowed contents

Project Localには次を保持してよい。

- Common ruleの明示override
- project固有AISPEC / rule
- environment-specific Adapter
- Adapter certification / test history
- project固有config / stateへのreference
- compatibility / migration instructions

Project Localはcanonical application source codeの置き場である必要はなく、SAHOU適用上のproject固有差分を保持するlayerである。

## 3. Authority, override, and mapping

Common SAHOUはbaseline authorityである。Project Localはproject固有差分だけを保持し、Common全体を複製しない。

### 3.1 Explicit override



SAHOU CommonとProject Localが同一事項を扱い、project固有overrideが必要な場合は黙って上書きしない。

最低限、override対象と理由を追跡可能にする。

```text
override_of: <Common RULE_ID or authority reference>
reason: <project-specific reason>
scope: <affected scope>
```

Commonの安全条件をoverrideする場合は、project側の明示authority / decision recordを必要とする。

### 3.2 Physical / logical mapping

folder / file / entrypoint / authority location等の差分を吸収する場合は、意味上のoverrideと区別してmappingとして記録する。

最低限:

```text
mapping_of: <Common logical role or authority reference>
actual_reference: <actual path / file / entrypoint / persistent reference>
reason: <why this project differs>
scope: <affected scope>
```

mappingは「Common ruleの意味を変更する」ことではなく、Common logical roleをactual project structureへ解決するためのものとする。

### 3.3 Effective SAHOU

startup / restart時は次のように解釈する。

```text
Common SAHOU
  -> baseline
Project Local explicit override / mapping / extension
  -> overlay
Effective SAHOU for this project
```

Project Localが `N/A` の場合:

```text
Effective SAHOU = Common SAHOU
```

Project Localが存在する場合:

```text
Effective SAHOU =
  Common SAHOU
  + explicit Project Local overlay
```

暗黙overrideはEffective SAHOUへ入れない。

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

## 6. Compatibility choice

既存repositoryへSAHOUを適用するとき、migrationを避けること自体も、Common layoutへ揃えること自体も目的化しない。

actual project stateを観測し、少なくとも次を比較する。

- migration cost
- Project Local adaptation / mapping cost
- operational risk
- maintenance cost
- third-party / read-only等のownership constraint

選択肢:

```text
A. migrate
B. Project Local adaptation
C. partial migration + Project Local adaptation
D. use as-is when already compatible
```

差分が小さく安全に直せるならmigrationしてよい。既存体系を維持する方が安全・単純ならProject Localで吸収してよい。hybridも許可する。

どの方法でも、最終的にCommon logical roleがactual project上で一意に解決できることを要求する。

## 7. Migration instructions

`migration/` は「必ず実行するversion upgrade script置き場」ではない。

次のような場合にだけmigration AISPEC / instructionを置いてよい。

- Common変更によりProject Local互換性が失われた
- Adapter contract変更により既存Adapterをそのまま使用できない
- schema変更によりruntimeが安全に解釈できない
- userが明示的な構造移行を採用した

migration instructionは可能ならfrom-version固定ではなく、observed state / precondition / target invariantを記述する。

## 8. Bootstrap requirement

Project Localを使用するprojectは、PROJECT_BOOTSTRAPへ少なくとも次を記載し、startup時にEffective SAHOUを構成できるようにする。

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
- migration / Project Local adaptation / hybridのうち単純・安全・保守しやすい方法を選んでいる
- Common + explicit Project Local overlayからEffective SAHOUを構成できる
- routing / Adapter / folder/path / authority解決がEffective SAHOUに従う
- Adapter / certificationが再発見可能である
- PROJECT_BOOTSTRAPからcurrent Project Localへ到達できる

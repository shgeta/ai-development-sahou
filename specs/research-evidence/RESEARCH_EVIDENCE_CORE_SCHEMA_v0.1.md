# Research Evidence Core Schema v0.1

- Updated: 2026-09-24
- Status: CANDIDATE
- Scope: domain-independent evidence semantics
- Relation to AISPEC: sibling semantic model. AISPEC defines current normative meaning; Research Evidence Core defines minimal evidence/provenance semantics that may support that meaning.
- Decision history: ai-development-sahou Issue #17

## 1. Purpose

Research Evidence Core is a deliberately small logical evidence model.

It defines only:
- reusable identities,
- information sources,
- evidence-producing activities,
- observations,
- propositions,
- research questions,
- assessments,
- and typed relations between them.

Anything specific to papers, clinical research, toxicology, chemistry, regulation, vehicles, products, patents, storage, UI, audit timestamps, indexing, or workflow belongs in a Plugin / Profile / Adapter unless it is proven to be universally semantic.

## 2. Core principles

1. Meaning MUST NOT depend on physical file, folder, row order, Markdown structure, or shard location.
2. Every semantic record MUST have a stable logical ID.
3. Source assertion, observation, and assessment MUST remain distinguishable.
4. UNKNOWN MUST NOT be collapsed into false, absent, not measured, not reported, or not retrieved.
5. Retrieval uses SEARCH -> seed -> required closure, not whole-database loading.
6. Physical shards are storage partitions, not semantic boundaries.
7. Field absence is schema-layer absence, not an epistemic value.
8. Plugins MAY extend Core but MUST NOT silently redefine Core semantics.
9. Operational convenience fields MUST NOT be promoted into Core merely because an implementation finds them useful.
10. Work history and implementation history remain outside the evidence semantics.

## 3. Minimal common record shape

Every semantic record requires only:

- `ID`
- `TYPE`

No other field is universally required by Core.

Fields such as the following are NOT Core requirements:
- TITLE
- DESCRIPTION
- STATUS
- CREATED_AT
- UPDATED_AT
- SOURCE_REF
- DECISION_REF
- TAGS
- owner / author / user
- file path
- storage location

A Plugin may require some of these for its own domain.
An Adapter may add audit, persistence, indexing, display, or workflow metadata.

## 4. Core semantic types

### 4.1 ENTITY

Reusable identity referenced by other records.

Identity boundary:
create a new ENTITY only when the real-world or conceptual referent changes.

Alias, spelling, language, identifier, or display-name changes alone do not create a new ENTITY.

### 4.2 SOURCE

A retrievable information-bearing object.

Identity boundary:
create a new SOURCE when the citable/versioned information object changes materially.

Different manifestations or versions may be connected explicitly rather than treated as unrelated sources.

### 4.3 ACTIVITY

An action or process that uses, transforms, searches, analyzes, or generates evidence.

Identity boundary:
create a new ACTIVITY when the execution/reproducibility unit materially changes.

### 4.4 OBSERVATION

An atomic observed or derived result.

Identity boundary:
create a new OBSERVATION when a change in endpoint, comparison, timepoint, sample/population stratum, analysis set, or value makes separate citation or assessment useful.

OBSERVATION does not itself mean that a proposition is supported.

### 4.5 PROPOSITION

A truth-evaluable statement whose evidential support may change.

Identity boundary:
create a new PROPOSITION when its truth conditions materially change.

A source statement is not automatically a true proposition, and a proposition is not automatically an observation.

### 4.6 QUESTION

A research question that can act as a retrieval/closure seed.

Identity boundary:
create a new QUESTION when its scope changes enough to change the relevant evidence set.

### 4.7 ASSESSMENT

An explicit evaluative judgment about one or more records or relations.

Examples may include support, contradiction, bias, independence, directness, applicability, duplication, authority, certainty, or evidence gap.

Identity boundary:
create a new ASSESSMENT when target, assessor, criterion/framework, evidence basis, or judgment materially changes.

Assessment semantics MUST NOT be silently embedded into an OBSERVATION.

## 5. Graph primitive: RELATION

RELATION connects semantic records.

Minimum shape:
- `SUBJECT_ID`
- `PREDICATE`
- `OBJECT_ID`

That is the entire Core relation requirement.

Qualifiers, provenance, timing, confidence, source location, and relation-specific metadata belong in Plugins or qualified ASSESSMENT structures when needed.

Core relation examples:
- SOURCE REPORTS ACTIVITY
- SOURCE ASSERTS PROPOSITION
- ACTIVITY USES ENTITY
- ACTIVITY GENERATES OBSERVATION
- OBSERVATION ABOUT ENTITY
- QUESTION TARGETS PROPOSITION
- ASSESSMENT EVALUATES <record>
- ASSESSMENT SUPPORTS PROPOSITION
- ASSESSMENT CONTRADICTS PROPOSITION
- SOURCE VERSION_OF SOURCE

Core defines relation semantics, not storage syntax.

## 6. Epistemic distinctions

Core defines these distinctions conceptually but does not require every record to carry an epistemic-state field.

UNKNOWN is distinct from:
- NOT_REPORTED
- NOT_MEASURED
- NOT_RETRIEVED
- NOT_APPLICABLE
- OUT_OF_SCOPE
- CONFLICTING
- REVIEW_REQUIRED

A Plugin decides where these values are valid and whether a field is required.

Missing field != UNKNOWN by default.

## 7. Evidence closure

Standard retrieval:

```text
SEARCH
  -> seed QUESTION / PROPOSITION / ENTITY / SOURCE
  -> follow explicit relations
  -> apply active Plugin closure rules
  -> stop when required evidence closure is satisfied
```

Default proposition-oriented closure:

```text
PROPOSITION
  -> relevant ASSESSMENT
  -> underlying OBSERVATION
  -> generating ACTIVITY
  -> reporting SOURCE
  -> referenced ENTITY identities
```

Additional bias, independence, access, methodological, or domain records are included only when required by the active Plugin or query.

Missing required referenced records -> REVIEW_REQUIRED.

## 8. Meaning separation

The following are different semantics:

- `SOURCE ASSERTS PROPOSITION`: the source says it.
- `ACTIVITY GENERATES OBSERVATION`: something was observed or derived.
- `ASSESSMENT SUPPORTS PROPOSITION`: an evaluator judges that evidence supports it.

Core MUST NOT collapse these.

A source assertion is not automatically evidence.
An observation is not automatically support.
Support does not imply strong, direct, unbiased, independent, or sufficient evidence.

## 9. Plugin contract

A Plugin MAY add:
- TYPE subtypes
- type-specific fields
- controlled vocabularies
- relation predicates
- closure rules
- validation rules
- normalization rules
- domain-specific derived states

A Plugin MUST declare:
- `PLUGIN_ID`
- `VERSION`
- `TARGET_CORE_VERSION`
- applicable Core TYPEs
- added fields and their semantics
- required vs optional
- field-absence meaning
- added relation vocabulary
- closure additions
- validation rules
- migration boundary

A Plugin MUST NOT:
- redefine a Core TYPE,
- change the meaning of an existing Core relation,
- make unrelated Core records invalid,
- treat Plugin absence as epistemic UNKNOWN,
- require unrelated legacy backfill without declaring migration.

Multiple compatible Plugins MAY coexist.

## 10. Schema evolution

When adding a field, define:
- meaning
- applicable TYPE / Plugin
- required or optional
- absence semantics
- default if any
- backfill rule
- migration trigger

A change is a MIGRATION when it changes:
- Core TYPE meaning,
- identity boundary,
- Core relation meaning,
- Core/Plugin authority boundary,
- or legacy meaning through a new universal requirement/default.

## 11. Physical storage

Core does not prescribe storage.

Possible representations include:
- Markdown
- JSONL
- CSV/TSV
- relational tables
- graph storage
- mixed versioned shards

Physical layout, timestamps, index files, manifests, and cache structures are not semantic authority unless a separate Adapter explicitly says otherwise.

## 12. Minimal validation

Validate at least:
- ID uniqueness within the logical evidence set
- TYPE is defined by Core or an active Plugin
- relation endpoints resolve
- relation predicate is valid
- required closure can resolve
- source assertion is not silently promoted to observation
- assessment is not silently merged into observation
- field absence is not auto-converted to UNKNOWN/false
- publication/source count is not silently treated as independent evidence count

## 13. Boundary with AISPEC

Research Evidence Core:
- represents evidence and evidence interpretation.

AISPEC:
- represents current normative/project semantic rules.

Evidence may support AISPEC through explicit provenance, but Research Evidence does not become AISPEC merely because a proposition is well supported.

## 14. Boundary with Work Item Tracker and Adapters

Work Item Tracker:
- search path
- dead ends
- design decisions
- why an interpretation was adopted
- next actions

Versioned repository:
- exact representation changes

Adapters:
- product/storage/workflow mappings
- timestamps
- persistence metadata
- indexing
- audit metadata
- UI/presentation conveniences

These MUST NOT be pushed into Core solely for operational convenience.

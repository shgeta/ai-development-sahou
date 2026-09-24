# Research Core v0.1

- Updated: 2026-09-25
- Status: CANDIDATE
- Scope: domain-independent research work model
- Evidence model: `RESEARCH_EVIDENCE_CORE_SCHEMA_v0.1.md`
- Decision history: ai-development-sahou Issue #17

## 1. Purpose

Research Core defines the common meaning of **research work** in SAHOU.

Research is broader than literature search.

In this model, research means:

> starting from a question, collecting or producing relevant information, analyzing it, evaluating evidence, resolving contradictions and uncertainty, and synthesizing a decision-useful finding.

Research therefore includes, when applicable:

- source research,
- literature / patent / web / document research,
- empirical investigation,
- data analytics,
- code / log / visual analysis,
- experiment and measurement,
- comparison and modeling,
- evidence evaluation,
- synthesis.

Research Core does not make all of these one universal schema.
It defines their common workflow and delegates detailed semantics to the Evidence Core and compatible Plugins / Profiles.

## 2. Research and Analytics

`Analytics` is a **subordinate research activity family**, not a sibling Core.

Conceptually:

```text
Research
  -> Source Research
  -> Empirical / Analytic Research
       -> Data Analytics
       -> Code Analysis
       -> Log Analysis
       -> Visual Analysis
       -> Statistical / Computational Analysis
       -> other analysis methods
  -> Evidence Evaluation
  -> Synthesis
```

The category boundaries are descriptive, not separate authorities.

An analytic task is research when it contributes evidence or findings toward a QUESTION, PROPOSITION, decision, or unresolved uncertainty.

Analytics MAY use domain-specific Plugins when structured fields are repeatedly needed.
Analytics MUST NOT require a universal analytics schema merely because one implementation uses tables, metrics, code, images, or logs.

## 3. Common research flow

Default conceptual flow:

```text
QUESTION
  -> plan / scope
  -> acquire or produce evidence
       -> source search
       -> experiment / observation
       -> analytics
  -> OBSERVATION / PROPOSITION
  -> ASSESSMENT
  -> contradiction / uncertainty handling
  -> synthesis
  -> finding / decision input
```

Not every research task requires every step.

Exploratory work may begin from an ENTITY, SOURCE, anomaly, dataset, code path, visual difference, or other seed and later create a QUESTION.

## 4. Evidence semantics

Research Core uses Research Evidence Core as the common evidence/provenance model.

Key mappings:

- research object / reusable identity -> `ENTITY`
- retrievable source -> `SOURCE`
- search / experiment / analysis / transformation -> `ACTIVITY`
- measured / derived / observed result -> `OBSERVATION`
- truth-evaluable statement -> `PROPOSITION`
- research seed / scope -> `QUESTION`
- interpretation / support / contradiction / applicability / certainty -> `ASSESSMENT`
- explicit graph connection -> `RELATION`

Analytics therefore does not need a new Core TYPE.
An analysis is normally an `ACTIVITY` that uses SOURCE / ENTITY / prior OBSERVATION and generates new OBSERVATION or derived artifacts.

Interpretation of an analytic result belongs in `ASSESSMENT` or `PROPOSITION`, not silently inside the raw observation.

## 5. Plugin model

Research Core stays light.

Plugins / Profiles add semantics only when a research domain or method repeatedly requires them.

Examples:

- Paper Research Plugin
- Patent Research Plugin
- regulatory-source plugin
- clinical / toxicology / chemistry domain profile
- data-analysis method profile when repeated structured analytics semantics justify it

A Plugin may add:
- ACTIVITY subtypes,
- method fields,
- controlled vocabularies,
- source-specific identifiers,
- closure additions,
- validation rules.

A Plugin MUST NOT redefine Research as only source search, only literature review, or only numerical analytics.

## 6. Relationship with Paper Research

Paper Research is one research path.

```text
Research Core
  -> Paper Research Plugin
       -> literature search
       -> screening
       -> access / retrieval
       -> extraction
       -> publication lineage
       -> paper-specific provenance
```

Paper Research MAY feed observations, propositions and assessments into a broader research closure together with non-paper evidence.

A research question may therefore combine:
- paper evidence,
- dataset analysis,
- code/log findings,
- visual inspection,
- experiment results,
without creating separate top-level research authorities.

## 7. Relationship with AISPEC

Research Core answers:

- what was investigated,
- what evidence was collected or produced,
- what analysis was performed,
- what was observed,
- how evidence was evaluated,
- what remains unknown or conflicting.

AISPEC answers:

- what current semantic / normative meaning has been adopted for the project.

Research findings may cause an AISPEC update, but research records do not become AISPEC automatically.

Typical flow:

```text
Research QUESTION
  -> evidence / analytics / assessment
  -> synthesis
  -> decision
  -> AISPEC update when current project meaning changes
```

## 8. Boundary with Work Item Tracker

Work Item / Issue remains the history of the research task:

- why the question was investigated,
- search/analysis dead ends,
- decisions about scope or method,
- why one interpretation was adopted,
- remaining work.

Research Core stores durable research semantics when they need to be searched, compared, reused, validated, or included in evidence closure.

Routine transient exploration does not need to become a durable research record.

## 9. Closure

Research closure begins from the active research seed and follows only explicit required relations plus active Plugin closure rules.

Examples:

```text
QUESTION
  -> relevant PROPOSITION
  -> ASSESSMENT
  -> OBSERVATION
  -> analytic / experimental ACTIVITY
  -> SOURCE / ENTITY
```

or:

```text
QUESTION
  -> literature-search ACTIVITY
  -> SOURCE
  -> extracted OBSERVATION
  -> ASSESSMENT
  -> synthesis
```

Mixed closures are normal.

A research task MUST NOT be forced to load all literature, all datasets, all analytics records, or the entire evidence graph.

## 10. Validation principles

A Research Core implementation should preserve at least these distinctions:

- search result != empirical observation
- raw observation != interpretation
- analytics output != automatically true proposition
- source assertion != independently verified evidence
- absence of result != evidence of absence
- UNKNOWN != false
- publication count != evidence independence
- analysis method != research question
- Research != Literature Research only
- Research != Analytics only

## 11. Current architecture

```text
SAHOU
  -> Research Core
       -> Research Evidence Core
       -> Paper Research Plugin
       -> future compatible research/domain plugins
  -> AISPEC
  -> Work Item / Issue
  -> validation / change workflows
```

This structure intentionally avoids creating a separate Analysis Core.

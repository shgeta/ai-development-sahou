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

## 3.1 Scope anchor and scope-drift guardrail

Each active research QUESTION SHOULD maintain a **Scope Anchor**: the current authoritative definition of the research universe, inclusion/exclusion boundary, and decision target.

Examples:
- all formulation-ready raw-material candidates;
- all implementations under a named runtime;
- all publications satisfying a stated population/intervention criterion.

A Scope Anchor is not replaced merely because the current activity is narrower.

Rules:

1. A source subset, search result set, paper-specific candidate list, plugin output, or local work queue is a **working subset**, not a new research universe.
2. A working subset MUST NOT silently replace the Scope Anchor.
3. A follow-up such as “find suppliers”, “compare products”, “validate implementations”, or “continue the search” MUST resolve its target set from the Scope Anchor unless the user explicitly narrows scope.
4. If only a subset is being processed, the activity/output MUST be labeled as a subset pass and MUST NOT be presented as a complete audit of the anchored universe.
5. Classification convenience MUST NOT become an implicit exclusion rule. Examples:
   - pure compound != research-only by definition;
   - extract != the definition of raw material;
   - one paper’s botanical candidates != all candidates;
   - one tool’s supported entities != the research universe.
6. When the user corrects scope, that correction SHOULD update durable current-state records / plan / issue notes so later turns do not regress to the prior scope.
7. Before changing the candidate universe, distinguish:
   - **scope decision**: intentional change to the Scope Anchor;
   - **subset activity**: temporary narrowing for one pass;
   - **evidence result**: findings from that subset.

### Scope-drift check

Before presenting a “complete”, “overall”, “all candidates”, “master”, or equivalent synthesis, verify:

- What is the current Scope Anchor?
- Did the current activity cover the entire anchored universe?
- If not, is the result clearly labeled as partial/subset?
- Did any recent source or paper accidentally redefine the candidate universe?
- Did a storage or schema category accidentally become an inclusion/exclusion criterion?

Failure to preserve this distinction is a research-process error even when every individual fact is correct.

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
- Analysis Research Plugin
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

## 6. Relationship with Analysis Research

Analysis Research is the standard Plugin for source-backed analysis, comparison, diagnostic classification, runtime-sensitive validation, and mixed empirical/computational evidence.

It generalizes reusable lessons from implementation reconstruction and visual/source analysis without making Figma, browser rendering, screenshots, or any one tool a universal Research Core requirement.

Typical Analysis Research flow:

```text
source closure
  -> deterministic facts / runtime readiness
  -> localized analysis
  -> observation
  -> difference / cause assessment
  -> triangulation when needed
  -> synthesis
```

Analysis Research keeps:
- source authority separate from derived artifacts,
- raw observation separate from interpretation,
- deterministic validation ahead of perceptual QA where possible,
- unresolved findings as explicit UNKNOWN / REVIEW_REQUIRED,
- exact source/runtime generation identity attached to reproducibility-sensitive results.

## 7. Relationship with Paper Research

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

## 8. Relationship with AISPEC

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

## 9. Boundary with Work Item Tracker

Work Item / Issue remains the history of the research task:

- why the question was investigated,
- search/analysis dead ends,
- decisions about scope or method,
- why one interpretation was adopted,
- remaining work.

Research Core stores durable research semantics when they need to be searched, compared, reused, validated, or included in evidence closure.

Routine transient exploration does not need to become a durable research record.

## 10. Closure

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

## 11. Validation principles

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
- working subset != Scope Anchor
- source-specific candidate set != research universe
- classification convenience != exclusion criterion

## 12. Current architecture

```text
SAHOU
  -> Research Core
       -> Research Evidence Core
       -> Paper Research Plugin
       -> Analysis Research Plugin
       -> future compatible research/domain plugins
  -> AISPEC
  -> Work Item / Issue
  -> validation / change workflows
```

This structure intentionally avoids creating a separate Analysis Core.

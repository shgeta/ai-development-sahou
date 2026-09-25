# Analysis Research Schema Plugin v0.1

- Updated: 2026-09-25
- Status: CANDIDATE
- Plugin ID: RESEARCH_EVIDENCE.ANALYSIS
- Target Core: Research Evidence Core Schema v0.1
- Parent work model: Research Core v0.1
- Scope: source-backed analysis, comparison, diagnostic classification, runtime-sensitive validation, and mixed empirical/computational evidence
- Decision history: ai-development-sahou Issue #17

## 1. Purpose

Analysis Research Plugin extends Research Evidence Core for research tasks where findings are produced by analyzing structured or semi-structured source material, generated artifacts, implementations, logs, rendered outputs, datasets, images, or other inspectable representations.

Typical uses include:
- data analysis,
- code analysis,
- log analysis,
- document/source-structure analysis,
- visual comparison,
- implementation-vs-source analysis,
- rendering/runtime analysis,
- computational diagnostics,
- regression investigation,
- multi-representation triangulation.

This Plugin does NOT make analytics a separate top-level Core.

## 2. Design principles

1. Source facts MUST be closed before downstream comparison is used to rediscover them.
2. Derived artifacts MUST NOT silently become semantic authority.
3. Analysis output MUST remain distinguishable from interpretation.
4. Localized analysis SHOULD precede whole-system conclusions when defects can be spatially or structurally isolated.
5. A threshold MUST NOT be widened merely to make a failing comparison pass.
6. Target-specific patches MUST NOT replace a missing general rule when the defect is systemic.
7. UNKNOWN / REVIEW_REQUIRED MUST remain explicit when available evidence cannot distinguish competing explanations.
8. Runtime-sensitive findings MUST carry enough runtime identity to be reproducible.
9. Comparison evidence MAY require multiple independent renderers / methods when one representation has known residual behavior.
10. Cache/dedupe MAY optimize repeated work but MUST NOT merge distinct source occurrences or distinct usage semantics.

## 3. Applicable Core types

This Plugin may extend:
- SOURCE
- ENTITY
- ACTIVITY
- OBSERVATION
- QUESTION
- ASSESSMENT
- RELATION

PROPOSITION normally uses Core semantics unchanged.

## 4. Source closure before analysis

### 4.1 Principle

A shallow extraction is insufficient when analysis depends on contextual or referenced source semantics.

Before analytic comparison, the active research closure SHOULD resolve all source context needed to interpret the target.

Possible closure dimensions:
- descendants / nested structure,
- ancestors / provenance,
- referenced definitions,
- sibling context when meaning depends on compound structure,
- effective inherited/overridden configuration,
- referenced assets,
- runtime dependencies,
- unresolved references.

A source-dependent analysis MUST NOT silently drop unresolved dependencies.

### 4.2 Closure status

Recommended derived status:
- SOURCE_CLOSED
- SOURCE_PARTIAL
- SOURCE_BLOCKED
- REVIEW_REQUIRED

SOURCE_PARTIAL MUST NOT be rounded to SOURCE_CLOSED.

### 4.3 Separation from discovery

Visual comparison, runtime screenshots, output diffs, and similar downstream QA are validation evidence.

They SHOULD NOT be the primary discovery mechanism for facts already deterministically available from the source.

If downstream QA reveals a missing explicit source fact, route the defect upstream to source inventory / closure / normalization instead of adding a target-specific patch.

## 5. ACTIVITY subtypes

Recommended analysis ACTIVITY subtypes:
- DATA_ANALYSIS
- STATISTICAL_ANALYSIS
- CODE_ANALYSIS
- LOG_ANALYSIS
- SOURCE_STRUCTURE_ANALYSIS
- VISUAL_COMPARISON
- IMPLEMENTATION_COMPARISON
- RENDERING_ANALYSIS
- RUNTIME_VALIDATION
- DIFFERENCE_LOCALIZATION
- TRIANGULATION
- REGRESSION_ANALYSIS
- SYNTHESIS_ANALYSIS

Domain Plugins MAY define more specific subtypes.

## 6. Analysis input and output

Recommended relations:
- ACTIVITY USES SOURCE
- ACTIVITY USES ENTITY
- ACTIVITY USES OBSERVATION
- ACTIVITY USES ACTIVITY
- ACTIVITY GENERATES OBSERVATION
- ACTIVITY COMPARES SOURCE
- ACTIVITY VALIDATES SOURCE
- ACTIVITY LOCALIZES OBSERVATION
- ASSESSMENT EVALUATES OBSERVATION
- ASSESSMENT CLASSIFIES OBSERVATION

An analytic ACTIVITY may generate:
- measured values,
- differences,
- counts,
- coordinates,
- regions,
- hashes,
- runtime observations,
- structural findings,
- residual classifications.

Interpretation remains separate.

## 7. Authority layers

Analysis SHOULD distinguish at least:

- SOURCE_AUTHORITY — original source or exact authoritative revision
- SOURCE_DERIVED — deterministic derivation from source
- IMPLEMENTATION_OR_CANDIDATE — object being evaluated
- VALIDATION_ARTIFACT — screenshot, capture, diff image, report, trace, checkpoint
- DIAGNOSTIC_EVIDENCE — localized residuals, renderer comparison, runtime observation

A screenshot/capture/diff is not automatically source authority.

A generated reference MAY be useful diagnostic evidence while still being non-authoritative.

Recommended qualifiers:
- AUTHORITY_ROLE
- DERIVED_FROM_ID
- EXACT_REVISION
- CONTENT_HASH

`AUTHORITY_ROLE` is the single classification for authority position. Do not add a parallel `AUTHORITATIVE = true|false` flag that can disagree with the role/provenance graph.

## 8. Runtime fingerprint

When result meaning can change with runtime, the ACTIVITY SHOULD preserve a reproducibility fingerprint.

Recommended fields:
- RUNTIME_KIND
- RUNTIME_VERSION
- TOOL_VERSION
- VIEWPORT_OR_INPUT_SHAPE
- DEVICE_SCALE_OR_EQUIVALENT
- RESOURCE_READY_STATE
- DEPENDENCY_VERSION_SET
- CONFIG_HASH
- SOURCE_REVISION

The exact field set is method-specific.

A result produced before a required runtime dependency is ready MUST NOT be promoted to READY merely because the same static configuration was declared.

## 9. Localize before global correction

When a comparison fails, prefer progressively localized analysis.

Conceptual flow:

```text
whole output
 -> major region / subsystem
 -> component / owner
 -> primitive / property
 -> independent diagnostic
 -> classification
 -> correction only after cause is bounded
```

This reduces the risk of compensating one defect with another.

A whole-output score MAY prioritize work, but SHOULD NOT by itself identify cause.

## 10. Deterministic gate before perceptual QA

If source-derived material can be transferred or checked deterministically, validate it before screenshot/pixel/perceptual QA.

Examples:
- exact text/configuration values,
- geometry,
- source-owned vector/shape information,
- image usage/order,
- transforms,
- explicit visibility,
- exact runtime dependency readiness,
- deterministic material properties.

Perceptual/visual QA is then reserved for:
- rasterization,
- antialiasing,
- subpixel residuals,
- renderer-specific behavior,
- complex composition not closed deterministically,
- heuristic/responsive regions,
- other genuinely non-deterministic residuals.

## 11. Triangulation

When one comparison method or renderer has known blind spots, use independent evidence rather than tuning toward one artifact.

Recommended ACTIVITY subtype:
- TRIANGULATION

Possible inputs:
- authoritative source data,
- implementation output,
- renderer A,
- renderer B,
- alternate parser/decoder,
- independent measurement,
- structural inspection.

Recommended ASSESSMENT judgments:
- SOURCE_OR_IMPLEMENTATION_DIFFERENCE
- RENDERER_SPECIFIC_RESIDUAL
- TOOLCHAIN_SPECIFIC_RESIDUAL
- INCONCLUSIVE
- REVIEW_REQUIRED

Agreement between two derived renderers does not automatically outrank the authoritative source.

## 12. Residual classification

A comparison residual SHOULD be classified before a corrective change.

Recommended ASSESSMENT_TYPE:
- DIFFERENCE_CLASSIFICATION

Recommended judgments:
- SOURCE_DIFFERENCE
- IMPLEMENTATION_DIFFERENCE
- RUNTIME_DIFFERENCE
- RENDERER_DIFFERENCE
- TOOLCHAIN_DIFFERENCE
- EXPECTED_NUMERICAL_RESIDUAL
- HEURISTIC_REGION
- UNKNOWN
- REVIEW_REQUIRED

Classification MAY be hierarchical.

A residual marked UNKNOWN or REVIEW_REQUIRED MUST NOT be converted to implementation defect solely to make a gate pass.

## 13. Threshold discipline

A tolerance or threshold is part of method semantics.

Rules:
1. record threshold and method version when it affects interpretation;
2. do not widen the threshold after seeing a failure solely to convert FAIL to PASS;
3. threshold changes require an explicit rationale and should invalidate prior comparisons when semantics change;
4. a passing global threshold does not erase localized blocking defects;
5. a failing global threshold does not prove every localized region is wrong.

## 14. Occurrence identity vs deduplication

Identical reusable material may be deduplicated for storage/computation.

However:
- source occurrence identity remains distinct,
- placement/transform/context remain occurrence-specific,
- validation may still need to inspect each occurrence.

Canonical material fingerprinting MUST exclude transport-only identity while retaining semantics that change visible/analytic meaning.

A cache key MUST include all usage parameters that can change the result.

For example, an image derivative cache keyed only by source bytes is invalid when crop, transform, target geometry, rotation, or effect chain can differ.

## 15. Hidden / implementation-only facts

Some source semantics are likely to disappear in flattened output.

Examples:
- sizing intent,
- constraint ownership,
- crop/focal-point semantics,
- component/variant state,
- clipping/mask/effect chain,
- authored responsive ownership,
- dependency provenance.

When these facts materially affect analysis or reconstruction, represent or preserve them before flattening.

Do not infer them from screenshots when an authoritative structural source exists.

## 16. Source generation coherence

Comparison requires source/cohort/revision coherence.

A validation ACTIVITY SHOULD record:
- source identity,
- source revision/fingerprint,
- candidate revision,
- comparison reference revision,
- dependency generation/version.

If source and comparison reference come from incompatible generations, invalidate the metric rather than optimizing against it.

## 17. Review artifact separation

Human-review UI/artifacts SHOULD be separated from the validated core output when review chrome can alter geometry, rendering, or runtime behavior.

The review artifact may wrap or embed the validated core, but it MUST NOT silently change the object being validated.

If review overlay changes the validated core, prior validation becomes stale.

## 18. Mixed research

Analysis Research may coexist with Paper Research and other Plugins in one evidence closure.

Example:

```text
QUESTION
 -> paper SOURCE / literature ACTIVITY
 -> dataset SOURCE / DATA_ANALYSIS
 -> code SOURCE / CODE_ANALYSIS
 -> visual SOURCE / VISUAL_COMPARISON
 -> OBSERVATION
 -> ASSESSMENT
 -> synthesis
```

No separate top-level analytics authority is required.

## 19. Validation

Validate at least:
- source closure status is explicit,
- unresolved source references are not silently dropped,
- source authority and derived artifact are distinguishable,
- analytic ACTIVITY and interpretation ASSESSMENT are separate,
- runtime-sensitive results carry sufficient fingerprint,
- stale/mismatched source generation invalidates comparison,
- thresholds are not silently changed post-failure,
- cache keys include render/analysis-relevant usage semantics,
- dedupe does not erase occurrence identity,
- review artifacts do not alter validated core unnoticed,
- unknown residuals remain UNKNOWN/REVIEW_REQUIRED,
- deterministic source facts are not deferred unnecessarily to perceptual QA.

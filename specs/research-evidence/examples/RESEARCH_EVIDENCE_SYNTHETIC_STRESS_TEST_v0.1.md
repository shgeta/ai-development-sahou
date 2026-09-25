# Research Evidence synthetic stress test v0.1

- Status: CANDIDATE TEST FIXTURE
- Public-safe: synthetic data only
- Core: RESEARCH_EVIDENCE_CORE_SCHEMA_v0.1
- Plugin: PAPER_RESEARCH_SCHEMA_PLUGIN_v0.1

## Scenario

A synthetic compound `Compound-A` is investigated for whether topical use generates `Metabolite-B` in human skin.

Available literature:
- Paper Alpha: paywalled publisher article; abstract says Compound-A is biologically active.
- Paper Beta: later clinical paper from the same research network.
- Thesis Gamma: same author/institution lineage; metadata visible, full text unavailable.
- Review Delta: states that Compound-A probably acts through Metabolite-B, citing Paper Alpha.
- Repository manuscript: an accepted-manuscript version of Paper Alpha is found in an institutional repository.
- The manuscript reports a 48-hour cell stability assay but does not directly measure human-skin metabolism.
- No independent external replication is identified.

## 1. QUESTION

ID: Q.001
TYPE: QUESTION
TITLE: Does topical Compound-A generate Metabolite-B in human skin?
STATUS: ACTIVE
EPISTEMIC_STATE: UNKNOWN

## 2. ENTITY

E.SUBSTANCE.001 = Compound-A
E.SUBSTANCE.002 = Metabolite-B
E.ORG.001 = Example Origin Lab
E.ORG.002 = Example University
E.PERSON.001 = Researcher One

Aliases belong to the same ENTITY identity unless the real-world referent changes.

## 3. SOURCE records

S.001
TYPE: SOURCE
SUBTYPE: JOURNAL_ARTICLE
TITLE: Synthetic mechanistic paper Alpha
DOI: 10.0000/example.alpha
VERSION_TYPE: VERSION_OF_RECORD
ACCESS_STATE: PAYWALLED_AFTER_FREE_ROUTE_CHECK

S.002
TYPE: SOURCE
SUBTYPE: AUTHOR_MANUSCRIPT
TITLE: Accepted manuscript of Alpha
VERSION_TYPE: ACCEPTED_MANUSCRIPT
VERSION_OF_SOURCE_ID: S.001
CONTENT_EQUIVALENCE: SUBSTANTIALLY_SAME
ACCESS_STATE: FREE_ALTERNATE_VERSION_VERIFIED

S.003
TYPE: SOURCE
SUBTYPE: THESIS
TITLE: Synthetic thesis Gamma
ACCESS_STATE: FREE_ROUTE_SEARCH_INCOMPLETE

S.004
TYPE: SOURCE
SUBTYPE: REVIEW_ARTICLE
TITLE: Synthetic review Delta
ACCESS_STATE: FREE_FULL_TEXT_VERIFIED

## 4. PAPER_ACCESS_CHECK activities

A.ACCESS.001
TYPE: ACTIVITY
SUBTYPE: PAPER_ACCESS_CHECK
TARGET_SOURCE_ID: S.001
ROUTE_TYPE: PUBLISHER_OA
RESULT: NOT_FOUND

A.ACCESS.002
TARGET_SOURCE_ID: S.001
ROUTE_TYPE: INSTITUTIONAL_REPOSITORY
RESULT: FULL_TEXT_FOUND
VERSION_TYPE: ACCEPTED_MANUSCRIPT
ACCESS_URL_OR_REF: synthetic://repository/alpha
CHECKED_AT: 2026-09-24

Expected behavior:
- S.001 itself remains publisher-paywalled.
- The work has a free alternate version S.002.
- The evidence closure for Alpha may be satisfied from S.002 if the required content is present.
- Purchase is NOT automatically required.

## 5. ACTIVITY

A.EXP.001
TYPE: ACTIVITY
SUBTYPE: IN_VITRO_EXPERIMENT
TITLE: 48-hour cell stability assay
RELATION:
- S.002 REPORTS A.EXP.001
- A.EXP.001 USES E.SUBSTANCE.001

A.CLIN.001
TYPE: ACTIVITY
SUBTYPE: RCT
TITLE: Small clinical study from origin-linked network
RELATION:
- S.005 REPORTS A.CLIN.001

## 6. OBSERVATION

O.001
TYPE: OBSERVATION
TITLE: Compound-A remains detectable after 48 hours
GENERATED_BY: A.EXP.001
RESULT_FORM: QUANTITATIVE
EPISTEMIC_STATE: KNOWN

O.002
TYPE: OBSERVATION
TITLE: Human-skin Metabolite-B formation
GENERATED_BY: none
EPISTEMIC_STATE: NOT_MEASURED

Expected behavior:
- O.001 does not prove O.002.
- NOT_MEASURED must not become false.
- absence of O.002 is not itself an empirical negative result.

## 7. PROPOSITION

P.001
TYPE: PROPOSITION
TITLE: Compound-A generates Metabolite-B in human skin after topical use
STATUS: ACTIVE

P.002
TYPE: PROPOSITION
TITLE: Compound-A itself persists in the tested cell system for 48 hours
STATUS: ACTIVE

Relations:
- S.004 ASSERTS P.001
- S.002 ASSERTS P.002

## 8. ASSESSMENT

AS.001
TYPE: ASSESSMENT
ASSESSMENT_TYPE: CLAIM_SUPPORT
TARGET: O.001 -> P.002
JUDGMENT: SUPPORTS
DIRECTNESS: DIRECT

AS.002
TYPE: ASSESSMENT
ASSESSMENT_TYPE: CLAIM_SUPPORT
TARGET: O.001 -> P.001
JUDGMENT: DOES_NOT_ESTABLISH
DIRECTNESS: INDIRECT
RATIONALE: cell stability does not directly establish metabolite formation in human skin

AS.003
TYPE: ASSESSMENT
ASSESSMENT_TYPE: INDEPENDENCE
TARGET: S.005
JUDGMENT: ORIGIN_LINKED
RATIONALE: author and organization network overlaps the origin program

AS.004
TYPE: ASSESSMENT
ASSESSMENT_TYPE: PUBLICATION_LINEAGE
TARGET: S.003, S.005
JUDGMENT: POSSIBLY_OVERLAPPING
RATIONALE: author, institution, timing, and endpoints overlap; raw-data identity not established

AS.005
TYPE: ASSESSMENT
ASSESSMENT_TYPE: EVIDENCE_GAP
TARGET: Q.001
JUDGMENT: DIRECT_HUMAN_SKIN_DATA_MISSING

## 9. Purchase candidate behavior

If the accepted manuscript S.002 contains all methods/results needed for the current question:
- do not create PURCHASE_NECESSITY for S.001.

If a decisive figure or method exists only in S.001 and is needed to resolve Q.001:
- create ASSESSMENT type PURCHASE_NECESSITY,
- link it to S.001 and Q.001,
- require completed free-route closure,
- record expected decision impact.

## 10. Closure test

Seed:
Q.001

Expected closure:
Q.001
 -> P.001
 -> AS.002 / AS.005
 -> O.001
 -> A.EXP.001
 -> S.002
 -> S.001 as version identity
 -> A.ACCESS.001 / A.ACCESS.002
 -> relevant ENTITY identities
 -> AS.003 / AS.004 when independence/duplication affects synthesis

Expected exclusions:
- unrelated endpoints from A.CLIN.001
- full author biography
- unrelated papers by the same organizations
- every record in the repository

## 11. Failure conditions exposed by this fixture

The schema fails if it:
1. marks the publisher article simply PAYWALLED and misses the free accepted manuscript,
2. converts a source assertion in Review Delta into an OBSERVATION,
3. treats cell stability as direct proof of human-skin metabolism,
4. converts NOT_MEASURED into a negative finding,
5. counts Thesis Gamma and Paper Beta as independent evidence without lineage assessment,
6. requires purchase before free-route closure,
7. cannot resolve Q.001 without loading the entire evidence graph.


## 12. Non-literature analytics stress test

A synthetic repository also contains:
- dataset `Dataset-X`,
- application log `Log-Y`,
- implementation source `Code-Z`,
- two rendered images `Visual-Before` and `Visual-After`.

Research question:

`Q.002` — Does the implementation change alter Output-M under Condition-N?

### 12.1 SOURCE / ENTITY

- `S.DATA.001` = Dataset-X
- `S.LOG.001` = Log-Y
- `S.CODE.001` = Code-Z
- `S.VIS.001` = Visual-Before
- `S.VIS.002` = Visual-After

These are retrievable SOURCE records when their exact content/version matters.

### 12.2 Analytic ACTIVITY

`A.ANALYTICS.001`
TYPE: ACTIVITY
SUBTYPE: DATA_ANALYSIS
USES: S.DATA.001
GENERATES: O.DATA.001

`A.ANALYTICS.002`
TYPE: ACTIVITY
SUBTYPE: LOG_ANALYSIS
USES: S.LOG.001
GENERATES: O.LOG.001

`A.ANALYTICS.003`
TYPE: ACTIVITY
SUBTYPE: CODE_ANALYSIS
USES: S.CODE.001
GENERATES: O.CODE.001

`A.ANALYTICS.004`
TYPE: ACTIVITY
SUBTYPE: VISUAL_COMPARISON
USES: S.VIS.001, S.VIS.002
GENERATES: O.VIS.001

Expected behavior:
- Analytics uses the existing ACTIVITY semantic type.
- DATA_ANALYSIS / LOG_ANALYSIS / CODE_ANALYSIS / VISUAL_COMPARISON may be Plugin-defined subtypes.
- No separate ANALYTICS Core TYPE is required.

### 12.3 OBSERVATION vs interpretation

Example observations:

- `O.DATA.001`: metric M changed from synthetic value A to B under the recorded comparison.
- `O.LOG.001`: event E appears only after the implementation change.
- `O.CODE.001`: branch condition C changed in the compared revision.
- `O.VIS.001`: rendered region R differs above the configured comparison threshold.

None of these observations automatically proves:

`P.003` — The implementation change is the cause of Output-M change under Condition-N.

Causal/support interpretation belongs in ASSESSMENT.

### 12.4 Mixed research closure

Expected closure for `Q.002` may combine:

```text
Q.002
 -> P.003
 -> causal/support ASSESSMENT
 -> O.DATA.001
 -> O.LOG.001
 -> O.CODE.001
 -> O.VIS.001
 -> A.ANALYTICS.001..004
 -> exact SOURCE revisions
 -> literature SOURCE only if external evidence is needed
```

This verifies that one research question may combine analytics and literature without creating separate top-level research systems.

### 12.5 Failure conditions

The schema fails if it:
1. requires a separate Analysis Core to represent these activities,
2. stores interpretation only as raw observation text,
3. treats an analytic output as automatically proving a proposition,
4. cannot combine paper evidence and empirical analytics in one closure,
5. treats every data/code/log/image field as universal Research Core columns.


## 13. Source-backed implementation analysis stress test

A synthetic design/source system is reconstructed into a browser/runtime implementation.

Available evidence:
- exact structural source with nested references and inherited properties,
- generated normalized source model,
- implementation candidate,
- browser runtime output,
- screenshot/reference render,
- two independent renderers with slightly different antialiasing behavior.

Research question:

`Q.003` — Is the observed visual residual caused by a source/implementation defect or by renderer/runtime behavior?

### 13.1 Source closure gate

Before visual comparison:
- descendant/source-reference closure must resolve,
- effective inherited/overridden properties must resolve,
- unresolved dependencies remain explicit,
- deterministic source facts must not be rediscovered from screenshot evidence.

Expected behavior:
- incomplete source closure produces SOURCE_PARTIAL / REVIEW_REQUIRED,
- downstream pixel comparison cannot convert incomplete closure into SOURCE_CLOSED.

### 13.2 Authority separation

Records distinguish:
- original source revision,
- deterministic normalized/derived source representation,
- implementation candidate,
- browser/runtime capture,
- diagnostic diff artifact.

Expected behavior:
- generated reference and screenshot remain validation/diagnostic evidence,
- neither silently replaces the original source as authority.

### 13.3 Runtime fingerprint

A runtime validation ACTIVITY records enough identity to reproduce the observation, including:
- runtime/browser version,
- viewport/input shape,
- device scale or equivalent,
- required resource readiness,
- source/candidate revision.

Expected behavior:
- a result captured before a required resource is ready cannot be promoted to READY merely because static configuration declared that resource.

### 13.4 Localize before correction

A global difference metric fails.

The analysis then localizes:
- page/system,
- region/component,
- source owner,
- primitive/property,
- residual shape.

Expected behavior:
- no global compensating correction is adopted before the defect is bounded,
- a localized blocking defect is not erased by an acceptable global score.

### 13.5 Deterministic gate before perceptual QA

Source-deterministic properties are checked first.

Only remaining residuals are sent to perceptual/rendering analysis.

Expected behavior:
- exact source geometry/material/configuration mismatch is classified before pixel tuning,
- antialiasing/subpixel residual remains a renderer/runtime question when deterministic facts already match.

### 13.6 Triangulation

Two independent renderers disagree slightly near the same edge while source and implementation geometry/material agree.

Expected assessment:
- renderer-specific or toolchain-specific residual may be favored,
- but agreement between derived renderers does not overrule the original source.

### 13.7 Threshold discipline

A comparison threshold fails for one localized region.

Expected behavior:
- threshold is not widened solely to turn FAIL into PASS,
- threshold changes require explicit method rationale and invalidate affected prior comparisons.

### 13.8 Generation coherence

The implementation candidate is compared against a stale reference from another source generation.

Expected behavior:
- comparison result is invalidated,
- the stale metric is not optimized further.

### 13.9 Dedupe vs occurrence identity

Two source occurrences share the same reusable visual/material fingerprint but use different placement/context.

Expected behavior:
- reusable material may be deduplicated,
- occurrence identity and occurrence-level validation remain distinct,
- cache key includes every usage parameter that can alter the result.

### 13.10 Failure conditions

The schema/plugin fails if it:
1. uses screenshot QA to infer source facts that were structurally available,
2. promotes a generated diagnostic artifact to source authority,
3. loses unresolved dependencies during source closure,
4. treats runtime-declared configuration as equivalent to runtime-ready state,
5. applies a global correction before localizing the defect,
6. widens tolerance only to make a failure pass,
7. accepts stale-generation comparison metrics,
8. deduplicates source occurrences together with reusable material,
9. converts UNKNOWN / REVIEW_REQUIRED residuals into implementation defects without evidence.


## 14. Scope-anchor / subset-drift stress test

A synthetic formulation project investigates all candidate raw materials that may activate or support Receptor-R in skin.

### 14.1 Scope Anchor

The anchored universe includes:
- defined small molecules,
- organic acids,
- vitamins,
- fatty acids and lipids,
- fragrance molecules,
- isolated natural products,
- standardized botanical extracts,
- complex cosmetic raw materials.

The project later reviews one publication that screens only botanical extracts.

The publication identifies several interesting botanical hits.

### 14.2 Follow-up request

After reviewing that publication, the user asks:

> Find the actual commercial raw-material names and manufacturers.

Expected behavior:
- resolve the follow-up target from the **full anchored universe**;
- use the botanical publication as one subset/source;
- map commercial suppliers across chemical, lipid, vitamin, fragrance, isolated-natural-product, extract, and complex-material classes;
- optionally run a botanical subset pass, but label it explicitly as such.

Failure behavior:
- treat the publication’s botanical hit list as the new universe;
- return only botanical suppliers while presenting the result as the project-wide supplier map;
- silently classify pure chemicals as “research reagents” and therefore not raw materials;
- use the previous turn’s local list as the authoritative scope without a scope decision.

### 14.3 User correction

The user then says:

> I did not ask to limit this to botanical raw materials.

Expected behavior:
- recognize this as a **scope correction**;
- restore the prior Scope Anchor;
- update durable current-state / issue notes;
- relabel earlier botanical-only output as a subset pass;
- continue future work from the restored full universe.

### 14.4 Failure conditions

The Research Core process fails if it:
1. allows a working subset to silently replace the Scope Anchor,
2. calls a subset pass a full audit,
3. turns a schema/storage category into an exclusion criterion,
4. repeats the same narrower scope after an explicit user correction,
5. fails to persist the corrected scope in durable project state.

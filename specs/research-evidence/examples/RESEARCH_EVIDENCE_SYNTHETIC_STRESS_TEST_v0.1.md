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

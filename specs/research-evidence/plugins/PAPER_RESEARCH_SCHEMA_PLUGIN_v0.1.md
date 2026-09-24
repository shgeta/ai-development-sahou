# Paper Research Schema Plugin v0.1

- Updated: 2026-09-24
- Status: CANDIDATE
- Plugin ID: RESEARCH_EVIDENCE.PAPER
- Target Core: Research Evidence Core Schema v0.1
- Scope: journal articles, conference papers/abstracts, theses/dissertations, preprints, systematic reviews, and related scholarly-source research
- Decision history: ai-development-sahou Issue #17

## 1. Purpose

This plugin extends Research Evidence Core for paper/literature research without contaminating Core with literature-specific fields.

It supports:
- bibliographic identity
- study design and cohort/sample detail
- author/affiliation/provenance
- publication lineage and overlap
- outcome/result extraction
- source access state
- legitimate free full-text retrieval trail
- purchase-candidate derivation
- risk-of-bias / directness / independence assessment
- systematic-review/search reproducibility

## 2. Applicable Core types

The plugin extends:
- SOURCE
- ENTITY
- ACTIVITY
- OBSERVATION
- QUESTION
- ASSESSMENT
- RELATION

PROPOSITION normally uses Core semantics without mandatory paper-specific fields.

## 3. SOURCE extensions

Recommended SOURCE subtypes:
- JOURNAL_ARTICLE
- CONFERENCE_PAPER
- CONFERENCE_ABSTRACT
- PREPRINT
- THESIS
- DISSERTATION
- REVIEW_ARTICLE
- SYSTEMATIC_REVIEW
- META_ANALYSIS
- CORRECTION
- RETRACTION_NOTICE

Bibliographic fields:
- DOI
- PMID
- PMCID
- TITLE_CANONICAL
- JOURNAL
- YEAR
- VOLUME
- ISSUE
- PAGES_OR_ARTICLE_NUMBER
- PUBLISHER
- LANGUAGE
- PUBLICATION_DATE
- RETRACTION_STATUS

Version fields:
- VERSION_TYPE = VERSION_OF_RECORD | ACCEPTED_MANUSCRIPT | PREPRINT | AUTHOR_MANUSCRIPT | OTHER
- VERSION_OF_SOURCE_ID
- CONTENT_EQUIVALENCE = SAME | SUBSTANTIALLY_SAME | DIFFERENT | UNKNOWN

Access summary fields are derived where possible and MUST NOT erase access-check history.

## 4. ENTITY extensions

Recommended ENTITY subtypes:
- PERSON
- ORGANIZATION
- POPULATION
- SPECIMEN
- INTERVENTION
- EXPOSURE
- COMPARATOR
- OUTCOME
- METHOD
- INSTRUMENT

Author/affiliation relations:
- SOURCE AUTHORED_BY ENTITY(PERSON)
- ENTITY(PERSON) AFFILIATED_WITH ENTITY(ORGANIZATION)
- SOURCE FUNDED_BY ENTITY(ORGANIZATION)
- SOURCE MATERIAL_PROVIDED_BY ENTITY(ORGANIZATION)
- SOURCE CONFLICT_DISCLOSURE_ABOUT ENTITY

Author/organization identity normalization SHOULD preserve aliases and name changes without multiplying entities.

## 5. ACTIVITY extensions

Recommended ACTIVITY subtypes:
- RCT
- NONRANDOMIZED_TRIAL
- OBSERVATIONAL_STUDY
- COHORT_STUDY
- CASE_CONTROL
- CROSS_SECTIONAL
- CASE_SERIES
- IN_VITRO_EXPERIMENT
- EX_VIVO_EXPERIMENT
- ANIMAL_EXPERIMENT
- ANALYTICAL_ASSAY
- COMPUTATIONAL_ANALYSIS
- SYSTEMATIC_SEARCH
- SCREENING
- DATA_EXTRACTION
- META_ANALYSIS_ACTIVITY
- PAPER_ACCESS_CHECK

Study/execution fields MAY include:
- STUDY_DESIGN
- STUDY_SITE
- RECRUITMENT_START
- RECRUITMENT_END
- SAMPLE_SIZE_PLANNED
- SAMPLE_SIZE_ANALYZED
- RANDOMIZATION
- BLINDING
- ANALYSIS_SET
- FOLLOWUP_DURATION

Domain-specific detail such as clinical PICO SHOULD be supplied by further compatible plugins/profile fields rather than promoted to Paper Core unless universally useful.

## 6. OBSERVATION extensions

Recommended fields:
- ENDPOINT_REF
- POPULATION_OR_SAMPLE_REF
- INTERVENTION_OR_EXPOSURE_REF
- COMPARATOR_REF
- TIMEPOINT
- VALUE
- UNIT
- EFFECT_MEASURE
- UNCERTAINTY_INTERVAL
- P_VALUE
- DIRECTION
- RESULT_FORM = QUANTITATIVE | QUALITATIVE | NULL | NEGATIVE | NONSIGNIFICANT | NOT_ESTIMABLE
- ANALYSIS_SET
- REPORTED_LOCATION

NOT_REPORTED and NOT_MEASURED MUST remain distinguishable.

## 7. ASSESSMENT extensions

Recommended ASSESSMENT_TYPE values:
- CLAIM_SUPPORT
- CONTRADICTION
- RISK_OF_BIAS
- INDEPENDENCE
- DIRECTNESS
- APPLICABILITY
- DUPLICATION
- COHORT_OVERLAP
- PUBLICATION_LINEAGE
- REPORTING_COMPLETENESS
- SOURCE_AUTHORITY
- EVIDENCE_GAP
- BODY_OF_EVIDENCE_CERTAINTY

Do not use one universal QUALITY_SCORE.

Framework-specific assessments SHOULD declare:
- FRAMEWORK
- FRAMEWORK_VERSION
- DOMAIN
- JUDGMENT
- RATIONALE

Examples:
- RoB 2 domain judgment
- GRADE certainty at outcome/body-of-evidence level

## 8. Research question extensions

QUESTION MAY carry:
- QUESTION_SCOPE
- DATE_WINDOW
- LANGUAGE_SCOPE
- INCLUSION_RULE_REF
- EXCLUSION_RULE_REF

PICO fields SHOULD be added only when a clinical-question profile/plugin is active.

## 9. Publication lineage and non-independence

Recommended relations:
- SOURCE PREPRINT_OF SOURCE
- SOURCE PUBLISHED_VERSION_OF SOURCE
- SOURCE EXTENDS SOURCE
- SOURCE SECONDARY_ANALYSIS_OF SOURCE
- SOURCE REPORTS_SAME_COHORT_AS SOURCE
- SOURCE POSSIBLY_OVERLAPS_WITH SOURCE
- SOURCE CORRECTED_BY SOURCE
- SOURCE RETRACTED_BY SOURCE

Publication count MUST NOT be used as independent-evidence count without resolving relevant duplication/cohort-overlap assessments.

## 10. Free full-text retrieval trail

A publisher paywall alone MUST NOT establish that no free full text exists.

Use ACTIVITY subtype:
- PAPER_ACCESS_CHECK

Required fields:
- TARGET_SOURCE_ID
- ROUTE_TYPE
- RESULT
- CHECKED_AT

Recommended ROUTE_TYPE:
- PUBLISHER_OA
- PMC_OR_DOMAIN_REPOSITORY
- INSTITUTIONAL_REPOSITORY
- AUTHOR_MANUSCRIPT
- PREPRINT_SERVER
- DOI_OA_DISCOVERY
- LIBRARY_CATALOG
- OTHER_LEGITIMATE_FREE_ROUTE

RESULT:
- FULL_TEXT_FOUND
- ABSTRACT_ONLY
- METADATA_ONLY
- NOT_FOUND
- ACCESS_BLOCKED
- VERSION_MISMATCH
- RETRACTED_OR_SUPERSEDED

Optional:
- ACCESS_URL_OR_REF
- VERSION_TYPE
- LICENSE
- NOTE

## 11. Derived source access state

Source-level ACCESS_STATE SHOULD be derived from access-check activities where possible.

Recommended values:
- FREE_FULL_TEXT_VERIFIED
- FREE_ALTERNATE_VERSION_VERIFIED
- ABSTRACT_ONLY
- METADATA_ONLY
- PAYWALLED_AFTER_FREE_ROUTE_CHECK
- FREE_ROUTE_SEARCH_INCOMPLETE
- UNAVAILABLE
- ACCESS_BLOCKED

Rules:
- PAYWALLED_AFTER_FREE_ROUTE_CHECK MUST NOT be inferred solely from a paywalled publisher page.
- FREE_FULL_TEXT_VERIFIED requires a retrievable full text matching the target source/version or an explicitly accepted alternate version.
- VERSION_MISMATCH does not satisfy exact-version full-text closure.
- CHECKED_AT is required because access availability can change.

## 12. Purchase candidate

PURCHASE_CANDIDATE is a derived assessment/state, not a Core SOURCE subtype.

A paper MAY become a purchase candidate when:
1. its evidence value is material to an unresolved QUESTION/PROPOSITION,
2. exact or adequate full text has not been obtained,
3. configured legitimate free-route closure has been attempted or explicitly waived,
4. abstract/metadata are insufficient for the required evidence closure.

Recommended ASSESSMENT_TYPE:
- PURCHASE_NECESSITY

Recommended fields:
- TARGET_SOURCE_ID
- PRIORITY = HIGH | MEDIUM | LOW
- REASON
- NEEDED_FOR
- FREE_ROUTE_CLOSURE_STATUS
- EXPECTED_DECISION_IMPACT
- KNOWN_PRICE
- PRICE_CURRENCY
- PRICE_CHECKED_AT

Known price is optional and MUST NOT be invented.

## 13. Paper access closure

For a source needed at full-text level:

SOURCE
  -> PAPER_ACCESS_CHECK activities
  -> legitimate route results
  -> version identity
  -> access state
  -> if unresolved and material: PURCHASE_NECESSITY assessment

A source MUST remain FREE_ROUTE_SEARCH_INCOMPLETE when required configured routes have not been checked.

## 14. Search reproducibility

For systematic or high-value literature searches, ACTIVITY subtype SYSTEMATIC_SEARCH SHOULD preserve:
- QUESTION_ID
- DATABASE_OR_INDEX
- SEARCH_STRING_OR_QUERY_REF
- DATE_SEARCHED
- DATE_COVERAGE
- FILTERS
- RESULT_COUNT
- DEDUPLICATION_METHOD
- SCREENING_ACTIVITY_REF

Routine exploratory web searches MAY remain in Work Item history unless project policy promotes them into durable evidence records.

## 15. Study identity boundary

One paper MAY report multiple ACTIVITY records.

Split ACTIVITY when:
- distinct cohort/sample
- distinct protocol
- distinct experiment
- distinct analytic population
- distinct assay with independently interpretable results

Do not split merely because a paper has multiple endpoints if one protocol/execution unit produced them; those normally become multiple OBSERVATION records.

## 16. Observation identity boundary

Split OBSERVATION when any of these materially changes:
- endpoint
- comparison
- dose/exposure
- timepoint
- population/sample stratum
- analysis set
- effect estimate/value

This makes result-level bias/directness assessment possible.

## 17. Source assertion handling

Statements in abstract/discussion/conclusion SHOULD be represented as PROPOSITIONs asserted by SOURCE when they matter to the research question.

They MUST NOT be converted into OBSERVATION unless the underlying activity/result is actually available and extracted.

## 18. Minimal paper evidence closure

For a proposition based on a paper:

PROPOSITION
  -> support/contradiction ASSESSMENT
  -> OBSERVATION
  -> ACTIVITY
  -> SOURCE
  -> author/organization provenance needed for independence
  -> relevant risk-of-bias/directness/duplication assessments
  -> access/version status when full-text sufficiency matters

## 19. Validation

At minimum validate:
- DOI/PMID/PMCID identifiers are not treated as separate source identities by default
- publication versions are linked when known
- paper count is not silently used as independent evidence count
- abstract-only access is not represented as full-text access
- publisher paywall is not equivalent to no legitimate free version
- NOT_REPORTED != NOT_MEASURED != NOT_RETRIEVED
- source conclusion text is not silently promoted to empirical observation
- result-level assessments can target specific OBSERVATION records
- purchase candidates are traceable to free-route search history
- systematic-search records preserve enough query/date/source information for reconstruction when required

## 20. Compatibility

This plugin may coexist with:
- clinical research plugin
- toxicology plugin
- analytical chemistry plugin
- regulatory evidence plugin

Those plugins may add further domain semantics without redefining Paper Plugin fields.

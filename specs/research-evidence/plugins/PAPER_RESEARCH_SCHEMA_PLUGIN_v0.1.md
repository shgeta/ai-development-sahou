# Paper Research Schema Plugin v0.1

- Updated: 2026-09-24
- Status: CANDIDATE
- Plugin ID: RESEARCH_EVIDENCE.PAPER
- Target Core: Research Evidence Core Schema v0.1
- Scope: scholarly-source identity, publication relations, literature-search provenance, access/retrieval, paper-level evidence extraction, and publication independence/lineage
- Decision history: ai-development-sahou Issue #17

## 1. Purpose

Paper Research Plugin extends Research Evidence Core only for semantics that arise from researching scholarly literature.

It covers:
- scholarly-source identity and identifiers,
- authorship / affiliation / funding provenance,
- publication-version and update relations,
- literature-search and screening activities,
- paper access and legitimate free-full-text retrieval,
- extraction location/provenance,
- publication lineage / overlap / independence,
- purchase-candidate assessment.

It does NOT own domain-specific scientific semantics such as:
- clinical PICO,
- RCT randomization/blinding detail,
- toxicology endpoints,
- analytical-chemistry conditions,
- animal-model fields,
- regulatory jurisdiction rules.

Those belong in compatible domain plugins.

## 2. Applicable Core types

This plugin may extend:
- SOURCE
- ENTITY
- ACTIVITY
- OBSERVATION
- QUESTION
- ASSESSMENT
- RELATION

PROPOSITION normally uses Core semantics unchanged.

## 3. Scholarly SOURCE identity

### 3.1 SOURCE_KIND

Recommended scholarly SOURCE_KIND values:
- JOURNAL_ARTICLE
- CONFERENCE_PAPER
- CONFERENCE_ABSTRACT
- PREPRINT
- THESIS
- DISSERTATION
- BOOK_CHAPTER
- REPORT
- CORRECTION_NOTICE
- RETRACTION_NOTICE
- OTHER_SCHOLARLY_SOURCE

`SYSTEMATIC_REVIEW`, `META_ANALYSIS`, `RCT`, `IN_VITRO` and similar research methods are NOT SOURCE_KIND values.
They describe ACTIVITY or a domain plugin's study design.

### 3.2 Bibliographic identifiers

Do not create one universal column per identifier system.

Use repeatable identifier records/values:

- IDENTIFIER_SCHEME
- IDENTIFIER_VALUE

Common schemes:
- DOI
- PMID
- PMCID
- ISBN
- ISSN
- HANDLE
- ARK
- INSTITUTIONAL_ID
- OTHER

Multiple identifiers may identify the same SOURCE.
DOI / PMID / PMCID MUST NOT be treated as separate SOURCE identities merely because the identifier schemes differ.

Normalization rules:
- DOI comparisons are case-insensitive after DOI normalization.
- identifier display formatting does not change SOURCE identity.
- raw identifier text MAY be retained by an Adapter or ingestion plugin.

### 3.3 Bibliographic description fields

Optional paper-level fields:
- TITLE
- CONTAINER_TITLE
- PUBLISHED_DATE
- VOLUME
- ISSUE
- LOCATOR
- LANGUAGE

`LOCATOR` may hold pages or article number.

`YEAR` is derived from PUBLISHED_DATE when the latter is available and SHOULD NOT be a second semantic authority.

Publisher is preferably represented as an ENTITY relation rather than a repeated free-text publisher field.

### 3.4 SOURCE identity boundary

Treat the following as the same SOURCE:
- HTML and PDF locators for the same content version,
- multiple repository/publisher locations serving the same exact content version,
- alternate identifier schemes pointing to the same scholarly source.

Treat materially different content versions as distinct SOURCE records and link them:
- preprint vs version of record,
- accepted manuscript vs version of record,
- translated version when content identity is not exact,
- correction/retraction notice vs affected paper.

If version identity is uncertain, do not merge; use an explicit uncertain lineage ASSESSMENT.

## 4. Publication/version relations

Recommended relation predicates:
- SOURCE PREPRINT_OF SOURCE
- SOURCE MANUSCRIPT_OF SOURCE
- SOURCE VERSION_OF SOURCE
- SOURCE TRANSLATION_OF SOURCE
- SOURCE DERIVED_FROM SOURCE
- SOURCE COMMENT_ON SOURCE
- SOURCE SUPPLEMENTS SOURCE
- SOURCE CORRECTS SOURCE
- SOURCE RETRACTS SOURCE
- SOURCE REPLACES SOURCE

These are aligned where practical with established scholarly relation vocabularies such as Crossref relations.

Version relation does not itself imply identical content.

When useful, attach a publication-lineage ASSESSMENT with:
- EQUIVALENCE = IDENTICAL | SUBSTANTIALLY_SAME | PARTIAL | DIFFERENT | UNKNOWN
- RATIONALE

## 5. Contributor and organization provenance

Recommended ENTITY kinds used by this plugin:
- PERSON
- ORGANIZATION

Recommended relations:
- SOURCE AUTHORED_BY PERSON
- SOURCE EDITED_BY PERSON
- SOURCE PUBLISHED_BY ORGANIZATION
- SOURCE FUNDED_BY ORGANIZATION
- SOURCE MATERIAL_PROVIDED_BY ORGANIZATION

Authorship relation qualifiers MAY include:
- CONTRIBUTOR_ORDER
- CORRESPONDING = true|false|unknown
- AFFILIATION_ENTITY_IDS
- RAW_AFFILIATION_TEXT

Affiliation is source-contextual.
Do NOT infer a person's timeless affiliation from one paper.

Author and organization identity normalization SHOULD preserve aliases, language variants, initials, and name changes without multiplying entities when identity is established.

## 6. Paper-research ACTIVITY kinds

Paper Plugin defines only literature-research-specific activities:

- LITERATURE_SEARCH
- SCREENING
- DATA_EXTRACTION
- PAPER_ACCESS_CHECK

Scientific study/experiment design belongs to domain plugins or Core ACTIVITY plus domain semantics.

A SOURCE may report one or many scientific ACTIVITY records even when Paper Plugin itself does not define their scientific subtype.

## 7. Literature search

### 7.1 LITERATURE_SEARCH fields

Recommended fields:
- QUESTION_ID
- SEARCH_TARGET_REF
- QUERY_TEXT_OR_REF
- SEARCHED_AT
- DATE_COVERAGE
- FILTERS
- RESULT_COUNT

Recommended relations:
- ACTIVITY DISCOVERED SOURCE
- ACTIVITY USED SOURCE_OR_ENTITY

`SEARCH_TARGET_REF` may identify a bibliographic database, search engine, repository, registry, or catalog.

High-value/systematic searches SHOULD preserve enough query/date/target detail to reconstruct the search.

Routine exploratory searches MAY remain only in Work Item history unless project policy promotes them into durable evidence.

### 7.2 Absence-of-evidence rule

"Nothing was found" is not timeless evidence.

Represent it as:
- bounded LITERATURE_SEARCH activity,
- search-result observation,
- optional EVIDENCE_GAP assessment.

Its meaning is bounded by query, target, filters, coverage, and SEARCHED_AT.

## 8. Screening and extraction

### 8.1 SCREENING

Recommended fields:
- QUESTION_ID
- STAGE = TITLE_ABSTRACT | FULL_TEXT | OTHER
- DECISION = INCLUDE | EXCLUDE | UNCERTAIN
- REASON

Screening decisions apply to SOURCE records and are question-specific.

### 8.2 DATA_EXTRACTION

Use DATA_EXTRACTION when durable provenance is needed for how paper content was converted into evidence records.

Recommended fields:
- TARGET_SOURCE_ID
- EXTRACTED_AT
- EXTRACTION_SCOPE

Recommended relations:
- DATA_EXTRACTION GENERATED OBSERVATION
- DATA_EXTRACTION GENERATED PROPOSITION
- DATA_EXTRACTION USED SOURCE

Extraction activity does not make the extracted statement true; it records extraction provenance.

## 9. OBSERVATION fields for paper extraction

Paper Plugin adds only source-reporting fields, not domain endpoint schemas.

Optional fields:
- OBSERVATION_FORM = QUANTITATIVE | QUALITATIVE | CATEGORICAL | TEXTUAL | NOT_ESTIMABLE
- VALUE
- UNIT
- STATISTIC_TYPE
- UNCERTAINTY_INTERVAL
- P_VALUE
- SOURCE_LOCATOR

`SOURCE_LOCATOR` may point to page, section, table, figure, supplement, paragraph anchor, or equivalent retrievable location.

Endpoint, exposure, comparator, specimen, population, timepoint, assay method, dose and similar scientific semantics belong in domain plugins or explicit ENTITY/RELATION structures.

`NEGATIVE`, `NONSIGNIFICANT`, and `SUPPORTIVE` are not OBSERVATION_FORM values because they embed interpretation.

NOT_REPORTED and NOT_MEASURED MUST remain distinguishable from an observed null result.

## 10. Source assertion handling

When an abstract/discussion/conclusion statement matters to the research question:
- represent its content as a PROPOSITION,
- link `SOURCE ASSERTS PROPOSITION`.

Do NOT convert the source's conclusion directly into OBSERVATION unless the underlying reported result was actually extracted.

A review article repeating another source's interpretation remains a source assertion until the underlying evidence is resolved.

## 11. Paper-related ASSESSMENT kinds

Recommended ASSESSMENT_TYPE values:
- CLAIM_SUPPORT
- DIRECTNESS
- APPLICABILITY
- RISK_OF_BIAS
- INDEPENDENCE
- DUPLICATION
- COHORT_OVERLAP
- PUBLICATION_LINEAGE
- REPORTING_COMPLETENESS
- ACCESS_SUFFICIENCY
- PURCHASE_NECESSITY
- EVIDENCE_GAP

Do NOT define one universal QUALITY_SCORE.

Framework-specific assessment fields MAY include:
- FRAMEWORK
- FRAMEWORK_VERSION
- DOMAIN
- JUDGMENT
- RATIONALE

Domain-specific frameworks such as clinical RoB or GRADE SHOULD normally be supplied by a compatible domain plugin; Paper Plugin only provides the assessment attachment pattern.

## 12. Publication lineage and non-independence

Publication count MUST NOT be used as independent-evidence count.

Recommended relations/assessments:
- SOURCE PREPRINT_OF SOURCE
- SOURCE MANUSCRIPT_OF SOURCE
- SOURCE DERIVED_FROM SOURCE
- SOURCE SECONDARY_ANALYSIS_OF SOURCE
- SOURCE REPORTS_SAME_COHORT_AS SOURCE
- SOURCE POSSIBLY_OVERLAPS_WITH SOURCE
- ASSESSMENT type PUBLICATION_LINEAGE
- ASSESSMENT type COHORT_OVERLAP
- ASSESSMENT type INDEPENDENCE

Use explicit uncertainty where raw-data identity is not established.

## 13. Full-text access and free-route search

### 13.1 Principle

A paywalled publisher page does not establish that no legitimate free full text exists.

Paper access is a search/retrieval problem with history.

### 13.2 PAPER_ACCESS_CHECK

Required:
- TARGET_SOURCE_ID
- ROUTE_TYPE
- RESULT
- CHECKED_AT

Recommended ROUTE_TYPE:
- PUBLISHER
- DOMAIN_REPOSITORY
- INSTITUTIONAL_REPOSITORY
- AUTHOR_MANUSCRIPT
- PREPRINT_SERVER
- OA_DISCOVERY_SERVICE
- LIBRARY_CATALOG
- OTHER_LEGITIMATE_ROUTE

Recommended RESULT:
- EXACT_FULL_TEXT_FOUND
- ALTERNATE_VERSION_FOUND
- ABSTRACT_ONLY
- METADATA_ONLY
- PAYWALL
- NOT_FOUND
- ACCESS_BLOCKED
- VERSION_MISMATCH
- RETRACTED_OR_SUPERSEDED

Optional:
- FOUND_SOURCE_ID
- LOCATOR_URL_OR_REF
- LICENSE
- RIGHTS_STATUS = VERIFIED_OPEN | VERIFIED_AUTHORIZED | UNKNOWN | RESTRICTED
- NOTE

If an alternate manuscript/preprint is found and has materially distinct content/version identity, create a SOURCE for it and set FOUND_SOURCE_ID.

A publicly reachable third-party copy with `RIGHTS_STATUS = UNKNOWN` MAY establish that content was technically inspected, but it MUST NOT by itself satisfy a policy requiring a legitimate/open full-text route. Access availability and rights/authorization are separate semantics.

### 13.3 Access location vs SOURCE identity

Multiple URLs/locations serving the same exact version do not require multiple SOURCE records.

Different scholarly versions do require distinct SOURCE records when their content version materially differs.

This allows:
- one SOURCE = version of record,
- one SOURCE = accepted manuscript,
- relation = MANUSCRIPT_OF,
- many access locations without duplicating the source identity.

## 14. Derived access state

Access state is derived convenience data and MUST NOT erase access-check history.

Recommended derived states:
- EXACT_FULL_TEXT_AVAILABLE
- ALTERNATE_FULL_TEXT_AVAILABLE
- ABSTRACT_ONLY
- METADATA_ONLY
- NO_FREE_FULL_TEXT_FOUND
- FREE_ROUTE_SEARCH_INCOMPLETE
- ACCESS_BLOCKED
- UNAVAILABLE

Do NOT use a single PAYWALLED state as the work-level conclusion because publisher paywall and free repository availability can coexist.

A project's access policy defines which free routes are required for closure.
Paper Plugin does not hard-code that every project must check every possible route.

## 15. Purchase candidate

Purchase need is an ASSESSMENT, not a SOURCE kind.

Use:
- ASSESSMENT_TYPE = PURCHASE_NECESSITY

Recommended fields:
- TARGET_SOURCE_ID
- PRIORITY = HIGH | MEDIUM | LOW
- REASON
- NEEDED_FOR
- NEEDED_CONTENT
- FREE_ROUTE_CLOSURE_STATUS
- EXPECTED_DECISION_IMPACT
- KNOWN_PRICE
- PRICE_CURRENCY
- PRICE_CHECKED_AT

Rules:
1. evidence value must be material to an unresolved QUESTION or PROPOSITION,
2. adequate full text is not already available,
3. configured legitimate free-route closure has been attempted or explicitly waived,
4. metadata/abstract/alternate version is insufficient for the required evidence closure.

Known price is optional and MUST NOT be invented.

## 16. Access closure

For a scholarly source needed at full-text level:

```text
SOURCE
  -> PAPER_ACCESS_CHECK activities
  -> access locations / FOUND_SOURCE_ID
  -> publication-version relations
  -> derived access state
  -> ACCESS_SUFFICIENCY assessment
  -> PURCHASE_NECESSITY assessment if still required
```

If the active access-policy route set is incomplete:
- derived state = FREE_ROUTE_SEARCH_INCOMPLETE.

If an alternate free version fully satisfies the evidence need:
- purchase necessity should normally be absent or NOT_NEEDED.

## 17. QUESTION extensions

Optional literature-research fields:
- DATE_WINDOW
- LANGUAGE_SCOPE
- INCLUSION_RULE_REF
- EXCLUSION_RULE_REF
- ACCESS_POLICY_REF

Clinical PICO is not defined here.

## 18. Scientific ACTIVITY identity from papers

One SOURCE may report multiple scientific ACTIVITY records.

Split scientific ACTIVITY when the execution/reproducibility unit materially changes, for example:
- different cohort/sample set,
- different experimental protocol,
- separate assay/analysis,
- distinct study phase,
- independent analytic population.

Do not split solely because one activity produced multiple endpoints; those can be separate OBSERVATION records.

Specific study-design fields belong to domain plugins.

## 19. Paper evidence closure

For a proposition whose evidence is reported in scholarly literature:

```text
PROPOSITION
  -> relevant ASSESSMENT
  -> OBSERVATION
  -> scientific ACTIVITY
  -> reporting SOURCE
  -> publication-version relation if relevant
  -> contributor/organization provenance only when needed
  -> lineage/duplication/independence assessments only when needed
  -> access/extraction provenance only when sufficiency depends on it
```

Do not automatically load every author, affiliation, citation, or access check when it is irrelevant to the current evidence question.

## 20. NOTE / remarks policy

Paper Plugin MAY use free-form NOTE fields for irregular details that do not affect evidence semantics.

Examples appropriate for NOTE:
- unusual formatting or OCR/display quirks,
- incidental retrieval comments,
- one-off contextual detail that does not affect identity, closure, comparison, or assessment.

Examples that MUST NOT exist only in NOTE when they matter to the task:
- a free full-text route that changes access sufficiency,
- suspected cohort overlap or publication duplication,
- a source location required to verify an extracted result,
- a version mismatch,
- a reason a source is included/excluded,
- a fact needed to determine purchase necessity.

Promotion rule:
when the same kind of information repeatedly appears in NOTE and is being used for search, filtering, comparison, closure, validation, or decisions, treat that repetition as evidence that the concept should be promoted into a structured Paper Plugin field/relation/assessment in a schema-evolution change.

## 21. Validation

Validate at least:
- multiple identifiers may map to one SOURCE
- identifier scheme differences do not create duplicate sources
- materially different publication versions are linked, not silently merged
- HTML/PDF locations of the same exact version are not duplicated as separate sources
- systematic review / meta-analysis are not confused with SOURCE_KIND
- source conclusion text is not silently promoted to OBSERVATION
- NOT_REPORTED != NOT_MEASURED != null/zero result
- publisher PAYWALL does not imply NO_FREE_FULL_TEXT_FOUND
- alternate-version access is distinguished from exact-version access
- purchase necessity traces to access-check closure and an unresolved evidence need
- publication count is not treated as independent-evidence count
- source-contextual affiliation is not inferred as timeless person affiliation
- search "no result" statements remain bounded by search activity/date/query
- paper-specific fields do not require clinical/toxicology/chemistry semantics

## 22. Compatibility

Paper Plugin may coexist with domain plugins such as:
- Clinical Research
- Toxicology
- Analytical Chemistry
- Regulatory Evidence
- Product/Vehicle Research

Those plugins may define scientific study design, endpoint, exposure, dose, model, and assessment vocabularies without redefining Paper Plugin source/access/publication semantics.

# Raw Material Research Schema Plugin v0.1

- Updated: 2026-09-29
- Status: CANDIDATE
- Plugin ID: RESEARCH_EVIDENCE.CHEMICAL.RAW_MATERIAL
- Target Core: Research Evidence Core Schema v0.1
- Parent Plugin: RESEARCH_EVIDENCE.CHEMICAL
- Required Dependency: Chemical Research Schema Plugin v0.1
- Parent work model: Research Core v0.1
- Scope: intended raw-material function, formulation use, functional consequence of chemical transformation, regulatory applicability, sourcing, supplier/specification evidence, and commercial interpretation
- Decision history: ai-development-sahou Issue #24

## 1. Purpose

Raw Material Research Plugin extends Chemical Research for questions where a chemical substance or mixture is being evaluated **as a usable raw material**.

It answers questions such as:
- What function is the material intended to provide?
- Which chemical species or structural features are relevant to that intended function?
- Does a chemical transformation preserve, release, reduce, or destroy the intended function?
- Is the material usable in the target formulation/process?
- What use level, vehicle, storage, processing, or compatibility constraints apply?
- What regulatory or supplier evidence affects use?
- Is the material commercially available, from whom, at what specification, and under what dated commercial conditions?
- Which commercial statements are supported by scientific evidence, supplier evidence, or remain unverified?

This Plugin does not redefine chemical facts.
Chemical identity, transformation, degradation, species balance, and structural-motif retention remain owned by Chemical Research.

## 2. Dependency hierarchy

Required dependency closure:

```text
Research Core
  -> Research Evidence Core
       -> Chemical Research Plugin
            -> Raw Material Research Plugin
```

When Raw Material Research is selected:
- load Chemical Research Plugin,
- then load Raw Material Research Plugin,
- then load Paper / Analysis / other domain plugins only as required by the task.

When only Chemical Research is needed:
- do not load Raw Material Research.

Physical folder nesting is convenience only. `Parent Plugin` and `Required Dependency` are semantic authority.

## 3. Design principles

1. Intended function is use-context dependent and belongs here, not in Chemical Research.
2. A chemical transformation may be "degradation" chemically while still preserving or releasing a functionally relevant species.
3. Functional consequence MUST be assessed from chemical evidence plus appropriate biological/technical/function evidence.
4. Structural motif retention alone does not prove function retention.
5. Supplier claims MUST remain supplier claims unless independently supported.
6. Commercial attractiveness MUST remain distinct from scientific truth.
7. Formulation compatibility MUST be condition-specific.
8. Regulatory applicability MUST be jurisdiction-, product-type-, use-level-, and date-specific.
9. Availability, price, MOQ, lead time, and supplier status are time-bounded observations.
10. Raw-material assessment MUST NOT overwrite conflicting or unfavorable chemical evidence.

## 4. Applicable Core types

This Plugin may extend:
- ENTITY
- SOURCE
- ACTIVITY
- OBSERVATION
- QUESTION
- ASSESSMENT
- RELATION

PROPOSITION normally uses Core semantics unchanged.

## 5. Raw-material ENTITY semantics

Recommended ENTITY_KIND values:
- RAW_MATERIAL_PRODUCT
- RAW_MATERIAL_GRADE
- FORMULATION_USE_CONTEXT
- INTENDED_FUNCTION
- COMMERCIAL_OFFER

Chemical species remain CHEMICAL_SPECIES from Chemical Research.
Supplier/manufacturer organizations use Core/Paper organization semantics where applicable.

A RAW_MATERIAL_PRODUCT may contain:
- one chemical species,
- multiple chemical species,
- carrier/solvent,
- stabilizer,
- blend,
- botanical or biological fraction,
- unspecified proprietary components.

Do not equate product identity with a single chemical species unless composition evidence supports it.

### 5.1 Mixtures, extracts, and incompletely characterized materials

Raw Material Research is **not limited to pure or fully structurally resolved substances**.

A RAW_MATERIAL_PRODUCT may be:
- a defined single chemical,
- a defined mixture,
- a botanical/mineral/fermentation extract,
- a fraction,
- a carrier-containing active,
- a proprietary blend,
- or a material whose composition is only partially characterized.

Chemical Research dependency means that known chemical identity/composition evidence is represented with chemical semantics when available. It does **not** require complete molecular resolution before raw-material research may proceed.

For incompletely characterized materials:
- represent the material/product identity at the raw-material level,
- represent known composition as CHEMICAL_SPECIES / CHEMICAL_MIXTURE where supported,
- keep unresolved composition explicit as UNKNOWN / NOT_IDENTIFIED / partially characterized,
- do not invent a single active species merely to satisfy the Chemical dependency.

A botanical or complex mixture MUST NOT be excluded from a raw-material candidate universe solely because it is not a pure compound.

## 6. Product-to-chemical relations

Recommended relations:
- RAW_MATERIAL_PRODUCT CONTAINS CHEMICAL_SPECIES
- RAW_MATERIAL_PRODUCT SPECIFIED_AS RAW_MATERIAL_GRADE
- RAW_MATERIAL_PRODUCT SUPPLIED_BY ORGANIZATION
- RAW_MATERIAL_PRODUCT MANUFACTURED_BY ORGANIZATION
- RAW_MATERIAL_PRODUCT HAS_INTENDED_FUNCTION INTENDED_FUNCTION
- RAW_MATERIAL_PRODUCT USED_IN_CONTEXT FORMULATION_USE_CONTEXT
- RAW_MATERIAL_PRODUCT FUNCTION_MEDIATED_BY CHEMICAL_SPECIES
- RAW_MATERIAL_PRODUCT FUNCTION_RELATED_TO STRUCTURAL_MOTIF

`FUNCTION_MEDIATED_BY` requires an evidentiary basis.
Do not infer it from marketing copy alone.

## 7. Intended function

### 7.1 Principle

Intended function expresses **why the material is being evaluated or used**.

Examples:
- pigmentation reduction,
- moisturization,
- antioxidant function,
- preservative support,
- UV attenuation,
- viscosity control,
- emulsification,
- odor masking,
- barrier support.

The same chemical material may have different intended functions in different use contexts.

Therefore intended function SHOULD be linked to a QUESTION or FORMULATION_USE_CONTEXT rather than treated as a timeless intrinsic property.

### 7.2 Recommended fields

- INTENDED_FUNCTION_ID
- USE_CONTEXT_ID
- TARGET_PRODUCT_TYPE
- TARGET_TISSUE_OR_SYSTEM
- TARGET_OUTCOME
- FUNCTION_PRIORITY
- FUNCTION_EVIDENCE_SCOPE

`FUNCTION_PRIORITY` may be used for project prioritization but is not scientific evidence.

## 8. Functional consequence of chemical transformation

### 8.1 Principle

Chemical transformation and raw-material functional consequence are separate semantic layers.

Example:

```text
DERIVATIVE-X -> REFERENCE-A
```

Chemical Research:
- DERIVATIVE-X decreased,
- REFERENCE-A increased,
- motif status measured/inferred.

Raw Material Research:
- assess what this means for the selected intended function.

### 8.2 Recommended ASSESSMENT_TYPE

- FUNCTIONAL_CONSEQUENCE_OF_TRANSFORMATION

Recommended judgments:
- FUNCTION_RELEASED
- FUNCTION_RETAINED
- FUNCTION_PARTIALLY_RETAINED
- FUNCTION_ENHANCED
- FUNCTION_REDUCED
- FUNCTION_LOST
- FUNCTION_CHANGED
- UNKNOWN
- NOT_APPLICABLE

Do not assign these from chemical species balance alone when function evidence is required.

### 8.3 Evidence basis

Recommended fields:
- TARGET_TRANSFORMATION_ACTIVITY_ID
- INTENDED_FUNCTION_ID
- FUNCTIONALLY_RELEVANT_SPECIES_IDS
- FUNCTIONALLY_RELEVANT_MOTIF_IDS
- FUNCTION_EVIDENCE_REFS
- CHEMICAL_EVIDENCE_REFS
- JUDGMENT
- RATIONALE

## 9. Functional species

A functionally relevant chemical species is context-dependent.

Recommended relations:
- INTENDED_FUNCTION MEDIATED_BY CHEMICAL_SPECIES
- INTENDED_FUNCTION ASSOCIATED_WITH STRUCTURAL_MOTIF

Evidence may come from:
- direct functional assay,
- biological assay,
- clinical study,
- technical performance test,
- validated mechanism,
- regulatory functional definition,
- other domain-specific evidence.

Do not convert a plausible mechanism into a confirmed functional-species relation without evidence.

## 10. Formulation suitability

Recommended ASSESSMENT_TYPE:
- FORMULATION_SUITABILITY

Possible dimensions:
- SOLUBILITY
- DISPERSIBILITY
- VEHICLE_COMPATIBILITY
- PH_COMPATIBILITY
- THERMAL_PROCESS_COMPATIBILITY
- LIGHT_SENSITIVITY
- OXIDATION_SENSITIVITY
- WATER_ACTIVITY_COMPATIBILITY
- EMULSION_COMPATIBILITY
- PACKAGING_COMPATIBILITY
- COLOR_ODOR_IMPACT
- PHYSICAL_STABILITY
- CHEMICAL_STABILITY
- DELIVERY_BEHAVIOR

Recommended judgment:
- SUITABLE
- SUITABLE_WITH_CONDITIONS
- NOT_SUITABLE
- UNKNOWN
- NOT_TESTED

A formulation condition MUST remain explicit.
Do not generalize a result from one matrix to all formulations.

## 11. Use level and processing conditions

Recommended fields/observations:
- RECOMMENDED_USE_LEVEL
- TESTED_USE_LEVEL
- MAX_STUDIED_USE_LEVEL
- ADDITION_PHASE
- PROCESS_TEMPERATURE
- PROCESS_TIME
- TARGET_PH
- STORAGE_CONDITION
- SPECIAL_HANDLING

Distinguish:
- supplier recommendation,
- experimentally tested condition,
- regulatory limit,
- project-selected condition.

Do not merge them into one "use level".

## 12. Supplier and specification evidence

Recommended SOURCE_KIND additions:
- SUPPLIER_SPECIFICATION
- TECHNICAL_DATA_SHEET
- CERTIFICATE_OF_ANALYSIS
- SAFETY_DATA_SHEET
- SUPPLIER_MARKETING_MATERIAL
- COMMERCIAL_CATALOG_ENTRY
- QUOTATION
- AVAILABILITY_CONFIRMATION

Recommended fields:
- PRODUCT_NAME
- GRADE
- SPECIFICATION_VERSION
- SPECIFICATION_DATE
- LOT_OR_BATCH_REF
- CLAIMED_COMPOSITION
- ASSAY
- PURITY
- APPEARANCE
- STORAGE
- SHELF_LIFE
- SUPPLIER_RECOMMENDED_USE
- SUPPLIER_CLAIM

Supplier evidence is valid evidence of **what the supplier claims/specifies**.
It is not automatically independent evidence of efficacy, safety, or superiority.

## 13. Sourcing and commercial availability

Recommended ACTIVITY subtype:
- COMMERCIAL_AVAILABILITY_CHECK

Recommended OBSERVATION fields:
- SUPPLIER_ENTITY_ID
- PRODUCT_ENTITY_ID
- CHECKED_AT
- MARKET_OR_REGION
- AVAILABILITY_STATUS
- MOQ
- MOQ_UNIT
- PRICE
- CURRENCY
- PRICE_BASIS
- LEAD_TIME
- SAMPLE_AVAILABLE
- ORDER_CHANNEL
- NOTE

Recommended AVAILABILITY_STATUS:
- LISTED
- CONFIRMED_AVAILABLE
- SAMPLE_ONLY
- MADE_TO_ORDER
- OUT_OF_STOCK
- DISCONTINUED
- REGION_RESTRICTED
- NOT_CONFIRMED
- UNKNOWN

Price and availability are dated observations, not timeless product properties.

## 14. Regulatory applicability

Raw Material Research may attach use-context regulatory assessments.

Recommended ASSESSMENT_TYPE:
- REGULATORY_APPLICABILITY

Recommended fields:
- JURISDICTION
- PRODUCT_CATEGORY
- USE_CONTEXT_ID
- MATERIAL_OR_SPECIES_ID
- LIMIT_OR_CONDITION
- EFFECTIVE_DATE
- AUTHORITY_SOURCE_ID
- JUDGMENT

Recommended judgments:
- PERMITTED
- PERMITTED_WITH_CONDITIONS
- RESTRICTED
- PROHIBITED
- NOT_LISTED
- NOT_ASSESSED
- UNKNOWN

A future dedicated Regulatory Research Plugin may own richer jurisdiction semantics.
Raw Material Research should reference rather than duplicate that authority.

## 15. Scientific evidence vs raw-material assessment

A raw-material conclusion should be reconstructable as:

```text
chemical identity/transformation evidence
  + function evidence
  + formulation evidence
  + regulatory evidence where relevant
  + sourcing/commercial evidence where relevant
  -> Raw Material ASSESSMENT
```

Do not directly convert:
- supplier slogan,
- patent claim,
- review assertion,
- chemical motif retention

into a strong functional/commercial conclusion.

## 16. Commercial interpretation

Recommended ASSESSMENT_TYPE:
- COMMERCIAL_INTERPRETATION

Possible dimensions:
- DIFFERENTIATION
- FORMULATION_ADVANTAGE
- EVIDENCE_STRENGTH
- CLAIMABILITY
- SUPPLY_RISK
- COST_IMPACT
- REGULATORY_FRICTION
- MANUFACTURING_FIT

Recommended judgment:
- FAVORABLE
- MIXED
- UNFAVORABLE
- UNKNOWN

Commercial interpretation is downstream judgment.
It MUST NOT alter the source scientific observations.

If a commercial statement is intended for external communication, preserve:
- supporting evidence,
- qualifiers,
- unsupported portions,
- regulatory/claim restrictions.

## 17. Comparator-aware derivative rule

When evaluating a derivative against the compound from which it is derived or to which it can convert:

Chemical layer MUST report:
- derivative amount/retention,
- reference/base-compound amount/formation,
- relevant intermediate/products,
- unresolved balance,
- relevant motif retention when justified.

Raw-material layer MAY then assess:
- whether the reference/base compound itself supports the intended function,
- whether conversion timing/location matters,
- whether the delivery/formulation context preserves useful exposure,
- whether conversion creates unwanted formulation or safety effects.

Therefore:

```text
derivative disappearance != automatic raw-material function loss
```

But also:

```text
reference-compound formation != automatic raw-material function retention
```

The latter still requires use-context evidence.

## 18. Synthetic examples

### 18.1 Function released

```text
DERIVATIVE-X -> REFERENCE-A
intended function = F-1
REFERENCE-A directly demonstrates F-1 in the relevant system
```

Possible assessment:
- FUNCTION_RELEASED

Only if timing, location, concentration, and context are sufficiently applicable.

### 18.2 Chemical skeleton retained but function unknown

```text
DERIVATIVE-X -> INTERMEDIATE-B
core motif retained
no function assay for INTERMEDIATE-B
```

Required:
- Chemical: motif retained
- Raw Material: functional consequence = UNKNOWN

### 18.3 Analytical-standard context

```text
DERIVATIVE-X is purchased as an analytical standard
DERIVATIVE-X -> REFERENCE-A during storage
```

Intended function:
- exact DERIVATIVE-X identity for quantitation

Assessment:
- FUNCTION_LOST or NOT_SUITABLE for that analytical use may be justified,
even if REFERENCE-A is biologically active.

### 18.4 Supplier-only superiority claim

Supplier says:
- "more stable and more effective than REFERENCE-A"

Available evidence:
- only supplier sheet,
- no defined stability endpoint,
- no independent efficacy comparison.

Required:
- record supplier assertion,
- do not create independent superiority proposition as established fact,
- functional/commercial conclusion remains UNKNOWN or supplier-claim-only.

## 19. Interaction with Paper and Analysis Plugins

Paper Research:
- handles publication identity, lineage, access, extraction provenance.

Analysis Research:
- handles derived comparison, normalization, quantitative synthesis, computational diagnostics.

Chemical Research:
- owns species/transformation/stability semantics.

Raw Material Research:
- owns intended-use and commercial/formulation interpretation.

One evidence closure may use all four without changing authority boundaries.

## 20. Validation

Validate at least:
- Chemical Research dependency is present,
- intended function is explicit for function-based assessment,
- function consequence is not inferred from parent loss alone,
- function consequence is not inferred from motif retention alone,
- supplier claim and independent evidence remain distinguishable,
- product identity and chemical-species identity remain distinguishable,
- use level source/type is explicit,
- formulation conditions are preserved,
- regulatory claims are jurisdiction/date/use-context bounded,
- price/availability observations include CHECKED_AT,
- commercial interpretation remains downstream from evidence,
- chemical facts are not rewritten by raw-material assessment.

## 21. Physical organization

This Plugin may be stored next to its parent under:

`specs/research-evidence/plugins/chemical/`

That physical nesting is for discoverability only.

Semantic nesting is defined by:
- Plugin ID = `RESEARCH_EVIDENCE.CHEMICAL.RAW_MATERIAL`
- Parent Plugin = `RESEARCH_EVIDENCE.CHEMICAL`
- Required Dependency = Chemical Research Schema Plugin v0.1

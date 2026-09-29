# Chemical Research Schema Plugin v0.1

- Updated: 2026-09-29
- Status: CANDIDATE
- Plugin ID: RESEARCH_EVIDENCE.CHEMICAL
- Target Core: Research Evidence Core Schema v0.1
- Parent work model: Research Core v0.1
- Scope: chemical-species identity, derivatization, transformation, degradation, analytical identity, species balance, structural-motif retention, and chemical stability
- Decision history: ai-development-sahou Issue #24

## 1. Purpose

Chemical Research Plugin extends Research Evidence Core for research where the identity, amount, transformation, or persistence of chemical species materially affects interpretation.

Typical uses:
- parent compound vs derivative comparison,
- ester / salt / glycoside / conjugate / complex research,
- degradation and stability studies,
- hydrolysis / oxidation / reduction / ring opening,
- analytical identity and assay,
- transformation-product tracking,
- species-level mass balance,
- structural or reactive-moiety retention.

This Plugin describes **what chemical species changed into what, under which conditions**.

It does NOT decide whether a transformation is commercially desirable, formulation-useful, therapeutically desirable, cosmetically desirable, or otherwise valuable for a particular use. Those are downstream domain assessments.

Raw-material use semantics belong to the nested Raw Material Research Plugin.

## 2. Dependency and composition

Required dependency closure:

```text
Research Core
  -> Research Evidence Core
       -> Chemical Research Plugin
```

Chemical Research may coexist with:
- Paper Research Plugin,
- Analysis Research Plugin,
- future toxicology, clinical, regulatory, pharmacology, or materials plugins.

Chemical Research does not require Raw Material Research.

Physical folder location is organizational only. Semantic dependency is defined by Plugin ID and explicit dependency metadata.

## 3. Design principles

1. Chemical-species loss MUST NOT automatically be interpreted as loss of function.
2. A derivative converting into its comparison/reference compound MUST be recorded as a transformation, not silently collapsed into generic loss.
3. Parent-species retention, product formation, motif retention, and total recoverable species balance are distinct endpoints.
4. A structural motif may be chemically retained even when the original species is not.
5. A structural motif being retained does NOT itself prove biological or commercial function is retained.
6. Unknown transformation products MUST remain UNKNOWN rather than being assigned to a presumed pathway.
7. A proposed mechanism MUST remain distinct from a directly measured transformation.
8. Formula, mass, CAS, registry name, structure string, and synonym are evidence about identity; disagreement among them MUST be preserved as an identity conflict.
9. Analytical method and matrix may determine what species can be observed; non-detection is method-bounded.
10. "Stable" MUST always identify the endpoint and conditions.

## 4. Applicable Core types

This Plugin may extend:
- ENTITY
- ACTIVITY
- OBSERVATION
- QUESTION
- ASSESSMENT
- RELATION
- SOURCE where chemical-source metadata is needed

PROPOSITION uses Core semantics unchanged.

## 5. Chemical ENTITY semantics

### 5.1 Recommended ENTITY_KIND values

- CHEMICAL_SPECIES
- CHEMICAL_MIXTURE
- STRUCTURAL_MOTIF
- REACTION_PRODUCT_CLASS
- ANALYTICAL_STANDARD

A commercial ingredient product is not automatically a CHEMICAL_SPECIES. Commercial product semantics belong to Raw Material Research.

### 5.2 Species identity fields

Recommended fields for CHEMICAL_SPECIES when available:
- PREFERRED_NAME
- SYNONYM
- FORMULA
- MOLAR_MASS
- CAS_RN
- INCHI
- INCHIKEY
- SMILES
- STRUCTURE_REF
- CHARGE_STATE
- STEREOCHEMISTRY_STATE
- HYDRATION_SOLVATION_STATE

Do not require all fields.

### 5.3 Identity conflict

Recommended ASSESSMENT_TYPE:
- CHEMICAL_IDENTITY_CONFLICT

Possible judgments:
- CONSISTENT
- CONFLICTING_STRUCTURE
- CONFLICTING_FORMULA
- CONFLICTING_IDENTIFIER
- VERSION_OR_FORM_DIFFERENCE
- UNRESOLVED

Do not silently choose one registry representation when material disagreement exists.

## 6. Derivative and reference relations

Recommended relations:
- CHEMICAL_SPECIES DERIVATIVE_OF CHEMICAL_SPECIES
- CHEMICAL_SPECIES SALT_OF CHEMICAL_SPECIES
- CHEMICAL_SPECIES ESTER_OF CHEMICAL_SPECIES
- CHEMICAL_SPECIES CONJUGATE_OF CHEMICAL_SPECIES
- CHEMICAL_SPECIES COMPLEX_OF CHEMICAL_SPECIES
- CHEMICAL_SPECIES STRUCTURALLY_RELATED_TO CHEMICAL_SPECIES
- CHEMICAL_SPECIES CONTAINS_MOTIF STRUCTURAL_MOTIF

A derivative/reference relation is a structural relation, not a function judgment.

The reference species used in a comparison SHOULD be explicit when interpretation depends on it.

Recommended QUESTION/ACTIVITY field:
- REFERENCE_SPECIES_ID

## 7. Chemical transformation ACTIVITY

Recommended ACTIVITY subtypes:
- CHEMICAL_TRANSFORMATION
- DEGRADATION_STUDY
- STABILITY_STUDY
- HYDROLYSIS_STUDY
- OXIDATION_STUDY
- REDUCTION_STUDY
- PHOTOLYSIS_STUDY
- THERMAL_STABILITY_STUDY
- ANALYTICAL_IDENTITY_TEST
- SPECIES_BALANCE_ANALYSIS

Recommended relations:
- ACTIVITY USES CHEMICAL_SPECIES
- ACTIVITY TRANSFORMS CHEMICAL_SPECIES
- ACTIVITY GENERATES CHEMICAL_SPECIES
- ACTIVITY GENERATES OBSERVATION
- ACTIVITY USES ANALYTICAL_STANDARD
- ACTIVITY MEASURES STRUCTURAL_MOTIF

A transformation mechanism may be proposed without all products being identified.

## 8. Transformation-pathway semantics

Recommended transformation labels:
- HYDROLYSIS
- ESTER_CLEAVAGE
- OXIDATION
- REDUCTION
- RING_OPENING
- ISOMERIZATION
- DECONJUGATION
- DEGLYCOSYLATION
- DECOMPLEXATION
- PHOTOLYSIS
- THERMOLYSIS
- OTHER
- UNKNOWN

A label may describe an observed or proposed pathway.

Recommended qualifier:
- PATHWAY_EVIDENCE = DIRECTLY_MEASURED | PRODUCT_SUPPORTED | INFERRED | PROPOSED | UNKNOWN

Do not promote PROPOSED to DIRECTLY_MEASURED because multiple sources repeat it.

## 9. Chemical OBSERVATION fields

Recommended fields:
- ANALYTE_SPECIES_ID
- REFERENCE_SPECIES_ID
- VALUE
- UNIT
- BASIS
- TIMEPOINT
- MATRIX
- TEMPERATURE
- PH
- LIGHT_CONDITION
- OXIDANT_REDUCTANT
- HUMIDITY
- OXYGEN_CONDITION
- SOLVENT_OR_VEHICLE
- ANALYTICAL_METHOD
- DETECTION_LIMIT
- QUANTITATION_LIMIT
- SOURCE_LOCATOR

Use only fields relevant to the activity.

### 9.1 Recommended BASIS values

- MASS_CONCENTRATION
- MOLAR_CONCENTRATION
- MASS_FRACTION
- MOLAR_FRACTION
- PERCENT_INITIAL
- RECOVERED_AMOUNT
- PEAK_AREA_RATIO
- OTHER

## 10. Stability must be endpoint-qualified

Do not store one unqualified "STABLE = true".

Recommended chemical stability endpoints:
- PARENT_SPECIES_RETENTION
- REFERENCE_SPECIES_FORMATION
- TRANSFORMATION_PRODUCT_FORMATION
- TOTAL_IDENTIFIED_SPECIES_RECOVERY
- CORE_MOTIF_RETENTION
- REACTIVE_MOIETY_RETENTION
- UNKNOWN_PRODUCT_FRACTION

These endpoints may move in different directions in the same experiment.

Example:

```text
DERIVATIVE-X initial = 100 mol-equivalent
after storage:
  DERIVATIVE-X = 40
  REFERENCE-A = 55
  UNKNOWN = 5
```

Valid observations:
- parent-species retention = 40%
- reference-species formation = 55 mol-equivalent
- identified-species recovery = 95 mol-equivalent

Invalid shortcut:
- "60% chemical function was lost"

Function was not measured by these observations.

## 11. Comparator-formation rule for derivative studies

When:
1. a derivative is compared with its base/reference species, and
2. the derivative can transform into that reference species,

the research MUST distinguish:
- disappearance of the derivative,
- appearance of the reference species,
- appearance of other products,
- unresolved balance.

A derivative disappearing into the comparator is chemically a transformation/degradation of the derivative, but it is not equivalent to disappearance of the comparator's chemical skeleton.

Therefore:
- derivative retention and reference-species formation MUST NOT be merged into one generic stability score;
- the comparison SHOULD report both species where analytically feasible.

## 12. Structural-motif retention

Use STRUCTURAL_MOTIF only when a substructure materially matters to the chemical question.

Recommended fields/relations:
- CHEMICAL_SPECIES CONTAINS_MOTIF STRUCTURAL_MOTIF
- OBSERVATION TARGET_MOTIF_ID
- MOTIF_STATE = INTACT | MODIFIED | ABSENT | UNKNOWN
- MOTIF_EVIDENCE = STRUCTURE_IDENTIFIED | SPECTRAL_SUPPORT | REACTION_INFERRED | UNKNOWN

Examples of appropriate motif questions:
- aromatic ring retained after hydrolysis,
- conjugated system preserved after derivatization,
- reactive hydroxyl group regenerated,
- chelating motif preserved or destroyed.

Do NOT infer biological activity merely because a motif is structurally present.

## 13. Species balance and mass balance

Recommended ASSESSMENT_TYPE:
- CHEMICAL_MASS_BALANCE

Recommended fields:
- INPUT_SPECIES_SET
- IDENTIFIED_PRODUCT_SET
- RECOVERED_EQUIVALENT
- BALANCE_BASIS
- JUDGMENT

Recommended judgments:
- CLOSED
- PARTIALLY_CLOSED
- OPEN
- NOT_ESTIMABLE

"Parent decreased" with no quantified product information is normally OPEN, not CLOSED.

A balance may be closed on:
- molar parent-equivalent basis,
- atom-specific basis,
- isotope basis,
- another explicitly defined conserved basis.

Do not compare mass percentages across species with different molar masses without an explicit basis.

## 14. Unknown and non-detection handling

Distinguish:
- NOT_MEASURED
- NOT_REPORTED
- BELOW_DETECTION
- BELOW_QUANTITATION
- NOT_IDENTIFIED
- SEARCH_NOT_PERFORMED
- UNKNOWN

A missing product peak does not prove that a product was not formed if the method could not detect it.

A missing reference-species increase does not prove destructive degradation unless the analytical scope and mass balance support that conclusion.

## 15. Chemical interpretation assessments

Recommended ASSESSMENT_TYPE values:
- CHEMICAL_IDENTITY
- TRANSFORMATION_PATHWAY
- CHEMICAL_STABILITY_INTERPRETATION
- CHEMICAL_MASS_BALANCE
- ANALYTICAL_COVERAGE
- STRUCTURAL_MOTIF_RETENTION
- SPECIES_COMPARABILITY

These assessments may interpret chemical evidence but MUST NOT encode intended-use value such as "good for whitening", "commercially superior", or "better raw material".

## 16. Paper and Analysis Plugin composition

Use Paper Research when:
- source identity,
- publication lineage,
- extraction provenance,
- access sufficiency,
- scholarly-source duplication
matter.

Use Analysis Research when:
- computational transformation analysis,
- spectral/structure comparison,
- cross-source normalization,
- quantitative derived analysis
materially affects evidence.

Chemical fields remain owned by Chemical Research even when observations were extracted from papers or generated by analysis.

## 17. Synthetic stress tests

### 17.1 Derivative converts to reference species

```text
DERIVATIVE-X -> REFERENCE-A
```

Required:
- record DERIVATIVE-X loss,
- record REFERENCE-A formation,
- keep chemical parent retention separate from reference-species formation.

### 17.2 Derivative converts to unidentified products

```text
DERIVATIVE-X -> UNKNOWN
```

Required:
- parent loss may be observed,
- destructive pathway MUST remain unresolved until products/motif balance support it.

### 17.3 Active intermediate without use-context interpretation

```text
DERIVATIVE-X -> INTERMEDIATE-B -> REFERENCE-A
```

Chemical Plugin may record all three species and retained motifs.
It does not label INTERMEDIATE-B "beneficial" without another domain's function evidence.

### 17.4 Analytical standard use

If DERIVATIVE-X is being used as an analytical reference standard, conversion to REFERENCE-A means the standard's species identity is degraded even if REFERENCE-A is functionally useful elsewhere.

This demonstrates why use-value does not belong in Chemical Research.

## 18. Validation

Validate at least:
- species identity is explicit enough for the question,
- derivative/reference relations are not inferred from names alone when structure matters,
- parent retention is separated from product formation,
- comparison-to-reference studies track comparator formation when relevant and measurable,
- mass-balance basis is explicit,
- motif retention does not silently become function retention,
- proposed pathways are labeled as proposed/inferred,
- non-detection remains method-bounded,
- chemical observation and downstream use-value assessment remain separate,
- unknown products remain UNKNOWN when not identified.

## 19. Nested plugin boundary

Chemical Research is the parent domain plugin for Raw Material Research.

Raw Material Research MAY consume:
- chemical species identity,
- transformation observations,
- parent/reference balances,
- motif-retention assessments,
- stability conditions.

Raw Material Research MUST NOT rewrite those chemical facts.

It may add use-context interpretation, including whether a transformation preserves, releases, reduces, or destroys an intended raw-material function.

See:
- `RAW_MATERIAL_RESEARCH_SCHEMA_PLUGIN_v0.1.md`

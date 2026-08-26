# Critical assessment of PMM

PMM is a promising evidence-aware ontology prototype. It is not yet a scientific reference map of psychology. The distinction matters: the current system demonstrates how claims and evidence can be represented, but its contents are selective and have not undergone independent expert curation.

## What is solid

1. **Claims are reified.** Correlation, prediction, mediation, moderation, causal effects, and hypotheses are records with scope and provenance rather than ambiguous graph arrows.
2. **Objects are separated from evidence.** A Behavior, State, Mechanism, Measurement, and Intervention cannot inherit empirical support merely by appearing near a supported Claim.
3. **Null and conflicting results remain visible.** The model can represent unsupported and mixed claims without absorbing them into a favorable narrative.
4. **Human-editable data are canonical.** Modular YAML, deterministic validation, JSON/RDF exports, and generated views provide a workable engineering foundation.
5. **Inference constraints are executable.** JSON Schema, semantic validation, tests, and SHACL catch several category and causal-modeling errors.

## What is weak or premature

### 1. Evidence selection is not systematic

Sources were selected to stress-test the ontology, not through reproducible systematic searches. The map therefore cannot estimate scientific consensus, publication bias, prevalence, or the proportion of supportive versus conflicting evidence.

**Consequence:** counts of supported Claims must not be interpreted as evidence that a field is mostly settled.

### 2. Confidence remains curator judgement

Confidence has a rationale and evidence-domain fields, but there is no validated scoring rubric, calibration study, or independent agreement estimate.

**Consequence:** `high`, `moderate`, and `low` improve transparency but are not standardized certainty ratings comparable to GRADE or a formal risk-of-bias instrument.

### 3. Claim granularity varies

Some Claims summarize one experiment; others integrate multiple paradigms or propose a broad mechanism. A graph can make these records look equivalent even when their inferential breadth differs substantially.

**Consequence:** future curation needs explicit rules for when to split a Claim by population, task, outcome channel, intervention, and follow-up time.

### 4. Mechanism evidence is often indirect

Outcome contrasts, neural measurements, antagonist challenges, and statistical mediation can constrain mechanisms without uniquely identifying them. Several current mechanisms remain integrative hypotheses despite multiple linked sources.

**Consequence:** adding sources must not automatically promote a `mechanism_hypothesis` to an established mechanism.

### 5. External ontology alignment is incomplete

PMM aligns selectively with RDoC and related resources, but many identifiers and mapping relations remain absent or provisional. Similar labels across Cognitive Atlas, NBO, MFO, HiTOP, and PMM are not automatically exact matches.

### 6. The interface can overstate graph semantics

Spatial proximity and generic arrows are cognitively read as causal even when the data encode association or moderation. The inspector now uses distinct diagrams, but the main graph remains primarily navigational.

### 7. Translation is not expert-reviewed

Russian presentation text is machine-translated with a small curated terminology override. It improves access but must not be treated as an authoritative Russian scientific vocabulary.

### 8. Coverage is intentionally sparse

Ten families cannot represent psychology or psychopathology as a whole. Development, culture, social structure, longitudinal clinical course, ecological measurement, genetics, and many intervention domains are substantially underrepresented.

## Quality gates before broad expansion

`Curation Protocol v0.1` and its first retrospective social-buffering log now provide the machine-readable infrastructure for gate 1. The protocol remains a pilot: the first log is not a systematic review, and gates 2-7 remain scientifically incomplete.

The social-buffering dual-review pilot now has a blinded 51-record title/abstract packet and an AI-assisted Reviewer A triage file. An independent human Reviewer B, agreement measurement, disagreement resolution, full-text screening, and extraction verification remain incomplete, so this does not yet satisfy gate 2.

PMM should not pursue comprehensive coverage until all of the following exist:

1. A machine-readable curation protocol with eligibility, search, deduplication, extraction, and update rules.
2. Source-search logs for every public family, including databases, queries, dates, and screening decisions.
3. Independent double review for a sample of objects, Claims, Evidence records, and confidence judgements.
4. A documented disagreement-resolution process and inter-rater agreement report.
5. A risk-of-bias instrument appropriate to each evidence design rather than one generic confidence label.
6. Explicit Claim-splitting rules and stable policies for deprecation and supersession.
7. Expert review of Russian terminology before presenting the translation as reviewed.

## Recommended next development sequence

PMM now separates product integration from evidence-quality work. Repeating a manual near-systematic review for every family would be unscalable and would duplicate mature evidence-synthesis systems without solving cross-family integration.

1. **Global mechanism index:** compare every Mechanism across families using derived Claim, Evidence, and Source metadata without asserting equivalence.
2. **Cross-family bridge audit:** add conservative, reviewed mapping records for exact, close, broader, narrower, or related matches; never use these mappings as causal predicates.
3. **Sampled dual review:** independently re-curate a heterogeneous sample and measure agreement on object type, claim type, scope, status, and confidence.
4. **Design-specific bias assessment:** pilot RoB-style fields for randomized experiments, observational studies, computational models, and reviews.
5. **Targeted expansion:** add a family only when it tests a declared ontology boundary, connects existing islands, or fills a measured coverage gap.

The rationale and completion criteria for this course correction are documented in [the strategy reset](strategy-reset.md).

## Interpretation rule

PMM currently answers:

> How can a selected set of psychological mechanism claims be represented without erasing inferential differences?

It does not yet answer:

> What is the complete, unbiased, or consensus-supported causal structure of the mind?

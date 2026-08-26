# PMM v0.2 methodology

## What PMM represents

PMM is a claim-and-evidence model that can later be projected into a graph. It does not assume that every named psychological construct is a mechanism, or that every edge is causal.

## Plain-language annotations

A scientific `Claim.statement` and its plain-language explanation are deliberately separate records. The Claim is canonical scientific data; `data/claim-explanations.yaml` is a bilingual editorial layer checked against the Claim's linked Evidence and Sources. An explanation may clarify the design, observed result, scope, and inference limit, but it must not strengthen causality, generality, confidence, or mechanism status.

The interface never generates these explanations from a claim type or node labels. Complete English and Russian coverage is validated before publication. Missing text is a build error because a fluent but unsupported fallback would be more misleading than an explicit gap.

| Record | Precise role |
|---|---|
| Entity | General base for a construct, event, outcome, process, disposition, agent, or other referent. |
| Mechanism | A process or organized disposition that transforms specified inputs into outputs under stated conditions. A statistical association is not a mechanism. |
| State | A time-indexed condition of a person, organism, group, environment, or interaction. |
| Behavior | An observable action, omission, or response pattern; its function must be established separately from its form. |
| Intervention | A deliberate manipulation with targets, delivery, and intended direction. Treatment efficacy is a separate claim. |
| Measurement | An operational method that produces an observation about one or more targets at a declared unit of analysis. |
| Context | Experimental, clinical, social, developmental, cultural, physical, or temporal conditions that bound a claim. |
| Relation | A graph-ready semantic edge. Empirical and integrative edges cite Claims. |
| Claim | A scoped statement with a declared inference type and confidence rationale. |
| Evidence | A source-linked extraction with design, population, inference support, and evidence-domain judgments. |
| Source | A versioned bibliographic or authoritative provenance record. |

## Inferential firewall

PMM distinguishes the following by required fields, not wording alone:

| Inference | Required identification content | What it does not establish |
|---|---|---|
| Correlation | Exposure, outcome, association estimate, confounding note | Temporal order, prediction, or causation |
| Prediction | Exposure, outcome, validation strategy, predictive metric | Intervention effect or mechanism |
| Mediation | Exposure, mediator, outcome, indirect effect, temporal order | Causal mediation unless all relevant paths are causally identified |
| Moderation | Predictor, moderator, outcome, interaction estimate | That the moderator itself is causal |
| Causation | Exposure, outcome, estimand, identification strategy, temporal order, causal assumptions | Generalization beyond the declared population/context |

Mediation and moderation describe different structures. A mediator is on a proposed exposure-to-outcome path; a moderator indexes effect or association heterogeneity. A variable can play both roles only in separate, explicit claims.

## Evidence and confidence

Confidence is ordinal (`high`, `moderate`, `low`, `very_low`) with a written rationale. PMM deliberately avoids an automatic numeric truth score. Each Evidence record assesses directness, risk of bias, consistency, precision, and replication. Evidence type is not a verdict: a randomized experiment may be indirect or biased, and a systematic review may synthesize heterogeneous designs.

`knowledge_status` and `confidence` answer different questions:

- `knowledge_status` says whether a claim is an operational definition, empirically established/supported/mixed, proposed integration, refuted, or unknown.
- `confidence` says how certain PMM curators are within the claim's stated scope.

High-confidence causal claims require evidence marked `causal_support: true`, an explicit causal estimand, and an identification strategy. Statistical significance alone never upgrades an association to causation.

## Pilot interpretation

The pilot contains three different levels that must not be collapsed:

1. **Established in a controlled contingency:** a specified avoidance response can change the programmed aversive outcome; contingent omission/reduction can increase future responding. This is the operational core of negative reinforcement.
2. **Supported but heterogeneous in humans:** anxiety and avoidance are associated, but both are multi-determined and can dissociate.
3. **Proposed/integrative:** repeated anxiety-related avoidance may produce short-term aversive reduction, reinforce avoidance, and reduce corrective learning. The whole longitudinal clinical chain is plausible and useful, but not encoded as a universal established mechanism.

The pilot explicitly rejects several shortcuts: relief alone is not reinforcement; avoidance is not always maladaptive; a threat cue is not the same as subjective anxiety; and active avoidance is not punishment or Pavlovian fear.

## Framework alignment

Framework alignment is faceted and polyhierarchical: an educational heading, an external framework term, and a canonical PMM record may point to the same scientific object without becoming identical ontology classes. General-psychology headings are navigation nodes only. They never change a `Context` such as N-back into a memory process, a `Measurement` into an ability, or a trait taxonomy into a Mechanism.

- [NIMH RDoC](https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/about-rdoc) supplies a dimensional research framework. PMM uses the official [Potential Threat (Anxiety)](https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/definitions-of-the-rdoc-domains-and-constructs) boundary where appropriate, but RDoC is not a diagnostic guide or a complete causal ontology.
- [Cognitive Atlas](https://www.cognitiveatlas.org/) separates concepts, tasks, and assertions. PMM follows that separation conceptually. The exact Working Memory concept and N-back task URLs are pinned, but both external pages are currently marked `Unreviewed`, so the mappings remain provisional.
- [Mental Functioning Ontology](https://bioportal.bioontology.org/ontologies/MF) supplies BFO/OGMS-grounded upper-level mental-functioning classes. Its indexed 2025-07-08 release is marked alpha; PMM therefore avoids fabricated exact matches.
- [Neuro Behavior Ontology](https://bioportal.bioontology.org/ontologies/NBO) supplies OWL classes for behavioral processes and phenotypes. PMM records a provisional relationship for avoidance pending release-level term review.
- [HiTOP](https://www.hitop-system.org/) supplies a hierarchical dimensional organization of psychopathology based primarily on symptom/trait covariation. It helps locate clinical phenotype dimensions; it does not by itself establish a learning mechanism.

## Serialization path

YAML is canonical for editing. JSON is a deterministic build artifact. PMM IDs are already CURIE-like, external mappings carry resolvable URLs, and relations use explicit subjects and objects. A later JSON-LD context can map these fields to RDF predicates. SHACL should enforce graph constraints equivalent to the current local validator; OWL should represent taxonomic semantics, while empirical Claims remain reified nodes because OWL class axioms are not a substitute for uncertain evidence.

## Curation policy

- Pin source and ontology release dates.
- Never promote a provisional external mapping without checking the exact term definition and stable identifier.
- Preserve deprecated IDs and point to successors.
- Split a claim when population, context, temporal scale, or inference type changes materially.
- Add quantitative estimates only when the metric and denominator are comparable.
- Record contradictory evidence instead of deleting it.
- Require domain-expert review before changing `review_status` to `expert_reviewed`.

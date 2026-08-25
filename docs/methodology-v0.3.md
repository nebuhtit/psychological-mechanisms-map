# PMM v0.3 methodology

## Modeling rule

PMM models scientific assertions, not a literal complete map of the psyche. A label is assigned to the narrowest defensible record type, and empirical status belongs to a Claim rather than to the object being discussed.

| Record | Role | Common category error |
|---|---|---|
| Construct | Theoretical or operational concept organizing observations | Treating it as an event or causal process |
| Mechanism | Process with participants and realization conditions | Renaming an association as a mechanism |
| State | Time-indexed condition borne by a person, organism, group, environment, or interaction | Treating a diagnostic dimension as an episode |
| Behavior | Observable or operationally inferred action, omission, or response pattern | Inferring behavioral function from topography |
| Intervention | Deliberate manipulation | Encoding intended efficacy as established efficacy |
| Measurement | Procedure yielding observations about a target | Equating score, task, and target construct |
| Context | Conditions bounding objects or claims | Treating threat context as anxiety itself |
| Event | Occurrent with temporal boundaries | Treating omission as a persistent state |
| Outcome | Consequence type or evaluated endpoint | Treating a numerical effect estimate as an outcome object |
| Contingency | N-ary antecedent-response-consequence-comparator dependency | Reducing a dependency to an ambiguous binary arrow |
| Observation | Measurement-result instance | Replacing the measured target with its value |
| Relation | Structural or operational edge | Using an edge to imply correlation or causation |
| Claim | Scoped definition, result, effect, or hypothesis | Attaching epistemic status directly to an ontology object |
| Evidence | One source-specific extraction | Combining reviews and primary studies into an unauditable summary |
| Source | Bibliographic or authoritative record | Treating an index or framework as evidence for every included claim |

`Entity` is only an abstract schema base. PMM v0.3 has no concrete catch-all Entity record.

## Inferential firewall

Claims are distinguished by required and forbidden fields.

| Claim | Required identification content | Does not establish |
|---|---|---|
| Association | Exposure, outcome, estimate, confounding note | Prospective prediction, temporal order, causation |
| Prediction | Exposure, outcome, held-out validation strategy, predictive metric | Intervention effect or mechanism |
| Mediation | Exposure, mediator, outcome, indirect effect, temporal ordering | Causal mediation without path-specific identification assumptions |
| Moderation | Exposure, moderator, outcome, interaction term | That the moderator is causal or is a mediator |
| Causal effect | Exposure, outcome, estimand, identification strategy, temporal order, causal assumptions, direct evidence | Generalization beyond declared scope or a mechanism |
| Causal hypothesis | Proposed estimand, assumptions, temporal order, falsifiable boundary | An established causal effect |
| Mechanism hypothesis | Mechanism, exposure, outcome, temporal order, falsifiable boundary | Unique mediation or biological implementation |

The JSON Schema implements conditional `required` and `not` constraints. The semantic validator additionally requires direct causal Evidence for `causal_effect`, validates relation domains/ranges, resolves references, and checks Evidence/Claim backlinks.

## Evidence and confidence

Each Evidence record represents one extraction from one Source. Reviews can support definitions, scope, consistency, or mechanism plausibility, but a review label does not itself supply direct causal identification. Evidence tracks directness, risk of bias, consistency, precision, replication, support direction, and causal support.

Multiple experiments within one article remain separate Evidence records. Null and analysis-sensitive results are retained with `challenges` or `mixed` support directions; they are not absorbed into a favorable article-level summary.

Confidence remains ordinal with a written rationale. PMM intentionally avoids a pseudo-precise numerical truth score. `epistemic_status` belongs to Claims; ontology objects use `curation_status` only.

## Anxiety pilot interpretation

The v0.3 pilot makes the following distinctions:

1. The official RDoC Potential Threat (Anxiety) term is a dimensional neurobehavioral Construct, not an individual anxiety state or threat context.
2. Aversive-outcome omission is an Event. Subjective relief is a State and requires its own measurement.
3. Negative reinforcement requires a response-consequence contingency and a later change in responding; omission or relief alone is insufficient.
4. The programmed contingency is part of a design. Whether learning occurred is an empirical Claim.
5. Anxiety-related avoidance and a longitudinal clinical maintenance loop are not universal laws; the broad loop is kept proposed and falsifiable.

## Heterogeneous validation lessons

- **Proactive interference:** the observed performance cost is a Construct/Outcome pattern; retrieval competition is one proposed Mechanism among encoding and retrieval accounts.
- **Reward prediction error:** the computational discrepancy is a Construct; temporal-difference updating is a Mechanism; neither is automatically identical to phasic dopamine activity.
- **HPA feedback:** glucocorticoid concentration and secretory drive are States; feedback is a physiological Mechanism; dexamethasone challenge is an Intervention used to test it.
- **Social buffering:** randomized parent-buffer assignment is an Intervention; condition-by-time interaction is a Moderation Claim; the randomized condition contrast is a separate Causal-effect Claim; the mediating social-buffering Mechanism remains unidentified by that contrast alone.

These cases validate the model more effectively than adding many near-duplicate anxiety terms.

## Framework alignment

External systems are aligned by role, not copied wholesale.

| System | Useful contribution | PMM boundary |
|---|---|---|
| NIMH RDoC | Dimensional neurobehavioral domains and constructs | Not a complete causal ontology or diagnostic taxonomy |
| Cognitive Atlas | Separation of cognitive concepts, tasks, and assertions | Concept/task IDs require release-level verification |
| Mental Functioning Ontology (MF) | Formal upper-level mental-functioning classes | An indexed alpha release is not grounds for invented exact mappings |
| Neuro Behavior Ontology (NBO) | Behavioral processes and phenotype vocabulary | Behavior class does not establish functional contingency |
| HiTOP | Hierarchical dimensional psychopathology phenotypes | Covariance-based phenotype structure does not establish mechanisms |

`exact_match` requires a verified stable external identifier. A verified webpage label without a stable term IRI remains `close_match` or provisional.

## Serialization

YAML is canonical. Deterministic JSON is generated only after validation. A later JSON-LD context can expand PMM IDs and structural predicates to RDF. SHACL should mirror cross-record validation. OWL may encode taxonomic commitments, but uncertain empirical Claims and Evidence must remain reified resources rather than being converted into unconditional class axioms.

## Known limits

- Primary-study extraction currently covers one focused negative-reinforcement pack; the other mechanism families still rely mainly on reviews.
- Confidence ratings are curator judgments, not a calibrated evidence-grading system.
- External ontology releases and stable IDs are not yet pinned locally.
- Claim scope is textual rather than a fully compositional population/intervention/comparator/outcome model.
- The current schema can represent statistical mediation and moderation but does not yet provide separate hypothesis subtypes for each.
- No expert review has been completed; `machine_validated` means structural and semantic checks passed, not scientific endorsement.

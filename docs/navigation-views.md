# PMM navigation views v0.1

PMM now exposes three projections over one canonical evidence model.

## 1. General Psychology

This is an educational navigation facet. It exposes 24 familiar topics across cognitive processes, emotion and motivation, action and self-regulation, social processes, body and consciousness, development, and individual differences. These headings are not added as new PMM object types and do not form one strict ontology.

Every linked card retains its canonical type:

- working-memory capacity is a `Construct`;
- N-back is a task `Context`;
- an N-back score is a `Measurement`;
- episodic retrieval is a proposed `Mechanism`;
- spatial selective attention is a `Construct`, while the cueing task is a `Context`, cue validity is an `Intervention`, and latency or accuracy are outcomes and measurements;
- declarative, episodic, and semantic memory are distinct `Construct` records, while incidental encoding is a task `Context`, recognition is a `Behavior`, and its score is a `Measurement`;
- visual perception and spatial contrast sensitivity are `Construct` records, while grating detection is a task `Context`, grating properties are an `Intervention`, a detection report is `Behavior`, and the contrast sensitivity function is a `Measurement`;
- deductive reasoning is a `Construct`, while a syllogism task is a `Context`, validity and believability are experimentally varied in an `Intervention`, the answer is `Behavior`, performance and signal-detection parameters are measurements, and parallel belief-logic evaluation remains a proposed `Mechanism`;
- anxiety is represented according to its use in a particular record, not forced into one universal type;
- Big Five is a descriptive trait taxonomy, not a causal mechanism;
- temperament is an area of stable individual differences in reactivity and self-regulation, not merely a list of classical types.

Coverage labels are epistemically important. `partial` means that at least one canonical evidence-linked record exists, not that the area is complete. `planned` means that PMM does not yet contain curated records for the area. Attention is narrowly limited to predictive spatial cueing, declarative memory to encoding, recognition, and one clinical dissociation, perception to grating contrast detection, and reasoning to syllogistic validity judgments under belief conflict. A task score is not treated as the entire psychological function.

## 2. Mechanisms & Evidence

This is the strict scientific core. It separates objects, structural relations, reified Claims, Evidence extractions, and Sources. Causation, association, prediction, mediation, and moderation remain distinct.

Open research questions appear as a faint peripheral annotation layer. They point to source-linked limitations but are not promoted into objects or Claims. Selecting one explains why the gap remains open and what kind of study could reduce the uncertainty.

## 3. Scientific Systems

This is a crosswalk, not a merged hierarchy:

- RDoC is a dimensional research framework, not a diagnostic manual or complete ontology.
- Cognitive Atlas distinguishes cognitive concepts from experimental tasks. Linked memory, attention, perception, deductive-reasoning, and task records are marked `Unreviewed`, so PMM mappings are provisional.
- Big Five organizes broad personality trait variation but does not identify mechanisms by itself.
- modern temperament models organize developmental dimensions of reactivity and self-regulation; PMM has not selected one universal model.
- HiTOP organizes psychopathology and must not be used as a general classification of normal mental functions.

## Data contract

The human-editable projection is [`data/navigation-views-v0.1.yaml`](../data/navigation-views-v0.1.yaml). `scripts/build_site_data.py` rejects unknown family IDs, unresolved canonical IDs, type mismatches, broken parents, and unknown source references. The generated website bundle remains disposable.

The language area now has a deliberately narrow visual-word pilot. It separates broad comprehension, visual lexical access, the lexical-decision task, manipulated prime relation and timing, observable classification, response latency, diffusion-model parameters, and competing automatic and strategic hypotheses. It does not yet cover production, syntax, discourse, pragmatics, or sign language. The next breadth expansion is Big Five, where descriptive trait structure must remain separate from questionnaire scores, prediction, and causal mechanism. The complete queue and promotion gate are documented in [`docs/coverage-roadmap.md`](coverage-roadmap.md).

## Practical interpretation layer

Practical implications are bilingual annotations over existing Claims and Sources, not new Claims or graph nodes. Each annotation states a possible action, expected change, evidence basis, application setting, what is not established, and any safety boundary. `direct_within_tested_scope` is reserved for the tested manipulation and outcome; `transfer_uncertain` marks extrapolation to a practical setting; `interpretation_only` marks a conceptual aid or untested candidate action. This prevents the interface from silently converting evidence about a laboratory effect into a treatment, learning method, or debiasing promise.

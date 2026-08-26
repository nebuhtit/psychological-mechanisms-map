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
- anxiety is represented according to its use in a particular record, not forced into one universal type;
- Big Five is a descriptive trait taxonomy, not a causal mechanism;
- temperament is an area of stable individual differences in reactivity and self-regulation, not merely a list of classical types.

Coverage labels are epistemically important. `partial` means that at least one canonical evidence-linked record exists, not that the area is complete. `planned` means that PMM does not yet contain curated records for the area. Attention is narrowly limited to predictive spatial cueing, and declarative memory to encoding, recognition, and one clinical dissociation. Perception remains planned: using visual stimuli does not by itself create a validated model of perception.

## 2. Mechanisms & Evidence

This is the strict scientific core. It separates objects, structural relations, reified Claims, Evidence extractions, and Sources. Causation, association, prediction, mediation, and moderation remain distinct.

## 3. Scientific Systems

This is a crosswalk, not a merged hierarchy:

- RDoC is a dimensional research framework, not a diagnostic manual or complete ontology.
- Cognitive Atlas distinguishes cognitive concepts from experimental tasks. Linked Working Memory, N-back, spatial-attention, and visuospatial-cueing records are marked `Unreviewed`, so PMM mappings are provisional.
- Big Five organizes broad personality trait variation but does not identify mechanisms by itself.
- modern temperament models organize developmental dimensions of reactivity and self-regulation; PMM has not selected one universal model.
- HiTOP organizes psychopathology and must not be used as a general classification of normal mental functions.

## Data contract

The human-editable projection is [`data/navigation-views-v0.1.yaml`](../data/navigation-views-v0.1.yaml). `scripts/build_site_data.py` rejects unknown family IDs, unresolved canonical IDs, type mismatches, broken parents, and unknown source references. The generated website bundle remains disposable.

The next expansion is visual perception. It must separate sensory stimuli, perceptual constructs, observable discriminations, psychophysical measurements, sensitivity, response criterion, and candidate sensory mechanisms. The complete queue and promotion gate are documented in [`docs/coverage-roadmap.md`](coverage-roadmap.md).

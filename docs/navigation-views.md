# PMM navigation views v0.1

PMM now exposes three projections over one canonical evidence model.

## 1. General Psychology

This is an educational navigation facet. It starts with familiar areas such as Memory, Emotional states and regulation, Temperament, and Big Five. These headings are not added as new PMM object types and do not form one strict ontology.

Every linked card retains its canonical type:

- working-memory capacity is a `Construct`;
- N-back is a task `Context`;
- an N-back score is a `Measurement`;
- episodic retrieval is a proposed `Mechanism`;
- anxiety is represented according to its use in a particular record, not forced into one universal type;
- Big Five is a descriptive trait taxonomy, not a causal mechanism;
- temperament is an area of stable individual differences in reactivity and self-regulation, not merely a list of classical types.

Coverage labels are epistemically important. `partial` means that some canonical records exist. `planned` means that PMM does not yet contain curated records for the area.

## 2. Mechanisms & Evidence

This is the strict scientific core. It separates objects, structural relations, reified Claims, Evidence extractions, and Sources. Causation, association, prediction, mediation, and moderation remain distinct.

## 3. Scientific Systems

This is a crosswalk, not a merged hierarchy:

- RDoC is a dimensional research framework, not a diagnostic manual or complete ontology.
- Cognitive Atlas distinguishes cognitive concepts from experimental tasks. Linked Working Memory and N-back records are currently marked `Unreviewed`, so PMM mappings are provisional.
- Big Five organizes broad personality trait variation but does not identify mechanisms by itself.
- modern temperament models organize developmental dimensions of reactivity and self-regulation; PMM has not selected one universal model.
- HiTOP organizes psychopathology and must not be used as a general classification of normal mental functions.

## Data contract

The human-editable projection is [`data/navigation-views-v0.1.yaml`](../data/navigation-views-v0.1.yaml). `scripts/build_site_data.py` rejects unknown family IDs, unresolved canonical IDs, type mismatches, broken parents, and unknown source references. The generated website bundle remains disposable.

The next expansion should add heterogeneous domains only after their boundaries are reviewed: attention/perception, episodic and semantic memory, motivation, social processes, development, and personality/temperament measures.

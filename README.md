# Psychological Mechanisms Map (PMM)

[![Validate PMM](https://github.com/nebuhtit/psychological-mechanisms-map/actions/workflows/validate.yml/badge.svg)](https://github.com/nebuhtit/psychological-mechanisms-map/actions/workflows/validate.yml)
[![Deploy Pages](https://github.com/nebuhtit/psychological-mechanisms-map/actions/workflows/pages.yml/badge.svg)](https://github.com/nebuhtit/psychological-mechanisms-map/actions/workflows/pages.yml)
[![Schema](https://img.shields.io/badge/schema-PMM%20v0.3.4-1f5f4a)](schema/pmm-v0.3.schema.yaml)
[![Data](https://img.shields.io/badge/data-CC--BY--4.0-b46a2a)](README.md#license-and-reuse)

**[Explore the live interactive map](https://nebuhtit.github.io/psychological-mechanisms-map/)** · **[Read the methodology](docs/methodology-v0.3.md)** · **[Inspect the YAML datasets](data/)**

PMM is an open, versioned, evidence-aware ontology and knowledge-graph project for psychological mechanisms. It represents psychological constructs, mental states, behaviors, interventions, measurements, contexts, empirical claims, evidence records, and scientific sources without collapsing them into an ambiguous diagram.

The canonical scientific data is human-editable YAML validated against JSON Schema and semantic rules. Deterministic JSON, JSON-LD, Turtle/RDF, and the interactive website are generated projections rather than independently maintained sources of truth.

PMM is intended for researchers, ontology engineers, computational psychiatry projects, evidence-synthesis tools, and developers building scientifically traceable mental-health knowledge systems.

> [!IMPORTANT]
> PMM is an early research prototype, not a diagnostic system, clinical decision-support tool, treatment recommendation engine, or claim that psychology already has a complete causal map of the mind. Most records have not received independent domain-expert review.

**Current version:** PMM Schema v0.3.4. Version 0.2 is preserved as a historical snapshot, not silently overwritten.

## Why this project exists

Psychology and psychiatry use many diagrams in which boxes and arrows mix fundamentally different things:

- a theoretical construct such as working-memory capacity;
- a momentary state such as anxiety or circulating cortisol;
- an observable behavior such as avoidance;
- a task score or questionnaire;
- a proposed cognitive, learning, social, or physiological mechanism;
- a statistical association;
- a causal intervention effect;
- a paper cited as evidence.

Once these categories are mixed, visual proximity starts to look like scientific proof. PMM addresses this with an **inferential firewall**: ontology objects, structural relations, empirical claims, evidence extractions, and bibliographic sources are represented separately and validated under different constraints.

PMM asks a narrow but demanding question:

> Can a machine-readable map preserve what is measured, what is inferred, what is causally identified, what remains proposed, and exactly which source supports each claim?

## What is currently mapped

The live explorer contains ten deliberately heterogeneous mechanism families. Breadth is used to test the ontology, not to imply comprehensive coverage.

| Family | Scientific boundary tested |
|---|---|
| Threat and avoidance | Threat context, anxiety state, avoidance behavior, relief, omission, contingency, and negative reinforcement |
| Fear extinction | Extinction procedure, response reduction, return of fear, and proposed context-sensitive extinction memory |
| Habit control | Goal-directed and habitual control, outcome devaluation, persistent responding, and failed diagnostic tests |
| Cognitive reappraisal | Instruction, proposed reinterpretation, subjective experience, expression, physiology, BOLD, and statistical mediation |
| Working-memory control | N-back task performance, complex span, backward recall, construct validity, and competing memory mechanisms |
| Interoception and anxiety | Physiology, objective heartbeat-task performance, self-evaluation, metacognition, appraisal, and anxiety |
| Social buffering | Randomized support conditions, cortisol trajectories, developmental context, moderation, and proposed co-regulation |
| Reward prediction error | Computational error, expected value, temporal-difference updating, dopamine activity, neural manipulation, and learned behavior |
| HPA feedback | Cortisol level, ACTH secretory drive, serial assays, pharmacological probes, and multi-site feedback |
| Placebo analgesia | Treatment expectation, pain report, naloxone challenge, dopamine null result, and statistical neural mediation |

Each family is a small evidence pack, not a textbook chapter. Null findings, incompatible operationalizations, alternative explanations, narrow populations, and untested mechanism hypotheses remain visible.

## What makes PMM different

PMM does not attempt to replace established projects. It uses them for complementary purposes while adding claim-level evidence and inferential constraints.

| Existing resource | Primary strength | PMM's complementary role |
|---|---|---|
| [NIMH RDoC](https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc) | Dimensional neurobehavioral domains and units of analysis | Represents scoped mechanism claims and evidence without treating the RDoC matrix as a causal graph |
| [Cognitive Atlas](https://www.cognitiveatlas.org/) | Cognitive concepts, tasks, and assertions | Adds explicit Evidence and Source records plus causal, mediation, moderation, and prediction boundaries |
| Mental Functioning Ontology | Formal ontology of mental functioning | Adds source-specific empirical claims and confidence/provenance fields |
| Neuro Behavior Ontology | Behavioral-process and phenotype vocabulary | Separates behavior topography from experimentally demonstrated function or contingency |
| [HiTOP](https://www.hitop-system.org/) | Hierarchical dimensional psychopathology taxonomy | Keeps covariance-based phenotype structure distinct from mechanisms and causal effects |

External mappings are conservative. An `exact_match` requires a verified stable identifier; similar labels are not enough.

## Core design principles

1. **Human-editable canonical data.** Curators work in modular YAML rather than editing generated graph files.
2. **No causal arrows by implication.** Correlation, prediction, statistical mediation, causal mediation, statistical moderation, causal effect modification, causal effects, and hypotheses have different required fields.
3. **One source-specific extraction per Evidence record.** Multiple experiments, null results, and analysis-sensitive findings remain separate.
4. **Measurements are not constructs.** A task, questionnaire, assay, fitted parameter, or neural recording does not become the thing it operationalizes.
5. **Interventions are not mechanisms.** Dexamethasone challenge, reappraisal instruction, outcome devaluation, or optogenetic stimulation can test a process without being that process.
6. **Computational variables are not neural signals.** Reward prediction error and dopamine activity, for example, remain distinct records connected only by scoped claims.
7. **Uncertainty is explicit.** Confidence is ordinal and justified in text; PMM avoids pseudo-precise truth scores.
8. **Generated views are disposable.** JSON, JSON-LD, Turtle, and website data can be rebuilt deterministically from the canonical registry and YAML.

## Possible uses

- curate a mechanism-centered literature review with traceable claim-to-source links;
- compare how different studies operationalize a nominally similar construct;
- build retrieval-augmented generation systems that distinguish evidence from hypotheses;
- export psychology knowledge to JSON, RDF, JSON-LD, or later OWL-compatible tooling;
- teach causal and ontology modeling using concrete psychology examples;
- identify where a proposed mechanism has only correlational, indirect, or single-source support;
- prototype research interfaces without embedding scientific claims directly in frontend code.

## Non-goals

- diagnosing a person or recommending treatment;
- ranking people, disorders, therapies, or research groups;
- replacing systematic reviews, meta-analyses, clinical guidelines, or expert judgment;
- presenting one grand unified theory of mind;
- converting every statistical association into a graph edge;
- claiming complete or unbiased coverage of psychological science.

## Architecture

```text
schema/pmm-v0.3.schema.yaml          Full JSON Schema Draft 2020-12 contract
vocab/relations-v0.3.yaml           Structural relation vocabulary and type ranges
vocab/evidence-v0.3.yaml            Evidence and causal-support rules
data/pilot-anxiety-avoidance-v0.3.yaml
                                     Corrected anxiety/avoidance pilot
data/stress-test-mechanisms-v0.3.yaml
                                     Four heterogeneous mechanism families
data/evidence-pack-negative-reinforcement-v0.3.yaml
                                     Seven primary-experiment extractions
data/evidence-pack-fear-extinction-v0.3.yaml
                                     Extinction and return-of-fear stress test
docs/fear-extinction-preview.md       Provisional GitHub-rendered diagram
data/evidence-pack-habit-control-v0.3.yaml
                                     Habit and goal-directed control stress test
docs/habit-control-preview.md         Provisional habit-control diagram
data/evidence-pack-cognitive-reappraisal-v0.3.yaml
                                     Reappraisal and multimodal outcome stress test
data/evidence-pack-working-memory-control-v0.3.yaml
                                     N-back construct-validity and competing-mechanism pack
data/evidence-pack-interoception-anxiety-v0.3.yaml
                                     Interoception measurement and anxiety boundary pack
data/evidence-pack-social-buffering-v0.3.yaml
                                     Social context, cortisol, moderation, and causal-contrast pack
data/evidence-pack-reward-prediction-error-v0.3.yaml
                                     Computational error, dopamine, and learning boundary pack
data/evidence-pack-hpa-feedback-v0.3.yaml
                                     Cortisol, ACTH dynamics, probes, and feedback boundary pack
data/evidence-pack-placebo-analgesia-v0.3.yaml
                                     Expectation, pain, pharmacological perturbation, and mediation boundary pack
docs/cognitive-reappraisal-preview.md Provisional reappraisal diagram
docs/methodology-v0.3.md             Scientific semantics and known limits
scripts/pmm_v03.py                   Schema + semantic validation and JSON export
scripts/build_site_data.py           Deterministic interactive-map data bundle
scripts/build_registry.py            Validate/export every registered dataset
data/families.yaml                   Single registry for datasets and public map families
scripts/new_evidence_pack.py         Schema-valid evidence-pack starter generator
site/                                Static interactive map v0.1
graph/pmm-context.jsonld             JSON-LD term and reference mapping
graph/pmm-shapes.ttl                 SHACL inferential constraints
tests/test_pmm_v03.py                Valid and deliberately invalid fixtures
```

PMM separates four layers:

1. **Ontology objects** describe what something is: `Construct`, `Mechanism`, `State`, `Behavior`, `Intervention`, `Measurement`, `Context`, `Event`, `Outcome`, `Contingency`, or `Observation`. `Entity` is an abstract base and cannot be instantiated.
2. **Relations** encode only structural, taxonomic, contextual, temporal, or operational links. They do not encode correlation or causation.
3. **Claims** encode definitions, association, prediction, mediation, moderation, causal effects, and explicitly proposed causal or mechanism hypotheses.
4. **Evidence and Sources** store one source-specific extraction per Evidence record, confidence domains, provenance, and bibliographic identity.

This is an inferential firewall: an arrow cannot silently become a causal statement.

JSON-LD export preserves that firewall by emitting Claims, Evidence, and Sources as separate graph nodes. SHACL mirrors the main causal and statistical constraints; uncertain Claims are not exported as OWL axioms.

### Record model

```text
Ontology object ── structural Relation ── Ontology object
       │                                      │
       └──────────── reified Claim ───────────┘
                              │
                    source-specific Evidence
                              │
                           Source
```

An edge such as `anxiety → avoidance` is therefore insufficient. PMM requires a typed claim with population, context, temporal scope, estimate or causal estimand, assumptions, limitations, evidence IDs, provenance, and confidence rationale as appropriate for the inferential mode.

### Machine-readable formats

- YAML is the canonical curation format.
- JSON is the deterministic application/build format.
- JSON-LD preserves Claims, Evidence, Sources, and identifiers as graph nodes.
- Turtle provides an RDF projection.
- SHACL shapes mirror important graph constraints.
- OWL export is intentionally conservative because uncertain empirical claims should not become unconditional logical axioms.

## Run locally

```bash
make setup
make validate
make test
make export
make verify
python3 -m http.server 8000 --directory site
```

`make setup` creates a local `.venv`. Validation applies the complete JSON Schema and additional cross-record constraints to every dataset in `data/families.yaml`. Export produces deterministic JSON in `build/` and rebuilds the public families declared by the same registry.

GitHub Actions runs `make verify` on every push and pull request. The command validates all v0.3 datasets, runs the test suite, rebuilds JSON, and fails if generated JSON differs from the committed artifacts.

The interactive map is a read-only projection. It exposes object types, reified
Claims, Evidence, confidence, limitations, and source links without converting
visual proximity into a scientific assertion. GitHub Pages deploys the `site/`
directory after changes reach `main`.

English remains the canonical language for identifiers, source records, and editable scientific datasets. The public interface has an `EN`/`RU` switch; Russian is a separate presentation-layer bundle in `site/data/i18n-ru.json`, generated by `scripts/build_ru_translation.py`. The current Russian scientific text is machine-translated and marked as pending expert review. Translation never replaces canonical English data, IDs, quotations, authors, DOI, or URLs.

## Add a new evidence pack

Create a schema-valid starter:

```bash
.venv/bin/python scripts/new_evidence_pack.py \
  cognitive-flexibility \
  "cognitive flexibility" \
  data/evidence-pack-cognitive-flexibility-v0.3.yaml
```

Then:

1. Add ontology objects with narrow definitions and boundary notes.
2. Add structural relations only where no statistical or causal assertion is implied.
3. Extract source-specific Claims, Evidence, and Sources.
4. Register the YAML and generated JSON path in `data/families.yaml`.
5. Run `make validate` and targeted tests.
6. Run `make export` to rebuild graph and website projections.

The registry test fails if a new v0.3 dataset is forgotten, duplicated, or omitted from the automated pipeline.

## ID convention

```text
pmm:<record-kind>:<lowercase-kebab-slug>
```

Example: `pmm:mechanism:negative-reinforcement`. IDs are permanent. Renamed records retain IDs; removed records are deprecated and may identify a successor. External mappings require a resolvable IRI, mapping relation, verification status, access date, and rationale.

## Pilot boundary

The anxiety pilot no longer treats anxiety, uncertain threat, aversive-outcome omission, subjective relief, and negative reinforcement as one kind of thing. It represents:

- RDoC Potential Threat as a `Construct`.
- uncertain threat as a `Context`.
- an anxiety episode and relief as separate `State` types.
- avoidance as `Behavior` whose function requires a demonstrated contingency.
- aversive consequence as `Outcome`, omission as `Event`, and response-consequence dependency as n-ary `Contingency`.
- negative reinforcement as a proposed `Mechanism`, not a synonym for relief.

The controlled causal result is narrowly scoped to an assigned loss-probability experiment. The general clinical maintenance loop remains a falsifiable proposed hypothesis.

## Heterogeneous test

The stress-test dataset checks the same model against proactive interference, temporal-difference value updating, glucocorticoid feedback, and social buffering. It deliberately distinguishes a computational reward-prediction-error variable from dopamine, a performance phenomenon from a retrieval mechanism, a statistical interaction from a causal contrast, and an intervention from its hypothesized mechanism.

## Primary evidence pack

The first evidence pack contains seven source-specific human experimental extractions. Five are kept as separate experiments from Fisher and Urcelay (2024), including a null similar-signal comparison and an analysis-sensitive transfer result. Independent monetary-loss and yoked shock-control paradigms test whether the same ontology survives different operationalizations. The pack does not pool incompatible outcomes or convert neural correlates into causal mechanisms.

The fear-extinction pack separates the extinction procedure from within-session
response decrement, return-of-fear tests, measurements, and a proposed
context-sensitive extinction-memory mechanism. A small
[provisional visual preview](docs/fear-extinction-preview.md) is included for
inspection on GitHub; it is not yet a stable visualization architecture.

The habit-control pack keeps instrumental behavior, current outcome value,
outcome-insensitive response patterns, measurement procedures, and proposed
habitual or goal-directed mechanisms separate. Its
[provisional visual preview](docs/habit-control-preview.md) also displays failed
devaluation as an explicit alternative explanation rather than silently
classifying every persistent response as a habit.

The cognitive-reappraisal pack separates an assigned instruction from proposed
meaning reinterpretation and from subjective, expressive, autonomic, and BOLD
measurements. Statistical neural mediation is recorded explicitly without
upgrading it to causal mediation. See the
[provisional visual preview](docs/cognitive-reappraisal-preview.md).

The working-memory pack separates the N-back task context, behavioral score,
latent construct, lure-induced errors, and competing familiarity-control and
episodic-retrieval accounts. It includes a large preregistered latent-variable
study and does not treat computational sufficiency as proof of human mechanism.

The interoception pack separates physiological activation, objective heartbeat-task
performance, self-evaluated sensibility, metacognitive awareness, and anxiety. It
preserves the meta-analytic null association for objective cardiac accuracy and
marks cardiorespiratory appraisal as an integrative hypothesis rather than mediation.

The social-buffering pack separates randomized support-condition effects from
condition-by-time and developmental-context moderation. Social co-regulation
remains a proposed mechanism because cortisol contrasts do not identify mediation.

The reward-learning pack separates a model-defined prediction error, temporal-
difference updating, phasic dopamine activity, optogenetic manipulation, and
learned behavior. Dopamine evidence is not represented as an identity assertion.

The HPA-feedback pack separates circulating cortisol, ACTH secretory drive,
serial assays, pharmacological perturbations, and multi-site feedback. A
dexamethasone challenge is represented as a probe, not as the mechanism itself.

## Next steps

1. Add independent primary-study replications and preregistered null results to the negative-reinforcement pack.
2. Extend independent SHACL invalid fixtures to prediction, mediation, and moderation.
3. Verify stable external ontology identifiers against pinned RDoC, Cognitive Atlas, MF, NBO, and HiTOP releases before promoting mappings.
4. Decide whether stable nested-resource IRIs are needed before publishing a public RDF endpoint.
5. Request domain-expert review of definitions and causal assumptions before expanding the interface beyond the current exploratory map.

## Contributing

Contributions are useful when they improve scientific traceability rather than merely add nodes.

Good contributions include:

- correcting an ontological category mistake;
- adding a primary-study replication, preregistered null result, or boundary condition;
- separating experiments currently summarized too broadly;
- improving causal assumptions or inferential classification;
- verifying stable external ontology identifiers;
- adding invalid fixtures that catch scientifically misleading modeling;
- improving accessibility, serialization, or deterministic validation.

Before proposing a large expansion, open an issue describing the mechanism family, candidate primary sources, intended claims, key alternative explanations, and which ontology distinctions the family tests. Every causal claim should identify the intervention or identification strategy, temporal order, assumptions, scope, and direct evidence.

## Project status

- **Schema:** active pilot, v0.3.4
- **Canonical language:** English
- **Interface languages:** English and Russian (Russian scientific terminology pending expert review)
- **Public interface:** exploratory read-only map
- **Scientific review:** machine-validated; independent domain-expert review still required
- **Coverage:** selective stress tests, not comprehensive psychology coverage
- **Stability:** IDs are intended to remain stable; schema and vocabularies may still change before v1.0

## Search terms

Psychological ontology, psychology knowledge graph, mental mechanisms, cognitive ontology, computational psychiatry, evidence graph, causal knowledge graph, behavioral science ontology, RDoC, Cognitive Atlas, HiTOP, negative reinforcement, fear extinction, habit learning, cognitive reappraisal, working memory, interoception, social buffering, reward prediction error, dopamine learning, HPA-axis feedback, placebo analgesia, treatment expectation, and endogenous opioid modulation.

## License and reuse

Dataset metadata currently declares `CC-BY-4.0`. Source articles retain their original copyrights; PMM stores bibliographic metadata and concise structured extractions rather than reproducing papers. Before a formal release, the repository should add explicit root-level license files covering data, documentation, and software separately.

If you reuse PMM before a tagged release, cite the repository URL, commit hash, PMM schema version, and access date so the exact evolving dataset can be reconstructed.

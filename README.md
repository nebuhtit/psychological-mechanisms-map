# Psychological Mechanisms Map (PMM)

PMM is a versioned, evidence-aware knowledge model for psychological mechanisms. The canonical source is human-editable YAML; validated JSON is a build artifact for graph and interface projections. An early interactive map is generated from those artifacts rather than maintained as a separate scientific dataset.

**Current version:** PMM Schema v0.3.4. Version 0.2 is preserved as a historical snapshot, not silently overwritten.

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
docs/cognitive-reappraisal-preview.md Provisional reappraisal diagram
docs/methodology-v0.3.md             Scientific semantics and known limits
scripts/pmm_v03.py                   Schema + semantic validation and JSON export
scripts/build_site_data.py           Deterministic interactive-map data bundle
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

## Run locally

```bash
make setup
make validate
make validate-stress
make validate-pack
make validate-extinction
make validate-habit
make validate-reappraisal
make test
make export
make verify
python3 -m http.server 8000 --directory site
```

`make setup` creates a local `.venv`. Validation applies the complete JSON Schema and additional cross-record constraints. Export produces deterministic JSON in `build/`.

GitHub Actions runs `make verify` on every push and pull request. The command validates all v0.3 datasets, runs the test suite, rebuilds JSON, and fails if generated JSON differs from the committed artifacts.

The interactive map is a read-only projection. It exposes object types, reified
Claims, Evidence, confidence, limitations, and source links without converting
visual proximity into a scientific assertion. GitHub Pages deploys the `site/`
directory after changes reach `main`.

The working interface and canonical scientific content are English-only while the model is changing quickly. Localization will be added later as a separate UI layer with an explicit language switch; translated labels must never replace canonical English identifiers or source extractions.

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

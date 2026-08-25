# Psychological Mechanisms Map (PMM)

PMM is a versioned, evidence-aware knowledge model for psychological mechanisms. The canonical source is human-editable YAML; validated JSON is a build artifact for later graph, JSON-LD, RDF, or OWL projections. No visual map is built yet.

**Current version:** PMM Schema v0.3. Version 0.2 is preserved as a historical snapshot, not silently overwritten.

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
docs/methodology-v0.3.md             Scientific semantics and known limits
scripts/pmm_v03.py                   Schema + semantic validation and JSON export
tests/test_pmm_v03.py                Valid and deliberately invalid fixtures
```

PMM separates four layers:

1. **Ontology objects** describe what something is: `Construct`, `Mechanism`, `State`, `Behavior`, `Intervention`, `Measurement`, `Context`, `Event`, `Outcome`, `Contingency`, or `Observation`. `Entity` is an abstract base and cannot be instantiated.
2. **Relations** encode only structural, taxonomic, contextual, temporal, or operational links. They do not encode correlation or causation.
3. **Claims** encode definitions, association, prediction, mediation, moderation, causal effects, and explicitly proposed causal or mechanism hypotheses.
4. **Evidence and Sources** store one source-specific extraction per Evidence record, confidence domains, provenance, and bibliographic identity.

This is an inferential firewall: an arrow cannot silently become a causal statement.

## Run locally

```bash
make setup
make validate
make validate-stress
make validate-pack
make test
make export
make verify
```

`make setup` creates a local `.venv`. Validation applies the complete JSON Schema and additional cross-record constraints. Export produces deterministic JSON in `build/`.

GitHub Actions runs `make verify` on every push and pull request. The command validates all v0.3 datasets, runs the test suite, rebuilds JSON, and fails if generated JSON differs from the committed artifacts.

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

## Next steps

1. Add independent primary-study replications and preregistered null results to the negative-reinforcement pack.
2. Add invalid fixtures for prediction, mediation, moderation, and context-dependent causal claims; then define SHACL-equivalent graph constraints.
3. Verify stable external ontology identifiers against pinned RDoC, Cognitive Atlas, MF, NBO, and HiTOP releases before promoting mappings.
4. Add JSON-LD/RDF export while keeping Claims and Evidence reified; do not translate uncertain empirical claims into OWL class axioms.
5. Request domain-expert review of definitions and causal assumptions before any visualization work.

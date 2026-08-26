# PMM strategy reset: from evidence packs to a mechanism space

## Original project thesis

PMM was conceived as a machine-readable map of psychological mechanisms, not as a visual encyclopedia or a new diagnostic taxonomy. Its distinctive proposition is:

> Represent psychological objects, proposed processes, empirical claims, evidence extractions, and sources separately, then make every scientifically meaningful connection inspectable and falsifiable.

The first anxiety and avoidance pilot expressed this as a pathway: threat context and anxiety state, avoidance behavior, aversive-outcome reduction, and negative reinforcement must remain distinct rather than becoming one informal arrow.

## Critical assessment of the current direction

The project has successfully built an inferential firewall, executable validation, human-editable YAML, graph exports, ten heterogeneous evidence packs, and a usable bilingual explorer. Those are real foundations.

However, PMM currently behaves more like ten separate evidence-pack demonstrations than one map of mechanisms. The family switcher hides cross-family comparison, and there are no explicit bridge records between related objects. Adding more families under this structure would increase volume without necessarily increasing integration.

The curation protocol and social-buffering screening pilot are useful quality controls, but they should not become the main product. Repeating a near-systematic review manually for every mechanism would be too slow, would duplicate mature evidence-synthesis workflows, and still would not solve PMM's central integration problem.

## Revised product thesis

PMM should be developed as an **evidence-addressable mechanism layer** that can sit above established ontologies, literature databases, and systematic reviews. Its unique value is not owning all source discovery. Its value is preserving the path:

```text
mechanism or object
  -> scoped empirical Claim
  -> source-specific Evidence extraction
  -> scientific Source
```

External reviews and databases may supply source sets. PMM must model what those sources do and do not license.

## Two development tracks

1. **Product track:** global mechanism index, explicit cross-family bridge semantics, queries, comparison views, and interoperable exports.
2. **Quality track:** sampled independent review, design-specific risk-of-bias fields, search logs, and expert terminology review.

The quality track gates public certainty claims, but it must not block all ontology and product development.

## Immediate stage

Build a global mechanism index from canonical family data and expose it in JSON, Markdown, and the website. The index must show definitions, mechanism kinds, linked Claim types and statuses, Evidence counts, and Source counts without implying that similarly named mechanisms are identical or connected.

This stage is complete when:

- every public Mechanism appears exactly once in the generated index;
- every count is derived deterministically from canonical PMM records;
- a visitor can open the index, compare mechanisms, and jump to the corresponding family record;
- the interface explicitly says that counts are traceability metadata rather than evidence scores;
- no cross-family equivalence or causal edge is inferred from label similarity.

## Next decision after this stage

Audit potential cross-family bridges and add a small, source-backed bridge vocabulary (`exact_match`, `close_match`, `broader_match`, `narrower_match`, `related_match`). Do not add causal predicates to that vocabulary. Only after this audit should PMM add further mechanism families.

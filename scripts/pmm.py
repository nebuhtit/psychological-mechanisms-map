#!/usr/bin/env python3
"""Validate PMM YAML and export it deterministically to JSON."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(
    r"^pmm:(dataset|entity|mechanism|state|behavior|intervention|measurement|context|"
    r"relation|claim|evidence|source):[a-z0-9]+(?:-[a-z0-9]+)*$"
)
TYPE_PREFIX = {
    "Entity": "entity",
    "Mechanism": "mechanism",
    "State": "state",
    "Behavior": "behavior",
    "Intervention": "intervention",
    "Measurement": "measurement",
    "Context": "context",
}
INFERENCE_REQUIRED = {
    "correlation": {"exposure_id", "outcome_id", "association_estimate", "confounding_note"},
    "prediction": {"exposure_id", "outcome_id", "validation_strategy", "predictive_metric"},
    "mediation": {
        "exposure_id",
        "mediator_id",
        "outcome_id",
        "indirect_effect",
        "mediation_path",
        "temporal_ordering",
    },
    "moderation": {"exposure_id", "moderator_id", "outcome_id", "interaction_term"},
    "causation": {
        "exposure_id",
        "outcome_id",
        "causal_estimand",
        "identification_strategy",
        "temporal_ordering",
        "causal_assumptions",
    },
}
EMPIRICAL_SCOPES = {"empirical", "integrative"}
CAUSAL_PREDICATES = {"causes", "prevents", "reinforces"}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: top-level YAML value must be an object")
    return value


def require_keys(record: dict[str, Any], keys: set[str], where: str, errors: list[str]) -> None:
    missing = sorted(key for key in keys if key not in record)
    if missing:
        errors.append(f"{where}: missing required fields: {', '.join(missing)}")


def collect_records(document: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for section in ("objects", "relations", "claims", "evidence", "sources"):
        values = document.get(section)
        if not isinstance(values, list):
            errors.append(f"{section}: must be a list")
            continue
        for index, record in enumerate(values):
            where = f"{section}[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{where}: must be an object")
                continue
            record_id = record.get("id")
            if not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
                errors.append(f"{where}: invalid PMM id {record_id!r}")
                continue
            if record_id in records:
                errors.append(f"{where}: duplicate id {record_id}")
            records[record_id] = record
    return records


def expect_ref(
    value: Any,
    records: dict[str, dict[str, Any]],
    where: str,
    errors: list[str],
    prefix: str | None = None,
) -> None:
    if not isinstance(value, str) or value not in records:
        errors.append(f"{where}: unresolved reference {value!r}")
    elif prefix and not value.startswith(f"pmm:{prefix}:"):
        errors.append(f"{where}: expected pmm:{prefix}: reference, got {value}")


def expect_refs(
    values: Any,
    records: dict[str, dict[str, Any]],
    where: str,
    errors: list[str],
    prefix: str | None = None,
) -> None:
    if not isinstance(values, list):
        errors.append(f"{where}: must be a list")
        return
    if len(values) != len(set(str(value) for value in values)):
        errors.append(f"{where}: contains duplicate references")
    for index, value in enumerate(values):
        expect_ref(value, records, f"{where}[{index}]", errors, prefix)


def validate(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require_keys(
        document,
        {
            "pmm_version",
            "document_type",
            "dataset_id",
            "metadata",
            "namespaces",
            "objects",
            "relations",
            "claims",
            "evidence",
            "sources",
        },
        "document",
        errors,
    )
    if document.get("pmm_version") != "0.2.0":
        errors.append("document: pmm_version must be the string '0.2.0'")
    if document.get("document_type") != "pmm_dataset":
        errors.append("document: document_type must be pmm_dataset")
    dataset_id = document.get("dataset_id")
    if not isinstance(dataset_id, str) or not dataset_id.startswith("pmm:dataset:"):
        errors.append("document: dataset_id must use pmm:dataset:<slug>")

    # Parsing these files catches broken schema/vocabulary edits as part of every run.
    schema = load_yaml(ROOT / "schema" / "pmm-v0.2.schema.yaml")
    relation_vocab = load_yaml(ROOT / "vocab" / "relations.yaml")
    load_yaml(ROOT / "vocab" / "evidence.yaml")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema: expected JSON Schema draft 2020-12")

    predicate_defs = {
        item["id"]: item
        for item in relation_vocab.get("predicates", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    records = collect_records(document, errors)

    for index, obj in enumerate(document.get("objects", [])):
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            continue
        where = f"objects[{index}] ({obj['id']})"
        require_keys(obj, {"type", "label", "definition", "knowledge_status", "provenance"}, where, errors)
        expected_prefix = TYPE_PREFIX.get(obj.get("type"))
        if expected_prefix is None:
            errors.append(f"{where}: unknown object type {obj.get('type')!r}")
        elif not obj["id"].startswith(f"pmm:{expected_prefix}:"):
            errors.append(f"{where}: id prefix does not match type {obj.get('type')}")
        for field in ("input_ids", "output_ids", "target_ids"):
            if field in obj:
                expect_refs(obj[field], records, f"{where}.{field}", errors)
        for mapping_index, mapping in enumerate(obj.get("external_mappings", [])):
            mapping_where = f"{where}.external_mappings[{mapping_index}]"
            if not isinstance(mapping, dict):
                errors.append(f"{mapping_where}: must be an object")
                continue
            if mapping.get("mapping_relation") == "exact_match" and mapping.get("mapping_status") != "verified":
                errors.append(f"{mapping_where}: exact_match requires mapping_status=verified")

    for index, relation in enumerate(document.get("relations", [])):
        if not isinstance(relation, dict) or not isinstance(relation.get("id"), str):
            continue
        where = f"relations[{index}] ({relation['id']})"
        require_keys(relation, {"subject_id", "predicate", "object_id", "epistemic_scope", "provenance"}, where, errors)
        expect_ref(relation.get("subject_id"), records, f"{where}.subject_id", errors)
        expect_ref(relation.get("object_id"), records, f"{where}.object_id", errors)
        predicate = relation.get("predicate")
        predicate_def = predicate_defs.get(predicate)
        if predicate_def is None:
            errors.append(f"{where}: predicate {predicate!r} is not in vocab/relations.yaml")
        claim_ids = relation.get("claim_ids", [])
        if relation.get("epistemic_scope") in EMPIRICAL_SCOPES and not claim_ids:
            errors.append(f"{where}: empirical/integrative relation requires claim_ids")
        expect_refs(claim_ids, records, f"{where}.claim_ids", errors, "claim")
        if "context_ids" in relation:
            expect_refs(relation["context_ids"], records, f"{where}.context_ids", errors, "context")
        linked_inferences = {
            records[claim_id].get("inference_type")
            for claim_id in claim_ids
            if claim_id in records
        }
        allowed = set(predicate_def.get("allowed_inference_types", [])) if predicate_def else set()
        if allowed and linked_inferences and not linked_inferences.issubset(allowed):
            errors.append(
                f"{where}: linked inference types {sorted(linked_inferences)} are not allowed for {predicate}"
            )
        if predicate in CAUSAL_PREDICATES and linked_inferences != {"causation"}:
            errors.append(f"{where}: {predicate} requires only causation claims")

    for index, claim in enumerate(document.get("claims", [])):
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str):
            continue
        where = f"claims[{index}] ({claim['id']})"
        require_keys(
            claim,
            {"statement", "inference_type", "knowledge_status", "confidence", "scope", "evidence_ids", "provenance"},
            where,
            errors,
        )
        inference_type = claim.get("inference_type")
        if inference_type not in {"descriptive", *INFERENCE_REQUIRED.keys()}:
            errors.append(f"{where}: unsupported inference_type {inference_type!r}")
        else:
            require_keys(claim, INFERENCE_REQUIRED.get(inference_type, set()), where, errors)
        for field in ("exposure_id", "outcome_id", "mediator_id", "moderator_id"):
            if field in claim:
                expect_ref(claim[field], records, f"{where}.{field}", errors)
        expect_refs(claim.get("evidence_ids", []), records, f"{where}.evidence_ids", errors, "evidence")
        scope = claim.get("scope", {})
        if isinstance(scope, dict):
            expect_refs(scope.get("context_ids", []), records, f"{where}.scope.context_ids", errors, "context")
        if claim.get("knowledge_status") == "proposed_integrative":
            integrated = claim.get("integrated_claim_ids", [])
            if not isinstance(integrated, list) or len(integrated) < 2:
                errors.append(f"{where}: proposed_integrative requires at least two integrated_claim_ids")
            else:
                expect_refs(integrated, records, f"{where}.integrated_claim_ids", errors, "claim")
            if not claim.get("falsifiable_boundary"):
                errors.append(f"{where}: proposed_integrative requires falsifiable_boundary")
        if inference_type == "causation" and claim.get("knowledge_status") != "proposed_integrative":
            evidence_ids = claim.get("evidence_ids", [])
            if not any(records.get(item, {}).get("causal_support") is True for item in evidence_ids):
                errors.append(f"{where}: established/supported causation requires causal_support evidence")

    for index, evidence in enumerate(document.get("evidence", [])):
        if not isinstance(evidence, dict) or not isinstance(evidence.get("id"), str):
            continue
        where = f"evidence[{index}] ({evidence['id']})"
        require_keys(
            evidence,
            {
                "claim_ids",
                "source_ids",
                "evidence_kind",
                "design",
                "population",
                "supports_inference",
                "domains",
                "causal_support",
                "summary",
                "provenance",
            },
            where,
            errors,
        )
        expect_refs(evidence.get("claim_ids", []), records, f"{where}.claim_ids", errors, "claim")
        expect_refs(evidence.get("source_ids", []), records, f"{where}.source_ids", errors, "source")
        if evidence.get("causal_support") is True and evidence.get("supports_inference") != "causation":
            errors.append(f"{where}: causal_support=true requires supports_inference=causation")

    # Require bidirectional claim/evidence links so updates cannot silently orphan support.
    for claim in document.get("claims", []):
        if not isinstance(claim, dict):
            continue
        for evidence_id in claim.get("evidence_ids", []):
            if claim.get("id") not in records.get(evidence_id, {}).get("claim_ids", []):
                errors.append(f"{claim.get('id')}: evidence {evidence_id} does not link back to the claim")
    for evidence in document.get("evidence", []):
        if not isinstance(evidence, dict):
            continue
        for claim_id in evidence.get("claim_ids", []):
            if evidence.get("id") not in records.get(claim_id, {}).get("evidence_ids", []):
                errors.append(f"{evidence.get('id')}: claim {claim_id} does not link back to the evidence")

    return errors


def validate_path(path: Path) -> dict[str, Any]:
    document = load_yaml(path)
    errors = validate(document)
    if errors:
        raise ValidationError("\n".join(f"- {error}" for error in errors))
    return document


def export_json(source: Path, destination: Path) -> None:
    document = validate_path(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def clean_build(path: Path) -> None:
    resolved = path.resolve()
    expected = (ROOT / "build").resolve()
    if resolved != expected:
        raise ValidationError(f"refusing to clean anything except {expected}")
    if resolved.exists():
        shutil.rmtree(resolved)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a PMM YAML document")
    validate_parser.add_argument("source", type=Path)

    export_parser = subparsers.add_parser("export", help="validate and export YAML to JSON")
    export_parser.add_argument("source", type=Path)
    export_parser.add_argument("destination", type=Path)

    clean_parser = subparsers.add_parser("clean", help="remove only the repository build directory")
    clean_parser.add_argument("path", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "validate":
            document = validate_path(args.source)
            print(
                f"valid: {args.source} "
                f"({len(document['objects'])} objects, {len(document['claims'])} claims, "
                f"{len(document['evidence'])} evidence records)"
            )
        elif args.command == "export":
            export_json(args.source, args.destination)
            print(f"exported: {args.destination}")
        elif args.command == "clean":
            clean_build(args.path)
            print(f"cleaned: {(ROOT / 'build').resolve()}")
    except (OSError, yaml.YAMLError, ValidationError) as exc:
        print(f"validation failed:\n{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

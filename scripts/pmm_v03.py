#!/usr/bin/env python3
"""Validate PMM v0.3 YAML and export deterministic JSON."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "pmm-v0.3.schema.yaml"
RELATIONS_PATH = ROOT / "vocab" / "relations-v0.3.yaml"
EVIDENCE_PATH = ROOT / "vocab" / "evidence-v0.3.yaml"

TYPE_PREFIX = {
    "Construct": "construct",
    "Mechanism": "mechanism",
    "State": "state",
    "Behavior": "behavior",
    "Intervention": "intervention",
    "Measurement": "measurement",
    "Context": "context",
    "Event": "event",
    "Outcome": "outcome",
    "Contingency": "contingency",
    "Observation": "observation",
}

OBJECT_REF_FIELDS = {
    "target_ids",
    "participant_ids",
    "antecedent_ids",
}
SINGLE_OBJECT_REF_FIELDS = {
    "response_id",
    "consequence_id",
    "measurement_id",
    "observed_object_id",
}
CLAIM_OBJECT_REF_FIELDS = {
    "defined_object_id",
    "exposure_id",
    "outcome_id",
    "mediator_id",
    "moderator_id",
    "mechanism_id",
}
EMPIRICAL_CLAIM_TYPES = {
    "association",
    "prediction",
    "mediation",
    "moderation",
    "causal_effect",
}
EVIDENCE_COMPATIBILITY = {
    "association": {"association", "causal_effect"},
    "prediction": {"prediction"},
    "mediation": {"mediation"},
    "moderation": {"moderation"},
    "causal_effect": {"causal_effect"},
    "causal_hypothesis": {"association", "causal_effect", "mechanism"},
    "mechanism_hypothesis": {"mechanism", "causal_effect"},
}


class ValidationError(Exception):
    """Raised when a PMM document violates schema or semantic constraints."""


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: top-level YAML value must be an object")
    return value


def format_jsonschema_error(error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "document"
    return f"{location}: {error.message}"


def validate_json_schema(document: dict[str, Any]) -> list[str]:
    schema = load_yaml(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        format_jsonschema_error(error)
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def collect_records(document: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for section in ("objects", "relations", "claims", "evidence", "sources"):
        for index, record in enumerate(document.get(section, [])):
            if not isinstance(record, dict):
                continue
            record_id = record.get("id")
            if not isinstance(record_id, str):
                continue
            if record_id in records:
                errors.append(f"{section}[{index}]: duplicate id {record_id}")
            records[record_id] = record
    return records


def expect_ref(
    value: Any,
    records: dict[str, dict[str, Any]],
    expected_prefix: str,
    where: str,
    errors: list[str],
) -> None:
    if not isinstance(value, str) or value not in records:
        errors.append(f"{where}: unresolved reference {value!r}")
    elif not value.startswith(f"pmm:{expected_prefix}:"):
        errors.append(f"{where}: expected pmm:{expected_prefix}: reference, got {value}")


def expect_refs(
    values: Any,
    records: dict[str, dict[str, Any]],
    expected_prefix: str,
    where: str,
    errors: list[str],
) -> None:
    if not isinstance(values, list):
        return
    for index, value in enumerate(values):
        expect_ref(value, records, expected_prefix, f"{where}[{index}]", errors)


def expect_object_ref(
    value: Any,
    object_types: dict[str, str],
    where: str,
    errors: list[str],
) -> None:
    if not isinstance(value, str) or value not in object_types:
        errors.append(f"{where}: unresolved object reference {value!r}")


def validate_semantics(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    relation_vocab = load_yaml(RELATIONS_PATH)
    load_yaml(EVIDENCE_PATH)
    records = collect_records(document, errors)

    objects = [record for record in document.get("objects", []) if isinstance(record, dict)]
    object_types = {
        record["id"]: record["type"]
        for record in objects
        if isinstance(record.get("id"), str) and isinstance(record.get("type"), str)
    }
    predicates = {
        record["id"]: record
        for record in relation_vocab.get("predicates", [])
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }

    for index, obj in enumerate(objects):
        object_id = obj.get("id")
        object_type = obj.get("type")
        where = f"objects[{index}] ({object_id})"
        expected_prefix = TYPE_PREFIX.get(object_type)
        if expected_prefix and not str(object_id).startswith(f"pmm:{expected_prefix}:"):
            errors.append(f"{where}: id prefix does not match type {object_type}")

        for field in OBJECT_REF_FIELDS:
            for ref_index, value in enumerate(obj.get(field, [])):
                expect_object_ref(value, object_types, f"{where}.{field}[{ref_index}]", errors)
        for field in SINGLE_OBJECT_REF_FIELDS:
            if field in obj:
                expect_object_ref(obj[field], object_types, f"{where}.{field}", errors)
        for binding_index, binding in enumerate(obj.get("role_bindings", [])):
            if isinstance(binding, dict):
                expect_object_ref(
                    binding.get("object_id"),
                    object_types,
                    f"{where}.role_bindings[{binding_index}].object_id",
                    errors,
                )
        for mapping_index, mapping in enumerate(obj.get("external_mappings", [])):
            if not isinstance(mapping, dict):
                continue
            if (
                mapping.get("mapping_relation") == "exact_match"
                and mapping.get("mapping_status") != "identifier_verified"
            ):
                errors.append(
                    f"{where}.external_mappings[{mapping_index}]: "
                    "exact_match requires mapping_status=identifier_verified"
                )

    for index, relation in enumerate(document.get("relations", [])):
        if not isinstance(relation, dict):
            continue
        relation_id = relation.get("id")
        where = f"relations[{index}] ({relation_id})"
        subject_id = relation.get("subject_id")
        object_id = relation.get("object_id")
        expect_object_ref(subject_id, object_types, f"{where}.subject_id", errors)
        expect_object_ref(object_id, object_types, f"{where}.object_id", errors)
        predicate = predicates.get(relation.get("predicate"))
        if predicate and subject_id in object_types and object_id in object_types:
            subject_type = object_types[subject_id]
            object_type = object_types[object_id]
            if subject_type not in predicate.get("subject_types", []):
                errors.append(
                    f"{where}: {relation.get('predicate')} does not allow subject type {subject_type}"
                )
            if object_type not in predicate.get("object_types", []):
                errors.append(
                    f"{where}: {relation.get('predicate')} does not allow object type {object_type}"
                )
            if predicate.get("claim_required") and not relation.get("claim_ids"):
                errors.append(f"{where}: predicate {relation.get('predicate')} requires claim_ids")
        expect_refs(relation.get("claim_ids", []), records, "claim", f"{where}.claim_ids", errors)
        expect_refs(relation.get("context_ids", []), records, "context", f"{where}.context_ids", errors)

        if relation.get("predicate") == "instantiates":
            subject = records.get(subject_id, {})
            target = records.get(object_id, {})
            if subject.get("ontological_level") != "instance":
                errors.append(f"{where}: instantiates subject must have ontological_level=instance")
            if target.get("ontological_level") != "type":
                errors.append(f"{where}: instantiates object must have ontological_level=type")
        if relation.get("predicate") == "is_a":
            if records.get(subject_id, {}).get("ontological_level") != "type":
                errors.append(f"{where}: is_a subject must have ontological_level=type")
            if records.get(object_id, {}).get("ontological_level") != "type":
                errors.append(f"{where}: is_a object must have ontological_level=type")

    for index, claim in enumerate(document.get("claims", [])):
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("id")
        claim_type = claim.get("claim_type")
        where = f"claims[{index}] ({claim_id})"
        for field in CLAIM_OBJECT_REF_FIELDS:
            if field in claim:
                expect_object_ref(claim[field], object_types, f"{where}.{field}", errors)
        expect_refs(claim.get("source_ids", []), records, "source", f"{where}.source_ids", errors)
        expect_refs(claim.get("evidence_ids", []), records, "evidence", f"{where}.evidence_ids", errors)
        expect_refs(
            claim.get("integrated_claim_ids", []),
            records,
            "claim",
            f"{where}.integrated_claim_ids",
            errors,
        )
        scope = claim.get("scope", {})
        if isinstance(scope, dict):
            expect_refs(scope.get("context_ids", []), records, "context", f"{where}.scope.context_ids", errors)

        evidence_ids = claim.get("evidence_ids", [])
        if claim_type == "definition" and evidence_ids:
            errors.append(f"{where}: definitions cite source_ids directly and must not grade evidence_ids")
        if claim_type in EMPIRICAL_CLAIM_TYPES and claim.get("epistemic_status") != "not_assessed" and not evidence_ids:
            errors.append(f"{where}: assessed empirical claim requires evidence_ids")
        if claim_type == "causal_effect":
            direct = any(
                records.get(evidence_id, {}).get("causal_support") == "direct"
                and records.get(evidence_id, {}).get("inference_support") == "causal_effect"
                for evidence_id in evidence_ids
            )
            if not direct:
                errors.append(f"{where}: causal_effect requires linked direct causal evidence")

        allowed_support = EVIDENCE_COMPATIBILITY.get(claim_type)
        if allowed_support:
            for evidence_id in evidence_ids:
                support = records.get(evidence_id, {}).get("inference_support")
                if support is not None and support not in allowed_support:
                    errors.append(
                        f"{where}: evidence {evidence_id} with inference_support={support} "
                        f"is incompatible with claim_type={claim_type}"
                    )

    for index, evidence in enumerate(document.get("evidence", [])):
        if not isinstance(evidence, dict):
            continue
        evidence_id = evidence.get("id")
        where = f"evidence[{index}] ({evidence_id})"
        expect_refs(evidence.get("claim_ids", []), records, "claim", f"{where}.claim_ids", errors)
        expect_ref(evidence.get("source_id"), records, "source", f"{where}.source_id", errors)
        if evidence.get("causal_support") == "direct" and evidence.get("inference_support") != "causal_effect":
            errors.append(f"{where}: causal_support=direct requires inference_support=causal_effect")

    # Backlinks are intentionally redundant so edits cannot silently orphan support.
    for claim in document.get("claims", []):
        if not isinstance(claim, dict):
            continue
        for evidence_id in claim.get("evidence_ids", []):
            if claim.get("id") not in records.get(evidence_id, {}).get("claim_ids", []):
                errors.append(f"{claim.get('id')}: evidence {evidence_id} does not link back")
    for evidence in document.get("evidence", []):
        if not isinstance(evidence, dict):
            continue
        for claim_id in evidence.get("claim_ids", []):
            if evidence.get("id") not in records.get(claim_id, {}).get("evidence_ids", []):
                errors.append(f"{evidence.get('id')}: claim {claim_id} does not link back")

    return errors


def validate(document: dict[str, Any]) -> list[str]:
    return validate_json_schema(document) + validate_semantics(document)


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

    validate_parser = subparsers.add_parser("validate", help="validate a PMM v0.3 YAML document")
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
    except (OSError, SchemaError, yaml.YAMLError, ValidationError) as exc:
        print(f"validation failed:\n{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

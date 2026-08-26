#!/usr/bin/env python3
"""Validate PMM curation protocols and search logs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "curation-v0.1.schema.yaml"
CURATION_ROOT = ROOT / "curation"


class CurationValidationError(Exception):
    """Raised when a curation document violates schema or semantic rules."""


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CurationValidationError(f"{path}: top-level YAML value must be an object")
    return value


def schema_errors(document: dict[str, Any]) -> list[str]:
    schema = load_yaml(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "document"
        context = "; ".join(child.message for child in error.context[:3])
        errors.append(f"{location}: {context or error.message}")
    return errors


def unique_by_id(items: list[dict[str, Any]], label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in indexed:
            errors.append(f"{label}[{index}]: duplicate id {item_id}")
        indexed[item_id] = item
    return indexed


def load_linked_records(relative_path: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    path = (ROOT / relative_path).resolve()
    if ROOT not in path.parents or not path.is_file():
        errors.append(f"linked_dataset: missing or unsafe path {relative_path}")
        return {}
    document = load_yaml(path)
    return {
        record["id"]: record
        for section in ("sources", "evidence")
        for record in document.get(section, [])
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }


def load_search_snapshot(search: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    relative_path = search.get("export_file")
    if not isinstance(relative_path, str):
        return {}
    path = (ROOT / relative_path).resolve()
    if ROOT not in path.parents or not path.is_file():
        errors.append(f"{search.get('id')}: missing or unsafe export_file {relative_path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{search.get('id')}: invalid search snapshot: {error}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{search.get('id')}: search snapshot must be a JSON object")
        return {}
    return value


def validate_log(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    information_sources = unique_by_id(document.get("information_sources", []), "information_sources", errors)
    searches = unique_by_id(document.get("searches", []), "searches", errors)
    records = unique_by_id(document.get("records", []), "records", errors)
    linked_records = load_linked_records(document.get("linked_dataset", ""), errors)
    snapshots: dict[str, dict[str, Any]] = {}

    for search_id, search in searches.items():
        if search.get("information_source_id") not in information_sources:
            errors.append(f"{search_id}: unresolved information_source_id {search.get('information_source_id')}")
        if search.get("result_count_status") == "recorded":
            snapshot = load_search_snapshot(search, errors)
            snapshots[search_id] = snapshot
            pmids = snapshot.get("pmids", [])
            if snapshot.get("search_id") != search_id:
                errors.append(f"{search_id}: snapshot search_id does not match")
            if snapshot.get("query") != search.get("strategy"):
                errors.append(f"{search_id}: snapshot query does not match strategy")
            if snapshot.get("result_count") != search.get("result_count"):
                errors.append(f"{search_id}: snapshot result_count does not match log")
            if len(pmids) != search.get("result_count") or len(pmids) != len(set(pmids)):
                errors.append(f"{search_id}: snapshot PMID count is incomplete or duplicated")

    deduplication_keys: dict[str, str] = {}
    for record_id, record in records.items():
        for search_id in record.get("discovered_by", []):
            if search_id not in searches:
                errors.append(f"{record_id}: unresolved discovered_by search {search_id}")
                continue
            search = searches[search_id]
            if search.get("result_count_status") == "recorded" and record.get("identifiers", {}).get("pmid"):
                snapshot = snapshots.get(search_id, {})
                if record["identifiers"]["pmid"] not in snapshot.get("pmids", []):
                    errors.append(f"{record_id}: PMID is absent from snapshot for {search_id}")

        deduplication_key = record.get("deduplication_key")
        if isinstance(deduplication_key, str):
            previous = deduplication_keys.get(deduplication_key)
            if previous:
                errors.append(f"{record_id}: duplicate deduplication_key also used by {previous}")
            deduplication_keys[deduplication_key] = record_id

        for field in ("linked_source_id",):
            linked_id = record.get(field)
            if linked_id and linked_id not in linked_records:
                errors.append(f"{record_id}: unresolved {field} {linked_id}")
        for evidence_id in record.get("linked_evidence_ids", []):
            if evidence_id not in linked_records:
                errors.append(f"{record_id}: unresolved linked evidence {evidence_id}")

        decisions = record.get("reviewer_decisions", [])
        reviewer_stage_pairs = [(item.get("reviewer"), item.get("stage")) for item in decisions]
        if len(reviewer_stage_pairs) != len(set(reviewer_stage_pairs)):
            errors.append(f"{record_id}: a reviewer may submit only one decision per stage")

        status = record.get("screening_status")
        full_text_includes = {
            item.get("reviewer")
            for item in decisions
            if item.get("stage") == "full_text" and item.get("decision") == "include"
        }
        if status == "included":
            if len(full_text_includes) < 2:
                errors.append(f"{record_id}: included records require two independent full-text include decisions")
            if record.get("consensus", {}).get("decision") != "include":
                errors.append(f"{record_id}: included records require include consensus")

        if status == "excluded" and any(item.get("stage") == "full_text" for item in decisions):
            full_text_reviewers = {
                item.get("reviewer") for item in decisions if item.get("stage") == "full_text"
            }
            if len(full_text_reviewers) < 2:
                errors.append(f"{record_id}: full-text exclusions require two independent reviewers")

    if document.get("status") == "complete":
        unfinished = [
            record_id
            for record_id, record in records.items()
            if record.get("screening_status") in {"awaiting_screening", "awaiting_full_text", "provisionally_included"}
        ]
        if unfinished:
            errors.append(f"complete log has unfinished records: {', '.join(sorted(unfinished))}")
        uncounted = [search_id for search_id, search in searches.items() if search.get("result_count_status") != "recorded"]
        if uncounted:
            errors.append(f"complete log has searches without recorded hit counts: {', '.join(sorted(uncounted))}")
    return errors


def validate_document(document: dict[str, Any]) -> list[str]:
    errors = schema_errors(document)
    if errors:
        return errors
    if document.get("document_type") == "curation_log":
        errors.extend(validate_log(document))
    return errors


def validate_path(path: Path) -> None:
    document = load_yaml(path)
    errors = validate_document(document)
    if errors:
        raise CurationValidationError("\n".join(f"- {error}" for error in errors))


def curation_paths() -> list[Path]:
    return [CURATION_ROOT / "protocol-v0.1.yaml", *sorted((CURATION_ROOT / "logs").glob("*.yaml"))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate",))
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or curation_paths()
    try:
        for path in paths:
            validate_path(path)
            print(f"valid: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    except (OSError, SchemaError, yaml.YAMLError, CurationValidationError) as error:
        print(f"curation validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

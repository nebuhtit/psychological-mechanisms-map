#!/usr/bin/env python3
"""Build the compact data bundle consumed by the PMM browser."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from claim_explanations import load_annotations, validate as validate_explanations


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "data" / "pmm-data.json"
REGISTRY_PATH = ROOT / "data" / "families.yaml"
VIEWS_PATH = ROOT / "data" / "navigation-views-v0.1.yaml"


def load_families() -> list[tuple[str, str, str, str]]:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return [
        (entry["family"]["id"], entry["family"]["title"], entry["output"], entry["family"]["description"])
        for entry in registry["datasets"]
        if "family" in entry
    ]


def compact_provenance(record: dict[str, Any]) -> dict[str, Any]:
    provenance = record.get("provenance", {})
    return {
        key: provenance[key]
        for key in ("record_version", "review_status", "source_snapshot_date")
        if key in provenance
    }


def compact_record(record: dict[str, Any]) -> dict[str, Any]:
    omitted = {"provenance", "causal_assumptions"}
    compact = {key: value for key, value in record.items() if key not in omitted}
    provenance = compact_provenance(record)
    if provenance:
        compact["provenance"] = provenance
    return compact


def build_family(
    family_id: str,
    title: str,
    relative_path: str,
    description: str,
    explanations: dict[str, dict[str, str]],
) -> dict[str, Any]:
    path = ROOT / relative_path
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        "id": family_id,
        "title": title,
        "description": description,
        "dataset_id": document["dataset_id"],
        "version": document["pmm_version"],
        "objects": [compact_record(item) for item in document["objects"]],
        "relations": [compact_record(item) for item in document["relations"]],
        "claims": [
            {
                **compact_record(item),
                "plain_language_summary": explanations[item["id"]]["en"],
                "plain_language_review_status": "source_checked_editorial",
            }
            for item in document["claims"]
        ],
        "evidence": [compact_record(item) for item in document["evidence"]],
        "sources": [compact_record(item) for item in document["sources"]],
    }


def build_mechanism_index(families: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build a cross-family inventory without asserting cross-family identity."""
    index: list[dict[str, Any]] = []
    role_fields = (
        "exposure_id",
        "mechanism_id",
        "mediator_id",
        "moderator_id",
        "outcome_id",
        "defined_object_id",
    )

    for family in families:
        evidence_by_id = {item["id"]: item for item in family["evidence"]}
        for mechanism in (item for item in family["objects"] if item["type"] == "Mechanism"):
            claims = [
                claim
                for claim in family["claims"]
                if mechanism["id"] in {claim.get(field) for field in role_fields}
            ]
            evidence_ids = sorted(
                {
                    evidence_id
                    for claim in claims
                    for evidence_id in claim.get("evidence_ids", [])
                }
            )
            source_ids = sorted(
                {
                    evidence_by_id[evidence_id]["source_id"]
                    for evidence_id in evidence_ids
                    if evidence_id in evidence_by_id
                }
            )
            status_counts: dict[str, int] = {}
            for claim in claims:
                status = claim["epistemic_status"]
                status_counts[status] = status_counts.get(status, 0) + 1

            index.append(
                {
                    "id": mechanism["id"],
                    "family_id": family["id"],
                    "family_title": family["title"],
                    "label": mechanism["label"],
                    "definition": mechanism["definition"],
                    "mechanism_kind": mechanism["mechanism_kind"],
                    "curation_status": mechanism["curation_status"],
                    "claim_ids": sorted(claim["id"] for claim in claims),
                    "claim_types": sorted({claim["claim_type"] for claim in claims}),
                    "claim_status_counts": dict(sorted(status_counts.items())),
                    "evidence_count": len(evidence_ids),
                    "source_count": len(source_ids),
                }
            )

    return sorted(index, key=lambda item: (item["family_title"], item["label"]))


def load_navigation_views(families: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate faceted navigation against canonical PMM records."""
    document = yaml.safe_load(VIEWS_PATH.read_text(encoding="utf-8"))
    family_by_id = {family["id"]: family for family in families}
    source_ids = {source["id"] for source in document["sources"]}

    def validate_sources(owner: str, references: list[str]) -> None:
        missing = set(references) - source_ids
        if missing:
            raise ValueError(f"{owner}: unknown navigation source IDs: {sorted(missing)}")

    def validate_membership(owner: str, membership: dict[str, Any]) -> None:
        family_id = membership["family_id"]
        if family_id not in family_by_id:
            raise ValueError(f"{owner}: unknown family {family_id}")
        records = {
            item["id"]: item
            for section in ("objects", "claims")
            for item in family_by_id[family_id][section]
        }
        canonical_id = membership["canonical_id"]
        if canonical_id not in records:
            raise ValueError(f"{owner}: {canonical_id} is not in family {family_id}")
        expected_type = membership.get("expected_type")
        if expected_type and records[canonical_id].get("type") != expected_type:
            raise ValueError(
                f"{owner}: expected {canonical_id} to be {expected_type}, "
                f"found {records[canonical_id].get('type')}"
            )

    general = document["general_psychology"]
    nodes = general["nodes"]
    node_ids = {node["id"] for node in nodes}
    if len(node_ids) != len(nodes):
        raise ValueError("general_psychology: duplicate node IDs")
    if general["root_id"] not in node_ids:
        raise ValueError("general_psychology: root_id does not resolve")
    for node in nodes:
        parent_id = node.get("parent_id")
        if parent_id is not None and parent_id not in node_ids:
            raise ValueError(f"{node['id']}: unknown parent {parent_id}")
        validate_sources(node["id"], node.get("source_ids", []))
        for membership in node.get("memberships", []):
            validate_membership(node["id"], membership)

    systems = document["scientific_systems"]["systems"]
    for system in systems:
        validate_sources(system["id"], system.get("source_ids", []))
        for membership in system.get("mapped_memberships", []):
            validate_membership(system["id"], membership)

    return document


def main() -> None:
    explanation_errors = validate_explanations()
    if explanation_errors:
        raise ValueError("invalid Claim explanations:\n" + "\n".join(explanation_errors))
    explanations = load_annotations()
    families = [build_family(*family, explanations) for family in load_families()]
    payload = {
        "pmm_version": "0.3.4",
        "interface_version": "0.5.0",
        "families": families,
        "mechanism_index": build_mechanism_index(families),
        "navigation_views": load_navigation_views(families),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"built: {OUTPUT.relative_to(ROOT)} "
        f"({len(payload['families'])} families, {len(payload['mechanism_index'])} mechanisms)"
    )


if __name__ == "__main__":
    main()

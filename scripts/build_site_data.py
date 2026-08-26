#!/usr/bin/env python3
"""Build the compact data bundle consumed by the PMM browser."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "data" / "pmm-data.json"
REGISTRY_PATH = ROOT / "data" / "families.yaml"


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
        "claims": [compact_record(item) for item in document["claims"]],
        "evidence": [compact_record(item) for item in document["evidence"]],
        "sources": [compact_record(item) for item in document["sources"]],
    }


def main() -> None:
    payload = {
        "pmm_version": "0.3.4",
        "interface_version": "0.3.0",
        "families": [build_family(*family) for family in load_families()],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"built: {OUTPUT.relative_to(ROOT)} ({len(payload['families'])} families)")


if __name__ == "__main__":
    main()

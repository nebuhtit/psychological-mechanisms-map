#!/usr/bin/env python3
"""Validate or export every PMM dataset declared in the registry."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

import build_site_data
import build_coverage_report
import pmm_v03


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "families.yaml"


def load_registry() -> list[dict]:
    document = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    datasets = document.get("datasets") if isinstance(document, dict) else None
    if not isinstance(datasets, list) or not datasets:
        raise pmm_v03.ValidationError("registry must contain a non-empty datasets list")

    sources: set[str] = set()
    outputs: set[str] = set()
    family_ids: set[str] = set()
    for index, entry in enumerate(datasets):
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), str):
            raise pmm_v03.ValidationError(f"datasets[{index}] must declare source")
        if not isinstance(entry.get("output"), str):
            raise pmm_v03.ValidationError(f"datasets[{index}] must declare output")
        source = entry["source"]
        output = entry["output"]
        if source in sources or output in outputs:
            raise pmm_v03.ValidationError(f"datasets[{index}] duplicates source or output")
        sources.add(source)
        outputs.add(output)
        family = entry.get("family")
        if family is not None:
            if not isinstance(family, dict) or not all(
                isinstance(family.get(field), str) and family[field]
                for field in ("id", "title", "description")
            ):
                raise pmm_v03.ValidationError(f"datasets[{index}].family is incomplete")
            if family["id"] in family_ids:
                raise pmm_v03.ValidationError(f"duplicate family id: {family['id']}")
            family_ids.add(family["id"])
    return datasets


def validate_all(datasets: list[dict]) -> None:
    for entry in datasets:
        source = ROOT / entry["source"]
        pmm_v03.validate_path(source)
        print(f"valid: {entry['source']}")


def export_all(datasets: list[dict]) -> None:
    for entry in datasets:
        pmm_v03.export_json(ROOT / entry["source"], ROOT / entry["output"])
    pmm_v03.export_jsonld(
        ROOT / "data/pilot-anxiety-avoidance-v0.3.yaml",
        ROOT / "build/pilot-anxiety-avoidance-v0.3.jsonld",
    )
    pmm_v03.export_turtle(
        ROOT / "data/pilot-anxiety-avoidance-v0.3.yaml",
        ROOT / "build/pilot-anxiety-avoidance-v0.3.ttl",
    )
    build_site_data.main()
    build_coverage_report.main()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "export", "report"))
    args = parser.parse_args()
    try:
        datasets = load_registry()
        if args.command == "validate":
            validate_all(datasets)
        elif args.command == "export":
            export_all(datasets)
        else:
            build_coverage_report.main()
    except (OSError, pmm_v03.ValidationError) as error:
        print(f"registry build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create a minimal, schema-valid PMM evidence-pack starter."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import yaml


def build_starter(slug: str, title: str, timestamp: datetime) -> dict:
    iso_time = timestamp.isoformat()
    snapshot_date = timestamp.date().isoformat()
    return {
        "pmm_version": "0.3.4",
        "document_type": "pmm_dataset",
        "dataset_id": f"pmm:dataset:{slug}-primary-evidence-v0-3",
        "metadata": {
            "title": f"Primary evidence pack for {title}",
            "description": f"Curated source-specific evidence records for {title}.",
            "status": "draft",
            "language": "en",
            "license": "CC-BY-4.0",
            "schema_path": "schema/pmm-v0.3.schema.yaml",
            "provenance": {
                "record_version": "0.1.0",
                "created_at": iso_time,
                "modified_at": iso_time,
                "created_by": ["PMM evidence-pack generator"],
                "review_status": "unreviewed",
                "source_snapshot_date": snapshot_date,
            },
        },
        "namespaces": {
            "pmm": "https://pmm.local/id/",
            "doi": "https://doi.org/",
            "pmid": "https://pubmed.ncbi.nlm.nih.gov/",
        },
        "objects": [],
        "relations": [],
        "claims": [],
        "evidence": [],
        "sources": [],
    }


def write_starter(slug: str, title: str, destination: Path, timestamp: datetime) -> dict:
    """Write a starter without replacing an existing curation file."""
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    document = build_starter(slug, title, timestamp)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="lowercase kebab-case topic slug")
    parser.add_argument("title", help="human-readable topic title")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        write_starter(args.slug, args.title, args.destination, datetime.now().astimezone())
    except FileExistsError as error:
        parser.error(str(error))
    print(f"created: {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

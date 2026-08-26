#!/usr/bin/env python3
"""Validate source-checked plain-language annotations for every PMM Claim."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ANNOTATIONS_PATH = ROOT / "data" / "claim-explanations.yaml"
REGISTRY_PATH = ROOT / "data" / "families.yaml"

FORBIDDEN_TEMPLATES = (
    "может вызывать изменение",
    "may cause a change in",
    "one factor",
    "один фактор",
)


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def registered_claims() -> dict[str, dict[str, Any]]:
    registry = read_yaml(REGISTRY_PATH)
    claims: dict[str, dict[str, Any]] = {}
    for dataset in registry["datasets"]:
        document = read_yaml(ROOT / dataset["source"])
        for claim in document["claims"]:
            if claim["id"] in claims:
                raise ValueError(f"duplicate registered Claim: {claim['id']}")
            claims[claim["id"]] = claim
    return claims


def load_annotations() -> dict[str, dict[str, str]]:
    document = read_yaml(ANNOTATIONS_PATH)
    entries = document.get("entries", [])
    annotations: dict[str, dict[str, str]] = {}
    for entry in entries:
        claim_id = entry.get("claim_id")
        if claim_id in annotations:
            raise ValueError(f"duplicate explanation: {claim_id}")
        annotations[claim_id] = entry
    return annotations


def validate() -> list[str]:
    claims = registered_claims()
    annotations = load_annotations()
    errors: list[str] = []

    missing = sorted(set(claims) - set(annotations))
    extra = sorted(set(annotations) - set(claims))
    errors.extend(f"missing explanation: {claim_id}" for claim_id in missing)
    errors.extend(f"unknown explanation Claim: {claim_id}" for claim_id in extra)

    for claim_id in sorted(set(claims) & set(annotations)):
        claim = claims[claim_id]
        entry = annotations[claim_id]
        for language in ("en", "ru"):
            value = entry.get(language, "").strip()
            if len(value) < 80:
                errors.append(f"{claim_id}: {language} explanation is too short")
            if value == claim["statement"]:
                errors.append(f"{claim_id}: {language} repeats the canonical statement")
            lowered = value.casefold()
            for fragment in FORBIDDEN_TEMPLATES:
                if fragment.casefold() in lowered:
                    errors.append(f"{claim_id}: {language} contains forbidden generic template {fragment!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"valid: {len(load_annotations())} source-checked bilingual Claim explanations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

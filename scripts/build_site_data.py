#!/usr/bin/env python3
"""Build the compact data bundle consumed by the PMM browser."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "data" / "pmm-data.json"
FAMILIES = (
    (
        "avoidance",
        "Threat and avoidance",
        "build/pilot-anxiety-avoidance-v0.3.json",
        "How threat, action, omission, relief, and reinforcement remain distinct.",
    ),
    (
        "extinction",
        "Fear extinction",
        "build/evidence-pack-fear-extinction-v0.3.json",
        "Why response reduction is not the same as erasure or extinction memory.",
    ),
    (
        "habit",
        "Habit control",
        "build/evidence-pack-habit-control-v0.3.json",
        "Goal-directed and habitual control with failed devaluation kept visible.",
    ),
    (
        "reappraisal",
        "Cognitive reappraisal",
        "build/evidence-pack-cognitive-reappraisal-v0.3.json",
        "Instruction, proposed reinterpretation, experience, physiology, and BOLD.",
    ),
    (
        "working-memory",
        "Working-memory control",
        "build/evidence-pack-working-memory-control-v0.3.json",
        "N-back performance, construct validity, lure interference, and competing memory mechanisms.",
    ),
    (
        "interoception",
        "Interoception and anxiety",
        "build/evidence-pack-interoception-anxiety-v0.3.json",
        "Bodily physiology, objective performance, self-evaluation, metacognition, and anxiety kept distinct.",
    ),
    (
        "social-buffering",
        "Social buffering",
        "build/evidence-pack-social-buffering-v0.3.json",
        "Randomized support conditions, cortisol trajectories, developmental context, and proposed co-regulation.",
    ),
    (
        "reward-learning",
        "Reward prediction error",
        "build/evidence-pack-reward-prediction-error-v0.3.json",
        "Model-defined error, value updating, dopamine signals, neural manipulation, and learned behavior.",
    ),
    (
        "hpa-feedback",
        "HPA feedback",
        "build/evidence-pack-hpa-feedback-v0.3.json",
        "Cortisol levels, ACTH secretory dynamics, pharmacological probes, and multi-site feedback.",
    ),
)


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
        "interface_version": "0.2.0",
        "families": [build_family(*family) for family in FAMILIES],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"built: {OUTPUT.relative_to(ROOT)} ({len(payload['families'])} families)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Export the generated cross-family mechanism inventory as JSON and Markdown."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "data" / "pmm-data.json"
JSON_OUTPUT = ROOT / "build" / "mechanism-index.json"
MARKDOWN_OUTPUT = ROOT / "docs" / "mechanism-index.md"


def main() -> None:
    payload = json.loads(SITE_DATA.read_text(encoding="utf-8"))
    mechanisms = payload["mechanism_index"]
    output = {
        "pmm_version": payload["pmm_version"],
        "generated_from": "site/data/pmm-data.json",
        "interpretation_warning": (
            "This is a cross-family inventory, not an assertion that similarly named "
            "mechanisms are identical or causally connected."
        ),
        "mechanisms": mechanisms,
    }
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# PMM mechanism index",
        "",
        "This generated index makes mechanisms comparable across public evidence packs. "
        "It does **not** assert that similarly named mechanisms are identical, that every "
        "mechanism is established, or that families are causally connected.",
        "",
        f"**Current inventory:** {len(mechanisms)} mechanisms across {len(payload['families'])} families.",
        "",
        "| Family | Mechanism | Kind | Linked claims | Evidence | Sources |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for mechanism in mechanisms:
        lines.append(
            "| {family} | **{label}**<br>{definition} | {kind} | {claims} | {evidence} | {sources} |".format(
                family=mechanism["family_title"],
                label=mechanism["label"],
                definition=mechanism["definition"],
                kind=mechanism["mechanism_kind"],
                claims=len(mechanism["claim_ids"]),
                evidence=mechanism["evidence_count"],
                sources=mechanism["source_count"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `Linked claims` counts scoped PMM Claims in which the mechanism occupies an explicit role.",
            "- `Evidence` counts unique source-specific Evidence records cited by those Claims.",
            "- `Sources` counts unique publications behind those Evidence records.",
            "- Counts measure modeled traceability, not truth, effect size, consensus, or importance.",
            "- Cross-family equivalence and broader/narrower mappings require explicit future bridge records.",
            "",
        ]
    )
    MARKDOWN_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"built: {JSON_OUTPUT.relative_to(ROOT)}")
    print(f"built: {MARKDOWN_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

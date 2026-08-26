from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteBundleTests(unittest.TestCase):
    def test_site_bundle_contains_expected_families(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        self.assertEqual(
            [item["id"] for item in document["families"]],
            ["avoidance", "extinction", "habit", "reappraisal", "working-memory", "interoception", "social-buffering"],
        )
        self.assertTrue(
            all(item["version"] == document["pmm_version"] for item in document["families"])
        )

    def test_site_bundle_references_resolve_within_each_family(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        for family in document["families"]:
            records = {
                item["id"]
                for section in ("objects", "claims", "evidence", "sources")
                for item in family[section]
            }
            for claim in family["claims"]:
                for field in ("exposure_id", "mechanism_id", "mediator_id", "moderator_id", "outcome_id"):
                    if field in claim:
                        self.assertIn(claim[field], records)
                for evidence_id in claim.get("evidence_ids", []):
                    self.assertIn(evidence_id, records)

    def test_site_has_no_inline_scientific_dataset(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text()
        self.assertIn('const DATA_URL = "data/pmm-data.json";', javascript)
        self.assertNotIn("pmm:evidence:", javascript)

    def test_interface_source_is_english_only(self) -> None:
        interface = "\n".join(
            (ROOT / "site" / filename).read_text(encoding="utf-8")
            for filename in ("index.html", "app.js")
        )
        self.assertIsNone(re.search(r"[А-Яа-яЁё]", interface))

    def test_reading_guide_is_collapsed_and_explains_visual_encoding(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.assertIn('<details class="map-guide">', page)
        self.assertNotIn('<details class="map-guide" open>', page)
        for phrase in ("How to read this map", "Claim colours", "Lines and interaction"):
            self.assertIn(phrase, page)


if __name__ == "__main__":
    unittest.main()

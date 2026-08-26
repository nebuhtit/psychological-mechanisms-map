from __future__ import annotations

import copy
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import curation  # noqa: E402
import screening  # noqa: E402


PACKET_PATH = ROOT / "curation" / "review-packets" / "social-buffering-title-abstract-v0.1.json"
REVIEW_A_PATH = ROOT / "curation" / "reviews" / "social-buffering-reviewer-a-v0.1.yaml"


class ScreeningWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = screening.read_json(PACKET_PATH)
        self.review_a = curation.load_yaml(REVIEW_A_PATH)

    def test_packet_is_complete_and_blinded(self) -> None:
        self.assertEqual(len(self.packet["records"]), 51)
        self.assertTrue(all(record["abstract_status"] == "available" for record in self.packet["records"]))
        self.assertTrue(all("authors" not in record and "journal" not in record for record in self.packet["records"]))
        self.assertTrue(all("decision" not in record for record in self.packet["records"]))

    def test_reviewer_a_is_complete_and_schema_valid(self) -> None:
        self.assertEqual(screening.validate_review(self.review_a, self.packet), [])
        self.assertEqual(self.review_a["status"], "complete")
        counts = Counter(item["decision"] for item in self.review_a["decisions"])
        self.assertEqual(counts, {"include": 10, "uncertain": 3, "exclude": 38})

    def test_complete_review_rejects_missing_decisions(self) -> None:
        pending = screening.new_review(
            self.packet,
            "test-reviewer",
            "pmm:screening-review:test-reviewer-v0-1",
            "2026-08-26T12:00:00+03:00",
        )
        with self.assertRaises(ValueError):
            screening.complete_review(pending, {}, "2026-08-26T12:01:00+03:00")

    def test_agreement_requires_no_pending_decisions(self) -> None:
        pending = copy.deepcopy(self.review_a)
        pending["decisions"][0]["decision"] = "pending"
        with self.assertRaises(ValueError):
            screening.agreement(self.review_a, pending)

    def test_abstract_snapshot_matches_search_snapshot(self) -> None:
        search = json.loads((ROOT / "curation" / "exports" / "pubmed-social-buffering-cortisol-youth-2026-08-26.json").read_text())
        abstracts = json.loads((ROOT / "curation" / "exports" / "pubmed-social-buffering-cortisol-youth-2026-08-26-abstracts.json").read_text())
        self.assertEqual(abstracts["source_search_id"], search["search_id"])
        self.assertEqual([record["pmid"] for record in abstracts["records"]], search["pmids"])


if __name__ == "__main__":
    unittest.main()

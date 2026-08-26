from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import curation  # noqa: E402
import pubmed_search  # noqa: E402


LOG_PATH = ROOT / "curation" / "logs" / "social-buffering-retrospective-v0.1.yaml"
SEARCH_ID = "search:pubmed-social-buffering-cortisol-youth-2026-08-26"


class PubMedSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.log = curation.load_yaml(LOG_PATH)
        self.search = pubmed_search.find_search(self.log, SEARCH_ID)
        self.snapshot = json.loads((ROOT / self.search["export_file"]).read_text(encoding="utf-8"))

    def test_snapshot_matches_committed_search(self) -> None:
        self.assertEqual(self.snapshot["database"], "PubMed")
        self.assertEqual(self.snapshot["search_id"], SEARCH_ID)
        self.assertEqual(self.snapshot["query"], self.search["strategy"])
        self.assertEqual(self.snapshot["result_count"], self.search["result_count"])
        self.assertEqual(len(self.snapshot["pmids"]), self.snapshot["result_count"])
        self.assertEqual(len(set(self.snapshot["pmids"])), self.snapshot["result_count"])
        self.assertEqual(
            {record["pmid"] for record in self.snapshot["records"]},
            set(self.snapshot["pmids"]),
        )

    def test_every_snapshot_record_is_in_screening_queue(self) -> None:
        queued_pmids = {
            record["identifiers"]["pmid"]
            for record in self.log["records"]
            if "pmid" in record["identifiers"]
        }
        self.assertTrue(set(self.snapshot["pmids"]).issubset(queued_pmids))
        self.assertEqual(
            sum(record["screening_status"] == "awaiting_screening" for record in self.log["records"]),
            45,
        )

    def test_sync_is_idempotent(self) -> None:
        before = len(self.log["records"])
        pubmed_search.sync_log(self.log, self.search, self.snapshot)
        self.assertEqual(len(self.log["records"]), before)

    def test_snapshot_cannot_be_silently_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.json"
            pubmed_search.write_snapshot({"result_count": 1}, path)
            pubmed_search.write_snapshot({"result_count": 1}, path)
            with self.assertRaises(FileExistsError):
                pubmed_search.write_snapshot({"result_count": 2}, path)


if __name__ == "__main__":
    unittest.main()

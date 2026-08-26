from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import curation  # noqa: E402


class CurationProtocolTests(unittest.TestCase):
    def test_all_curation_documents_validate(self) -> None:
        paths = curation.curation_paths()
        self.assertGreaterEqual(len(paths), 2)
        for path in paths:
            with self.subTest(path=path):
                curation.validate_path(path)

    def test_pilot_is_explicitly_incomplete_and_has_unmapped_candidates(self) -> None:
        path = ROOT / "curation" / "logs" / "social-buffering-retrospective-v0.1.yaml"
        document = curation.load_yaml(path)
        self.assertEqual(document["status"], "pilot")
        self.assertTrue(any("must not be described as a systematic review" in gap for gap in document["known_gaps"]))
        self.assertGreaterEqual(
            sum(record["screening_status"] == "awaiting_full_text" for record in document["records"]),
            4,
        )

    def test_single_reviewer_cannot_finalize_inclusion(self) -> None:
        path = ROOT / "curation" / "logs" / "social-buffering-retrospective-v0.1.yaml"
        document = curation.load_yaml(path)
        invalid = copy.deepcopy(document)
        record = invalid["records"][0]
        record["screening_status"] = "included"
        record["reviewer_decisions"][0]["stage"] = "full_text"
        record["consensus"] = {
            "decision": "include",
            "resolved_by": ["OpenAI Codex"],
            "resolved_at": "2026-08-26T11:50:00+03:00",
            "rationale": "Deliberately invalid one-reviewer fixture.",
        }
        errors = curation.validate_document(invalid)
        self.assertTrue(any("two independent full-text" in error for error in errors), errors)

    def test_complete_log_requires_recorded_search_counts(self) -> None:
        path = ROOT / "curation" / "logs" / "social-buffering-retrospective-v0.1.yaml"
        document = curation.load_yaml(path)
        document["status"] = "complete"
        errors = curation.validate_document(document)
        self.assertTrue(any("without recorded hit counts" in error for error in errors), errors)
        self.assertTrue(any("unfinished records" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()

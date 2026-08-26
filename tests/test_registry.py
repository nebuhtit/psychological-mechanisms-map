from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_registry  # noqa: E402
import build_coverage_report  # noqa: E402


class DatasetRegistryTests(unittest.TestCase):
    def test_registry_is_structurally_valid(self) -> None:
        datasets = build_registry.load_registry()
        self.assertGreaterEqual(len(datasets), 11)

    def test_every_v03_dataset_is_registered(self) -> None:
        datasets = build_registry.load_registry()
        registered = {entry["source"] for entry in datasets}
        discovered = {
            str(path.relative_to(ROOT))
            for path in (ROOT / "data").glob("*v0.3.yaml")
        }
        self.assertEqual(registered, discovered)

    def test_every_registered_source_and_generated_output_exists(self) -> None:
        for entry in build_registry.load_registry():
            self.assertTrue((ROOT / entry["source"]).is_file(), entry["source"])
            self.assertTrue((ROOT / entry["output"]).is_file(), entry["output"])

    def test_coverage_report_counts_public_families_and_flags_review_work(self) -> None:
        report = build_coverage_report.build_report()
        public = [entry for entry in build_registry.load_registry() if "family" in entry]
        self.assertEqual(report["family_count"], len(public))
        self.assertEqual(report["totals"]["claims"], sum(item["claims"] for item in report["families"]))
        self.assertGreater(report["claim_types"].get("causal_effect", 0), 0)
        self.assertGreater(report["claim_types"].get("mechanism_hypothesis", 0), 0)
        self.assertTrue(any("proposed claim" in item["reasons"] for item in report["review_queue"]))


if __name__ == "__main__":
    unittest.main()

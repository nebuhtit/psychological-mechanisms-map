from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_registry  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()

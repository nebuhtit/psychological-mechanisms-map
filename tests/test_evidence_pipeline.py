from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import new_evidence_pack  # noqa: E402
import pmm_v03  # noqa: E402


class EvidencePackPipelineTests(unittest.TestCase):
    def test_generated_starter_is_schema_valid(self) -> None:
        document = new_evidence_pack.build_starter(
            "interoception",
            "interoception",
            datetime(2026, 8, 26, tzinfo=timezone.utc),
        )
        self.assertEqual(pmm_v03.validate(document), [])

    def test_generator_refuses_to_overwrite_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "existing.yaml"
            destination.write_text("curated: true\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                new_evidence_pack.write_starter(
                    "interoception",
                    "interoception",
                    destination,
                    datetime(2026, 8, 26, tzinfo=timezone.utc),
                )
            self.assertEqual(destination.read_text(encoding="utf-8"), "curated: true\n")


if __name__ == "__main__":
    unittest.main()

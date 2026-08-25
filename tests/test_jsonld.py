from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pmm_v03  # noqa: E402


class JSONLDExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = ROOT / "data" / "pilot-anxiety-avoidance-v0.3.yaml"

    def export(self) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "pilot.jsonld"
            pmm_v03.export_jsonld(self.source, destination)
            return json.loads(destination.read_text(encoding="utf-8"))

    def test_export_reifies_every_record(self) -> None:
        source = pmm_v03.load_yaml(self.source)
        graph = self.export()
        expected_count = sum(
            len(source[section])
            for section in ("objects", "relations", "claims", "evidence", "sources")
        )
        self.assertEqual(len(graph["@graph"]), expected_count)
        self.assertEqual(graph["@id"], source["dataset_id"])
        self.assertNotIn("id", graph["@graph"][0])

    def test_claims_and_evidence_remain_separate_nodes(self) -> None:
        nodes = {node["@id"]: node for node in self.export()["@graph"]}
        claim = nodes["pmm:claim:assigned-loss-probability-changes-choice"]
        evidence_id = claim["evidence_ids"][0]
        self.assertEqual(claim["@type"], "Claim")
        self.assertEqual(nodes[evidence_id]["@type"], "Evidence")
        self.assertIn(claim["@id"], nodes[evidence_id]["claim_ids"])

    def test_context_declares_all_validator_reference_fields(self) -> None:
        context = json.loads((ROOT / "graph" / "pmm-context.jsonld").read_text())["@context"]
        reference_fields = (
            pmm_v03.OBJECT_REF_FIELDS
            | pmm_v03.SINGLE_OBJECT_REF_FIELDS
            | pmm_v03.CLAIM_OBJECT_REF_FIELDS
            | {
                "claim_ids", "context_ids", "evidence_ids", "integrated_claim_ids",
                "source_id", "source_ids", "subject_id", "object_id",
            }
        )
        self.assertTrue(reference_fields.issubset(context))

    def test_shacl_keeps_inferential_modes_explicit(self) -> None:
        shapes = (ROOT / "graph" / "pmm-shapes.ttl").read_text(encoding="utf-8")
        for term in ("causal_effect", "prediction", "mediation", "moderation"):
            self.assertIn(term, shapes)


if __name__ == "__main__":
    unittest.main()

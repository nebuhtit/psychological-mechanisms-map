from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pmm  # noqa: E402


class PMMValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm.load_yaml(ROOT / "data" / "pilot-anxiety-avoidance.yaml")

    def test_pilot_is_valid(self) -> None:
        self.assertEqual(pmm.validate(copy.deepcopy(self.document)), [])

    def test_empirical_relation_requires_claim(self) -> None:
        document = copy.deepcopy(self.document)
        document["relations"][0].pop("claim_ids")
        errors = pmm.validate(document)
        self.assertTrue(any("requires claim_ids" in error for error in errors))

    def test_causal_predicate_rejects_noncausal_claim(self) -> None:
        document = copy.deepcopy(self.document)
        reinforcing_relation = next(
            relation for relation in document["relations"] if relation["predicate"] == "reinforces"
        )
        reinforcing_relation["claim_ids"] = ["pmm:claim:anxiety-avoidance-association"]
        errors = pmm.validate(document)
        self.assertTrue(any("reinforces requires only causation claims" in error for error in errors))

    def test_integrative_claim_requires_falsifiable_boundary(self) -> None:
        document = copy.deepcopy(self.document)
        integrative_claim = next(
            claim for claim in document["claims"] if claim["knowledge_status"] == "proposed_integrative"
        )
        integrative_claim.pop("falsifiable_boundary")
        errors = pmm.validate(document)
        self.assertTrue(any("requires falsifiable_boundary" in error for error in errors))

    def test_unresolved_reference_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["relations"][0]["object_id"] = "pmm:state:not-present"
        errors = pmm.validate(document)
        self.assertTrue(any("unresolved reference" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

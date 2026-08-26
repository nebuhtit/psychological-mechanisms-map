from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pmm_v03  # noqa: E402


class PMMV03ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(ROOT / "data" / "pilot-anxiety-avoidance-v0.3.yaml")

    def test_pilot_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_schema_forbids_causal_fields_on_association(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "association")
        claim["causal_estimand"] = "An invalid causal interpretation"
        self.assertTrue(pmm_v03.validate(document))

    def test_abstract_entity_cannot_be_instantiated(self) -> None:
        document = copy.deepcopy(self.document)
        document["objects"][0]["type"] = "Entity"
        document["objects"][0]["id"] = "pmm:entity:invalid"
        self.assertTrue(pmm_v03.validate(document))

    def test_relation_domain_and_range_are_checked(self) -> None:
        document = copy.deepcopy(self.document)
        measured_by = next(item for item in document["relations"] if item["predicate"] == "measured_by")
        measured_by["object_id"] = "pmm:behavior:avoidance-response"
        errors = pmm_v03.validate(document)
        self.assertTrue(any("does not allow object type Behavior" in error for error in errors))

    def test_causal_effect_requires_direct_evidence(self) -> None:
        document = copy.deepcopy(self.document)
        evidence = next(item for item in document["evidence"] if item["causal_support"] == "direct")
        evidence["causal_support"] = "indirect"
        errors = pmm_v03.validate(document)
        self.assertTrue(any("requires linked direct causal evidence" in error for error in errors))

    def test_causal_effect_requires_boundary_conditions(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "causal_effect")
        claim["scope"].pop("boundary_conditions")
        errors = pmm_v03.validate(document)
        self.assertTrue(any("requires explicit scope.boundary_conditions" in error for error in errors))

    def test_supported_prediction_rejects_resubstitution(self) -> None:
        document = copy.deepcopy(self.document)
        source_claim = next(item for item in document["claims"] if item["claim_type"] == "association")
        prediction = copy.deepcopy(source_claim)
        prediction.update(
            {
                "id": "pmm:claim:invalid-resubstitution-prediction",
                "claim_type": "prediction",
                "epistemic_status": "supported",
                "validation_design": "resubstitution",
                "validation_strategy": "Performance estimated on model-development observations.",
                "data_separation_note": "No separation between development and evaluation data.",
                "predictive_metric": prediction.pop("estimate"),
            }
        )
        prediction.pop("confounding_note")
        document["claims"].append(prediction)
        for evidence_id in prediction["evidence_ids"]:
            evidence = next(item for item in document["evidence"] if item["id"] == evidence_id)
            evidence["claim_ids"].append(prediction["id"])
            evidence["inference_support"] = "prediction"
        errors = pmm_v03.validate(document)
        self.assertTrue(any("requires validation beyond resubstitution" in error for error in errors))

    def test_unassessed_temporal_prediction_is_representable(self) -> None:
        document = copy.deepcopy(self.document)
        source_claim = next(item for item in document["claims"] if item["claim_type"] == "association")
        prediction = copy.deepcopy(source_claim)
        predictive_metric = prediction.pop("estimate")
        prediction.pop("confounding_note")
        prediction.update(
            {
                "id": "pmm:claim:prospective-avoidance-prediction",
                "claim_type": "prediction",
                "statement": "Anxiety-state measurement may predict later avoidance in a temporally held-out evaluation set.",
                "epistemic_status": "not_assessed",
                "validation_design": "temporal_holdout",
                "validation_strategy": "Fit on earlier observations and evaluate once on later observations.",
                "data_separation_note": "Later outcomes are unavailable during model development.",
                "predictive_metric": predictive_metric,
                "evidence_ids": [],
            }
        )
        document["claims"].append(prediction)
        self.assertEqual(pmm_v03.validate(document), [])

    def test_exact_external_mapping_requires_verified_identifier(self) -> None:
        document = copy.deepcopy(self.document)
        mapping = document["objects"][0]["external_mappings"][0]
        mapping["mapping_relation"] = "exact_match"
        errors = pmm_v03.validate(document)
        self.assertTrue(any("identifier_verified" in error for error in errors))

    def test_evidence_backlink_is_checked(self) -> None:
        document = copy.deepcopy(self.document)
        document["evidence"][0]["claim_ids"] = []
        errors = pmm_v03.validate(document)
        self.assertTrue(any("does not link back" in error for error in errors))


class PrimaryEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-negative-reinforcement-v0.3.yaml"
        )

    def test_primary_evidence_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_pack_preserves_separate_experiments(self) -> None:
        self.assertEqual(len(self.document["evidence"]), 7)
        self.assertTrue(all(item["source_id"] for item in self.document["evidence"]))

    def test_pack_preserves_challenging_and_mixed_results(self) -> None:
        directions = {item["support_direction"] for item in self.document["evidence"]}
        self.assertIn("challenges", directions)
        self.assertIn("mixed", directions)

    def test_every_causal_effect_has_direct_evidence(self) -> None:
        evidence = {item["id"]: item for item in self.document["evidence"]}
        causal_claims = [
            item for item in self.document["claims"] if item["claim_type"] == "causal_effect"
        ]
        for claim in causal_claims:
            self.assertTrue(
                any(evidence[item]["causal_support"] == "direct" for item in claim["evidence_ids"])
            )


class FearExtinctionEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-fear-extinction-v0.3.yaml"
        )

    def test_fear_extinction_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_procedure_behavior_and_mechanism_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:intervention:cue-only-extinction-procedure"], "Intervention")
        self.assertEqual(records["pmm:behavior:within-session-response-decrement"], "Behavior")
        self.assertEqual(records["pmm:mechanism:extinction-memory-formation"], "Mechanism")

    def test_registered_null_is_preserved(self) -> None:
        evidence = next(
            item
            for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:chalkia-2020-registered-replication"
        )
        self.assertEqual(evidence["support_direction"], "challenges")
        self.assertEqual(evidence["effect"]["direction"], "null")


class HabitControlEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-habit-control-v0.3.yaml"
        )

    def test_habit_control_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_response_pattern_is_not_typed_as_mechanism(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:behavior:outcome-insensitive-responding"], "Behavior")
        self.assertEqual(records["pmm:mechanism:habitual-action-control"], "Mechanism")

    def test_null_replications_are_preserved(self) -> None:
        replication_ids = {
            "pmm:evidence:pool-2022-multilab-training",
            "pmm:evidence:smeets-2023-replication-1",
            "pmm:evidence:smeets-2023-replication-2",
        }
        records = {item["id"]: item for item in self.document["evidence"]}
        for evidence_id in replication_ids:
            self.assertEqual(records[evidence_id]["support_direction"], "challenges")
            self.assertEqual(records[evidence_id]["effect"]["direction"], "null")


class CognitiveReappraisalEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-cognitive-reappraisal-v0.3.yaml"
        )

    def test_cognitive_reappraisal_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_emotion_channels_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:state:negative-emotional-experience"], "State")
        self.assertEqual(records["pmm:state:autonomic-emotional-reactivity"], "State")
        self.assertEqual(records["pmm:behavior:emotion-expressive-behavior"], "Behavior")

    def test_neural_mediation_is_not_marked_direct_causal(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:neural-response-statistically-mediates-reappraisal"
        )
        evidence = next(
            item
            for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:wager-2008-neural-mediation"
        )
        self.assertEqual(claim["mediation_inference"], "statistical")
        self.assertEqual(evidence["inference_support"], "mediation")
        self.assertEqual(evidence["causal_support"], "indirect")

    def test_statistical_mediation_rejects_causal_fields(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "mediation")
        claim["causal_estimand"] = "Invalid path-specific causal effect"
        self.assertTrue(pmm_v03.validate(document))

    def test_causal_mediation_requires_direct_causal_evidence(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "mediation")
        claim["mediation_inference"] = "causal"
        claim["causal_estimand"] = "Path-specific indirect effect"
        claim["identification_strategy"] = "randomized_intervention"
        claim["causal_assumptions"] = {
            "consistency": "Defined interventions",
            "exchangeability": "Not established for the mediator-outcome relation",
            "positivity": "Assumed",
            "interference": "Assumed absent",
            "assessment": "unverified",
        }
        errors = pmm_v03.validate(document)
        self.assertTrue(any("requires linked direct causal evidence" in error for error in errors))

    def test_causal_mediation_accepts_direct_mediation_evidence(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "mediation")
        claim["mediation_inference"] = "causal"
        claim["causal_estimand"] = "Path-specific indirect effect"
        claim["identification_strategy"] = "randomized_intervention"
        claim["causal_assumptions"] = {
            "consistency": "Defined interventions",
            "exchangeability": "Assumed for this structural test",
            "positivity": "Assumed",
            "interference": "Assumed absent",
            "assessment": "plausible",
        }
        evidence = next(item for item in document["evidence"] if item["inference_support"] == "mediation")
        evidence["causal_support"] = "direct"
        self.assertEqual(pmm_v03.validate(document), [])


class InferentialModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(ROOT / "data" / "stress-test-mechanisms-v0.3.yaml")

    def test_social_buffering_is_statistical_moderation(self) -> None:
        claim = next(item for item in self.document["claims"] if item["claim_type"] == "moderation")
        self.assertEqual(claim["moderation_inference"], "statistical_interaction")

    def test_statistical_moderation_rejects_causal_estimand(self) -> None:
        document = copy.deepcopy(self.document)
        claim = next(item for item in document["claims"] if item["claim_type"] == "moderation")
        claim["causal_estimand"] = "Invalid causal effect-modification estimand"
        self.assertTrue(pmm_v03.validate(document))


class WorkingMemoryEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-working-memory-control-v0.3.yaml"
        )

    def test_working_memory_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_task_measurement_and_mechanisms_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:context:n-back-task"], "Context")
        self.assertEqual(records["pmm:measurement:n-back-performance"], "Measurement")
        self.assertEqual(records["pmm:measurement:operation-span-performance"], "Measurement")
        self.assertEqual(records["pmm:mechanism:familiarity-control"], "Mechanism")
        self.assertEqual(records["pmm:mechanism:episodic-retrieval-n-back"], "Mechanism")

    def test_computational_alternative_remains_a_hypothesis(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:episodic-retrieval-can-support-n-back"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")

    def test_duplicate_doi_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        duplicate = copy.deepcopy(document["sources"][0])
        duplicate["id"] = "pmm:source:duplicate-kane-record"
        duplicate.pop("pmid")
        document["sources"].append(duplicate)
        errors = pmm_v03.validate(document)
        self.assertTrue(any("duplicate doi" in error for error in errors))


class InteroceptionEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-interoception-anxiety-v0.3.yaml"
        )

    def test_interoception_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_physiology_measurement_construct_and_mechanism_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:state:cardiorespiratory-activation"], "State")
        self.assertEqual(records["pmm:measurement:heartbeat-task-performance"], "Measurement")
        self.assertEqual(records["pmm:construct:cardiac-interoceptive-accuracy"], "Construct")
        self.assertEqual(records["pmm:mechanism:cardiorespiratory-appraisal"], "Mechanism")

    def test_meta_analytic_null_is_preserved(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:cardiac-accuracy-not-generally-associated-with-anxiety"
        )
        self.assertEqual(claim["claim_type"], "association")
        self.assertEqual(claim["estimate"]["direction"], "null")

    def test_appraisal_remains_proposed_and_not_mediation(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:appraisal-may-link-bodily-signals-to-anxiety"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertNotIn("mediator_id", claim)


class SocialBufferingEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-social-buffering-v0.3.yaml"
        )

    def test_social_buffering_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_randomized_contrast_and_interaction_are_separate_claims(self) -> None:
        claims = {item["id"]: item for item in self.document["claims"]}
        causal = claims["pmm:claim:parent-buffer-changes-cortisol-trajectory"]
        interaction = claims["pmm:claim:buffer-condition-interacts-with-sampling-time"]
        self.assertEqual(causal["claim_type"], "causal_effect")
        self.assertEqual(interaction["claim_type"], "moderation")
        self.assertEqual(interaction["moderation_inference"], "statistical_interaction")

    def test_observational_developmental_context_is_not_causal_effect_modification(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:care-history-moderates-parent-support-effect"
        )
        self.assertEqual(claim["moderation_inference"], "statistical_interaction")
        self.assertNotIn("causal_estimand", claim)

    def test_co_regulation_remains_proposed_and_not_mediation(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:co-regulation-may-produce-buffering"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertNotIn("mediator_id", claim)


if __name__ == "__main__":
    unittest.main()

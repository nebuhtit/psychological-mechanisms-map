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

    def test_stimulus_contingency_forbids_response_role(self) -> None:
        document = copy.deepcopy(self.document)
        contingency = next(item for item in document["objects"] if item["type"] == "Contingency")
        contingency["contingency_kind"] = "stimulus_consequence"
        self.assertTrue(pmm_v03.validate(document))

    def test_stimulus_contingency_requires_antecedent(self) -> None:
        document = copy.deepcopy(self.document)
        contingency = next(item for item in document["objects"] if item["type"] == "Contingency")
        contingency["contingency_kind"] = "stimulus_consequence"
        contingency.pop("response_id")
        contingency.pop("antecedent_ids")
        self.assertTrue(pmm_v03.validate(document))

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


class RewardPredictionErrorEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-reward-prediction-error-v0.3.yaml"
        )

    def test_reward_prediction_error_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_computational_error_and_dopamine_state_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:reward-prediction-error"], "Construct")
        self.assertEqual(records["pmm:state:phasic-dopamine-neuron-activity"], "State")
        self.assertEqual(records["pmm:measurement:fitted-trialwise-rpe"], "Measurement")
        self.assertEqual(records["pmm:mechanism:temporal-difference-value-update"], "Mechanism")

    def test_optogenetic_claim_targets_behavior_not_rpe_identity(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:timed-dopamine-stimulation-increases-learned-seeking"
        )
        self.assertEqual(claim["claim_type"], "causal_effect")
        self.assertEqual(claim["outcome_id"], "pmm:behavior:cue-elicited-reward-seeking")
        self.assertNotEqual(claim["outcome_id"], "pmm:construct:reward-prediction-error")

    def test_td_update_remains_proposed(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:rpe-may-drive-temporal-difference-updating"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")


class HpaFeedbackEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-hpa-feedback-v0.3.yaml"
        )

    def test_hpa_feedback_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_hormone_states_mechanism_probe_and_measurement_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:state:circulating-cortisol-level"], "State")
        self.assertEqual(records["pmm:state:acth-secretory-drive"], "State")
        self.assertEqual(records["pmm:mechanism:glucocorticoid-negative-feedback"], "Mechanism")
        self.assertEqual(records["pmm:intervention:dexamethasone-challenge"], "Intervention")
        self.assertEqual(records["pmm:measurement:serial-acth-assay"], "Measurement")

    def test_opposite_direction_perturbations_are_separate_causal_claims(self) -> None:
        claims = {item["id"]: item for item in self.document["claims"]}
        replacement = claims["pmm:claim:cortisol-replacement-suppresses-acth-after-delay"]
        blockade = claims["pmm:claim:metyrapone-increases-continuous-and-pulsatile-acth"]
        self.assertEqual(replacement["claim_type"], "causal_effect")
        self.assertEqual(blockade["claim_type"], "causal_effect")
        self.assertNotEqual(replacement["exposure_id"], blockade["exposure_id"])

    def test_generic_feedback_remains_scoped_hypothesis(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:cortisol-signaling-may-limit-later-hpa-drive"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")


class PlaceboAnalgesiaEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-placebo-analgesia-v0.3.yaml"
        )

    def test_placebo_analgesia_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_multiple_antagonist_sources_do_not_promote_mechanism_to_fact(self) -> None:
        claim = next(
            item
            for item in self.document["claims"]
            if item["id"] == "pmm:claim:expectation-opioid-mechanism-hypothesis"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertEqual(len(claim["evidence_ids"]), 3)
        self.assertIn("pmm:evidence:sauro-2005-opioid-meta-analysis", claim["evidence_ids"])


class SpatialAttentionEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-spatial-attention-v0.3.yaml"
        )

    def test_spatial_attention_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_construct_task_intervention_response_measurement_and_mechanisms_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:spatial-selective-attention"], "Construct")
        self.assertEqual(records["pmm:context:predictive-visuospatial-cueing-task"], "Context")
        self.assertEqual(records["pmm:intervention:spatial-cue-validity-manipulation"], "Intervention")
        self.assertEqual(records["pmm:behavior:visual-target-response"], "Behavior")
        self.assertEqual(records["pmm:measurement:cueing-accuracy-and-sdt"], "Measurement")
        self.assertEqual(records["pmm:mechanism:sensory-evidence-enhancement"], "Mechanism")
        self.assertEqual(records["pmm:mechanism:spatial-decision-weighting"], "Mechanism")

    def test_candidate_mechanisms_remain_proposed(self) -> None:
        mechanism_claims = [
            claim for claim in self.document["claims"]
            if claim["claim_type"] == "mechanism_hypothesis"
        ]
        self.assertEqual(len(mechanism_claims), 2)
        self.assertTrue(all(claim["epistemic_status"] == "proposed" for claim in mechanism_claims))

    def test_sensory_account_preserves_support_and_challenge(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:sensory-enhancement-may-contribute-to-spatial-cueing"
        )
        evidence = {item["id"]: item for item in self.document["evidence"]}
        directions = {evidence[item]["support_direction"] for item in claim["evidence_ids"]}
        self.assertEqual(directions, {"supports", "challenges"})


class DeclarativeMemoryEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-declarative-memory-v0.3.yaml"
        )

    def test_declarative_memory_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_constructs_task_measurement_and_mechanism_remain_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:declarative-memory"], "Construct")
        self.assertEqual(records["pmm:construct:episodic-memory"], "Construct")
        self.assertEqual(records["pmm:construct:semantic-memory"], "Construct")
        self.assertEqual(
            records["pmm:context:incidental-word-encoding-recognition"], "Context"
        )
        self.assertEqual(
            records["pmm:intervention:encoding-question-depth-manipulation"],
            "Intervention",
        )
        self.assertEqual(
            records["pmm:measurement:old-new-recognition-performance"], "Measurement"
        )
        self.assertEqual(
            records["pmm:mechanism:elaborative-semantic-encoding"], "Mechanism"
        )

    def test_semantic_memory_is_not_semantic_encoding(self) -> None:
        records = {item["id"]: item for item in self.document["objects"]}
        semantic_memory = records["pmm:construct:semantic-memory"]
        encoding = records["pmm:mechanism:elaborative-semantic-encoding"]
        self.assertEqual(semantic_memory["type"], "Construct")
        self.assertEqual(encoding["type"], "Mechanism")
        self.assertNotEqual(semantic_memory["id"], encoding["id"])
        self.assertIn("not the same object", semantic_memory["boundary_notes"][0])

    def test_case_series_is_association_not_causal_effect(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:developmental-amnesia-dissociates-episodic-and-semantic-memory"
        )
        evidence = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:vargha-khadem-1997-dissociation"
        )
        self.assertEqual(claim["claim_type"], "association")
        self.assertEqual(evidence["causal_support"], "none")
        self.assertEqual(evidence["sample_size"], 3)

    def test_elaborative_encoding_remains_proposed(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:elaborative-semantic-encoding-may-support-retention"
        )
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")


class VisualPerceptionEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-visual-perception-v0.3.yaml"
        )

    def test_visual_perception_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_construct_task_stimulus_response_measurement_and_mechanism_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:visual-perception"], "Construct")
        self.assertEqual(records["pmm:construct:spatial-contrast-sensitivity"], "Construct")
        self.assertEqual(records["pmm:context:sine-wave-grating-detection-task"], "Context")
        self.assertEqual(
            records["pmm:intervention:grating-spatial-frequency-and-contrast-manipulation"],
            "Intervention",
        )
        self.assertEqual(records["pmm:behavior:grating-detection-response"], "Behavior")
        self.assertEqual(records["pmm:outcome:contrast-detection-threshold"], "Outcome")
        self.assertEqual(
            records["pmm:measurement:contrast-sensitivity-function"], "Measurement"
        )
        self.assertEqual(
            records["pmm:mechanism:divisive-visual-normalization"], "Mechanism"
        )

    def test_contrast_sensitivity_function_is_not_visual_perception(self) -> None:
        records = {item["id"]: item for item in self.document["objects"]}
        construct = records["pmm:construct:visual-perception"]
        measurement = records["pmm:measurement:contrast-sensitivity-function"]
        self.assertNotEqual(construct["id"], measurement["id"])
        self.assertIn("not visual perception as a whole", measurement["boundary_notes"][0])

    def test_normalization_remains_proposed_and_indirect(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:divisive-normalization-may-shape-visual-gain"
        )
        evidence = {item["id"]: item for item in self.document["evidence"]}
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertTrue(
            all(evidence[item]["causal_support"] == "indirect" for item in claim["evidence_ids"])
        )
        self.assertEqual(evidence["pmm:evidence:heeger-1992-normalization-model"]["species"], ["other"])

    def test_human_psychophysical_effect_is_not_the_normalization_claim(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:grating-properties-change-detection-threshold"
        )
        self.assertEqual(claim["claim_type"], "causal_effect")
        self.assertNotIn("mechanism_id", claim)
        self.assertEqual(
            claim["outcome_id"], "pmm:outcome:contrast-detection-threshold"
        )


class DeductiveReasoningEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-deductive-reasoning-v0.3.yaml"
        )

    def test_deductive_reasoning_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_construct_task_manipulation_response_outcome_measurement_and_mechanism_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:deductive-reasoning"], "Construct")
        self.assertEqual(
            records["pmm:context:syllogistic-validity-judgment-task"], "Context"
        )
        self.assertEqual(
            records["pmm:intervention:syllogism-validity-believability-manipulation"],
            "Intervention",
        )
        self.assertEqual(
            records["pmm:behavior:syllogism-validity-judgment"], "Behavior"
        )
        self.assertEqual(
            records["pmm:outcome:syllogistic-judgment-performance"], "Outcome"
        )
        self.assertEqual(
            records["pmm:measurement:condition-specific-syllogism-judgments"],
            "Measurement",
        )
        self.assertEqual(
            records["pmm:mechanism:parallel-belief-logic-evaluation"], "Mechanism"
        )

    def test_raw_judgments_and_signal_detection_parameters_are_distinct(self) -> None:
        records = {item["id"]: item for item in self.document["objects"]}
        raw = records["pmm:measurement:condition-specific-syllogism-judgments"]
        modeled = records["pmm:measurement:syllogistic-signal-detection-profile"]
        self.assertEqual(raw["measurement_kind"], "behavioral_task")
        self.assertEqual(modeled["measurement_kind"], "computational_parameter")
        self.assertNotEqual(raw["id"], modeled["id"])
        self.assertIn("not direct observations", modeled["boundary_notes"][0])

    def test_meta_analytic_null_is_association_not_causal_effect(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:believability-does-not-unconditionally-reduce-discriminability"
        )
        evidence = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:trippas-2018-sdt-meta-analysis"
        )
        self.assertEqual(claim["claim_type"], "association")
        self.assertEqual(claim["estimate"]["direction"], "null")
        self.assertEqual(evidence["causal_support"], "none")
        self.assertEqual(evidence["sample_size"], 993)

    def test_believability_effect_targets_the_observed_judgment(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:conclusion-believability-changes-validity-judgments"
        )
        self.assertEqual(claim["claim_type"], "causal_effect")
        self.assertEqual(
            claim["outcome_id"], "pmm:behavior:syllogism-validity-judgment"
        )
        self.assertNotEqual(
            claim["outcome_id"], "pmm:outcome:syllogistic-judgment-performance"
        )

    def test_parallel_process_remains_low_confidence_and_contested(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:belief-and-logic-may-be-evaluated-in-parallel"
        )
        evidence = {
            item["id"]: item for item in self.document["evidence"]
            if item["id"] in claim["evidence_ids"]
        }
        self.assertEqual(claim["claim_type"], "mechanism_hypothesis")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertEqual(claim["confidence"]["level"], "low")
        self.assertEqual(
            {item["support_direction"] for item in evidence.values()},
            {"supports", "challenges"},
        )
        challenge = evidence["pmm:evidence:kosourikhina-handley-2025-subjective-conflict"]
        self.assertEqual(challenge["sample_size"], 248)
        self.assertEqual(challenge["causal_support"], "indirect")


class LanguageComprehensionEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-language-comprehension-v0.3.yaml"
        )

    def test_language_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_construct_task_response_outcome_measurement_and_mechanisms_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:language-comprehension"], "Construct")
        self.assertEqual(records["pmm:construct:visual-lexical-access"], "Construct")
        self.assertEqual(records["pmm:context:semantic-priming-lexical-decision-task"], "Context")
        self.assertEqual(records["pmm:context:paired-word-classification-task"], "Context")
        self.assertEqual(records["pmm:intervention:semantic-relatedness-timing-manipulation"], "Intervention")
        self.assertEqual(records["pmm:behavior:word-nonword-classification"], "Behavior")
        self.assertEqual(records["pmm:outcome:lexical-decision-response-latency"], "Outcome")
        self.assertEqual(records["pmm:measurement:lexical-decision-diffusion-profile"], "Measurement")
        self.assertEqual(records["pmm:mechanism:automatic-semantic-preactivation"], "Mechanism")
        self.assertEqual(records["pmm:mechanism:strategic-postlexical-matching"], "Mechanism")

    def test_priming_effect_is_causal_only_for_observed_latency(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:semantic-relatedness-changes-lexical-decision-latency"
        )
        self.assertEqual(claim["claim_type"], "causal_effect")
        self.assertEqual(claim["outcome_id"], "pmm:outcome:lexical-decision-response-latency")
        self.assertNotIn("mechanism_id", claim)

    def test_diffusion_parameters_are_modeled_not_causal(self) -> None:
        claim = next(
            item for item in self.document["claims"]
            if item["id"] == "pmm:claim:diffusion-model-decomposes-lexical-decisions"
        )
        evidence = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:ratcliff-2004-diffusion-model"
        )
        self.assertEqual(claim["claim_type"], "association")
        self.assertEqual(evidence["evidence_kind"], "computational_model")
        self.assertEqual(evidence["causal_support"], "none")

    def test_competing_processes_remain_proposed(self) -> None:
        claims = {
            item["mechanism_id"]: item
            for item in self.document["claims"]
            if item["claim_type"] == "mechanism_hypothesis"
        }
        self.assertEqual(
            set(claims),
            {
                "pmm:mechanism:automatic-semantic-preactivation",
                "pmm:mechanism:strategic-postlexical-matching",
            },
        )
        self.assertTrue(all(item["epistemic_status"] == "proposed" for item in claims.values()))
        review = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:mangat-2026-automatic-strategic-review"
        )
        self.assertEqual(review["support_direction"], "mixed")
        self.assertEqual(review["causal_support"], "indirect")


class BigFiveEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(ROOT / "data" / "evidence-pack-big-five-v0.3.yaml")

    def test_big_five_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_taxonomy_items_scores_factors_and_outcome_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:big-five-trait-taxonomy"], "Construct")
        self.assertEqual(records["pmm:context:bfi2-self-report-assessment"], "Context")
        self.assertEqual(records["pmm:behavior:bfi2-item-rating"], "Behavior")
        self.assertEqual(records["pmm:measurement:bfi2-domain-facet-scores"], "Measurement")
        self.assertEqual(records["pmm:measurement:bfi2-hierarchical-factor-profile"], "Measurement")
        self.assertEqual(records["pmm:outcome:academic-performance"], "Outcome")

    def test_factor_model_and_trait_association_are_not_mechanisms_or_causes(self) -> None:
        self.assertFalse(any(item["type"] == "Mechanism" for item in self.document["objects"]))
        claim = next(item for item in self.document["claims"] if item["id"] == "pmm:claim:conscientiousness-associated-with-academic-performance")
        self.assertEqual(claim["claim_type"], "association")
        self.assertNotIn("causal_estimand", claim)
        evidence = next(item for item in self.document["evidence"] if item["id"] == "pmm:evidence:poropat-2009-academic-meta-analysis")
        self.assertEqual(evidence["causal_support"], "none")


class AttachmentEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-attachment-system-v0.3.yaml"
        )

    def test_attachment_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_system_state_behavior_mechanism_and_measurements_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:attachment-behavioral-system"], "Construct")
        self.assertEqual(records["pmm:state:attachment-system-activation"], "State")
        self.assertEqual(records["pmm:behavior:proximity-support-seeking"], "Behavior")
        self.assertEqual(records["pmm:mechanism:conditional-attachment-regulation"], "Mechanism")
        self.assertEqual(records["pmm:measurement:strange-situation-classification"], "Measurement")
        self.assertEqual(records["pmm:measurement:aai-state-of-mind-classification"], "Measurement")

    def test_stability_and_sensitivity_are_associations_not_causes(self) -> None:
        claims = {item["id"]: item for item in self.document["claims"]}
        evidence = {item["id"]: item for item in self.document["evidence"]}
        for claim_id in (
            "pmm:claim:caregiver-sensitivity-associated-with-child-security",
            "pmm:claim:attachment-security-shows-moderate-not-deterministic-stability",
        ):
            self.assertEqual(claims[claim_id]["claim_type"], "association")
        self.assertEqual(
            evidence["pmm:evidence:divito-kurkjian-2021-sensitivity-meta"]["causal_support"],
            "none",
        )
        mechanism = claims["pmm:claim:attachment-regulation-loop-is-integrative-hypothesis"]
        self.assertEqual(mechanism["epistemic_status"], "proposed")
        self.assertEqual(mechanism["confidence"]["level"], "low")

    def test_comma_rich_notes_remain_single_sentences(self) -> None:
        strange = next(
            item for item in self.document["objects"]
            if item["id"] == "pmm:context:strange-situation-procedure"
        )
        self.assertEqual(len(strange["boundary_notes"]), 1)
        sensitivity = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:divito-kurkjian-2021-sensitivity-meta"
        )
        self.assertEqual(len(sensitivity["limitations"]), 1)
        self.assertIn("heterogeneous coding", sensitivity["limitations"][0])


class CbtFormulationEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = pmm_v03.load_yaml(
            ROOT / "data" / "evidence-pack-cbt-formulation-v0.3.yaml"
        )

    def test_cbt_pack_is_valid(self) -> None:
        self.assertEqual(pmm_v03.validate(copy.deepcopy(self.document)), [])

    def test_efficacy_mediation_and_mechanism_are_not_collapsed(self) -> None:
        claims = {item["id"]: item for item in self.document["claims"]}
        efficacy = claims["pmm:claim:cbt-reduces-depression-versus-controls"]
        mediation = claims["pmm:claim:cognitive-change-statistically-mediates-some-prevention-effects"]
        mechanism = claims["pmm:claim:cbt-cycle-is-person-specific-mechanism-hypothesis"]
        self.assertEqual(efficacy["claim_type"], "causal_effect")
        self.assertNotIn("mechanism_id", efficacy)
        self.assertEqual(mediation["claim_type"], "mediation")
        self.assertEqual(mediation["mediation_inference"], "statistical")
        self.assertEqual(mechanism["claim_type"], "mechanism_hypothesis")
        self.assertEqual(mechanism["epistemic_status"], "proposed")

    def test_thought_emotion_physiology_behavior_and_outcome_are_distinct(self) -> None:
        records = {item["id"]: item["type"] for item in self.document["objects"]}
        self.assertEqual(records["pmm:construct:situational-interpretation"], "Construct")
        self.assertEqual(records["pmm:state:cbt-emotional-response"], "State")
        self.assertEqual(records["pmm:state:cbt-physiological-response"], "State")
        self.assertEqual(records["pmm:behavior:cbt-coping-response"], "Behavior")
        self.assertEqual(records["pmm:outcome:cbt-short-long-consequences"], "Outcome")

    def test_comma_rich_boundaries_remain_single_sentences(self) -> None:
        intervention = next(
            item for item in self.document["objects"]
            if item["id"] == "pmm:intervention:protocol-defined-cbt"
        )
        self.assertEqual(len(intervention["boundary_notes"]), 1)
        trial_evidence = next(
            item for item in self.document["evidence"]
            if item["id"] == "pmm:evidence:cuijpers-2023-cbt-depression-meta"
        )
        self.assertEqual(len(trial_evidence["limitations"]), 1)
        self.assertIn("sensitivity analyses", trial_evidence["limitations"][0])


if __name__ == "__main__":
    unittest.main()

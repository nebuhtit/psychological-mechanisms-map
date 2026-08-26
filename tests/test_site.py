from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_ru_translation import displayed_strings  # noqa: E402
from claim_explanations import load_annotations, registered_claims, validate  # noqa: E402


class SiteBundleTests(unittest.TestCase):
    def test_site_bundle_contains_expected_families(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        registry = yaml.safe_load((ROOT / "data" / "families.yaml").read_text())
        expected = [entry["family"]["id"] for entry in registry["datasets"] if "family" in entry]
        self.assertEqual(
            [item["id"] for item in document["families"]],
            expected,
        )
        self.assertTrue(
            all(item["version"] == document["pmm_version"] for item in document["families"])
        )

    def test_site_bundle_references_resolve_within_each_family(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        for family in document["families"]:
            records = {
                item["id"]
                for section in ("objects", "claims", "evidence", "sources")
                for item in family[section]
            }
            for claim in family["claims"]:
                for field in ("exposure_id", "mechanism_id", "mediator_id", "moderator_id", "outcome_id"):
                    if field in claim:
                        self.assertIn(claim[field], records)
                for evidence_id in claim.get("evidence_ids", []):
                    self.assertIn(evidence_id, records)

    def test_mechanism_index_is_complete_and_derived(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        expected = {
            (family["id"], item["id"])
            for family in document["families"]
            for item in family["objects"]
            if item["type"] == "Mechanism"
        }
        actual = {
            (item["family_id"], item["id"])
            for item in document["mechanism_index"]
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), len(document["mechanism_index"]))
        for item in document["mechanism_index"]:
            self.assertEqual(item["evidence_count"] >= item["source_count"], True)
            self.assertEqual(sum(item["claim_status_counts"].values()), len(item["claim_ids"]))

    def test_site_has_no_inline_scientific_dataset(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text()
        self.assertIn('const DATA_URL = "data/pmm-data.json?v=0.18.0";', javascript)
        self.assertNotIn("pmm:evidence:", javascript)

    def test_language_toggle_and_russian_bundle_are_present(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertIn('id="language-toggle"', page)
        self.assertIn('localStorage.getItem("pmm-language")', javascript)
        self.assertIn('const RU_URL = "data/i18n-ru.json?v=0.18.0";', javascript)

        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        bundle = json.loads((ROOT / "site" / "data" / "i18n-ru.json").read_text())
        self.assertEqual(bundle["canonical_language"], "en")
        self.assertEqual(bundle["language"], "ru")
        self.assertEqual(bundle["translation_status"], "machine_translated_pending_review")
        self.assertEqual(set(bundle["translations"]), displayed_strings(document))
        self.assertTrue(all(value.strip() for value in bundle["translations"].values()))
        self.assertEqual(
            bundle["translations"]["RDoC Potential Threat (Anxiety) concerns responses when harm may occur but is distant, ambiguous, or uncertain in probability."],
            "Конструкт RDoC «Потенциальная угроза (тревога)» описывает реакции на возможный вред, который отдалён во времени, неоднозначен или имеет неопределённую вероятность.",
        )
        self.assertEqual(
            bundle["translations"]["Spatial attention may improve performance in some cueing tasks by increasing perceptual sensitivity at the attended location."],
            "В некоторых заданиях с пространственной подсказкой внимание может улучшать результат за счёт повышения перцептивной чувствительности в указанном месте.",
        )
        self.assertEqual(bundle["translations"]["Attachment system"], "Система привязанности")
        self.assertEqual(
            bundle["translations"]["Conditional attachment regulation"],
            "Контекстно-зависимая регуляция привязанности",
        )
        self.assertEqual(
            bundle["translations"]["Strange Situation Procedure"],
            "Процедура «Незнакомая ситуация»",
        )
        self.assertEqual(
            bundle["translations"]["Social and observational learning"],
            "Социальное научение и научение через наблюдение",
        )
        self.assertEqual(
            bundle["translations"]["Model-behavior exposure"],
            "Предъявление поведения модели",
        )
        self.assertEqual(
            bundle["translations"]["Emotion components and appraisal"],
            "Компоненты эмоции и оценка ситуации",
        )
        self.assertEqual(
            bundle["translations"]["Appraisal-guided component coordination"],
            "Координация компонентов через оценку ситуации",
        )
        self.assertEqual(bundle["translations"]["Developmental temperament"], "Темперамент в развитии")
        self.assertEqual(
            bundle["translations"]["Developmental temperament transaction"],
            "Развивающее взаимодействие темперамента и среды",
        )

    def test_every_claim_has_a_source_checked_bilingual_explanation(self) -> None:
        self.assertEqual(validate(), [])
        annotations = load_annotations()
        self.assertEqual(set(annotations), set(registered_claims()))

        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        bundle = json.loads((ROOT / "site" / "data" / "i18n-ru.json").read_text())
        for family in document["families"]:
            for claim in family["claims"]:
                self.assertEqual(claim["plain_language_summary"], annotations[claim["id"]]["en"])
                self.assertEqual(
                    bundle["translations"][claim["plain_language_summary"]],
                    annotations[claim["id"]]["ru"],
                )

        corrected = annotations["pmm:claim:clinical-maintenance-loop-hypothesis"]["ru"]
        self.assertIn("ему может быстро стать легче", corrected)
        self.assertIn("не получит возможности проверить", corrected)
        self.assertNotIn("может вызывать изменение", corrected)

    def test_reading_guide_is_collapsed_and_explains_visual_encoding(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.assertIn('<details class="map-guide">', page)
        self.assertNotIn('<details class="map-guide" open>', page)
        for phrase in ("How to read this map", "Claim colours", "Lines and interaction", "Research question"):
            self.assertIn(phrase, page)

    def test_research_questions_are_valid_peripheral_annotations(self) -> None:
        source = yaml.safe_load(
            (ROOT / "data" / "research-questions-v0.1.yaml").read_text(encoding="utf-8")
        )
        schema = yaml.safe_load(
            (ROOT / "schema" / "research-questions-v0.1.schema.yaml").read_text(encoding="utf-8")
        )
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(source)
        )
        self.assertEqual(errors, [])

        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        self.assertEqual(document["research_questions_version"], "0.1.0")
        self.assertEqual(len(source["questions"]), len(document["families"]))
        for family in document["families"]:
            self.assertEqual(len(family["research_questions"]), 1)
            question = family["research_questions"][0]
            self.assertEqual(question["status"], "open")
            self.assertEqual(question["display_prominence"], "peripheral")
            self.assertTrue(question["question"]["en"])
            self.assertTrue(question["question"]["ru"])
            object_and_claim_ids = {
                item["id"] for section in ("objects", "claims") for item in family[section]
            }
            self.assertTrue(set(question["about_ids"]).issubset(object_and_claim_ids))
            self.assertNotIn(question["id"], object_and_claim_ids)
            self.assertTrue(
                set(question["source_ids"]).issubset(
                    {source["id"] for source in family["sources"]}
                )
            )

    def test_research_questions_are_visually_subordinate_and_explained(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
        self.assertIn('kind: "question"', javascript)
        self.assertIn("function renderResearchQuestionInspector(", javascript)
        self.assertIn("not a scientific finding", javascript)
        self.assertIn(".node.question { opacity: .48; }", stylesheet)
        self.assertIn(".node.question .node-shape", stylesheet)
        self.assertIn(".edge.question-edge", stylesheet)

    def test_practical_implications_are_separate_bounded_annotations(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        self.assertEqual(document["practical_implications_version"], "0.1.0")
        applications = [
            application
            for family in document["families"]
            for application in family["practical_implications"]
        ]
        self.assertGreaterEqual(len(applications), len(document["families"]))
        self.assertTrue(all(len(family["practical_implications"]) >= 1 for family in document["families"]))
        self.assertTrue(all(application["id"].startswith("pmm:application:") for application in applications))
        self.assertTrue(all(application["actionability"] in {"direct_within_tested_scope", "transfer_uncertain", "interpretation_only"} for application in applications))
        self.assertTrue(all(application["not_established"]["en"] for application in applications))

        memory = next(item for item in applications if item["family_id"] == "declarative-memory")
        reasoning = next(item for item in applications if item["family_id"] == "deductive-reasoning")
        avoidance = next(item for item in applications if item["family_id"] == "avoidance")
        self.assertEqual(memory["actionability"], "transfer_uncertain")
        self.assertEqual(reasoning["actionability"], "interpretation_only")
        self.assertIn("not directly test", reasoning["evidence_basis"]["en"])
        self.assertIn("safety_note", avoidance)

        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertIn("What can be done with this?", javascript)
        self.assertIn("Not automatic advice", javascript)
        self.assertIn("What is not established", javascript)
        self.assertIn("renderClaimPractical(record)", javascript)
        self.assertIn("No claim-specific application has been independently established yet", javascript)

    def test_cross_family_mechanism_catalog_is_collapsed_and_navigable(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
        self.assertIn('<details class="mechanism-catalog" id="mechanism-catalog">', page)
        self.assertNotIn('<details class="mechanism-catalog" id="mechanism-catalog" open>', page)
        self.assertIn('id="mechanism-search"', page)
        self.assertIn("function renderMechanismCatalog()", javascript)
        self.assertIn('state.data.mechanism_index.filter', javascript)
        self.assertIn('data-open-mechanism=', javascript)
        self.assertIn('selectNode(button.dataset.openMechanism)', javascript)
        self.assertIn("They are not truth scores", page)
        self.assertIn(".mechanism-grid", stylesheet)
        self.assertIn(".mechanism-card", stylesheet)

    def test_map_background_and_escape_clear_selection(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function clearSelection()", javascript)
        self.assertIn('if (!event.target.closest(".node")) clearSelection();', javascript)
        self.assertIn('if (event.key === "Escape") clearSelection();', javascript)
        self.assertIn('element.classList.remove("is-selected", "is-dimmed")', javascript)

    def test_inspector_explains_status_inference_and_element_roles(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
        for function in ("statusExplanation", "inferenceExplanation", "roleFor", "claimDiagram", "renderConnections"):
            self.assertIn(f"function {function}(", javascript)
        self.assertIn('"Degree of evidence", "Степень доказанности"', javascript)
        self.assertIn('"Source-checked plain explanation", "Проверенное по источникам объяснение"', javascript)
        self.assertIn("record.plain_language_summary", javascript)
        self.assertNotIn("function plainLanguageExplanation(", javascript)
        self.assertIn('"Association only:', javascript)
        self.assertIn(".evidence-summary", stylesheet)
        self.assertIn(".plain-language-card", stylesheet)
        self.assertIn(".connection-card", stylesheet)
        self.assertIn(".claim-diagram", stylesheet)
        self.assertIn(".moderator-branch", stylesheet)

    def test_inspector_does_not_render_moderator_as_mediator(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("function claimPath(", javascript)
        self.assertIn('claim.claim_type === "mediation" && claim.mediator_id', javascript)
        self.assertIn('const moderator = claim.moderator_id', javascript)
        self.assertIn('"associated; no causal direction"', javascript)
        self.assertIn('"predicts; does not prove cause"', javascript)

    def test_inspector_does_not_truncate_claim_heading(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
        self.assertIn('const heading = record.kind === "claim" ? t(record.statement) : t(record.label);', javascript)
        self.assertNotIn('wrapLabel(t(record.statement), 48)', javascript)
        self.assertIn(".inspector h2.claim-heading", stylesheet)

    def test_family_overview_explains_scope_and_links_sources(self) -> None:
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("state.family.description", javascript)
        self.assertIn("state.family.sources || []", javascript)
        self.assertIn('class="source-link" href="${escapeHtml(source.url)}"', javascript)
        self.assertIn('"What this section studies", "Что изучает этот раздел"', javascript)
        self.assertIn("There is no single defining source.", javascript)
        self.assertIn("not a diagnosis or an exhaustive systematic review", javascript)
        self.assertIn('String(index + 1).padStart(2, "0")', javascript)
        self.assertIn("else renderEmptyInspector();", javascript)
        self.assertIn(".family-overview-card", stylesheet)
        self.assertIn(".family-stats", stylesheet)

    def test_four_validated_navigation_views_are_exposed(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        self.assertIn('data-perspective="models"', page)
        self.assertIn('data-perspective="general"', page)
        self.assertIn('data-perspective="mechanisms"', page)
        self.assertIn('data-perspective="systems"', page)
        self.assertIn('localStorage.getItem("pmm-perspective")', javascript)
        self.assertIn("function openCanonicalRecord(", javascript)
        self.assertIn("navigation_views", document)
        self.assertEqual(document["navigation_views"]["view_version"], "0.1.0")
        models = document["navigation_views"]["foundational_models"]
        self.assertEqual(len(models["workflow"]), 5)
        self.assertEqual(len(models["models"]), 10)
        self.assertIn("Process-Based Therapy", models["process_based_note"]["en"])
        coverage = {item["id"]: item["coverage"] for item in models["models"]}
        self.assertEqual(coverage["model:attachment"], "partial")
        self.assertEqual(coverage["model:cbt-formulation"], "partial")
        self.assertEqual(coverage["model:social-learning"], "partial")

    def test_navigation_does_not_collapse_tasks_traits_and_mechanisms(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        view = document["navigation_views"]["general_psychology"]
        nodes = {node["id"]: node for node in view["nodes"]}
        memory = nodes["gp:memory"]
        types = {item["canonical_id"]: item["expected_type"] for item in memory["memberships"]}
        self.assertEqual(types["pmm:context:n-back-task"], "Context")
        self.assertEqual(types["pmm:measurement:n-back-performance"], "Measurement")
        self.assertEqual(types["pmm:mechanism:episodic-retrieval-n-back"], "Mechanism")
        self.assertIn("rather than memory itself", memory["ontological_note"]["en"])
        self.assertEqual(nodes["gp:temperament"]["coverage"], "partial")
        temperament_types = {
            item["canonical_id"]: item["expected_type"]
            for item in nodes["gp:temperament"]["memberships"]
        }
        self.assertEqual(temperament_types["pmm:construct:developmental-temperament-dimensions"], "Construct")
        self.assertEqual(temperament_types["pmm:state:context-specific-temperamental-reactivity"], "State")
        self.assertEqual(temperament_types["pmm:behavior:observed-temperament-relevant-response"], "Behavior")
        self.assertEqual(temperament_types["pmm:measurement:cbq-temperament-profile"], "Measurement")
        self.assertEqual(temperament_types["pmm:mechanism:developmental-temperament-transaction"], "Mechanism")
        self.assertEqual(nodes["gp:big-five"]["coverage"], "partial")
        self.assertTrue(nodes["gp:big-five"]["memberships"])

        attention = nodes["gp:attention"]
        attention_types = {
            item["canonical_id"]: item["expected_type"] for item in attention["memberships"]
        }
        self.assertEqual(attention["coverage"], "partial")
        self.assertEqual(
            attention_types["pmm:context:predictive-visuospatial-cueing-task"], "Context"
        )
        self.assertEqual(
            attention_types["pmm:measurement:cueing-accuracy-and-sdt"], "Measurement"
        )
        self.assertEqual(
            attention_types["pmm:mechanism:spatial-decision-weighting"], "Mechanism"
        )
        perception = nodes["gp:perception"]
        perception_types = {
            item["canonical_id"]: item["expected_type"]
            for item in perception["memberships"]
        }
        self.assertEqual(perception["coverage"], "partial")
        self.assertEqual(perception_types["pmm:construct:visual-perception"], "Construct")
        self.assertEqual(
            perception_types["pmm:context:sine-wave-grating-detection-task"], "Context"
        )
        self.assertEqual(
            perception_types["pmm:intervention:grating-spatial-frequency-and-contrast-manipulation"],
            "Intervention",
        )
        self.assertEqual(
            perception_types["pmm:behavior:grating-detection-response"], "Behavior"
        )
        self.assertEqual(
            perception_types["pmm:measurement:contrast-sensitivity-function"],
            "Measurement",
        )
        self.assertEqual(
            perception_types["pmm:mechanism:divisive-visual-normalization"],
            "Mechanism",
        )

        self.assertEqual(types["pmm:construct:declarative-memory"], "Construct")
        self.assertEqual(types["pmm:construct:episodic-memory"], "Construct")
        self.assertEqual(types["pmm:construct:semantic-memory"], "Construct")
        self.assertEqual(
            types["pmm:context:incidental-word-encoding-recognition"], "Context"
        )
        self.assertEqual(
            types["pmm:measurement:old-new-recognition-performance"], "Measurement"
        )

        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertIn('"Task context, not the construct"', javascript)
        self.assertNotIn('"Task context, not memory"', javascript)
        self.assertIn("The main-area scaffold is now visible", javascript)
        self.assertIn("partialTopicCount", javascript)

    def test_general_psychology_exposes_the_main_area_scaffold(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        nodes = {
            node["id"]: node
            for node in document["navigation_views"]["general_psychology"]["nodes"]
        }
        required_domains = {
            "gp:cognitive-processes",
            "gp:emotion-motivation",
            "gp:action-self-regulation",
            "gp:social-processes",
            "gp:body-consciousness",
            "gp:development",
            "gp:personality-individual-differences",
        }
        required_topics = {
            "gp:memory",
            "gp:attention",
            "gp:perception",
            "gp:sensation-interoception",
            "gp:learning",
            "gp:thinking-reasoning",
            "gp:language",
            "gp:imagery-imagination",
            "gp:emotional-states-regulation",
            "gp:motivation-reward",
            "gp:stress-coping",
            "gp:goal-directed-habitual-action",
            "gp:cognitive-control",
            "gp:volition",
            "gp:social-regulation-support",
            "gp:social-cognition",
            "gp:physiological-regulation",
            "gp:pain",
            "gp:consciousness",
            "gp:developmental-context",
            "gp:temperament",
            "gp:big-five",
            "gp:abilities-intelligence",
            "gp:self-concept",
        }
        self.assertTrue(required_domains.issubset(nodes))
        self.assertTrue(required_topics.issubset(nodes))
        for node_id in required_topics:
            self.assertIn(nodes[node_id]["coverage"], {"partial", "planned"})
            if nodes[node_id]["coverage"] == "planned":
                self.assertEqual(nodes[node_id]["memberships"], [])

    def test_framework_cards_preserve_scope_and_mapping_uncertainty(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        systems = {
            system["id"]: system
            for system in document["navigation_views"]["scientific_systems"]["systems"]
        }
        self.assertIn("not a diagnostic manual", systems["system:rdoc"]["limitation"]["en"])
        self.assertIn("Unreviewed", systems["system:cognitive-atlas"]["limitation"]["en"])
        self.assertIn("psychopathology", systems["system:hitop"]["scope"]["en"])
        self.assertEqual(systems["system:hitop"]["coverage"], "planned")

        working_memory = next(
            item
            for family in document["families"] if family["id"] == "working-memory"
            for item in family["objects"] if item["id"] == "pmm:construct:working-memory-capacity"
        )
        mappings = {item["system"]: item for item in working_memory["external_mappings"]}
        self.assertEqual(mappings["RDoC"]["mapping_relation"], "narrow_match")
        self.assertEqual(mappings["CognitiveAtlas"]["mapping_status"], "provisional")

        deductive_reasoning = next(
            item
            for family in document["families"] if family["id"] == "deductive-reasoning"
            for item in family["objects"]
            if item["id"] == "pmm:construct:deductive-reasoning"
        )
        mappings = {item["system"]: item for item in deductive_reasoning["external_mappings"]}
        self.assertEqual(mappings["CognitiveAtlas"]["mapping_status"], "provisional")

        spatial_attention = next(
            item
            for family in document["families"] if family["id"] == "spatial-attention"
            for item in family["objects"]
            if item["id"] == "pmm:construct:spatial-selective-attention"
        )
        mappings = {item["system"]: item for item in spatial_attention["external_mappings"]}
        self.assertEqual(mappings["RDoC"]["mapping_relation"], "narrow_match")
        self.assertEqual(mappings["CognitiveAtlas"]["mapping_status"], "provisional")

        declarative_memory = next(
            item
            for family in document["families"] if family["id"] == "declarative-memory"
            for item in family["objects"]
            if item["id"] == "pmm:construct:declarative-memory"
        )
        mappings = {item["system"]: item for item in declarative_memory["external_mappings"]}
        self.assertEqual(mappings["RDoC"]["mapping_relation"], "exact_match")
        self.assertEqual(mappings["RDoC"]["mapping_status"], "identifier_verified")

        visual_perception = next(
            item
            for family in document["families"] if family["id"] == "visual-perception"
            for item in family["objects"]
            if item["id"] == "pmm:construct:visual-perception"
        )
        mappings = {item["system"]: item for item in visual_perception["external_mappings"]}
        self.assertEqual(mappings["RDoC"]["mapping_relation"], "exact_match")
        self.assertEqual(mappings["RDoC"]["mapping_status"], "identifier_verified")
        self.assertEqual(mappings["CognitiveAtlas"]["mapping_status"], "provisional")

    def test_thinking_and_reasoning_is_partial_and_type_safe(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        nodes = {
            node["id"]: node
            for node in document["navigation_views"]["general_psychology"]["nodes"]
        }
        reasoning = nodes["gp:thinking-reasoning"]
        self.assertEqual(reasoning["coverage"], "partial")
        expected_types = {
            membership["canonical_id"]: membership["expected_type"]
            for membership in reasoning["memberships"]
        }
        self.assertEqual(expected_types["pmm:construct:deductive-reasoning"], "Construct")
        self.assertEqual(
            expected_types["pmm:context:syllogistic-validity-judgment-task"],
            "Context",
        )
        self.assertEqual(
            expected_types["pmm:behavior:syllogism-validity-judgment"],
            "Behavior",
        )
        self.assertEqual(
            expected_types["pmm:measurement:syllogistic-signal-detection-profile"],
            "Measurement",
        )
        self.assertEqual(
            expected_types["pmm:mechanism:parallel-belief-logic-evaluation"],
            "Mechanism",
        )

    def test_language_is_partial_and_preserves_task_measurement_boundaries(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        nodes = {
            node["id"]: node
            for node in document["navigation_views"]["general_psychology"]["nodes"]
        }
        language = nodes["gp:language"]
        self.assertEqual(language["coverage"], "partial")
        expected_types = {
            membership["canonical_id"]: membership["expected_type"]
            for membership in language["memberships"]
        }
        self.assertEqual(expected_types["pmm:construct:language-comprehension"], "Construct")
        self.assertEqual(expected_types["pmm:context:semantic-priming-lexical-decision-task"], "Context")
        self.assertEqual(expected_types["pmm:context:paired-word-classification-task"], "Context")
        self.assertEqual(expected_types["pmm:behavior:word-nonword-classification"], "Behavior")
        self.assertEqual(expected_types["pmm:outcome:lexical-decision-response-latency"], "Outcome")
        self.assertEqual(expected_types["pmm:measurement:lexical-decision-diffusion-profile"], "Measurement")
        self.assertIn("remain unmapped", language["ontological_note"]["en"])

    def test_big_five_is_partial_without_an_invented_mechanism(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        nodes = {
            node["id"]: node
            for node in document["navigation_views"]["general_psychology"]["nodes"]
        }
        big_five = nodes["gp:big-five"]
        self.assertEqual(big_five["coverage"], "partial")
        expected_types = {
            membership["canonical_id"]: membership["expected_type"]
            for membership in big_five["memberships"]
        }
        self.assertEqual(expected_types["pmm:construct:big-five-trait-taxonomy"], "Construct")
        self.assertEqual(expected_types["pmm:context:bfi2-self-report-assessment"], "Context")
        self.assertEqual(expected_types["pmm:behavior:bfi2-item-rating"], "Behavior")
        self.assertEqual(expected_types["pmm:measurement:bfi2-domain-facet-scores"], "Measurement")
        self.assertEqual(expected_types["pmm:outcome:academic-performance"], "Outcome")

        family = next(item for item in document["families"] if item["id"] == "big-five")
        self.assertFalse(any(item["type"] == "Mechanism" for item in family["objects"]))
        self.assertEqual(len(family["practical_implications"]), 2)

if __name__ == "__main__":
    unittest.main()

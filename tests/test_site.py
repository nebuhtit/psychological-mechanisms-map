from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

import yaml


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
        self.assertIn('const DATA_URL = "data/pmm-data.json?v=0.5.0";', javascript)
        self.assertNotIn("pmm:evidence:", javascript)

    def test_language_toggle_and_russian_bundle_are_present(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        self.assertIn('id="language-toggle"', page)
        self.assertIn('localStorage.getItem("pmm-language")', javascript)
        self.assertIn('const RU_URL = "data/i18n-ru.json?v=0.5.1";', javascript)

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
        for phrase in ("How to read this map", "Claim colours", "Lines and interaction"):
            self.assertIn(phrase, page)

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

    def test_three_validated_navigation_views_are_exposed(self) -> None:
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        self.assertIn('data-perspective="general"', page)
        self.assertIn('data-perspective="mechanisms"', page)
        self.assertIn('data-perspective="systems"', page)
        self.assertIn('localStorage.getItem("pmm-perspective")', javascript)
        self.assertIn("function openCanonicalRecord(", javascript)
        self.assertIn("navigation_views", document)
        self.assertEqual(document["navigation_views"]["view_version"], "0.1.0")

    def test_navigation_does_not_collapse_tasks_traits_and_mechanisms(self) -> None:
        document = json.loads((ROOT / "site" / "data" / "pmm-data.json").read_text())
        view = document["navigation_views"]["general_psychology"]
        nodes = {node["id"]: node for node in view["nodes"]}
        memory = nodes["gp:memory"]
        types = {item["canonical_id"]: item["expected_type"] for item in memory["memberships"]}
        self.assertEqual(types["pmm:context:n-back-task"], "Context")
        self.assertEqual(types["pmm:measurement:n-back-performance"], "Measurement")
        self.assertEqual(types["pmm:mechanism:episodic-retrieval-n-back"], "Mechanism")
        self.assertIn("neither is memory itself", memory["ontological_note"]["en"])
        for node_id in ("gp:temperament", "gp:big-five"):
            self.assertEqual(nodes[node_id]["coverage"], "planned")
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


if __name__ == "__main__":
    unittest.main()

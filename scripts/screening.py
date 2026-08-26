#!/usr/bin/env python3
"""Build blinded PubMed screening packets and validate independent reviews."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "screening-review-v0.1.schema.yaml"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
USER_AGENT = "PMM-curation/0.1 (https://github.com/nebuhtit/psychological-mechanisms-map)"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML document must be an object: {path}")
    return value


def request_abstract_xml(pmids: list[str]) -> str:
    command = [
        "curl", "-fsSLG", "--max-time", "60", "--user-agent", USER_AGENT,
        "--data-urlencode", "db=pubmed", "--data-urlencode", "retmode=xml",
        "--data-urlencode", f"id={','.join(pmids)}", EFETCH_URL,
    ]
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def element_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def parse_abstracts(xml_text: str) -> dict[str, dict[str, Any]]:
    root = ET.fromstring(xml_text)
    records: dict[str, dict[str, Any]] = {}
    for article in root.findall(".//PubmedArticle"):
        pmid = element_text(article.find("./MedlineCitation/PMID"))
        title = element_text(article.find("./MedlineCitation/Article/ArticleTitle")).rstrip(".")
        sections = []
        for part in article.findall("./MedlineCitation/Article/Abstract/AbstractText"):
            text = element_text(part)
            label = part.attrib.get("Label") or part.attrib.get("NlmCategory")
            sections.append(f"{label}: {text}" if label and label != "UNASSIGNED" else text)
        records[pmid] = {
            "pmid": pmid,
            "title": title,
            "abstract": "\n".join(section for section in sections if section),
            "abstract_status": "available" if any(sections) else "missing",
            "publication_types": [
                element_text(item)
                for item in article.findall("./MedlineCitation/Article/PublicationTypeList/PublicationType")
                if element_text(item)
            ],
            "mesh_terms": [
                element_text(item)
                for item in article.findall("./MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName")
                if element_text(item)
            ],
        }
    return records


def write_immutable_json(document: dict[str, Any], path: Path) -> None:
    if path.exists():
        if read_json(path) != document:
            raise FileExistsError(f"refusing to replace changed snapshot: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_abstract_snapshot(search_snapshot: dict[str, Any], xml_text: str, retrieved_at: str) -> dict[str, Any]:
    parsed = parse_abstracts(xml_text)
    missing_records = sorted(set(search_snapshot["pmids"]) - set(parsed))
    if missing_records:
        raise ValueError(f"PubMed XML omitted records: {', '.join(missing_records)}")
    return {
        "snapshot_version": 1,
        "database": "PubMed",
        "platform": "NCBI E-utilities EFetch",
        "source_search_id": search_snapshot["search_id"],
        "source_result_count": search_snapshot["result_count"],
        "source_search_executed_at": search_snapshot["executed_at"],
        "retrieved_at": retrieved_at,
        "records": [parsed[pmid] for pmid in search_snapshot["pmids"]],
    }


def build_packet(log: dict[str, Any], abstract_snapshot: dict[str, Any], packet_id: str) -> dict[str, Any]:
    queued = {record["identifiers"].get("pmid"): record for record in log["records"]}
    records = []
    for item in abstract_snapshot["records"]:
        record = queued.get(item["pmid"])
        if not record:
            raise ValueError(f"abstract PMID is absent from curation queue: {item['pmid']}")
        records.append({
            "record_id": record["id"],
            "pmid": item["pmid"],
            "title": item["title"],
            "abstract": item["abstract"],
            "abstract_status": item["abstract_status"],
            "publication_types": item["publication_types"],
        })
    return {
        "packet_version": 1,
        "packet_id": packet_id,
        "log_id": log["log_id"],
        "search_id": abstract_snapshot["source_search_id"],
        "stage": "title_abstract",
        "blinding": "Authors, affiliations, journal names, and other reviewers' decisions are omitted.",
        "review_question": log["review_question"],
        "eligibility": log["eligibility"],
        "decision_rule": "Include or mark uncertain whenever the abstract cannot confidently establish an exclusion criterion.",
        "reason_codes": [
            "potentially_eligible", "wrong_population", "wrong_exposure", "wrong_outcome", "wrong_design",
            "wrong_publication_type", "duplicate_or_no_unique_results", "insufficient_abstract_information",
        ],
        "records": records,
    }


def new_review(packet: dict[str, Any], reviewer_id: str, review_id: str, timestamp: str) -> dict[str, Any]:
    return {
        "review_version": "0.1.0",
        "document_type": "screening_review",
        "review_id": review_id,
        "packet_id": packet["packet_id"],
        "reviewer_id": reviewer_id,
        "stage": "title_abstract",
        "status": "in_progress",
        "blinded_to_other_decisions": True,
        "decisions": [
            {"record_id": record["record_id"], "decision": "pending", "reason_code": "pending", "rationale": "", "reviewed_at": None}
            for record in packet["records"]
        ],
        "provenance": {
            "created_at": timestamp,
            "modified_at": timestamp,
            "created_by": [reviewer_id],
            "note": "Review independently before inspecting any other review file.",
        },
    }


def complete_review(review: dict[str, Any], decisions: dict[str, Any], timestamp: str) -> dict[str, Any]:
    expected = {item["record_id"] for item in review["decisions"]}
    if set(decisions) != expected:
        missing = sorted(expected - set(decisions))
        extra = sorted(set(decisions) - expected)
        raise ValueError(f"decision map mismatch; missing={missing}, extra={extra}")
    for item in review["decisions"]:
        decision = decisions[item["record_id"]]
        item.update({
            "decision": decision["decision"],
            "reason_code": decision["reason_code"],
            "rationale": decision["rationale"],
            "reviewed_at": timestamp,
        })
    review["status"] = "complete"
    review["provenance"]["modified_at"] = timestamp
    return review


def validate_review(review: dict[str, Any], packet: dict[str, Any]) -> list[str]:
    schema = read_yaml(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(review)]
    expected = [record["record_id"] for record in packet["records"]]
    actual = [decision.get("record_id") for decision in review.get("decisions", [])]
    if actual != expected:
        errors.append("decision record order or membership does not match packet")
    if review.get("packet_id") != packet.get("packet_id"):
        errors.append("review packet_id does not match packet")
    if review.get("status") == "complete" and any(item.get("decision") == "pending" for item in review.get("decisions", [])):
        errors.append("complete review contains pending decisions")
    for item in review.get("decisions", []):
        if item.get("decision") != "pending" and (not item.get("rationale") or not item.get("reviewed_at")):
            errors.append(f"{item.get('record_id')}: completed decision requires rationale and reviewed_at")
    return errors


def agreement(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    first_decisions = {item["record_id"]: item["decision"] for item in first["decisions"]}
    second_decisions = {item["record_id"]: item["decision"] for item in second["decisions"]}
    if set(first_decisions) != set(second_decisions):
        raise ValueError("reviews do not contain the same records")
    categories = ("include", "exclude", "uncertain")
    pairs = [(first_decisions[key], second_decisions[key]) for key in first_decisions]
    if any(left == "pending" or right == "pending" for left, right in pairs):
        raise ValueError("agreement requires complete reviews")
    observed = sum(left == right for left, right in pairs) / len(pairs)
    first_counts = Counter(left for left, _ in pairs)
    second_counts = Counter(right for _, right in pairs)
    expected = sum((first_counts[category] / len(pairs)) * (second_counts[category] / len(pairs)) for category in categories)
    kappa = (observed - expected) / (1 - expected) if not math.isclose(expected, 1.0) else 1.0
    return {
        "record_count": len(pairs),
        "agreement_count": sum(left == right for left, right in pairs),
        "percent_agreement": round(observed * 100, 2),
        "cohen_kappa": round(kappa, 4),
        "disagreements": [
            {"record_id": key, "reviewer_a": first_decisions[key], "reviewer_b": second_decisions[key]}
            for key in first_decisions if first_decisions[key] != second_decisions[key]
        ],
    }


def write_yaml(document: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    fetch_parser = subparsers.add_parser("fetch-abstracts")
    fetch_parser.add_argument("search_snapshot", type=Path)
    fetch_parser.add_argument("retrieved_at")
    fetch_parser.add_argument("output", type=Path)
    packet_parser = subparsers.add_parser("build-packet")
    packet_parser.add_argument("log", type=Path)
    packet_parser.add_argument("abstract_snapshot", type=Path)
    packet_parser.add_argument("packet_id")
    packet_parser.add_argument("output", type=Path)
    review_parser = subparsers.add_parser("new-review")
    review_parser.add_argument("packet", type=Path)
    review_parser.add_argument("reviewer_id")
    review_parser.add_argument("review_id")
    review_parser.add_argument("timestamp")
    review_parser.add_argument("output", type=Path)
    complete_parser = subparsers.add_parser("complete-review")
    complete_parser.add_argument("review", type=Path)
    complete_parser.add_argument("decisions", type=Path)
    complete_parser.add_argument("timestamp")
    complete_parser.add_argument("output", type=Path)
    validate_parser = subparsers.add_parser("validate-review")
    validate_parser.add_argument("packet", type=Path)
    validate_parser.add_argument("review", type=Path)
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("first", type=Path)
    compare_parser.add_argument("second", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "fetch-abstracts":
            search = read_json(args.search_snapshot)
            document = build_abstract_snapshot(search, request_abstract_xml(search["pmids"]), args.retrieved_at)
            write_immutable_json(document, args.output)
            print(f"saved: {args.output} ({len(document['records'])} records)")
        elif args.command == "build-packet":
            document = build_packet(read_yaml(args.log), read_json(args.abstract_snapshot), args.packet_id)
            write_immutable_json(document, args.output)
            print(f"saved: {args.output} ({len(document['records'])} records)")
        elif args.command == "new-review":
            write_yaml(new_review(read_json(args.packet), args.reviewer_id, args.review_id, args.timestamp), args.output)
            print(f"created: {args.output}")
        elif args.command == "complete-review":
            write_yaml(complete_review(read_yaml(args.review), read_json(args.decisions), args.timestamp), args.output)
            print(f"completed: {args.output}")
        elif args.command == "validate-review":
            errors = validate_review(read_yaml(args.review), read_json(args.packet))
            if errors:
                raise ValueError("; ".join(errors))
            print(f"valid: {args.review}")
        else:
            print(json.dumps(agreement(read_yaml(args.first), read_yaml(args.second)), indent=2))
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as error:
        print(f"screening failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

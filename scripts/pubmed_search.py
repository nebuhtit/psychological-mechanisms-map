#!/usr/bin/env python3
"""Fetch a reproducible PubMed snapshot and sync it into a PMM screening log."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
USER_AGENT = "PMM-curation/0.1 (https://github.com/nebuhtit/psychological-mechanisms-map)"


def request_json(url: str, parameters: dict[str, str]) -> dict[str, Any]:
    command = ["curl", "-fsSLG", "--max-time", "45", "--user-agent", USER_AGENT]
    for key, value in parameters.items():
        command.extend(("--data-urlencode", f"{key}={value}"))
    command.append(url)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("NCBI response must be a JSON object")
    return value


def fetch_snapshot(search_id: str, query: str, executed_at: str) -> dict[str, Any]:
    result = request_json(ESEARCH_URL, {
        "db": "pubmed",
        "retmode": "json",
        "retmax": "10000",
        "term": query,
    })["esearchresult"]
    pmids = result["idlist"]
    count = int(result["count"])
    if count != len(pmids):
        raise RuntimeError(f"PubMed returned {len(pmids)} of {count} PMIDs")

    summaries: dict[str, Any] = {}
    for start in range(0, len(pmids), 200):
        batch = pmids[start:start + 200]
        response = request_json(ESUMMARY_URL, {
            "db": "pubmed",
            "retmode": "json",
            "id": ",".join(batch),
        })["result"]
        summaries.update({pmid: response[pmid] for pmid in batch})
        if start + 200 < len(pmids):
            time.sleep(0.35)

    records = []
    for pmid in pmids:
        summary = summaries[pmid]
        records.append({
            "pmid": pmid,
            "title": summary.get("title", "").rstrip("."),
            "publication_date": summary.get("pubdate", ""),
            "journal": summary.get("fulljournalname") or summary.get("source", ""),
            "authors": [author["name"] for author in summary.get("authors", []) if author.get("name")],
        })
    return {
        "snapshot_version": 1,
        "database": "PubMed",
        "platform": "NCBI E-utilities",
        "search_id": search_id,
        "executed_at": executed_at,
        "query": query,
        "query_translation": result.get("querytranslation", ""),
        "result_count": count,
        "pmids": pmids,
        "records": records,
    }


def find_search(document: dict[str, Any], search_id: str) -> dict[str, Any]:
    for search in document.get("searches", []):
        if search.get("id") == search_id:
            return search
    raise ValueError(f"search not found: {search_id}")


def load_log(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("document_type") != "curation_log":
        raise ValueError(f"not a curation log: {path}")
    return value


def write_snapshot(snapshot: dict[str, Any], output_path: Path) -> None:
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        if existing != snapshot:
            raise FileExistsError(
                f"snapshot changed: declare a new dated search_id and export_file instead of replacing {output_path}"
            )
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_log(document: dict[str, Any], search: dict[str, Any], snapshot: dict[str, Any]) -> None:
    search_id = search["id"]
    search["result_count_status"] = "recorded"
    search["result_count"] = snapshot["result_count"]
    by_pmid = {
        record.get("identifiers", {}).get("pmid"): record
        for record in document.get("records", [])
        if record.get("identifiers", {}).get("pmid")
    }
    for item in snapshot["records"]:
        pmid = item["pmid"]
        if pmid in by_pmid:
            discovered_by = by_pmid[pmid].setdefault("discovered_by", [])
            if search_id not in discovered_by:
                discovered_by.append(search_id)
            continue
        document["records"].append({
            "id": f"record:pubmed-{pmid}",
            "title": item["title"],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "identifiers": {"pmid": pmid},
            "discovered_by": [search_id],
            "deduplication_key": f"pmid:{pmid}",
            "screening_status": "awaiting_screening",
            "reviewer_decisions": [],
        })


def write_log(document: dict[str, Any], path: Path) -> None:
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("search_id")
    parser.add_argument("--sync", action="store_true", help="add unscreened PubMed records to the YAML log")
    args = parser.parse_args()
    document = load_log(args.log)
    search = find_search(document, args.search_id)
    output = search.get("export_file")
    if not output:
        parser.error("search must define export_file")
    snapshot = fetch_snapshot(search["id"], search["strategy"], search["executed_at"])
    try:
        write_snapshot(snapshot, ROOT / output)
    except FileExistsError as error:
        parser.error(str(error))
    if args.sync:
        sync_log(document, search, snapshot)
        write_log(document, args.log)
    print(f"saved: {output} ({snapshot['result_count']} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

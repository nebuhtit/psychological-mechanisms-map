#!/usr/bin/env python3
"""Build or update the committed Russian presentation-layer translation bundle."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "site" / "data" / "pmm-data.json"
OUTPUT_PATH = ROOT / "site" / "data" / "i18n-ru.json"

# Curated terminology takes precedence over generic machine translation.
OVERRIDES = {
    "Fear extinction": "Угасание страха",
    "HPA feedback": "Обратная связь ГГН-оси",
    "Multi-task working-memory battery": "Батарея заданий на рабочую память",
    "N-back performance measurement": "Результат выполнения N-back",
    "Operation-span performance measurement": "Результат выполнения теста operation span",
    "RDoC Potential Threat (Anxiety) concerns responses when harm may occur but is distant, ambiguous, or uncertain in probability.": "Конструкт RDoC «Потенциальная угроза (тревога)» описывает реакции на возможный вред, который отдалён во времени, неоднозначен или имеет неопределённую вероятность.",
    "Verbal N-back performance showed weak convergence with operation-span performance in Kane et al. 2007.": "В исследовании Kane et al. (2007) результаты вербального N-back были лишь слабо связаны с результатами теста operation span.",
    "Working-memory capacity": "Ёмкость рабочей памяти",
    "Working-memory control": "Контроль рабочей памяти",
}


def displayed_strings(document: dict) -> set[str]:
    strings: set[str] = set()
    for family in document["families"]:
        strings.update((family["title"], family["description"]))
        for item in family["objects"]:
            strings.update((item["label"], item["definition"]))
            strings.update(item.get("boundary_notes", []))
        for claim in family["claims"]:
            strings.add(claim["statement"])
            strings.add(claim["confidence"]["rationale"])
            strings.add(claim["scope"]["population"])
            strings.update(claim.get("limitations", []))
            strings.update(claim["scope"].get("boundary_conditions", []))
        for evidence in family["evidence"]:
            strings.add(evidence["summary"])
        for source in family["sources"]:
            strings.add(source["title"])
    return {value for value in strings if value}


def translate(value: str, attempts: int = 4) -> str:
    for attempt in range(attempts):
        try:
            result = subprocess.run(
                [
                    "curl", "-fsSLG", "--max-time", "30",
                    "--data-urlencode", "client=gtx",
                    "--data-urlencode", "sl=en",
                    "--data-urlencode", "tl=ru",
                    "--data-urlencode", "dt=t",
                    "--data-urlencode", f"q={value}",
                    "https://translate.googleapis.com/translate_a/single",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            translated = "".join(part[0] for part in payload[0] if part[0])
            if translated:
                return translated
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"translation failed: {value[:80]}")


def write_bundle(strings: set[str], translations: dict[str, str], status: str) -> None:
    translations.update({key: value for key, value in OVERRIDES.items() if key in strings})
    translations = {key: value.replace("\u200b", "") for key, value in translations.items()}
    payload = {
        "language": "ru",
        "canonical_language": "en",
        "translation_status": status,
        "translations": {key: translations[key] for key in sorted(strings) if key in translations},
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    document = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    strings = displayed_strings(document)
    existing = {}
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8")).get("translations", {})
    missing = sorted(strings - existing.keys())
    print(f"catalog: {len(strings)} strings; translating: {len(missing)}")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(translate, value): value for value in missing}
        for index, future in enumerate(as_completed(futures), start=1):
            source = futures[future]
            existing[source] = future.result()
            if index % 25 == 0 or index == len(missing):
                print(f"translated: {index}/{len(missing)}")
                write_bundle(strings, existing, "generation_in_progress")
    write_bundle(strings, existing, "machine_translated_pending_review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

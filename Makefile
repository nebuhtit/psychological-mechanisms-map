.PHONY: setup validate validate-v02 site-data translate-ru report test export verify pubmed-social-buffering clean

PYTHON := .venv/bin/python

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/build_registry.py validate
	$(PYTHON) scripts/curation.py validate

validate-v02:
	$(PYTHON) scripts/pmm.py validate data/pilot-anxiety-avoidance.yaml

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

site-data:
	$(PYTHON) scripts/build_site_data.py

translate-ru:
	$(PYTHON) -u scripts/build_ru_translation.py

report:
	$(PYTHON) scripts/build_registry.py report

export:
	$(PYTHON) scripts/build_registry.py export

verify: validate test export
	git diff --exit-code -- build docs/coverage-report.md site/data/pmm-data.json

pubmed-social-buffering:
	$(PYTHON) scripts/pubmed_search.py curation/logs/social-buffering-retrospective-v0.1.yaml search:pubmed-social-buffering-cortisol-youth-2026-08-26 --sync

clean:
	$(PYTHON) scripts/pmm_v03.py clean build

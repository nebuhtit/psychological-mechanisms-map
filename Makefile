.PHONY: setup validate validate-v02 site-data test export verify clean

PYTHON := .venv/bin/python

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/build_registry.py validate

validate-v02:
	$(PYTHON) scripts/pmm.py validate data/pilot-anxiety-avoidance.yaml

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

site-data:
	$(PYTHON) scripts/build_site_data.py

export:
	$(PYTHON) scripts/build_registry.py export

verify: validate test export
	git diff --exit-code -- build site/data/pmm-data.json

clean:
	$(PYTHON) scripts/pmm_v03.py clean build

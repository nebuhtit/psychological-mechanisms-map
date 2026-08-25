.PHONY: setup validate validate-v02 validate-stress test export clean

PYTHON := .venv/bin/python

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/pmm_v03.py validate data/pilot-anxiety-avoidance-v0.3.yaml

validate-v02:
	$(PYTHON) scripts/pmm.py validate data/pilot-anxiety-avoidance.yaml

validate-stress:
	$(PYTHON) scripts/pmm_v03.py validate data/stress-test-mechanisms-v0.3.yaml

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

export:
	$(PYTHON) scripts/pmm_v03.py export data/pilot-anxiety-avoidance-v0.3.yaml build/pilot-anxiety-avoidance-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/stress-test-mechanisms-v0.3.yaml build/stress-test-mechanisms-v0.3.json

clean:
	$(PYTHON) scripts/pmm_v03.py clean build

.PHONY: setup validate validate-v02 validate-stress validate-pack validate-extinction validate-habit validate-reappraisal site-data test export verify clean

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

validate-pack:
	$(PYTHON) scripts/pmm_v03.py validate data/evidence-pack-negative-reinforcement-v0.3.yaml

validate-extinction:
	$(PYTHON) scripts/pmm_v03.py validate data/evidence-pack-fear-extinction-v0.3.yaml

validate-habit:
	$(PYTHON) scripts/pmm_v03.py validate data/evidence-pack-habit-control-v0.3.yaml

validate-reappraisal:
	$(PYTHON) scripts/pmm_v03.py validate data/evidence-pack-cognitive-reappraisal-v0.3.yaml

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

site-data:
	$(PYTHON) scripts/build_site_data.py

export: site-data
	$(PYTHON) scripts/pmm_v03.py export data/pilot-anxiety-avoidance-v0.3.yaml build/pilot-anxiety-avoidance-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/stress-test-mechanisms-v0.3.yaml build/stress-test-mechanisms-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/evidence-pack-negative-reinforcement-v0.3.yaml build/evidence-pack-negative-reinforcement-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/evidence-pack-fear-extinction-v0.3.yaml build/evidence-pack-fear-extinction-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/evidence-pack-habit-control-v0.3.yaml build/evidence-pack-habit-control-v0.3.json
	$(PYTHON) scripts/pmm_v03.py export data/evidence-pack-cognitive-reappraisal-v0.3.yaml build/evidence-pack-cognitive-reappraisal-v0.3.json

verify: validate validate-stress validate-pack validate-extinction validate-habit validate-reappraisal test export
	git diff --exit-code -- build site/data/pmm-data.json

clean:
	$(PYTHON) scripts/pmm_v03.py clean build

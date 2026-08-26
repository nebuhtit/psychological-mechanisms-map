# Independent title/abstract screening

The canonical blinded packet is `curation/review-packets/social-buffering-title-abstract-v0.1.json`.

Reviewer B must not inspect `social-buffering-reviewer-a-v0.1.yaml` before completing and locking their own decisions. The repository cannot cryptographically enforce this separation; the review process must enforce it procedurally or assign Reviewer B a packet-only copy.

Create a private Reviewer B form:

```bash
.venv/bin/python scripts/screening.py new-review \
  curation/review-packets/social-buffering-title-abstract-v0.1.json \
  reviewer-b \
  pmm:screening-review:social-buffering-reviewer-b-v0-1 \
  2026-08-26T12:10:00+03:00 \
  curation/private-reviews/social-buffering-reviewer-b-v0.1.yaml
```

For every record, replace `pending` with `include`, `exclude`, or `uncertain`, add one controlled `reason_code`, a short rationale, and the actual review timestamp. Set `status: complete` only after all 51 records have decisions.

Validate without reading Reviewer A:

```bash
.venv/bin/python scripts/screening.py validate-review \
  curation/review-packets/social-buffering-title-abstract-v0.1.json \
  curation/private-reviews/social-buffering-reviewer-b-v0.1.yaml
```

After Reviewer B has locked the file, calculate agreement:

```bash
.venv/bin/python scripts/screening.py compare \
  curation/reviews/social-buffering-reviewer-a-v0.1.yaml \
  curation/private-reviews/social-buffering-reviewer-b-v0.1.yaml
```

Do not update the main curation log from either review alone. Reconcile disagreements first, preserve both original decisions, name the adjudicator where required, and then record consensus.

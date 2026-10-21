---
id: ISMS-PRC-003
title: Control of Documented Information
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: ["7.5"]
annex_a: ["5.33", "5.37"]
last_reviewed: ""
next_review: ""
---

# Control of Documented Information

## 1. Document identification
Every ISMS document is a Markdown file with YAML front matter containing:
`id`, `title`, `version`, `status` (Draft / Approved / Retired), `owner`, `approver`, `classification`, `iso_clauses`, `annex_a`, `last_reviewed`, `next_review`.

ID prefixes:
| Prefix | Type |
|---|---|
| ISMS-POL | Policy |
| ISMS-PRC | Procedure / process |
| ISMS-DOC | Other ISMS document |
| ISMS-REC | Record template |

Registers are CSV files in `registers/`.

## 2. Creating and updating (7.5.2)
1. Make changes on a branch and open a pull request. The pull request description says **what** changed and **why**.
2. The document **owner** reviews. The **approver** gives approval by approving the pull request. Branch protection requires at least one approval, plus passing CI (`tools/validate_isms.py`).
3. When the pull request is merged, update `version` and `last_reviewed`, and set `status: Approved`.
4. Git history is the change record: who, when and what changed.

Versioning: increase the minor version (0.1 → 0.2) for editorial changes, and the major version (1.x → 2.0) for changes in substance.

## 3. Control (7.5.3)
- **Availability:** the approved version is the `main` branch. Published copies (PDF or intranet) are generated from `main` and show their version.
- **Protection:** repository access follows the access control policy (ISMS-POL-002). Write access is limited to ISMS contributors. `main` is protected.
- **Retention:** records are kept for at least {{RETENTION_YEARS}} years, or longer if law or contract requires it (control 5.33). Retired documents stay in git history.
- **Documents of external origin** (standards, contracts, supplier certificates) are listed in `registers/legal-regulatory-register.csv` or stored in {{DMS_LOCATION}} with restricted access.
- **Sensitive records** (for example incident evidence and personal data) are **not** stored in this repository. Store them in {{SECURE_RECORDS_LOCATION}} and reference them by ID.

## 4. Review
Each document is reviewed by its `next_review` date, and at least annually. The validator reports overdue reviews.

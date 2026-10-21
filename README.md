# ISO/IEC 27001 Information Security Management System

A documentation-as-code ISMS for {{ORG_NAME}}. Policies, procedures and registers are versioned in git. Changes are approved through pull requests, and CI checks that the system stays internally consistent.

## Which standard edition?
This ISMS is built against **ISO/IEC 27001:2022 including Amendment 1:2024** (climate change). That is the current certifiable edition: **no ISO/IEC 27001:2026 has been published** (as of October 2026). Only the vocabulary standard ISO/IEC 27000 had a 2026 edition. If a new edition is released:
1. Add a new reference catalogue, for example `registers/reference-annex-a-20XX.csv`, and point `REFERENCE_CATALOGUE` in `tools/validate_isms.py` to it.
2. Run the validator. It lists every SoA row and document reference that must be remapped.
3. Update the clause mapping below and do a transition gap assessment.

Companion standards worth buying: ISO/IEC 27002:2022 (control guidance), ISO/IEC 27005:2022 (risk management) and ISO 19011 (auditing).

## Repository layout
```
docs/                    ISMS core documents, organized by clause (4–10)
policies/                Topic-specific policies supporting Annex A controls
registers/               CSV registers: SoA, risks, assets, interested parties, legal, audits, NCs
tools/validate_isms.py   Consistency checks (run locally and in CI)
```

## Mandatory documented information map
| Clause | Requirement | Location |
|---|---|---|
| 4.3 | ISMS scope | `docs/01-context/ISMS-DOC-002-isms-scope.md` |
| 5.2 | Information security policy | `docs/02-leadership/ISMS-POL-000-information-security-policy.md` |
| 6.1.2 | Risk assessment process | `docs/03-planning/ISMS-PRC-001-risk-management-methodology.md` |
| 6.1.3 | Risk treatment process | `docs/03-planning/ISMS-PRC-001-risk-management-methodology.md` |
| 6.1.3 d | Statement of Applicability | `registers/statement-of-applicability.csv` |
| 6.2 | Information security objectives | `docs/03-planning/ISMS-DOC-004-information-security-objectives.md` |
| 7.2 | Evidence of competence | `docs/04-support/ISMS-DOC-005-competence-and-awareness.md` + HR records |
| 7.5.1 b | Documents the organization determines as necessary | This repository; `ISMS-PRC-003` |
| 8.1 | Evidence that processes ran as planned | `docs/05-operation/ISMS-DOC-007-operational-planning-and-control.md` + records |
| 8.2 | Risk assessment results | `registers/risk-register.csv` |
| 8.3 | Risk treatment results | `registers/risk-register.csv` |
| 9.1 | Monitoring and measurement results | `docs/06-performance/ISMS-PRC-004-monitoring-and-measurement.md` + metrics |
| 9.2 | Audit programme and results | `registers/internal-audit-programme.csv`, `ISMS-PRC-005` |
| 9.3 | Management review results | `docs/06-performance/ISMS-PRC-006-management-review.md` + minutes |
| 10.2 | Nonconformities and corrective actions | `registers/nonconformity-log.csv`, `ISMS-PRC-007` |

Context (4.1, including the climate change determination) and interested parties (4.2) are in `ISMS-DOC-001` and `registers/interested-parties.csv`. Roles (5.3) are in `ISMS-DOC-003`.

## Implementation roadmap
| Phase | Activities | Output |
|---|---|---|
| 1. Initiate | Get management commitment; appoint the CISO; set the budget | Signed policy, roles |
| 2. Context and scope | Fill in ISMS-DOC-001 and ISMS-DOC-002; interested parties; legal register | Approved scope |
| 3. Risk | Build the asset inventory; run the risk assessment; decide applicability for all 93 controls | Risk register, SoA v1.0 |
| 4. Treat | Implement controls and policies; train staff; collect evidence | Treatment plan progress |
| 5. Operate and measure | Run the operating calendar for at least 2–3 months; collect metrics | Records, metrics |
| 6. Check | Full internal audit; management review; corrective actions | Audit report, minutes |
| 7. Certify | Stage 1 (documentation) and Stage 2 (implementation) audits by an accredited certification body | Certificate (3-year cycle, annual surveillance) |

## Working with this repository
1. Replace the `{{PLACEHOLDERS}}`. The validator lists the ones that remain.
2. Make changes on a branch and open a pull request. The approver approves the pull request (see ISMS-PRC-003).
3. Run `python3 tools/validate_isms.py` before pushing. Use `--strict` once you are preparing for audit: then warnings (draft documents, undecided SoA rows, placeholders, overdue reviews) fail the build.
4. Do **not** store evidence, personal data, secrets or incident details here. Keep them in the secure records location and reference them by ID.

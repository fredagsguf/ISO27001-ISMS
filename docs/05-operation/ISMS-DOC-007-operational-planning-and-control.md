---
id: ISMS-DOC-007
title: Operational Planning and Control
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["8.1", "8.2", "8.3"]
annex_a: ["5.37"]
last_reviewed: ""
next_review: ""
---

# Operational Planning and Control

## 1. Operational planning (8.1)
The organization plans, implements and controls the processes needed to meet ISMS requirements and to carry out the actions from clause 6 by:
- setting criteria for the processes (policies, procedures, SLAs and the metrics in ISMS-PRC-004)
- running the processes according to those criteria
- keeping documented information to the extent needed to be confident the processes ran as planned

## 2. ISMS operating calendar
| Activity | Frequency | Owner | Record |
|---|---|---|---|
| Risk assessment review | Annually + on change | CISO | Risk register |
| Risk treatment plan progress | Monthly | Risk owners | Risk register / tickets |
| SoA review | Annually + on change | CISO | SoA |
| Access reviews (privileged) | Quarterly | System owners | Review records |
| Access reviews (standard) | Semi-annually | Managers | Review records |
| Vulnerability scanning | Continuous / weekly | IT | Scanner reports |
| Backup restore test | Quarterly | IT | Test records |
| Supplier security review | Annually (critical suppliers) | Procurement / CISO | Supplier register |
| BC / ICT readiness test | Annually | CTO | Exercise report |
| Awareness training | Annually | HR | Training records |
| Phishing simulation | Quarterly | CISO | Reports |
| Internal audit | Per programme | Internal auditor | Audit reports |
| Management review | At least annually | CEO | Minutes |
| Policy review | Annually | Policy owners | Git history |

## 3. Externally provided processes, products or services
Externally provided processes, products or services relevant to the ISMS are determined and controlled through ISMS-POL-005 (supplier security).

## 4. Risk assessment and treatment in operation (8.2, 8.3)
Risk assessments are done at the planned intervals and when significant changes are proposed or happen. Treatment plans are implemented according to ISMS-PRC-001. Results are kept in `registers/risk-register.csv`.

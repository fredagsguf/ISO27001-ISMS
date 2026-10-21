---
id: ISMS-DOC-002
title: ISMS Scope Statement
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["4.3", "4.4"]
annex_a: []
last_reviewed: ""
next_review: ""
---

# ISMS Scope Statement

> **Mandatory documented information** (clause 4.3). The scope statement normally appears on the certificate, so keep it precise.

## 1. Scope statement
"The information security management system of {{ORG_NAME}} covers the {{DESIGN_DEVELOPMENT_OPERATION}} of {{PRODUCT_OR_SERVICE}}, including supporting functions of {{HR_FINANCE_IT}}, operated from {{SITES}} and the {{CLOUD_PROVIDER}} {{REGIONS}} environment. It is in accordance with Statement of Applicability version {{SOA_VERSION}}."

## 2. Inputs considered
- External and internal issues (ISMS-DOC-001, section 4–6)
- Requirements of interested parties (`registers/interested-parties.csv`)
- Interfaces and dependencies between activities done by the organization and activities done by other organizations

## 3. Boundaries
| Dimension | In scope | Out of scope (with justification) |
|---|---|---|
| Organizational units | {{UNITS}} | {{EXCLUDED_UNITS_AND_WHY}} |
| Locations | {{SITES}} | {{EXCLUDED_SITES_AND_WHY}} |
| Information systems | {{SYSTEMS}} | {{EXCLUDED_SYSTEMS_AND_WHY}} |
| Processes | {{PROCESSES}} | — |

## 4. Interfaces and dependencies
| Interface | Party | Managed by |
|---|---|---|
| Cloud hosting (IaaS/PaaS) | {{CLOUD_PROVIDER}} | ISMS-POL-005, control 5.23 |
| Identity provider | {{IDP}} | ISMS-POL-002 |
| Outsourced HR / payroll | {{PROVIDER}} | ISMS-POL-005 |
| {{OTHER}} | | |

## 5. The ISMS and its processes (clause 4.4)
The ISMS follows the Plan-Do-Check-Act cycle. The documents in this repository implement it:

| PDCA | Clauses | Documents |
|---|---|---|
| Plan | 4, 5, 6 | ISMS-DOC-001/002/003/004, ISMS-POL-000, ISMS-PRC-001/002 |
| Do | 7, 8 | ISMS-PRC-003, ISMS-DOC-005/006/007, topic-specific policies |
| Check | 9 | ISMS-PRC-004/005/006 |
| Act | 10 | ISMS-PRC-007 |

---
id: ISMS-DOC-003
title: ISMS Roles, Responsibilities and Authorities
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["5.1", "5.3"]
annex_a: ["5.2", "5.3", "5.4"]
last_reviewed: ""
next_review: ""
---

# ISMS Roles, Responsibilities and Authorities

## 1. Purpose
This document assigns and communicates the responsibilities and authorities for roles relevant to information security (clause 5.3).

## 2. Roles
| Role | Holder | Responsibilities | Authorities |
|---|---|---|---|
| Top management | {{CEO}} + leadership team | Shows leadership and commitment (5.1). Approves the policy, objectives, risk acceptance criteria and resources. Chairs management review. | Final approval and risk acceptance above the threshold |
| ISMS manager / CISO | {{CISO}} | Makes sure the ISMS conforms to ISO/IEC 27001. Reports ISMS performance to top management. Coordinates risk assessment, the SoA, audits and improvement. | Can stop activities that create unacceptable risk, pending management decision |
| Risk owners | Per risk register | Approve treatment plans and accept residual risk for their risks | Accept residual risk within the acceptance criteria |
| Asset owners | Per asset inventory | Classify assets, define access, and make sure controls are applied | Approve access to their assets |
| Control owners | Per SoA | Implement, operate and measure assigned controls | — |
| Data Protection Officer | {{DPO}} | Privacy compliance (5.34). Breach notification decisions. | Advise and escalate |
| IT / Engineering lead | {{CTO}} | Technological controls, change management, secure development | Approve production changes |
| HR lead | {{HR_LEAD}} | Screening, employment terms, awareness, disciplinary process, leavers | — |
| Internal auditor | {{AUDITOR}} | Plans and runs internal audits independently | Access to all records needed for audits |
| All personnel | — | Follow policies; report events and weaknesses (6.8) | — |

## 3. Segregation of duties (control 5.3)
These combinations of duties must not be held by the same person without compensating controls approved by the CISO:
- Requesting and approving access rights
- Developing and deploying code to production without peer review
- Administering logs and being the subject of those logs
- Auditing an area one is responsible for operating

## 4. Information security committee
| Item | Value |
|---|---|
| Members | {{CEO}}, {{CISO}}, {{CTO}}, {{HR_LEAD}}, {{DPO}} |
| Frequency | Monthly (operational); management review at least annually |
| Inputs | Risk status, incidents, metrics, audit findings, changes |
| Records | Minutes stored in {{RECORDS_LOCATION}} |

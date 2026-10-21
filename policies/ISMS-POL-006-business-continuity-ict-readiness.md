---
id: ISMS-POL-006
title: Business Continuity and ICT Readiness Policy
version: 0.1
status: Draft
owner: "{{CTO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["5.29", "5.30", "7.5", "7.11", "8.14"]
last_reviewed: ""
next_review: ""
---

# Business Continuity and ICT Readiness Policy

## 1. Objectives
Keep information security at an appropriate level during disruption (5.29), and make sure ICT services can be recovered within agreed targets (5.30).

## 2. Business impact analysis
| Service | Owner | RTO | RPO | Minimum security during disruption |
|---|---|---|---|---|
| {{CORE_SERVICE}} | {{OWNER}} | {{e.g. 4 h}} | {{e.g. 15 min}} | MFA, logging and encryption must remain active |
| Email & collaboration | IT | 8 h | 24 h | — |

## 3. Requirements
- Production runs across multiple availability zones. Critical services have documented redundancy (8.14).
- Backups follow ISMS-POL-009 and meet the RPO.
- Recovery runbooks exist for each critical service.
- Physical and environmental threats (7.5) and supporting utilities (7.11) are addressed by the hosting provider's controls (verified under ISMS-POL-005) and the office measures in {{OFFICE_MEASURES}}.
- Climate-related physical risks (flooding, heat, power) are considered when choosing hosting regions and sites (see ISMS-DOC-001, section 6).

## 4. Testing
The BC/DR plans are exercised at least annually (tabletop and technical failover/restore). Results and improvements are recorded.

---
id: ISMS-POL-004
title: Information Security Incident Management Policy
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["5.24", "5.25", "5.26", "5.27", "5.28", "6.8"]
last_reviewed: ""
next_review: ""
---

# Information Security Incident Management Policy

## 1. Reporting (6.8)
Everyone must report suspected information security events and weaknesses **immediately**. Use {{SECURITY_EMAIL}}, {{CHAT_CHANNEL}} or call {{PHONE}}. Do not investigate on your own, and do not delete evidence.

## 2. Planning and preparation (5.24)
- The incident response team: Incident Manager ({{CISO}}), IT/Engineering ({{CTO}}), DPO, Communications, Legal.
- Playbooks for ransomware, account compromise, data leak, lost device and DDoS are kept in {{PLAYBOOK_LOCATION}}.
- Tabletop exercises are held at least annually.

## 3. Assessment and decision (5.25)
| Severity | Criteria | Response target |
|---|---|---|
| SEV-1 Critical | Confirmed breach of Confidential/Restricted data; major outage; ransomware | Respond within 15 min, 24/7 |
| SEV-2 High | Probable compromise; limited data exposure; key service degraded | Within 1 h |
| SEV-3 Medium | Contained malware; policy violation with potential impact | Within 1 working day |
| SEV-4 Low | Event with no impact | Within 3 working days |

## 4. Response (5.26)
Identify → Contain → Eradicate → Recover → Communicate, following the playbooks. Decisions and actions are logged with timestamps in the incident record.

**Regulatory notification:** the DPO assesses personal data breaches for notification within **72 hours** (GDPR Art. 33). If NIS2 applies: early warning within **24 h**, notification within **72 h**, final report within **1 month**. Customer notification follows contract terms (see ISMS-DOC-006).

## 5. Evidence (5.28)
Evidence is collected, preserved and handled with chain of custody in a way that makes it admissible, using forensic copies where possible. It is stored in {{SECURE_RECORDS_LOCATION}}.

## 6. Learning (5.27)
A post-incident review is held for every SEV-1 and SEV-2 within 10 working days. The root cause and actions are logged in the nonconformity log (ISMS-PRC-007), and the risk register is updated.

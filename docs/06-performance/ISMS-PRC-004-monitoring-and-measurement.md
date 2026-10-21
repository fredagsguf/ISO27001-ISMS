---
id: ISMS-PRC-004
title: Monitoring, Measurement, Analysis and Evaluation
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["9.1"]
annex_a: ["5.36"]
last_reviewed: ""
next_review: ""
---

# Monitoring, Measurement, Analysis and Evaluation

> **Mandatory documented information:** evidence of the monitoring and measurement results (9.1).

For each metric, the table defines what is measured, the method, when it is measured, who measures, and when and by whom the results are analysed and evaluated.

| ID | Metric | Target | Method / source | Frequency | Measured by | Analysed by / when |
|---|---|---|---|---|---|---|
| M-01 | % staff who completed awareness training | ≥ 95% | Training platform export | Monthly | HR | CISO, monthly committee |
| M-02 | Phishing simulation click rate | < 5% | Simulation platform | Quarterly | CISO | Committee |
| M-03 | Critical vulnerabilities fixed within SLA | ≥ 95% | Vulnerability scanner | Monthly | IT | CTO + CISO, monthly |
| M-04 | Backup restore tests that meet RTO/RPO | 100% | Test records | Quarterly | IT | CTO, quarterly |
| M-05 | Access reviews completed on time | 100% | Review records | Quarterly | System owners | CISO, quarterly |
| M-06 | Security incidents (by severity) and mean time to resolve | Trend down | Incident register | Monthly | Incident manager | Committee |
| M-07 | Risk treatment actions overdue | 0 | Risk register / tickets | Monthly | CISO | Committee |
| M-08 | Corrective actions closed on time | ≥ 90% | Nonconformity log | Monthly | CISO | Committee |
| M-09 | Critical suppliers assessed in the last 12 months | 100% | Supplier register | Quarterly | Procurement | CISO |
| M-10 | Endpoints compliant (encryption, EDR, patch level) | ≥ 98% | MDM / EDR console | Monthly | IT | CTO |

Results are kept in {{METRICS_LOCATION}} and summarized for management review (ISMS-PRC-006). Compliance with policies (5.36) is checked through these metrics, internal audits and spot checks.

---
id: ISMS-PRC-007
title: Continual Improvement, Nonconformity and Corrective Action
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["10.1", "10.2"]
annex_a: ["5.27"]
last_reviewed: ""
next_review: ""
---

# Continual Improvement, Nonconformity and Corrective Action

> **Mandatory documented information:** the nature of nonconformities and actions taken, and the results of corrective actions (10.2).

## 1. Sources of nonconformities
Internal and external audits, incidents (lessons learned, 5.27), monitoring results, complaints, management review, and self-identification by staff.

## 2. Process
1. **React:** take action to control and correct the nonconformity, and deal with the consequences (the *correction*).
2. **Record:** log it in `registers/nonconformity-log.csv` (ID, source, description, clause/control).
3. **Evaluate the need for action:** find the **root cause** (5 Whys, fishbone), and check whether similar nonconformities exist or could occur.
4. **Corrective action:** implement the action needed to remove the root cause, with an owner and due date.
5. **Verify effectiveness:** after a suitable period, check that the problem has not recurred. Record the result in `effectiveness_verified`.
6. **Update the ISMS** if needed (risks, controls, documents).

Target closure times: Major NC within 30 days (or before the certification audit), Minor NC within 90 days.

## 3. Continual improvement (10.1)
Improvement opportunities come from metrics, audits, incidents, management review and staff suggestions. They are logged as `type: OFI` in the nonconformity log, prioritized by the information security committee, and tracked to completion.

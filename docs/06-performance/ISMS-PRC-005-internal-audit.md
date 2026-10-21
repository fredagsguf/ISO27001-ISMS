---
id: ISMS-PRC-005
title: Internal Audit Procedure
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["9.2.1", "9.2.2"]
annex_a: ["5.35", "8.34"]
last_reviewed: ""
next_review: ""
---

# Internal Audit Procedure

> **Mandatory documented information:** evidence of the audit programme(s) and the audit results (9.2.2).

## 1. Objective
Find out whether the ISMS conforms to the organization's own requirements and to ISO/IEC 27001, and whether it is effectively implemented and maintained.

## 2. Audit programme
- Maintained in `registers/internal-audit-programme.csv`.
- **All clauses 4–10 and all applicable Annex A controls** are covered within each certification cycle (3 years), and the core clauses every year.
- Frequency and priority take into account the importance of the processes, the risk register, and the results of previous audits.

## 3. Auditor selection
Auditors must be competent (ISO 19011 principles) and **objective and impartial**: they do not audit their own work. An external auditor can be used where no independent internal resource exists. Independence is recorded in the programme.

## 4. Audit process
1. **Plan:** define the scope, criteria and schedule, and notify auditees.
2. **Prepare:** review documents and the previous findings. Write a checklist.
3. **Run:** interviews, observation and sampling of records. Audit tests on operational systems are planned and agreed to minimise disruption (8.34).
4. **Report:** findings graded as **Major NC**, **Minor NC**, **Observation** or **Opportunity for improvement**. Report to the relevant management.
5. **Follow up:** log nonconformities in `registers/nonconformity-log.csv` and handle them according to ISMS-PRC-007.

## 5. Independent review (5.35)
The ISMS approach is independently reviewed at planned intervals or when significant changes occur. Examples are external audits and penetration tests.

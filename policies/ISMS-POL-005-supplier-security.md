---
id: ISMS-POL-005
title: Supplier and Cloud Security Policy
version: 0.1
status: Draft
owner: "{{PROCUREMENT_LEAD}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["5.19", "5.20", "5.21", "5.22", "5.23", "8.30"]
last_reviewed: ""
next_review: ""
---

# Supplier and Cloud Security Policy

## 1. Supplier tiering (5.19)
| Tier | Criteria | Due diligence | Review |
|---|---|---|---|
| Critical | Processes Confidential/Restricted data, or failure stops core service | Security questionnaire + certificate/report (ISO 27001, SOC 2 Type II) + DPA | Annually |
| Important | Access to Internal data or systems | Questionnaire + DPA if personal data | Every 2 years |
| Low | No data or system access | Basic check | On renewal |

A supplier register is maintained in {{SUPPLIER_REGISTER}}.

## 2. Agreements (5.20)
Contracts with Critical and Important suppliers include: security requirements, confidentiality, incident notification (within {{HOURS}} h), right to audit or to receive assurance reports, sub-processor control, data return and deletion on exit, and a DPA where personal data is processed.

## 3. ICT supply chain (5.21)
Suppliers must pass security requirements down to their sub-suppliers. Software components are tracked (SBOM) and checked for vulnerabilities (see ISMS-POL-008).

## 4. Monitoring and change (5.22)
Supplier performance, certificates and incidents are reviewed at the frequency set by the tier. Significant changes to a supplier service trigger a risk reassessment.

## 5. Cloud services (5.23)
- Cloud services are approved by IT and Security before use. Unapproved SaaS ("shadow IT") is not allowed.
- For each service, the shared responsibility split is documented, with SSO/MFA enabled, logging enabled, data location confirmed, and an exit strategy.
- Cloud configurations are monitored against baselines (CSPM: {{CSPM_TOOL}}).

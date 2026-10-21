---
id: ISMS-DOC-001
title: Context of the Organization
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["4.1", "4.2"]
annex_a: []
last_reviewed: ""
next_review: ""
---

# Context of the Organization

## 1. Purpose
This document records the internal and external issues that affect {{ORG_NAME}}'s ability to achieve the intended outcomes of its ISMS (clause 4.1). It also records the interested parties and their requirements (clause 4.2).

## 2. Organization overview
| Item | Description |
|---|---|
| Legal entity | {{ORG_NAME}} |
| Core business | {{DESCRIBE_PRODUCTS_SERVICES}} |
| Locations | {{SITES}} |
| Headcount | {{HEADCOUNT}} |
| Key technology | {{CLOUD_PROVIDER}}, {{KEY_SYSTEMS}} |

## 3. Intended outcomes of the ISMS
- Protect the confidentiality, integrity and availability of customer and company information.
- Meet legal, regulatory and contractual obligations (see `registers/legal-regulatory-register.csv`).
- Provide assurance to customers and stakeholders through certification.
- {{ADD_OUTCOME}}

## 4. Internal issues (clause 4.1)
| # | Issue | Effect on the ISMS | Treated in |
|---|---|---|---|
| I-1 | Culture and security awareness maturity | Human error risk | ISMS-DOC-005 |
| I-2 | Rapid growth / hiring | Joiner-mover-leaver control load | ISMS-POL-002 |
| I-3 | Dependence on a small number of key engineers | Availability of knowledge | Risk register |
| I-4 | Technology stack and technical debt | Vulnerability exposure | ISMS-POL-009 |
| I-5 | Budget and resources for security | Treatment capacity | ISMS-PRC-006 |

## 5. External issues (clause 4.1)
Use a PESTLE lens: political, economic, social, technological, legal, environmental.

| # | Issue | Effect on the ISMS | Treated in |
|---|---|---|---|
| E-1 | Threat landscape (ransomware, phishing, supply-chain attacks) | Likelihood of incidents | Risk register; control 5.7 |
| E-2 | Regulation (GDPR, NIS2, DORA, sector rules) | Compliance obligations | Legal register |
| E-3 | Customer security requirements and questionnaires | Contractual requirements | ISMS-POL-005 |
| E-4 | Reliance on cloud and SaaS suppliers | Concentration risk | ISMS-POL-005 |
| E-5 | Economic conditions | Budget pressure | Management review |

## 6. Climate change (clause 4.1, Amendment 1:2024)
The organization **shall determine whether climate change is a relevant issue**.

**Determination:** {{YES_OR_NO}}. **Rationale:** {{RATIONALE}}

Typical considerations:
- Physical risk to sites, data centres and suppliers (flooding, heat, power outages). This links to controls 5.29, 5.30, 7.5, 7.11 and 8.14.
- Customer, investor or regulatory expectations on climate disclosure and resilience.
- Hosting region selection and supplier resilience.

## 7. Interested parties (clause 4.2)
Interested parties, their relevant requirements, and which requirements the ISMS addresses are maintained in **`registers/interested-parties.csv`**. As required by Amendment 1:2024, that register notes when an interested party has climate-change-related requirements.

## 8. Review
Review at least annually, and whenever a significant change occurs (see ISMS-PRC-002). The results are an input to management review (ISMS-PRC-006).

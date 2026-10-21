---
id: ISMS-PRC-001
title: Information Security Risk Management Methodology
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CEO}}"
classification: Internal
iso_clauses: ["6.1.1", "6.1.2", "6.1.3", "8.2", "8.3"]
annex_a: []
last_reviewed: ""
next_review: ""
---

# Information Security Risk Management Methodology

> **Mandatory documented information:** the risk assessment process (6.1.2), the risk treatment process (6.1.3), and the results of risk assessment (8.2) and risk treatment (8.3). The methodology follows the principles of ISO/IEC 27005 and gives consistent, valid and comparable results.

## 1. When risk assessment is done
- A full assessment at least **annually**
- When a **significant change** happens (new system, supplier, location, regulation or major incident; see ISMS-PRC-002)
- Before a new product or service goes live (control 5.8)

## 2. Risk identification
Risks to confidentiality, integrity and availability are identified using an **asset-based** approach, supplemented by **scenarios**:
1. Take assets from `registers/asset-inventory.csv`.
2. For each asset or asset group, identify credible threats and the vulnerabilities they could exploit.
3. Assign a **risk owner**: the person accountable and with authority to manage the risk.
4. Record the risk in `registers/risk-register.csv`.

Also consider the issues in ISMS-DOC-001 and the requirements in `registers/interested-parties.csv` (6.1.1).

## 3. Risk analysis
### 3.1 Likelihood
| Score | Level | Description |
|---|---|---|
| 1 | Rare | Not expected within 5 years |
| 2 | Unlikely | Could happen within 5 years |
| 3 | Possible | Could happen within 1–2 years |
| 4 | Likely | Expected within a year |
| 5 | Almost certain | Expected several times a year |

### 3.2 Impact
| Score | Level | Financial | Customers / reputation | Legal / regulatory | Operations |
|---|---|---|---|---|---|
| 1 | Negligible | < {{AMOUNT_1}} | No noticeable effect | None | < 1 h disruption |
| 2 | Minor | < {{AMOUNT_2}} | Few customers affected | Minor non-compliance | < 4 h |
| 3 | Moderate | < {{AMOUNT_3}} | Local media; complaints | Reportable incident | < 1 day |
| 4 | Major | < {{AMOUNT_4}} | National media; customer loss | Regulatory sanction likely | < 1 week |
| 5 | Severe | ≥ {{AMOUNT_4}} | Lasting brand damage | Major fine / licence risk | > 1 week |

Use the **highest** applicable impact column.

### 3.3 Risk score
**Risk score = Likelihood × Impact** (1–25).

| Score | Level | Required action |
|---|---|---|
| 1–4 | Low | Accept; monitor at annual review |
| 5–9 | Medium | Treat where cost-effective; risk owner may accept |
| 10–16 | High | Must be treated; residual risk accepted by top management |
| 17–25 | Critical | Immediate treatment; escalate to top management |

## 4. Risk acceptance criteria
- Residual risks scored **≤ 9** can be accepted by the risk owner.
- Residual risks scored **10–16** need acceptance by top management, recorded in the risk register.
- Residual risks scored **≥ 17** cannot be accepted, except by a documented decision of the CEO with a time limit and a review date.

## 5. Risk treatment (6.1.3)
For each risk above the acceptance level, choose one or more options:
- **Modify:** apply controls to reduce likelihood or impact.
- **Avoid:** stop the activity that creates the risk.
- **Share:** transfer part of the risk, for example through insurance or contracts. Accountability stays with the organization.
- **Retain:** accept the risk according to the criteria in section 4.

Then:
1. Determine **all controls needed** to implement the chosen option, from any source.
2. **Compare with Annex A** to make sure no necessary control has been omitted.
3. Update the **Statement of Applicability** (`registers/statement-of-applicability.csv`) with the necessary controls, the justification for including them, whether they are implemented, and the justification for any Annex A exclusions.
4. Write the **risk treatment plan**: the treatment actions, owner, due date and resources in the risk register, with tasks tracked in {{TICKETING_SYSTEM}}.
5. Get the **risk owner's approval** of the plan and **acceptance of the residual risk** (`acceptance_status` = Accepted).

## 6. Records
- `registers/risk-register.csv`: risk assessment and treatment results (8.2, 8.3)
- `registers/statement-of-applicability.csv`: the SoA (6.1.3 d)
- `python tools/validate_isms.py` checks that scores are consistent and that controls referenced from the risk register exist.

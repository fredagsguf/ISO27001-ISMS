---
id: ISMS-POL-003
title: Information Classification and Handling Policy
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["5.12", "5.13", "5.14", "5.33", "5.34", "8.10", "8.11", "8.12"]
last_reviewed: ""
next_review: ""
---

# Information Classification and Handling Policy

## 1. Classification levels (5.12)
| Level | Description | Examples |
|---|---|---|
| **Public** | Approved for public release | Marketing material, public policy |
| **Internal** | Default for business information; low harm if disclosed | Internal procedures, org charts |
| **Confidential** | Significant harm if disclosed | Customer data, personal data, contracts, source code |
| **Restricted** | Severe harm; strictly need-to-know | Encryption keys, credentials, special-category personal data, M&A |

The information owner classifies the information. Unclassified information is treated as **Internal**.

## 2. Labelling (5.13)
Documents classified Confidential or Restricted are labelled in the header or footer, or with metadata labels ({{LABEL_TOOL}}). Systems are labelled by the highest classification they hold, as recorded in the asset inventory.

## 3. Handling rules
| Activity | Internal | Confidential | Restricted |
|---|---|---|---|
| Storage | Approved company systems | Approved systems, encrypted at rest | Dedicated restricted stores or vaults; encrypted |
| Transfer (5.14) | Company channels | Encrypted channels; approved file sharing with expiry | Encrypted end to end; named recipients only |
| External sharing | With NDA or contract | Owner approval + NDA/DPA | Owner + CISO approval |
| Printing | Allowed | Avoid; collect immediately | Not allowed without approval |
| Deletion (8.10) | Standard deletion | Secure deletion per retention schedule | Cryptographic erase or certified destruction |

## 4. Privacy and records (5.33, 5.34)
Personal data is processed according to the privacy programme and GDPR. Records are retained according to {{RETENTION_SCHEDULE}}.

## 5. Data masking and leakage prevention (8.11, 8.12)
Personal or confidential data used outside production is masked or pseudonymized. DLP controls in {{DLP_TOOL}} monitor and block unauthorized transfer of Confidential and Restricted data.

---
id: ISMS-POL-007
title: Cryptography and Key Management Policy
version: 0.1
status: Draft
owner: "{{CTO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["8.24"]
last_reviewed: ""
next_review: ""
---

# Cryptography and Key Management Policy

## 1. Requirements
| Use | Minimum standard |
|---|---|
| Data in transit | TLS 1.2+ (TLS 1.3 preferred); HSTS on web apps; no SSL/TLS 1.0/1.1 |
| Data at rest | AES-256 (or provider-managed equivalent) for Confidential/Restricted data; full-disk encryption on endpoints |
| Hashing of passwords | Argon2id, scrypt or bcrypt with suitable parameters |
| Signatures / asymmetric | RSA ≥ 3072, ECDSA P-256+ or Ed25519 |
| Post-quantum readiness | Keep an inventory of cryptographic use; follow NIST PQC migration guidance |

Custom or proprietary cryptographic algorithms are not allowed.

## 2. Key management
- Keys are generated and stored in a KMS or HSM ({{KMS}}). Keys are never stored in source code or tickets.
- Each key has a named owner, a defined lifetime and a rotation schedule (at least annually for data-encryption keys, unless the KMS rotates them automatically).
- Access to keys is logged and limited to least privilege.
- If compromise is suspected, revoke and rotate the key immediately and handle the event as an incident (ISMS-POL-004).
- Secrets (API keys, tokens) are kept in {{SECRETS_MANAGER}} and scanned for in code repositories.

## 3. Legal
The use, import and export of cryptography complies with applicable law (5.31).

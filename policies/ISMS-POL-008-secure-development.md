---
id: ISMS-POL-008
title: Secure Development and Change Management Policy
version: 0.1
status: Draft
owner: "{{CTO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["8.4", "8.25", "8.26", "8.27", "8.28", "8.29", "8.30", "8.31", "8.32", "8.33"]
last_reviewed: ""
next_review: ""
---

# Secure Development and Change Management Policy

## 1. Secure development life cycle (8.25)
Security is part of every phase: requirements → design → build → test → deploy → operate.

## 2. Requirements and architecture (8.26, 8.27)
- Security requirements (authentication, authorization, data protection, logging) are defined for new features that handle Confidential data.
- Threat modelling is done for new systems and significant architectural changes.
- Secure engineering principles: defence in depth, least privilege, secure defaults, zero trust.

## 3. Secure coding (8.28)
- Follow the OWASP Top 10 / ASVS guidance applicable to the stack.
- Dependencies are managed with lockfiles. Software composition analysis (SCA) and an SBOM are generated in CI.
- SAST and secret scanning run on every pull request ({{SAST_TOOL}}).

## 4. Source code access (8.4)
Repositories are accessed through SSO with MFA. Write access is role-based. The default branch is protected.

## 5. Testing (8.29, 8.33)
- Automated tests plus security tests (SAST, DAST, SCA) run in CI. Penetration testing happens annually and before major releases.
- Production personal data is **not** used in test environments, unless it is masked or anonymized and approved by the DPO.

## 6. Environments (8.31)
Development, test and production are separate (separate accounts or projects). Developers do not have standing write access to production.

## 7. Change management (8.32)
- All production changes go through a pull request with at least one independent reviewer, passing CI, and traceability to a ticket.
- Emergency changes are allowed with retrospective review within 2 working days.
- Infrastructure is managed as code where possible.

## 8. Outsourced development (8.30)
Outsourced developers follow this policy contractually. Their code is reviewed and scanned like internal code.

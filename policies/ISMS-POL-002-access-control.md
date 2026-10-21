---
id: ISMS-POL-002
title: Access Control Policy
version: 0.1
status: Draft
owner: "{{CISO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["5.15", "5.16", "5.17", "5.18", "8.2", "8.3", "8.5"]
last_reviewed: ""
next_review: ""
---

# Access Control Policy

## 1. Principles
- **Least privilege** and **need to know**: access is limited to what each role needs.
- **Deny by default**: access must be explicitly granted.
- **Segregation of duties** according to ISMS-DOC-003.

## 2. Identity management (5.16)
- Every user has one unique identity in the central identity provider ({{IDP}}). Shared accounts are not allowed, except documented service or break-glass accounts with a named owner.
- Identities are created only from an approved HR or contractor record, and disabled on the last working day (leavers) at the latest.

## 3. Access rights (5.18)
| Event | Process |
|---|---|
| Joiner | Role-based access from a template, approved by the manager |
| Mover | Access for the new role granted; old access removed within 5 working days |
| Leaver | All access revoked by the end of the last working day; immediately for terminations |
| Review | Privileged access quarterly; other access semi-annually, by asset owners |

## 4. Authentication (5.17, 8.5)
- SSO through {{IDP}} for all systems that support it.
- **MFA is required** for all remote access, email, cloud consoles, source code and admin interfaces. Use phishing-resistant MFA (FIDO2/passkeys) for privileged accounts.
- Passwords: at least 14 characters, checked against breached-password lists, stored in the approved password manager ({{PASSWORD_MANAGER}}). No forced periodic rotation unless compromise is suspected.
- Initial or reset credentials are delivered through a secure channel and must be changed at first use.

## 5. Privileged access (8.2)
- Use separate admin accounts, distinct from day-to-day accounts.
- Use just-in-time or time-bound elevation where it is supported.
- Privileged activity is logged and monitored (8.15).
- Break-glass accounts are sealed and alert when used, and are reviewed after each use.

## 6. Information access restriction (8.3)
Access to information follows its classification (ISMS-POL-003) and is enforced technically, for example with role-based access control, row-level security and storage permissions.

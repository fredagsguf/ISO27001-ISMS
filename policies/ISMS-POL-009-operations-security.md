---
id: ISMS-POL-009
title: Operations Security Policy
version: 0.1
status: Draft
owner: "{{CTO}}"
approver: "{{CISO}}"
classification: Internal
iso_clauses: []
annex_a: ["8.6", "8.7", "8.8", "8.9", "8.13", "8.15", "8.16", "8.17", "8.19", "8.20", "8.21", "8.22", "8.23"]
last_reviewed: ""
next_review: ""
---

# Operations Security Policy

## 1. Malware protection (8.7)
EDR ({{EDR_TOOL}}) is required on all endpoints and servers where supported. Email and web filtering block known malicious content (8.23).

## 2. Vulnerability management (8.8)
| Severity (CVSS / exploitability) | Remediation SLA |
|---|---|
| Critical or known-exploited (e.g. CISA KEV) | 14 days (48 h if actively exploited and internet-facing) |
| High | 30 days |
| Medium | 90 days |
| Low | Next maintenance cycle |

Systems are scanned at least weekly. Exceptions need risk acceptance (ISMS-PRC-001).

## 3. Configuration management (8.9, 8.19)
Hardened baselines (CIS Benchmarks) are defined as code. Drift is detected and corrected. Software is installed on operational systems only through approved pipelines.

## 4. Capacity (8.6)
Capacity and performance are monitored, with alerts and auto-scaling where possible.

## 5. Backup (8.13)
- Backups follow the 3-2-1 principle, with at least one **immutable or offline** copy.
- Backups are encrypted, with access restricted and separated from production credentials.
- Restore tests are run quarterly against RTO/RPO (ISMS-POL-006).

## 6. Logging and monitoring (8.15, 8.16, 8.17)
- Logged events include authentication, privileged actions, access to Confidential data, configuration changes and security alerts.
- Logs are centralized in {{SIEM}}, protected against tampering, and retained for at least {{LOG_RETENTION}} months.
- Alerts are triaged according to ISMS-POL-004.
- All systems synchronize to approved NTP sources (8.17).

## 7. Network security (8.20, 8.21, 8.22)
Networks are segmented by function and trust level: production, corporate, management and guest. Default-deny firewall rules are used, and they are reviewed at least annually. Requirements for network services from providers are agreed and monitored.

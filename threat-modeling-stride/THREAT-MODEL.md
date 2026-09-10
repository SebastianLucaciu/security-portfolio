# STRIDE Threat Model

## System Overview

This threat model analyzes a cloud-connected customer portal that allows users to:

- authenticate
- view account information
- perform account actions
- upload documents

Administrative users access a separate privileged interface.

The architecture includes:

- customer and administrator browsers
- web frontend
- authentication service
- application API
- customer database
- document storage
- administrative portal
- centralized logging / SIEM

The architecture definition is maintained in `architecture.yaml`, and the corresponding data-flow diagram is documented in `diagrams/data-flow-diagram.md`.

---

## Threat Modeling Method

The STRIDE methodology was applied to system components, data flows, and trust boundaries.

STRIDE categories:

- **S — Spoofing:** impersonating a user, administrator, or service identity
- **T — Tampering:** unauthorized modification of requests, files, records, or logs
- **R — Repudiation:** performing actions without sufficient evidence or accountability
- **I — Information Disclosure:** unauthorized exposure of sensitive information
- **D — Denial of Service:** degrading or preventing system availability
- **E — Elevation of Privilege:** gaining permissions beyond those originally granted

Each identified threat was assigned:

- affected component or data flow
- trust boundary
- threat scenario
- potential impact
- likelihood
- severity
- mitigation
- residual risk

The detailed register is available in `threat-register.csv`.

---

## Trust Boundaries

### TB1 — Internet to Application Boundary

Separates untrusted customer and administrator endpoints from publicly reachable or restricted application services.

Primary concerns include:

- stolen credentials
- forged authentication tokens
- malicious requests
- credential exposure
- request flooding
- administrator impersonation

### TB2 — Application to Data Boundary

Separates application services from customer records and document storage.

Primary concerns include:

- excessive service permissions
- unauthorized record modification
- sensitive data exposure
- malicious file handling
- storage abuse
- privilege escalation through backend service identities

### TB3 — Application to Monitoring Boundary

Separates production application services from centralized logging and monitoring infrastructure.

Primary concerns include:

- insufficient audit evidence
- log tampering or deletion
- sensitive information written to logs
- loss of forensic visibility

---

## Threat Summary

A total of **21 threats** were identified.

| STRIDE Category | Threats |
|---|---:|
| Spoofing | 3 |
| Tampering | 3 |
| Repudiation | 3 |
| Information Disclosure | 4 |
| Denial of Service | 4 |
| Elevation of Privilege | 4 |
| **Total** | **21** |

---

## Highest-Priority Threats

### TM-002 — Administrator Impersonation

**Category:** Spoofing  
**Severity:** Critical

An attacker who obtains administrator credentials or session tokens could impersonate a privileged user and perform administrative actions.

Key mitigations:

- phishing-resistant MFA
- conditional access
- short-lived privileged sessions
- privileged access monitoring

---

### TM-006 — Unauthorized Customer Record Modification

**Category:** Tampering  
**Severity:** Critical

A compromised application identity or excessive database permissions could allow unauthorized modification of customer records.

Key mitigations:

- least-privilege database permissions
- parameterized queries
- database auditing
- integrity monitoring
- service identity protection

---

### TM-009 — Log Tampering or Deletion

**Category:** Repudiation  
**Severity:** Critical

An attacker who can modify or delete security logs may conceal malicious activity and prevent reliable incident reconstruction.

Key mitigations:

- append-only or immutable log storage
- restricted delete permissions
- centralized log collection
- retention policies
- detection of logging gaps

---

### TM-011 — Customer Document Exposure

**Category:** Information Disclosure  
**Severity:** Critical

Incorrect storage permissions could expose private customer documents.

Key mitigations:

- private-by-default storage
- scoped access policies
- short-lived signed URLs
- encryption at rest
- access logging

---

### TM-018 — API Authorization Bypass

**Category:** Elevation of Privilege  
**Severity:** Critical

A normal authenticated user may gain access to privileged API functions if authorization checks are missing or inconsistent.

Key mitigations:

- centralized authorization controls
- role-based access control
- deny-by-default permissions
- authorization testing
- audit logging

---

### TM-020 — Database Privilege Escalation

**Category:** Elevation of Privilege  
**Severity:** Critical

A compromised application service identity with excessive database privileges could allow escalation from application access to unrestricted database control.

Key mitigations:

- scoped service identities
- separate read/write roles
- no administrative database permissions for application identities
- credential rotation
- database auditing

---

## Security Priorities

Based on the threat analysis, the highest-priority security controls are:

1. **Strong identity controls**
   - MFA
   - short-lived sessions and tokens
   - privileged access controls
   - robust token validation

2. **Centralized authorization**
   - role-based access control
   - deny-by-default permissions
   - authorization enforcement at the API layer

3. **Least-privilege service identities**
   - restricted database permissions
   - scoped storage access
   - separation of read/write capabilities

4. **Data protection**
   - encryption in transit and at rest
   - private-by-default storage
   - sensitive-data minimization and redaction

5. **Trusted audit logging**
   - centralized logging
   - immutable or append-only storage
   - correlation IDs
   - privileged action logging

6. **Availability controls**
   - rate limiting
   - request quotas
   - file size restrictions
   - autoscaling
   - capacity monitoring

---

## Residual Risk

The model assumes the listed mitigations are implemented correctly.

Residual risk remains because:

- valid user or administrator credentials may still be compromised
- upstream services may contain vulnerabilities
- authorization logic may contain implementation defects
- denial-of-service attacks may exceed designed capacity
- insider threats cannot be completely eliminated
- monitoring depends on reliable and complete telemetry

Security controls should therefore be continuously validated through testing, logging, monitoring, and periodic threat-model review.

---

## Artifacts

- `architecture.yaml` — architecture and data-flow source of truth
- `diagrams/data-flow-diagram.md` — Mermaid data-flow diagram
- `threat-register.csv` — detailed STRIDE threat register
- `THREAT-MODEL.md` — summarized threat analysis and mitigation priorities

# Threat Modeling with STRIDE

![STRIDE](https://img.shields.io/badge/STRIDE-Threat%20Modeling-6f42c1)
![Threat Modeling](https://img.shields.io/badge/Threat%20Modeling-Security%20Design-005571)
![Security Architecture](https://img.shields.io/badge/Security%20Architecture-Risk%20Analysis-2f855a)
![YAML](https://img.shields.io/badge/YAML-Architecture-CB171E?logo=yaml&logoColor=white)
![Mermaid](https://img.shields.io/badge/Mermaid-Data%20Flow%20Diagram-FF3670?logo=mermaid&logoColor=white)
![Threats](https://img.shields.io/badge/Threats%20Identified-21-critical)


A hands-on security architecture review using the STRIDE methodology to identify and prioritize threats in a cloud-connected customer portal.


[View Full Threat Model](THREAT-MODEL.md) •
[View Threat Register](threat-register.csv) •
[View Architecture](architecture.yaml) •
[View Data Flow Diagram](diagrams/data-flow-diagram.md)


## Project Summary

This project models a public web application containing:

- customer and administrator access
- web frontend
- authentication service
- application API
- customer database
- document storage
- administrative portal
- centralized logging / SIEM

The system was decomposed into components, data flows, and trust boundaries before applying STRIDE.

## STRIDE Analysis

The following threat categories were evaluated:

- **Spoofing**
- **Tampering**
- **Repudiation**
- **Information Disclosure**
- **Denial of Service**
- **Elevation of Privilege**

A total of **21 threats** were identified and documented.

| STRIDE Category | Threats |
|---|---:|
| Spoofing | 3 |
| Tampering | 3 |
| Repudiation | 3 |
| Information Disclosure | 4 |
| Denial of Service | 4 |
| Elevation of Privilege | 4 |
| **Total** | **21** |

## Trust Boundaries

Three primary trust boundaries were modeled:

- **TB1 — Internet to Application Boundary**
- **TB2 — Application to Data Boundary**
- **TB3 — Application to Monitoring Boundary**

Threats were mapped to specific system components, data flows, and trust boundaries rather than evaluated only at a generic application level.

## Highest-Risk Findings

Critical threats included:

- administrator impersonation
- unauthorized customer record modification
- log tampering or deletion
- customer document exposure
- API authorization bypass
- database privilege escalation

Mitigation priorities focused on:

- phishing-resistant MFA
- centralized authorization
- least-privilege service identities
- scoped database and storage permissions
- immutable audit logging
- encryption and sensitive-data minimization
- rate limiting and resource controls

## Project Artifacts

- `architecture.yaml` — system architecture and data-flow source of truth
- `diagrams/data-flow-diagram.md` — Mermaid data-flow diagram
- `threat-register.csv` — detailed 21-threat STRIDE register
- `THREAT-MODEL.md` — full threat analysis and mitigation priorities

## Skills Demonstrated

Threat Modeling • STRIDE • Security Architecture • Data Flow Analysis • Trust Boundaries • Risk Assessment • Identity & Access Management • Least Privilege • Secure Design • Security Logging • Cloud Security

# PKI / TLS Troubleshooting Lab

## Overview

This project demonstrates a structured troubleshooting process for common PKI and TLS failures in enterprise environments using OpenSSL and curl.

The lab covers certificate inspection, trust-chain validation, hostname verification, certificate expiration, incomplete chains, TLS protocol mismatches, and cipher mismatches.

## Scenario

A client application is unable to establish a trusted HTTPS connection to an internal service.

The service may be reachable over the network while TLS validation or negotiation still fails. The troubleshooting process separates connectivity problems from certificate, trust, identity, protocol, and cipher issues.

## Failure Modes Tested

- Untrusted issuing certificate authority
- Hostname mismatch
- Missing Subject Alternative Name (SAN)
- Expired certificate
- Incomplete certificate chain
- TLS protocol mismatch
- Cipher-suite mismatch

## Skills Demonstrated

- TLS and HTTPS troubleshooting
- PKI and certificate-chain analysis
- OpenSSL
- curl
- Certificate validation
- Hostname and SAN verification
- Trust-store troubleshooting
- TLS protocol and cipher analysis
- DNS and connectivity validation
- Technical documentation

## Lab Architecture

```text
Security Lab Root CA
        |
        +----------------------+
        |                      |
        v                      v
Directly Issued Server    Intermediate CA
Certificate                    |
                               v
                         Chain Server
                         Certificate
```

Local HTTPS services were tested on port `8443` using OpenSSL `s_server`.

## Troubleshooting Workflow

The lab follows a layered troubleshooting approach:

```text
Connectivity
    |
    v
Certificate Trust
    |
    v
Validity Period
    |
    v
Hostname / SAN
    |
    v
Certificate Chain
    |
    v
TLS Protocol
    |
    v
Cipher Compatibility
```

Each issue was reproduced, diagnosed, and then validated after correction.

## Tools

- OpenSSL
- curl
- macOS Terminal

## Project Contents

- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) — Step-by-step PKI/TLS troubleshooting guide
- [`evidence/`](evidence/) — Captured command output from successful and failed TLS tests
- [`certs/`](certs/) — Locally generated CA, intermediate, server certificates, CSRs, keys, and extension files

## Key Takeaway

A failed HTTPS connection does not automatically mean the server certificate is defective. TLS troubleshooting requires separating network connectivity, trust, certificate identity, validity, chain construction, protocol negotiation, and cipher compatibility.

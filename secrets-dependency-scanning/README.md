# Secrets & Dependency Scanning

[![Security Scan](https://github.com/SebastianLucaciu/security-portfolio/actions/workflows/security-scan.yml/badge.svg)](https://github.com/SebastianLucaciu/security-portfolio/actions/workflows/security-scan.yml)

## Overview

This project demonstrates how hard-coded secrets and vulnerable software dependencies can be detected and remediated before reaching production.

The lab combines local security scanning with automated CI checks using Gitleaks, pip-audit, and GitHub Actions.

## Security Issues Tested

- Hard-coded application secrets
- Organization-specific secret patterns
- Vulnerable Python dependencies
- Security findings requiring dependency upgrades

## Secret Scanning

A simulated API key was initially stored directly in source code.

Gitleaks did not detect the lab-specific credential format using its default rules, so a custom detection rule was created in `.gitleaks.toml`.

The custom rule successfully identified the exposed credential in `app/config.py`.

The secret was then removed from source code and replaced with environment-variable configuration.

A validation scan returned:

```text
no leaks found
```

## Dependency Scanning

The application initially used deliberately outdated versions of Flask and Jinja2.

`pip-audit` identified 10 known vulnerabilities across the two packages.

The dependencies were upgraded and the validation scan returned:

```text
No known vulnerabilities found
```

## Automated Security Scanning

A GitHub Actions workflow runs security checks automatically when changes are pushed or submitted through a pull request.

The pipeline performs:

- Dependency vulnerability scanning with `pip-audit`
- Secret scanning with Gitleaks
- Custom secret detection using `.gitleaks.toml`

## Skills Demonstrated

- DevSecOps
- Secret scanning
- Dependency vulnerability scanning
- Gitleaks
- pip-audit
- GitHub Actions
- CI security controls
- Environment-variable configuration
- Vulnerability remediation
- Security validation

## Project Contents

- [`SECURITY-FINDINGS.md`](SECURITY-FINDINGS.md) — Detection, remediation, and validation findings
- [`app/`](app/) — Sample application configuration and dependencies
- [`evidence/`](evidence/) — Security scan results before and after remediation
- [`security-scan.yml`](../.github/workflows/security-scan.yml) — Automated security scanning pipeline
- [`.gitleaks.toml`](.gitleaks.toml) — Custom secret detection rule

## Key Takeaway

Security scanning is most useful when it is integrated into the development workflow rather than performed only after deployment. Detecting secrets and vulnerable dependencies during development and CI helps prevent avoidable security issues from reaching production.

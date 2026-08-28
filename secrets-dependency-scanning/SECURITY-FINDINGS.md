# Security Findings

## 1. Hard-Coded Secret

### Finding

A simulated API key was stored directly in `app/config.py`.

Gitleaks initially did not detect the test credential using its default rules because the string did not match a built-in credential pattern.

A custom Gitleaks rule was added in `.gitleaks.toml` to detect the lab-specific API key format.

### Detection

The custom rule identified:

- Rule: `security-lab-api-key`
- File: `app/config.py`
- Line: 1

The captured evidence was redacted before being stored in the repository.

### Remediation

The hard-coded values were removed from source code and replaced with environment-variable lookups:

```python
import os

API_KEY = os.environ.get("SECURITY_LAB_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
```

A `.env.example` file documents the expected variables without containing real secrets.

`.env` files and the local Python virtual environment are excluded from Git through `.gitignore`.

### Validation

A second Gitleaks scan completed with:

```text
no leaks found
```

---

## 2. Vulnerable Dependencies

### Finding

The application initially used deliberately outdated dependencies:

```text
Flask==0.12.2
Jinja2==2.10
```

`pip-audit` identified 10 known vulnerabilities across the two packages.

### Remediation

The dependencies were upgraded to:

```text
Flask==3.1.3
Jinja2==3.1.6
```

### Validation

A second dependency scan returned:

```text
No known vulnerabilities found
```

---

## Key Takeaways

- Secret scanners may require organization-specific rules for custom credential formats.
- Detection evidence should not preserve exposed credentials in plaintext.
- Secrets should be removed from source code and supplied through an appropriate secrets-management mechanism or environment configuration.
- Dependency scanning should include both detection and remediation validation.
- A clean security scan after remediation provides stronger evidence than merely identifying vulnerabilities.

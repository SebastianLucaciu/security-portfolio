# Security Investigation

## Executive Summary

A simulated Linux web server, `web01`, was compromised through a successful SSH password login from the external IP address `203.0.113.77`.

Prior to the successful login, the same source generated repeated failed authentication attempts against multiple accounts, including `admin`, `root`, and `sebastian`.

After authenticating as `sebastian`, the attacker performed system reconnaissance, accessed sensitive credential material, downloaded and executed a remote script with elevated privileges, established persistence, staged application data, and exfiltrated the resulting archive to `198.51.100.42`.

The observed activity is consistent with a full host compromise involving credential access, privilege abuse, persistence, command execution, and data exfiltration.

## Initial Indicators

Key indicators included:

- Repeated SSH authentication failures from `203.0.113.77`
- Successful password authentication for `sebastian` from the same external IP
- Access to `/etc/shadow`
- Download of `/tmp/update.sh` from `198.51.100.42`
- Execution of the downloaded script using `sudo`
- Creation of persistence through `/etc/crontab`
- Execution of hidden binary `/usr/local/bin/.svc`
- Creation of `/tmp/appdata.tar.gz`
- Outbound HTTP POST containing approximately 184 KB of data to `198.51.100.42`

## Investigation Timeline

| Time | Event |
|---|---|
| 09:12:01 | SSH password attempts begin from `203.0.113.77` against invalid user `admin` |
| 09:18:23 | Source begins attempting authentication as `root` |
| 09:19:02 | Source begins attempting authentication as `sebastian` |
| 09:19:46 | Successful SSH password login as `sebastian` from `203.0.113.77` |
| 09:20:14 | System reconnaissance begins with `uname -a` |
| 09:20:26 | User context checked with `whoami` |
| 09:20:41 | Network services enumerated with `ss -tulpn` |
| 09:21:10 | `sudo` used to execute `id` as root |
| 09:21:46 | Filesystem searched for `.env` files |
| 09:22:31 | `/etc/shadow` accessed as root |
| 09:23:02 | Remote script downloaded from `198.51.100.42` |
| 09:23:11 | Downloaded script made executable |
| 09:24:18 | `/tmp/update.sh` executed as root |
| 09:24:18 | Hidden binary copied to `/usr/local/bin/.svc` |
| 09:24:19 | Persistence added to `/etc/crontab` using an `@reboot` entry |
| 09:24:29 | Hidden `.svc` binary executed |
| 09:25:06 | Application configuration and `.env` files archived to `/tmp/appdata.tar.gz` |
| 09:26:31 | Archive uploaded to `198.51.100.42` using HTTP POST |
| 09:27:44 | Attacker SSH session closed |

## Findings

### F-001 — SSH Password Attack

The external host `203.0.113.77` generated repeated failed SSH authentication attempts against several usernames before successfully authenticating as `sebastian`.

**Severity:** High

This behavior is consistent with password guessing, credential stuffing, or use of previously compromised credentials.

### F-002 — Successful External Login Following Failures

A successful password-based SSH login for `sebastian` occurred from the same IP responsible for the preceding failed attempts.

**Severity:** Critical

The close correlation between failed attempts and successful authentication strongly indicates unauthorized account access.

### F-003 — Privileged Credential Access

The compromised account used `sudo` to read `/etc/shadow`.

**Severity:** Critical

Access to `/etc/shadow` could enable offline password cracking and compromise of additional local accounts.

### F-004 — Malicious Payload Download

The attacker downloaded `update.sh` from `198.51.100.42` into `/tmp`.

**Severity:** Critical

The script originated from an external system and was downloaded shortly after unauthorized access.

### F-005 — Privileged Payload Execution

The downloaded script was executed as root through `sudo`.

**Severity:** Critical

Executing an untrusted remote script as root gave the attacker full control of the host.

### F-006 — Persistence Established

The attacker added the following persistence mechanism:

`@reboot root /usr/local/bin/.svc`

**Severity:** Critical

This causes the malicious binary to execute automatically following system reboot.

### F-007 — Sensitive Data Staging

Application configuration files and `.env` data were compressed into `/tmp/appdata.tar.gz`.

**Severity:** High

Environment files frequently contain application secrets, credentials, API keys, and connection strings.

### F-008 — Data Exfiltration

The staged archive was transmitted to `198.51.100.42` using an HTTP POST request.

**Severity:** Critical

Network telemetry showed approximately 184 KB of outbound data during this event, corroborating the process execution evidence.

## Indicators of Compromise

### IP Addresses

- `203.0.113.77` — source of unauthorized SSH activity
- `198.51.100.42` — payload hosting and exfiltration destination

### Files

- `/tmp/update.sh`
- `/usr/local/bin/.svc`
- `/tmp/appdata.tar.gz`

### Persistence

- `/etc/crontab`
- `@reboot root /usr/local/bin/.svc`

### Accounts

- `sebastian`

## Root Cause / Attack Path

The likely attack path was:

1. External attacker targeted the SSH service.
2. Multiple usernames were tested using password authentication.
3. The attacker successfully authenticated as `sebastian`.
4. The compromised account had sufficient `sudo` permissions to execute privileged commands.
5. The attacker performed reconnaissance and searched for sensitive data.
6. `/etc/shadow` was accessed.
7. A remote payload was downloaded and executed as root.
8. Persistence was established through `cron`.
9. Sensitive application data was archived.
10. The archive was exfiltrated to an attacker-controlled system.

## Recommended Remediation

- Disable or restrict password-based SSH authentication.
- Require SSH key authentication and MFA where supported.
- Restrict SSH access using firewall rules or VPN-based administrative access.
- Reset credentials associated with the compromised account.
- Rotate any application secrets stored in `.env` or configuration files.
- Review and restrict `sudo` permissions using least privilege.
- Remove malicious persistence mechanisms and files.
- Isolate and rebuild the compromised host from a trusted image.
- Review adjacent systems for reuse of compromised credentials or secrets.
- Implement centralized authentication and process logging.
- Alert on repeated failed SSH authentication followed by successful login.
- Alert on access to `/etc/shadow`.
- Alert on suspicious execution from `/tmp`.
- Alert on modifications to `/etc/crontab`.
- Monitor unusual outbound connections and large HTTP POST requests.

# Security Log Analysis

![Linux](https://img.shields.io/badge/Linux-Security-blue?logo=linux)
![Python](https://img.shields.io/badge/Python-Log%20Analysis-blue?logo=python)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-red)
![Incident Response](https://img.shields.io/badge/Incident-Response-orange)
![Log Analysis](https://img.shields.io/badge/Security-Log%20Analysis-green)

A simulated security investigation of a compromised Linux web server using authentication, process execution, and network telemetry.

The project demonstrates how multiple log sources can be correlated to reconstruct attacker activity, identify indicators of compromise, document findings, and develop practical detection opportunities.


<details>
<summary><strong>Project Highlights</strong></summary>

<br>

- Correlates authentication, process, and network logs
- Reconstructs a complete Linux compromise timeline
- Identifies credential abuse, persistence, and exfiltration
- Maps observed behavior to MITRE ATT&CK
- Includes practical detection engineering ideas
- Includes a Python-based automated triage script

</details>

## Scenario

A Linux web server begins generating suspicious authentication and system activity.

The investigation identifies:

- Repeated SSH authentication failures
- Successful external login using a valid account
- System reconnaissance
- Privilege abuse
- Access to sensitive credential material
- Remote payload download
- Persistence
- Sensitive data staging
- Data exfiltration

## Investigation Summary

The simulated attacker targeted the server's SSH service from `203.0.113.77`.

After repeated failed authentication attempts against several accounts, the attacker successfully authenticated as `sebastian`.

The compromised account was then used to:

1. Enumerate system and network information
2. Search for application secrets
3. Access `/etc/shadow`
4. Download a remote script
5. Execute the script with root privileges
6. Establish persistence through `cron`
7. Archive application configuration and environment data
8. Exfiltrate the archive to `198.51.100.42`


## Security & Business Impact

The compromise represents more than an isolated unauthorized login. Once the attacker gained access to the server, the activity created several high-impact risks to the wider environment.

### Credential and Secret Exposure

Access to `/etc/shadow` exposed local password hashes, while discovery and collection of application `.env` and configuration files created the possibility that additional credentials, API keys, database connection strings, or service secrets were compromised.

This means remediation cannot be limited to resetting the `sebastian` account. Any credentials or secrets stored on the host must be treated as potentially exposed and rotated.

### Full Host Compromise

The attacker executed a downloaded payload with root privileges.

Root-level execution means the integrity of the server can no longer be trusted. An attacker with this access can modify system files, disable security controls, create users, alter logs, install additional tooling, and conceal malicious activity.

The appropriate recovery action would be to isolate and rebuild the host from a trusted image rather than relying only on removal of observed malicious files.

### Persistent Unauthorized Access

The attacker created an `@reboot` cron entry that launches `/usr/local/bin/.svc`.

This persistence mechanism allows malicious code to survive a reboot and provides continued access even after the original SSH session ends.

### Sensitive Data Loss

Application configuration and environment data were collected into `/tmp/appdata.tar.gz` and transferred to an external host.

This creates a confirmed confidentiality impact and may expose application secrets or infrastructure credentials that could be reused against other systems.

### Potential Lateral Movement

If passwords, SSH credentials, service accounts, API tokens, or application secrets were reused elsewhere, the compromise could extend beyond `web01`.

The incident therefore requires investigation of adjacent systems, authentication logs, reused credentials, and any services accessible using secrets stored on the compromised server.

### Operational Impact

Because both privileged access and persistence were achieved, the server must be considered untrusted.

Likely incident-response actions include:

- Immediate host isolation
- Credential and secret rotation
- Blocking identified malicious infrastructure
- Investigation of related systems and accounts
- Restoration or rebuild from a trusted image
- Validation of application and data integrity
- Increased monitoring for recurrence

### Overall Risk

**Overall Severity: Critical**

The combination of valid-account compromise, root-level execution, credential access, persistence, and confirmed data exfiltration represents a complete system compromise with potential impact beyond the affected host.

## Log Sources

### Authentication Logs

`logs/auth.log`

Contains:

- SSH login attempts
- Successful authentication
- `sudo` activity
- Session activity

### Process Execution Logs

`logs/process.log`

Contains:

- Shell execution
- Reconnaissance commands
- File discovery
- Payload download
- Persistence creation
- Data staging
- Exfiltration commands

### Network Logs

`logs/network.log`

Contains:

- Inbound SSH activity
- Outbound payload retrieval
- External communication
- Data transfer telemetry

## Key Findings

| Finding | Severity |
|---|---|
| SSH password attack | High |
| Successful unauthorized login | Critical |
| Access to `/etc/shadow` | Critical |
| Remote payload download | Critical |
| Root-level payload execution | Critical |
| Cron persistence | Critical |
| Sensitive data staging | High |
| Data exfiltration | Critical |

Full findings are documented in:

[View Full Investigation](analysis/investigation.md)


<details>
<summary><strong>Indicators of Compromise</strong></summary>

<br>

### IP Addresses

- `203.0.113.77` — source of malicious SSH activity
- `198.51.100.42` — payload hosting and exfiltration destination

### Files

- `/tmp/update.sh`
- `/usr/local/bin/.svc`
- `/tmp/appdata.tar.gz`

### Persistence

- `/etc/crontab`
- `@reboot root /usr/local/bin/.svc`

### Compromised Account

- `sebastian`

</details>

## MITRE ATT&CK Mapping

Observed attacker behavior was mapped to MITRE ATT&CK techniques including:

- Brute Force
- Valid Accounts
- System Information Discovery
- File and Directory Discovery
- OS Credential Dumping
- Ingress Tool Transfer
- Unix Shell
- Persistence
- Archive Collected Data
- Exfiltration

See:

[View MITRE ATT&CK Mapping](analysis/mitre-attack-mapping.md)

## Detection Engineering

The project includes practical detection opportunities for:

- Repeated SSH failures followed by success
- Access to `/etc/shadow`
- Execution from `/tmp`
- Cron-based persistence
- Suspicious outbound HTTP transfers

See:

[View Detection Opportunities](detections/linux-detections.md)


<details>
<summary><strong>Detection Opportunities</strong></summary>

<br>

Potential detection logic includes:

- Multiple SSH failures followed by a successful login from the same source
- Access to `/etc/shadow`
- Execution of scripts or binaries from `/tmp`
- Unexpected changes to `/etc/crontab`
- New or unusual outbound connections from the server
- Large HTTP POST requests to external destinations

</details>

## Automated Log Triage

A Python triage script scans the simulated logs for security-relevant patterns.

Run:

```bash
python3 analysis/log_triage.py

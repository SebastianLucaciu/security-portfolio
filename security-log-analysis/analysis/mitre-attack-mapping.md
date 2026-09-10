# MITRE ATT&CK Mapping

This document maps the observed attacker behavior in the simulated compromise to relevant MITRE ATT&CK techniques.

| Technique | Name | Evidence | Observed Behavior |
|---|---|---|---|
| T1110 | Brute Force | Repeated failed SSH authentication attempts from `203.0.113.77` | Multiple usernames were targeted before a successful login |
| T1078 | Valid Accounts | Successful SSH login as `sebastian` | The attacker gained access using a valid user account |
| T1082 | System Information Discovery | `uname -a` | The attacker collected host and operating system information |
| T1033 | System Owner/User Discovery | `whoami` | The attacker confirmed the active user context |
| T1049 | System Network Connections Discovery | `ss -tulpn` | The attacker enumerated listening services and network connections |
| T1083 | File and Directory Discovery | `find /var/www /home -type f -name '*.env'` | The attacker searched for application configuration and secrets |
| T1003 | OS Credential Dumping | `cat /etc/shadow` | Password hash material was accessed |
| T1105 | Ingress Tool Transfer | `curl` download of `update.sh` | A remote script was transferred to the compromised host |
| T1059.004 | Unix Shell | `bash /tmp/update.sh` | The attacker executed commands through the Unix shell |
| T1547 | Boot or Logon Autostart Execution | `@reboot root /usr/local/bin/.svc` | Persistence was configured to execute after reboot |
| T1560 | Archive Collected Data | `tar czf /tmp/appdata.tar.gz ...` | Sensitive application data was compressed before transfer |
| T1041 | Exfiltration Over C2 Channel | HTTP POST to `198.51.100.42` | Staged data was transferred to an external system |

## Attack Progression

1. Credential attacks targeted the exposed SSH service.
2. A valid user account was compromised.
3. Host and service reconnaissance was performed.
4. Sensitive files and credential material were accessed.
5. A remote payload was downloaded.
6. The payload was executed with root privileges.
7. Persistence was established.
8. Application data was staged into an archive.
9. The archive was exfiltrated to an external destination.

## Defensive Value

Mapping observed activity to MITRE ATT&CK provides a standardized way to describe attacker behavior and helps connect investigation findings to:

- Detection engineering
- Threat hunting
- Incident response
- Security monitoring
- Control validation

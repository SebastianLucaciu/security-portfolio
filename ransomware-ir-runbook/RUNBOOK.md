# Incident Response Runbook: Ransomware via Phishing-Delivered Payload

**Framework:** This runbook uses a practical incident-response workflow — Preparation / Detection & Analysis / Containment-Eradication-Recovery / Post-Incident Activity — while incorporating current guidance from NIST SP 800-61r3 and the NIST Cybersecurity Framework 2.0.

**Scope:** Single-host ransomware infection with potential lateral movement via SMB

**Audience:** SOC Analyst (Tier 1/2), Incident Commander, IT Operations

---

## 1. Scenario Overview

At 02:14 AM, the SIEM generates a high-severity alert for abnormal SMB write activity originating from host `WKS-FIN-0472`, a finance department laptop. The alert pattern indicates rapid sequential file writes with renamed extensions across a mapped network drive (`\\FS01\Finance$`).

Initial triage of the endpoint's EDR telemetry shows a phishing email was opened by the logged-in user (`j.martinez`) at 01:34 AM, approximately 40 minutes prior to the alert. The email contained a malicious macro-enabled attachment disguised as an invoice (`Invoice_88213.docm`). Process telemetry shows `winword.exe` spawning `powershell.exe` with an encoded command shortly after the attachment was opened.

**Initial severity classification:** Critical — active encryption is confirmed on business-critical shared data, with potential lateral spread.

---

## 2. Preparation (Pre-Incident Baseline)

This section documents the controls and readiness that should already exist before an incident of this type occurs.

### 2.1 Asset & Network Awareness

- Maintain an up-to-date asset inventory including hostname, owner, department, and criticality tier
- Maintain network segmentation between user workstations and critical file servers using VLANs and access-control rules
- Keep a current network diagram showing key systems, trust boundaries, and isolation points

### 2.2 Backup Readiness

- Maintain multiple recoverable copies of critical data, including at least one offline or immutable copy
- Test backup restoration on a defined schedule rather than assuming backups are usable
- Keep backup systems isolated from ordinary production credentials where practical

### 2.3 Security Tooling Readiness

- Deploy EDR to endpoints with network-isolation capability
- Configure SIEM detections for ransomware-related behavior such as mass file changes, suspicious PowerShell execution, and shadow-copy deletion
- Ensure relevant endpoint, authentication, network, and email logs are retained long enough to support investigation
- Maintain approved forensic or evidence-collection tools for responders

### 2.4 Incident Response Roles

| Role | Responsibility |
|---|---|
| Incident Commander | Coordinates the response and owns major incident decisions |
| Technical Lead | Leads technical containment, investigation, eradication, and recovery |
| Communications Lead | Coordinates internal and external stakeholder communication |
| Scribe | Maintains the incident timeline, decisions, and actions taken |

### 2.5 Escalation & Communication Readiness

- Define when incidents must be escalated to security leadership, legal, compliance, or executive management
- Maintain current contact information for critical internal teams and third parties
- Define communication channels that remain usable if normal systems are affected
- Document any required cyber-insurance, regulatory, or law-enforcement notification procedures

---

## 3. Detection & Analysis

### 3.1 Initial Indicators

- SIEM alert: abnormal SMB write volume and rapid file modification activity originating from a single workstation
- EDR alert: suspicious process ancestry showing `winword.exe` spawning `powershell.exe` with an encoded command
- User-reported symptom, if available: files renamed unexpectedly, inaccessible documents, or a ransom note appearing

### 3.2 Immediate Isolation Trigger

If active encryption is confirmed, containment takes priority over completing the full triage sequence.

Immediately isolate the affected host and continue investigation in parallel if any of the following are observed:

- File modification or rename activity is actively increasing in real time
- A ransom note has appeared on the endpoint or affected share
- Shadow-copy deletion activity is observed
- Business-critical shared data is actively being encrypted

If encryption has not yet been confirmed, continue through the triage checklist below before determining the appropriate containment scope.

### 3.3 Triage Checklist

- [ ] Confirm the alert is a true positive by reviewing the EDR process tree and related telemetry
- [ ] Identify the affected host and currently logged-in user
- [ ] Determine whether similar activity is occurring on additional endpoints
- [ ] Review authentication activity for unusual logons, new administrative sessions, or signs of credential misuse
- [ ] Check for lateral movement indicators such as SMB connections, PsExec, WMI, RDP, or remote service creation
- [ ] Identify which shared drives, folders, or systems have been accessed or modified
- [ ] Determine the sensitivity and business impact of affected data
- [ ] Review PowerShell activity and command-line telemetry associated with the suspicious process chain
- [ ] Check for shadow-copy deletion or other anti-recovery behavior
- [ ] Review available network telemetry for suspicious outbound connections or possible command-and-control activity

### 3.4 Severity Classification

| Level | Criteria |
|---|---|
| Low | Activity is isolated to one non-critical host, no shared-data impact is confirmed, and automated controls have already contained the event |
| Medium | One host is confirmed affected and there is limited impact to non-sensitive shared data, with no evidence of lateral movement |
| High | Multiple hosts are affected, lateral movement is confirmed, sensitive data is involved, or business operations are materially disrupted |
| Critical | Domain controllers or core server infrastructure are affected, organization-wide spread is confirmed, or active encryption is impacting business-critical shared data |

**This scenario: Critical**

The incident is classified as Critical because active encryption is affecting a business-critical finance share. Although only one source endpoint is currently confirmed, the potential for lateral movement and broader business impact requires immediate high-priority response.

### 3.5 Evidence Preservation vs. Business Impact

Evidence preservation is important, but it must not delay actions needed to stop active business impact.

- Avoid powering off the affected host if network isolation is sufficient, because shutting down destroys volatile memory that may contain useful forensic artifacts
- Use EDR network isolation, switch-port shutdown, or another network-level containment method first where possible
- Capture volatile memory if approved tooling is available and doing so will not delay containment
- Preserve relevant logs before they roll over, including EDR telemetry, Windows Event Logs, authentication logs, firewall/network logs, and email-gateway records
- Record exact timestamps for major response actions, including detection, isolation, account restrictions, evidence collection, eradication, and recovery
- If active encryption cannot be stopped quickly through network isolation, prioritize stopping the damage even if some volatile evidence may be lost

---

## 4. Containment, Eradication & Recovery

### 4.1 Short-Term Containment

The immediate goal is to stop further damage and prevent the incident from spreading while preserving enough evidence to continue the investigation.

- Isolate the affected endpoint from the network using the EDR containment function where available
- If EDR isolation is unavailable or ineffective, isolate the host through switch-port shutdown, VLAN quarantine, or physical disconnection
- Restrict or disable the affected user account if credential compromise is suspected, confirmed, or required by containment policy
- Block confirmed malicious command-and-control IP addresses or domains at relevant security controls
- Coordinate with the file-server owner to temporarily restrict write access to affected shares if encryption is still occurring
- Notify the Incident Commander once immediate containment actions are complete and document all actions with timestamps

### 4.2 Long-Term Containment

Once immediate damage has been stopped, apply broader containment measures to reduce the chance of continued attacker access or reinfection.

- Rotate credentials for the affected user if compromise is confirmed or reasonably suspected
- Review privileged or service accounts that were used from the affected host and rotate them where exposure cannot be ruled out
- Remediate the control weakness that allowed the malicious document to execute, such as blocking macros from internet-sourced Office documents through Group Policy
- Expand blocking to additional validated indicators of compromise associated with the incident, such as malicious IP addresses, domains, hashes, or URLs
- Review firewall, proxy, endpoint, and email controls for additional opportunities to prevent recurrence
- Continue monitoring related hosts and accounts while the incident remains active

### 4.3 Eradication

After containment is stable, remove the threat from the environment and eliminate persistence or other artifacts that could allow the attacker to regain access.

- Rebuild the compromised workstation from a known-good image rather than attempting to clean the ransomware infection in place
- Scan systems that had network connectivity or trust relationships with the affected host for evidence of lateral movement or persistence
- Review scheduled tasks, services, registry run keys, startup locations, and other common persistence mechanisms
- Remove the phishing email from any additional mailboxes that received the same message, using sender, subject, attachment name, URL, or file hash as search indicators
- Verify that malicious files, scripts, or payloads identified during the investigation are no longer present in the environment
- Confirm that any compromised or exposed credentials have been reset and that unauthorized sessions or tokens have been revoked
- Validate that the control weakness used in the initial compromise has been remediated before recovery begins

### 4.4 Recovery

Once eradication is complete and confidence in the environment has been restored, return affected systems and data to normal operation in a controlled manner.

- Restore affected shared-drive data from the most recent known-good backup that predates the compromise
- Rebuild the affected workstation from a trusted image and apply current security patches before reconnecting it to the production network
- Validate restored data for integrity and expected accessibility before normal user access resumes
- Confirm endpoint protection, logging, monitoring, and required security controls are active on rebuilt systems
- Reconnect systems gradually rather than restoring everything at once, allowing monitoring for unexpected behavior
- Maintain heightened monitoring for a defined period after recovery, such as 72 hours based on organizational policy and risk
- Confirm with system owners that business functionality has been restored before formally closing the recovery phase

---

## 5. Post-Incident Activity

### 5.1 Root Cause Analysis

After recovery, determine how the incident occurred and which control failures allowed it to succeed.

- Determine how the phishing message bypassed email filtering
- Review whether macros from internet-sourced Office documents were blocked by policy or merely discouraged
- Identify whether the malicious payload exploited a software vulnerability, a configuration weakness, or user execution
- Review whether any credentials were stolen or misused during the incident
- If credential misuse occurred, evaluate whether MFA, Conditional Access, or other identity controls could have reduced the impact
- Document the confirmed root cause separately from assumptions or contributing factors

### 5.2 Lessons Learned

Hold a lessons-learned review after the incident is stabilized and recovery is complete.

Use the meeting to document what worked well, what failed or caused delays, and which improvements must be assigned to specific owners.

| What Worked | What Didn't | Action Item | Owner | Due Date |
|---|---|---|---|---|
| EDR isolation stopped further endpoint-driven SMB activity quickly | Macro execution controls were not enforced | Enforce blocking of internet-sourced Office macros | IT Operations | [date] |
| Backup restoration succeeded without confirmed data loss | Detection occurred after encryption had already begun | Tune SIEM and EDR detections for earlier suspicious process and file activity | SOC Lead | [date] |
| Cross-team escalation supported rapid file-share containment | Initial incident scope was not immediately clear | Improve asset ownership and network visibility documentation | Security Operations | [date] |

Track all agreed remediation items until completion rather than treating the lessons-learned meeting as the final step.

### 5.3 Metrics to Report

Track response metrics to evaluate incident-handling performance and identify areas for improvement.

- **Time to Detect (TTD):** time from initial compromise to the first validated security alert
- **Time to Contain (TTC):** time from validated alert to successful containment of the affected host or activity
- **Time to Recover (TTR):** time from containment to restoration of normal business operation
- **Affected Scope:** number of hosts, user accounts, systems, and data repositories involved
- **Business Impact:** operational disruption, affected business processes, and confirmed data impact
- **Control Effectiveness:** which preventive, detective, and recovery controls worked as expected and which failed or required improvement

### 5.4 Policy & Control Updates

Use confirmed findings from the incident to strengthen preventive, detective, and recovery controls.

- Enforce blocking of macros from internet-sourced Office documents through Group Policy or equivalent endpoint controls
- Review email security controls and tune filtering for malicious attachments, links, and known phishing patterns
- Require MFA for sensitive or high-risk user groups and review whether broader deployment is appropriate
- Add or tune SIEM and EDR detections for suspicious Office-to-PowerShell execution, mass file changes, and shadow-copy deletion
- Review access permissions to business-critical file shares and apply least-privilege where excessive access is identified
- Improve network segmentation where workstation-to-server access is broader than required
- Validate backup isolation, restoration procedures, and recovery testing based on lessons from the incident
- Update security awareness training using the confirmed attack pattern and lessons learned from the incident

---

## Appendix: Quick-Reference Decision Flow

```text
Alert Received
      |
      v
Confirm True Positive?
   |          |
  No         Yes
   |          |
Document      v
and Close   Active Encryption Confirmed?
              |          |
             Yes         No
              |          |
              v          v
       Isolate Host   Complete Triage
       Immediately    and Scope Incident
              |          |
              |__________|
                  |
                  v
     Restrict Account if Credential
      Compromise is Suspected/Confirmed
                  |
                  v
        Preserve Relevant Evidence
                  |
                  v
            Eradicate Threat
                  |
                  v
       Restore from Clean Backup
                  |
                  v
        Validate and Reconnect
                  |
                  v
        Heightened Monitoring
                  |
                  v
      Post-Incident Review

```

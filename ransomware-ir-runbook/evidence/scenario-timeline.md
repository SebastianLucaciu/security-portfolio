# Scenario Timeline

This timeline summarizes the simulated ransomware incident used in this project.

| Time | Event | Evidence Source | Significance |
|---|---|---|---|
| 01:34 | User opens `Invoice_88213.docm` | Email gateway / EDR | Initial phishing-delivered execution event |
| 01:35 | `winword.exe` spawns `powershell.exe` with an encoded command | EDR process telemetry | Strong indicator of suspicious document-driven execution |
| 01:36 | PowerShell launches the malicious payload | EDR / command-line telemetry | Confirms endpoint compromise |
| 02:10 | Rapid SMB write and file-rename activity begins against `\\FS01\Finance$` | Network / file-server telemetry | Indicates ransomware encryption activity affecting shared data |
| 02:14 | SIEM generates a high-severity alert | SIEM | First validated detection of active ransomware behavior |
| 02:16 | EDR network isolation initiated on `WKS-FIN-0472` | EDR action log | Stops further endpoint-driven network activity |
| 02:18 | Triage begins across authentication, SMB, endpoint, and network telemetry | SOC investigation notes | Determines scope and checks for lateral movement |
| 02:25 | File-share write access restricted while scope is confirmed | File-server / admin logs | Protects business-critical data from further modification |
| 02:40 | No additional infected hosts confirmed at this stage | SIEM / EDR / authentication review | Supports initial containment assessment |

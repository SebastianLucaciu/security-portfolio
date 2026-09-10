# Attack Flow

```mermaid
flowchart LR
    A[External Attacker<br>203.0.113.77]
    B[SSH Password Attempts]
    C[Successful Login<br>sebastian]
    D[System Reconnaissance]
    E[Privilege Abuse<br>sudo / root]
    F[Credential Access<br>/etc/shadow]
    G[Payload Download<br>update.sh]
    H[Root Execution]
    I[Persistence<br>@reboot cron]
    J[Data Staging<br>appdata.tar.gz]
    K[Exfiltration<br>198.51.100.42]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
    J --> K
```

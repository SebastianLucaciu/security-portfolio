# Data Flow Diagram

```mermaid
flowchart LR

    subgraph Internet
        U[Customer Browser]
        A[Administrator Browser]
    end

    subgraph Application_Zone[Application Zone]
        W[Web Frontend]
        AUTH[Authentication Service]
        API[Application API]
        ADMIN[Admin Portal]
    end

    subgraph Data_Zone[Data Zone]
        DB[(Customer Database)]
        OBJ[(Document Storage)]
    end

    subgraph Monitoring_Zone[Monitoring Zone]
        SIEM[Central Logging / SIEM]
    end

    U -->|DF1: HTTPS - session cookies, requests, uploads| W
    U -->|DF2: HTTPS - credentials, tokens| AUTH

    W -->|DF3: HTTPS - authenticated API requests| API

    API -->|DF4: TLS - customer account data| DB
    API -->|DF5: HTTPS - customer documents| OBJ

    A -->|DF6: HTTPS - administrative requests| ADMIN
    ADMIN -->|DF7: HTTPS - privileged API requests| API

    W -->|DF8: TLS - application/security logs| SIEM
    API -->|DF9: TLS - API/authentication/audit logs| SIEM
```

## Trust Boundaries

- **TB1 — Internet to Application Boundary**
  - separates customer/admin browsers from public and restricted application services

- **TB2 — Application to Data Boundary**
  - separates application services from customer data and document storage

- **TB3 — Application to Monitoring Boundary**
  - separates production application services from centralized logging and SIEM infrastructure

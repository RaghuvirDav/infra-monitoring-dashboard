## System Architecture

```mermaid
flowchart LR
    subgraph Infra[Infrastructure Targets]
        S1[Servers]
        A1[APIs]
        MS1[Microservices]
        C1[Containers]
    end

    Infra -->|metrics & health| BE[FastAPI Backend]

    subgraph BEG[Backend Responsibilities]
        M1[System Metrics\n(psutil)]
        M2[Service Health Checks\n(httpx)]
        M3[Alert Engine]
        M4[Prometheus /metrics\n(prometheus-client)]
    end

    BE --> M1
    BE --> M2
    BE --> M3
    BE --> M4

    M4 --> P[Prometheus]
    BE --> UI[Dashboard UI]

    M3 --> AL[Alerts\n(email/Slack/logs later)]
    UI -->|REST JSON| BE
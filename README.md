# Infra Monitoring Dashboard

A lightweight **infrastructure monitoring and observability platform** built with **FastAPI**, **Prometheus**, and a custom **dashboard UI**.

The system monitors:

- **Servers**: CPU, memory, disk, (optionally network)
- **APIs & Microservices**: health checks, latency, error status
- **Service Topology**: dependency graph between services
- **Alerts**: basic threshold-based alerts for critical signals

Unlike a pure Prometheus + Grafana setup, this project is a **code-first monitoring platform** where you fully control the backend logic, APIs, and UI.

---

## ✨ Features

- **System Metrics**
  - CPU, memory, disk usage (via `psutil`)
  - Exposed as JSON (`/metrics/system`) and Prometheus metrics (`/metrics`)

- **Service / API Health Monitoring**
  - Periodic HTTP checks to configured services (e.g. `/health` endpoints)
  - Captures latency and health status per service
  - Exposed via `/metrics/services` and `/services/status`

- **Alerting Engine (v1)**
  - CPU / memory / disk thresholds (e.g. > 90%)
  - Service health + latency alerts (e.g. status ≠ 200 or latency > 2s)
  - In-memory alert store exposed at `/alerts`
  - Designed for future pluggable notifiers (email, Slack, etc.)

- **Dashboard UI**
  - Simple HTML/JS dashboard (React-ready structure)
  - Widgets for:
    - System metrics
    - Service health and latency
    - Active alerts
    - Service topology (text-based to start; graph-ready later)

- **Prometheus Integration**
  - FastAPI backend exposes `/metrics` in Prometheus format
  - Prometheus server scrapes the backend on a configurable interval

- **Dockerized Stack**
  - `docker-compose` stack:
    - `backend` – FastAPI API
    - `prometheus` – metrics store
    - `dashboard` – UI (static or React-based)

---

## 🏗️ Architecture

### High-Level Flow

```text
[Servers / APIs / Services / Containers]
               |
        Metrics & Health Checks
               |
         [FastAPI Backend]
  - /metrics/system      (system metrics JSON)
  - /metrics/services    (service metrics JSON)
  - /services/status     (service health snapshot)
  - /services/graph      (service topology)
  - /alerts              (current alerts)
  - /metrics             (Prometheus scrape target)
               |
               +--> [Prometheus]        (scrapes /metrics)
               |
               +--> [Dashboard UI]      (polls JSON endpoints)
               |
               +--> [Alerting]          (email/Slack/logs later)
```

## Container / DevOps View

* backend (FastAPI)

  * Python 3.x
  * Exposes 8000
  * Implements:
  * metrics collection
  * health checks
  * alerts engine
  * Prometheus /metrics endpoint

* prometheus

  * Scrapes backend:8000/metrics
  * Stores metrics for graphing / querying

* dashboard

  * HTML/JS or React-based dashboard
  * Exposes 3000 (when using a frontend dev server) or 80 via nginx


## 📁 Project Structure
```text
    infra-monitoring-dashboard
├── backend
│   ├── app
│   │   ├── main.py          # FastAPI app & routes
│   │   ├── metrics.py       # System metrics + Prometheus gauges
│   │   ├── services.py      # Service/API health checks & topology
│   │   ├── alerts.py        # Alert evaluation & in-memory storage
│   │   └── models.py        # Pydantic models (metrics, alerts, graph)
│   └── requirements.txt
│
├── frontend
│   └── dashboard            # Dashboard UI (HTML/JS or React)
│       └── index.html       # Simple starter dashboard
│
├── exporters
│   └── system_metrics.py    # (optional) custom exporters
│
├── docker
│   ├── docker-compose.yml   # Backend + Prometheus + dashboard
│   └── prometheus.yml       # Prometheus scrape configuration
│
├── docs
│   └── architecture.md      # Architecture diagrams & notes
│
└── README.md
```
## 🧰 Tech Stack

* Backend

  * Python
  * FastAPI
  * Uvicorn
  * psutil
  * httpx
  * prometheus-client
  * Pydantic
* Metrics / Observability

  * Prometheus (scrapes /metrics)
* Frontend

  * Simple HTML/JS dashboard (upgradeable to React, Vite, etc.)
* Infrastructure

  * Docker
  * Docker Compose
* Optional (future)

  * Kubernetes
  * AWS / cloud deployment
  * Slack / email integration

## 🚀 Getting Started (Local Dev)

1. Clone & Setup
```
git clone <your-repo-url> infra-monitoring-dashboard

cd infra-monitoring-dashboard
```
2. Backend (FastAPI) – Local

    Create and activate a virtual environment (recommended):
    ```
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows
    pip install -r requirements.txt
   ```
    Run the backend:

    ```
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    Now test:

    http://localhost:8000/metrics/system – system metrics JSON
    http://localhost:8000/metrics/services – service health & latency
    http://localhost:8000/alerts – active alerts
    http://localhost:8000/services/graph – service topology
    http://localhost:8000/metrics – Prometheus metrics

3. Dashboard (Simple HTML)

    Starter version:
    
    * Open frontend/dashboard/index.html directly in your browser or
    * Serve it via a simple static server, e.g.:

        ```
        cd frontend/dashboard
        python -m http.server 3000
        ```

    Then visit:

    * http://localhost:3000
   
    The dashboard uses http://localhost:8000 as the API base.

## 🐳 Running with Docker Compose

```
Make sure Docker is installed and running.
```

From the docker directory:

```
cd docker
docker-compose up --build
```
* Services:
  * backend – http://localhost:8000
  * prometheus – http://localhost:9090
  * dashboard – usually http://localhost:3000 or http://localhost (depending on your frontend image)
  
Prometheus scrapes backend:8000/metrics as configured in prometheus.yml.

## 📡 API Overview

All endpoints are served by the FastAPI backend.

### System Metrics
* GET /metrics/system
  * Returns: current CPU, memory, disk usage.

```json
{
  "cpu_percent": 12.5,
  "memory_percent": 43.2,
  "disk_percent": 67.8
}
```


### Service Metrics

* GET /metrics/services

  * Returns: list of monitored services with their latest health & latency.
```json
[
  {
    "name": "user-api",
    "url": "http://user-api.local/health",
    "healthy": true,
    "latency_ms": 123.4,
    "last_error": null
  }
]
```
* GET /services/status
  * Same data shape as /metrics/services, intended as a quick status snapshot.

### Alerts

GET /alerts
Returns: list of active / historical alerts.
```json
[
  {
    "id": "uuid-...",
    "level": "warning",
    "message": "High CPU usage: 95.1%",
    "source": "system",
    "active": true
  }
]
```

### Service Topology Graph

* GET /services/graph
  * Returns: simple node/edge graph describing service dependencies.

```json
{
  "nodes": [
    { "id": "api-gateway", "label": "API Gateway" },
    { "id": "user-api", "label": "User API" },
    { "id": "auth-service", "label": "Auth Service" },
    { "id": "database", "label": "Database" }
  ],
  "edges": [
    { "from_id": "api-gateway", "to_id": "user-api" },
    { "from_id": "user-api", "to_id": "auth-service" },
    { "from_id": "auth-service", "to_id": "database" }
  ]
}
```
This is designed to feed into a topology graph on the dashboard.

### Prometheus Metrics

GET /metrics
Returns: Prometheus-compatible metrics (e.g. system_cpu_percent, system_memory_percent, system_disk_percent, plus any future custom metrics).



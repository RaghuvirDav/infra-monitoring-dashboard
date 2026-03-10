from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from .metrics import collect_system_metrics, prometheus_metrics_response
from .services import get_all_service_statuses
from .alerts import evaluate_system_alerts, evaluate_service_alerts, list_alerts
from .models import SystemMetrics, ServiceStatus, Alert
from .models import ServiceGraph
from .services import get_all_service_statuses, get_service_graph

app = FastAPI(title="Infra Monitoring Dashboard API")

# Allow your dashboard (and local dev) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/metrics/system", response_model=SystemMetrics)
def get_system_metrics():
    metrics = collect_system_metrics()
    evaluate_system_alerts(metrics)  # side-effect: may create alerts
    return metrics


@app.get("/metrics/services", response_model=list[ServiceStatus])
async def get_service_metrics():
    statuses = await get_all_service_statuses()
    evaluate_service_alerts(statuses)
    return statuses


@app.get("/services/status", response_model=list[ServiceStatus])
async def services_status():
    return await get_all_service_statuses()


@app.get("/alerts", response_model=list[Alert])
def get_alerts():
    return list_alerts()


@app.get("/metrics")
def prometheus_metrics():
    content_type, data = prometheus_metrics_response()
    return Response(content=data, media_type=content_type)


@app.get("/services/graph", response_model=ServiceGraph)
def service_graph():
    return get_service_graph()

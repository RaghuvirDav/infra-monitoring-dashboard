import json
import time
from pathlib import Path
from typing import Dict, List

import httpx

from .models import ServiceStatus, ServiceGraph, ServiceNode, ServiceEdge

CONFIG_PATH = Path(__file__).resolve().parent / "services.json"


def load_services_from_config() -> Dict[str, str]:
    if not CONFIG_PATH.exists():
        return {}
    data = json.loads(CONFIG_PATH.read_text())
    services: Dict[str, str] = {}
    for svc in data.get("services", []):
        services[svc["name"]] = svc["url"]
    return services


MONITORED_SERVICES: Dict[str, str] = load_services_from_config()


async def check_service(name: str, url: str) -> ServiceStatus:
    start = time.perf_counter()
    error: str | None = None
    healthy = False

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(url)
            healthy = resp.status_code == 200
            if not healthy:
                error = f"Status {resp.status_code}"
    except Exception as exc:
        error = str(exc)

    latency_ms = (time.perf_counter() - start) * 1000.0

    return ServiceStatus(
        name=name,
        url=url,
        healthy=healthy,
        latency_ms=latency_ms,
        last_error=error,
    )


async def get_all_service_statuses() -> List[ServiceStatus]:
    results: List[ServiceStatus] = []
    for name, url in MONITORED_SERVICES.items():
        status = await check_service(name, url)
        results.append(status)
    return results


def get_service_graph() -> ServiceGraph:
    # Simple example graph; you can evolve this or derive from config
    nodes = [
        ServiceNode(id="api-gateway", label="API Gateway"),
        ServiceNode(id="user-api", label="User API"),
        ServiceNode(id="auth-service", label="Auth Service"),
        ServiceNode(id="payments-service", label="Payments Service"),
        ServiceNode(id="database", label="Database"),
    ]
    edges = [
        ServiceEdge(from_id="api-gateway", to_id="user-api"),
        ServiceEdge(from_id="user-api", to_id="auth-service"),
        ServiceEdge(from_id="auth-service", to_id="database"),
        ServiceEdge(from_id="user-api", to_id="payments-service"),
        ServiceEdge(from_id="payments-service", to_id="database"),
    ]
    return ServiceGraph(nodes=nodes, edges=edges)
import time
from typing import Dict, List
from .models import ServiceGraph, ServiceNode, ServiceEdge

import httpx

from .models import ServiceStatus

# Example services to monitor (expand later / load from config)
MONITORED_SERVICES: Dict[str, str] = {
    "user-api": "http://user-api.local/health",
    "auth-service": "http://auth-service.local/health",
}


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



# Example dependency map:
# user-api -> auth-service -> database
#            \-> email-service
def get_service_graph() -> ServiceGraph:
    nodes = [
        ServiceNode(id="user-api", label="User API"),
        ServiceNode(id="auth-service", label="Auth Service"),
        ServiceNode(id="database", label="Database"),
        ServiceNode(id="email-service", label="Email Service"),
        ServiceNode(id="api-gateway", label="API Gateway"),
    ]
    edges = [
        ServiceEdge(from_id="api-gateway", to_id="user-api"),
        ServiceEdge(from_id="user-api", to_id="auth-service"),
        ServiceEdge(from_id="auth-service", to_id="database"),
        ServiceEdge(from_id="auth-service", to_id="email-service"),
    ]
    return ServiceGraph(nodes=nodes, edges=edges)
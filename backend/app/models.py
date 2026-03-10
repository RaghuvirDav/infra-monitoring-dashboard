from typing import List, Optional
from pydantic import BaseModel


class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float


class ServiceStatus(BaseModel):
    name: str
    url: str
    healthy: bool
    latency_ms: float
    last_error: Optional[str] = None


class Alert(BaseModel):
    id: str
    level: str  # "warning" | "critical"
    message: str
    source: str  # e.g. "system", "service:auth-api"
    active: bool


class ServiceNode(BaseModel):
    id: str
    label: str


class ServiceEdge(BaseModel):
    from_id: str
    to_id: str


class ServiceGraph(BaseModel):
    nodes: List[ServiceNode]
    edges: List[ServiceEdge]
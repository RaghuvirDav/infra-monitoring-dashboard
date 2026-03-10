import uuid
from typing import List

from .models import Alert, SystemMetrics, ServiceStatus

# naive in-memory alert store for demo
_ALERTS: List[Alert] = []


def _new_alert(level: str, message: str, source: str) -> Alert:
    alert = Alert(
        id=str(uuid.uuid4()),
        level=level,
        message=message,
        source=source,
        active=True,
    )
    _ALERTS.append(alert)
    return alert


def evaluate_system_alerts(metrics: SystemMetrics) -> List[Alert]:
    alerts: List[Alert] = []
    if metrics.cpu_percent > 90:
        alerts.append(
            _new_alert(
                level="warning",
                message=f"High CPU usage: {metrics.cpu_percent:.1f}%",
                source="system",
            )
        )
    if metrics.memory_percent > 90:
        alerts.append(
            _new_alert(
                level="warning",
                message=f"High memory usage: {metrics.memory_percent:.1f}%",
                source="system",
            )
        )
    if metrics.disk_percent > 90:
        alerts.append(
            _new_alert(
                level="warning",
                message=f"High disk usage: {metrics.disk_percent:.1f}%",
                source="system",
            )
        )
    return alerts


def evaluate_service_alerts(statuses: list[ServiceStatus]) -> List[Alert]:
    alerts: List[Alert] = []
    for s in statuses:
        if not s.healthy:
            alerts.append(
                _new_alert(
                    level="critical",
                    message=f"Service {s.name} unhealthy: {s.last_error}",
                    source=f"service:{s.name}",
                )
            )
        elif s.latency_ms > 2000:
            alerts.append(
                _new_alert(
                    level="warning",
                    message=f"Service {s.name} high latency: {s.latency_ms:.0f} ms",
                    source=f"service:{s.name}",
                )
            )
    return alerts


def list_alerts() -> List[Alert]:
    return _ALERTS

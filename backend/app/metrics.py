import psutil
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

from .models import SystemMetrics

# Prometheus metrics
CPU_USAGE = Gauge("system_cpu_percent", "System CPU usage percent")
MEM_USAGE = Gauge("system_memory_percent", "System memory usage percent")
DISK_USAGE = Gauge("system_disk_percent", "System disk usage percent")


def collect_system_metrics() -> SystemMetrics:
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    # update Prometheus gauges
    CPU_USAGE.set(cpu)
    MEM_USAGE.set(mem)
    DISK_USAGE.set(disk)

    return SystemMetrics(cpu_percent=cpu, memory_percent=mem, disk_percent=disk)


def prometheus_metrics_response():
    data = generate_latest()
    return CONTENT_TYPE_LATEST, data

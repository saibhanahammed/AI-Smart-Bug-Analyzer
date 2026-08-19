import re

def evaluate_severity_and_priority(log_text: str, summary: str = "") -> dict:
    """
    Evaluates error telemetry to classify severity, priority, component, and confidence.
    """
    combined = f"{summary} {log_text}".lower()
    
    # Defaults
    severity = "Medium"
    priority = "P2"
    component = "Core Engine"
    confidence = 88

    # Severity & Priority Classification Rules
    if any(k in combined for k in ["segfault", "sigsegv", "nullpointer", "deadlock", "memoryerror", "fatal", "out of memory"]):
        severity = "Critical"
        priority = "P0"
        confidence = 96
    elif any(k in combined for k in ["timeout", "connection refused", "broken pipe", "401 unauthorized", "unhandled"]):
        severity = "High"
        priority = "P1"
        confidence = 92
    elif any(k in combined for k in ["warning", "deprecated", "slow query", "css", "layout", "ui"]):
        severity = "Low"
        priority = "P3"
        confidence = 85

    # Component Detection
    if any(k in combined for k in ["canvas", "texture", "render", "ui", "css", "display"]):
        component = "Graphics / UI"
    elif any(k in combined for k in ["sql", "database", "hikaripool", "jdbc", "query"]):
        component = "Database / Pool"
    elif any(k in combined for k in ["auth", "token", "jwt", "session", "permission"]):
        component = "Auth & Security"
    elif any(k in combined for k in ["goroutine", "channel", "thread", "worker", "async"]):
        component = "Concurrency / Worker"
    elif any(k in combined for k in ["http", "payload", "fastapi", "middleware", "route"]):
        component = "API Gateway / Middleware"

    return {
        "severity": severity,
        "priority": priority,
        "component": component,
        "confidence": confidence
    }

# Alias for backwards compatibility
triage_defect = evaluate_severity_and_priority

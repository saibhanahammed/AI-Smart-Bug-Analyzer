def run_triage_agent(log_analysis_output: dict, vector_match: dict) -> dict:
    """Evaluates the log context to classify severity, priority, and affected components."""
    
    exc = log_analysis_output.get("exception_type", "").lower()
    comp = vector_match.get("component", "General Subsystem")
    
    # Logic rule engine for triage classification
    if "nullpointer" in exc or "fatal" in exc or "crash" in exc:
        severity = "Critical"
        priority = "P0 - Immediate Hotfix"
        reasoning = "Detected fatal runtime crash or unhandled null reference blocking execution thread."
        confidence = 0.95
    elif "leak" in exc or "memory" in exc:
        severity = "High"
        priority = "P1 - High Priority"
        reasoning = "Resource exhaustion/memory leak detected under high concurrency."
        confidence = 0.91
    else:
        severity = "Medium"
        priority = "P2 - Standard Sprint"
        reasoning = "Standard exception raised during lookup execution path."
        confidence = 0.85

    return {
        "agent_name": "Triage Agent",
        "status": "completed",
        "severity": severity,
        "priority": priority,
        "affected_component": comp,
        "confidence_score": confidence,
        "triage_reasoning": reasoning
    }
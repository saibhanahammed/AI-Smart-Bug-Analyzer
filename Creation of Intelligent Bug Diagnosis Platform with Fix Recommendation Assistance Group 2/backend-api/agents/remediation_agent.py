def run_remediation_agent(root_cause_output: dict, log_analysis_output: dict) -> dict:
    """Generates actionable fix recommendations and patch guidance."""
    
    exc = log_analysis_output.get("exception_type", "")
    
    if "NullPointer" in exc or "std::runtime_error" in exc:
        suggested_fix = "Implement defensive null checks prior to rendering invocation and enforce maximum texture dimension boundaries."
    elif "Timeout" in exc or "SQL" in exc:
        suggested_fix = "Increase database connection pool size, optimize query execution paths, and implement non-blocking connection retries."
    else:
        suggested_fix = "Apply defensive input validation, check memory allocation limits, and ensure resource descriptors are freed in finally blocks."

    return {
        "agent_name": "Remediation Agent",
        "status": "completed",
        "suggested_fix": suggested_fix,
        "best_practice_guidelines": [
            "Enforce strict bounds checking on external inputs.",
            "Utilize connection pool health checks to prevent resource leaks.",
            "Add automated unit tests covering edge-case boundary limits."
        ]
    }
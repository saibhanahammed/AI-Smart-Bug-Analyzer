import re

def run_log_analysis_agent(cleaned_log: str) -> dict:
    """Parses stack traces, identifies exception types, failure points, and code paths."""
    
    # Identify Exception Type
    exception_match = re.search(r'([a-zA-Z0-9_.]+(?:Exception|Error|Fault|Crash|runtime_error|NullPointer)[a-zA-Z0-9_.]*)', cleaned_log)
    exception_type = exception_match.group(1) if exception_match else "Unclassified System Exception"
    
    # Identify Failure Point / Line
    failure_match = re.search(r'at\s+([a-zA-Z0-9_.:]+(?:\(\w+\.\w+:\d+\))?)', cleaned_log)
    failure_point = failure_match.group(1) if failure_match else "Unknown Execution Context"
    
    # Identify Affected Code Path
    path_match = re.search(r'([a-zA-Z0-9_/\\]+\.(?:java|cpp|py|js|ts|go|c))', cleaned_log)
    affected_path = path_match.group(1) if path_match else "Core Module / Native Driver"

    return {
        "agent_name": "Log Analysis Agent",
        "status": "completed",
        "exception_type": exception_type,
        "failure_point": failure_point,
        "affected_code_path": affected_path,
        "raw_trace_summary": cleaned_log[:150] + "..." if len(cleaned_log) > 150 else cleaned_log
    }
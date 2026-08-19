import re

def analyze_stack_trace(raw_log: str) -> dict:
    """
    Parses exception stack traces to isolate exception type, failing file path, and line numbers.
    """
    lines = raw_log.split("\n")
    exception_type = "RuntimeError"
    file_path = "Unknown"
    line_number = "N/A"

    # Match exception types (e.g., NullPointerException, SIGSEGV, TypeError, MemoryError, etc.)
    exc_pattern = r"(?:([A-Za-z0-9_.]*(?:Exception|Error|Fault|SIGSEGV|SIGABRT|panic|deadlock)))"
    for line in lines:
        match = re.search(exc_pattern, line, re.IGNORECASE)
        if match:
            exception_type = match.group(1).strip()
            break

    # Match file paths and line numbers
    file_pattern = r"(?:(?:at|File|in)\s+)?([A-Za-z0-9_./\\-]+\.[a-zA-Z0-9]+)(?::|,\s*line\s*)(\d+)"
    for line in lines:
        match = re.search(file_pattern, line)
        if match:
            file_path = match.group(1).strip()
            line_number = match.group(2).strip()
            break

    return {
        "exception_type": exception_type,
        "file_path": file_path,
        "line_number": line_number,
        "raw_frames_count": len(lines)
    }

# Aliases
parse_log = analyze_stack_trace
analyze_log_trace = analyze_stack_trace

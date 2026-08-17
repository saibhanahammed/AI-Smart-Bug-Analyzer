# In-memory knowledge base with dynamic growth capabilities
DYNAMIC_KNOWLEDGE_BASE = [
    {
        "bug_id": "BUG-MOZ-7049",
        "repository": "Mozilla",
        "component": "Core::CanvasRenderer",
        "severity": "Critical",
        "description": "Crash in CanvasRenderer::Render. NullPointer exception occurs when canvas width exceeds texture size (> 16384px).",
        "fix_commit": "af8e12d3b4b8a927e",
        "score": 0.96
    },
    {
        "bug_id": "BUG-APA-1920",
        "repository": "Apache",
        "component": "httpd::mod_ssl",
        "severity": "High",
        "description": "Memory leak in ssl_filter_io_shutdown within mod_ssl. Connection keep-alive contexts fail to free descriptors.",
        "fix_commit": "88c21a9f0ee49271f",
        "score": 0.92
    },
    {
        "bug_id": "BUG-ECL-8830",
        "repository": "Eclipse",
        "component": "JDT::Compiler",
        "severity": "Medium",
        "description": "NullPointerException at ConstraintFormula.reduce when handling nested parameterized generics in Java lambda expressions.",
        "fix_commit": "c4a5b6d7e829fa771",
        "score": 0.89
    }
]

# Submission history for analytics tracking
SUBMISSION_HISTORY = [
    {"bug_id": "BUG-MOZ-7049", "component": "Core::CanvasRenderer", "severity": "Critical", "root_cause_theme": "Buffer/Hardware Overflow"},
    {"bug_id": "BUG-APA-1920", "component": "httpd::mod_ssl", "severity": "High", "root_cause_theme": "Resource / Memory Leak"},
    {"bug_id": "BUG-ECL-8830", "component": "JDT::Compiler", "severity": "Medium", "root_cause_theme": "Null Pointer Reference"},
    {"bug_id": "BUG-AUTH-1011", "component": "Auth::LoginService", "severity": "Critical", "root_cause_theme": "Connection Pool Exhaustion"},
    {"bug_id": "BUG-GATE-2041", "component": "Gateway::Proxy", "severity": "High", "root_cause_theme": "Concurrency Deadlock"}
]

def query_knowledge_base(query_text: str) -> dict:
    """Searches the dynamic knowledge base for the closest semantic match."""
    query_lower = query_text.lower()
    for item in DYNAMIC_KNOWLEDGE_BASE:
        if any(term in query_lower for term in item["component"].lower().split("::")):
            return item
    return DYNAMIC_KNOWLEDGE_BASE[0]

def add_resolved_bug_to_knowledge_base(new_bug: dict) -> dict:
    """Milestone 4 Growth Loop: Dynamically indexes confirmed resolved bugs."""
    new_entry = {
        "bug_id": f"BUG-RESOLVED-{len(DYNAMIC_KNOWLEDGE_BASE) + 1001}",
        "repository": new_bug.get("repository", "Production-App"),
        "component": new_bug.get("component", "General Module"),
        "severity": new_bug.get("severity", "Medium"),
        "description": new_bug.get("description", "Confirmed resolution issue."),
        "fix_commit": new_bug.get("fix_commit", "kb-growth-patch-001"),
        "score": 0.99
    }
    DYNAMIC_KNOWLEDGE_BASE.insert(0, new_entry)
    SUBMISSION_HISTORY.append({
        "bug_id": new_entry["bug_id"],
        "component": new_entry["component"],
        "severity": new_entry["severity"],
        "root_cause_theme": "Verified Resolution"
    })
    return new_entry

def compute_defect_analytics() -> dict:
    """Milestone 4 Analytics: Calculates recurring themes, component frequencies, and severities."""
    total_bugs = len(SUBMISSION_HISTORY)
    
    # Severity distribution
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    component_counts = {}
    theme_counts = {}

    for bug in SUBMISSION_HISTORY:
        sev = bug.get("severity", "Medium")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        comp = bug.get("component", "General")
        component_counts[comp] = component_counts.get(comp, 0) + 1
        
        theme = bug.get("root_cause_theme", "General Failure")
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    return {
        "total_submissions": total_bugs,
        "knowledge_base_size": len(DYNAMIC_KNOWLEDGE_BASE),
        "severity_breakdown": severity_counts,
        "frequent_components": sorted(component_counts.items(), key=lambda x: x[1], reverse=True)[:4],
        "systemic_patterns": sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    }
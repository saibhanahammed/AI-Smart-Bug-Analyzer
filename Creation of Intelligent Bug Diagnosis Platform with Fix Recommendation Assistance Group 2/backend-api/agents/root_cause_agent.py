def run_root_cause_agent(log_analysis: dict, vector_match: dict) -> dict:
    """Formulates a root cause hypothesis grounded in historical defect evidence."""
    
    exc = log_analysis.get("exception_type", "")
    failure = log_analysis.get("failure_point", "")
    hist_desc = vector_match.get("description", "")
    
    hypothesis = f"Execution path failure in {failure} triggered by {exc}. Matched historical pattern: '{hist_desc}'."
    
    return {
        "agent_name": "Root Cause Agent",
        "status": "completed",
        "root_cause_hypothesis": hypothesis,
        "confidence_score": vector_match.get("score", 0.88),
        "supporting_evidence": [
            f"Historical match {vector_match.get('bug_id')} in {vector_match.get('repository')}",
            f"Component target: {vector_match.get('component')}",
            f"Verified patch commit reference: {vector_match.get('fix_commit')}"
        ]
    }
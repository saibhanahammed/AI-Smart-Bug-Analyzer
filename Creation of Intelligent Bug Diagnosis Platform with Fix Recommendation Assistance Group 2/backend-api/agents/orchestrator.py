from agents.log_agent import run_log_analysis_agent
from agents.triage_agent import run_triage_agent
from agents.root_cause_agent import run_root_cause_agent
from agents.duplicate_agent import run_duplicate_detection_agent
from agents.remediation_agent import run_remediation_agent

def execute_multi_agent_pipeline(cleaned_log: str, vector_match: dict) -> dict:
    """Orchestrates all Milestone 3 AI agents sequentially."""
    
    # 1. Log Analysis
    log_results = run_log_analysis_agent(cleaned_log)
    
    # 2. Triage Classification
    triage_results = run_triage_agent(log_results, vector_match)
    
    # 3. Root Cause Agent (RAG Grounded)
    root_cause_results = run_root_cause_agent(log_results, vector_match)
    
    # 4. Duplicate Detection Agent
    duplicate_results = run_duplicate_detection_agent(cleaned_log)
    
    # 5. Remediation Agent
    remediation_results = run_remediation_agent(root_cause_results, log_results)
    
    return {
        "orchestration_status": "Success",
        "log_analysis": log_results,
        "triage": triage_results,
        "root_cause": root_cause_results,
        "duplicates": duplicate_results,
        "remediation": remediation_results
    }
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from triage_agent import evaluate_severity_and_priority
from log_agent import analyze_stack_trace
from root_cause_agent import generate_root_cause_hypothesis
from duplicate_agent import find_duplicate_tickets
from remediation_agent import generate_remediation_patch

def execute_multi_agent_pipeline(raw_log_text: str, summary: str = "") -> dict:
    """
    Sequential multi-agent orchestration pipeline passing context across all 5 agents.
    """
    triage = evaluate_severity_and_priority(raw_log_text, summary)
    log_analysis = analyze_stack_trace(raw_log_text)
    root_cause = generate_root_cause_hypothesis(raw_log_text, log_analysis, triage)
    duplicates = find_duplicate_tickets(raw_log_text, triage.get("component", "General"))
    remediation = generate_remediation_patch(root_cause, log_analysis, triage)

    return {
        "triage": triage,
        "logAnalysis": log_analysis,
        "rootCause": root_cause,
        "duplicateMatches": duplicates,
        "remediation": remediation
    }

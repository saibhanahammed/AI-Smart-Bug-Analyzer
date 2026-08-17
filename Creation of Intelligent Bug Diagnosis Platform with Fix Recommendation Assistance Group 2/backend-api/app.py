from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional
from pydantic import BaseModel
from preprocessor import clean_log_telemetry
from chunker import generate_text_chunks
from vector_store import (
    query_knowledge_base, 
    add_resolved_bug_to_knowledge_base, 
    compute_defect_analytics,
    DYNAMIC_KNOWLEDGE_BASE
)
from agents.orchestrator import execute_multi_agent_pipeline

# In backend-api/app.py
app = FastAPI(
    title="Creation of Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance Group 2",
    description="Multi-Agent AI Platform for Log Analysis, Root Cause Hypothesis, and Fix Recommendations"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConfirmFixPayload(BaseModel):
    component: str
    severity: str
    description: str
    fix_commit: str

@app.post("/api/v1/analyze-log")
async def analyze_log_file(
    file: Optional[UploadFile] = File(None),
    summary: Optional[str] = Form("")
):
    try:
        log_text = ""
        file_name = "Manual Summary Input"
        
        if file:
            if not file.filename.endswith(('.txt', '.log')):
                raise HTTPException(status_code=400, detail="Invalid format. Accepts .txt or .log files.")
            raw_content = await file.read()
            log_text = raw_content.decode("utf-8")
            file_name = file.filename
        elif summary:
            log_text = summary
        else:
            raise HTTPException(status_code=400, detail="Please upload a file or enter an issue summary.")

        cleaned = clean_log_telemetry(log_text)
        chunks = generate_text_chunks(cleaned)
        matched_defect = query_knowledge_base(log_text)
        
        agent_results = execute_multi_agent_pipeline(cleaned, matched_defect)

        return {
            "status": "success",
            "file_name": file_name,
            "triage": {
                "severity": agent_results["triage"]["severity"],
                "priority": agent_results["triage"]["priority"],
                "component": agent_results["triage"]["affected_component"],
                "confidence": int(agent_results["triage"]["confidence_score"] * 100),
                "reasoning": agent_results["triage"]["triage_reasoning"]
            },
            "logAnalysis": {
                "exceptionType": agent_results["log_analysis"]["exception_type"],
                "failurePoint": agent_results["log_analysis"]["failure_point"],
                "path": agent_results["log_analysis"]["affected_code_path"],
                "nextStep": "Verify stack trace parameters and inspect dependent resource connections."
            },
            "rootCause": {
                "hypothesis": agent_results["root_cause"]["root_cause_hypothesis"],
                "confidence": int(agent_results["root_cause"]["confidence_score"] * 100),
                "supportingEvidence": agent_results["root_cause"]["supporting_evidence"]
            },
            "duplicates": [
                {
                    "id": item["bug_id"],
                    "similarity": int(item.get("score", 0.85) * 100),
                    "title": item["description"],
                    "resolution": f"Resolved in commit {item['fix_commit']}."
                } for item in DYNAMIC_KNOWLEDGE_BASE[:3]
            ],
            "remediation": {
                "suggestedFix": agent_results["remediation"]["suggested_fix"],
                "bestPractices": agent_results["remediation"]["best_practice_guidelines"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Fault: {str(e)}")

@app.get("/api/v1/analytics")
def get_analytics():
    """Returns real-time Defect Pattern Analytics data."""
    return compute_defect_analytics()

@app.post("/api/v1/feedback/confirm-fix")
def confirm_and_grow_knowledge_base(payload: ConfirmFixPayload):
    """Adds a resolved fix to the Knowledge Base."""
    added_entry = add_resolved_bug_to_knowledge_base(payload.dict())
    return {
        "status": "success",
        "message": "Resolved bug successfully embedded into the vector database knowledge base.",
        "entry": added_entry,
        "analytics": compute_defect_analytics()
    }

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    with open("../frontend-ui/index.html", "r", encoding="utf-8") as f:
        return f.read()
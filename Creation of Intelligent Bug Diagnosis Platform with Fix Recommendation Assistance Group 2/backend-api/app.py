import os
import sys
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Ensure local imports resolve whether executed from root or backend-api
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from preprocessor import clean_log_telemetry
from chunker import generate_text_chunks
from vector_store import (
    query_knowledge_base,
    add_resolved_bug_to_knowledge_base,
    compute_defect_analytics,
    DYNAMIC_KNOWLEDGE_BASE
)
from agents.orchestrator import execute_multi_agent_pipeline

app = FastAPI(
    title="Creation of Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance Group 2",
    description="Multi-Agent AI Platform for Log Analysis, Root Cause Hypothesis, and Fix Recommendations",
    version="1.0.0"
)

# Enable CORS for local development and cloud hosting
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


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Locates and serves frontend-ui/index.html across local and cloud file paths."""
    search_paths = [
        os.path.join(CURRENT_DIR, "..", "frontend-ui", "index.html"),
        os.path.join(CURRENT_DIR, "frontend-ui", "index.html"),
        os.path.join(CURRENT_DIR, "..", "frontend-ui", "src", "index.html"),
        os.path.join(CURRENT_DIR, "index.html"),
    ]
    for path in search_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

    return "<h2>Intelligent Bug Diagnosis Platform API is running. Check /docs for Swagger UI.</h2>"


@app.get("/api/v1/analytics")
async def get_analytics():
    """Returns real-time aggregated defect distribution and knowledge base metrics."""
    try:
        data = compute_defect_analytics()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics computation error: {str(e)}")


@app.post("/api/v1/analyze-log")
async def analyze_log(
    file: Optional[UploadFile] = File(None),
    summary: Optional[str] = Form("")
):
    """Processes uploaded crash logs and triggers the 5-agent sequential pipeline."""
    try:
        content = ""
        if file is not None:
            raw_bytes = await file.read()
            content = raw_bytes.decode("utf-8", errors="ignore")

        combined_text = f"{summary.strip()}\n{content.strip()}".strip()
        if not combined_text:
            raise HTTPException(status_code=400, detail="No log content or issue summary provided.")

        # Execute multi-agent diagnostic orchestration
        analysis_result = execute_multi_agent_pipeline(combined_text)
        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-Agent Execution Fault: {str(e)}")


@app.post("/api/v1/feedback/confirm-fix")
async def confirm_fix(payload: ConfirmFixPayload):
    """Dynamically indexes validated bug fixes into the persistent vector store."""
    try:
        entry = add_resolved_bug_to_knowledge_base(
            component=payload.component,
            severity=payload.severity,
            description=payload.description,
            fix_commit=payload.fix_commit
        )
        return {"status": "success", "message": "Fix added to Knowledge Base", "entry": entry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge Base Indexing Error: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Intelligent Bug Diagnosis Platform"}

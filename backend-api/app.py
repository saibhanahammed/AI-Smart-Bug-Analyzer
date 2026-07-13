from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from preprocessor import clean_log_telemetry
from chunker import generate_text_chunks
from vector_store import query_knowledge_base

app = FastAPI(title="AI Smart Bug Analyzer Core API")

# Enable cross-origin calls for frontend display panels
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/analyze-log")
async def analyze_log_file(file: UploadFile = File(...)):
    # Validate file extension types
    if not file.filename.endswith(('.txt', '.log')):
        raise HTTPException(status_code=400, detail="Invalid log context format. System accepts only .txt or .log files.")
    
    try:
        raw_content = await file.read()
        log_text = raw_content.decode("utf-8")
        
        # Pipeline execution lane
        cleaned = clean_log_telemetry(log_text)
        chunks = generate_text_chunks(cleaned)
        matched_defect = query_knowledge_base(log_text)
        
        return {
            "status": "success",
            "file_name": file.filename,
            "pipeline_metrics": {
                "raw_character_count": len(log_text),
                "cleaned_character_count": len(cleaned),
                "total_chunks_generated": len(chunks)
            },
            "data_stages": {
                "cleaned_text": cleaned,
                "chunks": chunks
            },
            "vector_search_context": matched_defect
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Fault: {str(e)}")

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    # Points cleanly to the corrected frontend project directory root path
    with open("../frontend-ui/index.html", "r", encoding="utf-8") as f:
        return f.read()
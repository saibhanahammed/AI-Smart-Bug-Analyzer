# Creation of Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance Group 2

An AI-powered multi-agent platform designed to ingest raw telemetry and system crash reports, classify bug severity, parse stack traces, extract grounded root-cause hypotheses using RAG over historical defect datasets, surface duplicate issues, and provide actionable fix recommendations with continuous knowledge base growth.

---

## 📌 Features by Milestone

### 🔹 Milestone 1: Data Engineering & Vector Knowledge Base

* **Telemetry Intake:** Upload and process raw `.log` and `.txt` crash files.


* **Data Preprocessor:** Strips HTML/system noise, standardizes whitespace, and masks hex memory addresses into `[HEX_ADDR]` tokens.


* **Sliding Window Chunking:** Recursive chunking mechanism with configurable overlap to preserve stack trace continuity.


* **Vector Knowledge Base:** Semantic retrieval engine querying historical defect repositories (Mozilla, Apache, Eclipse).



### 🔹 Milestone 2: Stateful Multi-Agent Triage & Log Analysis

* **Log Analysis Agent:** Parses stack traces, extracting exception types, failing execution points, and affected file paths.


* **Triage & Severity Agent:** Determines severity (`Critical`, `High`, `Medium`, `Low`), priority tiers (P0–P3), component mapping, and confidence scores with reasoning.


* **Sequential Multi-Agent Orchestration:** Manages state flow across agents to enrich downstream defect context.



### 🔹 Milestone 3: Root Cause Hypothesis & Fix Remediation

* **Root Cause Agent (RAG-Grounded):** Synthesizes historical defect evidence and failure paths to output high-confidence root cause hypotheses.
* **Duplicate Detection Agent:** Identifies past resolved defects with similarity percentages and historical fix summaries.
* **Remediation Agent:** Provides patch guidance and best-practice engineering guidelines.
* **Structured Findings Dashboard:** Single-screen interface displaying all agent insights side-by-side.

### 🔹 Milestone 4: Defect Analytics & Knowledge Base Growth Loop

* **Defect Pattern Analytics:** Real-time metrics on total processed logs, severity distributions, high-frequency components, and systemic failure themes.
* **Knowledge Base Growth Mechanism:** Active learning loop allowing confirmed resolutions to be indexed dynamically back into the vector store.
* **Multi-Stack Validation Suite:** Verified across C++, Java, Python, JavaScript, and Go crash profiles.

---

## 🏗️ Architecture

```text
                       [ Raw Log / Telemetry Intake ]
                                     │
                        [ Regex & Hex Preprocessor ]
                                     │
                        [ Recursive Text Chunker ]
                                     │
                   [ Multi-Agent Orchestrator Pipeline ]
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
       [ Log Analysis Agent ]                  [ ChromaDB Vector Store ]
                 │                                       │
                 ▼                                       ▼
       [ Triage & Severity ]                   [ Duplicate Detection ]
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                        [ Root Cause Agent (RAG) ]
                                     │
                                     ▼
                         [ Remediation Agent ]
                                     │
                         [ Dynamic Growth Loop ] ──► (Indexed to Vector DB)
                                     │
                        [ UI Findings & Analytics ]

```

---

## 📂 Project Structure

```text
Ai_Smart_Bug_Analyzer/
├── backend-api/
│   ├── app.py                      # FastAPI core endpoints & static UI mount[cite: 1]
│   ├── preprocessor.py             # Telemetry cleaning & hex masking[cite: 3]
│   ├── chunker.py                  # Sliding window text chunking[cite: 2]
│   ├── vector_store.py             # Vector search, dynamic KB & analytics engine[cite: 4]
│   └── agents/
│       ├── __init__.py
│       ├── orchestrator.py         # Multi-agent state pipeline coordinator[cite: 6]
│       ├── log_agent.py            # Log Analysis Agent[cite: 5]
│       ├── triage_agent.py         # Triage & Severity Agent[cite: 7]
│       ├── root_cause_agent.py     # RAG Root Cause Agent
│       ├── duplicate_agent.py      # Duplicate Detection Agent
│       └── remediation_agent.py    # Fix Remediation Agent
├── frontend-ui/
│   └── index.html                  # React & Tailwind CSS dashboard[cite: 8]
├── LICENSE                         # MIT License
└── requirements.txt                # Project dependencies

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* Modern web browser (Chrome, Edge, Firefox)

### 1. Clone the Repository

```bash
git clone https://github.com/saibhanahammed/AI-Smart-Bug-Analyzer.git
cd AI-Smart-Bug-Analyzer

```

### 2. Set Up Virtual Environment & Dependencies

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install fastapi uvicorn pydantic python-multipart

```

### 3. Run the Backend API Server

```bash
cd backend-api
uvicorn app:app --reload

```

### 4. Access the Platform

Open your browser and navigate to:

```text
http://127.0.0.1:8000

```

---

## 🧪 Testing with Sample Defect Logs

You can test the multi-agent pipeline using varied sample defect logs:

* **C++ Hardware/Bounds Overflow:** `Mozilla::layers::CanvasRenderer::Render(CanvasRenderer.cpp:342)` bounds violation.


* **Java Concurrency / SQL Timeout:** `java.sql.SQLTimeoutException` on connection pool exhaustion.
* **Python Heap Exhaustion:** `MemoryError` during buffer allocation in streaming workers.
* **JavaScript / Node.js:** `UnhandledPromiseRejection` / `TypeError` on session verification.
* **Golang Concurrency:** Deadlock across unbuffered channel routines.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

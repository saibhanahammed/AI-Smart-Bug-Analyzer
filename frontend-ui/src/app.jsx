import React, { useState } from 'react';

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [pipelineData, setPipelineData] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setPipelineData(null);
    }
  };

  const submitLogFile = async () => {
    if (!selectedFile) {
      alert("Please select a diagnostic bug log file to execute pipeline ingestion.");
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/analyze-log", {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      setPipelineData(data);
    } catch (err) {
      alert("Failed to communicate with the FastAPI backend engine service.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-950/30 via-slate-950 to-slate-950">
      <header className="border-b border-slate-800 bg-slate-900/60 p-5 flex justify-between items-center">
        <div>
          <h1 className="text-lg font-bold text-white tracking-tight">AI Smart Bug Analyzer Dashboard</h1>
          <p className="text-xs text-slate-400">Milestone 1 Working Foundation • Connected via Asynchronous Python Service Layer</p>
        </div>
        <span className="text-xs font-mono bg-slate-900 border border-slate-800 px-3 py-1 rounded text-slate-400">
          Repository: saibhanahammed/AI-Smart-Bug-Analyzer
        </span>
      </header>

      <main className="flex-1 p-6 max-w-6xl w-full mx-auto space-y-6">
        
        {/* Bug Ingestion intake block */}
        <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-xl space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Bug Submission Module (Telemetry File Intake)</h3>
          
          <div className="flex flex-col items-center justify-center border-2 border-dashed border-slate-800 hover:border-blue-800 rounded-lg p-8 bg-slate-950 transition-all">
            <input type="file" id="logFileInput" accept=".log,.txt" onChange={handleFileChange} className="hidden" />
            <label htmlFor="logFileInput" className="cursor-pointer bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded shadow-md transition-all">
              Choose Telemetry Log File (.log, .txt)
            </label>
            {selectedFile && (
              <span className="text-xs font-mono text-blue-400 mt-3 font-semibold">Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)</span>
            )}
          </div>

          <div className="flex justify-end">
            <button onClick={submitLogFile} disabled={isUploading || !selectedFile} className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-bold text-xs px-5 py-2.5 rounded-lg transition-all shadow-lg">
              {isUploading ? "Executing Data Framework..." : "Upload & Analyze Log"}
            </button>
          </div>
        </div>

        {/* Dynamic Metric Telemetry Indicators */}
        {pipelineData && (
          <div className="space-y-6 animate-fade-in">
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-500 font-mono block uppercase">Data Ingestion Rate</span>
                <div className="text-xl font-bold font-mono mt-1 text-white">{pipelineData.pipeline_metrics.raw_character_count} Characters</div>
              </div>
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-500 font-mono block uppercase">Preprocessing Reductions</span>
                <div className="text-xl font-bold font-mono mt-1 text-emerald-400">Cleaned Down to {pipelineData.pipeline_metrics.cleaned_character_count}</div>
              </div>
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-500 font-mono block uppercase">Recursive Token Spaces</span>
                <div className="text-xl font-bold font-mono mt-1 text-blue-400">{pipelineData.pipeline_metrics.total_chunks_generated} Chunks Indexed</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                <span className="text-xs font-mono font-bold text-slate-400 block uppercase">Data Preprocessing &amp; Cleaning Output:</span>
                <p className="text-xs font-mono text-slate-300 bg-slate-950 p-3 rounded border border-slate-850 max-h-36 overflow-y-auto leading-relaxed">
                  {pipelineData.data_stages.cleaned_text}
                </p>
              </div>
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                <span className="text-xs font-mono font-bold text-slate-400 block uppercase">Recursive Character Text Chunking Windows:</span>
                <div className="max-h-36 overflow-y-auto space-y-1.5">
                  {pipelineData.data_stages.chunks.map((ch, idx) => (
                    <div key={idx} className="p-2 bg-slate-950 rounded border border-slate-850 text-[11px] font-mono">
                      <span className="text-[9px] text-blue-400 block font-bold">SLIDING WINDOW CONTEXT {idx+1}</span>
                      "{ch}..."
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
              <span className="text-xs font-mono font-bold text-slate-400 block uppercase">Knowledge Base Vector Store Query Retrieval Match:</span>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="bg-blue-950 text-blue-300 border border-blue-900 text-xs font-mono font-bold px-2 py-0.5 rounded">
                      {pipelineData.vector_search_context.bug_id}
                    </span>
                    <span className="text-xs font-semibold text-white">
                      {pipelineData.vector_search_context.repository} ({pipelineData.vector_search_context.component})
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 font-mono italic">"{pipelineData.vector_search_context.description}"</p>
                </div>
                <div className="text-left sm:text-right font-mono text-xs">
                  <div className="font-bold text-blue-400">Similarity Match: {(pipelineData.vector_search_context.score * 100).toFixed(1)}%</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Commit Hash Pointer: {pipelineData.vector_search_context.fix_commit}</div>
                </div>
              </div>
            </div>

          </div>
        )}

      </main>

      <footer className="border-t border-slate-900 bg-slate-950/80 px-6 py-4 text-center text-xs text-slate-500">
        © 2026 AI Smart Bug Analyzer &amp; Fix Advisor. Built by Shaik Saibhan Ahammed.
      </footer>
    </div>
  );
}
# Seeded knowledge base data records mimicking vector embeddings context
MOCK_KNOWLEDGE_BASE = [
    {
        "bug_id": "BUG-MOZ-7049",
        "repository": "Mozilla",
        "component": "Core::CanvasRenderer",
        "severity": "Critical",
        "description": "Crash in CanvasRenderer::Render. NullPointer exception occurs when canvas width is requested above maximum hardware acceleration texture size (> 16384px).",
        "fix_commit": "af8e12d3b4b8a927e",
        "score": 0.96
    },
    {
        "bug_id": "BUG-APA-1920",
        "repository": "Apache",
        "component": "httpd::mod_ssl",
        "severity": "Major",
        "description": "Memory leak in ssl_filter_io_shutdown within mod_ssl. Connection keep-alive contexts fail to free connection descriptors during heavy thread concurrency.",
        "fix_commit": "88c21a9f0ee49271f",
        "score": 0.92
    },
    {
        "bug_id": "BUG-ECL-8830",
        "repository": "Eclipse",
        "component": "JDT::Compiler",
        "severity": "Normal",
        "description": "NullPointerException at org.eclipse.jdt.internal.compiler.lookup.ConstraintFormula.reduce when handling highly nested parameterized generics inside Java lambda expressions.",
        "fix_commit": "c4a5b6d7e829fa771",
        "score": 0.89
    }
]

def query_knowledge_base(query_text: str) -> dict:
    """Simulates a RAG vector similarity database match based on trace footprints."""
    query_lower = query_text.lower()
    if "canvas" in query_lower or "mozilla" in query_lower:
        return MOCK_KNOWLEDGE_BASE[0]
    elif "ssl" in query_lower or "apache" in query_lower:
        return MOCK_KNOWLEDGE_BASE[1]
    return MOCK_KNOWLEDGE_BASE[2]
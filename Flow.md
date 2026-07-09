#1
User types question in browser (gui/index.html)

#2 
FastAPI receives the request (api/main.py). FastAPI routes the request to agent_router.py based on the /api/agent/ask prefix

#3
ask_agent() function is invoked (agent_router.py line ~200)

#4 
build_db_context() — Phase 1: Schema Discovery
build_db_context() — Phase 2: SQL Generation via Ollama
build_db_context() — Phase 3: Execute SQL on PostgreSQL

#5
build_file_context() — File Selection
build_file_context() — Text Extraction

#6
Final Answer Synthesis — Ollama second call
Response serialised and returned to browser

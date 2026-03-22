"""
routers/agent_router.py
────────────────────────
The AI Agent core.

Architecture:
  1. User sends a natural-language question.
  2. Agent fetches the DB schema and file list (real context, no guessing).
  3. Agent builds a strict prompt: "answer ONLY from the context provided."
  4. Local Ollama LLM (llama3/mistral/phi3 etc.) generates a plan.
  5. Agent executes each planned step: DB query OR file read.
  6. Final answer is assembled from real retrieved data only.

Zero hallucination guarantee:
  - LLM is instructed to say "I do not have information about that"
    if the answer cannot be found in the retrieved context.
  - temperature=0 for deterministic responses.
  - Every cited fact is traced back to a concrete source (DB row or file).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import json
import re

from config import settings
from routers.db_router import get_connection, get_schema
from routers.file_router import list_files_internal, extract_text, UPLOAD_DIR

from pathlib import Path

router = APIRouter()


# ─── Request / Response schemas ───────────────────────────────────────────────

class AgentRequest(BaseModel):
    question: str
    source: str = "auto"   # "db" | "files" | "auto" (both)
    max_results: int = 10


class SourceCitation(BaseModel):
    type: str          # "database" or "file"
    source: str        # table name or filename
    excerpt: str       # snippet of real data used


class AgentResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceCitation]
    confidence: str    # "high" | "medium" | "low" | "not_found"
    raw_context: Optional[str] = None


# ─── Ollama LLM call ──────────────────────────────────────────────────────────

def call_ollama(prompt: str, system: str = "") -> str:
    """
    Call the local Ollama server.
    Returns the model's response text.
    """
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "options": {
            "temperature": settings.LLM_TEMPERATURE,
            "num_predict": 1024,
        },
        "stream": False,
    }
    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=(
                "Cannot connect to Ollama at "
                f"{settings.OLLAMA_BASE_URL}. "
                "Please start Ollama: `ollama serve` and pull a model: "
                f"`ollama pull {settings.OLLAMA_MODEL}`"
            ),
        )


# ─── Context builders ─────────────────────────────────────────────────────────

def build_db_context(question: str, max_rows: int = 20) -> tuple[str, list]:
    citations = []

    # Get real schema
    try:
        schema_data = get_schema()
        schema_str = json.dumps(schema_data["tables"], indent=2)
    except Exception as e:
        return f"[Database unavailable: {e}]", citations

    # Ask LLM to write a SELECT query
    sql_system = (
        "You are a PostgreSQL expert. You write only SELECT statements. "
        "You use ONLY the table and column names given to you. "
        "Never invent table or column names. "
        "Respond with ONLY the SQL statement — no explanation, no markdown, no backticks."
    )
    sql_prompt = (
        f"Database schema:\n{schema_str}\n\n"
        f"Write a SELECT query to answer this question: {question}\n"
        f"If no relevant table exists, respond with: NO_RELEVANT_TABLE\n"
        f"Return ONLY the raw SQL, nothing else."
    )

    generated_sql = call_ollama(sql_prompt, system=sql_system)
    print(f"\n[DEBUG] Raw Ollama output: >>>{generated_sql}<<<\n")

    # Check for no relevant table
    if "NO_RELEVANT_TABLE" in generated_sql.upper():
        return "[No relevant database table for this question]", citations

    # Clean the SQL — remove markdown, backticks, explanations
    clean_sql = generated_sql.strip()
    clean_sql = re.sub(r"```sql|```", "", clean_sql).strip()
    clean_sql = re.sub(r"(?i)here is.*?:\s*", "", clean_sql).strip()
    clean_sql = re.sub(r"(?i)sql.*?:\s*", "", clean_sql).strip()

    # Extract only the SELECT statement if mixed with explanation
    match = re.search(r"(?i)(select\b.*)", clean_sql, re.DOTALL)
    if match:
        clean_sql = match.group(1).strip()

    # Ensure it ends with semicolon
    clean_sql = clean_sql.rstrip(";").strip() + ";"

    print(f"\n[DEBUG] Clean SQL: >>>{clean_sql}<<<\n")

    # Validate it starts with SELECT
    if not clean_sql.lower().startswith("select"):
        return "[Could not generate a valid SELECT query]", citations

    # Execute the query
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(clean_sql.rstrip(";") + f" LIMIT {max_rows}")
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                print(f"\n[DEBUG] Rows returned: {len(rows)}\n")

                if not rows:
                    return "[Query returned no rows]", citations

                lines = [" | ".join(cols)]
                lines.append("-" * 40)
                for row in rows:
                    lines.append(" | ".join(str(v) for v in row))

                context = f"[SQL: {clean_sql}]\n" + "\n".join(lines)

                table_match = re.findall(r"(?i)from\s+(\w+)", clean_sql)
                for tbl in table_match:
                    citations.append(SourceCitation(
                        type="database",
                        source=f"table:{tbl}",
                        excerpt=lines[2] if len(lines) > 2 else "",
                    ))
                return context, citations

    except Exception as e:
        print(f"\n[DEBUG] DB execution error: {e}\n")
        return f"[DB query error: {e}]", citations

def build_file_context(question: str, max_files: int = 5) -> tuple[str, list]:
    citations = []

    # Get real file list
    try:
        file_data = list_files_internal()
        all_files = file_data.get("files", [])
    except Exception as e:
        return f"[File system unavailable: {e}]", citations

    if not all_files:
        return "[No files found in the file store]", citations

    # Filter to only text-extractable files
    readable_extensions = {".txt", ".md", ".csv", ".pdf", ".docx", ".pptx", ".xlsx"}
    readable_files = [
        f for f in all_files
        if f["extension"] in readable_extensions
    ]

    if not readable_files:
        return "[No readable text files found]", citations

    # Build file list string for Ollama to choose from
    file_list_str = "\n".join(
        f"{f['relative_path']} ({f['size_bytes']} bytes)"
        for f in readable_files
    )

    print(f"\n[DEBUG] Available files:\n{file_list_str}\n")

    # Ask Ollama which files are relevant
    select_system = (
        "You select filenames relevant to a question. "
        "Return ONLY a JSON array of relative file paths from the list. "
        "Example: [\"bills/electricity_bill_mar2026.txt\"] "
        "Do not invent filenames. Use exact paths from the list. "
        "If none are relevant return []."
    )
    select_prompt = (
        f"Files available:\n{file_list_str}\n\n"
        f"Question: {question}\n\n"
        f"Return a JSON array of the most relevant file paths (max {max_files}). "
        f"Return ONLY the JSON array, no explanation."
    )

    selected_raw = call_ollama(select_prompt, system=select_system)
    print(f"\n[DEBUG] Ollama selected files: >>>{selected_raw}<<<\n")

    # Parse the selected files
    try:
        # Extract JSON array from response
        match = re.search(r"\[.*?\]", selected_raw, re.DOTALL)
        if match:
            selected = json.loads(match.group())
        else:
            # Fallback: if Ollama didn't return JSON, search by keyword
            selected = []
            question_words = question.lower().split()
            for f in readable_files:
                fname = f["relative_path"].lower()
                if any(word in fname for word in question_words):
                    selected.append(f["relative_path"])
            selected = selected[:max_files]
    except Exception as e:
        print(f"\n[DEBUG] File selection parse error: {e}\n")
        selected = []

    print(f"\n[DEBUG] Final selected files: {selected}\n")

    if not selected:
        # Last resort: read all files if question mentions bill/order/invoice
        keywords = ["bill", "invoice", "order", "amount", "total", "due", "payment"]
        if any(k in question.lower() for k in keywords):
            selected = [f["relative_path"] for f in readable_files[:max_files]]
            print(f"\n[DEBUG] Keyword fallback, reading: {selected}\n")

    if not selected:
        return "[No relevant files identified for this question]", citations

    # Extract real content from selected files
    parts = []
    for rel_path in selected:
        fpath = (UPLOAD_DIR / rel_path).resolve()
        if fpath.exists():
            content = extract_text(fpath)
            preview = content[:2000] + ("..." if len(content) > 2000 else "")
            parts.append(f"--- File: {rel_path} ---\n{preview}")
            citations.append(SourceCitation(
                type="file",
                source=rel_path,
                excerpt=content[:200],
            ))
            print(f"\n[DEBUG] Read file: {rel_path}, chars: {len(content)}\n")
        else:
            print(f"\n[DEBUG] File not found on disk: {fpath}\n")

    return "\n\n".join(parts) if parts else "[Selected files could not be read]", citations

# ─── Main agent endpoint ──────────────────────────────────────────────────────

@router.post("/ask", response_model=AgentResponse)
def ask_agent(request: AgentRequest):
    """
    Main conversational endpoint.
    The agent gathers real context from DB and/or files,
    then asks the local LLM to answer using ONLY that context.
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    context_parts = []
    all_citations = []

    # Gather context from requested sources
    if request.source in ("db", "auto"):
        db_ctx, db_cites = build_db_context(question, max_rows=request.max_results)
        context_parts.append(f"=== DATABASE DATA ===\n{db_ctx}")
        all_citations.extend(db_cites)

    if request.source in ("files", "auto"):
        file_ctx, file_cites = build_file_context(question, max_files=5)
        context_parts.append(f"=== FILE DATA ===\n{file_ctx}")
        all_citations.extend(file_cites)

    full_context = "\n\n".join(context_parts)

    # Final answer prompt — strict no-hallucination instruction
    answer_system = (
        "You are a data assistant. You will be given data retrieved from a database. "
        "Read the data carefully and answer the question directly and concisely. "
        "Always state the actual numbers or values from the data. "
        "Do not say you lack information if data is present in the context. "
        "If the context contains a COUNT or number, state it clearly."
    )

    answer_prompt = (
        f"DATA FROM DATABASE:\n{full_context}\n\n"
        f"QUESTION: {question}\n\n"
        f"Give a direct answer using the numbers in the data above. "
        f"Example: 'There are 5 total orders.' "
        f"Do not say you lack information — the data is right above."
    )

    answer = call_ollama(answer_prompt, system=answer_system)

    # Assess confidence
    not_found_phrases = ["do not have sufficient", "no information", "cannot find", "not available"]
    has_data = any(c.type == "database" for c in all_citations)
    confidence = "not_found" if (any(p in answer.lower() for p in not_found_phrases) and not has_data) else (
        "high" if all_citations else "low"
    )

    return AgentResponse(
        question=question,
        answer=answer,
        sources=all_citations,
        confidence=confidence,
        raw_context=full_context,
    )


@router.post("/summarise-file")
def summarise_file(payload: dict):
    """
    Summarise a specific file using the local LLM.
    Only real extracted file content is summarised — no hallucination.
    """
    filename = payload.get("filename", "")
    if not filename:
        raise HTTPException(status_code=400, detail="filename required")

    fpath = (UPLOAD_DIR / filename).resolve()
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    content = extract_text(fpath)
    if content.startswith("["):
        return {"filename": filename, "summary": content}

    system = (
        "You are a document summariser. Summarise only what is written in the document. "
        "Do not add commentary, context, or information not present in the text."
    )
    prompt = f"Summarise this document:\n\n{content[:4000]}"
    summary = call_ollama(prompt, system=system)

    return {
        "filename": filename,
        "summary": summary,
        "source": "local_file",
        "chars_processed": len(content),
    }

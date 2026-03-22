# Local Agentic AI System

A fully self-hosted, zero-cloud AI agent that retrieves information from your
PostgreSQL 18.1 database and local file system. Every answer is grounded in
real data. The system never fabricates content.

---

##python3.11
 python3.11 -m venv /home/hadoop/venv-claude
 source /home/hadoop/venv-claude/bin/activate
 deactivate

# run postgres
sudo docker run -d --name postgres18 -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres:18.1 postgres
sudo docker exec -it postgres18 bash
psql -U postgres
create database test;

#pip install -r requirements.txt
OR
Start.sh

-- one terminal
python api/main.py

--another terminal
python3 -m http.server 8080 --directory gui
http://0.0.0.0:8080/

--restart API
fuser -k 8000/tcp && cd ~/Agent-AI/api && python main.py


ComponentURLStatusGUI http://localhost:8080✅
API http://localhost:8000✅
Swagger docs http://localhost:8000/api/docs✅
PostgreSQL localhost:5432✅

# 
mkdir -p ~/Agent-AI/data/uploads/orders
mkdir -p ~/Agent-AI/data/uploads/bills
mkdir -p ~/Agent-AI/data/uploads/reports


## Architecture

```
gui/index.html          ← Single-file browser GUI (no build step)
api/
  main.py               ← FastAPI application entry point
  config.py             ← All configuration (DB, paths, LLM model)
  routers/
    db_router.py        ← PostgreSQL 18.1 queries (psycopg3)
    file_router.py      ← File system: browse, upload, extract text
    agent_router.py     ← AI agent: plan → retrieve → answer
data/
  uploads/              ← Drop files here (images, PDFs, docs, videos, PPTs…)
```

### Request flow

```
User question
    │
    ▼
agent_router.py
    ├── GET /api/db/schema          (discover real tables)
    ├── LLM generates SELECT SQL    (Ollama, local)
    ├── Run SELECT on PostgreSQL    (real rows only)
    ├── LLM selects relevant files  (from actual file list)
    ├── Extract text from files     (pdfplumber / docx / pptx / OCR)
    └── LLM synthesises answer      (ONLY from retrieved context)
```

---

## Prerequisites

| Component        | Version  | License    | Install                         |
|------------------|----------|------------|---------------------------------|
| Python           | ≥ 3.11   | PSF        | python.org                      |
| PostgreSQL       | 18.1     | PostgreSQL | postgresql.org                  |
| Ollama           | latest   | MIT        | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Tesseract OCR    | ≥ 5      | Apache 2   | `apt install tesseract-ocr`     |
| ffprobe (ffmpeg) | any      | LGPL       | `apt install ffmpeg`            |

All software is open-source. No cloud services are used. No API keys are required.

---

## Quick Start

```bash
# 1. Clone / copy this folder to your server
cd local-ai-agent

# 2. Edit database credentials
nano api/config.py          # set DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# 3. Run everything
chmod +x start.sh
./start.sh

# 4. Open the GUI
# Open gui/index.html in your browser
# OR: python -m http.server 8080 --directory gui   (serves on localhost:8080)
```

---

## API Reference

All endpoints are self-documented at `http://localhost:8000/api/docs`

### Agent

| Method | Endpoint           | Description                            |
|--------|--------------------|----------------------------------------|
| POST   | /api/agent/ask     | Ask a natural-language question        |
| POST   | /api/agent/summarise-file | Summarise a specific file        |

#### POST /api/agent/ask

```json
Request:
{
  "question": "Show me all overdue invoices from last month",
  "source": "auto",      // "auto" | "db" | "files"
  "max_results": 10
}

Response:
{
  "question": "Show me all overdue invoices from last month",
  "answer": "Based on the invoices table, there are 3 overdue invoices...",
  "sources": [
    { "type": "database", "source": "table:invoices", "excerpt": "INV-001 | 2024-01-15 | overdue" }
  ],
  "confidence": "high"   // "high" | "medium" | "low" | "not_found"
}
```

### Database

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /api/db/schema      | List all tables and columns        |
| POST   | /api/db/query       | Run a SELECT query                 |
| GET    | /api/db/reports     | List reports (search, paginate)    |
| GET    | /api/db/reports/{id}| Fetch a single report              |

### Files

| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| GET    | /api/files/list       | List all uploaded files          |
| POST   | /api/files/upload     | Upload a file                    |
| GET    | /api/files/read/{f}   | Extract text content from file   |
| GET    | /api/files/download/{f}| Download a file                 |
| DELETE | /api/files/delete/{f} | Delete a file                    |

---

## Supported File Types

| Type         | Extensions                          | Extraction method      |
|--------------|-------------------------------------|------------------------|
| Images       | jpg, jpeg, png, webp, gif, bmp      | Tesseract OCR          |
| PDFs         | pdf                                 | pdfplumber             |
| Word docs    | docx, doc                           | python-docx            |
| Presentations| pptx, ppt                           | python-pptx            |
| Spreadsheets | xlsx, xls                           | openpyxl               |
| Text/Markdown| txt, md, csv, log                   | direct read            |
| Video        | mp4, avi, mov, mkv                  | ffprobe metadata       |

---

## No-Hallucination Design

The system prevents fabricated answers through four mechanisms:

1. **Schema-first queries.** The agent reads the actual database schema before
   writing any SQL. It cannot invent table or column names.

2. **SELECT-only enforcement.** The query endpoint rejects any statement that
   does not begin with `SELECT`, preventing unintended data modification.

3. **Strict LLM prompt.** The final answer prompt instructs the model:
   *"Answer using only the context provided. If the context does not contain
   enough information, say so."*

4. **Zero temperature.** `temperature=0` makes the LLM deterministic, reducing
   creative fabrication to a minimum.

---

## Configuration

Edit `api/config.py` (or create a `.env` file):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=reports_db
DB_USER=postgres
DB_PASSWORD=your_password

UPLOAD_DIR=../data/uploads
OLLAMA_MODEL=llama3          # or: mistral, phi3, gemma2, deepseek-r1
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.0
```

### Choosing a local LLM model

| Model         | Size  | Good for                          |
|---------------|-------|-----------------------------------|
| llama3        | 4 GB  | General purpose (recommended)     |
| mistral       | 4 GB  | Fast, efficient                   |
| phi3          | 2 GB  | Low-RAM machines                  |
| gemma2        | 5 GB  | Strong reasoning                  |
| deepseek-r1   | 7 GB+ | Complex multi-step tasks          |

Pull any model: `ollama pull <model-name>`

---

## License

All dependencies are open-source (MIT, Apache 2, PostgreSQL, PSF).
This code is yours — no third-party licensing restrictions.

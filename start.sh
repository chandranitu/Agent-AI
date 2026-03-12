#!/usr/bin/env bash
# =============================================================================
# Local Agentic AI System — One-shot setup and run
# Tested on Ubuntu 22.04 / Debian 12 / macOS 13+
# =============================================================================
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Local Agentic AI System — Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Python deps ────────────────────────────────────────────────────────────
echo ""
echo "[1/4] Installing Python dependencies…"
pip install -r requirements.txt --quiet

# ── 2. System deps (Tesseract for image OCR, ffprobe for video) ──────────────
echo ""
echo "[2/4] Checking system tools…"

if command -v apt-get &>/dev/null; then
  sudo apt-get install -y --no-install-recommends tesseract-ocr ffmpeg 2>/dev/null || true
elif command -v brew &>/dev/null; then
  brew install tesseract ffmpeg 2>/dev/null || true
fi

# ── 3. Ollama ─────────────────────────────────────────────────────────────────
echo ""
echo "[3/4] Checking Ollama (local LLM runtime)…"

if ! command -v ollama &>/dev/null; then
  echo "  Ollama not found. Installing…"
  curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama in background if not running
if ! pgrep -x ollama &>/dev/null; then
  echo "  Starting Ollama daemon…"
  ollama serve &>/tmp/ollama.log &
  sleep 3
fi

# Pull model if not already downloaded
MODEL="llama3"
if ! ollama list 2>/dev/null | grep -q "$MODEL"; then
  echo "  Pulling $MODEL (this downloads ~4 GB, one-time only)…"
  ollama pull $MODEL
fi

echo "  Ollama ready. Model: $MODEL"

# ── 4. Start the API ──────────────────────────────────────────────────────────
echo ""
echo "[4/4] Starting FastAPI server on http://localhost:8000 …"
echo "      Swagger UI: http://localhost:8000/api/docs"
echo ""
echo "  ┌──────────────────────────────────────────────────┐"
echo "  │  GUI:  open gui/index.html in your browser        │"
echo "  │  API:  http://localhost:8000                      │"
echo "  │  Docs: http://localhost:8000/api/docs             │"
echo "  └──────────────────────────────────────────────────┘"
echo ""

cd api
python main.py

# ── Stage 1: Build dependencies ───────────────────────────────────────────────
FROM python:3.11-alpine AS builder

# Install build tools (only needed to compile packages)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    postgresql-dev

WORKDIR /build

COPY api/requirements.txt .

# Install Python packages into a separate folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Final lean image ─────────────────────────────────────────────────
FROM python:3.11-alpine

# Only runtime dependencies — no compilers
RUN apk add --no-cache \
    tesseract-ocr \
    ffmpeg \
    curl \
    libpq \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY api/ .

# Non-root user for security
RUN adduser -D -u 1000 appuser && \
    mkdir -p /app/data/uploads && \
    chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

CMD ["python", "main.py"]

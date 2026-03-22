from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from routers import db_router, file_router, agent_router
from config import settings

app = FastAPI(
    title="Agent-AI Local System",
    version="1.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/files", StaticFiles(directory=settings.UPLOAD_DIR), name="files")

app.include_router(db_router.router,    prefix="/api/db",    tags=["Database"])
app.include_router(file_router.router,  prefix="/api/files", tags=["File System"])
app.include_router(agent_router.router, prefix="/api/agent", tags=["Agent"])

@app.get("/")
def root():
    return {"status": "ok", "service": "Agent-AI API"}

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Agent-AI running in Docker"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

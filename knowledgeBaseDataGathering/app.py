"""FastAPI entrypoint.

Run: uvicorn knowledgeBaseDataGathering.app:app --reload
"""

from fastapi import FastAPI

from .routes import router

app = FastAPI(title="FootBallRag - NFL data API", version="0.1.0")
app.include_router(router)

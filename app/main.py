from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.claim_router import router
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="FNOLAgent — Autonomous Insurance Claims Processing Agent",
    description=(
        "AI-powered FNOL document processing system that extracts structured claim data, "
        "validates mandatory fields, and routes claims automatically using Azure OpenAI."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

logger.info("FNOLAgent API started")

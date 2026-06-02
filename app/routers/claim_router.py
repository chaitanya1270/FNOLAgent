from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.response_models import ClaimResponse, HealthResponse
from app.services.document_parser import parse_document
from app.services.extraction_service import extract_claim_fields
from app.services.validation_service import validate_claim
from app.services.routing_service import determine_route
from app.services.reasoning_service import generate_reasoning
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

ALLOWED_TYPES = {"application/pdf", "text/plain"}
ALLOWED_EXTENSIONS = {".pdf", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Service health check."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model=settings.openai_structured_output_model,
    )


@router.post(
    "/upload-claim",
    response_model=ClaimResponse,
    tags=["Claims"],
    summary="Upload and process an FNOL document",
    response_description="Extracted claim data with routing decision",
)
async def upload_claim(file: UploadFile = File(...)) -> ClaimResponse:
    """
    Accept a PDF or TXT FNOL document, extract structured claim fields via
    Azure OpenAI, validate mandatory fields, apply routing rules, and return
    the full structured JSON result.
    """
    _validate_file_type(file)

    file_bytes = await file.read()
    _validate_file_size(file_bytes, file.filename)

    logger.info("Processing claim document: %s (%d bytes)", file.filename, len(file_bytes))

    document_text = parse_document(file_bytes, file.filename)
    if not document_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not extract text from the uploaded document. "
                   "Ensure it is a readable PDF or plain-text file.",
        )

    extracted = await extract_claim_fields(document_text)
    missing = validate_claim(extracted)
    route = determine_route(extracted, missing)
    reasoning = generate_reasoning(route, extracted, missing)

    logger.info("Claim processed — route: %s", route)

    return ClaimResponse(
        extractedFields=extracted,
        missingFields=missing,
        recommendedRoute=route,
        reasoning=reasoning,
    )


def _validate_file_type(file: UploadFile) -> None:
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    content_type = file.content_type or ""

    if ext not in ALLOWED_EXTENSIONS and content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{ext}'. Only PDF and TXT files are accepted.",
        )


def _validate_file_size(file_bytes: bytes, filename: str) -> None:
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File '{filename}' exceeds the 10 MB size limit.",
        )
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

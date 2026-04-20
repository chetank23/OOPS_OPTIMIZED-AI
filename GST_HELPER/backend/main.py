from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schemas import ErrorResponse, ProcessInvoiceResponse
from services.pipeline import InvoiceProcessingPipeline, PipelineStageError
from storage import init_storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pipeline = InvoiceProcessingPipeline()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize local JSON storage before the app starts serving requests."""

    init_storage()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="GST Invoice AI Processing Pipeline",
        version="1.0.0",
        description="Processes GST invoices through OCR, extraction, validation, reconciliation, anomaly detection, and reporting.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(PipelineStageError)
    async def pipeline_stage_error_handler(_request, exc: PipelineStageError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(error=exc.message, stage=exc.stage).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(_request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error=exc.errors()[0].get("msg", "Invalid request."),
                stage="request_validation",
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception in GST invoice API")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Unexpected server error.",
                stage="internal",
            ).model_dump(),
        )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/process-invoice",
        response_model=ProcessInvoiceResponse,
        responses={
            400: {"model": ErrorResponse},
            422: {"model": ErrorResponse},
            500: {"model": ErrorResponse},
        },
    )
    async def process_invoice(file: UploadFile = File(...)) -> ProcessInvoiceResponse:
        """Run the full GST invoice processing pipeline for a single upload."""

        return await pipeline.process_uploaded_invoice(file)

    return app


app = create_app()

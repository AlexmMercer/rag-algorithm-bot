import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openai import APIError

from app.routes.chat import router

logger = logging.getLogger(__name__)

app = FastAPI(title="RAGStudyBot", version="0.1.0")


@app.exception_handler(APIError)
async def api_error_handler(request, exc: APIError) -> JSONResponse:
    logger.exception("LLM API error")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc.message)},
    )


app.include_router(router)

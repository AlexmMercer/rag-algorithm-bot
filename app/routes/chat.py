from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.clients.llm import LLMClient
from app.dependencies import get_llm_client, get_settings
from app.schemas.chat import AnswerResponse, QuestionRequest
from app.settings import Settings

router = APIRouter()


@router.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"status": "ok", "model": settings.llm_model}


@router.post("/question")
async def question(
    body: QuestionRequest,
    llm: LLMClient = Depends(get_llm_client),
) -> AnswerResponse:
    answer = await llm.ask(body.text)
    return AnswerResponse(text=answer)

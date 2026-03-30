from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=2000, description="User question text"
    )


class AnswerResponse(BaseModel):
    text: str = Field(..., description="LLM answer text")

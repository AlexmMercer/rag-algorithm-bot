from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_redirects_to_docs() -> None:
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model" in data


@patch("app.main.ask_llm", new_callable=AsyncMock)
def test_question_success(mock_llm: AsyncMock) -> None:
    mock_llm.return_value = "Binary search has O(log n) complexity."
    response = client.post("/question", json={"text": "What is binary search?"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Binary search has O(log n) complexity."
    mock_llm.assert_awaited_once_with("What is binary search?")


def test_question_empty_text() -> None:
    response = client.post("/question", json={"text": ""})
    assert response.status_code == 422


def test_question_missing_text() -> None:
    response = client.post("/question", json={})
    assert response.status_code == 422


def test_question_text_too_long() -> None:
    response = client.post("/question", json={"text": "a" * 2001})
    assert response.status_code == 422


def test_question_whitespace_only() -> None:
    """Single space is valid (min_length=1 counts characters, not stripped)."""
    with patch("app.main.ask_llm", new_callable=AsyncMock, return_value="..."):
        response = client.post("/question", json={"text": " "})
    assert response.status_code == 200


def test_question_exactly_max_length() -> None:
    with patch("app.main.ask_llm", new_callable=AsyncMock, return_value="ok"):
        response = client.post("/question", json={"text": "a" * 2000})
    assert response.status_code == 200


@patch("app.main.ask_llm", new_callable=AsyncMock)
def test_question_llm_api_error(mock_llm: AsyncMock) -> None:
    import httpx
    from openai import APIStatusError

    mock_llm.side_effect = APIStatusError(
        message="Service overloaded",
        response=httpx.Response(status_code=503, request=httpx.Request("POST", "/")),
        body=None,
    )
    response = client.post("/question", json={"text": "hello"})
    assert response.status_code == 500
    assert "Service overloaded" in response.json()["detail"]


@pytest.mark.parametrize(
    "payload",
    [
        {"text": 123},
        {"text": None},
        "not json",
    ],
)
def test_question_invalid_types(payload: object) -> None:
    if isinstance(payload, str):
        response = client.post(
            "/question", content=payload, headers={"content-type": "application/json"}
        )
    else:
        response = client.post("/question", json=payload)
    assert response.status_code == 422

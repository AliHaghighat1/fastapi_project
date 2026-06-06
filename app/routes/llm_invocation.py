"""LLM invocation endpoint."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/get_llm_joke", tags=["get_llm_joke"])


@router.get("")
@router.get("/", include_in_schema=False)
def call_llm() -> dict[str, str]:
    """Call Cohere and return a short joke."""
    if not settings.cohere_api_token:
        return {"error": "COHERE_API_TOKEN not set"}

    try:
        import cohere

        co_v2 = cohere.ClientV2(api_key=settings.cohere_api_token)
        response = co_v2.chat(
            model="command-a-plus-05-2026",
            messages=[{"role": "user", "content": "Tell me a joke!"}],
            thinking={"type": "disabled"},
        )
        return {"llm_response": response.message.content[0].text}
    except Exception as exc:
        return {"error": f"Client validation failed: {exc}"}

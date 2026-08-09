import cohere
from app.config import settings

co = cohere.Client(settings.COHERE_API_KEY)


def test_cohere():
    response = co.chat(
        model=settings.COHERE_MODEL,
        message="Say hello!",
        max_tokens=200
    )
    return response.text


def chat_with_ai(user_message: str, context: str = None):
    preamble = None
    if context:
        preamble = (
            "You are a helpful customer service assistant. Answer the question "
            "using only the context below. If the answer is not in the context, "
            f"say you don't know.\n\nContext:\n{context}"
        )

    response = co.chat(
        model=settings.COHERE_MODEL,
        message=user_message,
        preamble=preamble,
        max_tokens=200
    )

    tokens = int(response.meta.tokens.input_tokens + response.meta.tokens.output_tokens)

    return response.text, tokens

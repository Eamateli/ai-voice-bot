import cohere 
from app.config import settings

co = cohere.Client(settings.COHERE_API_KEY)


def test_cohere():
    response = co.generate(
        model ="command",
        prompt="Say hello!",
        max_tokens=200

    )
    return response.generations[0].text


def chat_with_ai(user_message: str):
    response = co.generate(
        model ="command",
        prompt=user_message,
        max_tokens=200

    )
    return response.generations[0].text
    
    text = response.generations[0].text
    tokens = len(user_message.split()) + lne(text.split())

    return text, tokens
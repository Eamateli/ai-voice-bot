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


def chat_with_ai(user_message: str, context: str = None):
    if context:
        prompt = f"Context: {context}\n\nQuestion: {user_message}"
    else:
        prompt = user_message
    
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=200
    )
    
    text = response.generations[0].text
    tokens = len(prompt.split()) + len(text.split())
    
    return text, tokens
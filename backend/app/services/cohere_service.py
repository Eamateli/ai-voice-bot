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
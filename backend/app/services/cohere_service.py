import cohere 
from app.config import settings

co = cohere.Client(settings.cohere_api_key)

def test_cohere():
    response = co.generate(
        model ="command-r",
        prompt="Say hello!",
        max_tokens=50

    )
    return response.generations[0].text
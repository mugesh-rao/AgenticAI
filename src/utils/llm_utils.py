import openai
from typing import List, Dict, Any

def setup_openai(api_key: str) -> None:
    """Setup OpenAI with the provided API key."""
    openai.api_key = api_key

def create_chat_completion(
    messages: List[Dict[str, str]], 
    model: str = "gpt-4-turbo",
    temperature: float = 0.7
) -> str:
    """Create a chat completion using OpenAI's API."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error in chat completion: {str(e)}") 
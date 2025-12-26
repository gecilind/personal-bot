import os
from openai import OpenAI
from django.conf import settings


def get_embedding(text: str) -> list:
    """
    Generate embedding for text using OpenAI API.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    # Get API key - try multiple sources
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        # Try loading from environment directly
        api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables. Please check your .env file.")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Error generating embedding: {str(e)}")


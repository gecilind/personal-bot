import json
from openai import OpenAI
from django.conf import settings
from assistant.services.vector_search import get_relevant_context
from assistant.services.embeddings import get_embedding
from assistant.models import AssistantMemory


def generate_response(user_message: str) -> dict:
    """
    Generate AI assistant response using RAG (Retrieval Augmented Generation).
    Also stores user message and assistant response with embeddings.
    
    Args:
        user_message: User's question/message
        
    Returns:
        Dictionary with 'response' and 'relevant_knowledge' keys
    """
    # Get API key - try multiple sources
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        # Try loading from environment directly
        import os
        api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables. Please check your .env file.")
    
    client = OpenAI(api_key=api_key)
    
    # Store user message with embedding
    try:
        user_embedding = get_embedding(user_message)
        user_embedding_json = json.dumps(user_embedding)
        AssistantMemory.objects.create(
            content=f"User: {user_message}",
            embedding=user_embedding_json,
            type='memory'
        )
    except Exception as e:
        # Log but don't fail
        print(f"Error storing user message: {str(e)}")
    
    # Get relevant context from vector search
    context = get_relevant_context(user_message)
    
    # Build prompt with context
    knowledge_text = "\n".join([f"- {k}" for k in context['knowledge']])
    memory_text = "\n".join([f"- {m}" for m in context['memory']])
    
    system_prompt = """You are a personal AI assistant trained on professional CV data. 
Use the provided knowledge and memory to answer questions accurately and helpfully.
If the information is not available in the context, say so politely."""
    
    user_prompt = f"""Based on the following knowledge and memory, answer the user's question.

KNOWLEDGE BASE:
{knowledge_text if knowledge_text else "No relevant knowledge found."}

PREVIOUS MEMORIES:
{memory_text if memory_text else "No relevant memories found."}

USER QUESTION: {user_message}

Provide a helpful and accurate response based on the above information."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store assistant response with embedding (always store responses)
        try:
            assistant_embedding = get_embedding(assistant_response)
            assistant_embedding_json = json.dumps(assistant_embedding)
            AssistantMemory.objects.create(
                content=f"Assistant: {assistant_response}",
                embedding=assistant_embedding_json,
                type='memory'
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error storing assistant response: {str(e)}")
        
        return {
            'response': assistant_response,
            'relevant_knowledge': context['knowledge'],
        }
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")


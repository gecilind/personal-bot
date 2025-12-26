import json
from openai import OpenAI
from django.conf import settings
from assistant.services.vector_search import get_relevant_context
from assistant.services.embeddings import get_embedding
from assistant.models import AssistantMemory


# Check if resume has been ingested (cache to avoid checking on every request)
_resume_ingested_check = None

def _ensure_resume_ingested():
    """Check if resume knowledge base exists, if not try to ingest it."""
    global _resume_ingested_check
    
    # Check once per process
    if _resume_ingested_check is not None:
        return _resume_ingested_check
    
    knowledge_count = AssistantMemory.objects.filter(type='knowledge').count()
    _resume_ingested_check = knowledge_count > 0
    
    if not _resume_ingested_check:
        # Try to ingest resume automatically
        try:
            from assistant.services.ingest_resume import ingest_resume
            print("[INFO] No resume knowledge found. Attempting to ingest resume...")
            ingest_resume()
            _resume_ingested_check = True
            print("[INFO] Resume successfully ingested!")
        except Exception as e:
            print(f"[WARNING] Could not auto-ingest resume: {str(e)}")
            print("[INFO] Please run: python manage.py ingest_resume")
            _resume_ingested_check = False
    
    return _resume_ingested_check


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
    
    # Ensure resume is ingested before generating response
    _ensure_resume_ingested()
    
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
    
    # Get relevant context from vector search - increase knowledge limit to get more resume content
    context = get_relevant_context(user_message, knowledge_limit=10, memory_limit=3)
    
    # Build prompt with context
    knowledge_text = "\n\n".join([f"{i+1}. {k}" for i, k in enumerate(context['knowledge'])])
    memory_text = "\n".join([f"- {m}" for m in context['memory']])
    
    system_prompt = """You are a personal AI assistant that answers questions about Lind Geci based on their professional CV/resume. 
Your primary source of information is the KNOWLEDGE BASE below which contains detailed information from the CV.
Always prioritize information from the KNOWLEDGE BASE when answering questions.
Answer questions accurately, helpfully, and in a professional manner based on the CV data provided."""
    
    user_prompt = f"""Answer the user's question about Lind Geci using the following CV/resume information:

=== CV/RESUME KNOWLEDGE BASE ===
{knowledge_text if knowledge_text else "No knowledge base found. Please note that the resume data may not be loaded."}

=== PREVIOUS CONVERSATION CONTEXT ===
{memory_text if memory_text else "No previous conversation context."}

=== USER QUESTION ===
{user_message}

Provide a comprehensive and accurate answer based primarily on the CV/resume knowledge base above. If you cannot find specific information, acknowledge that politely but provide what you can from the available information."""
    
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


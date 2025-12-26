# Temporarily using simple text search until pgvector is installed
# from pgvector.django import CosineDistance
from django.db.models import Q
from assistant.models import AssistantMemory
# from assistant.services.embeddings import get_embedding


def search_similar_memories(query_text: str, limit: int = 5, memory_type: str = None):
    """
    Search for similar memories using simple text search (temporary until pgvector is ready).
    
    Args:
        query_text: Query text to search for
        limit: Maximum number of results to return
        memory_type: Filter by type ('knowledge' or 'memory'), None for both
        
    Returns:
        QuerySet of AssistantMemory objects
    """
    # Build query with simple text search
    queryset = AssistantMemory.objects.all()
    
    # Filter by type if specified
    if memory_type:
        queryset = queryset.filter(type=memory_type)
    
    # Simple text search - look for query words in content
    # Handle name variations (e.g., "lind geci", "lindgeci", "Lind Geci")
    query_normalized = query_text.lower().replace(' ', '')
    query_words = query_text.lower().split()
    
    q_objects = Q()
    for word in query_words:
        # Regular word match
        q_objects |= Q(content__icontains=word)
        # Also check for concatenated version (e.g., "lindgeci")
        if len(word) > 3:
            q_objects |= Q(content__icontains=word.replace(' ', ''))
    
    # Also search for normalized version of the query
    if len(query_normalized) > 5:
        q_objects |= Q(content__icontains=query_normalized)
    
    results = queryset.filter(q_objects).order_by('-created_at')[:limit]
    
    # If no specific results but we're looking for knowledge, return all knowledge items (up to limit)
    if not results and memory_type == 'knowledge':
        results = queryset.order_by('-created_at')[:limit]
    # If still no results, return recent items
    elif not results:
        results = queryset.order_by('-created_at')[:limit]
    
    return results


def get_relevant_context(query_text: str, knowledge_limit: int = 10, memory_limit: int = 3):
    """
    Get relevant knowledge and memory for RAG context.
    
    Args:
        query_text: User query
        knowledge_limit: Number of knowledge chunks to retrieve (increased default for better CV coverage)
        memory_limit: Number of memory chunks to retrieve
        
    Returns:
        Dictionary with 'knowledge' and 'memory' lists
    """
    knowledge_results = search_similar_memories(
        query_text, 
        limit=knowledge_limit, 
        memory_type='knowledge'
    )
    
    memory_results = search_similar_memories(
        query_text, 
        limit=memory_limit, 
        memory_type='memory'
    )
    
    # If we found some knowledge results, use them; otherwise try to get all knowledge items
    if not knowledge_results:
        # Try to get all knowledge items if no specific matches
        from assistant.models import AssistantMemory
        all_knowledge = AssistantMemory.objects.filter(type='knowledge').order_by('-created_at')[:knowledge_limit]
        knowledge_results = all_knowledge
    
    return {
        'knowledge': [item.content for item in knowledge_results],
        'memory': [item.content for item in memory_results],
    }


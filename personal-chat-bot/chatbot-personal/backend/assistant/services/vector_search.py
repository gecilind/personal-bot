"""
Vector similarity search using cosine similarity.
Embeddings are stored as JSON strings in PostgreSQL and compared using numpy.
"""
import json
import numpy as np
from assistant.models import AssistantMemory
from assistant.services.embeddings import get_embedding


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector (list or numpy array)
        vec2: Second vector (list or numpy array)
        
    Returns:
        Cosine similarity score between -1 and 1 (1 = identical, 0 = orthogonal, -1 = opposite)
    """
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)
    
    # Calculate dot product
    dot_product = np.dot(vec1, vec2)
    
    # Calculate norms
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    # Cosine similarity
    return dot_product / (norm1 * norm2)


def search_similar_memories(query_text: str, limit: int = 5, memory_type: str = None):
    """
    Search for similar memories using vector similarity (cosine similarity).
    
    Args:
        query_text: Query text to search for
        limit: Maximum number of results to return
        memory_type: Filter by type ('knowledge' or 'memory'), None for both
        
    Returns:
        List of AssistantMemory objects ordered by similarity (most similar first)
    """
    # Generate embedding for the query
    try:
        query_embedding = get_embedding(query_text)
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        # If embedding generation fails, return empty list
        return []
    
    # Get all memories of the specified type
    queryset = AssistantMemory.objects.filter(type=memory_type) if memory_type else AssistantMemory.objects.all()
    
    # Calculate similarity for each memory that has an embedding
    similarities = []
    for memory in queryset:
        if memory.embedding:
            try:
                # Parse the stored embedding (stored as JSON string)
                stored_embedding = json.loads(memory.embedding)
                
                # Calculate cosine similarity
                similarity_score = cosine_similarity(query_embedding, stored_embedding)
                
                # Store tuple of (similarity_score, memory_object)
                similarities.append((similarity_score, memory))
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                # Skip memories with invalid embeddings
                print(f"Error processing embedding for memory {memory.id}: {e}")
                continue
    
    # Sort by similarity score (highest first) and return top results
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Return only the memory objects (not the similarity scores)
    return [memory for _, memory in similarities[:limit]]


def get_relevant_context(query_text: str, knowledge_limit: int = 10, memory_limit: int = 3):
    """
    Get relevant knowledge and memory for RAG context using vector similarity.
    
    Args:
        query_text: User query
        knowledge_limit: Number of knowledge chunks to retrieve
        memory_limit: Number of memory chunks to retrieve
        
    Returns:
        Dictionary with 'knowledge' and 'memory' lists
    """
    # Search for similar knowledge using vector similarity
    knowledge_results = search_similar_memories(
        query_text, 
        limit=knowledge_limit, 
        memory_type='knowledge'
    )
    
    # Search for similar memory using vector similarity
    memory_results = search_similar_memories(
        query_text, 
        limit=memory_limit, 
        memory_type='memory'
    )
    
    # If no knowledge results found (e.g., no embeddings exist yet), fallback to recent items
    if not knowledge_results:
        all_knowledge = AssistantMemory.objects.filter(type='knowledge').order_by('-created_at')[:knowledge_limit]
        knowledge_results = list(all_knowledge)
    
    # Same fallback for memory
    if not memory_results:
        all_memory = AssistantMemory.objects.filter(type='memory').order_by('-created_at')[:memory_limit]
        memory_results = list(all_memory)
    
    return {
        'knowledge': [item.content for item in knowledge_results],
        'memory': [item.content for item in memory_results],
    }


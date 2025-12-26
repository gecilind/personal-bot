import os
import json
from pathlib import Path
from django.conf import settings
from assistant.models import AssistantMemory
from assistant.services.embeddings import get_embedding


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def clean_text(text: str) -> str:
    """
    Clean and normalize text from PDF.
    
    Args:
        text: Raw text from PDF
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    return ' '.join(cleaned_lines)


def ingest_resume():
    """
    Read resume.txt, chunk it, generate embeddings, and store in database.
    Clears existing knowledge entries before ingesting.
    """
    # Get path to resume.txt
    base_dir = Path(__file__).resolve().parent.parent
    resume_path = base_dir / 'resume.txt'
    
    if not resume_path.exists():
        raise FileNotFoundError(f"Resume file not found at {resume_path}")
    
    # Read resume text
    with open(resume_path, 'r', encoding='utf-8') as f:
        resume_text = f.read()
    
    if not resume_text.strip():
        raise ValueError("Resume file is empty. Please add your CV content to resume.txt")
    
    # Clean text
    cleaned_text = clean_text(resume_text)
    
    # Chunk text
    chunks = chunk_text(cleaned_text)
    
    if not chunks:
        raise ValueError("No chunks generated from resume text")
    
    # Clear existing knowledge entries
    AssistantMemory.objects.filter(type='knowledge').delete()
    print(f"Cleared existing knowledge entries. Ingesting {len(chunks)} chunks...")
    
    # Generate embeddings and store (as JSON string for now, until pgvector is ready)
    for i, chunk in enumerate(chunks, 1):
        try:
            embedding = get_embedding(chunk)
            # Store embedding as JSON string (will convert to vector later)
            embedding_json = json.dumps(embedding)
            AssistantMemory.objects.create(
                content=chunk,
                embedding=embedding_json,
                type='knowledge'
            )
            print(f"Processed chunk {i}/{len(chunks)}")
        except Exception as e:
            print(f"Error processing chunk {i}: {str(e)}")
            continue
    
    print(f"Successfully ingested {len(chunks)} chunks into the knowledge base.")


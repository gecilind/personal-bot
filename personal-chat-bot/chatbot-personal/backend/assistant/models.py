from django.db import models
# Temporarily using TextField instead of VectorField until pgvector is installed
# from pgvector.django import VectorField


class AssistantMemory(models.Model):
    MEMORY_TYPE_CHOICES = [
        ('knowledge', 'Knowledge'),
        ('memory', 'Memory'),
    ]
    
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    embedding = models.TextField(null=True, blank=True)  # Temporary: store as JSON string
    # embedding = VectorField(dimensions=1536, null=True, blank=True)  # Will use this when pgvector is ready
    type = models.CharField(max_length=20, choices=MEMORY_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assistant_memory'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.type}: {self.content[:50]}..."


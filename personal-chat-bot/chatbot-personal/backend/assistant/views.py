from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from assistant.serializers import (
    ChatRequestSerializer, 
    ChatResponseSerializer, 
    MemorySerializer
)
from assistant.services.llm import generate_response
from assistant.models import AssistantMemory


@api_view(['POST'])
def chat(request):
    """
    POST /api/chat/
    Send a message to the AI assistant.
    """
    serializer = ChatRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        result = generate_response(serializer.validated_data['message'])
        response_serializer = ChatResponseSerializer(result)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_memory(request):
    """
    GET /api/memory/
    Retrieve stored memories.
    """
    memories = AssistantMemory.objects.all().order_by('-created_at')[:50]
    serializer = MemorySerializer(memories, many=True)
    return Response({'memories': serializer.data}, status=status.HTTP_200_OK)


@ensure_csrf_cookie
def chat_view(request):
    """
    Render the chat interface.
    """
    return render(request, 'chat.html')

